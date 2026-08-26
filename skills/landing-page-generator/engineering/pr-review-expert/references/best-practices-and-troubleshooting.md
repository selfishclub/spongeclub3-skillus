# Pitfalls, Best Practices, Troubleshooting & Success Criteria

Read this before and after a review for quality control: common reviewer pitfalls, best-practice habits, a troubleshooting table for the workflow commands/scripts, and the success-criteria bar.

## Common Pitfalls

- **Reviewing style over substance** — let the linter handle formatting; focus on logic, security, correctness
- **Missing blast radius** — a 5-line change in a shared utility can break 20 services
- **Approving untested happy paths** — always check that error paths have coverage
- **Ignoring migration risk** — NOT NULL additions need a default or two-phase migration
- **Indirect secret exposure** — secrets in error messages and logs, not just hardcoded values
- **Skipping large PRs** — if too large to review properly, request it be split
- **Trickle feedback** — batch all comments in one review round; do not drip-feed over hours

## Best Practices

1. **Read the linked ticket first** — context prevents false positives in the review
2. **Check CI before reviewing** — do not review code that fails to build
3. **Prioritize blast radius and security over style** — these are where real bugs live
4. **Label every comment** — `must:`, `nit:`, `question:` so authors know what matters
5. **Batch all comments in one round** — multiple partial reviews frustrate authors
6. **Acknowledge good patterns** — specific praise improves code quality culture
7. **Reproduce locally for non-trivial changes** — especially auth and performance-sensitive code

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Blast radius analysis misses dependents | `grep` only searches `src/` by default | Expand search paths to include `packages/`, `libs/`, and monorepo service directories |
| Security scan produces false positives on test files | Diff includes test fixtures with fake secrets | Filter scan output to exclude `*.test.*`, `*.spec.*`, `__tests__/`, and `fixtures/` paths |
| Breaking change detection flags internal-only types | No distinction between exported and internal interfaces | Check whether flagged types are re-exported from the package entry point before reporting |
| Test coverage delta shows 0 when tests exist | Test files use non-standard naming conventions | Adjust the `grep -E` pattern in Step 5 to match your project's test file naming (e.g., `*.unit.*`, `*_test.*`) |
| `gh pr diff` returns empty output | PR has no commits yet or branch is not pushed | Verify the PR has at least one commit pushed to the remote with `gh pr view $PR --json commits` |
| N+1 detection flags ORM eager-loaded queries | Pattern matching cannot distinguish eager vs lazy loading | Cross-reference flagged lines with ORM configuration to confirm whether relations are pre-loaded |
| Review report is too long for PR comment | PR touches 50+ files across multiple services | Split the review into per-service comments or request the author break the PR into smaller scoped PRs |

## Success Criteria

- Review turnaround time under 30 minutes for PRs with fewer than 500 changed lines
- Zero post-merge security findings on PRs that received a full review using this skill
- Blast radius severity rating matches actual production impact in 90%+ of cases
- All must-fix items are resolved before merge with no exceptions
- Test coverage delta is calculated and reported on every reviewed PR
- Breaking changes are detected before merge in 95%+ of cases, validated against deployment incidents
- Reviewer feedback is batched into a single review round at least 90% of the time
