# SOC 2 Pre-Audit Punch List

Detailed punch list per Trust Services Criterion (TSC). For each item: evidence required, common gap, remediation pattern, evidence template.

This is the working document for the audit-prep sprint. Walk through each item; mark complete or gap; remediate gaps.

---

## CC1 — Control Environment

### CC1.1 — Demonstrates commitment to integrity / ethical values

| Item | Evidence | Common gap |
|------|----------|------------|
| Code of Conduct | Signed acknowledgment per employee | Not signed for recent hires |
| Whistleblower / ethics hotline | Policy + hotline number; usage stats | Hotline exists but never used (or used and ignored) |
| Background checks | Per-hire vendor reports | Missing for early hires |

### CC1.2 — Board oversight independence

| Item | Evidence | Common gap |
|------|----------|------------|
| Board composition | Org chart, independence per director | All-insider board |
| Board minutes referencing security | Quarterly minutes | Security never on board agenda |
| Audit committee charter | Charter document | No audit committee at startup stage |

### CC1.3 — Structures / authorities / responsibilities

| Item | Evidence | Common gap |
|------|----------|------------|
| Org chart | Current chart with reporting lines | Out-of-date (mergers, restructuring) |
| Role responsibilities documented | Job descriptions or RACI matrix | Verbal-only |
| Segregation of duties | Documented in roles or matrix | Same person creates + approves changes |

### CC1.4 — Demonstrates commitment to competence

| Item | Evidence | Common gap |
|------|----------|------------|
| Security training | LMS completion records | Annual training skipped for some employees |
| Role-specific training | Per-role training plans | Generic training only |
| New-hire security onboarding | Onboarding checklist with sign-off | Inconsistent |

### CC1.5 — Holds individuals accountable

| Item | Evidence | Common gap |
|------|----------|------------|
| Performance reviews referencing security | Sample reviews | Security not in performance criteria |
| Disciplinary action for security violations | Sample tickets / records | No documented enforcement |

---

## CC2 — Communication and Information

### CC2.1 — Internal information communication

| Item | Evidence | Common gap |
|------|----------|------------|
| Security policy + procedures published | Wiki / intranet links | Out-of-date version live |
| Incident communication channels | Slack channels, email lists | Reliance on tribal knowledge |

### CC2.2 — External communication

| Item | Evidence | Common gap |
|------|----------|------------|
| Customer-facing security documentation | Trust page / whitepaper | Not published |
| Sub-service org communication | Vendor contact + escalation paths | Lost when CSM changes |
| Privacy notice (if P1 in scope) | Published privacy page | Out-of-date |

### CC2.3 — Communication with external parties

| Item | Evidence | Common gap |
|------|----------|------------|
| Customer SLA reporting | Monthly SLA reports | Not regularly produced |
| Incident notification process | DPA notification clauses + sample | Never invoked, untested |

---

## CC3 — Risk Assessment

### CC3.1 — Specifies suitable objectives

| Item | Evidence | Common gap |
|------|----------|------------|
| Business + security objectives documented | Strategy doc | Not connected to security |
| Performance / availability targets | SLA targets | No formal targets |

### CC3.2 — Identifies and analyzes risks

| Item | Evidence | Common gap |
|------|----------|------------|
| Risk register | Current register with risk owners | Stale; not reviewed |
| Annual risk assessment | Workshop output, signed | Skipped years |
| Risk treatment plans | Per-risk mitigation tracking | Documented but not followed |

### CC3.3 — Considers fraud potential

| Item | Evidence | Common gap |
|------|----------|------------|
| Fraud risk assessment | Subset of risk register or separate | Often missing entirely |

### CC3.4 — Identifies / assesses changes that affect controls

| Item | Evidence | Common gap |
|------|----------|------------|
| Change-impact assessment process | Process doc; sample assessments | Only IT change; not org/business changes |

---

## CC4 — Monitoring Activities

### CC4.1 — Selects / develops / performs ongoing / separate evaluations

| Item | Evidence | Common gap |
|------|----------|------------|
| Internal audit / security review | Audit reports | None performed |
| Penetration testing | Annual pen test report | Skipped |
| Vulnerability scans | Weekly/monthly scan reports + remediation tracking | Scan happens, remediation ad-hoc |

### CC4.2 — Evaluates / communicates deficiencies

| Item | Evidence | Common gap |
|------|----------|------------|
| Audit finding tracking | Findings register with status | Findings never closed |
| Management response to findings | Documented per finding | Verbal-only |

---

## CC5 — Control Activities

### CC5.1 — Selects / develops control activities

| Item | Evidence | Common gap |
|------|----------|------------|
| Control catalog mapping risks to controls | Excel / GRC tool | Risks and controls in separate places |

### CC5.2 — Selects / develops general controls over technology

| Item | Evidence | Common gap |
|------|----------|------------|
| Per-system control inventory | Per app/system | Missing for newer systems |

### CC5.3 — Deploys through policies and procedures

| Item | Evidence | Common gap |
|------|----------|------------|
| Procedures supporting policies | Wiki / handbook | Policy exists; procedure doesn't |

---

## CC6 — Logical and Physical Access

### CC6.1 — Restricts logical access

| Item | Evidence | Common gap |
|------|----------|------------|
| SSO enforced for production | IdP configuration screenshot | Local accounts exist |
| MFA universal for production | IdP MFA enforcement | Exceptions documented but not justified |
| Privileged access management | PAM tool config + audit log | Direct root access common |
| Quarterly access review | Review records signed off | Reviews happen, access not removed |

### CC6.2 — Prior to issuing access

| Item | Evidence | Common gap |
|------|----------|------------|
| Authorization for new access | Ticket / approval per access grant | Granted by chat / verbally |

### CC6.3 — Removes access (terminations)

| Item | Evidence | Common gap |
|------|----------|------------|
| Access removed within X days of termination | HR-IT integration logs | Manual; some delays |
| Annual termination audit | Audit of accounts vs HR records | Orphan accounts found |

### CC6.4 — Restricts physical access

| Item | Evidence | Common gap |
|------|----------|------------|
| Office badge access logs | Building access reports | Reception lets people in without badge |
| Data center access (if applicable) | DC vendor attestation | Self-hosted DC lacks evidence |

### CC6.5 — Disposes of physical access components

| Item | Evidence | Common gap |
|------|----------|------------|
| Badge revocation at termination | Same as access | Same as above |

### CC6.6 — Implements logical access security software

| Item | Evidence | Common gap |
|------|----------|------------|
| Antivirus / EDR deployed | Coverage report | Some endpoints uncovered |
| Disk encryption | MDM compliance | BYOD outside MDM |

### CC6.7 — Restricts transmission

| Item | Evidence | Common gap |
|------|----------|------------|
| TLS 1.2+ enforced | Configuration evidence | TLS 1.0/1.1 still accepted somewhere |
| Encryption at rest verified | DB encryption settings | Encryption configured but not validated |

### CC6.8 — Prevents introduction of unauthorized software

| Item | Evidence | Common gap |
|------|----------|------------|
| Application allowlisting (if applicable) | EDR policy | Open install policy |
| Container image scanning | Scan results | Scans run; failures ignored |

---

## CC7 — System Operations

### CC7.1 — Detects security events

| Item | Evidence | Common gap |
|------|----------|------------|
| SIEM deployment | SIEM config + sample events | Logs collected; not analyzed |
| IDS/IPS or behavioral monitoring | Alert evidence | Alerts disabled due to noise |

### CC7.2 — Monitoring system performance

| Item | Evidence | Common gap |
|------|----------|------------|
| Monitoring dashboards | Screenshots | Dashboards exist; no one watches |
| Alerting thresholds | Alert config | Alerts firing constantly (noise) |

### CC7.3 — Evaluates events

| Item | Evidence | Common gap |
|------|----------|------------|
| Incident response process | IR runbook | Out-of-date |
| Incident triage records | Ticket archive | Incidents never formally closed |

### CC7.4 — Responds to incidents

| Item | Evidence | Common gap |
|------|----------|------------|
| Past-period incident records | Tickets + post-mortems | Post-mortems skipped |
| Customer / regulator notification | Communications evidence | Process untested |

### CC7.5 — Recovers from incidents

| Item | Evidence | Common gap |
|------|----------|------------|
| DR test evidence | Annual DR test report | Never tested |
| Backup restore test | Quarterly restore tests | Backups exist; restore never tested |

---

## CC8 — Change Management

### CC8.1 — Authorizes / designs / develops / implements / approves / tests changes

| Item | Evidence | Common gap |
|------|----------|------------|
| Code review evidence per change | PR records | Some merged without review |
| Production deployment approval | Deploy tickets / change requests | Direct deploys to prod |
| Pre-production testing | CI test logs | Tests run; failures ignored |
| Emergency change process | Process doc + sample emergency tickets | All changes treated as emergency |

---

## CC9 — Risk Mitigation

### CC9.1 — Identifies / analyzes risk

(see CC3)

### CC9.2 — Vendor management

| Item | Evidence | Common gap |
|------|----------|------------|
| Vendor inventory | Current list with risk classification | Missing minor vendors |
| Per-vendor due diligence | SOC 2 / ISO 27001 reports | Reports stale or missing |
| Vendor risk reviews | Annual reviews | Done at onboarding; never repeated |
| DPA / data processing agreements | Per vendor | Standard MSA only; no DPA |

---

## A1 — Availability (if in scope)

### A1.1 — Capacity / availability requirements

| Item | Evidence | Common gap |
|------|----------|------------|
| Capacity planning evidence | Quarterly capacity reviews | Reactive only |
| SLA monitoring + reporting | SLA dashboards | No formal SLA |

### A1.2 — Environmental protections

| Item | Evidence | Common gap |
|------|----------|------------|
| DR plan + test evidence | Plan doc + test report | Plan exists; never tested |
| Backup verification | Restore test results | Not tested |

### A1.3 — Recovers from disruption

| Item | Evidence | Common gap |
|------|----------|------------|
| RTO/RPO documented + tested | Test results | RTO/RPO documented; never validated |

---

## PI1 — Processing Integrity (if in scope)

### PI1.1 — Inputs / processing / outputs

| Item | Evidence | Common gap |
|------|----------|------------|
| Data validation controls | Per system documentation | Manual processes; no controls |
| Error handling | Error logs + handling procedure | Errors logged; never reviewed |
| Reconciliation | Per process evidence | Reconciliation skipped if "looks right" |

---

## C1 — Confidentiality (if in scope)

| Item | Evidence | Common gap |
|------|----------|------------|
| Data classification documented | Classification policy | Not all data classified |
| Encryption per classification | Configuration evidence | Encryption inconsistent |
| Disposal of confidential data | Procedures + evidence | Disposal evidence missing |

---

## P1 — Privacy (if in scope)

### P1.1 — Notice / consent

| Item | Evidence | Common gap |
|------|----------|------------|
| Privacy notice published | Live URL | Out-of-date |
| Consent records | Consent management evidence | Implicit consent only |

### P1.2 — Data subject rights

| Item | Evidence | Common gap |
|------|----------|------------|
| Process documented | Procedure doc | Process undefined |
| Request handling evidence | Sample tickets | Never received any request (or never responded) |

### P1.3 — Data minimization / retention

| Item | Evidence | Common gap |
|------|----------|------------|
| Retention policy | Policy doc | Defined; not enforced |
| Deletion evidence | Sample deletions | Never executed |

---

## Evidence templates

### Standard evidence packet structure

For each control:
```
- Control description: [from your control catalog]
- Control owner: [name]
- Frequency: [continuous / monthly / quarterly / annual]
- Evidence type: [policy / configuration / log / report]
- Evidence file(s): [paths or links]
- Date range covered: [start - end]
- Notes: [any deviations, exceptions, planned remediations]
```

### Walkthrough preparation

For each control owner:
```
- Control(s) owned
- Walkthrough script: how the control works in your words
- Sample evidence to show
- Common auditor questions + your answers
- Documented exceptions / planned changes
```

---

## Punch-list cheat sheet

| If your audit is | Use |
|------------------|-----|
| Type I, mostly ready | 4-week punch-list sprint |
| Type I, gaps | 8-week punch-list sprint |
| Type II observation prep | 12-week sprint (then observation period) |
| Annual recurrence | 4-week sprint + quarterly evidence refresh |
