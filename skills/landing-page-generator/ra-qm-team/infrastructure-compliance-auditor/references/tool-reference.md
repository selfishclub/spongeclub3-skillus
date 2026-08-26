# Tool Reference & Troubleshooting

CLI flag reference for the three audit scripts and a troubleshooting table for common audit issues. Read this when running the tools or diagnosing unexpected audit output.

## Tool Reference

### infra_audit_runner.py

Comprehensive infrastructure audit across 11 domains with compliance framework mapping.

| Flag | Required | Description |
|------|----------|-------------|
| `--config <file>` | Yes (unless `--generate-template`) | Path to JSON file describing infrastructure configuration |
| `--generate-template` | No | Generate blank infrastructure configuration template |
| `--frameworks <list>` | No | Comma-separated framework filter (e.g., `soc2,iso27001,hipaa`); uses identifiers: `soc2`, `iso27001`, `hipaa`, `gdpr`, `pci_dss`, `nis2`, `dora`, `nist_csf`, `fedramp`, `ccpa` |
| `--format <fmt>` | No | Output format: `json` (default) or `markdown` |
| `--output <file>` | No | Export report to specified file path |

**Output:** Per-domain scores (0-100), overall weighted score, per-control pass/fail/unknown status, framework-mapped findings with severity, and remediation recommendations.

### dns_security_checker.py

DNS-specific security audit validating email authentication, DNSSEC, certificate authority authorization, and subdomain takeover risk.

| Flag | Required | Description |
|------|----------|-------------|
| `--domain <domain>` | Yes | Domain name to audit (e.g., `example.com`) |
| `--output <file>` | No | Export report to specified file path |
| `--format <fmt>` | No | Output format: `json` (default) or `markdown` |
| `--subdomains <list>` | No | Comma-separated subdomains to check for takeover risk (e.g., `sub1,sub2,sub3`) |
| `--dkim-selectors <list>` | No | Comma-separated DKIM selectors to validate (e.g., `google,selector1`) |

**Checks:** SPF record syntax and lookup count, DKIM record presence and key strength, DMARC policy and reporting configuration, DNSSEC validation, CAA record authorization, MTA-STS policy, and subdomain takeover risk assessment.

### access_control_auditor.py

Access control audit covering identity, authentication, authorization, and privileged access management.

| Flag | Required | Description |
|------|----------|-------------|
| `--config <file>` | Yes (unless `--generate-template`) | Path to JSON file describing access control configuration |
| `--generate-template` | No | Generate blank access control configuration template |
| `--format <fmt>` | No | Output format: `json` (default) or `markdown` |
| `--output <file>` | No | Export report to specified file path |

**Audit Categories:** Identity Provider (IdP) configuration, SSO/SCIM provisioning, MFA enforcement, hardware security key (FIDO2/YubiKey) deployment, Privileged Access Management (PAM), RBAC, service account governance, SSH key management, API key management, and Zero Trust architecture.

---

## Troubleshooting

| Problem | Possible Cause | Resolution |
|---------|---------------|------------|
| Infra audit runner returns mostly "UNKNOWN" statuses | Config JSON missing required keys or key paths do not match expected `check_key` format | Generate a fresh template with `--generate-template` and verify all key paths match the control registry (e.g., `aws.iam.root_mfa_enabled`); fill in actual values from your infrastructure |
| DNS security checker cannot resolve records | `dig` command not available on the system or DNS resolver blocking queries | Install `dnsutils` (Linux) or `bind` (macOS via Homebrew); alternatively the tool falls back to socket-based lookups but with reduced functionality; check network connectivity to DNS resolvers |
| Access control auditor shows Critical findings for MFA | SMS/TOTP MFA deployed instead of hardware security keys for admin accounts | Migrate admin accounts to FIDO2/WebAuthn hardware keys (YubiKey 5, Titan); disable SMS MFA for privileged access; use `--generate-template` to review all MFA-related control expectations |
| Framework-filtered report shows zero controls for a specific framework | Framework label mismatch in `--frameworks` flag (e.g., `pci-dss` instead of `pci_dss`) | Use exact framework identifiers: `soc2`, `iso27001`, `hipaa`, `gdpr`, `pci_dss`, `nis2`, `dora`, `nist_csf`, `fedramp`, `ccpa` |
| Overall score low despite strong cloud security | Domain weights distribute score across all 11 domains; weak areas (e.g., physical security, DNS) drag down the average | Review per-domain scores to identify weakest areas; prioritize remediation in highest-weighted domains (Cloud Infrastructure 15%, Access Control 15%, Network Security 12%) |
| Container security audit fails with all controls non-compliant | Organization does not use containers but config JSON contains default/empty container section | Set container controls to `N/A` or remove the container section from the config; tool scores only applicable controls |
| Audit report too large for stakeholder review | Full 250+ control audit generates extensive output | Use `--frameworks` flag to filter to relevant frameworks; use `--format markdown` for human-readable summary; generate separate reports per domain for team-specific remediation |

