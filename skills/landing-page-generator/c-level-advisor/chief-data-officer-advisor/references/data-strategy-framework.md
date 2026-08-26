# Data Strategy Framework

Practical reference for Chief Data Officers building or refreshing a data
strategy. Designed to be opinionated.

## 1. The four flavors of CDO — pick yours honestly

Most companies want all four; you typically get budget for one or two.
Picking is not optional — pretending you're all of them produces mush.

| Flavor | Primary mandate | Reports to | Typical context |
|--------|-----------------|-----------|-----------------|
| **Defensive CDO** | Risk, compliance, audit response | GC, CRO, or CEO | Regulated industry, post-incident |
| **Architect CDO** | Platform, governance plumbing, modernization | CTO or CEO | Tech-debt-heavy, replatform underway |
| **Governor CDO** | Policy, stewardship, data quality | COO or CEO | Data inconsistencies break the business |
| **Monetizer CDO** | Data products, AI/ML enablement, revenue | CEO | Established company looking to commercialize data |

Strategy specifics differ sharply across flavors. A monetizer CDO who
spends 60% of their time on governance posture has the wrong job.

## 2. What a credible data strategy answers

1. **What business outcomes does data move?** (retention, revenue, cost, risk, speed)
2. **What are the critical data domains?** (customer, product, transaction, supplier, regulatory)
3. **What's the operating model?** (central, federated, mesh, hybrid)
4. **What's the platform direction?** (warehouse-first, lake-first, lakehouse, polyglot)
5. **What's the governance posture?** (controls, evidence, enforcement teeth)
6. **What's the monetization thesis (if any)?**
7. **What does success look like in 12 months?** (3–5 KPIs, attributable)

If you don't have an answer to each, you have an aspiration, not a strategy.

## 3. Strategic themes (pick 3–5)

Common themes worth picking from:

### Foundation
- **Single source of truth for [domain]** — start with the most-fought-over domain (usually customer or product)
- **Data platform modernization** — replatform off legacy DWH or fix tool sprawl
- **Governance baseline** — policies, stewardship, classification, basic catalog

### Reliability
- **Quality SLAs on critical datasets** — freshness, completeness, accuracy
- **Lineage end-to-end** — from source to consumer
- **Pipeline reliability** — observability, on-call, SLOs

### Use cases
- **Self-service analytics** — BI for the long tail, well-governed
- **AI/ML enablement** — feature store, model-ready datasets, governance
- **Embedded analytics** — analytics inside the product
- **Data monetization** — productize data (internal apps, external products, partnerships)

### Compliance
- **GDPR/CCPA/sector readiness** — DSARs, consent, retention, residency
- **Audit response** — internal audit cadence, external audit prep

Pick 3–5. Resist adding the sixth — it dilutes everything else.

## 4. Target operating model (TOM)

### Pattern A — Central platform + analytics
Single team owns platform, governance, analytics, and (often) data science.

| Fits when | Breaks when |
|-----------|-------------|
| <200 engineers, single BU, early maturity | BUs need to self-serve and they don't trust the center |
| Highly regulated industry where consistency matters most | Pace of change is too high for one team |

### Pattern B — Federated with domain ownership
Each domain (or BU) owns its data team; light platform standards.

| Fits when | Breaks when |
|-----------|-------------|
| Strong BU autonomy, mature engineering culture | Standards aren't enforced; quality and governance vary wildly |
| Diverse use cases per domain | Cross-domain analytics fall apart |

### Pattern C — Data mesh
Domains own data products; central platform team provides a data-product
platform; federated governance via committee.

| Fits when | Breaks when |
|-----------|-------------|
| >500 engineers, true domain ownership, strong product culture, willing to invest 2+ years | Org has weak product discipline (mesh becomes mush) |
| Need to scale data without scaling a central team linearly | Domains are too small or volatile to own a "product" |

### Pattern D — Hub-and-spoke (recommended default)
Central hub owns: platform, governance, catalog, quality tooling, classification, audit prep.
Spokes (domain teams) own: data products, transformations, quality outcomes, BI for their domain.

The hub publishes standards; the spokes follow them. The hub measures
adherence and brings up gaps to the data council.

## 5. Monetization thesis — three flavors

Don't claim a monetization thesis if you don't have one.

### Internal monetization
- **Mechanism:** new internal apps and decisions powered by data
- **Owner of value:** the consuming team's P&L
- **Measurement:** attribution to business KPI (revenue, cost, retention)
- **Risk:** under-measured; often invisible

### External data product
- **Mechanism:** sell data products, APIs, or insights to customers
- **Owner of value:** the data org's P&L
- **Measurement:** product revenue, gross margin, NDR
- **Risk:** privacy / consent; commercial terms vs cost of building

### AI-enabled product
- **Mechanism:** data feeds AI features in the product; ML drives outcomes
- **Owner of value:** product P&L (data org enables)
- **Measurement:** AI-attributable outcome (conversion, retention)
- **Risk:** double-counting; AI-attributable measurement is hard

If you can't say which one(s) you're pursuing, the monetization claim is decorative.

## 6. Prioritization heuristics

### The 3-bucket portfolio (mirrors AI bucketing)

- **Bucket 1 — Run the data org.** Pipeline reliability, governance baseline, quality SLAs, audit prep. ~50%.
- **Bucket 2 — Grow the data org.** Self-service expansion, new domain onboarding, advanced analytics. ~35%.
- **Bucket 3 — Transform the business.** New data products, AI enablement, monetization. ~15%.

Drift toward Bucket 3 looks exciting and usually fails — the foundation
can't carry it.

### Scoring (used by `data_platform_evaluator.py` and `data_maturity_assessor.py`)
- **Strategic fit** — alignment to themes (0–5)
- **Value** — magnitude of business impact (0–5)
- **Confidence** — data quality + prior art (0–5)
- **Risk** — model risk, regulatory, vendor lock-in (0–5; penalty)
- **Time-to-value** — months to first usable output

### Kill criteria (publish in advance)
- The pilot can't reach the published threshold within 1 quarter
- The data quality cost more than the use case is worth
- Vendor lock-in becomes existential
- Regulatory change makes the use case non-viable

## 7. KPIs that matter

Pick 3–5. Common picks:

- **Critical-dataset SLA hit rate** (freshness + completeness ≥ threshold)
- **Time-to-insight** for new analyses (median, by complexity tier)
- **Data product count + adoption** (with usage; not just published)
- **Audit findings — open and overdue** (governance health)
- **Mean time to detect / restore** for data incidents
- **% of critical fields with documented lineage**
- **Data-attributable business KPI** (with named methodology)

Avoid:
- "Tables in the warehouse" — incentivizes copying
- "Dashboards published" — incentivizes shelfware
- "Engineers using the platform" without depth

## 8. The 90/180/360 plan

**Day 0–90 — Inventory and stabilize**
- Inventory: domains, datasets, pipelines, tooling, headcount, spend
- Stand up the data council (exec) + data governance working group (technical)
- Publish a data classification policy + an interim catalog
- Pick the 3–5 strategic themes; ratify with the CEO and CTO

**Day 91–180 — Platform and governance**
- Pick the target platform stack; publish a one-page architecture
- Define quality SLAs on 5–10 critical datasets; instrument them
- Stand up the model approval / data product approval workflow
- Sign or consolidate the 2–3 anchor vendor contracts

**Day 181–360 — Ship and measure**
- Ship 2–3 named data products with named owners and SLAs
- Publish KPIs to the board with a quarter of trend
- Pass the first internal audit on the new governance program
- Plan year 2 from the platform you've now proven

## 9. Executive frictions — and the moves

| Friction | Move |
|----------|------|
| CFO wants ROI per dataset | Move to a data-product mindset; cost-attribute per product |
| CTO wants data in engineering | Hub-and-spoke; share infra ownership |
| CISO blocks the lake | Co-author classification + access policy; pilot a sanctioned pattern |
| GC won't approve the data sale | Engage early with a privacy impact assessment |
| BUs run their own analytics with no governance | Self-serve with guardrails > policing |
| Board asks "are we behind on data?" | Show the portfolio (themes × bets × KPIs), not the architecture diagram |

## 10. Common pitfalls

- **A strategy with no kill criteria.** You'll fund zombies.
- **One huge governance committee.** Split exec council from technical working group.
- **Catalog without enforcement.** Wire classification into access; otherwise it's a wiki.
- **Quality as a central problem.** Domain owners must own; platform provides tooling.
- **Replatforming to keep busy.** Replatforming is a tactic; if it doesn't unlock a named use case, don't do it.
