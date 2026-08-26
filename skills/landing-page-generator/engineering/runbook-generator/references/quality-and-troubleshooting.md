# Quality Bar: Pitfalls, Best Practices, Troubleshooting & Success Criteria

Read this before shipping a runbook — check it against the pitfalls, best-practice checklist, troubleshooting table, and success criteria.

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Commands with placeholder values | Use environment variables: `$PROD_DB_URL` not `postgres://user:pass@host/db` |
| No expected output after commands | Add VERIFY block with exact expected output |
| Missing rollback steps | Every destructive step needs a corresponding undo |
| Runbooks that never get tested | Schedule quarterly staging dry-runs |
| Outdated escalation contacts | Review contacts every quarter |
| Migration runbook ignores table locks | Explicitly call out lock risk for large table operations |
| Copy-pasting production URLs into runbooks | Use environment variable references that resolve at runtime |

## Best Practices

1. **Every command must be copy-pasteable** — use env vars, not placeholder text
2. **VERIFY after every step** — explicit expected output, not "it should work"
3. **Time estimates are mandatory** — engineers need to know if they have time before SLA breach
4. **Rollback before you deploy** — plan the undo before executing the action
5. **Runbooks live in the repo** — `docs/runbooks/`, versioned with the code they describe
6. **Postmortem drives runbook updates** — every incident should improve at least one runbook
7. **Link, do not duplicate** — reference the canonical config, do not copy its contents
8. **Test runbooks like you test code** — untested runbooks are worse than no runbooks (false confidence)

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Stack detection returns no results | Repo uses non-standard config file names or paths | Manually specify the stack in the runbook header; extend detection script with custom paths |
| Generated commands fail in staging | Environment variables not set or differ between environments | Verify all referenced env vars exist in the target environment with `printenv \| grep PROD` before executing |
| Staleness script reports false positives | Config files touched by formatting-only commits (linting, whitespace) | Filter staleness checks by diffing actual content changes: `git diff --stat` on the flagged commit |
| Runbook steps are out of order after a platform upgrade | Hosting provider changed their deploy pipeline or CLI flags | Re-run stack detection after every major platform upgrade; diff the new CLI help output against runbook commands |
| Escalation contacts are stale | Team rotations or org changes not reflected in runbooks | Integrate escalation tables with your on-call tool API (PagerDuty, Opsgenie) so contacts resolve dynamically |
| Rollback procedure fails mid-execution | Database migration was partially applied before the deploy failed | Always wrap migrations in transactions where the engine supports it; include a "partial rollback" section for non-transactional DDL |
| Runbook verification checks pass but the feature is broken | Smoke tests only cover health endpoint, not critical user paths | Add at least three smoke-test URLs per runbook: health, auth, and one core business endpoint |

## Success Criteria

- **Runbook coverage >= 90%** — every production service has at least a deployment and incident response runbook
- **Mean time to mitigate (MTTM) drops by 30%+** within one quarter of adopting generated runbooks
- **Zero placeholder commands** — every command in every runbook is copy-pasteable without manual editing beyond env var substitution
- **Staleness rate < 10%** — fewer than 10% of runbooks flagged as stale in any given quarterly review cycle
- **Quarterly dry-run pass rate >= 95%** — at least 95% of runbook steps execute successfully in staging during scheduled dry-runs
- **On-call onboarding time < 2 hours** — a new engineer can read all runbooks for their service and feel confident to handle L1 incidents within two hours
- **Post-incident runbook update rate = 100%** — every postmortem produces at least one runbook addition or correction
