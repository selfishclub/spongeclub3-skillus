---
description: Deep research and discovery before building something new
argument-hint: "[focused: 1 question | wide: landscape | deep: full build plan] [topic]"
---

Load the `deep-research` skill.

Parse $ARGUMENTS for depth and topic:

| Depth | What it means | Use when |
|-------|--------------|----------|
| `focused` | Answer one specific question. Quick comparison, 1-page recommendation. | "Should I use X or Y?" |
| `wide` | Understand the whole landscape. Competitors, ecosystem, architecture options. Enough to write a spec. | "What's out there for [category]?" |
| `deep` | Leave no stone unturned. Everything in wide + libraries, plugins, GitHub issues, forums, future-casting. Enough to drive weeks of coding. | "Plan a major build from scratch" |

Default: `wide`

Examples: `/deep-research deep obsidian replacement on cloudflare`, `/deep-research focused codemirror vs prosemirror`, `/deep-research wide knowledge management tools`
