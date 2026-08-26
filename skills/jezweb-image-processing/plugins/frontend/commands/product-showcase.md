---
description: Generate a marketing website for a web app — multi-page with real screenshots and animated GIF walkthroughs
argument-hint: "[quick: single page | standard: multi-page site | thorough: comprehensive with GIFs + use cases]"
---

Load the `product-showcase` skill.

Parse $ARGUMENTS for depth:
- `quick` — single page, hero + features + CTA (15-20 min)
- `standard` — multi-page: home, features, how-it-works with screenshots (1-2 hours)
- `thorough` — comprehensive: per-feature pages, animated GIF walkthroughs, use case scenarios, comparison page (3-6 hours)

URL auto-detected from wrangler.jsonc or running dev server.

Examples: `/product-showcase thorough`, `/product-showcase standard`, `/product-showcase quick`
