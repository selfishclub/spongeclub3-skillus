# Assessment, Roadmap, and Validation

Read this when running an engagement: how to assess each function, the phased maturity-assessment workflow, the 12-month implementation roadmap, validation checkpoints, and success criteria.

---

## Infrastructure Security Assessment

### Assessment Across All Functions

**GOVERN Assessment:**
- Review governance documentation completeness
- Validate board reporting cadence and content
- Assess supply chain risk management program maturity
- Evaluate policy framework coverage and currency

**IDENTIFY Assessment:**
- Audit asset inventory accuracy (sample validation)
- Review risk assessment methodology and outputs
- Evaluate threat intelligence integration
- Assess improvement tracking and closure rates

**PROTECT Assessment:**
- Test authentication controls (MFA enforcement, password policy)
- Review access control configurations (least privilege validation)
- Assess encryption implementation (at rest, in transit, key management)
- Validate hardening baselines against benchmarks
- Test backup and recovery capabilities

**DETECT Assessment:**
- Validate SIEM log coverage (are all critical systems sending logs?)
- Test detection rules against MITRE ATT&CK scenarios
- Assess SOC operational maturity
- Review threat hunting program effectiveness

**RESPOND Assessment:**
- Review incident response plan currency and completeness
- Evaluate IR team capabilities and training
- Assess forensic readiness
- Test communication plans and notification workflows

**RECOVER Assessment:**
- Test disaster recovery procedures and measure RPO/RTO achievement
- Validate backup integrity through restore testing
- Assess recovery communication effectiveness
- Review post-incident improvement tracking

---

## Maturity Assessment Workflow

### Phase 1: Preparation (Week 1)

1. **Define Scope** — Identify organizational units, systems, and processes in scope
2. **Gather Documentation** — Collect policies, procedures, architecture diagrams, audit reports
3. **Schedule Interviews** — Book time with CISO, IT leadership, security team, business stakeholders
4. **Review Prior Assessments** — Analyze previous CSF assessments, audit findings, penetration test results

### Phase 2: Assessment (Weeks 2-3)

1. **Function-by-Function Evaluation** — Assess each category using the csf_maturity_assessor tool
2. **Evidence Collection** — Gather artifacts supporting each score (screenshots, configs, reports)
3. **Stakeholder Interviews** — Validate documented state against operational reality
4. **Technical Validation** — Verify technical controls through testing (not just documentation)

### Phase 3: Analysis (Week 4)

1. **Score Compilation** — Aggregate scores across all functions and categories
2. **Gap Analysis** — Compare current profile to target profile
3. **Risk Prioritization** — Rank gaps by risk exposure and remediation effort
4. **Cross-Reference** — Map findings to applicable regulatory requirements

### Phase 4: Reporting and Roadmap (Week 5)

1. **Executive Summary** — High-level maturity scores with trend analysis
2. **Detailed Findings** — Category-level findings with evidence and recommendations
3. **Remediation Roadmap** — Phased plan with milestones, owners, and resource requirements
4. **Board Presentation** — Strategic summary suitable for governance bodies

---

## Implementation Roadmap

### Phase 1: Foundation (Months 1-3)

**Focus: GOVERN + IDENTIFY**

- Establish cybersecurity governance structure (GV.RR)
- Define organizational context and risk appetite (GV.OC, GV.RM)
- Develop or update cybersecurity policy framework (GV.PO)
- Conduct comprehensive asset inventory (ID.AM)
- Perform baseline risk assessment (ID.RA)

**Deliverables:**
- Cybersecurity charter and governance structure
- Risk appetite statement
- Policy framework
- Asset inventory
- Baseline risk register

### Phase 2: Core Protections (Months 4-6)

**Focus: PROTECT**

- Implement identity and access management improvements (PR.AA)
- Deploy MFA organization-wide (PR.AA)
- Enhance data protection controls (PR.DS)
- Apply hardening baselines to all systems (PR.PS)
- Establish security awareness program (PR.AT)

**Deliverables:**
- MFA deployment complete
- PAM solution operational
- Data classification applied to critical data
- Hardened system baselines deployed
- Training program launched

### Phase 3: Visibility and Response (Months 7-9)

**Focus: DETECT + RESPOND**

- Deploy or enhance SIEM/SOC capabilities (DE.CM)
- Develop detection rules mapped to MITRE ATT&CK (DE.AE)
- Update incident response plan and test via tabletop (RS.MA)
- Establish forensic readiness (RS.AN)
- Develop communication templates and procedures (RS.CO)

**Deliverables:**
- SIEM operational with critical log sources
- Detection coverage for top ATT&CK techniques
- Tested incident response plan
- Forensic toolkit and procedures
- Communication templates approved

### Phase 4: Resilience and Maturity (Months 10-12)

**Focus: RECOVER + Continuous Improvement**

- Test and validate disaster recovery procedures (RC.RP)
- Establish recovery communication procedures (RC.CO)
- Launch supply chain risk management program (GV.SC)
- Implement continuous improvement processes (ID.IM)
- Conduct year-one maturity reassessment

**Deliverables:**
- DR procedures tested and validated
- C-SCRM program operational
- Improvement tracking system active
- Year-one maturity assessment complete
- Year-two roadmap drafted

---

## Validation Checkpoints

### Before Starting Assessment
- [ ] Scope defined and approved by stakeholders
- [ ] Assessment team identified with appropriate expertise
- [ ] Prior assessment results and audit reports collected
- [ ] Target tier defined for each function

### During Assessment
- [ ] Each category scored with supporting evidence
- [ ] Stakeholder interviews conducted and documented
- [ ] Technical controls validated (not just documented)
- [ ] Cross-framework obligations identified

### After Assessment
- [ ] Gap analysis completed with prioritized recommendations
- [ ] Remediation roadmap with milestones and owners
- [ ] Executive summary prepared for governance bodies
- [ ] Reassessment timeline established

### Implementation Validation
- [ ] Phase milestones achieved on schedule
- [ ] Controls tested and validated post-implementation
- [ ] Metrics established and baseline measurements taken
- [ ] Continuous monitoring operational

---

## Success Criteria

- Current profile documented with evidence-backed scores for all 22 CSF 2.0 categories across all 6 functions
- Target profile defined with stakeholder-approved tier targets aligned to organizational risk appetite and regulatory obligations
- Gap analysis completed with each gap scored by risk exposure, remediation effort, and business impact, producing a prioritized roadmap
- GOVERN function fully implemented: cybersecurity governance charter, board reporting cadence established, CISO role defined, risk appetite documented
- Cross-framework control mapping completed for all applicable compliance obligations (ISO 27001, SOC 2, HIPAA, PCI-DSS) reducing audit duplication by 30%+
- Maturity reassessment conducted within 12 months showing measurable tier improvement in at least 75% of assessed categories
- Supply chain risk management program (GV.SC) operational with tiered supplier assessments and SBOM tracking for critical applications
