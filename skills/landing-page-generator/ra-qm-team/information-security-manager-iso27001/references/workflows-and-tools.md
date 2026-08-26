# ISMS Workflows, Validation & Tool Reference

Step-by-step procedures for ISMS implementation, security risk assessment, and incident response; validation checkpoints and certification-readiness checklists; a fully worked healthcare risk-assessment example; troubleshooting and success criteria; and complete `risk_assessment.py` / `compliance_checker.py` flag references. Read this when executing any end-to-end ISMS workflow, preparing for a certification audit, diagnosing a tooling result, or looking up a script flag.

## Tools

### risk_assessment.py

Automated security risk assessment following ISO 27001 Clause 6.1.2 methodology.

**Usage:**

```bash
# Full risk assessment
python scripts/risk_assessment.py --scope "cloud-infrastructure" --output risks.json

# Healthcare-specific assessment
python scripts/risk_assessment.py --scope "ehr-system" --template healthcare --output risks.json

# Quick asset-based assessment
python scripts/risk_assessment.py --assets assets.csv --output risks.json
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--scope` | Yes | System or area to assess |
| `--template` | No | Assessment template: `general`, `healthcare`, `cloud` |
| `--assets` | No | CSV file with asset inventory |
| `--output` | No | Output file (default: stdout) |
| `--format` | No | Output format: `json`, `csv`, `markdown` |

**Output:**
- Asset inventory with classification
- Threat and vulnerability mapping
- Risk scores (likelihood × impact)
- Treatment recommendations
- Residual risk calculations

### compliance_checker.py

Verify ISO 27001/27002 control implementation status.

**Usage:**

```bash
# Check all ISO 27001 controls
python scripts/compliance_checker.py --standard iso27001

# Gap analysis with recommendations
python scripts/compliance_checker.py --standard iso27001 --gap-analysis

# Check specific control domains
python scripts/compliance_checker.py --standard iso27001 --domains "access-control,cryptography"

# Export compliance report
python scripts/compliance_checker.py --standard iso27001 --output compliance_report.md
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--standard` | Yes | Standard to check: `iso27001`, `iso27002`, `hipaa` |
| `--controls-file` | No | CSV with current control status |
| `--gap-analysis` | No | Include remediation recommendations |
| `--domains` | No | Specific control domains to check |
| `--output` | No | Output file path |

**Output:**
- Control implementation status
- Compliance percentage by domain
- Gap analysis with priorities
- Remediation recommendations

---

## Workflows

### Workflow 1: ISMS Implementation

**Step 1: Define Scope and Context**

Document organizational context and ISMS boundaries:
- Identify interested parties and requirements
- Define ISMS scope and boundaries
- Document internal/external issues

**Validation:** Scope statement reviewed and approved by management.

**Step 2: Conduct Risk Assessment**

```bash
python scripts/risk_assessment.py --scope "full-organization" --template general --output initial_risks.json
```

- Identify information assets
- Assess threats and vulnerabilities
- Calculate risk levels
- Determine risk treatment options

**Validation:** Risk register contains all critical assets with assigned owners.

**Step 3: Select and Implement Controls**

Map risks to ISO 27002 controls:

```bash
python scripts/compliance_checker.py --standard iso27002 --gap-analysis --output control_gaps.md
```

Control categories:
- Organizational (policies, roles, responsibilities)
- People (screening, awareness, training)
- Physical (perimeters, equipment, media)
- Technological (access, crypto, network, application)

**Validation:** Statement of Applicability (SoA) documents all controls with justification.

**Step 4: Establish Monitoring**

Define security metrics:
- Incident count and severity trends
- Control effectiveness scores
- Training completion rates
- Audit findings closure rate

**Validation:** Dashboard shows real-time compliance status.

### Workflow 2: Security Risk Assessment

**Step 1: Asset Identification**

Create asset inventory:

| Asset Type | Examples | Classification |
|------------|----------|----------------|
| Information | Patient records, source code | Confidential |
| Software | EHR system, APIs | Critical |
| Hardware | Servers, medical devices | High |
| Services | Cloud hosting, backup | High |
| People | Admin accounts, developers | Varies |

**Validation:** All assets have assigned owners and classifications.

**Step 2: Threat Analysis**

Identify threats per asset category:

| Asset | Threats | Likelihood |
|-------|---------|------------|
| Patient data | Unauthorized access, breach | High |
| Medical devices | Malware, tampering | Medium |
| Cloud services | Misconfiguration, outage | Medium |
| Credentials | Phishing, brute force | High |

**Validation:** Threat model covers top-10 industry threats.

**Step 3: Vulnerability Assessment**

```bash
python scripts/risk_assessment.py --scope "network-infrastructure" --output vuln_risks.json
```

Document vulnerabilities:
- Technical (unpatched systems, weak configs)
- Process (missing procedures, gaps)
- People (lack of training, insider risk)

**Validation:** Vulnerability scan results mapped to risk register.

**Step 4: Risk Evaluation and Treatment**

Calculate risk: `Risk = Likelihood × Impact`

| Risk Level | Score | Treatment |
|------------|-------|-----------|
| Critical | 20-25 | Immediate action required |
| High | 15-19 | Treatment plan within 30 days |
| Medium | 10-14 | Treatment plan within 90 days |
| Low | 5-9 | Accept or monitor |
| Minimal | 1-4 | Accept |

**Validation:** All high/critical risks have approved treatment plans.

### Workflow 3: Incident Response

**Step 1: Detection and Reporting**

Incident categories:
- Security breach (unauthorized access)
- Malware infection
- Data leakage
- System compromise
- Policy violation

**Validation:** Incident logged within 15 minutes of detection.

**Step 2: Triage and Classification**

| Severity | Criteria | Response Time |
|----------|----------|---------------|
| Critical | Data breach, system down | Immediate |
| High | Active threat, significant risk | 1 hour |
| Medium | Contained threat, limited impact | 4 hours |
| Low | Minor violation, no impact | 24 hours |

**Validation:** Severity assigned and escalation triggered if needed.

**Step 3: Containment and Eradication**

Immediate actions:
1. Isolate affected systems
2. Preserve evidence
3. Block threat vectors
4. Remove malicious artifacts

**Validation:** Containment confirmed, no ongoing compromise.

**Step 4: Recovery and Lessons Learned**

Post-incident activities:
1. Restore systems from clean backups
2. Verify integrity before reconnection
3. Document timeline and actions
4. Conduct post-incident review
5. Update controls and procedures

**Validation:** Post-incident report completed within 5 business days.

---

## Validation Checkpoints

### ISMS Implementation Validation

| Phase | Checkpoint | Evidence Required |
|-------|------------|-------------------|
| Scope | Scope approved | Signed scope document |
| Risk | Register complete | Risk register with owners |
| Controls | SoA approved | Statement of Applicability |
| Operation | Metrics active | Dashboard screenshots |
| Audit | Internal audit done | Audit report |

### Certification Readiness

Before Stage 1 audit:
- [ ] ISMS scope documented and approved
- [ ] Information security policy published
- [ ] Risk assessment completed
- [ ] Statement of Applicability finalized
- [ ] Internal audit conducted
- [ ] Management review completed
- [ ] Nonconformities addressed

Before Stage 2 audit:
- [ ] Controls implemented and operational
- [ ] Evidence of effectiveness available
- [ ] Staff trained and aware
- [ ] Incidents logged and managed
- [ ] Metrics collected for 3+ months

### Compliance Verification

Run periodic checks:

```bash
# Monthly compliance check
python scripts/compliance_checker.py --standard iso27001 --output monthly_$(date +%Y%m).md

# Quarterly gap analysis
python scripts/compliance_checker.py --standard iso27001 --gap-analysis --output quarterly_gaps.md
```

---

## Worked Example: Healthcare Risk Assessment

**Scenario:** Assess security risks for a patient data management system.

### Step 1: Define Assets

```bash
python scripts/risk_assessment.py --scope "patient-data-system" --template healthcare
```

**Asset inventory output:**

| Asset ID | Asset | Type | Owner | Classification |
|----------|-------|------|-------|----------------|
| A001 | Patient database | Information | DBA Team | Confidential |
| A002 | EHR application | Software | App Team | Critical |
| A003 | Database server | Hardware | Infra Team | High |
| A004 | Admin credentials | Access | Security | Critical |

### Step 2: Identify Risks

**Risk register output:**

| Risk ID | Asset | Threat | Vulnerability | L | I | Score |
|---------|-------|--------|---------------|---|---|-------|
| R001 | A001 | Data breach | Weak encryption | 3 | 5 | 15 |
| R002 | A002 | SQL injection | Input validation | 4 | 4 | 16 |
| R003 | A004 | Credential theft | No MFA | 4 | 5 | 20 |

### Step 3: Determine Treatment

| Risk | Treatment | Control | Timeline |
|------|-----------|---------|----------|
| R001 | Mitigate | Implement AES-256 encryption | 30 days |
| R002 | Mitigate | Add input validation, WAF | 14 days |
| R003 | Mitigate | Enforce MFA for all admins | 7 days |

### Step 4: Verify Implementation

```bash
python scripts/compliance_checker.py --controls-file implemented_controls.csv
```

**Verification output:**

```
Control Implementation Status
=============================
Cryptography (A.8.24): IMPLEMENTED
  - AES-256 at rest: YES
  - TLS 1.3 in transit: YES

Access Control (A.8.5): IMPLEMENTED
  - MFA enabled: YES
  - Admin accounts: 100% coverage

Application Security (A.8.26): PARTIAL
  - Input validation: YES
  - WAF deployed: PENDING

Overall Compliance: 87%
```

---

## Troubleshooting

| Problem | Possible Cause | Resolution |
|---------|---------------|------------|
| Compliance checker shows low score despite documented policies | Controls documented but not implemented or operating effectively; evidence of operation missing | Focus on evidence of control operation (logs, reports, screenshots) rather than just policy documents; run `compliance_checker.py --gap-analysis` to identify implementation gaps |
| Risk assessment generates excessive number of high/critical risks | Asset classification overly conservative or threat likelihood ratings not calibrated to organization context | Calibrate likelihood and impact scales to actual organizational experience; review threat catalog against industry benchmarks; use `--template healthcare` or `--template cloud` for context-appropriate threat catalogs |
| Stage 1 audit identifies significant documentation gaps | ISMS documentation not aligned with ISO 27001:2022 clause structure or missing mandatory documented information | Review the 2022 mandatory documentation list (information security policy, SoA, risk assessment methodology, risk treatment plan); ensure clause 4-10 documentation uses the 2022 structure |
| Transitioning from ISO 27001:2013 -- controls do not map | 2022 revision restructured 114 controls into 93 across 4 themes; some controls merged or renamed | Use the 11 new controls list as starting point; map merged controls; update Statement of Applicability to reflect 4-theme structure (Organizational, People, Physical, Technological) |
| Cloud security controls insufficient for multi-cloud environment | Generic controls applied without cloud-provider-specific implementation | Map ISO 27001 controls to provider-specific services (AWS: GuardDuty, Config; Azure: Defender, Policy; GCP: SCC, DLP); use the cloud-specific control tables in this skill |
| Zero Trust implementation conflicts with existing network architecture | Legacy perimeter-based security model incompatible with microsegmentation | Follow the phased Zero Trust roadmap (Foundation 0-6mo, Enhancement 6-12mo, Maturation 12-18mo); start with identity and MFA before network changes |
| Supply chain security assessment overwhelmed by vendor count | No vendor risk tiering applied; all vendors assessed at same depth | Apply the Third-Party Risk Tiers (Critical, High, Medium, Low); focus full security audits on Critical tier; use questionnaires for Medium/Low |

---

## Success Criteria

- **Overall compliance score above 85%** -- as measured by `compliance_checker.py`, with all high-priority controls implemented and operating effectively
- **Risk register complete with assigned owners for all high/critical risks** -- every risk assessed using Likelihood x Impact methodology with documented treatment plans and target remediation dates
- **Statement of Applicability current and approved** -- covering all 93 Annex A controls with justification for inclusion/exclusion, aligned with the 2022 four-theme structure
- **Internal audit conducted annually** -- covering all ISMS clauses (4-10) and all Annex A controls within the 3-year certification cycle, with findings documented and corrective actions tracked
- **Management review completed with documented outputs** -- including ISMS performance metrics, audit findings, risk treatment status, and improvement decisions
- **Security awareness training completion rate above 95%** -- all personnel trained annually with records maintained; specialized training for security and IT staff
- **Incident response tested and validated** -- at least one tabletop exercise or simulation annually; post-incident reviews conducted for all actual incidents; lessons learned documented and implemented

---

## Tool Reference (Full Flag Tables)

### risk_assessment.py

Automated security risk assessment following ISO 27001 Clause 6.1.2 methodology.

| Flag | Required | Description |
|------|----------|-------------|
| `--scope <name>` | Yes (unless `--assets`) | System or area to assess (e.g., `cloud-infrastructure`, `ehr-system`, `patient-data-system`) |
| `--template <type>` | No | Assessment template: `general` (default), `healthcare`, `cloud` -- each provides context-appropriate threat catalogs |
| `--assets <file>` | No | CSV file with asset inventory (columns: asset_id, name, type, owner, classification) |
| `--output <file>` | No | Output file path (default: stdout) |
| `--format <fmt>` | No | Output format: `json` (default), `csv`, `markdown` |

**Output:** Asset inventory with classification, threat and vulnerability mapping, risk scores (Likelihood x Impact on 1-5 scale), treatment recommendations per risk level, and residual risk calculations.

### compliance_checker.py

Verifies ISO 27001/27002 control implementation status with gap analysis and remediation recommendations.

| Flag | Required | Description |
|------|----------|-------------|
| `--standard <std>` | Yes | Standard to check: `iso27001`, `iso27002`, `hipaa` |
| `--controls-file <file>` | No | CSV file with current control implementation status |
| `--gap-analysis` | No | Include detailed remediation recommendations in output |
| `--domains <domains>` | No | Comma-separated specific control domains to check (e.g., `access-control,cryptography`) |
| `--output <file>` | No | Output file path for compliance report |

**Output:** Control implementation status per domain, compliance percentage by theme/domain, gap analysis with priorities (when `--gap-analysis` flag used), and remediation recommendations mapped to ISO 27002 control guidance.
