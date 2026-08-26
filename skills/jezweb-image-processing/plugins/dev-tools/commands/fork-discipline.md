---
description: Audit and enforce the core/client boundary in multi-client codebases
argument-hint: "[audit|document|refactor]"
---

Load the `fork-discipline` skill.

Parse $ARGUMENTS for mode:
- `audit` — map the boundary, find violations, produce a report (default)
- `document` — generate FORK.md for the project
- `refactor` — audit then produce concrete refactoring steps and scripts

Examples: `/fork-discipline`, `/fork-discipline audit`, `/fork-discipline refactor`
