# Extended Risk Domains — AI/ML, Cybersecurity, Supply Chain & Cross-Framework

Extensions to the core ISO 14971 process for AI/ML medical devices, health-software cybersecurity
(IEC 81001-5-1), supply chain risk, post-market monitoring automation, and cross-framework mapping
(NIST CSF 2.0, DORA, NIS2). Read this when the device includes AI/ML or connected/software
components, or when risk management must align with security and resilience frameworks.

## AI-Specific Risk Management (ISO 14971 + AI Risk Considerations)

### AI/ML Medical Device Risk Categories

Traditional ISO 14971 hazard categories must be extended for AI/ML-based devices:

| AI-Specific Hazard | Description | Severity Potential | Detection Difficulty |
|--------------------|-------------|-------------------|---------------------|
| Model bias | Discriminatory outputs across patient subgroups | S3-S5 (misdiagnosis) | High — requires subgroup analysis |
| Data drift | Input data distribution shifts from training data | S2-S4 (degraded performance) | Medium — requires monitoring |
| Concept drift | Clinical ground truth changes over time | S3-S5 (outdated predictions) | High — requires clinical validation |
| Adversarial inputs | Intentionally crafted inputs to deceive model | S2-S5 (incorrect output) | High — requires adversarial testing |
| Hallucination/confabulation | Plausible but incorrect outputs | S3-S5 (false diagnosis) | Medium — requires output validation |
| Training data poisoning | Corrupted training data leads to systematic errors | S3-S5 | Very High — requires data provenance |
| Automation complacency | Users over-trust AI outputs | S3-S5 (missed clinical findings) | Medium — requires human factors study |

### AI Risk Analysis Methodology

```
Step 1: AI System Characterization
        → Define intended use, user population, clinical context
        → Classify: locked algorithm vs. adaptive vs. continuously learning
        → Map to SaMD risk framework (IMDRF)

Step 2: AI-Specific Hazard Identification
        → Apply standard ISO 14971 hazard categories
        → ADD: data quality hazards, algorithmic hazards, integration hazards
        → Consider: training data representativeness, edge cases, failure modes

Step 3: AI Failure Mode Analysis
        → Extend FMEA with AI-specific failure modes:
           - False positive/negative beyond acceptable rates
           - Performance degradation over time
           - Out-of-distribution input handling
           - Feature importance shift
        → For each failure mode: determine harm pathway to patient

Step 4: AI-Specific Risk Controls
        → Confidence thresholds (reject uncertain predictions)
        → Human-in-the-loop for high-risk decisions
        → Input validation and out-of-distribution detection
        → Continuous performance monitoring with drift detection
        → Automated model retraining safeguards
        → Fail-safe modes when AI system is unavailable

Step 5: AI Risk Monitoring Plan
        → Define performance metrics and acceptable thresholds
        → Establish monitoring frequency (real-time, daily, weekly)
        → Define retraining triggers and validation requirements
        → Plan for model versioning and rollback procedures
```

### AI Risk Acceptability Considerations

| Risk Factor | Additional Consideration for AI |
|-------------|--------------------------------|
| Probability | Include statistical confidence intervals for model performance |
| Severity | Consider both direct harm and harm from delayed correct treatment |
| Detectability | Factor in opacity of AI decision-making (explainability) |
| Benefit | Quantify clinical benefit vs. non-AI alternative |
| ALARP | State-of-the-art includes current AI best practices (GMLP) |

---

## Cybersecurity Risk Integration (IEC 81001-5-1)

### Health Software Cybersecurity Risk Management

IEC 81001-5-1:2021 establishes cybersecurity lifecycle requirements for health software. Integrate with ISO 14971:

| ISO 14971 Stage | IEC 81001-5-1 Integration | Combined Output |
|----------------|--------------------------|-----------------|
| Risk Management Plan | Include cybersecurity scope, threat modeling methodology | Combined RM + cybersecurity plan |
| Hazard identification | Add cybersecurity threat identification (STRIDE, attack trees) | Extended hazard analysis with cyber threats |
| Risk estimation | Estimate probability based on threat landscape and exploitability | Risk register with cyber-specific likelihood factors |
| Risk control | Implement security controls as risk mitigations | Controls traceable to both safety and security risks |
| Residual risk | Evaluate residual cybersecurity risk | Combined residual risk assessment |
| Post-production | Monitor threat landscape, CVE databases, incident reports | Integrated PMS + security monitoring |

### Cybersecurity Threat Categories for Medical Devices

| Threat Category | Examples | ISO 14971 Harm Pathway |
|----------------|----------|----------------------|
| Unauthorized access | Credential theft, privilege escalation | Modification of device settings → patient harm |
| Data breach | PHI exfiltration, ransomware | Loss of data availability → delayed treatment |
| Denial of service | Network flooding, resource exhaustion | Device unavailable → delayed diagnosis/treatment |
| Malware | Ransomware, trojans, supply chain compromise | Device malfunction → incorrect output |
| Data integrity | Man-in-the-middle, data manipulation | Corrupted clinical data → incorrect treatment |
| Supply chain | Compromised dependencies, malicious updates | Backdoor access → any harm pathway |

### Cybersecurity FMEA Extension

Add these columns to standard FMEA for cybersecurity failure modes:

```
CYBERSECURITY FMEA EXTENSION

| ID | Component | Security Function | Threat | Attack Vector | Exploitability | Impact | S | O | D | RPN | Security Control |
|----|-----------|-------------------|--------|---------------|---------------|--------|---|---|---|-----|-----------------|
| CS-001 | Auth module | User authentication | Credential theft | Phishing | High (8) | Full access | 8 | 6 | 4 | 192 | MFA + session management |
| CS-002 | Data store | Data confidentiality | SQL injection | Network input | Medium (5) | Data breach | 9 | 4 | 3 | 108 | Parameterized queries + WAF |
| CS-003 | Update mechanism | Integrity | Supply chain | Compromised update | Low (3) | Malware install | 10 | 2 | 7 | 140 | Code signing + integrity verification |
```

---

## Supply Chain Risk Management

### Medical Device Supply Chain Risks

| Risk Category | Description | Probability | Impact | Control Strategy |
|--------------|-------------|-------------|--------|-----------------|
| Single-source component | Critical component from sole supplier | Medium | Critical | Dual-source qualification, safety stock |
| Counterfeit components | Fraudulent parts entering supply chain | Low-Medium | Catastrophic | Supplier audits, incoming inspection, chain of custody |
| Supplier quality failure | Supplier QMS breakdown | Medium | High | Supplier qualification, periodic audits, quality agreements |
| Software dependency | Vulnerable or unsupported open-source library | High | Medium-High | SBOM management, vulnerability scanning, update policy |
| Geopolitical disruption | Sanctions, trade restrictions, supply interruption | Low-Medium | High | Geographic diversification, buffer inventory |
| Raw material shortage | Rare earth, specialty materials unavailability | Low | High | Alternative material qualification, forward contracts |

### Supply Chain Risk Assessment Workflow

```
Step 1: Supply Chain Mapping
        → Identify all direct suppliers (Tier 1)
        → Map critical Tier 2 and Tier 3 suppliers
        → Document component criticality (safety-critical, quality-critical, standard)

Step 2: Supplier Risk Scoring
        → Quality risk: past performance, certification status, audit results
        → Financial risk: stability, dependency on your business
        → Geographic risk: natural disaster, political stability
        → Cyber risk: supplier's information security posture
        → Concentration risk: single-source, regional concentration

Step 3: Risk Treatment
        → Critical suppliers: quality agreements, annual audits, dual-sourcing
        → High-risk suppliers: enhanced monitoring, contingency plans
        → Medium-risk suppliers: periodic review, performance metrics
        → Low-risk suppliers: standard purchasing controls

Step 4: Ongoing Monitoring
        → Supplier scorecard tracking (quality, delivery, responsiveness)
        → Annual supplier risk reassessment
        → Trigger-based reassessment (quality event, financial change, M&A)
```

---

## Post-Market Risk Monitoring Automation

### Automated Signal Detection

| Data Source | Automation Approach | Alert Threshold |
|------------|--------------------|-----------------|
| Complaint database | Statistical process control (SPC) charts on complaint rates | >2 sigma deviation from baseline |
| Adverse event reports | NLP-based classification + trend analysis | Any serious event; trend >3x baseline |
| Literature monitoring | Automated PubMed/regulatory database searches | New publication on similar device adverse events |
| Field service data | Automated failure rate tracking | Failure rate exceeds design MTBF by >20% |
| Social media/forums | Keyword monitoring for device-related complaints | Cluster of similar complaints in 30-day window |
| Regulatory databases | MAUDE, EUDAMED vigilance module, BfArM monitoring | New recall or safety communication for similar device |

### Risk Management File Update Automation

```
Automated Trigger → Risk Review Decision Tree

New complaint received
    → Classify by hazard category (auto or manual)
    → Check: Known hazard?
        YES → Update frequency data → Recalculate risk level
                → Risk level changed? → Flag for risk management review
        NO  → New hazard identified → Initiate risk analysis
              → Estimate initial risk → Determine controls needed
              → Update risk management file

Trend threshold exceeded
    → Generate trend report with statistical analysis
    → Convene risk management review within 30 days
    → Update risk management file with new probability estimates
    → Evaluate if additional risk controls needed
    → If safety issue: initiate FSCA/field action assessment
```

---

## Cross-Reference: NIST Cybersecurity Framework Risk Assessment

Map ISO 14971 risk management to NIST CSF 2.0 for comprehensive risk coverage:

| ISO 14971 Process | NIST CSF 2.0 Function | Integration Point |
|-------------------|----------------------|-------------------|
| Hazard identification | Identify (ID.RA) | Combine clinical and cyber threat identification |
| Risk estimation | Identify (ID.RA-03, ID.RA-04) | Unified likelihood and impact scales |
| Risk evaluation | Identify (ID.RA-05, ID.RA-06) | Single risk register with combined acceptance criteria |
| Risk control | Protect (PR), Detect (DE) | Security controls as risk mitigations |
| Residual risk evaluation | Govern (GV.RM) | Combined residual risk statement |
| Post-production monitoring | Detect (DE.CM, DE.AE) | Unified monitoring for safety and security events |

> **See also:** `../information-security-manager-iso27001/SKILL.md` for ISO 27001 security controls that serve as risk mitigations.

---

## Cross-Reference: DORA ICT Risk Management

For medical device companies operating as or supplying to financial entities in the EU, the Digital Operational Resilience Act (DORA, Regulation 2022/2554) adds ICT risk requirements:

| DORA Requirement | ISO 14971 Integration | Action |
|-----------------|----------------------|--------|
| ICT risk management framework (Art. 6) | Extend risk management plan to include ICT risks | Add ICT-specific risk categories to hazard analysis |
| ICT incident management (Art. 17) | Align with post-production monitoring | Unified incident classification and response |
| Digital operational resilience testing (Art. 24-27) | Complement risk control verification | Include penetration testing in verification activities |
| Third-party ICT risk (Art. 28-30) | Extend supply chain risk management | Assess ICT service providers per DORA requirements |
| Information sharing (Art. 45) | Enhance post-market information sources | Participate in threat intelligence sharing arrangements |

---

## Enhanced FMEA with Cybersecurity Failure Modes

### Combined Safety-Security FMEA Template

```
COMBINED SAFETY-SECURITY FMEA

Product: [Device Name]
Subsystem: [Subsystem]
Date: [Date]

TRADITIONAL SAFETY FAILURE MODES:
| ID | Item | Function | Failure Mode | Effect | S | Cause | O | Detection | D | RPN | Control |
|----|------|----------|--------------|--------|---|-------|---|-----------|---|-----|---------|
| FM-001 | Sensor | Measure vital sign | Incorrect reading | Wrong diagnosis | 8 | Calibration drift | 4 | Self-test | 3 | 96 | Auto-calibration |

CYBERSECURITY FAILURE MODES:
| ID | Asset | Security Objective | Threat | Attack Vector | Exploitability (O) | Impact (S) | Detection (D) | RPN | Security Control |
|----|-------|-------------------|--------|---------------|-------------------|-----------|---------------|-----|-----------------|
| CS-001 | Sensor data | Integrity | Data manipulation | MITM attack | 3 | 8 | 5 | 120 | TLS + data signing |
| CS-002 | Firmware | Integrity | Malicious update | Supply chain | 2 | 10 | 6 | 120 | Secure boot + code signing |
| CS-003 | User interface | Availability | DoS attack | Network flooding | 5 | 6 | 4 | 120 | Rate limiting + redundancy |

AI/ML FAILURE MODES (if applicable):
| ID | Component | ML Function | Failure Mode | Clinical Effect | S | Cause | O | Detection | D | RPN | ML Control |
|----|-----------|-------------|--------------|----------------|---|-------|---|-----------|---|-----|-----------|
| AI-001 | Classifier | Diagnose condition | False negative | Missed diagnosis | 9 | Distribution shift | 4 | Performance monitoring | 5 | 180 | Drift detection + human review |
| AI-002 | Classifier | Diagnose condition | Biased output | Health disparity | 8 | Unrepresentative training data | 3 | Subgroup analysis | 6 | 144 | Fairness constraints + diverse data |

COMBINED RPN THRESHOLDS:
>200: Critical — Immediate action required (all categories)
100-200: High — Action plan within 30 days
50-100: Medium — Monitor and consider action
<50: Low — Accept and monitor
```

### Cybersecurity-Safety Interaction Analysis

| Safety Control | Cybersecurity Impact | Mitigation |
|---------------|---------------------|------------|
| Alarm system | Alarm suppression via unauthorized access | Access control + alarm integrity monitoring |
| Fail-safe mode | Denial of service forcing perpetual safe mode | Rate limiting + redundant communication |
| Software update | Malicious update compromising safety function | Code signing + dual authorization + rollback capability |
| Data logging | Log tampering concealing safety events | Append-only logs + cryptographic integrity |
| User authentication | Lockout preventing emergency use | Break-glass procedures + local override |

---

## Enhanced Risk Management — AI, Cybersecurity & Cross-Framework Integration

### AI-Specific Risk Management

When managing risk for AI/ML medical devices, extend ISO 14971 with:

- **AI Model Risk:** Training data bias, model drift, adversarial attacks, explainability gaps
- **Performance Degradation:** Monitor for distribution shift, concept drift, and data quality issues
- **Algorithmic Bias:** Demographic parity, equalized odds, calibration across subgroups
- **Human-AI Interaction Risks:** Over-reliance, automation bias, alert fatigue, trust calibration
- **Cross-reference:** See `eu-ai-act-specialist` for EU AI Act risk classification

### Cybersecurity Risk Integration (IEC 81001-5-1)

- **Health Software Cybersecurity:** IEC 81001-5-1 extends ISO 14971 for cybersecurity
- **Threat Modeling:** STRIDE methodology applied to medical device architecture
- **Cybersecurity FMEA:** Failure modes include unauthorized access, data breach, ransomware, supply chain attack
- **Vulnerability Management:** CVSS scoring integrated with ISO 14971 severity/probability matrix
- **Cross-reference:** See `infrastructure-compliance-auditor` for technical security checks

### Supply Chain Risk Management

- **Component Risk:** Third-party software vulnerabilities (SBOM-based assessment)
- **Supplier Risk:** Single-source dependencies, geopolitical risks, quality history
- **Cloud Risk:** Data residency, service availability, vendor lock-in
- **Cross-reference:** See `nis2-directive-specialist` for NIS2 supply chain requirements

### Cross-Framework Risk Mapping

| Risk Area | ISO 14971 | NIST CSF 2.0 | DORA | NIS2 |
|-----------|-----------|-------------|------|------|
| Risk Assessment | Clause 4 | ID.RA | Art. 6 | Art. 21.1 |
| Risk Treatment | Clause 7 | PR (all) | Art. 9 | Art. 21.2 |
| Monitoring | Clause 9 | DE.CM | Art. 10 | Art. 21.2.f |
| Incident Response | Clause 9 | RS.MA | Art. 17 | Art. 23 |
| Continuous Improvement | Clause 10 | ID.IM | Art. 13 | Art. 21.2.f |
