# Operations, Troubleshooting & Tool Reference

Troubleshooting table, success criteria, and the full `qms_audit_checklist.py` flag reference. Read this when diagnosing tool output, validating QMS completeness, or running the audit checklist generator.

---

## Troubleshooting

| Problem | Likely Cause | Resolution |
|---------|-------------|------------|
| Audit checklist generator returns empty output | Clause number not recognized | Use exact clause numbers from ISO 13485:2016 (e.g., `7.3`, `4.2.3`, `8.5.2`). Run with `--interactive` to see all available clauses. |
| System audit checklist is very large | `--audit-type system` includes all clauses | For targeted audits, use `--clause` or `--process` flags to generate focused checklists. System audits intentionally cover the full standard. |
| Gap analysis matrix shows all clauses as "Major" gaps | Assessment conducted against a greenfield organization | Prioritize gaps by regulatory criticality and product safety impact. Address Clauses 4.2, 7.3, 8.2.4, 8.3, and 8.5 first as these require mandatory documented procedures. |
| QMSR transition mapping unclear | QSR sections not aligned to ISO 13485 clauses | The QMSR (effective Feb 2, 2026) incorporates ISO 13485 by reference. Map QSR 21 CFR 820 sub-parts to ISO 13485 clauses using the QMSR Gap Analysis Checklist in this skill. |
| Supplier qualification score borderline (60-80) | Supplier meets some criteria but has gaps | Issue conditional approval with documented improvement requirements and a defined reassessment date. Increase monitoring frequency until the supplier exceeds the 80-point threshold. |
| Process validation protocol incomplete | IQ/OQ/PQ phases not clearly separated | Each qualification phase must have distinct objectives, acceptance criteria, and documented results. Use the Validation Documentation Requirements table as a template for protocol structure. |
| Design control audit questions not applicable | Organization does not perform design activities | ISO 13485 permits exclusion of Clause 7.3 if the organization does not design products. Document the exclusion justification in the Quality Manual per Clause 4.2.2. |

---

## Success Criteria

- QMS gap analysis completed against all ISO 13485:2016 clauses with documented current state, gap severity, priority, and remediation actions
- All 6 mandatory documented procedures established, trained, and effective (document control, record control, internal audit, NC product, corrective action, preventive action)
- Quality Manual approved with justified clause exclusions, process interactions documented, and scope clearly defined
- QMSR transition completed: all QSR SOPs mapped to ISO 13485 clauses, FDA-retained requirements addressed, internal audit checklist updated for combined ISO 13485 + FDA requirements
- Supplier qualification program operational with category-based assessment (A/B/C), documented scoring, and approved supplier list maintained
- Process validation completed for all special processes (IQ/OQ/PQ documented with approved protocols and reports)
- Certification audit passed with zero Major nonconformities and a plan to address any Minor findings within 60 days

---

## Tool Reference

### qms_audit_checklist.py

Generates ISO 13485:2016 audit checklists by clause, process, or full system audit.

| Flag | Required | Description |
|------|----------|-------------|
| `--clause` | No | ISO 13485 clause number to generate a clause-specific checklist (e.g., `7.3`, `4.2.3`, `8.5.2`) |
| `--process` | No | Process name for a process-based checklist (e.g., `design-control`, `purchasing`, `capa`) |
| `--audit-type` | No | Audit type: `system` for a full-system checklist covering all clauses |
| `--output` | No | Output format: `json` for structured output, omit for human-readable text |
| `--interactive` | No | Launch interactive mode for guided clause/process selection |

**Audit Checklist Generator Features:**
- Generate clause-specific checklists (e.g., `--clause 7.3`)
- Generate process-based checklists (e.g., `--process design-control`)
- Full system audit checklist (`--audit-type system`)
- Text or JSON output formats
- Interactive mode for guided selection
