# Cohort, Retention & Funnel Analysis Reference

Practical reference for cohort, retention, and funnel analysis techniques.

## 1. What a cohort is — and why it matters

A cohort is a group of users sharing a common characteristic, typically
the date they joined (signup cohort) or first did a key action (activation
cohort).

Cohort analysis is the right way to look at retention because:
- Aggregate retention masks improvement / decline of recent cohorts
- New cohorts can hide the truth about old ones
- Cohort views show whether the product is getting stickier

### Common cohort axes
- Acquisition date (signup week)
- Activation date (first key action)
- Acquisition source / channel
- Plan / segment
- Geography / locale
- App version (esp. for mobile)
- Experiment treatment

## 2. Retention curve shapes — diagnostic guide

### Power-law smile (idealized)
```
100% — first day
 30% — week 1
 25% — week 2
 23% — week 4
 22% — week 12 (flat = retained)
```
Strong product-market fit; the retained users are a real audience.
Action: invest in scale; pour acquisition fuel.

### Slow decay then flat
```
100% — first day
 80% — week 1
 60% — week 2
 40% — week 4
 30% — week 12 (slow flatten)
```
Generally healthy; some PMF but value realization is slow.
Action: shorten time-to-value; improve onboarding.

### Steep then zero
```
100% — first day
 40% — week 1
 10% — week 2
  3% — week 4
  1% — week 12
```
Novelty product; few users find lasting value.
Action: re-examine value proposition; talk to retained 1%.

### Linear decline / leaky bucket
```
100% — first day
 70% — week 1
 50% — week 2
 30% — week 4
 10% — week 12
```
No flatten; users keep churning. Bad sign.
Action: investigate retention drivers; usually a value-realization issue.

### Rising (network effects)
```
100% — first day
 60% — week 1
 65% — week 4 (rises)
 72% — week 12 (rises)
```
Rare and beautiful; usually network-effects products.
Action: scale acquisition aggressively.

## 3. Reading cohort tables

A retention cohort table looks like:

```
Cohort week | n   | W0   | W1   | W2   | W4   | W8   | W12
--------------------------------------------------------
2026-01-01  | 100 | 100% | 35%  | 28%  | 22%  | 20%  | 18%
2026-01-08  | 120 | 100% | 38%  | 30%  | 24%  | 22%  | 20%
2026-01-15  | 90  | 100% | 42%  | 33%  | 27%  | 24%  | -
2026-01-22  | 110 | 100% | 40%  | 32%  | -    | -    | -
```

Read vertically (down a column) to see how recent cohorts compare to old:
- W4 retention 22% → 27% across cohorts = product is getting stickier
- W4 retention 22% → 18% across cohorts = product is getting weaker

Read horizontally (across a row) to see how a specific cohort decays.

## 4. Cohort segmentation

Beyond signup-week cohorts, useful segmentations:

### By acquisition source
- Paid vs organic
- Channel (Facebook, Google, partner, direct)
- Campaign

Look for: channels that activate well but churn fast — these are the
metric-gaming channels that hurt long-term.

### By activation status
- Activated vs not-activated cohorts
- Compare retention; activation is usually a 5–10x retention multiplier

### By segment / plan
- Free vs paid
- Enterprise vs SMB
- By role / persona

Different segments retain differently; aggregating hides the truth.

### By feature use
- Users who tried feature X vs not
- Users who completed onboarding milestone Y vs not

Identifies retention-driving behaviors; informs activation design.

## 5. The funnel

A funnel measures user progress through a sequence of steps.

### Common funnel types
- **Signup funnel:** landing → signup → activation
- **Conversion funnel:** trial → activation → paid
- **Checkout funnel:** cart → review → payment → complete
- **Feature adoption funnel:** awareness → tried → adopted

### Building a useful funnel
1. **Define each step** as an event
2. **Define the time window** between steps (e.g., signup to activation within 7 days)
3. **Define the population** (e.g., new signups in last 30 days)
4. **Display conversion rates** between consecutive steps + cumulative

### Reading funnel drop-offs
- **Biggest absolute loss** = invest first
- **Steepest % drop** = clearest UX issue
- **Drop concentrated in segment** = check that segment's UX

### Funnel anti-patterns
- Funnels with 10+ steps (noise)
- Funnels that span weeks without time windows
- Funnels averaged across segments (masks real issues)
- Funnels with steps not tracked consistently
- Funnels ignoring resurrection (users who drop then return)

## 6. Activation rate — the early retention metric

Activation rate = % of new users who reach the activation event within
the defined time window.

### Setting the activation criterion
1. Look at user behavior in their first 7–30 days
2. Identify behaviors strongly correlated with 30+ day retention
3. Pick the simplest one (e.g., "added 3 collaborators")
4. Validate: do users who hit this event retain >2x users who don't?

### Common activation events
- Slack: "200 messages in 7 days within first 14 days"
- Facebook: "10 friends in 14 days"
- Dropbox: "1 file in 1 folder on 1 device"
- Notion: "Created 3+ blocks in 2 days"

Activation criteria evolve as the product evolves; revisit annually.

## 7. Segmentation in retention analysis

Aggregate retention is almost always less useful than segmented.

Common segments to break out:
- **By acquisition source / channel** — quality of traffic
- **By onboarding path** — which paths retain
- **By activation status** — activated vs not
- **By plan / pricing tier**
- **By company size / role** (B2B)
- **By feature usage** (used feature X vs not)
- **By geography / locale**
- **By app version** (mobile)

Segmentation reveals where the product is working and where it isn't.

## 8. Mix shift — the hidden retention killer

Aggregate retention can decline even when no segment's retention changed,
if the **mix of segments shifted** toward lower-retention segments.

Example: acquisition spend shifted to a cheaper-but-lower-quality channel
last month → aggregate retention drops next month → looks like product
problem; actually channel problem.

Always cross-check aggregate trends against segment-level trends.

## 9. Retention rate types

| Type | Definition | Use case |
|------|------------|----------|
| **N-day retention** | % who returned on day N exactly | Habit products |
| **Bracket retention** | % who returned on any day in bracket | Less precise; smoother |
| **Rolling retention** | % who returned on day N or later | Forgives skipped days |
| **Range retention** | % active any day in a window | Frequency-tolerant |

For most products, **rolling retention** with weekly buckets is the
most-honest measure.

## 10. The "weekly active = healthy" trap

WAU isn't always meaningful. For products with natural weekly cadence
(productivity), it works. For monthly products (billing, admin tools),
WAU is the wrong frequency.

Pick the right frequency:
- Real-time / chat: DAU
- Productivity: WAU
- Admin / billing: MAU
- Marketplaces / transactions: depends on user role

Don't pick DAU as your stickiness metric for a tool used once a month.

## 11. Funnel improvement — the right order

Most teams improve funnels in the wrong order. The right order:

1. **Top-of-funnel quality** — if signups are noise, no UX fix helps
2. **Biggest absolute drop step** — most impact per fix
3. **Conversion rate within a step** — if step rate is < 50%, there's likely a UX win
4. **Time-between-steps** — too long = friction; too short = no consideration

## 12. Common pitfalls

- **Cohort tables aggregated across acquisition sources.** Hides everything important.
- **Reporting "retention is improving" without showing cohorts.** It might not be.
- **Funnel without time windows.** Numbers can be anything.
- **Activation event without validation.** "We picked X" without showing retention lift.
- **Aggregating mobile + web cohorts.** Different products often.
- **Looking at one metric in isolation.** Decompose, segment, cross-check.
- **Conflating active with retained.** Activity ≠ value realized.
