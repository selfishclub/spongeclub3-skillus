# Engineering Productivity & Quality Reference

Practical reference for measuring and improving engineering productivity
and quality. Grounded in DORA, SPACE, and DevEx frameworks.

## 1. The frameworks — what each is for

### DORA (Accelerate)
Four metrics that correlate with high-performing orgs:
- **Deployment frequency** — how often code reaches production
- **Lead time for changes** — commit to production
- **Mean time to recover (MTTR)** — restoration time after incident
- **Change failure rate** — % of deploys that cause a production incident

Used for: org-level delivery performance; benchmarking; identifying
slow-moving teams.

### SPACE (research framework)
Five dimensions of productivity:
- **S**atisfaction & well-being
- **P**erformance (delivery + quality)
- **A**ctivity (commits, PRs, etc — used cautiously)
- **C**ommunication & collaboration
- **E**fficiency & flow

Used for: holistic view; reminds you not to over-index on Activity.

### DevEx (Developer Experience)
Three loops:
- **Feedback loops** — fast CI, fast tests, fast deploys
- **Cognitive load** — context-switching, complexity
- **Flow state** — uninterrupted focus time

Used for: identifying friction; pairs with SPACE for the "Why"
behind DORA numbers.

## 2. DORA classification bands

The Accelerate research classifies orgs into bands:

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| Deploy frequency | On-demand (multiple/day) | Daily–weekly | Weekly–monthly | < monthly |
| Lead time | < 1 hour | 1 day–1 week | 1 week–1 month | > 1 month |
| MTTR | < 1 hour | < 1 day | 1 day–1 week | > 1 week |
| Change fail rate | 0–15% | 16–30% | 31–45% | > 45% |

These are bands, not targets. The Elite band is rare and not always
desirable (e.g., regulated industries may have appropriate change
management overhead).

## 3. How to measure (without lying to yourself)

### Deploy frequency
- Count actual production deploys, per service, per week
- Exclude infrastructure no-ops; exclude rollbacks
- Aggregate at team level

### Lead time
- Time from commit to first deploy to production
- Use deployment system + git commits; don't ask engineers to log it
- Median + P75 + P95 (P95 is where the pain is)

### MTTR
- Time from incident declared to incident resolved
- Use incident management system; exclude false alarms
- Median + P75

### Change failure rate
- (Deploys causing incident) / (Total deploys)
- Define "incident" consistently; SEV1-3 typical
- Track per service and aggregate

### DevEx (qualitative)
- Quarterly survey: 8–12 questions
- Net Promoter Score for DevEx
- Theme tagging on open-ended responses
- Tied to action commitments

## 4. Productivity anti-metrics

DO NOT use:
- **Lines of code** — incentivizes verbosity
- **PR count per engineer** — incentivizes shallow PRs
- **Commit count** — incentivizes micro-commits
- **Story points completed** — incentivizes inflation; not portable
- **Hours worked** — incentivizes burnout
- **Closed tickets** — incentivizes wrong work

These metrics show activity, not outcomes. Track DORA + DevEx + business
outcomes instead.

## 5. SLOs and error budgets

Service Level Objectives are the contract between reliability and velocity.

### SLO basics
- Pick 1–3 critical user journeys per service
- Define an SLI (Service Level Indicator) per journey (e.g., latency, error rate)
- Set an SLO (e.g., 99.9% of requests under 200ms)
- Compute error budget = (1 - SLO) over time window

### Error budget policy
- Healthy budget: ship freely
- Budget consumed > 50%: prioritize reliability work
- Budget exhausted: feature work pauses; reliability focus until budget recovers

See `engineering/observability-designer` for deeper SLO design.

## 6. Incident management

### Severity definition (publish in advance)
- **SEV1** — customer-facing outage or material data loss
- **SEV2** — significant degradation
- **SEV3** — minor degradation
- **SEV4** — internal-only

### Response targets
| Severity | Initial response | Resolution target |
|----------|------------------|-------------------|
| SEV1 | < 5 minutes | < 1 hour |
| SEV2 | < 15 minutes | < 4 hours |
| SEV3 | < 1 hour | < 1 day |
| SEV4 | < 1 day | < 1 week |

### Blameless postmortem
- Within 5 business days of incident
- Focus on systems, not individuals
- Action items with owners + due dates
- Published widely (don't hide failures)

See `engineering/incident-commander` for deeper incident response practice.

## 7. On-call

### Rotation design
- 4–8 engineers per rotation
- Weekly rotations (with handoff doc)
- Primary + secondary
- Coverage across time zones if global

### On-call expectations
- Acknowledge alerts within published SLA
- Investigate, mitigate, escalate
- Document during the incident; don't wait
- Postmortem ownership

### Health checks
- Page volume per rotation (target: < 5 actionable pages per week)
- After-hours page rate (target: < 25% of pages)
- Sleep disruption tracking
- On-call satisfaction in DevEx survey

If on-call is broken, productivity dies. Fix the noisy alerts; fix the
unstable services; expand rotation; pay extra; not just "thanks for on-call."

## 8. Code review

### Review SLA
- Initial review within 1 business day
- Resolution within 2 business days
- Auto-assignment based on code ownership

### Review norms
- Kindness + rigor
- Approve when ready; don't gate on style nits
- Use comments for blocking vs nit distinction
- Review for design + correctness + readability
- Don't review for things linters / CI catch

### Health checks
- PR review cycle time
- PR size distribution (smaller is better)
- Re-review rate (high = unclear initial feedback)

## 9. Testing strategy

### Test pyramid
- Unit tests: fast, cover business logic
- Integration tests: cover key paths
- E2E tests: cover top user journeys (small number, high value)
- Manual / exploratory: for unusual paths

### Coverage targets
- Don't enforce % coverage as a target; it incentivizes worthless tests
- Do enforce: critical paths covered; new code has tests

### Test reliability
- Flake rate < 1% — kill flaky tests aggressively
- Test runtime in CI: < 10 minutes ideally; < 30 minutes maximum
- Failed tests block merge

## 10. Tech debt management

### Visibility
- Maintain a tech debt register per team
- Prioritize like features: cost of carrying vs cost of fixing
- Allocate 15–25% of capacity to tech debt (per quarter)

### Categories
- **Forced** — must fix (security, dependency EOL)
- **Strategic** — fixes unblock future work
- **Optional** — quality of life

### Anti-patterns
- "Tech debt sprint" once a year — doesn't work; debt accumulates faster
- Tech debt with no impact statement — gets de-prioritized
- All tech debt funded; no features ship — wrong balance

## 11. Engineering experience surveys

### Cadence
- Quarterly is standard
- 8–12 questions max
- Mix Likert + open-ended

### Sample questions
1. "I can ship code to production confidently."
2. "Our CI pipeline is fast enough to support my work."
3. "I get useful feedback on my code reviews."
4. "Our on-call rotation is sustainable for me."
5. "I have enough time for focused, deep work."
6. "I know what's expected of me and how I'm performing."
7. "My manager helps me grow in my career."
8. "I'd recommend [company] as a place to engineer." (eNPS)

### Action loop
- Synthesis published company-wide
- Top 3 themes addressed with named owners
- Closed-loop comm at next survey ("you said / we did")

## 12. Quality programs

### Quality engineering
- Not a separate QA team; quality is everyone's job
- Quality engineers as enablers: test infrastructure, test data, eval harness
- Specialists for security testing, performance testing, accessibility

### Product quality KPIs
- Bug escape rate (bugs found post-release / total bugs)
- Customer-reported bugs per million sessions
- P1 / P0 bug count
- Time to fix per severity

### Release quality
- Pre-prod environments match prod closely
- Canary releases for risky changes
- Feature flags for risky features (see `engineering/feature-flags-architect`)
- Rollback procedure tested

## 13. Productivity tools

A modern engineering productivity stack:

| Layer | Pick |
|-------|------|
| Git hosting | GitHub / GitLab |
| CI/CD | GitHub Actions / GitLab CI / CircleCI / Jenkins |
| Code review | GitHub PR / GitLab MR |
| Observability | DataDog / Honeycomb / Grafana stack |
| Incident management | PagerDuty / Opsgenie / VictorOps |
| Internal developer portal | Backstage / Cortex |
| Feature flags | LaunchDarkly / Flagsmith / Statsig |
| Productivity analytics | LinearB / Swarmia / Allstacks / Jellyfish |
| DevEx survey | DX / Pulse / custom |

Don't buy three tools that do the same thing.

## 14. Common pitfalls

- **DORA metrics as a performance stick.** Use as compass, not weapon.
- **Activity metrics in performance reviews.** Punishes deep work.
- **Postmortems that find a culprit.** Blameless or not at all.
- **On-call burnout ignored.** Top engineers leave first.
- **Test coverage targets above 80%.** Diminishing returns; perverse incentives.
- **Tech debt is "free" to engineering.** Carry cost compounds.
- **DevEx survey without action.** Trains the org not to respond.
- **CI pipeline > 20 minutes.** Kills flow; demands optimization.
