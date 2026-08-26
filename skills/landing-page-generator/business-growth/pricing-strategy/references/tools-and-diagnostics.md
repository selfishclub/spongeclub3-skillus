# Output Artifacts, Tools, Troubleshooting & Success Criteria

Read this when producing deliverables, running the Python scripts, debugging a
pricing problem, checking success criteria, or avoiding common anti-patterns.

## Output Artifacts

| Artifact | Format | Description |
|----------|--------|-------------|
| Pricing Strategy Document | Structured analysis | Value metric, packaging, price points with rationale |
| Tier Architecture | Feature allocation table | What goes in each tier with justification |
| Pricing Page Specification | Layout + copy | Above-fold design, feature table, FAQ, toggle behavior |
| Price Increase Plan | Timeline + communications | Strategy selection, rollout schedule, email templates |
| Competitive Pricing Analysis | Comparison table + position map | Market pricing landscape with positioning recommendation |
| Van Westendorp Survey | Question set + interpretation guide | Ready-to-deploy pricing research |
| Pricing Health Scorecard | Signal + diagnosis table | Current pricing health assessment with action items |

---

## Tool Reference

### 1. pricing_model_analyzer.py

Analyzes a SaaS pricing model against best practices. Evaluates value metric alignment, tier architecture, feature allocation, and identifies pricing anti-patterns. Outputs a health scorecard with prioritized recommendations.

```bash
python scripts/pricing_model_analyzer.py pricing.json --format text
python scripts/pricing_model_analyzer.py pricing.json --format json
```

| Flag | Type | Description |
|------|------|-------------|
| `pricing.json` | positional | Path to JSON file with pricing model configuration |
| `--format` | optional | Output format: `text` (default) or `json` |

### 2. price_sensitivity_calculator.py

Implements the Van Westendorp Price Sensitivity Meter. Takes survey responses (too cheap, bargain, expensive, too expensive) and calculates the optimal price point, acceptable price range, and indifference price point.

```bash
python scripts/price_sensitivity_calculator.py survey.json --format text
python scripts/price_sensitivity_calculator.py survey.json --format json
```

| Flag | Type | Description |
|------|------|-------------|
| `survey.json` | positional | Path to JSON file with Van Westendorp survey responses |
| `--format` | optional | Output format: `text` (default) or `json` |

### 3. price_increase_modeler.py

Models the revenue impact of price increases at various retention scenarios. Takes current customer base, pricing, and proposed increase, then projects revenue impact at 80%, 90%, and 100% retention with break-even analysis.

```bash
python scripts/price_increase_modeler.py increase.json --format text
python scripts/price_increase_modeler.py increase.json --format json
```

| Flag | Type | Description |
|------|------|-------------|
| `increase.json` | positional | Path to JSON file with price increase scenario data |
| `--format` | optional | Output format: `text` (default) or `json` |

---

## Troubleshooting

| Problem | Likely Cause | Resolution |
|---------|-------------|------------|
| Trial-to-paid conversion above 40% | Product is likely underpriced -- customers convert too easily because price is well below perceived value | Test a 20-30% price increase on new customers first; monitor conversion rate and revenue per user |
| All customers concentrate on middle tier | No compelling reason to upgrade to top tier; enterprise features missing or unclear | Add SSO, audit logs, dedicated support, SLA, and custom integrations to top tier; ensure 3-5x price jump from middle |
| Frequent discount requests from prospects | Price may exceed perceived value, or value proposition is poorly communicated | Audit sales collateral for ROI messaging; consider adding a lighter entry tier rather than discounting |
| Price unchanged for 2+ years | Inflation alone justifies 10-15% increase; likely leaving significant revenue on the table | Plan a structured price increase using the execution timeline; start with new customers only to test |
| High involuntary churn on usage-based pricing | Unpredictable bills cause customers to cancel; usage spikes create bill shock | Add usage bands, committed minimums, or spending caps with alerts at 80% threshold |
| Customers game the value metric | Per-seat pricing with shared logins, or usage metrics that can be artificially reduced | Switch to a harder-to-game metric; add audit capabilities; consider hybrid model |
| Pricing page has low conversion but product is strong | Pricing page design issues (too many tiers, unclear differentiation, hidden annual toggle) | Simplify to 3 tiers, highlight recommended plan, show annual savings prominently, add FAQ |

---

## Success Criteria

- Trial-to-paid conversion rate stabilizes at 15-30% (healthy SaaS range) after pricing optimization
- Tier distribution shows healthy spread: 20-30% entry, 50-60% middle, 15-25% top tier
- Net revenue retention exceeds 110% (expansion revenue from upsells outpaces contraction)
- Price increase execution retains 85%+ of affected customers within 90 days
- Annual plan adoption reaches 50%+ when toggle defaults to annual pricing
- Van Westendorp survey confirms current price falls within the acceptable range for 70%+ of respondents
- Pricing page conversion rate improves by 15%+ after redesign implementing best practices

---

## Anti-patterns

| Anti-pattern | Failure mode | Fix |
|--------------|--------------|-----|
| Jumping to the price point before locking the value metric | Discounts and "just lower the price" become the only lever; packaging is stuck | Work the axes in order: value metric → packaging → price point |
| Copying a competitor's pricing model | Inherits their positioning and unit economics — which may not fit the product | Use competitor pricing as a data point for the corridor, not a template |
| Per-seat pricing on a tool where one power user does the work | Usage grows but seats don't; revenue stalls | Switch to usage-based, hybrid (base + usage), or per-feature |
| Raising prices to fix a churn problem | Churn accelerates; pricing gets blamed for a retention problem | Diagnose churn drivers first; if the product is the issue, price increases amplify the damage |
| Adding a fourth tier to "capture more willingness to pay" | Paradox of choice collapses conversion; sales cycle lengthens | Keep 3 tiers public; put the fourth behind "Contact Sales" if enterprise-specific |
| Announcing a price increase without grandfathering existing customers | Immediate churn spike; NPS collapse; public backlash | Grandfather for 6-12 months on annual plans; communicate 90+ days in advance |
| Using MSRP or list price internally for forecasting | Actual ACV diverges from list by 20-40% due to discounts; forecasts miss | Forecast on expected-realized price net of standard discount, not list |
| Freemium tier that gives away the core value metric | Free users never convert; paid tier cannibalized | Gate the value metric (volume, seats, integrations) — not feature access only |
