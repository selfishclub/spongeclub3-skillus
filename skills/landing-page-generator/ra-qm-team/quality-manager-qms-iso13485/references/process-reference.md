# QMS Process Reference & Decision Frameworks

Reference tables for the ISO 13485 clause structure, management review inputs, record retention, plus decision frameworks for exclusions, nonconformity disposition, and CAPA initiation. Read this when mapping clauses, planning management review, or making disposition/CAPA decisions.

---

## QMS Process Reference

### ISO 13485 Clause Structure

| Clause | Title | Key Requirements |
|--------|-------|-----------------|
| 4.1 | General Requirements | Process identification, interaction, outsourcing |
| 4.2 | Documentation | Quality Manual, procedures, records |
| 5.1-5.5 | Management Responsibility | Commitment, policy, objectives, organization |
| 5.6 | Management Review | Inputs, outputs, records |
| 6.1-6.4 | Resource Management | Personnel, infrastructure, environment |
| 7.1 | Product Realization Planning | Quality plan, risk management |
| 7.2 | Customer Requirements | Determination, review, communication |
| 7.3 | Design and Development | Planning, inputs, outputs, review, V&V, transfer, changes |
| 7.4 | Purchasing | Supplier control, purchasing info, verification |
| 7.5 | Production | Control, cleanliness, validation, identification, traceability |
| 7.6 | Monitoring Equipment | Calibration, control |
| 8.1 | Measurement Planning | Monitoring and analysis planning |
| 8.2 | Monitoring | Feedback, complaints, reporting, audits, process, product |
| 8.3 | Nonconforming Product | Control, disposition |
| 8.4 | Data Analysis | Trend analysis |
| 8.5 | Improvement | CAPA |

### Management Review Required Inputs (Clause 5.6.2)

| Input | Source | Prepared By |
|-------|--------|-------------|
| Audit results | Internal and external audits | QA Manager |
| Customer feedback | Complaints, surveys | Customer Quality |
| Process performance | Process metrics | Process Owners |
| Product conformity | Inspection data, NCs | QC Manager |
| CAPA status | CAPA system | CAPA Officer |
| Previous actions | Prior review records | QMR |
| Changes affecting QMS | Regulatory, organizational | RA Manager |
| Recommendations | All sources | All Managers |

### Record Retention Requirements

| Record Type | Minimum Retention | Regulatory Basis |
|-------------|-------------------|------------------|
| Device Master Record | Life of device + 2 years | 21 CFR 820.181 |
| Device History Record | Life of device + 2 years | 21 CFR 820.184 |
| Design History File | Life of device + 2 years | 21 CFR 820.30 |
| Complaint Records | Life of device + 2 years | 21 CFR 820.198 |
| Training Records | Employment + 3 years | Best practice |
| Audit Records | 7 years | Best practice |
| CAPA Records | 7 years | Best practice |
| Calibration Records | Equipment life + 2 years | Best practice |

---

## Decision Frameworks

### Exclusion Justification (Clause 4.2.2)

| Clause | Permissible Exclusion | Justification Required |
|--------|----------------------|------------------------|
| 6.4.2 | Contamination control | Product not affected by contamination |
| 7.3 | Design and development | Organization does not design products |
| 7.5.2 | Product cleanliness | No cleanliness requirements |
| 7.5.3 | Installation | No installation activities |
| 7.5.4 | Servicing | No servicing activities |
| 7.5.5 | Sterile products | No sterile products |

### Nonconformity Disposition Decision Tree

```
Nonconforming Product Identified
            │
            ▼
    Can it be reworked?
            │
       Yes──┴──No
        │       │
        ▼       ▼
    Is rework     Can it be used
    procedure     as is?
    available?        │
        │        Yes──┴──No
    Yes─┴─No     │       │
     │    │     ▼       ▼
     ▼    ▼  Concession  Scrap or
  Rework  Create    approval    return to
  per SOP  rework    needed?    supplier
          procedure     │
                    Yes─┴─No
                     │    │
                     ▼    ▼
                 Customer  Use as is
                 approval  with MRB
                          approval
```

### CAPA Initiation Criteria

| Source | Automatic CAPA | Evaluate for CAPA |
|--------|----------------|-------------------|
| Customer complaint | Safety-related | All others |
| External audit | Major NC | Minor NC |
| Internal audit | Major NC | Repeat minor NC |
| Product NC | Field failure | Trend exceeds threshold |
| Process deviation | Safety impact | Repeated deviations |
