# Dashboard Anti-Patterns + Fixes

## A1 — The wall-of-metrics dashboard
**Symptom:** 30+ charts on one page. Cognitive overload.

**Fix:** Limit per audience. Cut to top 8-12 max. Move rest to drill-down.

## A2 — No North Star
**Symptom:** 12 equally-weighted metrics; team optimizes randomly.

**Fix:** Designate 1 metric as NS. All others ladder to it (inputs) or
counter it (guardrails).

## A3 — Vanity metrics dominate
**Symptom:** Page views, signups, dashboard-views are headline metrics.

**Fix:** Replace with action-driving metrics. Apply the +/-10% test.

## A4 — No guardrails
**Symptom:** Only "growth" metrics; nothing to protect against optimization gone wrong.

**Fix:** Add 3-5 guardrails — abuse rate, support ticket volume, churn,
team-burnout-proxy.

## A5 — No comparisons
**Symptom:** Number "1,234,567 active users" — no context.

**Fix:** Add comparisons:
- vs prior period (% change)
- vs target
- vs same period last year (seasonality)

## A6 — Cargo-cult real-time
**Symptom:** Every metric refreshes every minute.

**Fix:** Most metrics don't need real-time. Refresh cadence should match
decision cadence:
- Real-time: errors, active users (for triage)
- Hourly: conversion, performance
- Daily: cohorts, MRR
- Weekly: NPS, retention, business KPIs

## A7 — Wrong audience
**Symptom:** Exec dashboard has eng SLOs; team dashboard has board-level metrics.

**Fix:** Per-audience dashboards. Different layers; different cadence.

## A8 — No metric ownership
**Symptom:** When a metric drops, no one knows who to ask.

**Fix:** Per metric: named owner, alert routing, escalation path.

## A9 — Composite "health score" of 17 components
**Symptom:** Single number nobody understands; can't explain when it
moves.

**Fix:** Either:
- Decompose into 4-6 components, each independently legible
- Show the components + a roll-up

## A10 — Pretty but useless
**Symptom:** Dashboard wins a design award. Nobody uses it for decisions.

**Fix:** Lead with action. Each chart should answer: "what decision does
this support?"

## A11 — No drill-down
**Symptom:** Dashboard shows numbers; can't filter or explore.

**Fix:** Build filter / drill-down / export. Half the dashboard's value
is exploratory.

## A12 — Built once, never refreshed
**Symptom:** Dashboard from 2 quarters ago; metrics no longer reflect strategy.

**Fix:** Quarterly review. Cut dead metrics; add new ones for new
priorities.

## Worked example — refactoring a bad dashboard

### Before (bad)

```
Top of dashboard:
- 14 metrics in a grid
- DAU, MAU, signups, page views, sessions, time on site,
  bounce rate, revenue, ARPU, churn, NPS, support tickets,
  feature usage X, feature usage Y

No hierarchy. No comparisons. No owners. Refreshed live.
Nobody uses for decisions.
```

### After (refactored)

```
North Star (top, prominent):
- Weekly Active Companies × Messages Sent per Company
  - This week: 4,250 × 38 = 161,500
  - vs last week: +4.2%
  - vs target (180,000): -10%
  - Owner: CPO; review cadence: weekly

Input metrics (4 cards, smaller):
1. New customer acquisition (this week vs last)
2. Activation rate (W1 reaching 10 messages, 14d cohort)
3. Retention (W4 cohort rate)
4. Per-company message volume (median + P75)

Guardrails (3 cards, in orange):
1. Spam rate (% messages flagged) — alert if > 0.5%
2. User-reported complaint rate — alert if > 5/day
3. Power-user churn (annual) — alert if > 10%

Operational (drill-down):
- Growth team: signup quality, channel CAC, signup-to-trial conversion
- Product team: feature adoption curves, time-to-aha
- CS team: NPS, churn, save-room health
- Platform team: SLOs, on-call pages

Each: named owner, comparison, weekly review.
```

The refactored version has 1 NS + 4 inputs + 3 guardrails + ~16 operational
(spread across teams). Each has owner + comparison.

## Dashboard review checklist

Before declaring a dashboard done:

- [ ] 1 North Star metric prominent
- [ ] 3-5 input metrics decomposing NS
- [ ] 3-5 guardrail metrics with thresholds
- [ ] Operational metrics per team (4-8 each)
- [ ] Per metric: name, definition, source, owner
- [ ] Per metric: comparison (vs period / vs target)
- [ ] Cadence appropriate (not all real-time)
- [ ] Drill-down capability
- [ ] Each audience has its own view
- [ ] Quarterly review scheduled
- [ ] Stale metrics pruned at last review

## Final discipline test

The ultimate dashboard test: did the team make a decision from it this week?

- Yes (1-3 decisions) — healthy dashboard
- Many decisions — possibly too operational; ok if it works
- No decisions — vestigial dashboard; cut metrics until it drives decisions
