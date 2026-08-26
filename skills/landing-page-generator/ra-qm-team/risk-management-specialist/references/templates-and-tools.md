# Risk Assessment Templates, Tool Reference, Troubleshooting & Success Criteria

Copy-ready worksheet and report templates, the full `risk_matrix_calculator.py` flag reference,
the troubleshooting table, and the success criteria for an ISO 14971 program. Read this when
documenting a risk assessment, running the calculator, diagnosing tool issues, or auditing
whether the risk management program is complete.

## Risk Assessment Templates

### Hazard Analysis Worksheet

```
HAZARD ANALYSIS WORKSHEET

Product: [Device Name]
Document: HA-[Product]-[Rev]
Analyst: [Name]
Date: [Date]

| ID | Hazard | Hazardous Situation | Harm | P | S | Initial Risk | Control | Residual P | Residual S | Final Risk |
|----|--------|---------------------|------|---|---|--------------|---------|------------|------------|------------|
| H-001 | [Hazard] | [Situation] | [Harm] | [1-5] | [1-5] | [Level] | [Control ref] | [1-5] | [1-5] | [Level] |
```

### FMEA Worksheet

```
FMEA WORKSHEET

Product: [Device Name]
Subsystem: [Subsystem]
Analyst: [Name]
Date: [Date]

| ID | Item | Function | Failure Mode | Effect | S | Cause | O | Control | D | RPN | Action |
|----|------|----------|--------------|--------|---|-------|---|---------|---|-----|--------|
| FM-001 | [Item] | [Function] | [Mode] | [Effect] | [1-10] | [Cause] | [1-10] | [Detection] | [1-10] | [S×O×D] | [Action] |

RPN Action Thresholds:
>200: Critical - Immediate action
100-200: High - Action plan required
50-100: Medium - Consider action
<50: Low - Monitor
```

### Risk Management Report Summary

```
RISK MANAGEMENT REPORT

Product: [Device Name]
Date: [Date]
Revision: [X.X]

SUMMARY:
- Total hazards identified: [N]
- Risk controls implemented: [N]
- Residual risks: [N] Low, [N] Medium, [N] High
- Overall conclusion: [Acceptable / Not Acceptable]

RISK DISTRIBUTION:
| Risk Level | Before Control | After Control |
|------------|----------------|---------------|
| Unacceptable | [N] | 0 |
| High | [N] | [N] |
| Medium | [N] | [N] |
| Low | [N] | [N] |

CONTROLS IMPLEMENTED:
- Inherent safety: [N]
- Protective measures: [N]
- Information for safety: [N]

OVERALL RESIDUAL RISK: [Acceptable / ALARP Demonstrated]
BENEFIT-RISK CONCLUSION: [If applicable]

APPROVAL:
Risk Management Lead: _____________ Date: _______
Quality Assurance: _____________ Date: _______
```

---

## Tools and References

### Scripts

| Tool | Purpose | Usage |
|------|---------|-------|
| [risk_matrix_calculator.py](../scripts/risk_matrix_calculator.py) | Calculate risk levels and FMEA RPN | `python risk_matrix_calculator.py --help` |

**Risk Matrix Calculator Features:**
- ISO 14971 5x5 risk matrix calculation
- FMEA RPN (Risk Priority Number) calculation
- Interactive mode for guided assessment
- Display risk criteria definitions
- JSON output for integration

### References

| Document | Content |
|----------|---------|
| [iso14971-implementation-guide.md](iso14971-implementation-guide.md) | Complete ISO 14971:2019 implementation with templates |
| [risk-analysis-methods.md](risk-analysis-methods.md) | FMEA, FTA, HAZOP, Use Error Analysis methods |

### risk_matrix_calculator.py

Calculates ISO 14971 risk levels and FMEA Risk Priority Numbers.

| Flag | Required | Description |
|------|----------|-------------|
| `--probability` | Yes (for ISO 14971 mode) | Probability level (1-5): 1=Improbable, 2=Remote, 3=Occasional, 4=Probable, 5=Frequent |
| `--severity` | Yes (for both modes) | Severity level: 1-5 for ISO 14971 mode, 1-10 for FMEA mode |
| `--fmea` | No | Switch to FMEA RPN calculation mode (requires `--severity`, `--occurrence`, `--detection`) |
| `--occurrence` | Yes (for FMEA mode) | Occurrence rating (1-10) for FMEA RPN calculation |
| `--detection` | Yes (for FMEA mode) | Detection rating (1-10) for FMEA RPN calculation |
| `--interactive` | No | Launch interactive mode for guided risk assessment |
| `--list-criteria` | No | Display probability, severity, and risk level criteria definitions |

---

## Troubleshooting

| Problem | Likely Cause | Resolution |
|---------|-------------|------------|
| Risk matrix calculator returns "Invalid probability" | Probability value outside 1-5 range | Use integers 1-5 for probability (`--probability`) and 1-5 for severity (`--severity`). Run `--list-criteria` to display the full scale definitions. |
| FMEA RPN calculation produces unexpected results | Severity, occurrence, or detection values outside 1-10 range | FMEA mode (`--fmea`) requires `--severity`, `--occurrence`, and `--detection` values each in the 1-10 range. Values outside this range produce unreliable RPNs. |
| Risk level shows "Medium" but stakeholders expect "High" | Risk acceptability criteria differ from the tool's default 5x5 matrix | The default matrix follows common ISO 14971 practice. If your organization uses a custom risk matrix, adjust the risk acceptability criteria in your Risk Management Plan and document deviations. |
| Post-production risk data not triggering file updates | Review triggers not defined or too narrow | Define explicit triggers: any serious incident (immediate), new hazard identification (30 days), trend increase (60 days), design change (before implementation), and standards update (per transition period). |
| AI-specific hazards not captured in FMEA | Standard FMEA template lacks AI failure modes | Extend the FMEA with AI-specific failure modes: model bias, data drift, concept drift, adversarial inputs, automation complacency. Use the AI Risk Analysis Methodology section as a guide. |
| Cybersecurity threats not integrated into risk assessment | Threat modeling methodology not aligned to ISO 14971 | Use STRIDE methodology for threat identification, then map each threat to an ISO 14971 harm pathway. Reference IEC 81001-5-1 for health software cybersecurity integration. |
| Benefit-risk analysis requested but no template available | The tool calculates risk levels but does not generate benefit-risk documents | The benefit-risk analysis is a narrative document per ISO 14971 Clause 8. Use the risk matrix outputs as quantitative inputs, then document clinical benefits vs. residual risks in the Risk Management Report. |

---

## Success Criteria

- Risk Management Plan approved with defined scope, risk acceptability matrix, RACI chart, and post-production monitoring plan before design input phase
- 100% of ISO 14971 hazard categories analyzed (electrical, mechanical, thermal, radiation, biological, chemical, software, use error, environmental) with documented rationale for each
- All identified risks evaluated against the 5x5 acceptability matrix with no uncontrolled "Unacceptable" residual risks remaining
- Risk controls implemented following the priority hierarchy (inherent safety first, then protective measures, then information for safety) with verification records for every control
- Overall residual risk evaluated as acceptable or ALARP demonstrated, with benefit-risk analysis completed for any residual risks remaining in High territory
- Post-production risk monitoring operational with defined information sources, review triggers, and a documented process for updating the Risk Management File
- For AI/ML devices: AI-specific risk categories (bias, drift, adversarial inputs) assessed per BS/AAMI 34971:2023 or equivalent, with continuous performance monitoring thresholds defined
