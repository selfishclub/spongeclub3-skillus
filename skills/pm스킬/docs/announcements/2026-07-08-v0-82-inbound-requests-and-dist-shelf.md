# v0.82 — Inbound-Request Triage and a Browsable Download Shelf

**July 8, 2026**

Two moves in one release: a new skill for the messages that land in your lap, and a much easier way for anyone — including PMs who never open a terminal — to get the whole library.

## What changed in v0.82

- **New skill: `incoming-request-advisor`** (Interactive, `theme: stakeholder-comms`). Drop in an incoming message — a Slack ping, an email, a mandate, an escalation, an FYI, as text or a screenshot — and get a chief-of-staff-grade read on it. It:
  - separates the **literal ask** from the **job-to-be-done** underneath it,
  - reads sender **power and stake** (upstream, peer, or downstream),
  - distinguishes **success criteria** (how they'll judge it) from **must-haves** (what goes in the deliverable) — a distinction PMs routinely blur,
  - marks every guess as an inference and surfaces it for you to validate,
  - scales depth to the message (a one-line ping doesn't get twelve dense sections),
  - and opens toward a reply, an agenda, a discovery reframe, or an outcome-protecting counter-proposal.

  It ships with a copy/paste `template.md` so you can run the breakdown by hand for your own prep, and a worked `examples/conversation-flow.md`. Distilled from Dean's "Incoming Request Breakdown" prompt in the [product-manager-prompts](https://github.com/deanpeters/product-manager-prompts) repo.

- **`dist/` is now a committed, browsable download shelf.** Navigate to [`github.com/deanpeters/Product-Manager-Skills/tree/main/dist`](https://github.com/deanpeters/Product-Manager-Skills/tree/main/dist) and you get:
  - a plain-language `README.md` that renders right there on GitHub — pick a pack or a skill, unzip, upload to Claude, done,
  - a `CATALOG.md` listing all 56 skills by category with descriptions and direct download links,
  - all **56 individual skill ZIPs** flat in the folder, and
  - a `packages/` subfolder with the curated bundles (starter, discovery, strategy, delivery, AI PM, all-skills) plus the Codex package.

  No terminal. No hunting through the Releases tab. `README.md` and `CATALOG.md` are **generated from `skills/`** by `scripts/build-dist.sh`, so they never drift from the source; the intermediate build directories stay git-ignored. GitHub Releases still exist and are still built on version tags — the committed shelf is a complement, not a replacement.

- **Library is now 56 skills** — 23 Component, 26 Interactive, 7 Workflow.

## Why the download shelf

The mission of this library is to make PMs more awesome and to send the ladder down — including to PMs who aren't developers. Publishing the ZIPs only as tagged release assets quietly worked against that: it asked a non-technical PM to understand GitHub Releases before they could download a skill. A folder you can click into, with a README that explains itself, meets people where they are. Easy and educational is the whole point.

## Upgrading

- **Claude Desktop / Web:** grab a pack from [`dist/packages/`](https://github.com/deanpeters/Product-Manager-Skills/tree/main/dist/packages) or an individual skill from [`dist/`](https://github.com/deanpeters/Product-Manager-Skills/tree/main/dist), unzip, and upload.
- **Claude Code (plugin marketplace):** the marketplace manifest already lists `incoming-request-advisor`; update the plugin to pull it.
- **Codex:** re-download `pm-skills-codex.zip` from `dist/packages/`.

## References

- Skill: [`skills/incoming-request-advisor/SKILL.md`](../../skills/incoming-request-advisor/SKILL.md)
- Distribution policy: [`docs/RELEASE-PACKAGING.md`](../RELEASE-PACKAGING.md)
- Source prompt: `incoming-request-breakdown.md` in [product-manager-prompts](https://github.com/deanpeters/product-manager-prompts)
