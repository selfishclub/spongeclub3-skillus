# Retention & Expansion Frameworks

Practical reference for the NRR / GRR levers and the operational programs
that move them.

## 1. NRR / GRR — the math and what it hides

**Net Revenue Retention (NRR):**
```
NRR = (Starting ARR + Expansion - Downgrades - Churn) / Starting ARR
```

**Gross Revenue Retention (GRR):**
```
GRR = (Starting ARR - Downgrades - Churn) / Starting ARR
```

NRR includes expansion; GRR is the pure retention number. Track both — NRR
tells you the trajectory of existing customers; GRR tells you the
underlying durability.

### Benchmarks (rough, 2026)

| Segment / Motion | NRR median | NRR top quartile | GRR median |
|------------------|------------|------------------|------------|
| SMB SaaS | 95–105% | 110%+ | 80–88% |
| Mid-Market SaaS | 105–115% | 120%+ | 88–93% |
| Enterprise SaaS | 110–120% | 125%+ | 92–96% |
| PLG | 105–115% | 130%+ | 85–92% |
| Consumption / usage | 115–130% | 140%+ | 88–94% |

A 1-point NRR move on a $100M base = $1M ARR/yr; over 3 years compounding, much more.

## 2. NRR drivers — actually moveable

In order of typical impact:

1. **Onboarding-to-first-value time** — every week of delay drags NRR
2. **Adoption depth in first 90 days** — predicts year-1 NRR
3. **Expansion paths tied to usage** — durable, repeatable
4. **Executive engagement in top-20** — defends large logos
5. **Renewal motion discipline** — 90/60/30 day playbook, not fire drill
6. **Health-score-driven CSM allocation** — focus the team's time
7. **Save-room execution** — captures last-mile losses
8. **Pricing-model alignment** — per-seat works only if seats grow

What rarely moves NRR:
- More NPS surveys
- Bigger CSM team without better book design
- Discount-heavy save offers
- One-off advocacy programs

## 3. The renewal motion (90/60/30 standard)

A standard motion every CSM follows:

**90 days out:**
- Renewal health snapshot
- Identify exec sponsor + champion
- Discover any disruption: org change, vendor consolidation, budget changes
- Initial commercial conversation

**60 days out:**
- Renewal proposal in hand
- Procurement engaged if required
- Any technical asks (e.g., a feature gap) escalated and tracked
- Save room engaged if health is red

**30 days out:**
- Signed renewal or formal extension
- Escalate to CCO if not closed
- Risk-tier categorization: lost / extended / on track

If renewals consistently slip past 30 days, the motion isn't working.

## 4. The save room

A weekly forum reviewing at-risk accounts.

**Membership:** CSM, save team lead, engineering escalation contact, GTM
ops, sometimes a finance / product partner.

**Agenda:**
- New entries (last week)
- Active interventions (status, owner, next action)
- Wins / losses since last meeting
- Patterns (driver concentration, segment risk)

**Discipline:**
- Every at-risk account has an owner and a next action
- Interventions classified by driver (usage, technical, commercial, relationship)
- Postmortems on losses; pattern detection on wins
- Save rate tracked (target: save-room saves / save-room entries)

## 5. Health score that actually works

Start simple. A 6-component model beats a 16-component model.

### Recommended starter components

| Component | Weight | Signal |
|-----------|--------|--------|
| Product usage | 25% | Active users, frequency, depth |
| Engagement | 20% | Communication response, training attendance, exec touches |
| Support / sentiment | 15% | Tickets, CSAT, sentiment |
| Onboarding / activation | 15% | Milestones met on schedule |
| Adoption depth | 15% | % features / modules in active use |
| Renewal posture | 10% | Renewal indicators 90 days out |

Calibrate quarterly against actual churn. Drop components that don't
predict; tune weights; add new signals if they earn it.

### Anti-pattern: the "perfect" score
A health score with 17 components, machine-learned weights, no one knows
how it works. Rots fast. Better: a simple model you can defend to a CSM.

## 6. Expansion motions

Two distinct motions; pick which applies per opportunity:

### Usage-driven expansion (CSM-owned)
- Seats added as the customer grows
- Usage tiering (more data, more transactions)
- Feature uptake (adding modules they're already eligible for)
- New use cases on the same product

Owner: CSM. Comp: typically share of expansion ARR.

### Cross-sell expansion (Account-management-owned)
- New product lines
- New business units
- New regions
- Multi-year, multi-product deals

Owner: Account Manager or AE. Comp: full sales quota credit.

### The boundary question
If CSMs carry quota for cross-sell, they're sales. If AEs own usage
expansion, the CSM has no leverage. Pick a clean split; review yearly.

## 7. Churn types and counter-actions

Different churn types deserve different programs.

| Churn type | Description | Best counter |
|------------|-------------|--------------|
| **Adoption churn** | Never adopted | Better onboarding; activation focus |
| **Usage churn** | Adopted then declined | Usage monitoring; CSM intervention; product fix |
| **Sponsor churn** | Champion left | Multi-thread; exec sponsorship from day 1 |
| **Technical churn** | Product gaps / bugs | Feature roadmap; technical CSM |
| **Commercial churn** | Price / packaging | Pricing review; tier engineering |
| **Strategic churn** | Customer pivoted away | Hard to prevent; sometimes the customer was wrong-fit |
| **Forced churn** | Failed payment, expired card | Payment health; dunning playbook |
| **Consolidation churn** | Vendor consolidation push | Get to the consolidator early |

Tag each churn with type; investment shifts based on which dominates.

## 8. Pricing model alignment

Pricing model alignment is the silent NRR driver. Mismatches:

- **Per-seat model + flat customer headcount → flat NRR** — explore consumption or tiering
- **Flat enterprise license + heavy usage → margin compression** — meter and tier
- **Consumption-based pricing + lumpy customer adoption → revenue volatility** — minimum commits, rollover

Pricing changes have to be done carefully — refer to `business-growth/pricing-strategy`
for the deeper playbook.

## 9. QBRs and EBRs — when they earn their keep

**Quarterly Business Review (QBR):** structured customer conversation
covering adoption, outcomes, and roadmap.

When QBRs are worth it:
- Enterprise segment with named exec sponsor
- Customers buying outcomes, not features
- Renewal cycle ≥ annual

When QBRs aren't worth it:
- SMB / PLG; replace with quarterly digital summary
- Mid-market; replace with usage-driven check-ins triggered by signals
- When the customer's executive sponsor stops attending — escalate, don't keep cadence

**Executive Business Review (EBR):** semi-annual or annual; CEO/CCO + customer C-level.
Reserved for top 20 accounts. ROI is real but lift is high.

## 10. Save offers — when they work, when they're poison

Save offers (discount, extension, additional resources) work when:
- The customer has a temporary cash constraint
- The driver is commercial, not product or trust
- The size of the offer is proportional to the deal value and the risk

Save offers are poison when:
- Used to paper over a product / trust issue (the issue resurfaces in 1–2 quarters)
- Discount levels become known and gamed by procurement
- Becomes the default response in the save room

Track save offers separately. If > 20% of saves involve discount > 15%, you
have a structural problem, not a churn problem.

## 11. The customer advocacy bench

A high-functioning CX org builds a deliberate advocacy bench:

- **20–30 customers** who'll do references calls
- **5–10 customers** who'll speak publicly
- **3–5 customers** who'll co-author case studies / appear at events
- **Lighthouse logos** who define product narrative

Build, don't accidental-discover. Cultivate through CX, not marketing
alone; marketing operationalizes; CX maintains relationships.

## 12. Common pitfalls

- **NRR as the only metric.** It hides expansion-masked churn; pair with GRR + logo churn.
- **Renewals owned by no one specific.** Renewals slip to the last week; expect surprises.
- **Save room without root cause.** Treats symptoms; pattern goes unaddressed.
- **Health score that never changes.** Models rot; recalibrate quarterly.
- **CSMs paid only on retention.** No leverage; can't influence expansion.
- **CSMs paid only on expansion.** Renewals get neglected.
- **QBR every quarter for everyone.** Wastes mid-market time; reserve for enterprise.
