---
description: Generate publishable user documentation with screenshots from a running app
argument-hint: "[quick: quick-start | standard: full guide | thorough: comprehensive | exhaustive: publishable suite]"
---

Load the `app-docs` skill.

Parse $ARGUMENTS for depth:
- `quick` — quick-start guide, 10 screenshots, key screens only
- `standard` — full user guide, 30 screenshots, all pages and workflows (default)
- `thorough` — comprehensive guide, 80+ screenshots, every state, mobile, dark mode, troubleshooting
- `exhaustive` — publishable documentation suite, 150+ screenshots, HTML version, admin guide, FAQ, every edge case

URL auto-detected from wrangler.jsonc or running dev server.
