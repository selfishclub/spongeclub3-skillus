# Cloud Security, Zero Trust & Cross-Framework Mapping

Cloud-provider control mappings (AWS/Azure/GCP), Zero Trust architecture integration, hardware security key (FIDO2/WebAuthn) requirements, supply chain security controls, and mappings from ISO 27001:2022 to SOC 2, NIST CSF 2.0, and NIS2. Read this when implementing controls in a specific cloud, designing Zero Trust, hardening authentication, managing vendor/supply-chain risk, or pursuing multiple certifications at once.

## Cross-Reference: SOC 2 Control Mapping

Map ISO 27001:2022 controls to SOC 2 Trust Services Criteria for organizations requiring both certifications:

| SOC 2 Trust Criteria | ISO 27001:2022 Controls | Notes |
|----------------------|------------------------|-------|
| CC1 — Control Environment | A.5.1, A.5.2, A.5.4, A.6.2 | Governance and organizational structure |
| CC2 — Communication and Information | A.5.14, A.6.3, A.6.8, A.5.37 | Internal/external communication |
| CC3 — Risk Assessment | A.5.7, Clause 6.1.2 (risk assessment) | Threat identification and analysis |
| CC4 — Monitoring Activities | A.8.15, A.8.16, A.5.35, A.5.36 | Logging, monitoring, compliance |
| CC5 — Control Activities | A.5.15-A.5.18, A.8.1-A.8.5 | Access control and authentication |
| CC6 — Logical and Physical Access | A.5.15, A.7.1, A.7.2, A.8.2, A.8.3 | Access management |
| CC7 — System Operations | A.8.7, A.8.8, A.8.9, A.8.32 | Change management, malware, vulnerability management |
| CC8 — Change Management | A.8.25, A.8.32, A.8.31 | SDLC, change control, environment separation |
| CC9 — Risk Mitigation | A.5.19-A.5.22, A.8.30 | Vendor/supplier risk management |
| Availability | A.5.29, A.5.30, A.8.6, A.8.14 | Business continuity, capacity, redundancy |
| Confidentiality | A.5.12, A.5.13, A.8.11, A.8.12, A.8.24 | Classification, DLP, encryption |
| Processing Integrity | A.8.25-A.8.29, A.8.33 | Secure development, testing |
| Privacy | A.5.34, A.8.10, A.8.11 | PII protection, deletion, masking |

> **See also:** `../soc2-compliance-specialist/SKILL.md` for full SOC 2 compliance workflows.

---

## Cross-Reference: NIS2 Directive Alignment

The NIS2 Directive (EU 2022/2555) mandates cybersecurity measures for essential and important entities, including healthcare organizations. ISO 27001 provides a strong foundation for NIS2 compliance:

| NIS2 Requirement (Art. 21) | ISO 27001:2022 Controls | Gap Analysis |
|---------------------------|------------------------|--------------|
| (a) Risk analysis and IS policies | Clause 6.1.2, A.5.1 | Fully covered |
| (b) Incident handling | A.5.24-A.5.28 | Add NIS2 reporting timelines (24h/72h) |
| (c) Business continuity and crisis management | A.5.29, A.5.30 | Add crisis management procedures |
| (d) Supply chain security | A.5.19-A.5.22 | Strengthen ICT supply chain assessment |
| (e) Security in network and IS acquisition | A.8.25-A.8.29 | Add vulnerability handling and disclosure |
| (f) Policies for assessing cybersecurity effectiveness | A.5.35, A.5.36 | Add metrics-based effectiveness measurement |
| (g) Basic cyber hygiene and training | A.6.3, A.6.8 | Covered |
| (h) Policies on use of cryptography and encryption | A.8.24 | Covered |
| (i) Human resources security and access control | A.5.15-A.5.18, A.6.1-A.6.8 | Covered |
| (j) Multi-factor authentication and secure communications | A.8.5, A.8.20-A.8.22 | Ensure MFA enforced for all critical systems |

**NIS2-specific additions beyond ISO 27001:**
- **Incident reporting:** 24-hour early warning to CSIRT, 72-hour incident notification, 1-month final report
- **Management accountability:** Senior management must approve cybersecurity measures and undergo training
- **Penalties:** Up to EUR 10M or 2% of global turnover for essential entities
- **Supply chain:** Must assess each direct supplier's cybersecurity practices

> **See also:** `../nis2-compliance-specialist/SKILL.md` for complete NIS2 implementation workflows.

---

## Cloud Security Controls

### AWS-Specific Controls

| ISO 27001 Control | AWS Implementation | Service |
|-------------------|-------------------|---------|
| A.5.23 Cloud services | AWS Organizations, SCPs | AWS Organizations |
| A.8.2 Privileged access | IAM roles, permission boundaries | AWS IAM |
| A.8.3 Access restriction | Resource policies, VPC endpoints | IAM, VPC |
| A.8.5 Secure authentication | IAM Identity Center, MFA | IAM |
| A.8.9 Configuration management | AWS Config rules, conformance packs | AWS Config |
| A.8.12 Data leakage prevention | Macie, S3 Block Public Access | Macie |
| A.8.13 Information backup | AWS Backup, cross-region replication | AWS Backup |
| A.8.15 Logging | CloudTrail, CloudWatch Logs | CloudTrail |
| A.8.16 Monitoring | GuardDuty, Security Hub | GuardDuty |
| A.8.20 Network security | Security Groups, NACLs, WAF | VPC, WAF |
| A.8.22 Network segregation | VPC subnets, Transit Gateway | VPC |
| A.8.24 Cryptography | KMS, CloudHSM, ACM | KMS |

### Azure-Specific Controls

| ISO 27001 Control | Azure Implementation | Service |
|-------------------|---------------------|---------|
| A.5.23 Cloud services | Management Groups, Azure Policy | Azure Policy |
| A.8.2 Privileged access | PIM, RBAC, Conditional Access | Entra ID |
| A.8.5 Secure authentication | Entra ID MFA, passwordless | Entra ID |
| A.8.9 Configuration management | Azure Policy, Blueprints | Azure Policy |
| A.8.12 Data leakage prevention | Microsoft Purview DLP | Purview |
| A.8.15 Logging | Azure Monitor, Log Analytics | Monitor |
| A.8.16 Monitoring | Microsoft Defender for Cloud | Defender |
| A.8.20 Network security | NSGs, Azure Firewall, Front Door WAF | Network |
| A.8.24 Cryptography | Azure Key Vault, Managed HSM | Key Vault |

### GCP-Specific Controls

| ISO 27001 Control | GCP Implementation | Service |
|-------------------|-------------------|---------|
| A.5.23 Cloud services | Organization policies, Resource Manager | Resource Manager |
| A.8.2 Privileged access | IAM, Workload Identity | Cloud IAM |
| A.8.5 Secure authentication | Identity Platform, 2-Step Verification | Identity |
| A.8.9 Configuration management | Security Health Analytics, Assured Workloads | SCC |
| A.8.12 Data leakage prevention | Cloud DLP (Sensitive Data Protection) | DLP |
| A.8.15 Logging | Cloud Audit Logs, Cloud Logging | Logging |
| A.8.16 Monitoring | Security Command Center, Chronicle SIEM | SCC |
| A.8.20 Network security | VPC firewall rules, Cloud Armor | VPC, Cloud Armor |
| A.8.24 Cryptography | Cloud KMS, Cloud HSM, CMEK | Cloud KMS |

---

## Zero Trust Architecture Integration

Align ISO 27001 controls with Zero Trust principles (NIST SP 800-207):

### Zero Trust Pillars Mapped to ISO 27001

| Zero Trust Pillar | Principle | ISO 27001 Controls | Implementation |
|-------------------|-----------|-------------------|----------------|
| Identity | Verify explicitly | A.5.16, A.5.17, A.8.5 | MFA everywhere, continuous authentication, identity governance |
| Devices | Validate device health | A.8.1, A.8.7, A.8.9 | Endpoint detection and response (EDR), device compliance checks |
| Networks | Segment and encrypt | A.8.20-A.8.22, A.8.24 | Microsegmentation, mTLS, encrypted tunnels |
| Applications | Secure by design | A.8.25-A.8.29 | SAST/DAST, runtime protection, API security |
| Data | Classify and protect | A.5.12, A.5.13, A.8.11, A.8.12 | Data classification, DLP, rights management |
| Visibility | Monitor and analyze | A.8.15, A.8.16, A.5.7 | SIEM/SOAR, threat intelligence, behavioral analytics |

### Zero Trust Implementation Roadmap

```
Phase 1: Foundation (0-6 months)
├── Implement identity provider with MFA for all users
├── Deploy EDR on all endpoints
├── Enable centralized logging and SIEM
└── Classify critical data assets

Phase 2: Enhancement (6-12 months)
├── Implement network microsegmentation
├── Deploy conditional access policies
├── Enable continuous device compliance monitoring
└── Implement DLP for classified data

Phase 3: Maturation (12-18 months)
├── Deploy zero-trust network access (ZTNA) replacing VPN
├── Implement just-in-time (JIT) privileged access
├── Enable automated threat response (SOAR)
└── Continuous verification with behavioral analytics
```

---

## Hardware Security Key Requirements

### FIDO2/WebAuthn Implementation

For high-assurance authentication per A.5.17 and A.8.5:

| Requirement | Specification | Priority |
|-------------|---------------|----------|
| Admin accounts | Hardware security key (YubiKey 5, Titan) mandatory | Critical |
| Developer accounts | Hardware key or platform authenticator | High |
| All employees | Hardware key recommended; MFA minimum | Medium |
| Service accounts | Certificate-based or workload identity | High |

**Supported standards:**
- FIDO2 / WebAuthn (passwordless primary authentication)
- FIDO U2F (second-factor authentication)
- PIV/Smart Card (legacy enterprise systems)
- TOTP (fallback only — hardware keys preferred)

**Deployment checklist:**
- [ ] Procure minimum 2 hardware keys per critical user (primary + backup)
- [ ] Register keys with identity provider (Entra ID, Okta, Google Workspace)
- [ ] Enforce phishing-resistant MFA policy for privileged access
- [ ] Disable SMS/voice MFA for admin accounts
- [ ] Document key recovery procedures
- [ ] Test break-glass procedures with backup keys

---

## Supply Chain Security Controls

### ICT Supply Chain Risk Management (A.5.19-A.5.22)

| Control Area | Requirements | Evidence |
|-------------|-------------|----------|
| Supplier assessment | Security questionnaire + evidence review | Completed assessment scorecard |
| Contractual requirements | Security clauses in all vendor agreements | Signed agreements with security schedule |
| Software supply chain | SBOM requirements, dependency scanning | SBOM in CycloneDX/SPDX format |
| Continuous monitoring | Monitor supplier security posture changes | Quarterly supplier security reviews |
| Incident notification | Require supplier breach notification within 24 hours | Contractual clause + test exercises |

### Software Bill of Materials (SBOM) Requirements

| Element | Description | Standard |
|---------|-------------|----------|
| Component inventory | All direct and transitive dependencies | CycloneDX or SPDX |
| Vulnerability tracking | Map components to known CVEs | OSV, NVD integration |
| License compliance | Track all open-source licenses | SPDX license identifiers |
| Update cadence | Regenerate SBOM on every release | CI/CD integration |
| Sharing | Provide SBOM to customers on request | Machine-readable format |

### Third-Party Risk Tiers

| Tier | Access Level | Assessment Frequency | Assessment Depth |
|------|-------------|---------------------|-----------------|
| Critical | Processes/stores sensitive data, system access | Annual on-site + continuous monitoring | Full security audit, penetration test review |
| High | Access to internal systems or non-sensitive data | Annual questionnaire + evidence | Security questionnaire + SOC 2 report review |
| Medium | Limited access, SaaS tools | Biennial questionnaire | Security questionnaire |
| Low | No data access, no system access | On onboarding | Basic due diligence |

---

## Cross-Framework Mapping Table

| Requirement Area | ISO 27001:2022 | SOC 2 TSC | NIST CSF 2.0 | NIS2 (Art. 21) |
|-----------------|----------------|-----------|--------------|----------------|
| Governance | A.5.1-A.5.4 | CC1.1-CC1.5 | GV.OC, GV.RM | Art. 20 |
| Risk management | Clause 6.1.2, A.5.7 | CC3.1-CC3.4 | ID.RA | Art. 21(2)(a) |
| Access control | A.5.15-A.5.18, A.8.2-A.8.5 | CC6.1-CC6.8 | PR.AA | Art. 21(2)(i) |
| Incident management | A.5.24-A.5.28 | CC7.3-CC7.5 | RS.MA, RS.AN | Art. 21(2)(b), Art. 23 |
| Business continuity | A.5.29-A.5.30 | A1.1-A1.3 | RC.RP | Art. 21(2)(c) |
| Supply chain | A.5.19-A.5.22 | CC9.1-CC9.2 | GV.SC | Art. 21(2)(d) |
| Cryptography | A.8.24 | CC6.1, CC6.7 | PR.DS | Art. 21(2)(h) |
| Network security | A.8.20-A.8.22 | CC6.6 | PR.IR | Art. 21(2)(e) |
| Vulnerability management | A.8.8 | CC7.1 | ID.RA-01 | Art. 21(2)(e) |
| Awareness and training | A.6.3 | CC1.4 | PR.AT | Art. 21(2)(g) |
| Logging and monitoring | A.8.15-A.8.16 | CC7.2 | DE.CM, DE.AE | Art. 21(2)(f) |
| Data protection | A.5.34, A.8.10-A.8.12 | P1-P8 | PR.DS | Art. 21(2)(e) |
| Secure development | A.8.25-A.8.29 | CC8.1 | PR.DS | Art. 21(2)(e) |
| Asset management | A.5.9-A.5.11 | CC6.1 | ID.AM | Art. 21(2)(a) |

> **Cross-references:** See `../gdpr-dsgvo-expert/SKILL.md` for GDPR privacy controls mapping, and `../risk-management-specialist/SKILL.md` for ISO 14971 risk management integration with ISO 27001.

---

## ISO 27001:2022 Enhanced Controls & Cross-Framework Integration

### Annex A Control Themes (93 Controls)

| Theme | Controls | Key Areas |
|-------|----------|-----------|
| **Organizational (37)** | A.5.1-A.5.37 | Policies, roles, threat intelligence, asset management, access, supplier security |
| **People (8)** | A.6.1-A.6.8 | Screening, T&C, awareness, disciplinary, termination, remote work, reporting |
| **Physical (14)** | A.7.1-A.7.14 | Perimeters, entry, offices, monitoring, utilities, cabling, equipment, storage media |
| **Technological (34)** | A.8.1-A.8.34 | Endpoints, access, authentication, code, config, data, backup, logging, networks, web |

### Hardware Security Key Requirements

- **YubiKey 5 Series:** Required for admin accounts, cloud console access, VPN, code signing
- **FIDO2/WebAuthn:** Phishing-resistant MFA for all users within 90 days of ISMS deployment
- **Policy:** SMS/voice MFA PROHIBITED (SIM swapping risk). TOTP acceptable as interim for non-admin
- **Backup Keys:** Minimum 2 hardware keys per user (primary + backup stored securely)
- **Recovery:** Manager approval + identity verification required for key replacement

### Zero Trust Architecture Integration

- **Never Trust, Always Verify:** All access decisions based on identity, device, and context
- **Microsegmentation:** Network segmentation at workload level, not just network perimeter
- **Least Privilege:** Just-in-time access, time-bounded permissions, automated deprovisioning
- **Continuous Verification:** Session-level authentication, device health checks, behavioral analytics

### Cross-Framework Mapping (ISO 27001 ↔ SOC 2 ↔ NIST CSF ↔ NIS2)

| ISO 27001 | SOC 2 TSC | NIST CSF 2.0 | NIS2 Art.21 |
|-----------|-----------|-------------|-------------|
| A.5.1 Policies | CC1.1 | GV.PO | Art.21.2.a |
| A.5.23 Cloud security | CC6.7 | PR.DS | Art.21.2.e |
| A.5.24 Incident mgmt | CC7.4 | RS.MA | Art.21.2.b |
| A.6.3 Awareness | CC1.4 | PR.AT | Art.21.2.g |
| A.8.5 Authentication | CC6.1 | PR.AA | Art.21.2.j |
| A.8.9 Config mgmt | CC8.1 | PR.PS | Art.21.2.e |
| A.8.15 Logging | CC7.2 | DE.CM | Art.21.2.b |
| A.8.24 Cryptography | CC6.7 | PR.DS | Art.21.2.h |

### Supply Chain Security Controls

- **Supplier Risk Assessment:** Due diligence before onboarding, annual reassessment
- **Contractual Security Clauses:** Data protection, incident reporting, audit rights, exit terms
- **Continuous Monitoring:** Vendor security ratings, certificate expiry alerts, breach notifications
- **SBOM Requirements:** Software Bill of Materials for all third-party software components
