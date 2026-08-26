# Data Governance & Quality Reference

A pragmatic reference for the governance and quality halves of the CDO
mandate. Anchored on DAMA-DMBOK v2, with modern additions for cloud
warehouses, lake/lakehouse architectures, and AI/ML data needs.

## 1. Governance pillars (DAMA-DMBOK)

DMBOK enumerates 11 knowledge areas. For practical executive-level use,
group them into 5 pillars:

### A) Data governance (the umbrella)
- Policies and standards
- Roles and accountability (data owners, stewards, custodians)
- Governance bodies (council, working group)
- Compliance and audit

### B) Data architecture and modeling
- Reference data architecture
- Logical and physical models
- Master data management (MDM)
- Reference data management (RDM)

### C) Data operations
- Storage and platform operations
- Integration and interoperability
- Data warehouse / lake operations

### D) Data quality
- Quality dimensions and metrics
- Quality SLAs per dataset
- Incident response and remediation

### E) Data security and privacy
- Classification and access
- Privacy compliance (GDPR, CCPA, sector regs)
- Consent management
- Retention and minimization

## 2. Governance bodies — a two-tier model

### Tier 1 — Data Council (executive)
- **Chair:** CEO or CFO; **Sponsor:** CDO
- **Members:** CTO, CISO, GC, CHRO, business-line heads
- **Cadence:** quarterly (or monthly during major changes)
- **Mandate:** strategy, spend, policy ratification, escalations
- **Decision rights:** budget, scope, top-risk acceptance

### Tier 2 — Data Governance Working Group (technical)
- **Chair:** Head of Data Governance; **Sponsor:** CDO
- **Members:** Data owners, stewards, platform lead, privacy lead, security lead
- **Cadence:** biweekly
- **Mandate:** policy detail, data product approval, quality SLAs, classification reviews
- **Decision rights:** can require remediation; can block new ingestion; can publish standards

Plus working groups as needed (privacy, MDM, AI/ML data).

## 3. Roles — owners, stewards, custodians

| Role | Accountable for | Typical seniority |
|------|-----------------|-------------------|
| Data owner | Definition + meaning + classification of a data domain | Business leader (VP/Director) |
| Data steward | Quality and stewardship operationally | Manager / Sr IC, business or data side |
| Data custodian | Storage, access, technical care | Data engineer / platform |
| Privacy lead | Personal data handling | DPO / privacy office |
| Security lead | Classification and access controls | CISO org |
| Catalog admin | Catalog hygiene | Data governance team |

Common confusion: owners ≠ producers. The owner is accountable for the
data; the producer is whoever generates it. They may be different people.

## 4. Data classification (the table-stakes policy)

Most organizations standardize on 4 tiers:

| Tier | Examples | Default treatment |
|------|----------|-------------------|
| **Public** | Marketing site copy, published reports | Open access |
| **Internal** | Internal dashboards, product analytics | Authenticated org access |
| **Confidential** | Customer data, contract terms | Need-to-know, audit logged |
| **Restricted** | PII subject to GDPR, PCI cardholder data, PHI, source code | Encrypted, masked outside originating domain, strict access, audited |

The classification ties to access (RBAC + ABAC), to encryption requirements,
to retention, and to where data can live (residency). Without wiring
classification to controls, the policy is decorative.

## 5. Catalog — what to require, what to skip

A catalog earns its keep when it answers:

- Where does this dataset live, and what does it represent?
- Who owns it; who is the steward?
- What's its classification and retention?
- What's its lineage (upstream sources, downstream consumers)?
- What's its quality SLA and current state?
- Is it certified for use in BI / ML / external products?

Avoid:
- Catalogs that require manual curation of every field — adoption dies
- "Marketplace" features no one uses
- AI auto-tagging without human review (false sense of governance)

Pragmatic adoption strategy: certify the top 50 datasets first; fill out
the long tail via automation + spot-checks.

## 6. Data quality — dimensions and SLAs

### Dimensions

| Dimension | Definition | Common measure |
|-----------|-----------|----------------|
| Accuracy | Conforms to ground truth | Reconciliation vs source |
| Completeness | All required fields populated | % non-null |
| Consistency | Same fact across sources | Cross-system reconciliation |
| Timeliness / freshness | Available when needed | Latency from source event |
| Validity | Matches expected format / range | Schema + constraint checks |
| Uniqueness | No unwanted duplicates | Distinct-key count |
| Integrity | Referential / structural integrity | FK and constraint checks |

### Critical-dataset SLAs

For each critical dataset, publish:

- **Freshness target** (e.g., 95% of partitions land within 30 min of SLA window)
- **Completeness target** (e.g., < 0.1% null in required fields)
- **Schema stability** (breaking changes communicated ≥ 14 days in advance)
- **Quality test pass rate** (≥ 99% across the test suite)
- **Owner + on-call rotation**
- **Incident response runbook**

Pair with `engineering/data-quality-auditor` for tooling.

### Quality program scope creep

Don't put quality SLAs on every dataset; quality programs that try this
collapse. Pick the top 20–50 critical datasets and run them at high
quality; let the long tail be best-effort with monitoring.

## 7. Lineage — what to capture

End-to-end lineage is the goal. Practical phases:

- **Phase 1 — pipeline lineage:** dataset-to-dataset edges. Auto-extracted from orchestrators (Airflow, Dagster) and SQL parsers.
- **Phase 2 — column-level lineage:** which input columns drive which output columns. Required for impact analysis on PII fields.
- **Phase 3 — application lineage:** which apps and dashboards consume which datasets. Required for change impact comms.
- **Phase 4 — business lineage:** which business KPI a dataset feeds. Required for executive impact reporting.

OpenLineage as the spec; integration via the catalog. Don't try to skip
to Phase 4 — without 1 and 2 it's all hand-waved.

## 8. Privacy by design

Bake privacy into the governance program, don't bolt it on:

- **Data minimization:** capture only what you need; document why.
- **Purpose binding:** ingestion tagged with the lawful basis and purpose.
- **Consent management:** durable consent record per subject, queryable, revocable.
- **DSAR readiness:** automated subject access fulfillment (find, return, delete).
- **Retention enforcement:** delete on schedule, not on demand.
- **Cross-border transfer posture:** documented SCCs, residency constraints in storage.
- **PIA/DPIA:** for new processing of high-risk personal data.

For GDPR / DSGVO depth see `ra-qm-team/gdpr-dsgvo-expert`.

## 9. Master data management (MDM) — when it's needed

MDM is the formal process for managing critical reference entities
(customer, product, supplier, location, employee).

You need MDM when:
- The same customer/product appears in 4+ systems with different IDs
- Reconciliation reports take a person more than a day
- Sales, finance, and product disagree on customer count
- M&A creates conflicting master records

You don't need MDM when:
- One source of truth already exists and is unambiguous
- The cost of disagreement is < the cost of MDM tooling and process

MDM patterns: registry (lightweight, points to sources), consolidation
(builds golden record from sources), centralized (single source for an
entity), coexistence (golden record + sources stay in sync).

Most enterprises run consolidation for customer, centralized for chart of
accounts, and registry for everything else.

## 10. Reference data management (RDM)

Smaller cousin of MDM. Covers country codes, currency codes, product
categories, units of measure. Often neglected but causes downstream
breakage when undisciplined.

Practical move: maintain RDM as code in a versioned repo; publish to the
warehouse; require all transformations to reference it.

## 11. Access controls — RBAC + ABAC

A governance program that doesn't reach access is theater. Practical model:

- **RBAC for the base case:** roles wired to job functions (analyst, engineer, exec)
- **ABAC for sensitive scope:** attribute-based — e.g., "can see EU customer data only if EU-cleared"
- **Just-in-time elevation** for incidents and audits, with auto-expiry
- **Audit logged** access on Restricted data, with anomaly alerts

Wire classification → controls automatically. Manual workflows fail.

## 12. Audit readiness

Most CDOs face audit pressure from one or more of:

- SOC 2, ISO 27001 (security-led, data adjacent)
- GDPR / sector privacy regulators
- Industry-specific (HIPAA, PCI DSS, FDA, banking)
- Internal audit

A baseline audit-ready governance program needs:

1. Published, signed policies
2. RACI for data ownership and stewardship
3. Catalog with classification and ownership filled for critical datasets
4. Evidence: who approved what, when, with which attestation
5. Quarterly internal audit with findings tracked to closure
6. Quality SLAs and incident runbook with evidence of tests

Pair with `ra-qm-team/audit-prep/*` skills for framework-specific sprints.

## 13. Incident response (data quality + breach)

### Quality incidents
- Detection: drift, SLA breach, downstream consumer complaint
- Triage: severity, blast radius, business impact, regulatory implication
- Containment: pause downstream, freeze upstream change
- Investigation: root cause (source change, transformation bug, infra)
- Communication: stakeholder notice, customer comm if external
- Postmortem within 5 business days, action items tracked

### Privacy / breach incidents
- Detection: SIEM alert, DLP hit, manual report, regulator notice
- Triage: data-subject impact, lawful basis affected
- Containment: revoke access, rotate credentials, freeze data
- Notification:
  - GDPR Art. 33: supervisory authority within 72 hours
  - GDPR Art. 34: subjects without undue delay if high risk
  - Sector regs (HIPAA, state laws) vary; pre-publish your matrix
- Remediation + lessons-learned

## 14. Governance metrics

Track 6–10. Common picks:

- **Critical-dataset SLA hit rate**
- **% of Restricted fields with documented lineage**
- **Catalog freshness** (median age of last review on certified datasets)
- **Open audit findings — by age**
- **Time-to-fulfill DSAR (median + P95)**
- **% of new datasets onboarded with classification at intake**
- **Number of data products with documented owner + SLA**

Avoid:
- "Catalog entries" — incentivizes spam
- "Policies published" — once is enough

## 15. Common pitfalls

- **Governance with no enforcement teeth.** Tie controls to systems.
- **Quality program with no SLA-receiving consumer.** SLAs need a counter-party.
- **Stewardship as a part-time job for unwilling people.** It fails.
- **Catalog as a wiki.** A wiki is a wiki.
- **Audit prep that starts 60 days before audit.** Build evidence as you go; quarterly internal audit beats panicked sprints.
- **MDM project disconnected from a use case.** No use case = no funding = no value.
