# Skill Shape

How to write a `SKILL.md` Claude reads as a contract — goal, process, success — not as a tutorial.

This doc applies the [Agent Skills specification](https://agentskills.io/specification), [agentskills.io best practices](https://agentskills.io/skill-creation/best-practices), and [Anthropic's `skill-creator`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) to this repo's conventions. The spec is the authority; this doc is the editorial layer.

## Principles

These do most of the work. Section templates and patterns below are just servants of the principles.

### Spend context wisely

Once a skill activates, its full body loads into Claude's context window. Every line competes with conversation history, system prompt, and other active skills. Ask of each sentence: *would Claude get this wrong without it?* If no, cut.

Don't restate what Claude already knows. Don't explain what a PDF is, what HTTP does, what a database migration is. Focus on what's project-specific: our APIs, our conventions, our gotchas, our defaults.

### Favor procedures over declarations

A skill teaches *how to approach a class of problems*, not *what to produce for one instance*. The reusable method outlasts the specific answer.

```markdown
<!-- Specific answer — only useful for this exact task -->
Join `orders` to `customers` on `customer_id`, filter `region = 'EMEA'`, sum `amount`.

<!-- Reusable method — works for any analytical query -->
1. Read the schema from `references/schema.yaml`
2. Join tables using the `_id` foreign key convention
3. Apply filters from the user's request as WHERE clauses
4. Aggregate as needed; format as a markdown table
```

Specific details (output templates, named constraints) still earn their place. The *approach* must generalise.

### Match specificity to fragility

Not every part of a skill needs the same prescription level. Calibrate per section.

- **Give Claude freedom** when multiple approaches are valid and the task tolerates variation. Explain *why*; let Claude make context-dependent calls.
- **Be prescriptive** when operations are fragile, order matters, or consistency is required. Name exact commands, exact sequences, exact flags.

Most skills mix both. A code review skill: prescriptive about *what to look for*, loose about *how to phrase the review*. A migration skill: prescriptive about *the exact command sequence*, loose about *how to summarise the result*.

### Provide defaults, not menus

When multiple tools or approaches could work, pick a default and mention alternatives briefly.

```markdown
<!-- Too many options -->
You can use pypdf, pdfplumber, PyMuPDF, or pdf2image...

<!-- Default with escape hatch -->
Use `pdfplumber` for text. For scanned PDFs requiring OCR, use `pdf2image` with `pytesseract`.
```

A menu of equal options leaves Claude to choose; usually the choice doesn't matter and the deliberation is overhead.

### Explain why, drop musty MUSTs

A skill that says *"you MUST use library X"* dates fast and doesn't help Claude reason about edge cases. A skill that says *"use library X because it handles unicode-encoded PDFs that the alternatives mangle"* lets Claude carry the principle to situations the skill didn't anticipate.

Reserve hard MUSTs for genuine constraints (security, fragility, contract). Everywhere else, explain.

### Start from real expertise

The 3-instance rule: write the skill the third time you run the procedure, not before. Earlier than that, you don't know what the recognition signals are, where the trips are, or which steps need prescription.

Sources of real expertise:

- A real task you ran with corrections from the user along the way
- Your team's existing runbooks, incident reports, code-review comments, fix patterns
- Version control history — what actually changed when this broke before

Generic best-practices articles produce generic skills. Project-specific material produces skills that earn their place.

### Refine with real execution

The first draft is a draft. Run it on a real task, read the trace (not just the output), and revise. Common signals:

- Claude tries several approaches before finding one that works → instructions were too vague
- Claude follows an instruction that didn't apply → the skill conflates separate cases
- Claude waste time on unproductive steps → the skill suggests too many options without a default

A single execute-then-revise cycle visibly lifts quality. Complex skills benefit from several.

## The `description` field — make it pushy

The `description` is the only field Claude reads before deciding to activate. Claude tends to *under-trigger* skills, so descriptions should be *pushy*, not neutral.

```yaml
# Too neutral — Claude may skip when relevant
description: How to build internal data dashboards.

# Pushy — fires on relevant intents even when user doesn't say "dashboard"
description: How to build internal data dashboards. Use whenever the user mentions dashboards, data visualization, internal metrics, KPIs, or wants to display company data — even if they don't explicitly say "dashboard".
```

Lead with what the skill does + when to use it. Include trigger phrases real users would type. Max 1024 chars.

For an existing description that under-triggers, see [Anthropic's skill-description optimizer](https://github.com/anthropics/skills/tree/main/skills/skill-creator) for a systematic improvement procedure.

## Body — no required structure

The spec is explicit: *"There are no format restrictions. Write whatever helps agents perform the task effectively."* Don't follow a section template just because one exists.

Most working skills in this repo land on something like:

- A short blurb under the title (1–2 sentences — what the skill is for)
- Step-by-step instructions in imperative form
- Examples of inputs and outputs
- Common edge cases (often as a "Gotchas" section)
- Verification — what success looks like

Pick the sections that earn their place. Don't add empty `## Failure modes` or `## When NOT to invoke` headings if the content isn't there.

## High-value patterns

These are reusable techniques from agentskills.io — use the ones that fit.

### Gotchas section

Often the highest-value content in a skill. *Concrete corrections to mistakes Claude will make without being told.* Not general advice — specific facts that defy reasonable assumptions.

```markdown
## Gotchas

- The `users` table uses soft deletes. Queries must include `WHERE deleted_at IS NULL` or results will include deactivated accounts.
- User ID is `user_id` in the database, `uid` in auth, `accountId` in billing. All three refer to the same value.
- `/health` returns 200 as long as the web server runs, even if the database is down. Use `/ready` for full service health.
```

When you correct Claude during a session, add the correction to gotchas. Most direct route to skill improvement.

### Templates for output format

When Claude needs to produce output in a specific shape, give a template inline. More reliable than describing the format in prose.

```markdown
## Report structure

Use this template:

# [Analysis Title]

## Executive summary
[One paragraph]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data

## Recommendations
1. Specific actionable recommendation
```

Short templates inline. Longer ones in `assets/` referenced from `SKILL.md`.

### Checklists for multi-step workflows

```markdown
## Form processing workflow

- [ ] Step 1: Analyze the form (`scripts/analyze_form.py`)
- [ ] Step 2: Create field mapping (edit `fields.json`)
- [ ] Step 3: Validate mapping (`scripts/validate_fields.py`)
- [ ] Step 4: Fill the form (`scripts/fill_form.py`)
- [ ] Step 5: Verify output (`scripts/verify_output.py`)
```

### Validation loops

Instruct Claude to verify its own work before moving on.

```markdown
## Editing workflow

1. Make your edits
2. Run validation: `python scripts/validate.py output/`
3. If validation fails: review the error, fix the issues, re-run
4. Only proceed when validation passes
```

### Plan-validate-execute

For batch or destructive operations: create an intermediate plan, validate against a source of truth, only then execute. The validator's error messages are what let Claude self-correct.

### Bundled scripts

If you notice Claude reinventing the same logic across runs (parsing a format, building a chart, validating output), write the script once and bundle it in `scripts/`. Tested, deterministic, no per-run drift.

## Length and progressive disclosure

The spec recommends keeping `SKILL.md` under 500 lines and 5,000 tokens. Not a hard limit — *"feel free to go longer if needed"* per Anthropic's skill-creator — but a real signal. Over 500 usually means the skill carries content that should be in `references/`, `assets/`, or `scripts/`.

This repo's own rule (in `CLAUDE.md`): *"a working skill that's 800 lines beats a broken skill that's 300 lines with critical content in references the agent never reads."* That's right. Reconciliation:

- **Inline** everything Claude needs *every run* — workflow steps, commands, scripts, mapping tables, gotchas
- **Externalise** content that's variant-specific or rarely needed — with an **explicit load trigger**: *"read `references/aws-variant.md` if deploying to AWS"*, not *"see references/ for details"*

The vague trigger is the failure mode. A specific trigger names *when* to load and *what to use it for*; a vague trigger competes with "do the task" and loses.

For multi-domain skills, the canonical structure is workflow-in-`SKILL.md` + per-variant-in-`references/`:

```
cloud-deploy/
├── SKILL.md            # workflow + variant selection logic
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

## Multi-file layout

```
plugins/<plugin>/skills/<skill-name>/
  SKILL.md            # always
  ERRATA.md           # versioned corrections (this repo's convention)
  scripts/            # executable helpers Claude RUNS (doesn't always read)
  references/         # variant/optional docs loaded on demand
  assets/             # templates/data copied into user projects
```

Reference companion files from `SKILL.md` by relative path: `see ./references/aws-variant.md`. Earned-place rule: don't pre-create empty folders or stub files.

## When to retire a skill

Most skill rot is invisible — a skill nobody fires anymore is also a skill nobody updates, but it still ships in the marketplace and competes for activation. Retire when:

- The pattern is now common knowledge in Claude's training (an older guide that was useful in 2024 may now be redundant)
- The library/tool the skill teaches has been replaced or deprecated
- The skill has been split into two more-focused skills (retire the parent)
- It has not been invoked or updated in 6+ months and you can't think of when you'd reach for it

Retirement options:

- **Archive in git** — delete from the active tree, tag the last commit, note the tag in the repo's README history section (this repo did this for v1's 105 skills → `v1-final` tag)
- **Roll into another skill** — if the content is still useful but doesn't earn standalone activation
- **Replace** — write a new tighter version, retire the old one in the same commit

Don't agonise. Retirement is reversible (git history); a stale skill in the marketplace isn't free.

## Authoring checklist

After drafting, before relying on the skill:

- [ ] Frontmatter `name` is kebab-case ≤64 chars
- [ ] `description` is ≤1024 chars, leads with trigger phrases, is *pushy* about when to fire
- [ ] Body is in imperative form
- [ ] A reader cold could execute the procedure without asking; *and* the procedure generalises beyond the example
- [ ] Critical-path content is inline; only variant/optional content is in `references/` with a specific load trigger
- [ ] No marketing language (*comprehensive*, *robust*, *world-class*), no restated universal patterns, no duplicate code blocks
- [ ] Run the skill once on a real task; revise based on the trace (not just the output)
- [ ] If applicable, `## Gotchas` captures the corrections you made during the real run

If any are missing, the skill is in draft state. Finish before listing it in the marketplace.

## Trimming an existing skill

Most skills in this repo predate this guide. Audit pass:

1. **Description.** Does it lead with trigger phrases? Is it pushy? Rewrite if not.
2. **Body.** For each paragraph, ask: *does this change what Claude does?* If no, cut.
3. **Section sprawl.** Empty headings, restated universals, duplicated code blocks → cut or merge.
4. **`references/`.** Does anything load-bearing live there? Inline it. Are load triggers specific? Rewrite vague ones.
5. **Length sanity.** If still over ~500 lines, push variant/optional content into `references/` with explicit triggers.
6. **Verification section.** Name concrete artefacts: *"deployment succeeds"* → *"`wrangler deploy` exits 0 and `curl <prod-url>` returns 200"*.
7. **Run it once.** Read the trace. Revise what was unclear.

One commit per skill if sweeping the repo. Each diff legible standalone.

## See also

- [`CLAUDE.md`](CLAUDE.md) — repo conventions, plugin anatomy, frontmatter validation, quality bar
- [`README.md`](README.md) — public-facing overview, plugin list
- [Agent Skills specification](https://agentskills.io/specification) — authoritative spec
- [agentskills.io best practices](https://agentskills.io/skill-creation/best-practices) — patterns and principles this doc applies
- [Anthropic's `skill-creator`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) — canonical skill-authoring skill, with the eval/iterate loop
- [Anthropic's `skills` repo](https://github.com/anthropics/skills) — reference implementations across many domains

## Last updated

2026-05-13 — initial. Applies the Agent Skills spec + agentskills.io best-practices + Anthropic's skill-creator practice to this repo's conventions. Replaces an earlier draft that over-prescribed a fixed section order without authority behind it.
