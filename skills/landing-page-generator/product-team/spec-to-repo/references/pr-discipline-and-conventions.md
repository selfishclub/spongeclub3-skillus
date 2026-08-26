# PR Discipline & Conventions

Reference for PR size, structure, review, and the conventions that make
PRs ship faster with fewer regressions.

## 1. PR size — the single biggest variable

Smaller PRs:
- Get reviewed faster
- Get reviewed better
- Cause fewer regressions
- Merge faster
- Are easier to revert

Larger PRs:
- Get rubber-stamped
- Hide bugs
- Block merges
- Are harder to revert

### Size guidelines
- **< 100 lines:** ideal; review in 5 min
- **100-300 lines:** good; review in 15-30 min
- **300-500 lines:** acceptable; review in 30-45 min
- **500-1000 lines:** large; consider splitting
- **> 1000 lines:** almost always split

### What to count
- Net lines (additions − deletions)
- Exclude generated files (lock files, snapshots, etc.)
- Exclude test data fixtures

### When large is unavoidable
- Major refactors (call it out, find specialized reviewer)
- New file additions (less risky than modifications)
- Generated code

## 2. PR structure

### Title
- Conventional commit style if your team uses it
- Imperative mood: "Add mute-channel feature" not "Added"
- < 70 characters
- Reference ticket: "(PROJ-123)"

### Description (template)
```markdown
## What
Brief description of what changed.

## Why
Link to PRD / ticket; brief context.

## How
High-level approach; non-obvious decisions.

## Testing
- Unit tests added
- Manual test plan
- How to verify in staging

## Risk + rollout
- Feature flag: PROJ_FLAG_X
- Rollout plan: behind flag, internal first
- Rollback: flip flag

## Screenshots / videos
[If UI]

## Checklist
- [ ] Tests added/updated
- [ ] Docs updated
- [ ] Telemetry events added
- [ ] Feature flag configured
- [ ] Accessibility checked
- [ ] Performance considered
```

Templates enforced in the PR creation flow ensure consistency.

## 3. The review SLA

A working review SLA:

- **Initial review:** within 1 business day
- **Re-review:** within 1 business day of changes
- **Approval-or-discussion:** within 2 business days of opening

Track median + P95 PR cycle time. Slow review is a productivity killer.

## 4. Review behaviors

### What to do
- Review for design, correctness, readability
- Be specific in feedback ("Consider extracting line 47-60 to function" not "Refactor")
- Distinguish blocking from optional
- Approve when you'd accept; don't gate on nits
- Use thread-resolution to track follow-ups
- Speak through behavior, not personality

### What to avoid
- Reviewing for style issues a linter catches
- "Looks good" without actually reading
- Stacking required revisions on minor issues
- Reviewing in passive-aggressive mode
- Re-architecting the PR in review comments

### Reviewer responsibilities
- **Code owner:** must approve
- **Domain expert:** may be asked for input
- **General reviewer:** double-checks readability + obvious issues

For sensitive areas (security, data, billing), require specialist review.

## 5. Definition of done (DoD)

A PR is "done" when:

### Always
- Code is written and reviewed
- Required reviewers approved
- All CI checks pass
- Conversations resolved
- Branch up-to-date with main

### When applicable
- Tests added (or explicit "tests deferred to PR-Y")
- Docs updated
- Telemetry events firing in staging
- Feature flag configured
- Migration tested in staging
- Performance benchmarked
- Accessibility reviewed
- Security review done

### Per-team additions
- Code owners listed
- Specific QA acceptance
- Designer sign-off (if UI change)
- Product sign-off (if user-visible change)

## 6. CI checks

Standard set:
- Linter
- Unit tests
- Integration tests
- Build / typecheck
- Security scan (SAST, dependency scan)
- Code coverage report
- Bundle size / perf budget (frontend)
- Visual regression (UI)
- Mobile build + tests (if mobile)

Bad CI tax: slow CI delays every PR. Aim for < 10 min total CI time.

## 7. Auto-merge

Auto-merge ships PRs when criteria are met:
- All required reviews approved
- All CI checks pass
- No outstanding conversations
- Branch up-to-date with main

Useful for:
- Low-risk PRs in heavily-trafficked repos
- Multi-PR sequences where each PR is reviewed
- Out-of-hours work that's safe to merge

Don't use auto-merge for:
- Risky changes
- PRs that touch sensitive areas
- Changes you want a human to make the final call on

## 8. Mergeable types

### Squash and merge
- Single commit on main
- Cleaner history
- Loses commit-level context

Recommended for:
- Most feature PRs
- Most fix PRs

### Rebase and merge
- Original commits preserved
- Linear history
- Forces local rebase before merge

Recommended for:
- Multi-commit PRs where each commit is meaningful

### Merge commit
- Preserves branch structure
- "Merged feature/X" commit appears on main

Use when:
- Long-running branch with intentional structure
- Avoid if team prefers linear history

Pick one as default; enforce in repo settings.

## 9. Reverting

When a merged PR breaks something:

### Option 1: revert PR
- Git revert; create revert PR
- Fast; uncontroversial
- May lose collateral fixes

### Option 2: forward-fix PR
- Fix the breakage with a new PR
- Slower; sometimes inevitable
- Better when revert is destructive

Choose based on: speed needed, how isolated the bug is, whether revert
creates conflicts.

## 10. PR ownership and review load

### Track:
- PRs authored per engineer per week
- Reviews completed per engineer per week
- Review cycle time per engineer

### Common imbalances:
- Senior engineers review more than they author
- New engineers author more than they review
- Specialists become bottlenecks in their domain

Address through:
- Code-ownership rotation
- Pair reviewing for sensitive areas
- "Backup reviewer" for any single-point area
- Tooling-based review routing (CODEOWNERS file)

## 11. Drafts and WIP

Use draft PRs for:
- Early feedback before complete
- Architectural review before deep implementation
- Coordinating with another PR

Drafts shouldn't:
- Be the default state for everything
- Stay drafts for weeks
- Have CI run repeatedly (wastes resources)

## 12. PR labels (useful conventions)

- `type:feature`, `type:fix`, `type:chore`
- `area:backend`, `area:frontend`, `area:infra`
- `risk:low`, `risk:medium`, `risk:high`
- `needs-design-review`, `needs-security-review`
- `do-not-merge` (with reason)
- `breaking-change`

Labels enable filtering + automation.

## 13. PR-to-ticket linkage

Every PR should reference its ticket:
- In the title or body
- Closes / refs syntax that auto-links in the tracker
- Makes it easy to trace code change to product decision

Without linkage, future you can't tell why a change was made.

## 14. Common pitfalls

- **PRs that touch 30 files.** Split.
- **PRs with no description.** Reviewer must reverse-engineer.
- **Style-only review comments.** Lint catches these; don't waste reviewer time.
- **Approve-without-reading.** Trust dies.
- **PRs that languish for weeks.** Author moves on; reviewer forgets context.
- **Auto-merge on risky changes.** Bypass review safeguards.
- **Re-architecting in review.** Should have been a design conversation earlier.
- **No tests in PRs that need them.** "We'll add later" = never.
- **Linked ticket marked done before PR merges.** Loses traceability.
