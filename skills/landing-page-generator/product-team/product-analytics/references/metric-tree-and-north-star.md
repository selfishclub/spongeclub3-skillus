# Metric Tree & North Star Reference

Practical reference for designing the product metric tree.

## 1. The North Star — what to pick and why

A North Star metric (NSM) is the single metric that best captures the
value your product delivers. It should be:

- **Value-aligned:** moves only when users get more value
- **Leading:** predicts long-term outcomes
- **Actionable:** moves week-over-week with product changes
- **Single:** one number, not five

### Common picks by product type

| Product | Plausible NSM | What it captures |
|---------|---------------|------------------|
| Slack | Messages sent per WAU per company | Engagement + collaboration |
| Spotify | Hours streamed per active listener | Value consumption |
| Airbnb | Nights booked | Transaction completion |
| Notion | Workspaces with ≥3 active editors weekly | Team adoption depth |
| Stripe | Active payment volume per customer | Customer value realized |
| Figma | Files created per user per week | Creation activity |
| GitHub | Engaged developers (action ≥X times/week) | Engagement |
| Linear | Issues moved per project per week | Workflow value |

### Anti-patterns
- "Revenue" — outcome, not input; can mask deteriorating engagement
- "DAU" — counts presence, not value
- "Signups" — measures top of funnel; ignores activation
- "Page views" — almost always vanity
- "Stars / followers" — social-graph metrics that don't equal value

## 2. The 3-layer metric tree

```
                  North Star Metric
                         |
        ┌────────────────┼────────────────┐
        |                |                |
   Input 1          Input 2          Input 3
   (e.g., activation)  (engagement)  (retention)
        |                |                |
   Drivers           Drivers          Drivers
   (4-5 metrics)     (4-5 metrics)    (4-5 metrics)
```

### Layer 1 — North Star (1 metric)
Captures aggregate value delivered.

### Layer 2 — Inputs (3–5 metrics)
Inputs combine multiplicatively to produce the North Star.

Common decompositions:
- Acquisition × Activation × Retention × Monetization
- WAU × Sessions/user × Actions/session
- New + Resurrected − Churned + Returning

### Layer 3 — Drivers (per input, 3–5 metrics)
Drivers are the operational levers a team can influence.

Example for Activation as an input:
- Signup completion rate
- Time to first value (median)
- 7-day activation rate (% reaching activation event)
- Onboarding step completion rate
- Activation by acquisition channel

## 3. Guardrails / counter-metrics

For each input, ask "what would make this metric look good but actually be bad?"

Examples:
- **NSM:** messages sent per WAU
  - **Guardrail:** spam rate, abuse reports, sender complaint rate
- **NSM:** hours streamed
  - **Guardrail:** % of plays under 30 seconds (skip rate)
- **Input:** signup completion
  - **Guardrail:** activation rate by signup channel (low-quality channels game signup)
- **Input:** revenue
  - **Guardrail:** retention rate; CSAT; refund rate
- **Input:** notification opens
  - **Guardrail:** unsubscribe rate; user-reported "too many"

Guardrails should appear on the dashboard, not be hidden.

## 4. Metric definitions — be explicit

A metric without a precise definition is worthless. For each metric, document:

- **Name** (no abbreviations)
- **Definition** (the exact computation, including filters)
- **Source** (which event(s), which table)
- **Granularity** (per user / per company / per session)
- **Time window** (rolling 7-day / fiscal week / calendar month)
- **Owner** (the team accountable)
- **Update cadence** (real-time / hourly / daily)
- **Known caveats** (what could distort it)

If two teams compute "WAU" differently, you have two different metrics.

## 5. Metric tree by product stage

### Pre-product-market-fit
- North Star: typically engagement-based (frequency × depth)
- Inputs: activation rate, retention curve shape, qualitative signal
- Skip: deep monetization metrics

### Early growth
- North Star: usage × retention compound
- Inputs: acquisition channels, activation, retention curve
- Add: cohort comparisons; mix shift detection

### Scaling
- North Star: value delivered + monetization signal
- Inputs: segment-level metrics, geographic, plan/tier
- Add: monetization metrics (ARPU, LTV, payback)

### Mature
- North Star: same as before, but with extensive segmentation
- Inputs: net new + expansion + churn (NRR-style)
- Add: customer-segment-specific dashboards, opportunity metrics

## 6. Common decomposition patterns

### AAARRR (pirate metrics) variant
Acquisition × Activation × Retention × Referral × Revenue (per segment).

Useful early; over time, decompose retention into more useful inputs.

### HEART (Google)
Happiness × Engagement × Adoption × Retention × Task success.

Useful for design / UX-led measurement. Pair with quantitative engagement.

### Compound growth
Each input contributes to growth multiplicatively:
Growth Rate = (New + Resurrected) − (Churned) + Expansion

### Pirate metrics for marketplaces
Supply growth × Demand growth × Match rate × Transaction success × Repeat rate

## 7. Frequency-based engagement metrics

A useful slice of engagement:

| Metric | Definition | When useful |
|--------|------------|-------------|
| DAU | Daily active users | Real-time products (chat, social) |
| WAU | Weekly active users | Weekly-cadence products (productivity) |
| MAU | Monthly active users | Monthly-cadence products (admin) |
| DAU/MAU | "Stickiness" ratio | All consumer; > 50% is strong |
| WAU/MAU | Engaged WAU share | Productivity products |
| L7/L28 | Days active in last 7/28 | Habit strength |

Don't pick DAU as North Star, but DAU as a guardrail is fine.

## 8. Metric tree review cadence

A healthy tree is reviewed and pruned regularly:

| Cadence | Activity |
|---------|----------|
| Weekly | Team-level dashboards reviewed |
| Monthly | Input metrics reviewed for trends |
| Quarterly | NS + inputs reviewed; targets set |
| Annually | Metric tree pruned (sunset / add) |

Metrics rot. Yearly cleanup is non-negotiable.

## 9. Common pitfalls

- **NS that's a vanity metric.** Pick value-driven.
- **NS that can't move week-over-week.** Useless as a steering metric.
- **NS without guardrails.** Open to gaming.
- **30 KPIs on one dashboard.** No focus = no signal.
- **Different definitions across teams.** Aligned definitions, then aligned numbers.
- **No metric ownership.** Orphan metrics rot.
- **Tree never updated.** Reflects historical product, not current.
- **Inputs that don't combine to produce NS.** Tree is decorative.
