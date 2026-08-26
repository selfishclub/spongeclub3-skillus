# Quality, Best Practices & Troubleshooting

Read this when verifying generated onboarding docs and before shipping them — it holds the quality verification checklist, common pitfalls, best practices, troubleshooting matrix, and success criteria.

## Quality Verification

After generating onboarding docs, validate with this checklist:

1. **Fresh machine test** — can a new developer follow the setup guide verbatim on a clean machine?
2. **10-minute target** — does local setup complete in under 10 minutes?
3. **Error coverage** — do the documented errors match what developers actually encounter?
4. **Link validity** — do all links to external resources and internal docs resolve?
5. **Currency** — are all version numbers, commands, and screenshots current?

## Common Pitfalls

- **Docs written once, never updated** — add doc update checks to the PR template
- **Missing "why" for architecture decisions** — document why, not just what
- **Untested setup instructions** — test the docs on a fresh machine quarterly
- **No debugging section** — the debugging guide is the most valuable section for new hires
- **Too much detail for the wrong audience** — contractors need task-specific docs, not deep architecture
- **Stale screenshots** — UI screenshots go stale fast; link to running instances when possible

## Best Practices

1. **Keep setup under 10 minutes** — if it takes longer, fix the setup process, not the docs
2. **Test the docs** — have a new hire follow them literally and fix every gap they hit
3. **Link, do not repeat** — reference ADRs, issues, and external docs instead of duplicating
4. **Update docs in the same PR as code changes** — documentation drift is the number one failure mode
5. **Version-specific notes** — call out what changed in recent versions so returning developers catch up
6. **Runbooks over theory** — "run this command" is more useful than "the system uses Redis for caching"
7. **Key file map is mandatory** — every project should have an annotated list of the 10-20 most important files

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Generated setup guide fails on fresh machine | Implicit dependencies not captured during analysis | Re-run Phase 1 gather commands on a clean environment; add every missing tool to the prerequisites table |
| Architecture diagram does not match actual data flow | Analysis relied on stale code paths or unused modules | Cross-reference with `git log --since="90 days"` to find active code paths; interview a senior engineer to validate |
| Key file map is too large (30+ files) | No prioritization applied; every file treated equally | Limit to 15-20 files maximum; rank by edit frequency (`git log --format='%H' -- <file> | wc -l`) and coupling |
| Onboarding doc goes stale within weeks | No process ties doc updates to code changes | Add a "docs" checkbox to the PR template; schedule quarterly freshness reviews |
| Audience sections feel generic | Same content served to juniors, seniors, and contractors | Generate separate docs per audience or use collapsible sections; run the audience customization checklist from this skill |
| Debugging guide missing real errors | Errors were invented rather than collected from logs | Mine actual error messages from Sentry, CI logs, and Slack support channels before writing the guide |
| Environment variable list is incomplete | `grep` scan missed dynamically constructed variable names | Supplement grep results with a manual review of config loader files and `.env.example`; verify against deployment manifests |

## Success Criteria

- **Setup completion rate**: 90%+ of new developers reach a working local environment within 10 minutes using only the generated guide (no Slack questions needed).
- **First-commit time**: New hires make their first meaningful commit within 2 business days of starting onboarding.
- **Error coverage**: The debugging guide covers at least 80% of errors reported in the team's support channel over the prior 90 days.
- **Doc freshness**: Onboarding documentation passes a quarterly freshness audit with fewer than 3 stale sections flagged.
- **Key file accuracy**: The key file map covers all files edited in more than 5 PRs during the past quarter.
- **Audience satisfaction**: Post-onboarding survey scores average 4.0+ out of 5.0 across junior, senior, and contractor cohorts.
- **Link validity**: Zero broken internal or external links when validated by an automated link checker at publish time.
