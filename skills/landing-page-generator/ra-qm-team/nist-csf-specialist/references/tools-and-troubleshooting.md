# Tools and Troubleshooting

Read this when running the scripts: detailed capabilities, input formats, full usage examples, flag reference tables, and a troubleshooting guide for both `csf_maturity_assessor.py` and `csf_control_mapper.py`.

---

## Tools

### csf_maturity_assessor.py

Comprehensive maturity assessment engine for NIST CSF 2.0.

**Capabilities:**
- Scores each function and category on a 1–4 tier scale
- Compares current profile against target profile
- Generates prioritized gap analysis with remediation actions
- Maps gaps to specific CSF subcategories
- Produces JSON or Markdown output

**Usage:**

```bash
# Full maturity assessment with gap analysis
python scripts/csf_maturity_assessor.py \
  --input current_state.json \
  --target-tier 3 \
  --output report.json

# Markdown report for executive presentation
python scripts/csf_maturity_assessor.py \
  --input current_state.json \
  --target-tier 4 \
  --format markdown \
  --output executive_report.md

# Assess specific functions only
python scripts/csf_maturity_assessor.py \
  --input current_state.json \
  --functions GOVERN,IDENTIFY,PROTECT \
  --target-tier 3 \
  --output partial_report.json
```

**Input Format (current_state.json):**

```json
{
  "organization": "Acme Corp",
  "assessment_date": "2026-03-09",
  "assessor": "Security Team",
  "functions": {
    "GOVERN": {
      "GV.OC": {
        "score": 2,
        "evidence": "Mission documented, partial stakeholder mapping",
        "notes": "Legal requirements catalog incomplete"
      },
      "GV.RM": {
        "score": 1,
        "evidence": "No formal risk management strategy",
        "notes": "Risk appetite not defined"
      }
    },
    "IDENTIFY": {
      "ID.AM": {
        "score": 3,
        "evidence": "CMDB maintained, automated discovery",
        "notes": "Shadow IT gap exists"
      }
    }
  }
}
```

### csf_control_mapper.py

Cross-framework control mapping engine.

**Capabilities:**
- Maps NIST CSF 2.0 categories to ISO 27001, SOC 2, HIPAA, PCI-DSS
- Identifies overlapping controls for multi-framework programs
- Generates unified control matrices
- Highlights gaps unique to each framework

**Usage:**

```bash
# Map CSF to ISO 27001
python scripts/csf_control_mapper.py \
  --source-framework nist-csf \
  --target-framework iso27001 \
  --output iso_mapping.json

# Map CSF to all supported frameworks
python scripts/csf_control_mapper.py \
  --source-framework nist-csf \
  --target-framework all \
  --output unified_matrix.json

# Map specific functions only
python scripts/csf_control_mapper.py \
  --source-framework nist-csf \
  --target-framework soc2 \
  --functions GOVERN,PROTECT \
  --output soc2_mapping.json

# Markdown output for documentation
python scripts/csf_control_mapper.py \
  --source-framework nist-csf \
  --target-framework iso27001 \
  --format markdown \
  --output mapping_report.md
```

---

## Tool Reference

### csf_maturity_assessor.py

Assesses cybersecurity maturity across NIST CSF 2.0 functions and generates gap analysis.

| Flag | Required | Description |
|------|----------|-------------|
| `--input` | Yes | Path to current state assessment JSON file with per-category scores (1-4) and evidence |
| `--target-tier` | Yes | Target maturity tier for gap analysis (1-4: Partial, Risk Informed, Repeatable, Adaptive) |
| `--output` | Yes | Path to write the output report file |
| `--format` | No | Output format: `json` (default) or `markdown` |
| `--functions` | No | Comma-separated list of functions to assess (e.g., `GOVERN,IDENTIFY,PROTECT`). Omit for all 6. |

### csf_control_mapper.py

Maps NIST CSF 2.0 categories to controls in other compliance frameworks.

| Flag | Required | Description |
|------|----------|-------------|
| `--source-framework` | Yes | Source framework identifier (use `nist-csf`) |
| `--target-framework` | Yes | Target framework: `iso27001`, `soc2`, `hipaa`, `pci-dss`, or `all` |
| `--output` | Yes | Path to write the mapping output file |
| `--format` | No | Output format: `json` (default) or `markdown` |
| `--functions` | No | Comma-separated list of CSF functions to include (e.g., `GOVERN,PROTECT`). Omit for all. |

---

## Troubleshooting

| Problem | Likely Cause | Resolution |
|---------|-------------|------------|
| Maturity assessor output shows all categories at Tier 1 | Input JSON missing score entries or all scores set to default | Verify the input JSON has a `score` field (1-4) for each assessed category. Run with `--functions` to test a subset first. |
| Control mapper produces empty mappings for a target framework | Framework identifier misspelled or unsupported | Use exact identifiers: `iso27001`, `soc2`, `hipaa`, `pci-dss`, or `all`. Check `--source-framework` is set to `nist-csf`. |
| Gap analysis shows no gaps despite immature program | Target tier set too low (e.g., Tier 1) | Increase `--target-tier` to 3 or 4 to reflect a meaningful target state. Tier 1 is "Partial" and almost any control satisfies it. |
| Markdown output formatting broken | Special characters in evidence or notes fields | Ensure evidence text in input JSON does not contain unescaped pipe characters or markdown syntax. Use plain text descriptions. |
| Assessment does not include GOVERN function | Input JSON uses CSF 1.1 structure without GOVERN | GOVERN is new in CSF 2.0. Update the input JSON to include `GOVERN` with categories GV.OC, GV.RM, GV.RR, GV.PO, GV.OV, and GV.SC. |
| Cross-framework mapping missing subcategory detail | Mapper operates at category level, not subcategory | The mapper provides category-to-control mappings. For subcategory-level detail, consult the NIST CSF 2.0 Informative References online catalog. |
| Report file not created | Output path directory does not exist | Create the output directory before running. The tool does not create intermediate directories automatically. |
