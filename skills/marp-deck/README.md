# Presentation Skills for Claude Code

A collection of [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills for creating presentations. Each skill teaches Claude a specialized workflow — complete with visual QA, iteration loops, and format-specific best practices.

## How it works

Skills are markdown files that extend Claude Code's capabilities. When installed, Claude reads the skill's instructions and follows its workflow automatically. Skills follow the [Agent Skills](https://agentskills.io) spec and are compatible with any tool that supports it.

The key innovation in these skills is the **visual feedback loop**: Claude generates presentation markdown, renders it to images, then uses its vision capability to inspect each slide — catching layout issues, text overflow, and contrast problems that would be invisible from markdown alone.

## Skills

| Skill | Description | Status |
|-------|-------------|--------|
| [marp-deck](skills/marp-deck/) | Create polished Marp presentations with iterative visual QA | Stable |

## Installation

1. Clone this repo (or copy the skill folder you want):
   ```bash
   git clone https://github.com/anthropics/presentation-skills.git
   ```

2. Add the skill to your project's `.claude/skills/` directory, or install it globally:
   ```bash
   # Project-level (recommended)
   cp -r skills/marp-deck /your-project/.claude/skills/marp-deck

   # Or symlink it
   ln -s /path/to/presentation-skills/skills/marp-deck /your-project/.claude/skills/marp-deck
   ```

3. Claude Code will automatically discover and use the skill when relevant.

## Creating a skill

Want to contribute a new presentation skill? Use the [template](template/SKILL.md) as a starting point.

A good presentation skill should:
- Define a clear, repeatable workflow
- Include a visual QA step (export to images, inspect with vision)
- Ship with a reference doc and a starter template in `examples/`
- Handle common failure modes with explicit guidance

See the [Agent Skills spec](https://agentskills.io) for the full format reference.

## License

[Apache 2.0](LICENSE)
