# Application Playbooks

Read this when diagnosing a specific conversion problem or applying psychology to an asset — covers the behavioral diagnosis workflows, principle-by-challenge tables (landing pages, pricing, email, churn, ads), the pricing framework, the conversion playbook, and copy techniques.

## Core Workflows

### Workflow 1: Behavioral Diagnosis

When something is not converting, diagnose through a behavioral lens:

**Step 1: Map the Decision Journey**

| Stage | What Visitor Does | What Visitor Feels | Potential Barriers |
|-------|------------------|-------------------|--------------------|
| Arrival | Lands on page | Curious or skeptical | No immediate value recognition |
| Evaluation | Reads content | Interested or confused | Too much information, unclear benefits |
| Comparison | Considers alternatives | Analytical | No differentiation visible |
| Decision | Approaches CTA | Hesitant | Risk perception, friction, objections |
| Action | Clicks/purchases | Committed or uncertain | Form complexity, hidden costs, trust deficit |

**Step 2: Identify Behavioral Barriers**

For each stage, check for these barrier types:

| Barrier Type | Description | Example |
|-------------|-------------|---------|
| Cognitive load | Too much to process | 15 pricing options, walls of text |
| Choice paralysis | Too many options | 6 plans with unclear differences |
| Loss aversion | Fear of making wrong choice | No guarantee, no trial, no refund |
| Trust deficit | Not enough credibility | No social proof, no named testimonials |
| Status quo bias | Effort of switching feels too high | No migration support, complex setup |
| Friction | Too many steps to complete action | Long forms, mandatory account creation |

**Step 3: Prescribe Principles**

Match each barrier to the psychological principle that addresses it. See the Mental Model Catalog (`references/mental-models.md`).

### Workflow 2: Principle Application

**Step 1: Select 3-5 Relevant Principles**

Do not apply every principle at once. Select the 3-5 most relevant to the specific challenge.

**Step 2: Implement Concretely**

For each principle, define:
- Where on the page/flow it applies
- What specific change to make
- What the expected behavioral impact is

**Step 3: Test and Measure**

Every psychology-based change should be A/B tested:
- Hypothesis: "Applying [principle] to [element] will increase [metric] because [behavioral reason]"
- Test duration: minimum 14 days or 1,000 visitors per variant
- Success metric: conversion rate, click rate, or engagement rate

## Application by Marketing Challenge

### Landing Page Not Converting

| Principle | Where to Apply | Specific Change |
|-----------|---------------|----------------|
| Loss Aversion | Headline | Frame as what they lose without you, not what they gain |
| Social Proof | Below hero | Customer count, logos, or star rating visible above fold |
| Anchoring | Near CTA | Show the value they get vs. the price they pay |
| Hick's Law | Navigation | Remove all navigation links — one page, one CTA |
| Cognitive Fluency | Throughout | Simplify language, increase white space, reduce choices |

### Pricing Page Optimization

| Principle | Where to Apply | Specific Change |
|-----------|---------------|----------------|
| Decoy Effect | Plan structure | Add a tier that makes your target tier the obvious value choice |
| Charm Pricing | Price display | Use $49 not $50 (consumer) or round $100 (enterprise) |
| Good-Better-Best | Tier design | Three tiers, middle is "Most Popular," clearly highlighted |
| Anchoring | Top of page | Show highest price or enterprise price first |
| Default Effect | Toggle | Pre-select annual billing (saves them money, you get commitment) |
| Zero-Price Effect | Free tier | If free tier exists, make it clearly useful but limited |

### Email Engagement

| Principle | Where to Apply | Specific Change |
|-----------|---------------|----------------|
| Zeigarnik Effect | Subject line | Open loops: "The one thing we got wrong about..." |
| Reciprocity | Email content | Give genuine value before asking for anything |
| Goal-Gradient | Onboarding | "You're 2 steps from your first dashboard" |
| Commitment | Micro-asks | Start with easy asks (reply to this email) before hard asks (book a demo) |
| Curiosity Gap | Preview text | Create knowledge gap that the email body closes |

### Reducing Churn

| Principle | Where to Apply | Specific Change |
|-----------|---------------|----------------|
| Endowment Effect | Cancel flow | Show what they will lose (data, history, integrations) |
| Sunk Cost | Cancel flow | "You've created 47 dashboards and saved 120 hours" |
| Loss Aversion | Retention email | "Without [Product], you'll go back to [painful manual process]" |
| Switching Costs | Product | Deep integrations, team workflows, embedded in daily routine |
| Status Quo Bias | Throughout | Make staying easy, make leaving feel effortful |

### Ad Creative Improvement

| Principle | Where to Apply | Specific Change |
|-----------|---------------|----------------|
| Mere Exposure | Retargeting | Show consistent branding across multiple touchpoints |
| Contrast Effect | Ad copy | Before/after comparison, competitor comparison |
| Framing | Headline | Frame the same benefit from a loss vs. gain perspective |
| Social Proof | Ad body | "Join 10,000+ teams" or customer testimonial snippet |
| Pratfall Effect | Brand messaging | "We're not the cheapest — but teams stay 3x longer" |

## Pricing Psychology Framework

### Three-Tier Pricing Design

**Tier 1 (Starter):** Anchors the low end. Useful but limited. Makes Tier 2 look like great value.

**Tier 2 (Growth — Target Tier):** The one you want most people to buy. Best value ratio. Label as "Most Popular" or "Recommended."

**Tier 3 (Enterprise):** Anchors the high end. Makes Tier 2 feel affordable by comparison. Custom pricing creates exclusivity.

### Decoy Pricing Example

**Without decoy (equal attractiveness):**
- Basic: $19/mo (5 users)
- Pro: $49/mo (25 users)

**With decoy (Pro becomes obvious choice):**
- Basic: $19/mo (5 users)
- Plus: $39/mo (10 users) ← Decoy: close to Pro price, much less value
- Pro: $49/mo (25 users) ← Now clearly the best value

### Price Display Best Practices

- Show monthly price even when billing annually (it is a smaller number)
- Pre-select annual billing as the default
- Show the savings: "Save 20% with annual billing"
- Enterprise tier: "Contact us" or "Custom" (no fixed price — enables value-based selling)
- Include "per user" only if the per-user price is low ($5-15/user)
- For usage-based: show an example calculation ("For a team of 10, that is $X/month")

## Conversion Psychology Playbook

### The Trust Cascade

Trust must be built in sequence. Visitors will not convert until sufficient trust is established:

```
1. Visual Trust (0-3 seconds)
   → Professional design, brand consistency, no visual errors
   → If this fails, visitor bounces immediately

2. Relevance Trust (3-10 seconds)
   → Headline matches their need, content speaks their language
   → If this fails, visitor leaves without scrolling

3. Credibility Trust (10-60 seconds)
   → Social proof, authority signals, specific claims
   → If this fails, visitor evaluates competitors instead

4. Risk Trust (60+ seconds)
   → Guarantee, free trial, easy cancellation, clear pricing
   → If this fails, visitor abandons at the CTA
```

### Micro-Commitment Ladder

Build toward the big ask through small steps:

```
Read a blog post (zero commitment)
↓
Download a guide (email exchange)
↓
Start a free trial (product experience)
↓
Activate a key feature (value realization)
↓
Upgrade to paid (financial commitment)
↓
Expand to team (organizational commitment)
```

Each step increases commitment incrementally. Do not ask for the big commitment first.

## Copy Psychology Techniques

### Loss-Framed vs. Gain-Framed Headlines

| Gain-Framed | Loss-Framed (usually stronger) |
|-------------|-------------------------------|
| "Save 4 hours every week" | "Stop losing 4 hours every week" |
| "Get more leads" | "Stop letting leads slip through" |
| "Improve your conversion rate" | "Your conversion rate is costing you $X" |

### Specificity Bias

Specific claims are more believable than round numbers:
- "Save 37% on infrastructure costs" beats "Save over 30%"
- "2,847 teams" beats "thousands of teams"
- "Setup in 8 minutes" beats "Setup in minutes"

### Future Pacing

Help readers visualize the outcome:
- "Imagine opening your dashboard Monday morning and seeing every metric you need, already organized."
- "Picture your next board meeting where you present data you trust, not data you spent all weekend assembling."
