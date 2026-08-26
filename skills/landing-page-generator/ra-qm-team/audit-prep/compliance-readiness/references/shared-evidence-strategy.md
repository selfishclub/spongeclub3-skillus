# Shared Evidence Strategy

Reference for implementing shared evidence across compliance frameworks. Covers GRC tooling, evidence-collection patterns, evidence-mapping techniques, and the organizational design that supports shared evidence.

---

## Why shared evidence

Without coordination, organizations:
- Take the same screenshot 5x for 5 frameworks
- Maintain 5 separate procedures (one per framework)
- Hold 5 separate management reviews
- Run 5 separate internal audits
- Pay for 5 separate certifications

With shared evidence:
- One screenshot, tagged per framework
- One procedure (mapped to framework requirements)
- One management review (covering all frameworks)
- One internal audit (per-clause but covers multiple)
- Multiple certifications from shared foundation

Savings: typically 30-50% of compliance ongoing cost.

---

## Shared-evidence implementation patterns

### Pattern 1: Common Control Catalog

Build one catalog of controls; each control maps to multiple frameworks.

```
Control ID: AC-01
Name: User access reviews (quarterly)
Description: All user accounts reviewed quarterly by their team manager;
              evidence retained for 1 year minimum.

Maps to:
- SOC 2 CC6.3
- ISO 27001 A.5.18
- NIST CSF PR.AA-04
- HIPAA §164.308(a)(4)(ii)
- GDPR Art.32

Owner: IT Security
Frequency: Quarterly
Evidence type: Access review records with sign-off
Retention: 1 year
Last reviewed: 2026-04-15
```

One control entry; one evidence trail; satisfies 5 frameworks.

### Pattern 2: GRC platform (Drata / Vanta / Sprinto / Thoropass / Hyperproof)

Modern GRC platforms:
- Auto-collect evidence (cloud configs, access reviews, change records)
- Map evidence to multiple frameworks
- Generate per-framework audit reports
- Continuous compliance monitoring

Selection criteria:
- Frameworks supported
- Integrations with existing tools (cloud, IdP, CI/CD)
- Auditor familiarity (your auditor may prefer specific platforms)
- Cost (per-employee + per-framework pricing common)
- Implementation complexity

### Pattern 3: Manual but disciplined

For orgs not ready for GRC platform:
- Shared folder structure (one folder per control)
- Tagging system (per-framework tags on evidence)
- Spreadsheet-based control mapping
- Calendar-driven evidence refresh

Works for < 100 controls; gets unwieldy beyond.

### Pattern 4: Hybrid

GRC platform for technical controls (auto-collected) + manual for procedural controls (interviews, policies, training).

Most organizations end up here.

---

## Evidence types and shareability

| Evidence type | Shareable across frameworks? | Notes |
|---------------|------------------------------|-------|
| Policy document | Yes — same policy satisfies all | Map references to framework requirements |
| Access review records | Yes | Same review covers SOC 2 + ISO 27001 + HIPAA + more |
| Vulnerability scan reports | Yes | Same scans evidence multiple frameworks |
| Change tickets | Yes | Same tickets evidence SOC 2 CC8 + ISO 27001 A.5.36 |
| Training records | Yes | Same training records evidence SOC 2 CC1.4 + ISO 27001 A.6.3 + HIPAA §164.308 |
| Vendor SOC 2 reports | Yes | Evidence vendor management in your SOC 2 + ISO 27001 |
| DR test results | Yes | Same test evidences SOC 2 A1.3 + ISO 27001 A.5.30 |
| Incident response records | Yes | Same incident records evidence SOC 2 CC7.4 + ISO 27001 A.5.24 |
| ROPA (Records of Processing) | GDPR-specific | But informs vendor management for other frameworks |
| AIIA (AI Impact Assessment) | ISO 42001 / AI Act-specific | But informs risk management broadly |
| Specific framework attestations | Framework-specific | E.g., SOC 2 management assertions |

---

## Evidence collection cadence (shared)

Standard evidence types + their cadences (apply across all frameworks):

| Evidence | Cadence | Owners |
|----------|---------|--------|
| Policy review | Annual | Policy owner |
| Access review | Quarterly | Team manager |
| Vulnerability scan | Monthly (or per CI/CD push) | Security ops |
| Vulnerability remediation | Continuous | Security ops |
| Patch compliance | Monthly | IT ops |
| Backup test | Quarterly | IT ops |
| DR test | Annual | DR coordinator |
| Penetration test | Annual | Security or 3rd party |
| Training completion | Quarterly check | HR / Security |
| Vendor SOC 2 report collection | Annual (per vendor) | Vendor manager |
| Internal audit | Annual (per framework area) | Internal audit |
| Management review | Annual | Quality / Compliance manager |
| Risk register update | Quarterly | Risk owner |
| Incident response test | Annual (table-top) + Quarterly (process check) | IR lead |

---

## Avoiding shared-evidence pitfalls

### Pitfall: Auditor doesn't accept shared evidence

**Mitigation**: most auditors do; some have specific format preferences. Confirm during scoping. If auditor insists on framework-specific evidence with same content, format the same evidence differently for each.

### Pitfall: Evidence becomes generic and loses specificity

When a single evidence item maps to 5 frameworks, it can drift toward lowest-common-denominator. Risk: auditor finds it's too generic to fully satisfy any one framework.

**Mitigation**: write evidence to satisfy the most-demanding framework. Other frameworks get more than they need (fine).

### Pitfall: Mapping becomes stale

Controls change; mappings to framework requirements don't get updated.

**Mitigation**: Quarterly mapping review; assign owner.

### Pitfall: Different audit calendars create crunches

5 frameworks, 5 audits, all in Q4 = burned-out team.

**Mitigation**: Stagger audits; coordinate auditor schedules; possibly combine where same auditor can do multiple.

### Pitfall: Single GRC platform locks you in

Platform pricing scales unfavorably; switching is expensive.

**Mitigation**: Plan for platform migration in scoping; choose platform with reasonable export. Maintain control mappings in a portable format (CSV / YAML).

---

## Organizational design for shared evidence

### Centralized compliance function

One team owns all compliance frameworks. Pros: consistency, expertise, economies of scale. Cons: bottleneck, knowledge concentration risk.

Typical size:
- $5M-$50M ARR: 1-2 FTEs
- $50M-$500M ARR: 3-6 FTEs
- $500M+: 7-15 FTEs (often broken into compliance + privacy + risk teams)

### Distributed model with central enablement

Compliance function is small (1-2 people); they enable compliance owners in each business area. Pros: scales with business; embedded ownership. Cons: requires strong central function; risk of inconsistency.

### Common roles

- **Compliance Manager / VP Compliance**: program leadership
- **Compliance Analyst**: day-to-day evidence collection + audit coordination
- **DPO**: GDPR-specific (sometimes external)
- **CISO / Information Security Manager**: technical controls owner
- **Internal Audit Lead**: ISO standards internal audit
- **Quality Manager (medical / regulated)**: industry-specific compliance

---

## Audit coordination across frameworks

### Calendar planning

Annual:
- Q1: SOC 2 Type II (covers prior calendar year)
- Q1-Q2: Vendor reviews; risk assessment
- Q2-Q3: Internal audit; management review
- Q3: ISO 27001 surveillance
- Q4: GDPR review + DPA refresh

Staggered to avoid crunches.

### Single audit covering multiple frameworks

Some auditors offer "integrated audit" covering multiple frameworks in one engagement.

Example: SOC 2 Type II + ISO 27001 surveillance + NIST CSF self-assessment in one 2-week engagement.

Pros: efficient; one auditor relationship.
Cons: less specialization; specific framework requirements may be glossed.

### Sharing evidence with auditor

GRC platform: auditor gets read-only access to evidence repository; pulls what they need.

Manual: shared folder organized by control; auditor browses.

Discussion: walk-through meetings with auditor (efficient; evidence is then validated by the discussion).

---

## Continuous compliance vs point-in-time

### Point-in-time

Evidence collected for audit:
- Snapshot at audit time
- Risk of "audit theater" (controls perform during audit; degrade rest of year)
- Requires sprint per audit

### Continuous compliance

Evidence continuously collected:
- GRC platform with continuous monitoring
- Evidence always current
- Audit becomes verification, not collection
- More expensive in tooling; cheaper in audit prep

Most mature programs use continuous compliance for technical controls; point-in-time for procedural / annual ones (training, management review, etc.).

---

## Cheat sheet

| Question | Answer |
|----------|--------|
| First step toward shared evidence? | Build common control catalog with framework mappings |
| When to invest in GRC platform? | 3+ frameworks; or 1 framework with high evidence volume |
| Auditor accepts shared evidence? | Usually yes; confirm in scoping |
| How much overlap SOC 2 + ISO 27001? | 60-80% |
| Run multiple internal audits or one? | One audit, mapped to multiple frameworks |
| Same auditor for multiple frameworks? | Possible; weigh independence vs efficiency |
| Manual shared evidence sustainable? | Up to ~50 controls; beyond, get platform |
| Continuous vs point-in-time? | Continuous for tech controls; point-in-time for annual procedural |
| Time savings from shared evidence? | 30-50% of compliance ongoing cost |
