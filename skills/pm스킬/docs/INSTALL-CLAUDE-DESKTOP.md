# Install PM Skills in Claude Desktop or Claude Web

Claude Desktop and Claude Web are the easiest path for nontechnical PMs: download one pack, unzip it, upload the skill ZIPs inside, and start working.

## Quick Setup

1. Open the [Product Manager Skills Releases page](https://github.com/deanpeters/Product-Manager-Skills/releases/latest).
2. Download [`pm-skills-starter-pack.zip`](https://github.com/deanpeters/Product-Manager-Skills/releases/latest/download/pm-skills-starter-pack.zip), or choose a different pack from the table below.
3. Unzip the pack on your computer.
4. Open Claude.
5. Go to `Settings -> Capabilities -> Skills`.
6. Upload the individual skill ZIPs inside the pack.
7. Start a new chat and ask Claude to use the Product Manager Skills.

Try:

```text
Use the Product Manager Skills to help me frame this product problem.
```

## Which Pack Should I Choose?

| Pack | Best for | Use when |
|---|---|---|
| [`pm-skills-starter-pack.zip`](https://github.com/deanpeters/Product-Manager-Skills/releases/latest/download/pm-skills-starter-pack.zip) | Most PMs | You want a small, practical starter set. |
| [`02-discovery-pack.zip`](https://github.com/deanpeters/Product-Manager-Skills/releases/latest/download/02-discovery-pack.zip) | Discovery work | You need to understand customers, problems, jobs, or opportunities. |
| [`03-strategy-pack.zip`](https://github.com/deanpeters/Product-Manager-Skills/releases/latest/download/03-strategy-pack.zip) | Strategy work | You need positioning, market thinking, or product direction. |
| [`04-delivery-pack.zip`](https://github.com/deanpeters/Product-Manager-Skills/releases/latest/download/04-delivery-pack.zip) | Delivery work | You need stories, epics, PRDs, or roadmap execution. |
| [`05-ai-pm-pack.zip`](https://github.com/deanpeters/Product-Manager-Skills/releases/latest/download/05-ai-pm-pack.zip) | AI product work | You need to evaluate AI-shaped opportunities and risks. |
| [`99-all-skills-pack.zip`](https://github.com/deanpeters/Product-Manager-Skills/releases/latest/download/99-all-skills-pack.zip) | Advanced users | You want everything and can tolerate a larger skill list. |

## A Good First Prompt

```text
Use the Product Manager Skills. Ask me the minimum useful questions, then help me turn this rough idea into a clear problem statement.
```

## Notes

- Start with the starter pack unless you know you need a specific pack.
- Do not upload the outer pack ZIP to Claude. Unzip the pack first, then upload the skill ZIPs inside it.
- Use one practical problem from your work. These skills are strongest with real context.
- Claude Code users should usually use the plugin marketplace instead of these ZIPs. See [`INSTALL-CLAUDE-CODE.md`](INSTALL-CLAUDE-CODE.md).
- Codex users should use the Codex ZIP or clone the repo. See [`INSTALL-CODEX.md`](INSTALL-CODEX.md).
