---
description: Audit and manage project configuration — permissions, context, docs
argument-hint: "[full | setup | tidy | capture | preset | restructure]"
allowed-tools: "*"
---

Run the project-health skill with the specified mode.

Load the `project-health` skill first, then execute based on $ARGUMENTS:

| Argument | Mode |
|----------|------|
| (none) / `full` | Full health check: permissions + context audit |
| `setup` | New project setup (settings.local.json, CLAUDE.md, .gitignore) |
| `tidy` | Tidy permissions file only |
| `capture` | Capture session learnings to CLAUDE.md |
| `preset` | Add a permission preset (will ask which one) |
| `restructure` | Restructure oversized context files |

If no argument provided, run the full health check.
