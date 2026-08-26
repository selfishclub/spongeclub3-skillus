---
description: Generate project documentation from codebase analysis
argument-hint: "[all|architecture|api|database]"
---

Load the `project-docs` skill.

Parse $ARGUMENTS for which docs to generate:
- `all` — ARCHITECTURE.md + API_ENDPOINTS.md + DATABASE_SCHEMA.md
- `architecture` — ARCHITECTURE.md only
- `api` — API_ENDPOINTS.md only
- `database` — DATABASE_SCHEMA.md only

Default: detect what's needed based on project type.
