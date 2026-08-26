# v0.79 — Community Contributions: Thank You

**Released:** May 15, 2026

---

## What Happened

This release belongs to the community.

Since v0.78, four contributors showed up with fixes and additions that made the repo meaningfully better — without being asked. This note is a record of what they did and why it matters.

---

## The Contributions

### `pm-skill-creator` — [@KNE-AI](https://github.com/KNE-AI)

A new interactive skill that walks you through designing a repo-compliant skill from scratch via guided conversation. Five adaptive questions take you from raw idea or content to a complete `SKILL.md` draft — covering material type, skill type decision, naming, key content, and failure modes.

This is meta-tooling: a skill about building skills. It complements `skill-authoring-workflow` (which defines the process and validation gates) with a design partner that helps you figure out what to build before you build it.

The skill is at `skills/pm-skill-creator/SKILL.md`.

---

### Security hardening in `run-pm.sh` and `add-a-skill.sh` — [@xiaolai](https://github.com/xiaolai)

xiaolai ran a full automated security audit of the repo and submitted two targeted fixes:

**`run-pm.sh` — configurable input length guard**

User-supplied CLI input was passed to `claude` and `codex` without a length check. The fix adds a guard that rejects inputs over a configurable character limit. We took the code and adjusted one thing: instead of hard-coding the limit at 2000 characters, it is now set via the `PM_MAX_INPUT` environment variable with a default of 4000. Override it for longer prompts:

```bash
PM_MAX_INPUT=8000 ./scripts/run-pm.sh skill prd-development "..."
```

**`add-a-skill.sh` — adapter name validation and path traversal protection**

The script dynamically sources adapter files based on user-supplied names. Without validation, a crafted `--agent` argument could traverse outside the adapters directory and source an arbitrary file. The fix adds a two-layer guard: a character allowlist that rejects names with unsafe characters, and a `realpath` check that confirms the resolved path stays inside `ADAPTERS_DIR` regardless of what the name looks like.

Both fixes are minimal, non-breaking changes to local developer tooling. No skill content was touched.

---

### Missing `plugin.json` manifest — [@changyan01](https://github.com/changyan01) and [@harley-chenhailin](https://github.com/harley-chenhailin)

changyan01 filed a bug report: Claude Code users were seeing skills fail to load. harley-chenhailin followed up with a precise technical diagnosis.

The root cause: Claude Code's plugin loader requires a `.claude-plugin/plugin.json` manifest to register the plugin and discover skills. We had `.claude-plugin/marketplace.json` (which serves a different purpose — catalog listing for the marketplace) but not `plugin.json`. Skills were already at the correct path (`skills/*/SKILL.md`); the manifest was the only missing piece.

The fix is a single file: `.claude-plugin/plugin.json`. This was a real bug affecting real users. It would not have been caught without someone actually installing the plugin and reporting what broke.

---

## Why This Release Exists

Most of what goes into open source repos is invisible: the people who notice something wrong, take the time to document it precisely, and show up with a solution. That work is easy to absorb quietly and move on.

This release names the contributors explicitly because the work deserves to be named.

If you use PM Skills and notice something broken, confusing, or missing — the contribution path is open. See [`CONTRIBUTING.md`](../../CONTRIBUTING.md) and [`docs/Building PM Skills.md`](../Building%20PM%20Skills.md).

---

## What Changed in the Repo

- Added `skills/pm-skill-creator/SKILL.md` — interactive skill for guided skill design
- Added `.claude-plugin/plugin.json` — required plugin manifest for Claude Code skill discovery
- Updated `scripts/run-pm.sh` — configurable input length guard via `PM_MAX_INPUT` (default 4000)
- Updated `scripts/add-a-skill.sh` — adapter name allowlist and path traversal protection via `validate_adapter()`

---

## Plain-English Blurb

Product Manager Skills v0.79 is a community release.

Four contributors fixed a skill-discovery bug that was silently breaking Claude Code installs, hardened two developer scripts against security edge cases, and added a new interactive skill for designing skills through guided conversation.

This release names them and thanks them. That's the whole point.

---

*Release authored by Dean Peters with Claude Code.*
