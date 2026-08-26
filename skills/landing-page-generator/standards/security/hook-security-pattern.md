# Hook-Enforced Security Pattern

**Status:** Active
**Scope:** Repository-wide Claude Code sessions

This standard describes the hook-layer defenses shipped under `.claude/hooks/` and how to extend them safely.

## Why hooks (and not just prompt rules)

Prompt-level guidance asking the model to "never paste secrets" can be ignored, paraphrased, or routed around. Hook-layer defenses run deterministically outside the model — they cannot be argued with, distracted, or socially engineered. A hook that exits non-zero blocks the tool call regardless of what the conversation looked like.

This repository uses hooks for two narrowly-scoped jobs:

1. **Secret scanning at the Bash boundary** — prevent obvious credential leaks before they hit the shell.
2. **Registry freshness check at session start** — surface a one-line notice when `registry.json` is out of date relative to the skill files, so contributors regenerate it.

Both run on stdlib Python — no dependencies, no network calls, fail-open on errors so they cannot brick a session.

## Files

| Path | Trigger | Purpose |
|------|---------|---------|
| `.claude/settings.json` | — | Registers both hooks for every session that opens this repo |
| `.claude/hooks/pre_tool_secret_scan.py` | `PreToolUse` on `Bash` | Reads the proposed command, blocks if it matches an AWS / GitHub / Slack / Anthropic / OpenAI key pattern, an inline PEM private key, or a `.env` write of a secret-bearing env var |
| `.claude/hooks/session_start_skill_check.py` | `SessionStart` | Compares `registry.json` `generated_at` against the newest `SKILL.md` mtime; prints a one-line stale-registry notice if behind |

## Threat model

**In scope (the secret scanner blocks):**
- `aws configure set aws_access_key_id AKIA…`
- `curl -H "Authorization: token ghp_…"`
- `echo $API_TOKEN >> .env`
- Inline private keys (`-----BEGIN … PRIVATE KEY-----`)
- Anthropic (`sk-ant-`) / OpenAI (`sk-`) inline keys

**Out of scope (this hook is intentionally conservative):**
- Secrets read from already-existing files (`.env`, vaults, password managers) — the hook only catches inline literals
- Detection-evasion patterns (base64-encoded secrets, split string concatenation)
- Network-layer exfiltration (the hook does not parse outbound URLs)
- Repo-wide secret scanning (use `engineering/skill-security-auditor` or `gitleaks` for that)

The goal is **make the obvious accidents impossible**, not to be a comprehensive DLP system.

## Extending the secret scanner

To add a pattern:

1. Edit `.claude/hooks/pre_tool_secret_scan.py` and append to `SECRET_PATTERNS`:
   ```python
   (re.compile(r"\bsk_live_[A-Za-z0-9]{24,}\b"), "Stripe live secret key"),
   ```
2. Add a `tests/` smoke case if you want CI coverage (write a JSON payload that should match, pipe into the script, assert exit code 2).
3. Bias toward **false negatives** over false positives — a hook that fires on every other command will be disabled by users and protect nothing.

## Disabling the hooks

Hooks are configured in the **committed** `.claude/settings.json` so they apply to every contributor's session. To disable temporarily:

- Edit `.claude/settings.local.json` (gitignored) and override with an empty hooks block.
- Or rename `.claude/settings.json` for one session.

Permanent removal requires a PR — these defenses are part of the repo's contract.

## When a hook fires

If the secret-scan hook blocks a command you believe is legitimate (e.g. revoking a known-leaked key as part of an incident response):

1. Run the command outside Claude.
2. Open a PR documenting the case in this file so we can refine the pattern.

Never bypass a hook by mutating the command to evade the pattern — that defeats the purpose and trains a habit that will eventually leak a real secret.
