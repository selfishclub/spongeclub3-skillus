# AIMS Internal Audit Playbook

Reference for running ISO 42001 internal audits (required by Clause 9.2) — covers audit scope, scheduling, audit team selection, audit techniques, nonconformity classification, and reporting.

---

## Why internal audit matters

ISO 42001 Clause 9.2 requires internal audits:
- At planned intervals
- To provide information on AIMS conformity + effectiveness
- Covering all AIMS clauses + Annex A controls applied

Internal audit:
- Finds gaps before external auditor does
- Maintains AIMS competence
- Generates evidence for management review
- Drives continual improvement

Without internal audit:
- External audit becomes the discovery process (more expensive)
- AIMS deteriorates between certification cycles

---

## Internal audit cadence + scope

### Annual internal audit (required)

- Covers all clauses + applicable Annex A controls
- Typically broken into multiple sub-audits across the year
- Risk-based: higher-risk areas audited more frequently

### Risk-based scheduling

| Area | Frequency |
|------|-----------|
| High-risk AI systems (per AIIA) | Every 6 months |
| AI lifecycle process | Annually |
| Data governance | Annually |
| Third-party AI vendors | Annually (per-vendor more frequent) |
| Documentation control | Annually |
| Management responsibility | Annually |

### Triggered audits

Additional audits after:
- Major AIMS change
- Significant incident
- New high-risk AI system deployment
- External audit nonconformity (verify corrective action effectiveness)
- Major change to operating environment (regulatory, technology)

---

## Internal auditor selection

### Required competencies

- ISO 42001 trained
- AIMS lifecycle knowledge
- AI / ML technical literacy
- Audit techniques (interviewing, observation, sampling)
- Independent from area being audited

### Internal vs external auditors

| Source | Pros | Cons |
|--------|------|------|
| Internal employees | Cheap; embedded knowledge | Independence concerns; competence gaps |
| Internal cross-team | Better independence | Logistical |
| External consultants | Independent; expert | Cost; outsider perspective |
| Combined (internal + external observer) | Balance | More complex |

For smaller orgs: external auditor for at least one annual internal audit cycle.

---

## Audit scope definition

For each internal audit:

```
Audit ID: IA-YYYY-NN
Date(s): YYYY-MM-DD
Auditor(s): [names]
Scope:
  AIMS clauses: [list]
  Annex A controls: [list]
  AI systems / scope: [list]
Criteria: ISO 42001:2023; AIMS documented procedures; applicable regulatory
Methodology: [interviews / document review / observation / sampling]
Out of scope: [explicitly listed]
```

---

## Audit techniques

### Document review

- AIMS documentation completeness
- Document version control
- Approval evidence
- Update cadence
- Consistency across documents

### Interviews

For each role:
- Role-specific questions per clause
- "Walk me through what you do for..."
- Look for: actual practice vs documented practice

Standard interview targets:
- Senior leader (Clause 5)
- AI governance lead (Clauses 4, 5, 9)
- Data lead (Annex A.7)
- AI engineering lead (Annex A.6)
- Security lead (Annex A.6 + A.10)
- Customer success / external comms (A.8)
- Vendor manager (A.10)

### Observation

Watch AIMS in action:
- AI development pipeline (V&V actually executed)
- AI Impact Assessment process (actually applied to new system)
- Incident response (table-top exercise if no recent incident)
- Vendor onboarding (next vendor process)

### Sampling

For evidence-heavy areas:
- AI system inventory: sample 3-5 systems; deep-dive
- AIIA: sample 3-5 AIIAs; check completeness + currency
- Training records: sample 10-20 employees; check role-appropriate training
- Change records: sample 5-10 changes; check change control
- Incidents: review all in audit period

---

## Nonconformity classification

### Major nonconformity

- Total breakdown of a clause / control
- Multiple minor NCs revealing systemic failure
- High-risk control not implemented
- Risk of certification suspension if not addressed

Examples:
- AIMS does not have AI Impact Assessment process
- Internal audit never conducted
- AI policy not approved by leadership
- AI system inventory severely incomplete

### Minor nonconformity

- Isolated failure to apply documented procedure
- Documentation gap with low risk
- Single instance of control failure

Examples:
- AIIA missing for one specific system
- Training record missing for one employee
- One vendor without AI assessment
- Document with incorrect version reference

### Observation (not nonconformity)

- Improvement opportunity
- Not a violation of standard or AIMS
- Recommended for continual improvement

Examples:
- AIIA template could be more user-friendly
- Internal audit could be more efficient with tooling
- Training content could include more examples

---

## Nonconformity tracking

```
NC ID: NC-YYYY-NN
Audit Reference: IA-YYYY-NN (internal) or EA-YYYY-NN (external)
Classification: Major / Minor / Observation
Clause / Annex A control: [specific reference]
Description: [what was found]
Evidence: [what was observed]
Root cause: [identified per RCA]
Correction (immediate fix): [what was done immediately]
Corrective action (systemic): [what's being done to prevent recurrence]
Owner: [name]
Due date: [date]
Status: Open / Closed / Verified Effective
Effectiveness verification: [how + when]
```

---

## Audit report structure

```
# Internal Audit Report: IA-YYYY-NN

## Summary
- Date(s): YYYY-MM-DD
- Auditor(s): [names]
- Scope: [clauses, Annex A, systems]
- Status: [completed / in-progress]

## Executive summary
[2-3 paragraph: overall AIMS health; major findings; recommendations]

## Audit methodology
- Approach used
- Documents reviewed
- People interviewed
- Observations performed
- Samples taken

## Findings

### Major nonconformities ([count])
[Detailed per NC]

### Minor nonconformities ([count])
[Detailed per NC]

### Observations ([count])
[Improvement opportunities]

### Positive observations
[Things working well; not required but useful]

## Conclusion
[Overall assessment]

## Distribution
- Management representative
- Quality manager
- Senior leadership
- AIMS owners affected
```

---

## Linking internal audit to management review

ISO 42001 Clause 9.3 (Management Review) requires consideration of:
- Internal audit results
- Nonconformities + corrective actions

Standard management review agenda inputs:
- Internal audit summary (last 12 months)
- Nonconformity trends
- Corrective action effectiveness
- Recurring issues

Output:
- Resource decisions
- AIMS improvement decisions
- Strategic AI direction adjustments

---

## Common internal audit failures

| Failure | Recovery |
|---------|----------|
| Internal audit skipped | Schedule immediately; document why missed |
| Auditor not independent (audited own work) | Re-do audit with independent auditor |
| Audit too narrow (didn't cover required clauses) | Schedule supplemental audits |
| NCs identified but not tracked | Build NC log; close prior NCs retroactively |
| Same NCs every year | Indicates corrective action not effective; deeper RCA needed |
| No followup audit on prior NCs | Schedule verification audit |

---

## Maturity progression

### Year 1 (initial certification)

- Establish internal audit program
- Conduct first full annual audit
- All NCs tracked + closed
- Build evidence baseline

### Year 2 (surveillance)

- Risk-based audit scheduling
- Trend analysis across audits
- Increased rigor in higher-risk areas
- External auditor finds nothing new (everything caught internally)

### Year 3+ (mature)

- Predictable audit cadence
- Continual improvement driven by audit findings
- Audit results contribute to management review
- Increasing auditor competence

---

## Cheat sheet

| Question | Answer |
|----------|--------|
| Frequency? | Annual minimum; risk-based for higher cadence in critical areas |
| Who can be internal auditor? | Trained + independent (not from audited area) |
| Major vs minor NC? | Major: systemic failure; Minor: isolated instance |
| What if external auditor finds NCs internal audit missed? | Update internal audit scope; gap in internal program |
| How long to close NCs? | Minor: 30-60 days; Major: 90 days max with interim controls |
| Where do internal audit results go? | Management review (Clause 9.3) |
| What evidence does external auditor want? | Audit reports, NC log, corrective action closure, trend analysis |
| Pre-external-audit prep? | Run mock internal audit; close any findings before external |
