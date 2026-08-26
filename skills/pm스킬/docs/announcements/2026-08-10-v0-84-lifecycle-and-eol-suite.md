# v0.84 — The Lifecycle & End-of-Life Suite

**Released:** August 10, 2026
**Library:** 77 skills (28 Component, 29 Interactive, 20 Workflow) + 6 commands
**New themes:** `eol-transition`, `product-lifecycle`

---

## Why this suite

Every PM curriculum teaches you how to launch a product. Almost none teach you what to do when one
stops growing — or how to retire it without torching the customer relationship you spent years
building.

That gap is expensive. The public record is full of it: an FTC investigation over "lifetime"
hardware hubs that got bricked. State-level fines over a service retirement with no adequate
alternative. A generational OS transition that cancelled enterprise contracts and poisoned the
appetite for the next three upgrades.

None of those were product failures. They were **transition** failures.

This release adds seven skills and upgrades one, covering the full arc — from "should this product
change at all?" through "the retirement is closed and here's what we learned."

---

## The governing idea

**Lose the product without losing the customer.**

Everything in the suite protects the second half of that sentence. A retirement that hits every
internal milestone and produces a churn spike did not succeed.

---

## What's new

### Upstream: the play decision

Before "should we kill this?" there's a bigger question, and it has three answers.

**[`lifecycle-play-advisor`](../../skills/lifecycle-play-advisor/SKILL.md)** (Interactive) — four
questions that establish where a product actually sits and which play fits. Seven **transition
questions** do the diagnosis (*is defending market share still profitable? are legacy support costs
becoming unsustainable?*), then the pressure source — demand-side, supply/cost-side, or capability —
discriminates the play.

It defaults toward the cheapest play that addresses the real pressure, and it's willing to answer
**"nothing yet."** A mature product throwing off margin doesn't need a project.

**[`product-lifecycle-plays`](../../skills/product-lifecycle-plays/SKILL.md)** (Component) — the
framework behind that call. The PLC strategy grid by stage, the three plays with their reasons-why,
the **seven replacement hazards**, and a risk register whose final column asks the question teams
skip: *what is Plan B?* Ships a portfolio worksheet for running the decision across a whole product
line.

The teaching point at its center: on a replacement play, **GTM and EOL happen simultaneously**, for
two products that compete with each other. Kodak feared cannibalizing film and lost the market;
Amgen cannibalized deliberately and managed it. Fear it and you lose the future; ignore it and you
lose margin.

### The EOL chain

**[`eol-readiness-advisor`](../../skills/eol-readiness-advisor/SKILL.md)** (Interactive) — the
go/no-go. Four retire signals against four hold signals, and five verdicts including **Hold**,
**Harvest**, and **Extend**. It will tell you not to retire, and it separates the presenting problem
from the underlying one — "free up the manufacturing line" is answered by End of Sale, not
End of Life.

**[`eol-stakeholder-sequence`](../../skills/eol-stakeholder-sequence/SKILL.md)** (Component) — who
to talk to, in what order, and what each conversation must cover. Legal before Finance before Sales
before Marketing before CS. Get the order wrong and you discover the landmines after the
announcement instead of before. Every stop declares what you need **from** them and what you owe
**to** them — and the sequence includes your three most difficult customers, because they will find
the things you forgot.

**[`eol-checklist`](../../skills/eol-checklist/SKILL.md)** (Component) — the phase-gated operational
plan. Up to 15 functional areas across the lifecycle gates, every item 4-8 words with a named owner,
and gate criteria with approvers. Covers the four things sunsets strand: **data, contracts, access,
money.**

**[`eol-internal-enablement`](../../skills/eol-internal-enablement/SKILL.md)** (Component) — the
support FAQ, sales talking points, and objection handling your teams need *before* customers hear.
Objections use Acknowledge-Reframe-Offer, and **every offer is pre-approved with a limit** — an
objection handler ending in "I'll see what I can do" trains reps to promise what the company hasn't
agreed to.

**[`eol-message`](../../skills/eol-message/SKILL.md)** (Component, upgraded) — now right-sized
(Brief / Standard / Full) with **three transition paths**: replacement, migration, and the honest
graceful exit where nothing replaces it and you name competitors as alternatives. Gates are stated
in customer consequences, not internal acronyms.

**[`eol-process`](../../skills/eol-process/SKILL.md)** (Workflow) — the whole thing in six phases:
decide, align, plan, prepare, announce, **close**. Phase 6 exists because it's the one everyone
skips, and it's the one that makes the next sunset cheaper.

---

## Two design decisions worth naming

### Right-sizing is a dial you set

Not all EOLs play out the same. Some are a changelog entry. Some consume the company for three
quarters. **Most land in the middle.**

Every skill in the suite offers **Light / Standard / Heavy**, recommends a level, and then hands you
the dial. Choose lighter than recommended and it names the specific thing that goes uncovered — so
it's a choice, not a surprise. Every skill states that Standard is the default and that you should
**never default to Heavy**.

The reason is pedagogic, not procedural: process theater on a small sunset teaches a team to ignore
the process on the big one. A Level 1 checklist that gets *used* beats a Level 3 that gets ignored.

### It's a route, not a pipeline

Every skill runs standalone. None requires another to have run first. `eol-process` is a
**recommended route through independent stops**, which means you can enter at any phase, skip
phases, and — importantly — **go backwards**.

Going back is a success condition. Phase 2 routinely invalidates a Phase 1 decision, and finding
that out in a conference room is cheap. Finding it out after the announcement is not.

The workflow includes an **"Entering Mid-Stream"** diagnostic, because most people meet this skill
in the middle of a sunset that's already going badly: *"Support is drowning"* → Phase 4 got skipped.
*"Legal just found a contract problem"* → Phase 2 got skipped; return to Phase 1.

---

## Fully adorned, two domains

Every Component and Workflow skill ships `template.md` plus **two worked examples** — one SaaS, one
industrial — and they interlock into two continuous stories:

- **Fieldlight** (field service SaaS) retires Classic Dispatch. The story starts as one row in a
  four-product portfolio worksheet, runs through all six phases, and ends with a lessons-learned
  review reporting 94% retention against a 90% target — and naming the late migration offer that
  cost 11 of the 19 churned accounts.
- **Northfield Automation** (industrial retrofit controllers) plans to retire the NFA-200 — and
  can't. Its risk register named the right hazard and **mis-rated it**, Phase 2 broke the plan, and
  the outcome became End of Sale with no EOL date and the retrofit path funded as the precondition.

The industrial example is deliberately a *failure* worked forward. The play was right; the rating
was wrong. That's the more useful lesson.

---

## Also in this release

- New pack: **`07-lifecycle-eol-pack.zip`** — the full suite in one download
- `eol-readiness-advisor` gained an upstream pointer to the play advisor, so a PM who hasn't settled
  on retirement gets offered the wider question without being forced through it

---

## Sources

Distilled from practitioner experience running product lifecycle transitions and product
retirements, plus the five EOL prompts in
[`product-manager-prompts`](https://github.com/deanpeters/product-manager-prompts).
