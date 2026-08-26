# Regulatory & Litigation Management Reference

Practical reference for tracking regulatory exposure and managing
litigation (active and pre-litigation) across the company's footprint.

## 1. Regulatory exposure mapping

For each jurisdiction the company operates in, map:

- **Sector regulators** (e.g., FDA, FCA, FINRA, EBA)
- **Data protection authority** (e.g., ICO, CNIL, GDPR supervisory authority)
- **Sanctions / export control** (OFAC, EU sanctions, dual-use)
- **Employment regulator** (varies by jurisdiction)
- **Tax authority requirements**
- **Industry-specific regs** (e.g., HIPAA, GLBA, sectoral)

Even a 100-employee company can have 30+ regulatory regimes applicable;
inventory them explicitly.

## 2. The regulatory calendar

A useful calendar tracks:

- **Filing deadlines** (financial reports, beneficial ownership, foreign agent)
- **Notification windows** (breach, incident, material change)
- **Renewal dates** (licenses, registrations, certifications)
- **New regulation effective dates** (EU AI Act, DORA, NIS2, sector updates)
- **Audit / examination scheduled dates**
- **Internal compliance deadlines** (annual training, attestation, reviews)

Run the calendar in a system every owner can see; emergency-only beats no
calendar at all.

## 3. Tracking regulatory change

A modern compliance program tracks both enacted and proposed regulation:

| Activity | Cadence |
|----------|---------|
| Monitor regulator news feeds | Weekly |
| Industry association updates | Weekly |
| Outside counsel alerts | As they arrive |
| Regulatory horizon scan | Quarterly |
| Material change impact assessment | Per change |
| Internal stakeholder briefing | Quarterly (or on event) |

Common services: Bloomberg Law, Lexology, Westlaw, sector-specific
trackers, plus outside counsel alerts.

## 4. Major regulatory regimes — quick reference

### Privacy
- **GDPR (EU/EEA)** — comprehensive personal data regime; supervisory authorities; DSARs; breach notification
- **UK GDPR** — substantially aligned to GDPR; ICO is supervisory authority
- **CCPA/CPRA (California)** — California privacy regime; CPPA enforces
- **Other US state privacy laws** — VA, CO, CT, UT, TX, FL, others (varying scope)
- **PIPEDA (Canada)** — federal; provincial variants in QC, BC, AB
- **Brazil LGPD** — comprehensive personal data regime
- **PDPA (Singapore)** — comprehensive personal data regime
- **South Korea PIPA** — strict consent regime

### Sector
- **HIPAA** (US health) — protected health information
- **GLBA** (US financial) — non-public personal information
- **PCI DSS** (global card industry) — cardholder data
- **HITECH** (US health) — health data security extension to HIPAA
- **FDA QSR / 21 CFR Part 11** — medical device + electronic records
- **CFPB** rules (US consumer finance)
- **SEC / FINRA** (US securities)
- **FCA / PRA** (UK financial)

### AI / data-driven
- **EU AI Act** — enacted; tiered obligations through 2027
- **NIST AI RMF 1.0** — US voluntary framework
- **ISO/IEC 42001** — certifiable AI management system
- **Sector AI guidance** (FDA, EU MDR for AI in medical devices)

### Cybersecurity
- **NIS2 (EU)** — applies broadly; member-state implementation
- **DORA (EU financial)** — operational resilience
- **NIST CSF 2.0** — US voluntary framework
- **SOC 2** — service organization controls
- **ISO/IEC 27001** — security management system
- **State breach notification laws** (US, state-by-state)

### Trade / sanctions
- **OFAC** (US Treasury sanctions)
- **EU sanctions**
- **Export controls** (US EAR / ITAR; EU dual-use)
- **Foreign Corrupt Practices Act (FCPA)** — US anti-bribery
- **UK Bribery Act** — broader than FCPA

## 5. Regulator engagement

When a regulator engages you:

| Engagement type | Default posture |
|-----------------|-----------------|
| Informal inquiry | Cooperative; engage outside counsel for response |
| Formal request | Privileged response; outside counsel handles |
| Investigation | Outside counsel leads; do not respond directly without coordination |
| Examination (regulated entity) | Cooperative; full preparation |
| Enforcement action | Outside counsel + insurance + board notification |
| Cease & desist | Immediate outside counsel + executive escalation |

Common errors: replying directly to a regulator without legal review,
producing documents without privilege screening, missing notification
windows.

## 6. Breach notification — the high-stakes window

Breach notification windows vary; build a matrix.

| Regime | Window | Trigger |
|--------|--------|---------|
| GDPR Art. 33 | 72 hours to supervisory authority | Likely to result in risk to rights |
| GDPR Art. 34 | Without undue delay to data subjects | High risk to rights and freedoms |
| HIPAA Breach Notification | 60 days to individuals | Breach of unsecured PHI |
| US state laws | Varies (often 30-60 days) | Depends on state |
| NIS2 | 24-hour early warning + further updates | Significant incident |
| EU AI Act Art. 73 | 15 days; immediate for fundamental rights | Serious incident high-risk AI |
| PCI DSS | Per card brand | Compromise of cardholder data |
| Sector-specific (FCA, SEC) | Varies | Specific events |
| Customer contracts | Often 24-72 hours | Defined per contract |

Pre-publish the matrix internally; tie it to the security incident
response runbook.

## 7. Litigation pipeline

Most companies see a pipeline of pre-litigation matters before any
actual lawsuit. Track them:

| Stage | Description | GC engagement |
|-------|-------------|---------------|
| Complaint / inquiry | Customer or third-party complaint | Document, monitor |
| Demand letter | Threatened claim | Outside counsel review |
| Settlement negotiation | Pre-suit settlement | Outside counsel |
| Litigation filed | Lawsuit served | Outside counsel litigation |
| Discovery | Document production, depositions | Coordinate with outside counsel |
| Trial / arbitration | Hearing | Outside counsel leads |
| Settlement or judgment | Resolution | GC approval + board notice if material |
| Appeal | Post-trial | Outside counsel |

Maintain a litigation register with: matter, plaintiff/defendant, status,
budget, exposure, next event, outside counsel.

## 8. Litigation hold

When litigation is reasonably anticipated, issue a hold:

### Steps
1. Identify custodians (employees with relevant information)
2. Issue hold notice (preserved as evidence)
3. Suspend relevant retention auto-deletion
4. Coordinate with IT for technical preservation
5. Periodic re-notice (annually minimum, on departure)
6. Release notice when matter concludes

Failure to issue hold is a sanctionable offense; spoliation findings
can be devastating.

## 9. Outside counsel management

### Panel
A typical panel: 3–6 firms across specialties.

- **Corporate / securities** — financing, M&A, securities compliance
- **IP** — patents, trademarks, litigation
- **Employment** — escalations, RIF, exec-level
- **Privacy / cybersecurity** — breach response, complex DPA, sector
- **Sector regulatory** — depends on industry
- **Litigation** — general commercial litigation

### Rate management
- Annual rate negotiation
- Alternative fee arrangements (AFA) for predictable matters
- Volume discounts where appropriate
- Periodic spend review by matter type and firm

### Performance
- Annual review of each firm
- Quarterly spend report
- NPS-style satisfaction check by the in-house partner

### eBilling
- Adopt eBilling at ≥ $2M annual outside spend
- Common picks: Onit, BrightFlag, SimpleLegal
- Enforce budget approvals; track variance

## 10. M&A legal workstream

For an active acquisition:

### Pre-LOI
- NDA + clean team for diligence
- Initial diligence scope

### Diligence
- Streams: corporate, IP, employment, privacy, security, regulatory, commercial, tax
- Issue list with materiality categorization
- Reps & warranties development (start from prior deals)

### Definitive agreement
- Merger/purchase agreement
- Disclosure schedules
- Reps & warranties insurance (often)
- Closing conditions
- Indemnification structure

### Closing
- Regulatory approvals (HSR, sector-specific, foreign)
- Closing conditions satisfied
- Officer's certificates
- Stockholder consent

### Integration
- Day-1 integration plan
- Employment / equity harmonization
- Customer/vendor contract assignment / consent
- Regulatory transition
- Litigation hold updates

## 11. Internal investigations

Triggered by: whistleblower report, regulatory inquiry, material allegation,
audit finding.

### Posture
- Privilege from the start
- Outside counsel typically (for independence + privilege)
- Audit committee oversight for material matters
- Document preservation immediate
- Witness interviews planned and structured

### Communication
- Need-to-know only
- Privileged communications marked
- No premature conclusions externally
- Regulator engagement coordinated

## 12. Ethics and reporting

A mature compliance program includes:

- Code of conduct with annual attestation
- Anonymous reporting hotline
- Investigation protocol for reports
- Anti-retaliation policy with teeth
- Annual ethics training
- Periodic audits of compliance with code

## 13. Common pitfalls

- **No regulatory calendar.** Missed deadlines are unforced errors.
- **Treating GDPR as "Europe's problem."** Extraterritorial; meaningful US exposure.
- **Litigation hold issued too late.** Spoliation risk; weak case.
- **No outside-counsel budget.** Spend balloons.
- **One firm for everything.** Lose specialization; conflicts.
- **AI vendors without no-training terms.** Privilege risk, IP risk.
- **No breach notification matrix.** Miss a window; pay a fine.
- **No litigation register.** Surprises in board meetings.
- **GC not on the AI council.** AI risk concentrates without legal eyes.
