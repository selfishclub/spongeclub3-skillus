# Dashboards, Examples & Success Criteria

Read this when generating executive/engineering dashboards, running an end-to-end scan example, or validating that the tracker meets its quality bar.

## Executive Dashboard

```
TECH DEBT HEALTH
  Overall Score: [0-100]  |  Trend: [improving/declining]
  Cost of Delayed Fixes: [X development days]
  High-Risk Items: [count]

MONTHLY REPORT:
  1. Executive Summary (3 bullet points)
  2. Health Score Trend (6-month view)
  3. Top 3 Risk Items (business impact focus)
  4. Investment Recommendation (resource allocation)
  5. Success Stories (debt resolved last month)
```

## Engineering Dashboard

```
DAILY:
  New items identified  |  Items resolved  |  Interest rate by component

SPRINT REVIEW:
  Debt points completed vs planned  |  Velocity impact
  Newly discovered debt  |  Team code quality sentiment
```

## Example: Scanning a Python Microservice

```bash
# Run debt scanner
python scripts/debt_scanner.py --repo ./payment-service --output debt_inventory.json

# Output summary:
#   Total items found: 47
#   Critical: 3  |  High: 8  |  Medium: 21  |  Low: 15
#
#   Top 3 by cost-of-delay:
#     1. DEBT-001: payment_processor.py - nested exception handling (CoD: 420)
#     2. DEBT-002: db/migrations/ - 12 unapplied migrations (CoD: 315)
#     3. DEBT-003: tests/ - 62% coverage on payment flow (CoD: 280)

# Prioritize items
python scripts/debt_prioritizer.py --inventory debt_inventory.json --sprint-capacity 40

# Generate executive report
python scripts/debt_dashboard.py --inventory debt_inventory.json --baseline previous_scan.json
```

## Success Criteria

- Scan completes in under 60 seconds for repositories up to 100,000 lines of code.
- Every detected debt item includes a unique ID, file path, line number (where applicable), severity, and debt type -- no fields left as null or unknown.
- Health score correlates with manual code review assessments within 15 points on the 0-100 scale when validated against a senior engineer's judgment.
- Prioritized backlog produces a clear top-10 list where the first item has at least 2x the priority score of the tenth item, confirming meaningful differentiation.
- Sprint allocation recommendations fit within the configured capacity (no single sprint exceeds 100% of debt budget) and cover all high-priority items within the first 3 sprints.
- Dashboard trend analysis correctly identifies improving, declining, or stable directions when compared against at least 3 historical snapshots with known trajectories.
- Cost-of-delay calculations produce actionable dollar-equivalent values that engineering managers can use directly in sprint planning and quarterly roadmap discussions.
