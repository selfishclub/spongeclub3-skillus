# Context Bricks

Git-aware statusline for Claude Code CLI with context brick visualisation.

## Install

```bash
npx contextbricks init
```

Requires Node.js (already installed with Claude Code) and `git`.

## What It Shows

3-line display:

```
[Opus 4.6:expl] my-project:main *↑1 | @my-agent | wt
[abc1234] Fix auth redirect loop | +12/-3
[■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□] 30% | 140k free | 0h 12m | $1.50
```

| Line | Content |
|------|---------|
| 1 | Model, output style, repo:branch, git status, agent name, worktree |
| 2 | Latest commit hash + message, lines changed |
| 3 | Context brick bar, percentage, free tokens, duration, cost |

### Indicators

| Indicator | Meaning |
|-----------|---------|
| `*` | Uncommitted changes |
| `↑2` | 2 commits ahead of remote |
| `↓1` | 1 commit behind remote |
| `@agent-name` | Running with `claude --agent` |
| `wt` | Inside a git worktree |
| `:expl` | Output style (explanatory, concise, verbose) |
| `73%!` | Context exceeds 200k tokens (extended context) |

## Manual Install

```bash
cp scripts/statusline.js ~/.claude/statusline.js
```

Add to `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "node ~/.claude/statusline.js",
    "padding": 0
  }
}
```

Restart Claude Code.

## Uninstall

```bash
contextbricks uninstall
```

## License

MIT
