---
description: Post project updates to team chat, gather and triage feedback
argument-hint: "[update | check | standup | feedback | plan]"
allowed-tools: "*"
---

Load the `team-update` skill and execute based on $ARGUMENTS:

| Argument | Action |
|----------|--------|
| `update` | Full cycle: gather context, draft, post, read feedback, triage |
| `check` | Read and triage team feedback only (Phase 3) |
| `standup` | Gather and post update, skip feedback (Phase 1 + 2) |
| `feedback` | Read feedback and plan next steps (Phase 3 + 4) |
| `plan` | Gather, post, and plan — skip feedback triage (Phase 1 + 2 + 4) |
| (none) | Default to full cycle (`update`) |
