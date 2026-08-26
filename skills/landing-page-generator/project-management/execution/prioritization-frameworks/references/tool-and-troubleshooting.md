# Tool Reference, Troubleshooting & Success Criteria

Read this when running `prioritization_scorer.py` (input schemas, flags), diagnosing a scoring problem, or checking whether a prioritization exercise met its bar.

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| RICE scores dominated by high-reach items regardless of impact | Reach values vary by orders of magnitude, drowning out other factors | Normalize reach to a consistent time window (e.g., users per quarter); consider log-scale for extreme ranges |
| ICE scores feel arbitrary and inconsistent across raters | No calibration on 1-10 scale definitions; different people use different anchors | Define what 1, 5, and 10 mean for each dimension; score independently first, then discuss outliers |
| MoSCoW results in 80% Must-Haves | Team reluctant to deprioritize anything, or no effort constraint applied | Enforce the rule: Must-Haves should be no more than 60% of total effort; make the constraint visible |
| Opportunity Score returns 0 for satisfied needs | Satisfaction scored at 1.0 (fully satisfied), zeroing out the score | Verify satisfaction is on 0-1 scale; values above 1 are auto-converted from 0-10 scale |
| Weighted Decision Matrix produces tied scores | Criteria weights are too evenly distributed, or scoring lacks variance | Increase weight differentiation; force-rank criteria by importance; use the full 1-10 scoring range |
| Framework selection is itself a bottleneck | Team spends time debating which framework to use instead of scoring | Use the Decision Tree in this skill; default to RICE for 15+ items with data, ICE for quick sorts under 15 items |
| Stakeholders disagree with prioritization results | Framework selected does not match stakeholder values, or inputs not transparent | Use Weighted Decision Matrix when multiple stakeholder groups are involved; agree on criteria and weights before scoring |

## Success Criteria

- Prioritization framework selected using the Decision Tree, not by habit or preference
- All items scored with consistent definitions for each dimension (documented before scoring begins)
- Results reviewed and discussed as a team, not treated as a mechanical ranking
- Top-priority items have clear next steps (assigned to sprints, PRDs, or experiments)
- Prioritization is repeated at least quarterly, or when significant new information arrives
- The two-step approach is followed: prioritize problems first (Opportunity Score), then prioritize solutions (RICE/ICE)
- MoSCoW Must-Haves never exceed 60% of total effort for a release

## Tool Reference

### prioritization_scorer.py

Scores and ranks items using 5 supported prioritization frameworks. Outputs sorted results with scores, formulas, and category breakdowns.

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--input` | string | (required, mutually exclusive with --demo) | Path to JSON file containing items to score |
| `--demo` | flag | off | Run scoring on built-in demo data for the selected framework |
| `--framework` | choice | (required) | Framework to use: `rice`, `ice`, `opportunity`, `moscow`, `weighted` |
| `--format` | choice | `text` | Output format: `text` or `json` |

**Input JSON schema by framework:**

- **RICE:** `{"items": [{"name": "...", "reach": N, "impact": N, "confidence": N, "effort": N}]}`
- **ICE:** `{"items": [{"name": "...", "impact": N, "confidence": N, "ease": N}]}`
- **Opportunity:** `{"items": [{"name": "...", "importance": N, "satisfaction": N}]}`
- **MoSCoW:** `{"items": [{"name": "...", "category": "must|should|could|wont", "effort": N}]}`
- **Weighted:** `{"items": [{"name": "...", "scores": {"criterion": N}}], "criteria": [{"name": "...", "weight": N}]}`
