# Control Mapping: SOC 2 / ISO 27001 / NIST CSF / Others

Detailed control mapping across major compliance frameworks. Reference table for shared-evidence implementation.

For each control area, mapping shows where the same underlying control satisfies multiple frameworks. Use this to build a common control catalog.

---

## Access Management

### Logical access control (RBAC + MFA + SSO)

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC6.1 |
| ISO 27001:2022 | A.5.15, A.5.18, A.8.5 |
| NIST CSF 2.0 | PR.AA-01, PR.AA-02, PR.AA-03 |
| NIST SP 800-53 | AC-2, AC-3, IA-2 |
| HIPAA | §164.308(a)(4), §164.312(a)(1) |
| GDPR | Art.32(1)(b) (security of processing) |
| PCI-DSS v4.0 | Req 7 (need-to-know), Req 8 (authentication) |
| NIS2 | Art.21.2(j) |
| DORA | Art.9(4) |
| ISO 13485 | 4.1.5 |

### Privileged access management

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC6.1, CC6.6 |
| ISO 27001:2022 | A.5.16, A.5.17, A.8.4 |
| NIST CSF | PR.AA-04, PR.PS-03 |
| HIPAA | §164.308(a)(4)(ii) |
| PCI-DSS v4.0 | Req 7.2.5 |

### Access reviews (periodic)

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC6.3 |
| ISO 27001 | A.5.18, A.8.3 |
| NIST CSF | PR.AA-04 |
| HIPAA | §164.308(a)(4)(ii)(C) |
| PCI-DSS | Req 7.2.4 |

### Termination access removal

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC6.3 |
| ISO 27001 | A.6.4 |
| HIPAA | §164.308(a)(3)(ii)(C) |
| NIST CSF | PR.AA-02 |

---

## Encryption

### Encryption at rest

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC6.7 |
| ISO 27001 | A.8.24 |
| NIST CSF | PR.DS-01 |
| HIPAA | §164.312(a)(2)(iv) |
| PCI-DSS | Req 3.4, 3.5 |
| GDPR | Art.32(1)(a) |

### Encryption in transit

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC6.7 |
| ISO 27001 | A.8.24 |
| NIST CSF | PR.DS-02 |
| HIPAA | §164.312(e)(2)(ii) |
| PCI-DSS | Req 4.1, 4.2 |

### Key management

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC6.7 |
| ISO 27001 | A.8.24 |
| NIST CSF | PR.DS-01 |
| PCI-DSS | Req 3.6, 3.7 |

---

## Logging and Monitoring

### Security event logging

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC7.2 |
| ISO 27001 | A.8.15, A.8.16 |
| NIST CSF | DE.CM-01, DE.AE-02 |
| HIPAA | §164.312(b) |
| PCI-DSS | Req 10 |
| NIS2 | Art.21.2(b) |
| DORA | Art.10 |
| GDPR | Art.30 (records of processing) |

### Log retention

| Framework | Typical requirement |
|-----------|---------------------|
| SOC 2 | Reasonable for audit (1 year typical) |
| ISO 27001 | Defined per A.8.15 |
| NIST CSF | Per agency / sector |
| HIPAA | 6 years |
| PCI-DSS | 1 year (3 months online + 9 months archive) |

### Anomaly detection / SIEM

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC7.1, CC7.2 |
| ISO 27001 | A.8.16 |
| NIST CSF | DE.AE-02, DE.CM-09 |
| PCI-DSS | Req 10.4 |

---

## Incident Response

### Incident response plan

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC7.3 |
| ISO 27001 | A.5.24, A.5.25 |
| NIST CSF | RS.MA, RS.AN |
| HIPAA | §164.308(a)(6) |
| PCI-DSS | Req 12.10 |
| NIS2 | Art.23 |
| DORA | Art.17, Art.19 |
| GDPR | Art.33, Art.34 |

### Breach notification

| Framework | Timing |
|-----------|--------|
| GDPR | 72 hours to supervisory authority; without undue delay to subjects |
| HIPAA | 60 days to affected individuals (CE); 60 days post-discovery |
| PCI-DSS | Immediately to card brands |
| NIS2 | 24 hours (early warning); 72 hours (incident notification) |
| DORA | 4 hours (major incident initial); 1 week (intermediate); 1 month (final) |

### Forensic capability

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC7.4 |
| ISO 27001 | A.5.28 |
| NIST CSF | RS.AN-04 |
| PCI-DSS | Req 12.10.4 |

---

## Risk Management

### Risk assessment

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC3.1, CC3.2 |
| ISO 27001 | Clause 6.1.2 |
| NIST CSF | ID.RA |
| HIPAA | §164.308(a)(1)(ii)(A) |
| NIS2 | Art.21.1 |
| DORA | Art.6 |
| GDPR | Art.35 (DPIA) |
| ISO 14971 | (Medical devices specific) |

### Risk treatment

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC3.3, CC3.4 |
| ISO 27001 | Clause 6.1.3 |
| NIST CSF | ID.RA-06 |

---

## Vendor Management

### Vendor due diligence

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC9.2 |
| ISO 27001 | A.5.19, A.5.20 |
| NIST CSF | GV.SC-04 |
| HIPAA | §164.308(b) (BAA) |
| PCI-DSS | Req 12.8 |
| NIS2 | Art.21.2(d) |
| DORA | Art.28 |
| GDPR | Art.28 (DPA) |

### Vendor SOC 2 / ISO 27001 reports

Required (or strongly evidence): SOC 2, ISO 27001, NIS2, DORA, GDPR (for processors).

### Sub-processor management

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC9.2 |
| GDPR | Art.28.4 |
| DORA | Art.28 |

---

## Change Management

### Change control process

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC8.1 |
| ISO 27001 | A.5.36, A.8.32 |
| NIST CSF | PR.PS-06 |
| HIPAA | §164.308(a)(8) |
| PCI-DSS | Req 6.5 |

### Code review

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC8.1 |
| ISO 27001 | A.8.28 |
| PCI-DSS | Req 6.3.2 |
| NIST | SC-30 (SP 800-53) |

### Production deployment approvals

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC8.1 |
| ISO 27001 | A.5.36 |

---

## Backup and Recovery

### Backups

| Framework | Reference |
|-----------|-----------|
| SOC 2 | A1.2 |
| ISO 27001 | A.8.13 |
| NIST CSF | RC.RP, PR.DS-11 |
| HIPAA | §164.308(a)(7)(ii)(A) |
| PCI-DSS | Req 9.5 (media), Req 10 (log backup) |
| GDPR | Art.32 |

### Disaster recovery

| Framework | Reference |
|-----------|-----------|
| SOC 2 | A1.2, A1.3 |
| ISO 27001 | A.5.30 |
| NIST CSF | RC.RP |
| HIPAA | §164.308(a)(7) |
| NIS2 | Art.21.2(c) |
| DORA | Art.11 |

---

## Training and Awareness

### Security awareness training

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC1.4 |
| ISO 27001 | A.6.3 |
| NIST CSF | PR.AT-01 |
| HIPAA | §164.308(a)(5) |
| PCI-DSS | Req 12.6 |
| NIS2 | Art.21.2(g) |
| DORA | Art.13 |
| GDPR | Art.39(1)(b) |
| EU AI Act | Art.4 (AI literacy) |

### Role-specific training

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC1.4 |
| ISO 27001 | A.6.3 |
| HIPAA | §164.530(b) (privacy) + §164.308 (security) |
| PCI-DSS | Req 12.6 |

---

## Vulnerability Management

### Vulnerability scanning

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC7.1, CC7.5 |
| ISO 27001 | A.8.8 |
| NIST CSF | ID.RA-01 |
| PCI-DSS | Req 11.3 |

### Penetration testing

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC4.1 |
| ISO 27001 | A.5.7, A.8.29 |
| NIST CSF | ID.RA-08 |
| PCI-DSS | Req 11.4 |

### Patch management

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC7.1 |
| ISO 27001 | A.8.8 |
| NIST CSF | PR.PS-01 |
| HIPAA | §164.308(a)(8) |
| PCI-DSS | Req 6.3.3 |

---

## Physical Security

### Physical access control

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC6.4 |
| ISO 27001 | A.7.2, A.7.3 |
| NIST CSF | PR.AA-06 |
| HIPAA | §164.310(a) |
| PCI-DSS | Req 9 |

### Media handling

| Framework | Reference |
|-----------|-----------|
| SOC 2 | CC6.5 |
| ISO 27001 | A.7.10, A.7.14 |
| HIPAA | §164.310(d) |
| PCI-DSS | Req 9.4, 9.5 |

---

## Quick lookup for common evidence

| Evidence type | Satisfies |
|--------------|-----------|
| Information security policy (signed) | SOC 2 CC1, ISO 27001 5.2, NIST CSF GV.PO, HIPAA §164.308(a)(1), PCI Req 12.1 |
| Risk assessment (annual) | SOC 2 CC3, ISO 27001 6.1.2, NIST CSF ID.RA, HIPAA §164.308(a)(1), GDPR DPIA |
| Access review records | SOC 2 CC6.3, ISO 27001 A.5.18, NIST CSF PR.AA-04, HIPAA §164.308(a)(4), PCI Req 7.2.4 |
| Vulnerability scan reports | SOC 2 CC7.1, ISO 27001 A.8.8, NIST CSF ID.RA-01, PCI Req 11.3 |
| Pen test report | SOC 2 CC4.1, ISO 27001 A.5.7, PCI Req 11.4 |
| Training completion records | SOC 2 CC1.4, ISO 27001 A.6.3, HIPAA §164.530, PCI Req 12.6, GDPR Art.39, AI Act Art.4 |
| Incident response runbook | SOC 2 CC7.3, ISO 27001 A.5.24, HIPAA §164.308(a)(6), GDPR Art.33, NIS2 Art.23 |
| DR test report | SOC 2 A1.2, ISO 27001 A.5.30, HIPAA §164.308(a)(7), NIS2 Art.21.2(c), DORA Art.11 |
| Vendor SOC 2 reports collected | SOC 2 CC9.2, ISO 27001 A.5.19, GDPR Art.28, NIS2 Art.21.2(d) |

---

## Mapping maintenance

| Item | Frequency |
|------|-----------|
| Control catalog review | Annual |
| Framework requirement update check | Annual (more often per framework news) |
| Mapping validation with auditor | At each audit |
| New control added | Inline as introduced |
| New framework added | Map at decision-to-pursue |

---

## Cheat sheet

| Question | Answer |
|----------|--------|
| How to start mapping? | Pick most-comprehensive framework as base (often ISO 27001); map others against it |
| Best framework for control granularity? | ISO 27001:2022 Annex A (93 controls) or NIST SP 800-53 (very granular) |
| Mapping format? | Spreadsheet or YAML; per-control row with framework columns |
| Auditor disputes mapping? | Common; come prepared with rationale; may need framework-specific evidence |
| GRC platform required for mapping? | Beyond ~50 controls, very helpful |
