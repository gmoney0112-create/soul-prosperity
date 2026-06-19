#!/usr/bin/env python3
"""
Soul Prosperity — GHL Deploy Script
Runs against the GHL v2 API to:
  1. Test connection
  2. Create quiz_result custom field
  3. Print all 20 sequence emails formatted for copy-paste into GHL
  4. Print workflow blueprint and FastPayDirect checklist

Usage:
  python3 docs/ghl-deploy.py

Credentials loaded from .env in project root (never committed).
"""

import json
import os
import sys
import urllib.request
import urllib.error

# Force UTF-8 output on Windows so unicode characters render correctly
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Load credentials ──────────────────────────────────────────────────────────
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    env = {}
    try:
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    loc = env.get("GHL_LOCATION_ID") or os.environ.get("GHL_LOCATION_ID", "")
    pit = env.get("GHL_PIT_KEY") or os.environ.get("GHL_PIT_KEY", "")
    if not loc or not pit:
        print("ERROR: GHL_LOCATION_ID and GHL_PIT_KEY must be set in .env or environment.")
        sys.exit(1)
    return loc, pit


# ── GHL API helpers ───────────────────────────────────────────────────────────
BASE = "https://services.leadconnectorhq.com"

def ghl_request(method, path, pit, body=None):
    url = BASE + path
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {pit}")
    req.add_header("Version", "2021-07-28")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        return e.code, {"error": body_text}
    except Exception as e:
        return 0, {"error": str(e)}


def step(label):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print('='*60)


def ok(msg):  print(f"  [OK]   {msg}")
def fail(msg): print(f"  [FAIL] {msg}")
def info(msg): print(f"  [INFO] {msg}")


# ── Step 1: Connection test ───────────────────────────────────────────────────
def test_connection(loc, pit):
    step("STEP 1 — Test GHL Connection")
    status, resp = ghl_request("GET", f"/locations/{loc}", pit)
    if status == 200:
        name = resp.get("location", {}).get("name", "(unknown)")
        ok(f"Connected to sub-account: {name}")
        return True
    else:
        fail(f"HTTP {status}: {resp.get('error', resp)}")
        info("Check that your PIT key has Location access scope.")
        return False


# ── Step 2: Create quiz_result custom field ───────────────────────────────────
def create_custom_field(loc, pit):
    step("STEP 2 — Create quiz_result Custom Field")

    # Check if it already exists
    status, resp = ghl_request("GET", f"/locations/{loc}/customFields", pit)
    if status == 200:
        fields = resp.get("customFields", [])
        for f in fields:
            if f.get("fieldKey", "").endswith("quiz_result") or f.get("name", "").lower() == "quiz result":
                ok(f"quiz_result already exists (id={f.get('id')}) — skipping creation")
                return f.get("id")

    payload = {
        "name": "Quiz Result",
        "dataType": "TEXT",
        "fieldKey": "quiz_result",
        "placeholder": "seedling | builder | operator | scaler",
        "position": 0,
    }
    status, resp = ghl_request("POST", f"/locations/{loc}/customFields", pit, payload)
    if status in (200, 201):
        field_id = resp.get("customField", {}).get("id") or resp.get("id", "")
        ok(f"Created quiz_result custom field (id={field_id})")
        return field_id
    else:
        fail(f"HTTP {status}: {resp.get('error', resp)}")
        info("You may need to create this manually: GHL → Settings → Custom Fields → Contacts → + New Field")
        info("  Name: Quiz Result | Key: quiz_result | Type: Text")
        return None


# ── Email content ─────────────────────────────────────────────────────────────
SEQUENCES = [
    {
        "name": "SP — Kingdom Seedling Sequence",
        "persona": "Kingdom Seedling",
        "emails": [
            {
                "day": 0,
                "subject": "Your Kingdom Stage result is inside, {{contact.firstName}}",
                "preview": "You're a Kingdom Seedling — here's what that actually means",
                "body": """Hey {{contact.firstName}},

You just took the Kingdom Business Assessment and your result is in.

You're a Kingdom Seedling.

That means you have the vision, the faith, and the hunger — but you're still figuring out how to turn that into a real business that pays you.

Here's the truth nobody told you: the people making money from their stories had the same doubts you have right now. They just started anyway.

Habakkuk 2:2 says "Write the vision and make it plain."

It didn't say "only if you have everything figured out."

Your first move is simpler than you think:

→ Get the eBook: How to Write a 40-Page eBook (Even If You've Never Written a Grocery List)

This is the exact framework that shows you how to take what's already in your head — your story, your lessons, your faith — and turn it into a product someone will pay for this week.

[GET THE EBOOK FOR $7]
https://link.fastpaydirect.com/payment-link/69ef5c807dd3512d9207b2a2

Your story is worth more than you know. Let's start there.

— Terrance
Soul Prosperity Group

P.S. The eBook is 40 pages and reads in under 2 hours. By the time you're done you'll have your 12 chapter titles written. That's your whole book in one sitting."""
            },
            {
                "day": 1,
                "subject": "The real reason you haven't started yet",
                "preview": "It's not what you think",
                "body": """Hey {{contact.firstName}},

I want to ask you something real.

What are you actually waiting for?

Most Kingdom Seedlings say they're waiting to "be ready." But ready is a feeling that never fully arrives. The people who build something don't wait for ready — they start with what they have and figure the rest out in motion.

Paul wrote his most powerful letters from prison. No laptop. No WiFi. No publisher. Just a message he couldn't keep inside.

You have more resources than Paul had. And you still have something to say.

The block isn't ability. It's the absence of a starting point.

That's exactly what the eBook framework gives you — a 12-chapter structure that removes the blank page completely. You don't write Chapter 1. You write 12 titles first. That's your whole book in 20 minutes.

[GET THE $7 EBOOK AND START TODAY]
https://link.fastpaydirect.com/payment-link/69ef5c807dd3512d9207b2a2

Let's go.

— Terrance"""
            },
            {
                "day": 3,
                "subject": "What happened when I hit publish for the first time",
                "preview": "It wasn't perfect. It worked anyway.",
                "body": """Hey {{contact.firstName}},

The first thing I ever published wasn't great.

The cover was basic. The writing wasn't polished. There were probably typos.

I hit publish anyway.

And something happened that I didn't expect: people bought it. Not because it was perfect — but because it was real. Because it was mine. Because somebody needed exactly what I had been through.

That's the thing about your story. It doesn't have to be perfect to be powerful. It just has to be honest.

The eBook framework I use has one rule: write how you talk. Not how you think a "real author" sounds. Not how your English teacher wanted. Just you.

That's what converts. That's what people share. That's what gets screenshotted and posted on Instagram at 1am.

Your first product doesn't have to be your best product. It just has to exist.

[GET THE EBOOK — $7]
https://link.fastpaydirect.com/payment-link/69ef5c807dd3512d9207b2a2

— Terrance

P.S. If you've been sitting on this since Monday, today's the day. Proverbs 21:5 — the plans of the diligent lead to abundance. The keyword is diligent — not perfect."""
            },
            {
                "day": 5,
                "subject": "Ready to go deeper? (upgrade option inside)",
                "preview": "One step up from the eBook",
                "body": """Hey {{contact.firstName}},

Quick one today.

If you've been reading these emails and thinking "I get it, I just need to actually do it" — the eBook is your next step.

But if you're the kind of person who learns better by listening — on the job, in the truck, between calls — then the Audiobook Bundle was made for you.

It's the full eBook + the complete audiobook version. So you can read it at night and listen while you work during the day.

Same framework. Two ways to absorb it. $17 total.

[GET THE AUDIOBOOK BUNDLE — $17]
https://link.fastpaydirect.com/payment-link/69ef5e77557558e89e524ca3

Or if you're starting with the eBook:
[GET THE EBOOK — $7]
https://link.fastpaydirect.com/payment-link/69ef5c807dd3512d9207b2a2

Either way — start something this week.

— Terrance"""
            },
            {
                "day": 7,
                "subject": "Last call, {{contact.firstName}}",
                "preview": "This is the one that changes the trajectory",
                "body": """Hey {{contact.firstName}},

This is my last email in this sequence — so I'll be straight with you.

Seven days ago you took the Kingdom Business Assessment. You found out you're a Kingdom Seedling. You got 4 emails from me.

And if you haven't started yet, I get it. Life is busy. The grind is real. There's always something more urgent.

But here's what I know: the people who are still in the same spot a year from now are the ones who kept waiting. And the people who changed their trajectory — they made one decision and moved.

This is that moment.

The eBook is $7. That's less than lunch. And it gives you the complete framework to build your first digital product — from idea to published — using the story you already have.

[GET THE EBOOK FOR $7 — FINAL REMINDER]
https://link.fastpaydirect.com/payment-link/69ef5c807dd3512d9207b2a2

Want the community too? Join Money Masters Academy free for 7 days:
https://skool.com/money-masters-academy-5443/about

I'm rooting for you.

— Terrance Gee
Soul Prosperity Group

"Write the vision and make it plain." — Habakkuk 2:2"""
            },
        ]
    },
    {
        "name": "SP — Grinding Builder Sequence",
        "persona": "Grinding Builder",
        "emails": [
            {
                "day": 0,
                "subject": "Your result: The Grinding Builder — here's what that means",
                "preview": "You've proven it works. Now let's make it work without you.",
                "body": """Hey {{contact.firstName}},

Your Kingdom Business Assessment result is in.

You're a Grinding Builder.

That means you've already proven this works. You've made money from something you built. You know it's possible.

But it's inconsistent. Every week feels like starting over. Income goes up, then it dips. You're still doing everything manually, and you're tired.

Here's the real issue: you have a product, but you don't have a system yet.

The framework that fixes this is the eBook + Audiobook Bundle — built specifically for builders who are moving but need their income to start moving on its own.

[GET THE AUDIOBOOK BUNDLE — $17]
https://link.fastpaydirect.com/payment-link/69ef5e77557558e89e524ca3

Read the eBook at night. Listen to the audiobook in the truck, on the job, between calls. Two formats. One framework. Everything you need to build the system your grind deserves.

— Terrance
Soul Prosperity Group"""
            },
            {
                "day": 1,
                "subject": "The grind is honorable. But God didn't call you to be exhausted.",
                "preview": "Proverbs 21:5 hits different when you're in it",
                "body": """Hey {{contact.firstName}},

Proverbs 21:5 — "The plans of the diligent lead surely to abundance."

Notice what it says: the PLANS of the diligent. Not just the hustle. The plans.

You can be the hardest working person in your field and still not build wealth — if you don't have a system behind the effort. The grind earns the income. The system multiplies it.

Right now you're grinding without a multiplier.

The fix is a repeatable offer with automated delivery. Something that sells while you're working, sleeping, or at church on Sunday.

The Audiobook Bundle walks you through exactly how to build that — using the story and knowledge you already have. No tech degree required. No huge budget. Just a framework and the willingness to execute it.

[GET THE BUNDLE — $17]
https://link.fastpaydirect.com/payment-link/69ef5e77557558e89e524ca3

— Terrance"""
            },
            {
                "day": 3,
                "subject": "What does $3K/month actually look like for a builder?",
                "preview": "The math might surprise you",
                "body": """Hey {{contact.firstName}},

Let me show you what $3,000/month actually breaks down to.

$7 eBook: you need 429 buyers/month → about 14 per day
$17 bundle: you need 177 buyers/month → about 6 per day
$67 course: you need 45 buyers/month → about 1-2 per day

Six people per day finding your $17 bundle. That's it.

Not 6,000 followers. Not a viral TikTok. Not a massive email list.

Six people a day who need exactly what you went through and are willing to pay $17 to learn from it.

That's achievable. That's realistic. And it starts with having the product built and the system in place to sell it automatically.

The Audiobook Bundle gives you the framework to build that product this week.

[BUILD THE PRODUCT — $17 BUNDLE]
https://link.fastpaydirect.com/payment-link/69ef5e77557558e89e524ca3

— Terrance"""
            },
            {
                "day": 5,
                "subject": "Ready to add the physical copy? (upgrade inside)",
                "preview": "The paperback turns your product into a physical legacy",
                "body": """Hey {{contact.firstName}},

Quick one today.

If you're ready to go all in — the Paperback Bundle includes the eBook, audiobook, AND the physical paperback copy.

Why does the physical copy matter?

Because a paperback on someone's shelf is a reminder that you exist. It gets passed around. It gets recommended. It sits on a desk in front of someone for months.

Digital products get downloaded and forgotten. Physical products stick.

[UPGRADE TO THE PAPERBACK BUNDLE — $27]
https://link.fastpaydirect.com/payment-link/69ef5ed97dd3512d9207b2a6

Or start with the audiobook bundle:
[GET THE $17 BUNDLE]
https://link.fastpaydirect.com/payment-link/69ef5e77557558e89e524ca3

— Terrance"""
            },
            {
                "day": 7,
                "subject": "{{contact.firstName}}, one more thing before I go",
                "preview": "The community changes the game at your stage",
                "body": """Hey {{contact.firstName}},

Last email from this sequence.

You're a Grinding Builder. You've proven you can make money. What you need now is the system to make it consistent — and accountability to actually build it.

That's what the Money Masters Academy Skool community is for.

Live monthly coaching calls. Real operators who are building in the same space you are. A place to ask questions and get answers from people who have already figured out the piece you're stuck on.

First 7 days are free.

[TRY SKOOL FREE FOR 7 DAYS]
https://skool.com/money-masters-academy-5443/about

And if you haven't grabbed the bundle yet:
[GET THE $17 AUDIOBOOK BUNDLE]
https://link.fastpaydirect.com/payment-link/69ef5e77557558e89e524ca3

Let's build something that multiplies.

— Terrance
"The plans of the diligent lead surely to abundance." — Proverbs 21:5"""
            },
        ]
    },
    {
        "name": "SP — Kingdom Operator Sequence",
        "persona": "Kingdom Operator",
        "emails": [
            {
                "day": 0,
                "subject": "Your result: Kingdom Operator — and what's really blocking you",
                "preview": "You're not missing hustle. You're missing architecture.",
                "body": """Hey {{contact.firstName}},

Your Kingdom Business Assessment result is in.

You're a Kingdom Operator.

That means you're running a real business. Real revenue. Real customers. Real problems that only the owner — you — can solve.

And that's exactly the issue.

You've built a business that depends on your presence. The moment you step away, things slow down. That's not a business — that's a high-paying job.

The fix isn't working harder. It's building Kingdom Systems that run under God's order, not just your energy.

The Online Course Bundle is built for exactly where you are: you get the full eBook + audiobook + paperback + complete Modern eBook Blueprint Mastery video course — everything you need to architect a business that runs without you.

[GET THE COURSE BUNDLE — $67]
https://link.fastpaydirect.com/payment-link/69ef5fc0557558e89e524ca5

Proverbs 16:3 — "Commit your work to the LORD, and your plans will be established."

Commit the architecture. Build the system. Let God multiply it.

— Terrance
Soul Prosperity Group"""
            },
            {
                "day": 1,
                "subject": "What \"systems\" actually means for a blue-collar operator",
                "preview": "It's not robots. It's repeatable decisions.",
                "body": """Hey {{contact.firstName}},

When most people hear "systems" they think of complex tech stacks and engineers. That's not what this is.

A system is a repeatable decision you make once that runs without you making it again.

Your quiz funnel is a system — someone finds it, takes the quiz, gets a result, receives an email sequence, and moves toward a purchase. You set it up once. It runs while you work.

Your GHL follow-up is a system. Your checkout page is a system. Your onboarding email is a system.

At the Operator stage, your job is to find every place where YOU are the system — and replace yourself with a process.

The Modern eBook Blueprint Mastery course inside the Course Bundle walks you through exactly that. GHL workflows, quiz funnels, automated follow-up, client systems — all of it.

[GET THE COURSE BUNDLE — $67]
https://link.fastpaydirect.com/payment-link/69ef5fc0557558e89e524ca5

— Terrance"""
            },
            {
                "day": 3,
                "subject": "The real cost of being the bottleneck",
                "preview": "It's not just your time. It's your ceiling.",
                "body": """Hey {{contact.firstName}},

Here's a question worth sitting with:

If you took a full week off — completely disconnected — what would happen to your revenue?

If the honest answer is "it would drop significantly" — you're the bottleneck. And your current revenue is your ceiling, not your floor.

The operators who break through $10K/month consistently have one thing in common: they built systems before they felt ready to build them. They automated the repetitive decisions before the business demanded it.

That's what the Course Bundle gives you — a 30-day implementation roadmap so you're not just learning systems in theory, you're building your actual business infrastructure in real time.

[GET THE COURSE BUNDLE — $67]
https://link.fastpaydirect.com/payment-link/69ef5fc0557558e89e524ca5

Lifetime access. Every future update included.

— Terrance"""
            },
            {
                "day": 5,
                "subject": "The community is where operators like you scale",
                "preview": "You've outgrown learning alone",
                "body": """Hey {{contact.firstName}},

At the Operator stage, the fastest path to your next level is other operators who are already there.

Not inspiration content. Not YouTube tutorials. Real people who have already solved the exact problem you're facing and can tell you what they did.

That's the Money Masters Academy. Live monthly coaching calls with me. A private community of Christian business owners who operate at your level. The full Kingdom Systems curriculum inside.

First 7 days free.

[TRY SKOOL FREE]
https://skool.com/money-masters-academy-5443/about

And if you're ready for the full infrastructure:
[GET THE COURSE BUNDLE — $67]
https://link.fastpaydirect.com/payment-link/69ef5fc0557558e89e524ca5

— Terrance"""
            },
            {
                "day": 7,
                "subject": "Last one — the choice operators make",
                "preview": "The next level requires a decision, not more information",
                "body": """Hey {{contact.firstName}},

Last email.

You're a Kingdom Operator. You already know more than enough to build something great. The gap isn't information — it's architecture and execution.

Here's the choice that separates operators who scale from those who plateau:

Operators who scale invest in the infrastructure before the revenue demands it. They build the system while the business is still manageable.

Operators who plateau wait until they're overwhelmed — and by then they're too busy to build anything.

You're at that decision point right now.

[GET THE COURSE BUNDLE — $67]
https://link.fastpaydirect.com/payment-link/69ef5fc0557558e89e524ca5

[OR JOIN SKOOL FREE FOR 7 DAYS]
https://skool.com/money-masters-academy-5443/about

"Commit your work to the LORD, and your plans will be established." — Proverbs 16:3

— Terrance Gee
Soul Prosperity Group"""
            },
        ]
    },
    {
        "name": "SP — Kingdom Scaler Sequence",
        "persona": "Kingdom Scaler",
        "emails": [
            {
                "day": 0,
                "subject": "Your result: Kingdom Scaler — welcome to your level",
                "preview": "You're not building a business anymore. You're building a legacy.",
                "body": """Hey {{contact.firstName}},

Your Kingdom Business Assessment result is in.

You're a Kingdom Scaler.

That means you've already done the hard part. You've generated real income. You've survived the hard seasons. You know this works.

What you need now isn't another course. You need a community of operators who think at your level — and the systems to break through your next ceiling.

That's the Money Masters Academy.

Live monthly coaching calls. A private Skool community of blue-collar Christian business owners who are building at scale. The complete Kingdom Systems curriculum. Accountability partners who actually understand the grind and the faith behind it.

First 7 days are completely free.

[START YOUR FREE 7-DAY TRIAL]
https://skool.com/money-masters-academy-5443/about

"For I know the plans I have for you, declares the LORD, plans to prosper you and not to harm you, plans to give you a future and a hope." — Jeremiah 29:11

— Terrance
Soul Prosperity Group"""
            },
            {
                "day": 1,
                "subject": "The #1 thing that limits Kingdom Scalers",
                "preview": "It's not strategy. It's isolation.",
                "body": """Hey {{contact.firstName}},

I've worked with a lot of people at your stage.

And the #1 thing that limits scalers isn't strategy or money or time.

It's isolation.

You've outgrown your current peer group. The people around you are operating at a different level — and as much as they support you, they can't challenge your thinking at the level you need.

The next ceiling only breaks when you're in a room — physical or digital — with people who have already broken through it.

That's what the community is for.

[JOIN THE COMMUNITY — 7 DAYS FREE]
https://skool.com/money-masters-academy-5443/about

You belong at the table. Come find your seat.

— Terrance"""
            },
            {
                "day": 3,
                "subject": "What legacy actually looks like at your stage",
                "preview": "It's not about the money anymore — or is it?",
                "body": """Hey {{contact.firstName}},

At the Scaler stage, something shifts.

You stop thinking about survival and start thinking about significance. Not just "can I pay my bills" but "what does this become in 10 years?"

That's the Kingdom mindset. And it's exactly where the conversation inside Money Masters Academy lives.

We talk about recurring revenue models. We talk about building something that runs without the founder. We talk about what it means to leave a legacy that outlives your involvement.

Paul's letters are still being read 2,000 years later. That's legacy. Your business, built right, can outlive you too.

[JOIN THE COMMUNITY]
https://skool.com/money-masters-academy-5443/about

Or if you're ready to go all in — Lifetime Access is $497 (no monthly fees, ever):
https://link.fastpaydirect.com/payment-link/69ef60c87dd3512d9207b2ac

— Terrance"""
            },
            {
                "day": 5,
                "subject": "Annual or Lifetime — the math inside",
                "preview": "One of these is obviously better",
                "body": """Hey {{contact.firstName}},

Quick breakdown for the Kingdom Scaler who's already decided they're in:

Monthly: $47/month → $564/year
Annual: $247/year → saves you $317
Lifetime: $497 once → pays for itself in less than 11 months, free forever after

If you're planning to stay in the community for more than a year — and I hope you are — Lifetime is the obvious play.

[GET LIFETIME ACCESS — $497]
https://link.fastpaydirect.com/payment-link/69ef60c87dd3512d9207b2ac

[OR START FREE FOR 7 DAYS]
https://skool.com/money-masters-academy-5443/about

Either way, get in. The community is where the real work happens.

— Terrance"""
            },
            {
                "day": 7,
                "subject": "{{contact.firstName}} — your free trial ends soon",
                "preview": "Here's what you'll lose access to",
                "body": """Hey {{contact.firstName}},

Your 7-day free trial in Money Masters Academy ends soon.

Here's what you'll lose access to if you don't upgrade:

* Monthly live coaching calls with me
* The full Kingdom Systems curriculum
* The private community of Christian business owners at your level
* Accountability partners who are building in the same space

To continue: simply upgrade inside Skool before your trial ends.

Monthly ($47): upgrade inside the Skool app
Annual ($247): upgrade inside the Skool app
Lifetime ($497 — best value):
https://link.fastpaydirect.com/payment-link/69ef60c87dd3512d9207b2ac

If you haven't joined the trial yet, today is the day:
https://skool.com/money-masters-academy-5443/about

"For I know the plans I have for you." — Jeremiah 29:11

God's plan for you doesn't have an expiration date. Neither does mine.

— Terrance Gee
Soul Prosperity Group"""
            },
        ]
    },
]


# ── Step 3: Print all emails ──────────────────────────────────────────────────
def print_email_sequences():
    step("STEP 3 — Email Sequence Copy (paste into GHL)")
    print("""
  GHL Navigation: Automation → Email Marketing → Campaigns → + New Campaign
  OR: Automation → Sequences → + New Sequence
  Sender for ALL emails: Terrance | Soul Prosperity  /  terrance@inspirebuildmotivate.com
""")
    for seq in SEQUENCES:
        print(f"\n{'-'*60}")
        print(f"  SEQUENCE: {seq['name']}")
        print(f"  Persona:  {seq['persona']}")
        print(f"{'='*60}")
        for i, email in enumerate(seq["emails"], 1):
            d = email['day']
            delay = "(send immediately)" if d == 0 else f"(wait {d} day{'s' if d > 1 else ''})"
            print(f"\n  -- Email {i} of 5 | Day {d} {delay}")
            print(f"  Subject:  {email['subject']}")
            print(f"  Preview:  {email['preview']}")
            print(f"\n  Body:\n")
            for line in email["body"].split("\n"):
                print(f"    {line}")
            print()


# ── Step 4: Print workflow blueprint ─────────────────────────────────────────
def print_workflow_blueprint():
    step("STEP 4 — GHL Workflow Blueprint (build manually in UI)")
    print("""
  GHL Navigation: Automation → Workflows → + New Workflow → Start from Scratch
  Workflow Name: Soul Prosperity — Quiz Funnel Lead Router
  Status: Published/Active

  TRIGGER: Inbound Webhook
  ---------------------------------------------------------
  ACTION 1: Create or Update Contact
    - First Name  <- {{trigger.firstName}}
    - Email       <- {{trigger.email}}

  ACTION 2: Update Contact Field
    - Field: quiz_result
    - Value: {{trigger.quizResult}}

  ACTION 3: Add Tag
    - Tag: quiz-funnel-lead

  ACTION 4: If/Else Branch (4 branches)
    [BRANCH 1] quiz_result = "seedling"
        Add Tag: quiz-seedling
        Enroll:  SP -- Kingdom Seedling Sequence

    [BRANCH 2] quiz_result = "builder"
        Add Tag: quiz-builder
        Enroll:  SP -- Grinding Builder Sequence

    [BRANCH 3] quiz_result = "operator"
        Add Tag: quiz-operator
        Enroll:  SP -- Kingdom Operator Sequence

    [BRANCH 4] quiz_result = "scaler"
        Add Tag: quiz-scaler
        Enroll:  SP -- Kingdom Scaler Sequence

    [ELSE fallback]
        Add Tag: quiz-no-result
        Enroll:  SP -- Kingdom Seedling Sequence
""")


# ── Step 5: Print FastPayDirect checklist ─────────────────────────────────────
def print_fastpaydirect_checklist():
    step("STEP 5 — FastPayDirect Redirect Checklist (manual)")
    print("""
  Login: https://app.fastpaydirect.com
  For each link: Edit → Success/Redirect URL → paste → Save

  $7   link (ID: ...9207b2a2)  → https://gmoney0112-create.github.io/soul-prosperity-quiz-all-in-one/thank-you.html?tier=7
  $17  link (ID: ...e524ca3)   → https://gmoney0112-create.github.io/soul-prosperity-quiz-all-in-one/thank-you.html?tier=17
  $27  link (ID: ...9207b2a6)  → https://gmoney0112-create.github.io/soul-prosperity-quiz-all-in-one/thank-you.html?tier=27
  $67  link (ID: ...e524ca5)   → https://gmoney0112-create.github.io/soul-prosperity-quiz-all-in-one/thank-you.html?tier=67
  $97  link (ID: ...1e7e8747)  → https://gmoney0112-create.github.io/soul-prosperity-quiz-all-in-one/thank-you.html?tier=97
  $497 link (ID: ...9207b2ac)  → https://gmoney0112-create.github.io/soul-prosperity-quiz-all-in-one/thank-you.html?tier=497

  NOTE: The Starter Stack ($47, Stripe link) also needs a success redirect
  once you create a FastPayDirect link for it:
  → https://gmoney0112-create.github.io/soul-prosperity-quiz-all-in-one/thank-you.html?tier=47
""")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    loc, pit = load_env()
    print(f"\nSoul Prosperity — GHL Deploy")
    print(f"Location ID: {loc}")
    print(f"PIT Key:     {pit[:12]}...")

    connected = test_connection(loc, pit)
    if not connected:
        print("\n  Cannot connect to GHL. Continuing with offline output...\n")

    create_custom_field(loc, pit)
    print_email_sequences()
    print_workflow_blueprint()
    print_fastpaydirect_checklist()

    step("DONE")
    print("""
  API tasks complete. Remaining manual steps:
  1. Build 4 sequences in GHL using the email copy above (~45 min)
  2. Build the Quiz Funnel Lead Router workflow using the blueprint above (~20 min)
  3. Set 6 FastPayDirect redirect URLs (~8 min)

  Total: ~75 min to full revenue loop.
""")


if __name__ == "__main__":
    main()
