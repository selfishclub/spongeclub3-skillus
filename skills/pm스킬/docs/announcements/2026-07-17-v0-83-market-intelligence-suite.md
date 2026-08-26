# v0.83 — The Market Intelligence Suite

**July 17, 2026**

The biggest single addition in the library's history: **14 new skills and 2 major upgrades** that turn competitive and market research from a term paper into an operating capability. Stop doing "competitive research" like a homework assignment — run collection disciplines like an intelligence agency: independent channels, signal → inference chains, confidence stacking, and a fusion cadence.

## What changed in v0.83

### A new interaction mode: autonomous investigation

- **New protocol skill: `autonomous-investigation`** (Workflow, `theme: market-intelligence`). The counterpart to `workshop-facilitation` for skills where the *world* holds the context instead of you. Every investigation skill honors its seven-clause contract: a hard question budget (then proceed on labeled assumptions), a search-plan gate ("reviewing a plan takes 10 seconds; reviewing a wrong report takes 10 minutes"), **Fact / Inference / Assumption** labels on every claim, domain-specific do-not-invent lists, Just Enough Mode, stable diffable schemas, and an exactly-4-option Final Step. Because these skills degrade gracefully when nobody answers questions, they can run as agent tasks, in loops, or on schedules — re-run and diff against last quarter.

### The backbone

- **New: `intelligence-collection-disciplines`** (Component). Eight collection disciplines — OSINT, FININT, GEOINT/DEMOINT, TECHINT, HUMINT, SIGINT, MASINT, and All-Source Fusion — each with free/paid source tables, signal → inference chains, and the PM artifact it feeds. Includes the bottom-up TAM/SAM/SOM recipe, the Confidence Stacking Rule (1 discipline = watch item; 3+ = actionable intelligence), the fusion cadence, and SCIP-grounded guardrails: if you'd be uncomfortable explaining your method on stage at the target's user conference, don't use the method.
- **New: `intel-discipline-advisor`** (Interactive). The triage pairing for the compendium: three adaptive questions about the decision on your desk, then numbered recommendations naming the discipline mix, cadence, and executing skill — teaching the mapping as it routes, with an honest off-ramp to discovery and win/loss when no public-web sweep answers your question.

### The investigation chain

Four Workflow skills, each consuming the prior's stable schema:

- **`market-landscape-scan`** — segments as *buyers* see them (not analyst quadrants), player map including substitutes and non-consumption, and whitespace that must survive the "or is it a dead zone?" test.
- **`competitive-research-snapshot`** — cited competitor snapshots, a comparison matrix with an evidence-quality row, and so-what implications sized to the decision.
- **`competitive-intel-watch`** — the scheduled delta monitor: material shifts only, battle-card update flags, and "no material change" as a first-class result. A watch reports change, not state.
- **`battle-card-builder`** — a field-action card that fits a rep's thirty seconds: every claim sourced and labeled, trap questions only where the documented answer is known, and a "Do Not Say" section that protects reps from the team's own folklore.

### Strategy frameworks, evidence-cited

- **`swot-analysis`** — quadrant discipline (an "opportunity" that requires them to act is a strategy), strengths from customer voice rather than marketing, and the S-O / W-T crossings, because a SWOT without "so what" is a parking lot with four sections.
- **`porters-five-forces`** — each force rated with documented signals that survive "how do you know?", AI-driven substitution named explicitly, closing at the profit pool: where margin sits and who is squeezing it.
- **`ansoff-matrix`** — growth options with evidence per quadrant and a risk gradient that makes diversification carry the burden it deserves. Cross-referenced with `organic-growth-advisor`: diagnose your constraint there, evidence the options here.

### Monitors and miners

- **`voice-of-customer-miner`** — public reviews, app stores, and forums mined for unmet needs and switching triggers, themed by *need* rather than feature, with verbatim quotes, source-bias notes, and a mandatory handoff to real interviews.
- **`pricing-packaging-tracker`** — competitor pricing as a diffable time series. Packaging changes (gates, limits, tier restructures) signal strategy earlier than price changes do.
- **`pestel-delta-monitor`** — the quarterly re-scan that pairs with `pestel-analysis`: which macro factors moved, which baseline assumptions broke (the real output), what's new to the frame.

### Orchestration

- **`competitive-analysis-process`** — the six-step umbrella (landscape → product comparison → customer-need fulfillment → business baseline → perception/positioning → strategic direction), each step naming its frameworks — Porter, Kano, ODI, Ries & Trout, Hamel & Prahalad — and delegating to the right suite skill. Step 6 is the one most teams skip, which is why they're perpetually surprised.

### Two upgraded skills

- **`tam-sam-som-calculator`** now has three entry modes: bring your own numbers, guided interview, or **autonomous research** — a bottom-up, citation-backed estimate built from establishment counts × benchmarks, with SOM capture rates derived from competitor filings. Bottom-up wins scrutiny because a skeptical CFO can attack one assumption at a time instead of dismissing the slide.
- **`company-intel`** gained the **Executive Signal Refresh** rerun pattern (Then/Now diffs with exact quotes, plus **Dropped Language** — what leaders *stop* saying is often the strongest signal), a source priority ladder, a do-not-sanitize rule, sharper product-org heuristics (CPO tenure, PM job postings as culture documents), and an optional organizational distress read.

- **Library is now 70 skills** — 24 Component, 27 Interactive, 19 Workflow — plus 6 commands. New marketplace category: `market-intelligence`.

## Why an intelligence suite

Most competitive research is a deck of unlabeled inference assembled the week before a strategy offsite, stale by the time it's presented. The intelligence community solved this decades ago: independent collection channels that fail differently, explicit evidence labels, confidence that escalates only as channels corroborate, and a cadence instead of a heroic annual effort. Every skill in this suite teaches that tradecraft while doing the work — the human PM should finish a run knowing more about evidence discipline than when they started. That's the mission: functional and pedagogic in equal measure.

## Upgrading

- **Claude Desktop / Web:** grab the refreshed packs or individual skill ZIPs from [`dist/`](https://github.com/deanpeters/Product-Manager-Skills/tree/main/dist).
- **Claude Code (plugin marketplace):** the marketplace manifest lists all 14 new skills; update the plugin to pull them.
- **Codex:** re-download `pm-skills-codex.zip` from `dist/packages/`.

## References

- Distilled from Dean Peters' [product-manager-prompts](https://github.com/deanpeters/product-manager-prompts) market-intelligence collection, plus practitioner field material on competitive and market intelligence
- Framework attributions: Michael E. Porter (HBR, 1979); H. Igor Ansoff (HBR, 1957); Kano; Ulwick (ODI); Osterwalder & Pigneur; Ries & Trout; Hamel & Prahalad (HBR, 1994); SCIP Code of Ethics
