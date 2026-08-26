# Scoring, Prioritization & Sprint Methodology

Read this when scoring debt items, computing cost-of-delay, prioritizing the backlog, allocating sprint capacity, or planning quarterly debt themes.

## Workflow

1. **Scan codebase** -- Run the Debt Scanner against the target repository. It uses AST parsing and pattern matching to detect debt signals across all six categories (code, architecture, test, documentation, dependency, infrastructure).
2. **Score each item** -- Apply the Severity Scoring Framework. Rate each item on velocity impact, quality impact, productivity impact, and business impact (1-10 each). Estimate effort (XS-XL) and risk level.
3. **Calculate interest rate** -- For each item, compute `Interest Rate = Impact Score x Frequency of Encounter` per sprint. Calculate `Cost of Delay = Interest Rate x Sprints Until Fix x Team Size Multiplier`.
4. **Prioritize** -- Plot items on the Cost-of-Delay vs Effort matrix. Assign priority: Immediate (high cost, low effort), Planned (high cost, high effort), Opportunistic (low cost, low effort), Backlog (low cost, high effort).
5. **Allocate sprint capacity** -- Apply the Debt-to-Feature Ratio based on current team velocity. Reserve the recommended percentage for debt work.
6. **Generate reports** -- Produce the Executive Dashboard (health score, trend, top risks, investment recommendation) and the Engineering Dashboard (daily new/resolved, interest rate by component, hotspots).
7. **Track trends** -- Compare current scan against previous baselines. Alert if debt accumulation rate exceeds paydown rate for two consecutive sprints.

## Debt Classification

| Category | Key Indicators | Detection Method |
|----------|---------------|-----------------|
| Code | Functions > 50 lines, nesting > 4 levels, cyclomatic complexity > 10, duplicate blocks > 3 | AST parsing, complexity metrics |
| Architecture | Circular dependencies, tight coupling, missing abstraction layers, monolithic components | Dependency analysis, coupling metrics |
| Test | Coverage < 80% on critical paths, flaky tests, test suite > 10 min | Coverage reports, failure pattern analysis |
| Documentation | Missing API docs, outdated READMEs, no ADRs, stale comments | Coverage analysis, freshness checking |
| Dependency | Known CVEs, deprecated APIs, unused packages, version conflicts | Vulnerability scanning, usage analysis |
| Infrastructure | Manual deploys, missing monitoring, env inconsistencies, no DR plan | Audit checklists, config drift detection |

## Severity Scoring Framework

Rate each dimension 1-10:

| Dimension | 1-2 | 5-6 | 9-10 |
|-----------|-----|-----|------|
| Velocity Impact | Negligible | Affects some features | Blocks new development |
| Quality Impact | No defect increase | Moderate defect increase | Critical reliability problems |
| Productivity Impact | No team impact | Regular complaints | Causing developer turnover |
| Business Impact | No customer impact | Moderate performance hit | Revenue-impacting issues |

**Effort sizing**: XS (1-4 hrs), S (1-2 days), M (3-5 days), L (1-2 weeks), XL (3+ weeks)

## Interest Rate and Cost of Delay

```
Interest Rate = Impact Score x Frequency of Encounter (per sprint)
Cost of Delay = Interest Rate x Sprints Until Fix x Team Size Multiplier

Example:
  Legacy auth module with poor error handling
  Impact: 7  |  Frequency: 15 encounters/sprint  |  Team: 8 devs
  Planned fix: sprint 4 (3 sprints away)

  Interest Rate = 7 x 15 = 105 points/sprint
  Cost of Delay = 105 x 3 x 1.2 = 378 total cost points
```

## Prioritization Matrix

| Quadrant | Cost of Delay | Effort | Action |
|----------|--------------|--------|--------|
| Immediate (quick wins) | High | Low | Do first |
| Planned (major initiatives) | High | High | Schedule dedicated sprints |
| Opportunistic | Low | Low | Fix when touching related code |
| Backlog | Low | High | Reconsider quarterly |

### WSJF Alternative

```
WSJF = (Business Value + Time Criticality + Risk Reduction) / Effort
```

Each component scored 1-10. Highest WSJF items are prioritized first.

## Sprint Allocation (Debt-to-Feature Ratio)

| Team Velocity | Debt % | Feature % | Strategy |
|--------------|--------|-----------|----------|
| < 70% of capacity | 60% | 40% | Remove major blockers |
| 70-85% of capacity | 30% | 70% | Balanced maintenance |
| > 85% of capacity | 15% | 85% | Opportunistic only |

**Sprint planning rule**: Reserve 20% of sprint capacity for debt. Prioritize items with the highest interest rates. Add "debt tax" to feature estimates when working in high-debt areas.

## Debt Item Data Structure

```json
{
  "id": "DEBT-2024-001",
  "title": "Legacy user authentication module",
  "category": "code",
  "subcategory": "error_handling",
  "location": "src/auth/legacy_auth.py:45-120",
  "description": "Authentication error handling uses generic exceptions",
  "impact": { "velocity": 7, "quality": 8, "productivity": 6, "business": 5 },
  "effort": { "size": "M", "risk": "medium", "skill_required": "mid" },
  "interest_rate": 105,
  "cost_of_delay": 378,
  "priority": "high",
  "status": "identified",
  "tags": ["security", "user-experience", "maintainability"]
}
```

**Status lifecycle**: Identified > Analyzed > Prioritized > Planned > In Progress > Review > Done | Won't Fix

## Refactoring Strategies

| Strategy | When to Use | How It Works |
|----------|-------------|-------------|
| Strangler Fig | Large monoliths, high-risk migrations | Build new around old; gradually redirect traffic; remove old |
| Branch by Abstraction | Need old + new running in parallel | Create interface; implement both behind it; switch via config |
| Feature Toggles | Gradual rollout of refactored components | Add toggle at decision points; test both paths; remove old |
| Parallel Run | Critical business logic changes | Run both implementations; compare outputs; build confidence |

## Quarterly Planning

1. Identify 1-2 major debt themes per quarter
2. Allocate dedicated sprints for large-scale refactoring
3. Plan debt work around major feature releases
4. Track: debt interest rate reduction, velocity improvements, defect rate reduction, code review cycle time
