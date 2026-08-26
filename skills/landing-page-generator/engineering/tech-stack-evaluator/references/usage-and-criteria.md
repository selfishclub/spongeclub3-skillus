# Usage, Input Formats & Criteria

Read this when invoking the evaluator: example prompts, accepted input formats, analysis depth tiers, confidence scoring, troubleshooting, and success criteria.

## Quick Start

### Compare Two Technologies

```
Compare React vs Vue for a SaaS dashboard.
Priorities: developer productivity (40%), ecosystem (30%), performance (30%).
```

### Calculate TCO

```
Calculate 5-year TCO for Next.js on Vercel.
Team: 8 developers. Hosting: $2500/month. Growth: 40%/year.
```

### Assess Migration

```
Evaluate migrating from Angular.js to React.
Codebase: 50,000 lines, 200 components. Team: 6 developers.
```

## Input Formats

The evaluator accepts three input formats:

**Text** - Natural language queries
```
Compare PostgreSQL vs MongoDB for our e-commerce platform.
```

**YAML** - Structured input for automation
```yaml
comparison:
  technologies: ["React", "Vue"]
  use_case: "SaaS dashboard"
  weights:
    ecosystem: 30
    performance: 25
    developer_experience: 45
```

**JSON** - Programmatic integration
```json
{
  "technologies": ["React", "Vue"],
  "use_case": "SaaS dashboard"
}
```

## Analysis Types

### Quick Comparison (200-300 tokens)
- Weighted scores and recommendation
- Top 3 decision factors
- Confidence level

### Standard Analysis (500-800 tokens)
- Comparison matrix
- TCO overview
- Security summary

### Full Report (1200-1500 tokens)
- All metrics and calculations
- Migration analysis
- Detailed recommendations

## Confidence Levels

| Level | Score | Interpretation |
|-------|-------|----------------|
| High | 80-100% | Clear winner, strong data |
| Medium | 50-79% | Trade-offs present, moderate uncertainty |
| Low | < 50% | Close call, limited data |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Weighted scores all return 50.0 | Technology data dictionaries missing `score` keys under each category | Ensure each category dict contains a `score` key on a 0-100 scale (e.g., `{"performance": {"score": 85}}`) |
| TCO projections look unrealistically low | Default cost parameters used when `operational_costs` or `initial_costs` are empty | Populate `monthly_hosting`, `annual_licensing`, `developer_hourly_rate`, and `maintenance_hours_per_dev_monthly` with real figures |
| Ecosystem health score stuck at 50 for npm | `npm_data` dict is empty or not provided | Pass npm metrics (`weekly_downloads`, `version`, `dependencies_count`, `days_since_last_publish`); 50 is the neutral fallback when npm data is absent |
| Security compliance returns "Unknown standard" | Unsupported standard name passed to `assess_compliance()` | Use one of the supported keys: `GDPR`, `SOC2`, `HIPAA`, `PCI_DSS` (case-sensitive) |
| Migration complexity always shows moderate | `architecture_change_level` defaults to `moderate` when not specified | Set `architecture_change_level` explicitly to `minimal`, `moderate`, `significant`, or `complete` in `codebase_stats` |
| Report renders ASCII tables instead of markdown | `ReportGenerator` auto-detects CLI context when stdout is a TTY | Pass `output_context='desktop'` to force rich markdown output |
| Format detector misclassifies YAML as text | Fewer than 50% of lines match YAML key-value patterns | Ensure input uses standard YAML syntax with `key: value` pairs and proper indentation |

## Success Criteria

- **TCO variance under 15%**: Calculated TCO deviates less than 15% from actual costs when validated against real-world spending data over the projection period.
- **Security score above 80/100**: Technologies recommended for production use achieve a minimum overall security score of 80, corresponding to grade B or higher.
- **Ecosystem health score above 65/100**: Recommended technologies demonstrate viable long-term ecosystem health with a risk level no worse than "Low-Medium."
- **Migration effort estimate within 20%**: Person-hours and timeline estimates land within 20% of actual migration effort when measured post-completion.
- **Comparison confidence above 70%**: Final technology recommendations carry a confidence score of 70% or higher, indicating a meaningful score gap between top candidates.
- **Compliance readiness at "Mostly Ready" or above**: Technologies targeting regulated environments achieve at least 70% feature coverage against required compliance standards (GDPR, SOC2, HIPAA, PCI-DSS).
- **Report generation under 5 seconds**: All report types (executive summary, full report) render within 5 seconds for evaluations comparing up to 5 technologies.
