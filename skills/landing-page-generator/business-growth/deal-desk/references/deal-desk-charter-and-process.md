# Deal Desk Charter and Process

Reference for designing and operating a deal-desk function: full charter template, intake form specification, SLA framework, deal-desk team structure, and the operational rhythm that keeps the function effective.

---

## Charter — the foundational document

A deal-desk charter is the contract between deal desk, sales, finance, and legal. Without it, you have an informal review process that nobody trusts and everyone bypasses when it's inconvenient.

### Full charter template

```markdown
# Deal Desk Charter

## Purpose
Deal Desk is the cross-functional function that reviews, structures, and approves
non-standard commercial deals. Its mandate is to enable Sales to close faster
while keeping commercial, legal, financial, and operational risk within company
tolerance.

## Sponsors
- CRO (Sales sponsor)
- CFO (Finance sponsor)
- General Counsel (Legal sponsor)

## Scope

### In-scope deals
A deal must go through Deal Desk if ANY of the following apply:
- Total ACV exceeds $X
- Discount from list price exceeds Y%
- Contract length deviates from standard 12-month term
- Payment terms deviate from standard Net 30
- SLA commitments deviate from standard published SLA
- Custom legal language requested (any deviation from standard MSA)
- Multi-product bundle spanning >1 business unit
- Customer is in a regulated industry (financial services, healthcare, government)
- Customer-requested concessions: ramp deal, payment-on-acceptance, custom termination rights, MFN clauses, source code escrow, custom security questionnaire response
- Renewal with > 20% expansion or > 10% contraction
- Reseller or partner-mediated deal
- Deal involves a publicly named reference / case study commitment
- First deal with a strategic enterprise account (logo deal)

### Out-of-scope (Sales has full authority)
- Self-serve / PLG transactions
- Standard renewals at published renewal terms
- Trial extensions ≤ 30 days
- Add-ons to existing customers up to $X without other deviations

## SLAs

| Deal type | Time to deal-desk decision |
|-----------|---------------------------|
| Standard non-standard (no exec approval needed) | 1 business day |
| Needs CFO/CRO approval | 2 business days |
| Needs CEO/Board approval | 5 business days |
| Legal-only review (no commercial concession) | 2 business days |
| Custom security/compliance questionnaire response | 5 business days |

Deal-desk decision = recommend approve/counter/decline + route to approver(s).
Total elapsed (intake → executed contract) target: 5 business days for routine, 10 for complex.

## Intake

Deals enter Deal Desk via:
- Salesforce/HubSpot deal-desk request object (preferred)
- Slack form `#deal-desk-requests` (fallback)

Required fields (intake form enforces):
- Customer account name + size + industry
- Primary product(s) being sold
- Standard ACV (per published pricing)
- Requested ACV
- Specific deviation(s) requested: discount %, custom terms (list each)
- Justification: competitor situation, customer constraint, strategic rationale
- Customer's other vendor options
- Contract length + payment terms
- Implementation timeline + SLA expectations
- Required close-by date
- Sales rep + Sales manager
- Decision-maker on customer side

## Roles

### Deal Desk Lead
Owns the function. Sets policy in coordination with sponsors. Triages incoming
requests. Escalates complex deals. Owns metrics and reports quarterly to sponsors.

### Deal Desk Analyst
Day-to-day deal review. Builds packets. Routes to approvers. Tracks SLA.
Maintains intake-form spec and approval matrix.

### Standing Approvers
- CRO: deals > $1M ACV, discount > 40%, custom commission impact
- CFO: payment terms > Net 60, deals with revenue-recognition complexity, large multi-year discounts
- VP Sales: deals in their region/segment per matrix
- General Counsel: any custom legal language (red-lined MSA, custom terms)
- VP Engineering: custom SLA, custom security/compliance commitments
- VP Customer Success: custom onboarding commitments, ramp deals, success-criteria-based payment

### Consulted as needed
- Engineering Lead: technical feasibility of custom integrations
- Security Lead: compliance with security policies
- Finance Operations: revenue recognition treatment, deferred revenue handling

## Decision framework

Deal Desk recommends one of:
- **Approve** — deal is within policy or has compelling strategic rationale; risks understood and acceptable
- **Counter** — deal is close but has issues; specific changes requested
- **Decline** — deal violates non-negotiable policy or has unacceptable risk; reasoning + alternatives provided

Recommendations consider:
1. Financial: discount impact, margin impact, LTV, payback
2. Strategic: logo value, reference value, vertical foothold, competitive replacement
3. Risk: credit, compliance, integration, concession follow-through
4. Precedent: would approving this set a problematic precedent?
5. Sales reality: is the deal real, or wishful thinking?

## Outputs

For every Deal Desk-processed deal:
- Decision recorded in CRM (approve / counter / decline + reasoning)
- Approval packet archived (for audit / future precedent)
- Conditions explicit (expiration, contingencies, customer obligations)
- Single-instance language explicit when applicable

## Metrics

Tracked weekly, reported monthly to sponsors:
- Median time-to-decision per deal type
- 90th percentile time-to-decision
- Approval rate (% approved vs total requests)
- Sales rep NPS (quarterly survey)
- Discount-on-discount rate (customer negotiated further after approval)
- Win rate of approved deals
- Margin impact (deal desk decisions tracked against gross margin)

## Governance

- Charter reviewed quarterly by sponsors
- Approval matrix reviewed quarterly with sales leadership
- Material policy changes require sponsor sign-off
- Quarterly business review with sales, finance, legal sponsors

## Effective date
<date>

## Sign-off
- CRO: <signature>
- CFO: <signature>
- GC: <signature>
- Deal Desk Lead: <signature>
```

---

## Intake form — what to ask

A well-designed intake form is the difference between a packet that's approvable in 1 hour vs one that takes 3 days of back-and-forth.

### Field-by-field spec

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Customer name | Text | Yes | |
| Customer industry | Dropdown | Yes | (controls which approvers apply) |
| Customer size (employees) | Numeric | Yes | (correlates with regulatory complexity) |
| Customer revenue (annual, if known) | Numeric | No | |
| Country / region | Dropdown | Yes | (determines regional approver set + legal jurisdiction) |
| Primary product(s) | Multi-select | Yes | |
| Standard ACV (per published price) | Numeric | Yes | |
| Requested ACV | Numeric | Yes | |
| Discount % | Auto-calculated | n/a | (from ACVs above) |
| Contract length (months) | Numeric | Yes | |
| Payment terms | Dropdown | Yes | Net 0/15/30/45/60/90/Custom |
| Payment frequency | Dropdown | Yes | Annual / Quarterly / Monthly / Custom |
| SLA tier requested | Dropdown | Yes | Standard / Enhanced / Custom |
| Custom legal terms requested | Long text | Conditional | (Required if any deviation from standard MSA) |
| Justification narrative | Long text | Yes | (Free-text; 100+ chars enforced) |
| Customer's other vendor options | Long text | Yes | (Or "evaluation closed — only us") |
| Strategic value (rep's view) | Dropdown | Yes | Logo / Reference / Vertical / Expansion / Replacement |
| Required close-by date | Date | Yes | |
| Decision-maker on customer side | Text | Yes | (Name + title; if unknown, that's a yellow flag) |
| Champion on customer side | Text | Yes | |
| Implementation requirements | Long text | Conditional | (For custom integrations) |
| Reseller / partner involved | Yes/No | Yes | (If yes: which partner, what split) |
| Will customer commit to: case study? press release? reference call? | Multi-checkbox | Yes | |
| Quote attached (if any) | File upload | No | |
| Standard MSA red-line (if customer red-lined) | File upload | Conditional | |

### Common omissions that slow review

- "Customer wants a discount." — How much? Why? What's the alternative?
- "Custom legal terms" without the actual red-line attached.
- No close-by date → urgency unclear.
- No identified decision-maker → reps shopping internally for approval before customer has bought in.
- "We need this approved today" → if SLA exceptions become routine, the SLA is broken.

---

## SLA framework in depth

### How to set SLAs

Base SLAs on:
- **Approver availability** — if exec is in board meetings, 5-day SLA realistic; if always available, 2-day is reasonable
- **Decision complexity** — financial-impact analysis takes time; standard discounts don't
- **Volume** — high-volume deal desks need tighter SLAs to avoid queue blowout
- **Sales urgency** — quarter-end / month-end demand faster turnaround; bake into SLAs

### Publishing SLAs

Publish on a deal-desk wiki page that sales can reference. Include:
- SLAs per deal type
- Required intake fields
- Expected turnaround for each step (intake review, deal-desk analysis, approval routing, customer-facing decision)
- Escalation contact for SLA breaches
- Current queue / aging status (dashboard link)

### Measuring SLA performance

Weekly:
- % of deals decided within SLA
- Top 5 SLA breaches (root cause analysis)
- Aging deals (anything > SLA)

If consistently > 10% miss rate, the SLA is wrong (too aggressive for current volume / staffing) or the function is under-resourced.

### SLA exceptions

Some deals legitimately need faster turnaround:
- Sole-source deal at quarter-end
- Customer with a competing deadline (vendor RFP closing)
- Strategic must-win

Have a documented "expedite" process:
- Rep requests expedite via direct message to Deal Desk Lead
- Deal Desk Lead approves or denies (if everyone gets expedited, nobody does)
- Approved expedites get explicit faster SLA + dedicated analyst
- Track expedite usage; if > 20% of deals, something is wrong

---

## Operational rhythm

### Daily

- Deal Desk Lead reviews intake queue first thing in morning
- Analysts assigned new deals; SLA timer starts
- Aging dashboard reviewed (anything > 4h without assignment is escalated)
- Slack `#deal-desk` channel for sales questions

### Weekly

- Deal Desk team standup: aging review, blockers, approver bottlenecks
- Output: weekly metrics email to CRO/CFO/GC sponsors

### Monthly

- Approval rate, discount distribution, win rate analysis
- Sales feedback (informal: rep retros; formal: NPS once per quarter)
- Process improvements identified + scheduled

### Quarterly

- Threshold matrix review (discounts, ACV breakpoints) — adjust based on market conditions, win rate by discount band
- Charter review with sponsors
- Audit sample: pull 10-20 deals; were conditions met? did precedent hold?
- Headcount review

---

## Common process improvements (when starting from L1 manual operation)

| Step | Mature ops upgrade |
|------|--------------------|
| Intake | CRM-integrated form, validates required fields, auto-creates deal-desk record |
| Triage | Auto-assign to analyst on round-robin or by region |
| Packet generation | Templated packet auto-populated from CRM + intake fields |
| Approval routing | Auto-routes per matrix; serial vs parallel approval; SLA timer per approver |
| Reminders | Auto-nudge to approvers at 50% / 75% / 100% of SLA |
| Decision recording | Approval/decline recorded in CRM; conditions in approval packet |
| Archive | All packets stored in searchable archive (Notion / Confluence / Drive) |
| Audit | Quarterly random-sample audit; check packet completeness + condition follow-through |

---

## Charter sign-off — the conversation

When you bring the charter to sponsors, expect these objections:

| Objection | Response |
|-----------|----------|
| "This will slow down sales" | "It will speed up non-standard deals (current state: ad-hoc multi-week negotiations). Standard deals are out of scope — sales has full authority there." |
| "Too much process for our stage" | "Start with minimum viable: $X threshold, top 3 deal types. Expand as we grow." |
| "Approvers will be a bottleneck" | "Approval matrix delegates; SLAs measure; weekly aging review forces accountability. Bottleneck = visible." |
| "We trust our reps" | "Trust isn't the issue. Consistency, audit trail, and predictability are. Deal desk gives reps cover and gives finance/legal/exec visibility." |
| "We don't have headcount" | "Start as part-time function on someone's plate (often RevOps lead or VP Sales' chief of staff). Hire dedicated when volume justifies." |

---

## When deal desk isn't right (yet)

Deal desk is overhead. It's worth it when:
- Volume of non-standard deals > 1-2 per week
- Customer ACVs are big enough that mistakes hurt
- Multiple stakeholders need to be consulted (legal, finance, eng) per deal
- You're regulated or selling to regulated customers

Don't stand up a formal deal desk if:
- < 1 non-standard deal per month (RevOps lead handles ad-hoc)
- All deals are similar shape (no real "non-standard" pattern)
- Sales team < 5 people (informal coordination is fine)
- ACVs are small enough that bad concessions are immaterial

---

## Cheat sheet for charter design

| Question | Default answer |
|----------|----------------|
| What's in-scope? | Any deal that's not perfectly standard |
| Who owns the function? | Sales operations or RevOps; matrix-reports to CRO + CFO + GC |
| How many people? | 1 for < 50 deals/month, 2 for 50-200, 3+ for 200+ |
| What SLA is realistic? | 1-3 business days for routine; 5 for exec-needed |
| How often to review charter? | Quarterly |
| When does sales know it worked? | Median time-to-decision drops + win rate of approved deals stays stable + sales NPS positive |
