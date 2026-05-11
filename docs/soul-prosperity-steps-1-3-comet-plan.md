# Soul Prosperity — Autonomous Execution Plan
## Steps 1–3: GHL Email Sequences + Webhook Workflow + FastPayDirect Redirects
### Comet Browser Assistant Handoff Document
**Version:** 1.0 | **Date:** 2026-05-09 | **Operator:** Terrance Gee / Soul Prosperity Group

---

## CRITICAL CONTEXT — READ BEFORE EXECUTING

- **GHL Sub-Account:** Soul Prosperity Group
- **GHL Location ID:** `gbUy4Z0Ug5dziTftbJNP`
- **GHL API Key:** `pit-c044f21a-01ea-4fd7-b16c-9ad7a0cb135a`
- **GHL Webhook URL:** `https://services.leadconnectorhq.com/hooks/ucphPUkSafuQF0ZCZh1T/webhook-trigger/54531478-e2bc-406b-9500-35242e28e4ff`
- **Meta Pixel ID:** `1655287592408855`
- **Skool Community:** `https://skool.com/money-masters-academy-5443/about`
- **GHL Login URL:** `https://app.gohighlevel.com`
- **FastPayDirect Login URL:** `https://app.fastpaydirect.com`

### Quiz Result Profile Values (used for branching)
| Value | Persona | Entry Offer | Price |
|-------|---------|-------------|-------|
| `seedling` | Kingdom Seedling | eBook | $7 |
| `builder` | Grinding Builder | Audiobook Bundle | $17 |
| `operator` | Kingdom Operator | Course Bundle | $67 |
| `scaler` | Kingdom Scaler | Skool Trial | Free |

### FastPayDirect Payment Links
| Product | Price | URL |
|---------|-------|-----|
| eBook | $7 | `https://link.fastpaydirect.com/payment-link/69ef5c807dd3512d9207b2a2` |
| Audiobook Bundle | $17 | `https://link.fastpaydirect.com/payment-link/69ef5e77557558e89e524ca3` |
| Paperback Bundle | $27 | `https://link.fastpaydirect.com/payment-link/69ef5ed97dd3512d9207b2a6` |
| Course Bundle | $67 | `https://link.fastpaydirect.com/payment-link/69ef5fc0557558e89e524ca5` |
| Lifetime Access | $497 | `https://link.fastpaydirect.com/payment-link/69ef60c87dd3512d9207b2ac` |
| AI System Upsell | $97 | `https://link.fastpaydirect.com/payment-link/69fe563e34d67b041e7e8747` |

### Thank-You Page URL
`https://gmoney0112-create.github.io/soul-prosperity-quiz-all-in-one/thank-you.html?tier=[TIER]`

---

## EXECUTION ORDER

```
STEP 3 → STEP 2 → STEP 1
```

Run in this order. Step 3 (FastPayDirect redirects) is fastest and fully independent. Step 2 (GHL Workflow) must exist before Step 1 (email sequences) so sequences have a workflow to live inside.

---

## ═══════════════════════════════════════
## STEP 3: FastPayDirect — Set Success Redirect URLs
## Estimated time: 8–12 minutes
## ═══════════════════════════════════════

### Objective
Set the post-purchase redirect URL on all 6 FastPayDirect payment links so buyers land on the thank-you page after completing payment.

### Target URLs — one per link (tier parameter required for Pixel tracking)
```
$7   → https://gmoney0112-create.github.io/soul-prosperity-quiz-all-in-one/thank-you.html?tier=7
$17  → https://gmoney0112-create.github.io/soul-prosperity-quiz-all-in-one/thank-you.html?tier=17
$27  → https://gmoney0112-create.github.io/soul-prosperity-quiz-all-in-one/thank-you.html?tier=27
$67  → https://gmoney0112-create.github.io/soul-prosperity-quiz-all-in-one/thank-you.html?tier=67
$97  → https://gmoney0112-create.github.io/soul-prosperity-quiz-all-in-one/thank-you.html?tier=97
$497 → https://gmoney0112-create.github.io/soul-prosperity-quiz-all-in-one/thank-you.html?tier=497
```
**Why the ?tier= parameter matters:** The thank-you page reads this value to fire `fbq('track', 'Purchase', { value: X })` with the correct dollar amount. Without it, Meta records a $0 purchase and ROAS data is useless.

### Execution Instructions

**3.1 — Log In**
1. Navigate to `https://app.fastpaydirect.com`
2. Log in with Terrance's credentials
3. Wait for dashboard to fully load

**3.2 — For each payment link below, repeat this process:**

```
LINK ORDER:
1. $7 eBook        → ID ending: 9207b2a2
2. $17 Bundle      → ID ending: e524ca3
3. $27 Paperback   → ID ending: 9207b2a6
4. $67 Course      → ID ending: e524ca5
5. $497 Lifetime   → ID ending: 9207b2ac
6. $97 AI System   → ID ending: 1e7e8747
```

**For each link:**
1. Navigate to Payment Links section
2. Find the link by name or price
3. Click Edit / Settings / Configure (UI label may vary)
4. Locate the field labeled: `Success URL`, `Redirect URL`, `After Payment URL`, or `Confirmation URL`
5. Clear existing value if any
6. Paste the URL for that specific link's tier (see Target URLs table above) — e.g. `thank-you.html?tier=7` for the $7 link
7. Save / Update
8. Confirm save was successful (look for success toast or confirmation message)
9. Move to next link

**3.3 — Verification**
After all 6 links are updated:
- Open any 1 payment link in a new tab
- Verify the redirect URL is saved correctly in the settings
- Log "STEP 3 COMPLETE" in your output

### Error Handling
- If a field is not visible, look under "Advanced Settings" or "Customization"
- If save fails, refresh and retry once
- If a link cannot be found, skip and log which one was missed

---

## ═══════════════════════════════════════
## STEP 2: GHL — Build the Webhook Receiver Workflow
## Estimated time: 15–20 minutes
## ═══════════════════════════════════════

### Objective
Build a single GHL automation workflow that:
1. Receives the quiz funnel webhook payload
2. Creates or updates the contact
3. Tags them with their quiz result
4. Branches by `quizResult` value
5. Enrolls them in the matching email sequence (built in Step 1)

### Pre-Check
Before building: confirm the custom field `quiz_result` exists in GHL.
- Go to: Settings → Custom Fields → Contacts
- If `quiz_result` does not exist: create it as a Text field, label "Quiz Result"

### Execution Instructions

**2.1 — Log In to GHL**
1. Navigate to `https://app.gohighlevel.com`
2. Log in and select the **Soul Prosperity Group** sub-account
3. Go to: **Automation → Workflows → + New Workflow**
4. Select: **Start from Scratch**
5. Name the workflow: `Soul Prosperity — Quiz Funnel Lead Router`
6. Set status to **Draft** (do not publish yet)

**2.2 — Set the Trigger**
1. Click **Add Trigger**
2. Select: **Inbound Webhook**
3. GHL will display a webhook URL — this is for reference only, the quiz pages already have the correct URL hardcoded
4. Save the trigger

**2.3 — Add Action: Create/Update Contact**
1. Click **+ Add Action**
2. Select: **Create or Update Contact**
3. Map fields:
   - First Name ← `{{contact.firstName}}` or webhook field `firstName`
   - Email ← `{{contact.email}}` or webhook field `email`
4. Save action

**2.4 — Add Action: Set Custom Field**
1. Click **+ Add Action**
2. Select: **Update Contact Field** or **Set Field Value**
3. Field: `quiz_result`
4. Value: `{{trigger.quizResult}}` (the webhook payload field)
5. Save action

**2.5 — Add Action: Add Tag**
1. Click **+ Add Action**
2. Select: **Add Tag**
3. Tag value: `quiz-funnel-lead`
4. Save action

**2.6 — Add Action: If/Else Branch**
1. Click **+ Add Action**
2. Select: **If/Else** or **Conditional Branch**
3. Build 4 branches using the condition: `quiz_result` equals each value

```
BRANCH 1: quiz_result = "seedling"
  → Action: Add Tag: quiz-seedling
  → Action: Enroll in sequence: "SP — Kingdom Seedling Sequence" (built in Step 1)

BRANCH 2: quiz_result = "builder"
  → Action: Add Tag: quiz-builder
  → Action: Enroll in sequence: "SP — Grinding Builder Sequence" (built in Step 1)

BRANCH 3: quiz_result = "operator"
  → Action: Add Tag: quiz-operator
  → Action: Enroll in sequence: "SP — Kingdom Operator Sequence" (built in Step 1)

BRANCH 4: quiz_result = "scaler"
  → Action: Add Tag: quiz-scaler
  → Action: Enroll in sequence: "SP — Kingdom Scaler Sequence" (built in Step 1)

ELSE (fallback):
  → Action: Add Tag: quiz-no-result
  → Action: Enroll in sequence: "SP — Kingdom Seedling Sequence" (default)
```

**2.7 — Publish the Workflow**
1. Click **Save**
2. Toggle status from Draft to **Published / Active**
3. Confirm activation

**2.8 — Test the Workflow**
1. Go to the quiz funnel: `https://gmoney0112-create.github.io/soul-prosperity-quiz-funnel/`
2. Enter test name: `Comet Test` and test email: `test+comet@soulprosperity.com`
3. Complete all 6 questions
4. Return to GHL → Contacts → search for the test email
5. Confirm: contact was created, `quiz_result` field is populated, correct tag applied
6. Log "STEP 2 COMPLETE" in your output

### Error Handling
- If the webhook trigger doesn't appear: search for "Webhook" or "Custom Webhook" in trigger list
- If field mapping fails: use `{{trigger.body.firstName}}` and `{{trigger.body.email}}` syntax
- If sequences are not yet available in the branch actions: create placeholder sequences named correctly and come back after Step 1

---

## ═══════════════════════════════════════
## STEP 1: GHL — Build 4 Email Sequences (20 Emails Total)
## Estimated time: 45–60 minutes
## ═══════════════════════════════════════

### Objective
Build 4 persona-specific 5-email nurture sequences inside GHL. Each sequence is triggered by the workflow built in Step 2 and delivers personalized content matching the lead's quiz result.

### Sender Settings (apply to ALL emails)
- **From Name:** Terrance | Soul Prosperity
- **From Email:** terrance@inspirebuildmotivate.com (or verified GHL sending address)
- **Reply-To:** terrance@inspirebuildmotivate.com

### Navigation
GHL → **Email Marketing → Campaigns** OR **Automation → Sequences**
(GHL UI may call these "Email Campaigns" or "Sequences" depending on version)

---

## SEQUENCE 1: Kingdom Seedling ($7 eBook)
**Sequence Name:** `SP — Kingdom Seedling Sequence`
**Entry offer:** $7 eBook
**Checkout URL:** `https://link.fastpaydirect.com/payment-link/69ef5c807dd3512d9207b2a2`

---

### EMAIL 1 — Day 0 (Send immediately)
**Subject:** Your Kingdom Stage result is inside, {{contact.firstName}}
**Preview text:** You're a Kingdom Seedling — here's what that actually means

**Body:**
```
Hey {{contact.firstName}},

You just took the Kingdom Business Assessment and your result is in.

You're a Kingdom Seedling.

That means you have the vision, the faith, and the hunger — but you're still 
figuring out how to turn that into a real business that pays you.

Here's the truth nobody told you: the people making money from their stories 
had the same doubts you have right now. They just started anyway.

Habakkuk 2:2 says "Write the vision and make it plain."

It didn't say "only if you have everything figured out."

Your first move is simpler than you think:

→ Get the eBook: How to Write a 40-Page eBook (Even If You've Never Written 
a Grocery List)

This is the exact framework that shows you how to take what's already in your 
head — your story, your lessons, your faith — and turn it into a product 
someone will pay for this week.

[GET THE EBOOK FOR $7]
https://link.fastpaydirect.com/payment-link/69ef5c807dd3512d9207b2a2

Your story is worth more than you know. Let's start there.

— Terrance
Soul Prosperity Group

P.S. The eBook is 40 pages and reads in under 2 hours. By the time you're 
done you'll have your 12 chapter titles written. That's your whole book in 
one sitting.
```

---

### EMAIL 2 — Day 1
**Subject:** The real reason you haven't started yet
**Preview text:** It's not what you think

**Body:**
```
Hey {{contact.firstName}},

I want to ask you something real.

What are you actually waiting for?

Most Kingdom Seedlings say they're waiting to "be ready." But ready is a 
feeling that never fully arrives. The people who build something don't wait 
for ready — they start with what they have and figure the rest out in motion.

Paul wrote his most powerful letters from prison. No laptop. No WiFi. No 
publisher. Just a message he couldn't keep inside.

You have more resources than Paul had. And you still have something to say.

The block isn't ability. It's the absence of a starting point.

That's exactly what the eBook framework gives you — a 12-chapter structure 
that removes the blank page completely. You don't write Chapter 1. You write 
12 titles first. That's your whole book in 20 minutes.

[GET THE $7 EBOOK AND START TODAY]
https://link.fastpaydirect.com/payment-link/69ef5c807dd3512d9207b2a2

Let's go.

— Terrance
```

---

### EMAIL 3 — Day 3
**Subject:** What happened when I hit publish for the first time
**Preview text:** It wasn't perfect. It worked anyway.

**Body:**
```
Hey {{contact.firstName}},

The first thing I ever published wasn't great.

The cover was basic. The writing wasn't polished. There were probably typos.

I hit publish anyway.

And something happened that I didn't expect: people bought it. Not because 
it was perfect — but because it was real. Because it was mine. Because 
somebody needed exactly what I had been through.

That's the thing about your story. It doesn't have to be perfect to be 
powerful. It just has to be honest.

The eBook framework I use has one rule: write how you talk. Not how you 
think a "real author" sounds. Not how your English teacher wanted. Just you.

That's what converts. That's what people share. That's what gets 
screenshotted and posted on Instagram at 1am.

Your first product doesn't have to be your best product. It just has to exist.

[GET THE EBOOK — $7]
https://link.fastpaydirect.com/payment-link/69ef5c807dd3512d9207b2a2

— Terrance

P.S. If you've been sitting on this since Monday, today's the day. 
Proverbs 21:5 — the plans of the diligent lead to abundance. 
The keyword is diligent — not perfect.
```

---

### EMAIL 4 — Day 5
**Subject:** Ready to go deeper? (upgrade option inside)
**Preview text:** One step up from the eBook

**Body:**
```
Hey {{contact.firstName}},

Quick one today.

If you've been reading these emails and thinking "I get it, I just need to 
actually do it" — the eBook is your next step.

But if you're the kind of person who learns better by listening — on the 
job, in the truck, between calls — then the Audiobook Bundle was made for you.

It's the full eBook + the complete audiobook version. So you can read it 
at night and listen while you work during the day.

Same framework. Two ways to absorb it. $17 total.

[GET THE AUDIOBOOK BUNDLE — $17]
https://link.fastpaydirect.com/payment-link/69ef5e77557558e89e524ca3

Or if you're starting with the eBook:
[GET THE EBOOK — $7]
https://link.fastpaydirect.com/payment-link/69ef5c807dd3512d9207b2a2

Either way — start something this week.

— Terrance
```

---

### EMAIL 5 — Day 7
**Subject:** Last call, {{contact.firstName}}
**Preview text:** This is the one that changes the trajectory

**Body:**
```
Hey {{contact.firstName}},

This is my last email in this sequence — so I'll be straight with you.

Seven days ago you took the Kingdom Business Assessment. You found out 
you're a Kingdom Seedling. You got 4 emails from me.

And if you haven't started yet, I get it. Life is busy. The grind is real. 
There's always something more urgent.

But here's what I know: the people who are still in the same spot a year 
from now are the ones who kept waiting. And the people who changed their 
trajectory — they made one decision and moved.

This is that moment.

The eBook is $7. That's less than lunch. And it gives you the complete 
framework to build your first digital product — from idea to published — 
using the story you already have.

[GET THE EBOOK FOR $7 — FINAL REMINDER]
https://link.fastpaydirect.com/payment-link/69ef5c807dd3512d9207b2a2

Want the community too? Join Money Masters Academy free for 7 days:
https://skool.com/money-masters-academy-5443/about

I'm rooting for you.

— Terrance Gee
Soul Prosperity Group

"Write the vision and make it plain." — Habakkuk 2:2
```

---

## SEQUENCE 2: Grinding Builder ($17 Bundle)
**Sequence Name:** `SP — Grinding Builder Sequence`
**Entry offer:** $17 Audiobook Bundle
**Checkout URL:** `https://link.fastpaydirect.com/payment-link/69ef5e77557558e89e524ca3`

---

### EMAIL 1 — Day 0
**Subject:** Your result: The Grinding Builder — here's what that means
**Preview text:** You've proven it works. Now let's make it work without you.

**Body:**
```
Hey {{contact.firstName}},

Your Kingdom Business Assessment result is in.

You're a Grinding Builder.

That means you've already proven this works. You've made money from 
something you built. You know it's possible.

But it's inconsistent. Every week feels like starting over. Income goes up, 
then it dips. You're still doing everything manually, and you're tired.

Here's the real issue: you have a product, but you don't have a system yet.

The framework that fixes this is the eBook + Audiobook Bundle — built 
specifically for builders who are moving but need their income to start 
moving on its own.

[GET THE AUDIOBOOK BUNDLE — $17]
https://link.fastpaydirect.com/payment-link/69ef5e77557558e89e524ca3

Read the eBook at night. Listen to the audiobook in the truck, on the job, 
between calls. Two formats. One framework. Everything you need to build 
the system your grind deserves.

— Terrance
Soul Prosperity Group
```

---

### EMAIL 2 — Day 1
**Subject:** The grind is honorable. But God didn't call you to be exhausted.
**Preview text:** Proverbs 21:5 hits different when you're in it

**Body:**
```
Hey {{contact.firstName}},

Proverbs 21:5 — "The plans of the diligent lead surely to abundance."

Notice what it says: the PLANS of the diligent. Not just the hustle. 
The plans.

You can be the hardest working person in your field and still not build 
wealth — if you don't have a system behind the effort. The grind earns 
the income. The system multiplies it.

Right now you're grinding without a multiplier.

The fix is a repeatable offer with automated delivery. Something that 
sells while you're working, sleeping, or at church on Sunday.

The Audiobook Bundle walks you through exactly how to build that — 
using the story and knowledge you already have. No tech degree required. 
No huge budget. Just a framework and the willingness to execute it.

[GET THE BUNDLE — $17]
https://link.fastpaydirect.com/payment-link/69ef5e77557558e89e524ca3

— Terrance
```

---

### EMAIL 3 — Day 3
**Subject:** What does $3K/month actually look like for a builder?
**Preview text:** The math might surprise you

**Body:**
```
Hey {{contact.firstName}},

Let me show you what $3,000/month actually breaks down to.

$7 eBook: you need 429 buyers/month → about 14 per day
$17 bundle: you need 177 buyers/month → about 6 per day
$67 course: you need 45 buyers/month → about 1-2 per day

Six people per day finding your $17 bundle. That's it.

Not 6,000 followers. Not a viral TikTok. Not a massive email list.

Six people a day who need exactly what you went through and are willing 
to pay $17 to learn from it.

That's achievable. That's realistic. And it starts with having the product 
built and the system in place to sell it automatically.

The Audiobook Bundle gives you the framework to build that product this week.

[BUILD THE PRODUCT — $17 BUNDLE]
https://link.fastpaydirect.com/payment-link/69ef5e77557558e89e524ca3

— Terrance
```

---

### EMAIL 4 — Day 5
**Subject:** Ready to add the physical copy? (upgrade inside)
**Preview text:** The paperback turns your product into a physical legacy

**Body:**
```
Hey {{contact.firstName}},

Quick one today.

If you're ready to go all in — the Paperback Bundle includes the eBook, 
audiobook, AND the physical paperback copy.

Why does the physical copy matter?

Because a paperback on someone's shelf is a reminder that you exist. 
It gets passed around. It gets recommended. It sits on a desk in front 
of someone for months.

Digital products get downloaded and forgotten. Physical products stick.

[UPGRADE TO THE PAPERBACK BUNDLE — $27]
https://link.fastpaydirect.com/payment-link/69ef5ed97dd3512d9207b2a6

Or start with the audiobook bundle:
[GET THE $17 BUNDLE]
https://link.fastpaydirect.com/payment-link/69ef5e77557558e89e524ca3

— Terrance
```

---

### EMAIL 5 — Day 7
**Subject:** {{contact.firstName}}, one more thing before I go
**Preview text:** The community changes the game at your stage

**Body:**
```
Hey {{contact.firstName}},

Last email from this sequence.

You're a Grinding Builder. You've proven you can make money. What you 
need now is the system to make it consistent — and accountability 
to actually build it.

That's what the Money Masters Academy Skool community is for.

Live monthly coaching calls. Real operators who are building in the same 
space you are. A place to ask questions and get answers from people who 
have already figured out the piece you're stuck on.

First 7 days are free.

[TRY SKOOL FREE FOR 7 DAYS]
https://skool.com/money-masters-academy-5443/about

And if you haven't grabbed the bundle yet:
[GET THE $17 AUDIOBOOK BUNDLE]
https://link.fastpaydirect.com/payment-link/69ef5e77557558e89e524ca3

Let's build something that multiplies.

— Terrance
"The plans of the diligent lead surely to abundance." — Proverbs 21:5
```

---

## SEQUENCE 3: Kingdom Operator ($67 Course Bundle)
**Sequence Name:** `SP — Kingdom Operator Sequence`
**Entry offer:** $67 Course Bundle
**Checkout URL:** `https://link.fastpaydirect.com/payment-link/69ef5fc0557558e89e524ca5`

---

### EMAIL 1 — Day 0
**Subject:** Your result: Kingdom Operator — and what's really blocking you
**Preview text:** You're not missing hustle. You're missing architecture.

**Body:**
```
Hey {{contact.firstName}},

Your Kingdom Business Assessment result is in.

You're a Kingdom Operator.

That means you're running a real business. Real revenue. Real customers. 
Real problems that only the owner — you — can solve.

And that's exactly the issue.

You've built a business that depends on your presence. The moment you step 
away, things slow down. That's not a business — that's a high-paying job.

The fix isn't working harder. It's building Kingdom Systems that run under 
God's order, not just your energy.

The Online Course Bundle is built for exactly where you are: you get the 
full eBook + audiobook + paperback + complete Modern eBook Blueprint Mastery video 
course — everything you need to architect a business that runs without you.

[GET THE COURSE BUNDLE — $67]
https://link.fastpaydirect.com/payment-link/69ef5fc0557558e89e524ca5

Proverbs 16:3 — "Commit your work to the LORD, and your plans will 
be established."

Commit the architecture. Build the system. Let God multiply it.

— Terrance
Soul Prosperity Group
```

---

### EMAIL 2 — Day 1
**Subject:** What "systems" actually means for a blue-collar operator
**Preview text:** It's not robots. It's repeatable decisions.

**Body:**
```
Hey {{contact.firstName}},

When most people hear "systems" they think of complex tech stacks and 
engineers. That's not what this is.

A system is a repeatable decision you make once that runs without you 
making it again.

Your quiz funnel is a system — someone finds it, takes the quiz, gets 
a result, receives an email sequence, and moves toward a purchase. 
You set it up once. It runs while you work.

Your GHL follow-up is a system. Your checkout page is a system. Your 
onboarding email is a system.

At the Operator stage, your job is to find every place where YOU are 
the system — and replace yourself with a process.

The Modern eBook Blueprint Mastery course inside the Course Bundle walks you 
through exactly that. GHL workflows, quiz funnels, automated follow-up, 
client systems — all of it.

[GET THE COURSE BUNDLE — $67]
https://link.fastpaydirect.com/payment-link/69ef5fc0557558e89e524ca5

— Terrance
```

---

### EMAIL 3 — Day 3
**Subject:** The real cost of being the bottleneck
**Preview text:** It's not just your time. It's your ceiling.

**Body:**
```
Hey {{contact.firstName}},

Here's a question worth sitting with:

If you took a full week off — completely disconnected — what would 
happen to your revenue?

If the honest answer is "it would drop significantly" — you're the 
bottleneck. And your current revenue is your ceiling, not your floor.

The operators who break through $10K/month consistently have one thing 
in common: they built systems before they felt ready to build them. 
They automated the repetitive decisions before the business demanded it.

That's what the Course Bundle gives you — a 30-day implementation 
roadmap so you're not just learning systems in theory, you're building 
your actual business infrastructure in real time.

[GET THE COURSE BUNDLE — $67]
https://link.fastpaydirect.com/payment-link/69ef5fc0557558e89e524ca5

Lifetime access. Every future update included.

— Terrance
```

---

### EMAIL 4 — Day 5
**Subject:** The community is where operators like you scale
**Preview text:** You've outgrown learning alone

**Body:**
```
Hey {{contact.firstName}},

At the Operator stage, the fastest path to your next level is other 
operators who are already there.

Not inspiration content. Not YouTube tutorials. Real people who have 
already solved the exact problem you're facing and can tell you 
what they did.

That's the Money Masters Academy. Live monthly coaching calls with me. 
A private community of Christian business owners who operate at your level. 
The full Kingdom Systems curriculum inside.

First 7 days free.

[TRY SKOOL FREE]
https://skool.com/money-masters-academy-5443/about

And if you're ready for the full infrastructure:
[GET THE COURSE BUNDLE — $67]
https://link.fastpaydirect.com/payment-link/69ef5fc0557558e89e524ca5

— Terrance
```

---

### EMAIL 5 — Day 7
**Subject:** Last one — the choice operators make
**Preview text:** The next level requires a decision, not more information

**Body:**
```
Hey {{contact.firstName}},

Last email.

You're a Kingdom Operator. You already know more than enough to build 
something great. The gap isn't information — it's architecture and execution.

Here's the choice that separates operators who scale from those who plateau:

Operators who scale invest in the infrastructure before the revenue 
demands it. They build the system while the business is still manageable.

Operators who plateau wait until they're overwhelmed — and by then 
they're too busy to build anything.

You're at that decision point right now.

[GET THE COURSE BUNDLE — $67]
https://link.fastpaydirect.com/payment-link/69ef5fc0557558e89e524ca5

[OR JOIN SKOOL FREE FOR 7 DAYS]
https://skool.com/money-masters-academy-5443/about

"Commit your work to the LORD, and your plans will be established." 
— Proverbs 16:3

— Terrance Gee
Soul Prosperity Group
```

---

## SEQUENCE 4: Kingdom Scaler (Skool Trial)
**Sequence Name:** `SP — Kingdom Scaler Sequence`
**Entry offer:** Free Skool Trial → $47/month
**Skool URL:** `https://skool.com/money-masters-academy-5443/about`

---

### EMAIL 1 — Day 0
**Subject:** Your result: Kingdom Scaler — welcome to your level
**Preview text:** You're not building a business anymore. You're building a legacy.

**Body:**
```
Hey {{contact.firstName}},

Your Kingdom Business Assessment result is in.

You're a Kingdom Scaler.

That means you've already done the hard part. You've generated real income. 
You've survived the hard seasons. You know this works.

What you need now isn't another course. You need a community of operators 
who think at your level — and the systems to break through your next ceiling.

That's the Money Masters Academy.

Live monthly coaching calls. A private Skool community of blue-collar 
Christian business owners who are building at scale. The complete Kingdom 
Systems curriculum. Accountability partners who actually understand the 
grind and the faith behind it.

First 7 days are completely free.

[START YOUR FREE 7-DAY TRIAL]
https://skool.com/money-masters-academy-5443/about

"For I know the plans I have for you, declares the LORD, plans to prosper 
you and not to harm you, plans to give you a future and a hope." 
— Jeremiah 29:11

— Terrance
Soul Prosperity Group
```

---

### EMAIL 2 — Day 1
**Subject:** The #1 thing that limits Kingdom Scalers
**Preview text:** It's not strategy. It's isolation.

**Body:**
```
Hey {{contact.firstName}},

I've worked with a lot of people at your stage.

And the #1 thing that limits scalers isn't strategy or money or time.

It's isolation.

You've outgrown your current peer group. The people around you are 
operating at a different level — and as much as they support you, 
they can't challenge your thinking at the level you need.

The next ceiling only breaks when you're in a room — physical or 
digital — with people who have already broken through it.

That's what the community is for.

[JOIN THE COMMUNITY — 7 DAYS FREE]
https://skool.com/money-masters-academy-5443/about

You belong at the table. Come find your seat.

— Terrance
```

---

### EMAIL 3 — Day 3
**Subject:** What legacy actually looks like at your stage
**Preview text:** It's not about the money anymore — or is it?

**Body:**
```
Hey {{contact.firstName}},

At the Scaler stage, something shifts.

You stop thinking about survival and start thinking about significance. 
Not just "can I pay my bills" but "what does this become in 10 years?"

That's the Kingdom mindset. And it's exactly where the conversation 
inside Money Masters Academy lives.

We talk about recurring revenue models. We talk about building 
something that runs without the founder. We talk about what it means 
to leave a legacy that outlives your involvement.

Paul's letters are still being read 2,000 years later. That's legacy. 
Your business, built right, can outlive you too.

[JOIN THE COMMUNITY]
https://skool.com/money-masters-academy-5443/about

Or if you're ready to go all in — Lifetime Access is $497 (no monthly fees, ever):
https://link.fastpaydirect.com/payment-link/69ef60c87dd3512d9207b2ac

— Terrance
```

---

### EMAIL 4 — Day 5
**Subject:** Annual or Lifetime — the math inside
**Preview text:** One of these is obviously better

**Body:**
```
Hey {{contact.firstName}},

Quick breakdown for the Kingdom Scaler who's already decided they're in:

Monthly: $47/month → $564/year
Annual: $247/year → saves you $317
Lifetime: $497 once → pays for itself in less than 11 months, free forever after

If you're planning to stay in the community for more than a year — 
and I hope you are — Lifetime is the obvious play.

[GET LIFETIME ACCESS — $497]
https://link.fastpaydirect.com/payment-link/69ef60c87dd3512d9207b2ac

[OR START FREE FOR 7 DAYS]
https://skool.com/money-masters-academy-5443/about

Either way, get in. The community is where the real work happens.

— Terrance
```

---

### EMAIL 5 — Day 7
**Subject:** {{contact.firstName}} — your free trial ends soon
**Preview text:** Here's what you'll lose access to

**Body:**
```
Hey {{contact.firstName}},

Your 7-day free trial in Money Masters Academy ends soon.

Here's what you'll lose access to if you don't upgrade:

✦ Monthly live coaching calls with me
✦ The full Kingdom Systems curriculum
✦ The private community of Christian business owners at your level
✦ Accountability partners who are building in the same space

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
Soul Prosperity Group
```

---

## ═══════════════════════════════════════
## COMPLETION CHECKLIST
## ═══════════════════════════════════════

After all 3 steps are complete, verify:

### Step 3 — FastPayDirect
- [ ] $7 eBook link → success redirect set to thank-you URL
- [ ] $17 Bundle link → success redirect set to thank-you URL
- [ ] $27 Paperback link → success redirect set to thank-you URL
- [ ] $67 Course link → success redirect set to thank-you URL
- [ ] $497 Lifetime link → success redirect set to thank-you URL
- [ ] $97 AI System link → success redirect set to thank-you URL

### Step 2 — GHL Workflow
- [ ] Workflow named `Soul Prosperity — Quiz Funnel Lead Router` created
- [ ] Inbound Webhook trigger set
- [ ] Create/Update Contact action mapped
- [ ] `quiz_result` custom field set from webhook payload
- [ ] Tag `quiz-funnel-lead` applied
- [ ] 4-branch If/Else routing by `quizResult` value built
- [ ] Fallback branch set to seedling sequence
- [ ] Workflow status set to Published/Active
- [ ] Test contact created and verified in GHL

### Step 1 — Email Sequences
- [ ] `SP — Kingdom Seedling Sequence` created (5 emails)
- [ ] `SP — Grinding Builder Sequence` created (5 emails)
- [ ] `SP — Kingdom Operator Sequence` created (5 emails)
- [ ] `SP — Kingdom Scaler Sequence` created (5 emails)
- [ ] All 16 FastPayDirect links verified correct in email bodies
- [ ] All 4 sequences set to sender: `Terrance | Soul Prosperity`
- [ ] All 4 sequences connected to workflow branches

---

## COMPLETION CONFIRMATION

When all tasks are complete, output the following summary:

```
SOUL PROSPERITY STEPS 1-3 — EXECUTION COMPLETE

Step 3 (FastPayDirect): [COMPLETE / PARTIAL — list any missed links]
Step 2 (GHL Workflow): [COMPLETE / issues found]
Step 1 (GHL Sequences): [COMPLETE — X of 4 sequences built]

Test contact result: [email used, quiz_result field value, tag applied]

Revenue loop status: CLOSED
- Leads hitting webhook: ✅
- Contacts created in GHL: ✅
- Email sequences firing: ✅
- Payment links wired: ✅
- Post-purchase redirect: ✅
```

---

*Document generated by Claude (Anthropic) for Soul Prosperity Group*
*Operator: Terrance Gee | Handoff target: Comet Browser Assistant*
*All credentials, URLs, and copy are production-ready as of 2026-05-09*
