# Audit Workflows, Scoring & Success Criteria

Step-by-step audit workflows, pre/post-audit validation checklists, the severity-weighted scoring methodology, and success criteria. Read this when planning or executing an audit engagement and interpreting scores.

## Workflows

### Workflow 1: Full Infrastructure Audit

```
1. Prepare inventory → Document all cloud accounts, domains, endpoints, services
2. Run infra_audit_runner.py → Generate findings across all 11 domains
3. Triage findings → Prioritize Critical > High > Medium > Low
4. Map to frameworks → Identify which framework requirements are met/unmet
5. Create remediation plan → Assign owners, set deadlines by severity SLA
6. Execute remediation → Fix Critical within 24h, High within 72h
7. Re-audit → Verify fixes, update compliance evidence
8. Generate report → Executive summary + detailed findings + evidence
```

**Severity SLAs:**
| Severity | Remediation Deadline | Re-audit Deadline |
|----------|---------------------|-------------------|
| Critical | 24 hours | 48 hours |
| High | 72 hours | 7 days |
| Medium | 7 days | 14 days |
| Low | 30 days | 45 days |
| Info | No deadline | Next audit cycle |

### Workflow 2: DNS Security Assessment

```
1. Enumerate domains → Primary + all subdomains
2. Run dns_security_checker.py → Check SPF, DKIM, DMARC, DNSSEC, CAA, MTA-STS
3. Validate email chain → SPF → DKIM → DMARC alignment
4. Check domain security → Registrar lock, 2FA, WHOIS, expiration
5. Subdomain audit → Check for dangling CNAME records (takeover risk)
6. Generate DNS report → Findings + remediation DNS records
```

### Workflow 3: Access Control Review

```
1. Export IdP configuration → Users, groups, roles, policies
2. Run access_control_auditor.py → Check MFA, SSO, RBAC, PAM, service accounts
3. Verify MFA coverage → Must be 100%, flag any exceptions
4. Review privileged access → Who has admin? Is JIT in place?
5. Check service accounts → Rotation, ownership, permissions
6. Access recertification → Verify all access is current and justified
7. Generate access report → Gaps + remediation steps
```

### Workflow 4: Continuous Compliance Monitoring

```
1. Schedule automated scans → Weekly infra audit, daily DNS check
2. Track compliance score trends → Score per domain over time
3. Alert on regressions → Score drop or new Critical finding triggers alert
4. Quarterly full audit → Manual review + automated scan
5. Annual certification preparation → Compile evidence for auditors
```


---

## Validation Checkpoints

### Pre-Audit Validation
- [ ] Infrastructure inventory is complete and current
- [ ] All cloud accounts identified and accessible
- [ ] Domain list verified (primary + all active subdomains)
- [ ] Endpoint MDM reports available
- [ ] IdP configuration export available
- [ ] Previous audit findings reviewed

### Post-Audit Validation
- [ ] All 11 domains audited with no skipped checks
- [ ] Every finding has severity, framework mapping, and remediation
- [ ] Critical and High findings have assigned owners
- [ ] Compliance score calculated per domain and overall
- [ ] Executive summary prepared
- [ ] Evidence package compiled for applicable frameworks
- [ ] Remediation deadlines set per severity SLA


---

## Scoring Methodology

Each audit domain is scored 0-100 based on the controls assessed:

**Score Calculation:**
```
Domain Score = (Passed Controls * Weight) / (Total Controls * Weight) * 100

Weights by severity:
  Critical = 10
  High = 5
  Medium = 2
  Low = 1
  Info = 0 (informational, not scored)
```

**Overall Score:**
```
Overall Score = Weighted Average of Domain Scores

Domain Weights:
  Cloud Infrastructure: 15%
  Access Control: 15%
  Network Security: 12%
  Secrets Management: 10%
  Logging/Monitoring: 10%
  CI/CD Pipeline: 8%
  Container/K8s: 8%
  Endpoint Security: 7%
  TLS/SSL: 5%
  DNS Security: 5%
  Physical Security: 5%
```

**Score Interpretation:**
| Score Range | Rating | Meaning |
|-------------|--------|---------|
| 90-100 | Excellent | Audit-ready, minimal findings |
| 80-89 | Good | Minor gaps, mostly compliant |
| 70-79 | Fair | Notable gaps, remediation needed before audit |
| 60-69 | Poor | Significant compliance gaps |
| Below 60 | Critical | Major overhaul required, not audit-ready |

---

## Success Criteria

- **Overall infrastructure score of 80+ (Good or Excellent)** -- indicating audit-readiness with only minor gaps across all 11 domains
- **Zero Critical findings across all domains** -- all Critical-severity controls (root MFA, no wildcard IAM policies, encryption at rest, hardware key admin MFA) passing
- **Framework-specific compliance above 85%** -- for each targeted compliance framework (SOC 2, ISO 27001, PCI-DSS, etc.), the mapped controls show 85%+ pass rate
- **DNS security fully configured** -- SPF, DKIM, and DMARC (policy=reject) records validated, DNSSEC enabled, CAA records set, and MTA-STS deployed
- **Access control audit passes all Critical and High controls** -- centralized IdP deployed, SSO integrated for all applications, hardware security keys enforced for admin accounts, PAM implemented, and RBAC documented
- **Secrets management score above 90%** -- dedicated secrets vault deployed, automated rotation configured, no secrets in source code (git scanning enabled), and HSM for cryptographic operations
- **Evidence artifacts generated for audit** -- JSON or markdown reports suitable for auditor review, with per-control pass/fail status and framework mapping

