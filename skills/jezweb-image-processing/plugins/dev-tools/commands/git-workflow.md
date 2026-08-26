---
description: Guided git workflows — PRs, branch cleanup, conflict resolution
argument-hint: "[pr|clean|conflicts|tag]"
---

Load the `git-workflow` skill.

Parse $ARGUMENTS for action:
- `pr` — prepare a pull request
- `clean` — clean up merged/stale branches
- `conflicts` — resolve merge conflicts
- `tag` — create a version tag

Default: detect what's needed from git status.
