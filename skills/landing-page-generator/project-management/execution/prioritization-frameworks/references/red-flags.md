# Red Flags: Prioritization Frameworks

> Common ways this skill's output goes wrong -- concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan before sharing a prioritization output (a ranked backlog, a RICE table, an opportunity score). Each red flag has a `bad` and `good` quoted example. If your output matches a bad example, fix it before the artifact leaves your machine.

---

## Red Flag 1: Everything Scores High Impact

**Symptom.** Every item in the backlog gets Impact = 3 (massive) on the RICE scale.
**Why it's bad.** RICE is a *relative* ranking tool. If every item is "massive", you've ranked nothing -- the score collapses to Reach x Confidence / Effort, and Impact loses signal. Worse, leadership starts ignoring impact entirely because it never differentiates.
**Bad example:**
> | Item | Reach | Impact | Confidence | Effort | RICE |
> | --- | --- | --- | --- | --- | --- |
> | Dark mode | 5000 | 3 (massive) | 80% | 2 | 6000 |
> | Onboarding redesign | 4000 | 3 (massive) | 70% | 4 | 2100 |
> | Tax form export | 800 | 3 (massive) | 90% | 1 | 2160 |
**Good example:**
> | Item | Reach | Impact | Confidence | Effort | RICE |
> | --- | --- | --- | --- | --- | --- |
> | Dark mode | 5000 | 0.5 (low) | 80% | 2 | 1000 |
> | Onboarding redesign | 4000 | 2 (high) | 70% | 4 | 1400 |
> | Tax form export | 800 | 3 (massive) | 90% | 1 | 2160 |
**How to catch it.** Histogram Impact across the backlog. If more than 30% of items score "massive" (3.0), force a recalibration round: only items with documented behavioral or revenue evidence keep the 3.

---

## Red Flag 2: Confidence Padding to Hit a Target Rank

**Symptom.** A favored item's Confidence is bumped from 50% to 80% with no new evidence, just to push it above the cut line.
**Why it's bad.** Confidence is supposed to *discount* unvalidated ideas. Padding it converts RICE from a calibration tool into a rubber stamp, and the resulting plan systematically over-invests in pet projects.
**Bad example:**
> "Marketing wants Item X in the quarter. Bumped Confidence from 50% to 80% so it crosses the line. We will revisit after launch."
**Good example:**
> "Marketing wants Item X. Current Confidence is 50% because we have no usage data. Running a 2-week landing-page test next sprint to gather signal -- if click-through > 4%, Confidence moves to 80% and the item re-enters scoring."
**How to catch it.** Require a written Confidence Source column. Empty source = Confidence capped at 50%.

---

## Red Flag 3: Effort Estimated Without Engineering

**Symptom.** The PM scored Effort solo, using "small / medium / large" gut feel.
**Why it's bad.** Effort is the only denominator in RICE / ICE. Get it wrong and the entire rank flips. PMs systematically under-estimate backend, security, and migration work because they don't see it.
**Bad example:**
> "Effort: 2 person-months. (Set by PM during planning.)"
**Good example:**
> "Effort: 4 person-months. Tech-lead estimate after spike: 2.5 weeks frontend + 3 weeks backend (new event-bus integration) + 1 week QA + 2 weeks security review. Logged in `effort-estimates.md`."
**How to catch it.** Reject any score where Effort lacks an engineering co-signer.

---

## Red Flag 4: Reach Counted as TAM, Not Quarterly Touch

**Symptom.** Reach = total addressable market (millions) instead of users who will encounter the feature in the next quarter.
**Why it's bad.** RICE's Reach is "people impacted per time unit" (Intercom's original definition was "per quarter"). Using TAM makes every B2C feature dominate every B2B feature, breaking comparability.
**Bad example:**
> "Reach: 50,000,000 (all US adults could theoretically use this)."
**Good example:**
> "Reach: 8,400 active users / quarter. Source: MAU report Q1 2026, filtered to users who hit the relevant flow at least once. See `reach-source.csv`."
**How to catch it.** Reach > 5x your quarterly MAU = wrong unit. Require a data source column.

---

## Red Flag 5: ICE for 80-Item Backlogs

**Symptom.** A 75-item backlog scored with ICE on a 1-10 scale.
**Why it's bad.** ICE is meant for quick triage on small lists (< 15 items). At 75 items the noise dominates -- a 7 and an 8 are statistically indistinguishable but appear adjacent in the rank. Teams treat the order as meaningful and ship low-value work.
**Bad example:**
> "Sorted 75 items by ICE. Top 12 go in the quarter."
**Good example:**
> "ICE-triaged 75 items down to top 30 candidates. Re-scored top 30 with RICE using engineering effort estimates. Top 12 by RICE go in the quarter."
**How to catch it.** Item count > 15 + framework = ICE = re-rank top tertile with RICE.

---

## Red Flag 6: MoSCoW with No Must / Should / Could Caps

**Symptom.** 70% of items are tagged "Must" and 25% are "Should". "Could" and "Won't" are empty.
**Why it's bad.** MoSCoW's value is the forcing function -- a deliverable scope where Musts are roughly 60% of effort, Shoulds 20%, Coulds 20%. Without caps it degenerates into "everything is critical", which is just a flat list.
**Bad example:**
> "Must: 23 items. Should: 8 items. Could: 0. Won't: 0."
**Good example:**
> "Must: 8 items (~55% of capacity). Should: 5 items (~25%). Could: 6 items (~20%, drop if Musts slip). Won't (this release): 14 items, documented in `wont-this-release.md`."
**How to catch it.** Must >= 75% of items = MoSCoW abuse. Re-run with explicit capacity caps.

---

## Red Flag 7: Opportunity Score Sourced from a 12-Person Survey

**Symptom.** Opportunity scores (Importance + Unsatisfaction) calculated from a 12-respondent internal survey.
**Why it's bad.** Ulwick's Outcome-Driven Innovation requires n >= 180 to separate signal from noise (and ideally 300+ across segments). Twelve responses produce wide confidence intervals and the rank can be reshuffled by 2-3 respondents changing minds.
**Bad example:**
> "Opportunity score for 'reduce time to first invoice' = 14.2. (n = 12 internal pilot users.)"
**Good example:**
> "Opportunity score for 'reduce time to first invoice' = 14.2 (95% CI: 12.8 - 15.6). n = 247 customers, segmented by ARR band and persona. Survey instrument and raw data in `odi-q1-2026/`."
**How to catch it.** Any opportunity score without n, segmentation, and confidence interval should be marked draft and not used for prioritization.

---

## Red Flag 8: WSJF Without Job-Size Calibration

**Symptom.** WSJF (Cost of Delay / Job Size) used on a team that has never calibrated story points.
**Why it's bad.** WSJF amplifies the denominator. If Job Size estimates are noisy (which they always are in an uncalibrated team), the rank is dominated by whoever shouted "small!" loudest, not by actual value-per-effort.
**Bad example:**
> "Item A: CoD = 80, Size = 1, WSJF = 80. Item B: CoD = 200, Size = 5, WSJF = 40. Ship A first."
**Good example:**
> "Item A: CoD = 80, Size = 1 (calibrated against 6 reference stories from last quarter; 80% confidence). Item B: CoD = 200, Size = 5 (same calibration). WSJF still favors A, but flagged for review because Item B has a hard deadline -- moving to CD3 framework instead."
**How to catch it.** No reference-story calibration = WSJF is not the right framework. Use Impact x Effort 2x2 instead.

---

## Red Flag 9: Kano Model Without Recent User Research

**Symptom.** Features classified as Delighter / Performance / Must-Have based on PM intuition, not Kano survey data.
**Why it's bad.** Kano categories shift over time -- yesterday's Delighter is today's Must-Have (think: search bar, dark mode, single-sign-on). Classifying from intuition produces a snapshot of *the PM's* mental model, not the market's.
**Bad example:**
> "Two-factor auth: Delighter. Users will love that we offer it."
**Good example:**
> "Two-factor auth: Must-Have for enterprise segment, Performance for SMB. Source: Kano survey Q4 2025 (n=412, both functional + dysfunctional questions). 78% of enterprise respondents in 'I expect it' band; SMB split 45 / 40."
**How to catch it.** Kano classification without a survey reference is fan-fiction.

---

## Red Flag 10: No Tie-Breaker Rule for Identical Scores

**Symptom.** Three items tied at RICE = 1400, no documented rule for picking which goes first.
**Why it's bad.** Ties get resolved by hallway politics. The most senior voice picks the winner, and the prioritization process loses credibility ("they were going to pick that one anyway").
**Bad example:**
> "Items A, B, C all scored 1400. Picked A because it was easiest to start."
**Good example:**
> "Items A, B, C all scored 1400. Tie-breaker rule (from `prioritization-charter.md`): strategic theme alignment first, then customer commitments, then team dependencies. A and B align to 'Activation' theme; B has a Q1 customer commitment. Picked B."
**How to catch it.** Identical scores without a documented tie-breaker = bring the charter, not the loudest voice.

---

## Red Flag 11: Mixing Frameworks Without Explanation

**Symptom.** Backlog spreadsheet has RICE for half the items, ICE for others, and MoSCoW tags on the rest -- combined into a single rank.
**Why it's bad.** Different frameworks produce different score distributions. Mixing them is like ranking athletes by combining marathon times with weightlifting kilos. The result looks rigorous but is meaningless.
**Bad example:**
> "Top of the backlog: RICE = 2400. Next item: ICE = 9. Next: MoSCoW = Must. Sorted by 'priority score'."
**Good example:**
> "Backlog split into three buckets: opportunities (ranked by Opportunity Score, n=247), features (ranked by RICE), and constraints (ranked by MoSCoW). Quarterly slate pulls top items from each bucket according to capacity rules in `prioritization-charter.md`."
**How to catch it.** A single sort column that mixes framework outputs is always wrong.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Everything is Impact = massive | Histogram Impact; >30% massive triggers recalibration |
| 2 | Confidence padding | Require a Confidence Source column |
| 3 | Effort estimated solo | Reject scores without engineering co-signer |
| 4 | Reach = TAM | Reach > 5x quarterly MAU = wrong unit |
| 5 | ICE for big backlogs | >15 items + ICE = re-rank top tertile with RICE |
| 6 | MoSCoW with no caps | Must >= 75% of items = abuse |
| 7 | Opportunity score, n=12 | Require n, segmentation, confidence interval |
| 8 | WSJF, no calibration | No reference-story calibration = use 2x2 instead |
| 9 | Kano from intuition | No survey reference = fan-fiction |
| 10 | Ties resolved by politics | Document a tie-breaker rule in charter |
| 11 | Mixed framework rank | Single sort column mixing outputs = always wrong |

## Related Reading

- `SKILL.md` -- framework decision tree (which framework when)
- `references/frameworks.md` -- the 9 frameworks with worked examples
- `scripts/prioritization_scorer.py --help` -- the scoring tool
- Sibling skill: `execution/backlog-refinement/` -- INVEST / DoR / DoD
- Sibling skill: `discovery/identify-assumptions/` -- before scoring, validate the assumption
