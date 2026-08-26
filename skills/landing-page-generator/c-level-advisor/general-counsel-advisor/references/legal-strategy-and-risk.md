# Legal Strategy & Risk Reference

Practical reference for in-house legal leaders building or refreshing
a legal strategy and risk framework. Designed to be opinionated and
operational, not exhaustive.

## 1. The GC mandate — name your flavor

Most companies want all flavors of GC; you typically have budget for one or two:

| Flavor | Primary mandate | Reports to | Typical stage |
|--------|-----------------|-----------|---------------|
| **Defensive GC** | Risk, compliance, litigation | CEO or board | Regulated industry, post-incident |
| **Transactional GC** | M&A, financings, partnerships | CEO or CFO | Active dealmaker |
| **Commercial GC** | Sales enablement, contract throughput | CRO or CEO | High-volume commercial |
| **Strategic GC** | Governance, board, policy, public affairs | CEO | Late-stage / public |

Each flavor weights team composition and outside-counsel mix differently.

## 2. What a credible legal strategy answers

1. **What legal risks could materially impact the business?** (Top 5–10)
2. **What's the legal operating model?** (in-house mix, embedded, hub-and-spoke)
3. **What's the contract standards posture?** (one MSA, deviation discipline)
4. **What's the regulatory tracking system?** (calendar, owners, response)
5. **How is litigation managed?** (panel, budgeting, escalation)
6. **What's the M&A legal readiness?** (diligence pack, NDA templates)
7. **What does success look like in 12 months?** (3–5 KPIs)

## 3. Legal risk taxonomy

Group risks into 7 categories for easier tracking:

### Commercial
- Customer contract liability exposure
- Vendor concentration / single-supplier failure
- Counterparty default
- Contract dispute / breach
- IP licensing-in issues
- Pricing / discounting policy violations

### Regulatory
- Sector-specific (banking, healthcare, energy)
- Cross-border (sanctions, export controls)
- Industry change (new regulation enacted or proposed)
- Investigation or enforcement action
- Reporting / filing deadlines missed

### Privacy & data
- GDPR / CCPA / sector privacy non-compliance
- DSAR / breach response failure
- Cross-border data transfer issues
- Vendor / processor management gaps
- DPIA gaps for high-risk processing

### Security & cyber
- Material security incident
- Breach notification obligation
- Customer security commitment failure
- Regulatory cyber requirements (NIS2, DORA, sector)

### IP
- Patent infringement (asserted or defensive)
- Trademark dispute
- Trade secret theft / misappropriation
- Open-source compliance
- IP ownership questions (contractor work, M&A)

### Employment
- Discrimination / harassment claim
- Misclassification (contractor vs employee)
- Severance / RIF execution
- Trade-secret / non-compete enforcement
- Cross-border employment / mobility

### Corporate / governance
- Securities (10b-5, insider trading)
- Equity-grant administration
- Board governance gaps
- D&O exposure
- M&A reps & warranties

### Litigation
- Active matters and exposure
- Pre-litigation pipeline
- Litigation hold compliance

## 4. Risk-scoring approach

For each risk, assess:
- **Severity** (1–5) — financial + reputational + operational impact if realized
- **Likelihood** (1–5) — probability over the next 12 months
- **Velocity** (1–3) — how quickly it could materialize
- **Detection** (1–3) — how early you'd see it coming
- **Mitigation strength** (0–5) — controls in place

Exposure = Severity × Likelihood. Use `legal_risk_register.py` to drive
consistent scoring across the register.

## 5. Operating model patterns

### Pattern A — Solo GC + outside panel
- < ~50 employees / pre-Series B
- GC handles commercial, equity, IP basics, employment basics
- Outside counsel: corporate, IP, employment, litigation
- Cost: $250K–$500K base + ~$300K–$500K outside spend

### Pattern B — GC + 2-4 in-house FTEs
- Series B–C
- Roles: GC, commercial counsel, employment counsel (often dotted to CHRO), legal ops
- Outside counsel: corporate, IP, sector regulatory, employment escalations, litigation
- Cost: $1M–$3M total

### Pattern C — Hub-and-spoke
- Series C+ / scale-up
- Hub: GC + commercial + privacy/security + employment + IP + corporate + legal ops
- Spokes: BU-embedded counsel for major product lines
- Outside panel: 3–6 specialist firms
- Cost: $5M–$15M typically

### Pattern D — Functional structure
- Public or near-public companies
- Functional groups: corporate/securities, commercial, IP, employment, regulatory, litigation
- Centralized legal ops
- Cost: $15M+

## 6. Legal ops — the often-missed function

Legal operations is the engine that scales the legal function. Common scope:
- CLM administration
- eBilling and outside counsel management
- Matter management
- Knowledge management (template library, playbooks)
- Reporting (metrics, spend, cycle time)
- Legal tech selection and operations
- Project management for major initiatives

A 5-person legal team can run without dedicated legal ops; a 15-person
legal team usually can't.

## 7. KPIs that matter

Pick 3–5 for the board. Common picks:

### Throughput
- Contract cycle time (median + P75) by tier
- NDA cycle time (often <1 day target)
- Standard MSA cycle time (target depends on segment)

### Risk
- Open audit / regulatory findings — by age
- Open litigation matters — by exposure
- Material contract deviations — by tier and counterparty
- DSAR fulfillment time

### Spend
- Total legal spend as % of revenue
- Outside counsel spend by matter type
- Legal spend per matter

### Quality
- Contract value lost / saved per quarter
- Deal terms scored against playbook
- Customer / vendor satisfaction with legal touch

Avoid:
- "Contracts signed" — incentivizes throughput at expense of quality
- "Hours worked" — meaningless
- Composite legal scores — bury underlying signals

## 8. The 90/180/360 plan for a new GC

**Day 0–90 — Listen and inventory**
- Meet every exec individually; capture top friction
- Pull all active matters; review with prior outside counsel
- Inventory contract portfolio (count, value, deviations)
- Identify the 3–5 highest-exposure risks
- Map regulatory exposure across jurisdictions

**Day 91–180 — Standardize and shore up**
- Publish or refresh: MSA, NDA, DPA, employment templates
- Stand up the matter management system / refresh
- Define contract approval thresholds (deviations, sign authority)
- Establish the legal risk register with quarterly review
- Define the litigation hold process

**Day 181–360 — Scale and measure**
- Hire or restructure the in-house team to the target operating model
- Tune the outside-counsel panel (rates, performance reviews)
- Implement legal-tech (CLM, eBilling, matter mgmt)
- Publish KPIs to the board
- Plan year-2 priorities from instrumented baseline

## 9. Board reporting cadence

| Audience | Cadence | Content |
|----------|---------|---------|
| Full board | Quarterly | Top matters, regulatory updates, risk register, asks |
| Audit committee | Quarterly | Litigation, regulatory, internal investigations, ethics |
| Compensation committee | As needed | Equity, employment matters affecting execs |
| Nominating / governance | Annually | Governance gaps, D&O, board composition |

Material events (breach, regulator inquiry, material litigation) trigger
out-of-cycle reporting.

## 10. Cross-functional integration

A modern GC sits on or supports several cross-functional bodies:

| Body | GC role |
|------|---------|
| AI Council | Co-owns AI policy with CAIO |
| Risk Committee | Often chair or vice-chair |
| Security incident response | Privilege, breach notification, regulatory |
| Privacy office | Often the GC's responsibility unless separate DPO |
| Ethics committee | Often chair |
| M&A IC | Diligence, deal structure, integration risk |
| Compensation / equity | Approvals, securities compliance |

## 11. Privilege management

Privilege is fragile and easily destroyed. Common protections:

- Clear marking of legal communications ("attorney work product", "privileged")
- Limited distribution — privilege can be waived by sharing too widely
- Use of outside counsel for sensitive matters (extra layer of protection)
- Separate retention for privileged materials
- Training non-legal staff on privilege basics
- Discovery readiness — pre-thought-through document retention

## 12. Common pitfalls

- **GC reporting to CFO at scale.** Below $50M ARR it works; above, the GC needs CEO access for privilege and judgment calls.
- **Legal as a "no" department.** Replaced with workarounds; lose visibility into risk.
- **No standard templates.** Every deal bespoke; throughput dies.
- **Outside counsel without budgets.** Matter creep; spend balloons.
- **Risk register reviewed annually.** Quarterly is the minimum; events drive updates.
- **GC isolated from product.** Misses regulatory exposure baked into product decisions.
