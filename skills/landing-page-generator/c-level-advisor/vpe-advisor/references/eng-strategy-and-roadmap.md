# Engineering Strategy & Roadmap Reference

Practical reference for capacity planning, investment allocation, and
the engineering-product-business roadmap interface.

## 1. What an engineering strategy answers

The VPE's engineering strategy answers:

1. **What are our engineering bets?** (Capacity allocation across themes)
2. **What's our delivery model?** (Cadence, rituals, release engineering)
3. **What's our quality bar?** (DORA targets, SLOs, reliability investment)
4. **What's our org shape?** (Squads, platform, embedded)
5. **What's our talent thesis?** (Hire, retain, develop)
6. **What's our productivity investment?** (Tooling, platform, paved paths)
7. **What's the KPI dashboard?**

A strategy without explicit capacity allocation is decoration.

## 2. The 3-bucket investment model

A pragmatic model for allocating engineering capacity:

- **Run the business (50–60%):** keep the lights on — bug fixes, security
  patches, on-call, support escalations, tech debt that's burning, customer
  blockers, compliance.
- **Grow the business (30–40%):** ship the product roadmap, feature delivery,
  performance improvements that move business metrics.
- **Transform the business (10–20%):** ambitious bets, new product lines,
  architectural rewrites, platform investments.

Drift away from these proportions usually indicates dysfunction. Too
much "run" = stuck in maintenance. Too much "transform" = product
roadmap stalls.

## 3. Capacity planning math

### Useful capacity per engineer (per quarter)
Start with: 1 engineer × 12 weeks = 12 engineer-weeks.

Subtract:
- ~15–20% PTO / holidays / sick
- ~10% on-call rotation overhead
- ~5–10% recruiting (interviews) for everyone
- ~10–15% meetings / overhead
- ~5% support tax (Slack questions, customer escalations)

**Result: ~6–8 useful engineer-weeks per quarter** for actual feature
delivery.

For a 5-engineer squad: 30–40 engineer-weeks of real capacity per
quarter. Most product roadmaps overcommit by 2–3x this number.

### Adjustments
- New engineer in first 90 days: 30–50% useful capacity
- New engineering manager: 50–70% useful capacity (some IC time)
- Engineer on platform team: 80–90% (less context-switch tax)
- Engineer in regulated environment: 60–70% (compliance overhead)

### The "fully loaded engineer cost"
- Comp: $200K base + $200K stock + benefits = ~$500K
- Tooling, devices, software: $5K–$15K
- Office / overhead: $10K–$50K
- Allocated platform infra: $5K–$20K

A fully-loaded engineer is $500K–$700K/year in a major US market. Plan
roadmap value accordingly — every quarter of an engineer is $125K–$175K
of opportunity cost.

## 4. Roadmap negotiation with product

The classic dysfunction: product commits, engineering can't deliver,
trust erodes.

### Healthy patterns
- Joint capacity reviews quarterly
- Product roadmap shows confidence bands (not just commits)
- Engineering surfaces tech debt budget upfront
- Stretch goals identified separately from commitments
- Changes mid-quarter require trade-offs (something else drops)

### Anti-patterns
- "Stretch" goals that are always expected to land
- Roadmap that ignores on-call, support, tech debt
- Mid-quarter additions with no trade-off
- Confidence in commits decoupled from team velocity history

## 5. Roadmap horizon

A useful roadmap has multiple horizons:

| Horizon | Specificity | Confidence |
|---------|------------|------------|
| Current quarter | Specific features, dates | High |
| Next quarter | Themes + key initiatives | Medium |
| Quarters 3–4 | Themes only | Low |
| Year 2+ | Strategic direction | Aspirational |

Don't pretend Q4 looks like Q1. Surface uncertainty explicitly.

## 6. Annual planning rhythm

### August / September (pre-Q4)
- Review trailing year: themes, hits, misses, surprises
- Pull customer signals (VoC, sales feedback)
- Define annual themes for next year
- Capacity baseline projection

### October (early Q4)
- Senior leadership planning offsite
- Annual themes ratified
- Per-pillar plans drafted
- Hiring plan drafted

### November (mid Q4)
- Per-squad planning
- Q1 commits + Q2 themes
- Budget locked
- Hiring plan locked

### December (end Q4)
- Per-engineer goals
- Comp / promotion / bonus cycles
- Org changes if any
- Year-end communication

### January (start Q1)
- Kick off Q1
- Communicate annual plan widely
- Begin Q1 execution

## 7. Quarterly planning rhythm

### Pre-quarter (2-3 weeks out)
- Squad-level draft of commits + stretch
- Product reviews quarterly with engineering
- Cross-team dependency identification

### Quarter kickoff
- All-hands or pillar-hands on commits
- Per-squad goals published
- KPI dashboard refreshed

### Mid-quarter check-in
- Squad-by-squad health review
- Adjustments for missed dependencies, new info
- Surface risk early

### End of quarter
- Retrospective per squad
- Cross-team retro at pillar level
- Carry-over rules (what spills to next quarter)

## 8. Capacity and the org chart

When capacity feels short:

1. **Look at WIP** — too much in-flight is the most common cause
2. **Look at coordination overhead** — too many teams touching same code
3. **Look at on-call burden** — noisy services kill productivity
4. **Look at the meeting load** — death by meeting
5. **Look at tooling** — slow CI is a 20% tax
6. **Then consider headcount**

Adding engineers without addressing 1-5 makes things worse for 1-2
quarters.

## 9. Hiring as a capacity strategy

### When hiring helps capacity
- Specific bottleneck capability is missing (e.g., ML, security)
- A team is consistently understaffed for its scope
- New scope requires new specialty (e.g., entering a new market)

### When hiring hurts
- Onboarding cost exceeds expected contribution in time available
- Existing team is dysfunctional — new hires inherit dysfunction
- Hiring bar lowered to meet headcount targets

### Ramp expectations
- 30 days: oriented, first PR merged
- 60 days: contributing to active sprints, modest features
- 90 days: full sprint contributor
- 6 months: real influence, owns features
- 12 months: senior contribution at hired level

## 10. Engineering business reviews

### Monthly engineering review
- DORA metrics by team
- Incident count + severity
- On-call health
- Squad-level updates (commits, blockers, asks)
- Hiring pipeline status
- Tech debt + reliability investment level

### Quarterly business review (QBR)
- Themes progress vs commits
- Material misses + recovery plans
- Talent trajectory (hires, attrition)
- Investment posture (run / grow / transform)
- Asks for next quarter

### Annual review
- Themes hit/miss
- Org health (DevEx, eNPS)
- Key hires, key losses
- Architecture evolution
- Strategy for next year

## 11. Board reporting

A useful engineering board section:

- **Delivery** (~30%): DORA trends, key shipments, key misses
- **Quality** (~25%): SLO posture, incidents, customer-reported quality
- **Talent** (~25%): headcount, hires, attrition, key roles
- **Investment** (~10%): bucket mix vs target, major projects
- **Asks** (~10%): budget, org structure, product priority

Keep to one page; appendix for detail.

## 12. Common pitfalls

- **Roadmap commits without capacity math.** Sets up consistent disappointment.
- **All capacity allocated to features.** No room for incidents, support, tech debt.
- **Hiring as the answer to every capacity problem.** Often makes it worse.
- **Annual planning with no mid-year adjustment.** Reality changes; plans must too.
- **Themes that are just feature lists.** Themes should be strategic intents.
- **No retrospective discipline.** Same mistakes repeat quarterly.
- **Cross-team dependencies discovered mid-quarter.** Capacity blown; trust eroded.
- **Eng KPIs not tied to business outcomes.** "Engineering shipped a lot but the business didn't grow."
