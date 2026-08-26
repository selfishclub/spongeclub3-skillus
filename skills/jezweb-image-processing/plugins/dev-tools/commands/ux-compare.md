---
description: Compare UX patterns across pattern libraries produced by ux-extract
argument-hint: "[topic or 'whole library'] [optional: 'across [app-1], [app-2], [app-3]']"
allowed-tools: "*"
---

Load the `ux-compare` skill and run the comparison.

$ARGUMENTS should identify the scope (what to compare) and optionally the libraries to include:

- `/ux-compare empty states` — across every available library
- `/ux-compare keyboard shortcuts across claude.ai, linear, superhuman` — specific subset
- `/ux-compare destructive actions` — across every available library
- `/ux-compare whole library across claude.ai and linear` — wide scope, two apps

If fewer than 2 pattern libraries exist under `docs/ux-extracts/` or `.jez/artifacts/ux-extracts/`, the skill will stop and suggest running `ux-extract` first. Comparison with one library is just the library.

Output goes to `docs/ux-comparisons/<topic>-YYYY-MM-DD.md` (or `.jez/artifacts/ux-comparisons/` if that path exists).
