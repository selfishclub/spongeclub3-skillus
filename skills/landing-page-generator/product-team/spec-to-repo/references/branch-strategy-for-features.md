# Branch Strategy for Features

Reference for branching, feature flags, and incremental shipping in a
modern engineering workflow.

## 1. The basic branching models

### Trunk-based (recommended for most teams)
- Single long-running branch (main / trunk)
- Short-lived feature branches (hours to days)
- All work merges back to trunk quickly
- Behind-flag for in-progress work
- Continuous deployment from trunk

**Fits when:** team has good CI, feature flags, and discipline.
**Breaks when:** team can't deploy frequently or lacks feature flags.

### GitFlow (legacy; mostly avoid)
- Multiple long-running branches (main, develop, release)
- Heavy ceremony for release management
- Slow integration cycle

**Fits when:** large release cycles, regulatory environments.
**Breaks when:** modern continuous-deployment culture is the goal.

### GitHub Flow (the middle ground)
- Main branch is always deployable
- Feature branches off main
- PR to merge back; deploy after merge

**Fits when:** SaaS web product, CI is strong, deploys aren't every commit.

## 2. Trunk-based + feature flags — the modern default

The pattern most modern engineering teams converge on:

1. Branch from main for a feature (lasts hours to a few days)
2. Implement behind a feature flag (off by default)
3. PR — small, reviewable, can be merged even if feature isn't complete
4. Repeat steps 1-3 until feature is complete
5. Enable flag (separate, small, reviewable PR)
6. Validate in production (canary → ramp)
7. Remove flag once stable

See `engineering/feature-flags-architect` for deep flag strategy.

## 3. Branch naming conventions

Pick one; enforce in CI / hooks.

### Common conventions

```
feature/{ticket}-{short-desc}    # feature/PROJ-123-mute-channel
fix/{ticket}-{short-desc}         # fix/PROJ-456-onboarding-crash
chore/{ticket}-{short-desc}       # chore/PROJ-789-upgrade-deps
hotfix/{ticket}-{short-desc}      # hotfix/PROJ-999-cancel-button
{owner}/{ticket}-{short-desc}     # alice/PROJ-123-mute-channel
{owner}/{short-desc}              # alice/mute-channel
```

### Rules
- Use lowercase, hyphens (not underscores)
- Include the ticket number (linkability)
- Keep < 60 characters
- Avoid version numbers (they age badly)
- Avoid dates (also age)

## 4. PR sequencing for a multi-PR feature

A clean sequence:

### PR 1 — Scaffolding / migration (no behavior change)
- Database migration (additive, backward-compatible)
- New file structure
- Empty service shells
- Feature flag defined (off)

### PR 2-N — Backend changes (behind flag)
- API endpoints
- Service logic
- Tests
- No frontend uses them yet

### PR M-X — Frontend changes (behind flag)
- UI components
- Wires up to backend
- Hidden when flag is off
- Tests assume flag both on + off

### PR Y — Telemetry + analytics
- Events fire
- Dashboards updated
- Alerts configured

### PR Z — Docs + runbooks
- User-facing docs
- Internal runbook
- Migration guide if needed

### PR W — Flag enablement
- Small change: flag default → on (or % rollout)
- Reviewable in isolation
- Easy to revert

## 5. Feature flag patterns

### Boolean flag (simplest)
On/off for everyone or for a tagged set.

### Percentage rollout
1% → 5% → 25% → 50% → 100% with bake time at each step.

### User segment flag
"On for internal employees first" or "on for early-access cohort."

### Multivariate
A/B/C test variants.

### Anti-patterns
- Flags that never get removed (flag debt)
- Flags that gate critical paths (single point of failure)
- Flag changes without comms (surprise launches)

## 6. Dark-launch

Ship code that runs but doesn't yet show user-facing changes:

- Backend computes new behavior; result discarded or shadow-compared
- Validates perf, error rates, correctness at scale
- Risk-free way to test infrastructure before user-facing launch

Used heavily for: search ranking changes, recommendation models,
performance optimizations.

## 7. Canary deployment

Deploy to a small subset of users / instances first:

- Catches deployment regressions before all users affected
- Pair with automatic rollback on error-rate spike
- Standard in modern infra

Distinct from flag-based rollout: canary is about the deploy; flag is
about the user-visible feature.

## 8. Rollback plan

Every meaningful change should have a documented rollback:

- Flag flip (preferred — instant)
- Service revert (slower)
- Migration rollback (sometimes irreversible — design forward)
- Comms plan if user-visible

If "rollback" requires emergency engineering, the rollout plan was incomplete.

## 9. Branch protection rules

Standard protections on main:
- PR required (no direct push)
- Reviews required (typically 1-2)
- CI checks must pass
- Conversation resolution required
- Up-to-date branches (rebase or merge before merging)
- Signed commits (in regulated environments)
- Protected from force-push and deletion

## 10. Branch lifecycle

### Short-lived (recommended)
- Hours to days
- Frequent rebases / merges from main
- Merged or abandoned quickly

### Long-lived (avoid where possible)
- Days to weeks
- Increasing merge conflicts over time
- Becomes its own integration project

If a branch must live long, alternate strategies:
- Behind-flag work merges to main frequently
- Long-lived branch only for genuinely non-mergeable refactors

## 11. Hotfix workflow

When prod is on fire:

1. Branch from main (`hotfix/PROJ-999-name`)
2. Minimal fix; small PR
3. Expedited review (one senior reviewer; CI green)
4. Merge + deploy immediately
5. Postmortem follows

Don't use hotfix for non-emergencies — it bypasses normal discipline.

## 12. Commit conventions

Use a commit standard (e.g., Conventional Commits):

```
feat(scope): short description
fix(scope): short description
docs(scope): short description
chore(scope): short description
refactor(scope): short description
test(scope): short description
```

Why:
- Enables automated changelog generation
- Aids semantic versioning
- Easier to scan history

## 13. Common pitfalls

- **Long-lived branches.** Merge conflicts grow exponentially.
- **No feature flags.** Every change is all-or-nothing.
- **Flag-on PR mixed with implementation PR.** Hard to revert independently.
- **No CI checks on branch.** Bad code merges.
- **No rollback plan.** Production incidents become PR-revert dramas.
- **Inconsistent branch naming.** Tooling can't auto-link to tickets.
- **Hotfix bypassing all review.** Quality debt accumulates.
- **Branches deleted before merge complete.** Lost work / context.
