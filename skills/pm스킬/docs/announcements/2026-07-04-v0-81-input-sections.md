# v0.81 — Every Skill Now Declares Its Inputs (and Why We Don't Use `$ARGUMENTS`)

**July 4, 2026**

This release started with a fair question: other skill libraries have `INPUTS` sections and `$ARGUMENTS` templating — are we doing our users a disservice without them?

Half yes, half no. The gap was real: none of our skills told you what context to bring, or what happens to context you supply up front. The fix other libraries use, though, is the wrong fix for this library — and understanding why is the interesting part.

## What changed in v0.81

- **Every skill now has a required `## Input` section** — all 55 of them, plus the validator, authoring wizard, templates, and contributor docs. Each one says, in plain language, what the skill works best with, what else sharpens the output, and — critically — what happens when you arrive with nothing.
- **Inline input is now honored everywhere.** Every Input section carries the same rule: anything you supply with the invocation — text after the skill name, a pasted context dump — counts as answers already given. The skill uses it and skips what it covers instead of re-asking. Give `discovery-interview-prep` your goal and constraints up front, and it opens at the first question you *haven't* answered.
- **Invitation, not gate.** No Input section labels anything "Required." Each ends with "Arriving empty-handed? That works too" and says what the guided flow does instead. The whole point of interactive skills is that you can show up with a half-formed thought and be walked to a sharp one — the Input section now says so explicitly.
- **`argument-hint` frontmatter added to 53 skills** — Claude Code users get autocomplete hints like `/user-story [feature or user need]`; every other runtime ignores the field harmlessly.
- **The `$ARGUMENTS` decision is now documented and enforced.** CONTRIBUTING.md gains a "Why We Don't Use `$ARGUMENTS`" section, and `check-skill-metadata.py` now fails any skill body containing bare `$ARGUMENTS`. Smoke checks warn when an Input section lacks an example invocation or the empty-handed fallback.
- **Streamlit playground: "What to bring" pre-flight.** Every skill detail page now renders the skill's own Input section in an expander before you start — labeled "all optional" so the pedagogy survives the UI.
- **New example flow:** `workshop-facilitation/examples/inline-input-flow.md` shows a full transcript of inline input skipping answered questions — including honest progress labels (`Context Q2/6` when Q1 came in with the invocation) and the re-asking anti-pattern to avoid.
- **Restored a lost skill: `agent-orchestration-advisor`.** The pre-release audit for v0.81 caught that this Phase 6 interactive skill — 759 lines on designing multi-agent workflows, referenced by the README and CLAUDE.md since February — only ever existed on an orphaned commit that never made it to main. Recovered from git history, upgraded to current standards (trigger-oriented description, `intent`, theme metadata, and of course an Input section), and finally shipped. Library count: 55 skills.

## Why we don't use `$ARGUMENTS`

`$ARGUMENTS` is Claude Code's input substitution: invoke `/skill-name some text` and the token expands before the model sees it. Other libraries build their skills around it. We deliberately don't, for three reasons:

1. **Portability.** The substitution only happens in Claude Code. In the Claude Desktop/Web packs, Codex, and the Streamlit playground, `$ARGUMENTS` renders as literal, unexplained template syntax — broken scaffolding in front of the reader.
2. **Pedagogy.** These skills teach human PMs as much as they instruct agents. A plain-language Input section shows you what a well-formed request looks like — and tells you that you can arrive with nothing and be guided through it. `$ARGUMENTS` teaches you nothing.
3. **It's unnecessary.** Claude Code already appends your typed arguments to the skill content. A skill that says "treat inline input as answers already given" gets the same behavior on every runtime, without the syntax.

This is the same species of decision as v0.75's pedagogic-first stance: the convenient shortcut optimizes for one runtime and one audience, and this library serves several of each. So the convention is named, documented, and — this time from day one — machine-enforced, so it can't erode one well-meaning PR at a time.

## For contributors

New skills fail validation without an `## Input` section between Purpose and Key Concepts. The section template lives in CONTRIBUTING.md; the short version: works-best-with, also-useful, the inline-input rule, the empty-handed fallback, and an example invocation. Frame it as an invitation, not a gate — and skip the template syntax.
