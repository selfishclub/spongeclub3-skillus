---
description: Exhaustively extract UX patterns from a reference web app into a reusable pattern library
argument-hint: "[URL or app name] [optional: 'focus on X' for a narrower scope]"
allowed-tools: "*"
---

Load the `ux-extract` skill and run the extraction.

$ARGUMENTS should identify the reference app (URL or well-known name) and optionally a scope or focus lens:
- `/ux-extract claude.ai` — extract the whole app
- `/ux-extract claude.ai focus on empty states` — narrower scope
- `/ux-extract https://linear.app the onboarding flow` — specific feature area

Output goes to `docs/ux-extracts/<app-name>/pattern-library.md` (or `.jez/artifacts/ux-extracts/<app-name>/` if that directory exists).

The pattern library can be consumed by `ux-audit` as a comparison bar.
