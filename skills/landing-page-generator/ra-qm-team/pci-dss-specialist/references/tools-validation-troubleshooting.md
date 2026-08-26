# Tools, Input Formats, Validation Checkpoints, Troubleshooting, and Success Criteria

Read this for full tool usage detail (capabilities, input JSON formats, CLI flag reference), assessment validation checklists, troubleshooting common tool/scoping issues, and success criteria for a PCI DSS engagement.

---

## Tools

### pci_compliance_checker.py

Comprehensive PCI DSS v4.0 compliance assessment engine.

**Capabilities:**
- Checks against all 12 PCI DSS requirements
- Validates cardholder data environment scope
- Assesses technical controls (encryption, access, logging)
- Scores compliance per requirement (0-100)
- Identifies gaps with remediation priorities
- Generates JSON or Markdown output

**Usage:**

```bash
# Full compliance check
python scripts/pci_compliance_checker.py \
  --input controls.json \
  --output report.json

# Markdown report for stakeholders
python scripts/pci_compliance_checker.py \
  --input controls.json \
  --format markdown \
  --output compliance_report.md

# Check specific requirements only
python scripts/pci_compliance_checker.py \
  --input controls.json \
  --requirements 3,4,7,8 \
  --output data_security_report.json
```

**Input Format (controls.json):**

```json
{
  "organization": "Acme Payments",
  "assessment_date": "2026-03-09",
  "merchant_level": 2,
  "requirements": {
    "1": {
      "network_segmentation": true,
      "firewall_rules_documented": true,
      "waf_deployed": true,
      "inbound_traffic_restricted": true,
      "outbound_traffic_restricted": false,
      "wireless_networks_segmented": true,
      "notes": "Outbound filtering planned for Q2"
    },
    "3": {
      "pan_storage_minimized": true,
      "pan_masked_when_displayed": true,
      "pan_encrypted_at_rest": true,
      "encryption_algorithm": "AES-256",
      "key_management_procedures": true,
      "tokenization_implemented": true,
      "sad_not_stored_after_auth": true,
      "notes": "Tokenization covers 95% of stored PANs"
    }
  }
}
```

### pci_scope_analyzer.py

CDE scoping and SAQ type determination engine.

**Capabilities:**
- Determines appropriate SAQ type based on business model
- Maps cardholder data environment boundaries
- Identifies connected systems and security-impacting systems
- Generates scoping worksheet with system classifications
- Recommends scope reduction strategies

**Usage:**

```bash
# Determine SAQ type and CDE scope
python scripts/pci_scope_analyzer.py \
  --input business_model.json \
  --output scope_report.json

# Markdown scoping worksheet
python scripts/pci_scope_analyzer.py \
  --input business_model.json \
  --format markdown \
  --output scoping_worksheet.md
```

**Input Format (business_model.json):**

```json
{
  "organization": "Acme Payments",
  "business_type": "e-commerce",
  "payment_channels": ["web", "mobile_app"],
  "card_present": false,
  "card_not_present": true,
  "stores_pan": false,
  "processes_pan": false,
  "transmits_pan": false,
  "payment_processor": "Stripe",
  "uses_iframe_redirect": true,
  "uses_p2pe": false,
  "annual_transactions": 500000,
  "card_brands": ["visa", "mastercard", "amex"],
  "systems": [
    {
      "name": "web-frontend",
      "type": "web_server",
      "handles_cardholder_data": false,
      "connected_to_cde": false,
      "security_impacting": true,
      "description": "Customer-facing e-commerce site with iframe payment"
    },
    {
      "name": "payment-api",
      "type": "application_server",
      "handles_cardholder_data": false,
      "connected_to_cde": true,
      "security_impacting": true,
      "description": "API server that communicates with Stripe"
    }
  ]
}
```

---

## Tool Reference

### pci_compliance_checker.py

Assesses compliance against all 12 PCI DSS v4.0 requirements with per-requirement scoring.

| Flag | Required | Description |
|------|----------|-------------|
| `--input` | Yes | Path to controls JSON file with per-requirement control status (boolean values) |
| `--output` | Yes | Path to write the compliance report |
| `--format` | No | Output format: `json` (default) or `markdown` |
| `--requirements` | No | Comma-separated list of requirement numbers to assess (e.g., `3,4,7,8`). Omit for all 12. |

### pci_scope_analyzer.py

Determines SAQ type and maps CDE boundaries based on business model.

| Flag | Required | Description |
|------|----------|-------------|
| `--input` | Yes | Path to business model JSON file with payment channel, data handling, and system inventory details |
| `--output` | Yes | Path to write the scope analysis report |
| `--format` | No | Output format: `json` (default) or `markdown` |

---

## Validation Checkpoints

### Before Starting Assessment
- [ ] Merchant/SP level determined based on transaction volume
- [ ] CDE scope defined with data flow diagrams
- [ ] SAQ type identified (or ROC requirement confirmed)
- [ ] All systems in scope inventoried
- [ ] Payment processor compliance attestation obtained

### During Assessment
- [ ] Each requirement assessed with evidence collected
- [ ] Network segmentation validated
- [ ] Encryption verified (at rest and in transit)
- [ ] Access controls tested (RBAC, MFA, least privilege)
- [ ] Logging and monitoring validated (SIEM, log retention)
- [ ] Vulnerability scans and pen test results reviewed

### After Assessment
- [ ] SAQ/ROC completed with all sections addressed
- [ ] AOC signed by authorized officer
- [ ] Quarterly ASV scans scheduled
- [ ] Remediation plan for any findings
- [ ] Next assessment date scheduled
- [ ] Scope re-validation trigger process documented

### Ongoing Compliance
- [ ] Quarterly internal vulnerability scans
- [ ] Quarterly external ASV scans
- [ ] Annual penetration testing
- [ ] Annual security awareness training
- [ ] Annual policy review
- [ ] Annual scope re-validation
- [ ] Semi-annual firewall rule review
- [ ] Semi-annual access review
- [ ] Daily log review (automated)

---

## Troubleshooting

| Problem | Likely Cause | Resolution |
|---------|-------------|------------|
| Compliance checker reports 0% for a requirement | Controls JSON missing the requirement section entirely | Ensure the `requirements` object in the input JSON includes entries for all 12 requirements (keys `"1"` through `"12"`). Use a sample template as a starting point. |
| Scope analyzer returns wrong SAQ type | Business model flags incorrectly set (e.g., `stores_pan` true when using tokenization) | Review all boolean flags: `stores_pan`, `processes_pan`, `transmits_pan`, `uses_iframe_redirect`, `uses_p2pe`. Tokenized PANs are not considered stored CHD. |
| Gap report shows requirements as non-applicable | The `--requirements` flag is filtering scope | Remove the `--requirements` flag to assess all 12 requirements. When specified, only the listed requirements are evaluated. |
| Encryption controls flagged despite AES-256 | Disk-level encryption used instead of file/column-level | PCI DSS v4.0 no longer accepts disk-level encryption as encryption at rest (except removable media). Implement file-level, column-level, or application-layer encryption. |
| MFA requirement flagged even though MFA is deployed | MFA not covering all CDE access paths | PCI DSS v4.0 requires MFA for all access into the CDE, not just remote access. Verify MFA covers console, VPN, API, and administrative access. |
| Payment page script controls failing | Requirements 6.4.3 and 11.6.1 not addressed | Inventory all scripts on payment pages, document authorization and integrity for each, and deploy tamper-detection mechanisms. These became mandatory March 31, 2025. |
| Third-party service provider compliance gaps | TPSP AOC not obtained or expired | Obtain current Attestation of Compliance (AOC) from every third-party service provider handling cardholder data. Verify scope coverage matches your use case. |

---

## Success Criteria

- CDE scope clearly defined with network diagrams, data flow documentation, and system inventory covering all in-scope components
- SAQ type correctly determined and validated against actual business model, payment channels, and data handling practices
- Compliance score of 80%+ across all 12 requirements on initial assessment, trending to 95%+ before formal audit
- All future-dated v4.0 requirements (mandatory since March 31, 2025) fully implemented, including payment page script controls (6.4.3, 11.6.1), targeted risk analysis, and enhanced MFA
- Quarterly ASV scans passing with no exploitable vulnerabilities, and annual penetration testing completed with findings remediated
- Third-party service providers validated with current AOCs covering the services used, and TPSP monitoring procedures documented
- Scope reduction strategies implemented (tokenization, P2PE, network segmentation) reducing the number of in-scope systems by 30%+
