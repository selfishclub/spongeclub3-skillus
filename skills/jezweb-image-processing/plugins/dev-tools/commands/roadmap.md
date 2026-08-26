---
description: Plan and execute entire application builds — roadmap generation + autonomous phase-by-phase execution
argument-hint: "[plan|start|resume|status] [product brief or topic]"
---

Load the `roadmap` skill.

Parse $ARGUMENTS for mode:
- `plan [topic]` — generate a ROADMAP.md from a brief or deep-research output
- `start` — begin executing from phase 1, don't stop until done or stuck
- `resume` — pick up from where the last session left off, keep going
- `status` — show which phases are complete and what's next

Default: `plan` if no roadmap exists, `resume` if one does.

Examples: `/roadmap plan markdown note app on cloudflare`, `/roadmap start`, `/roadmap resume`, `/roadmap status`
