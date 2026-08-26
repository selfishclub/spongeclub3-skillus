# Adornment Plan 4 — Back-Catalog Backfill

**Status:** Approved Aug 10, 2026. Not started.
**Predecessor:** `docs/maintenance/2026-07-17-adornment-and-docs-plan.md` (Plans 1-3, shipped)

Bring the back catalog up to the "fully adorned" standard in CLAUDE.md: every Component and
Workflow skill ships a `template.md` and worked examples from **two business domains**.

---

## The measured gap

The earlier brief said "~30 back-catalog skills." Measured Aug 10 against the actual repo, it is
**28 skills in two groups needing different work.**

### Group A — missing files outright (7)

| Skill | Missing |
|---|---|
| `altitude-horizon-framework` | `template.md` |
| `company-intel` | `template.md` |
| `executive-onboarding-playbook` | `template.md` |
| `finance-metrics-quickref` | `template.md` + `examples/` |
| `skill-authoring-workflow` | `template.md` + `examples/` |
| `stakeholder-identification` | `template.md` + `examples/` |
| `stakeholder-mapping` | `template.md` + `examples/` |

### Group B — single-domain examples (21)

`user-story` · `problem-statement` · `positioning-statement` · `proto-persona` · `press-release` ·
`epic-hypothesis` · `storyboard` · `jobs-to-be-done` · `pol-probe` · `pestel-analysis` ·
`recommendation-canvas` · `company-research` · `user-story-mapping` · `user-story-splitting` ·
`product-sense-interview-answer` · `altitude-horizon-framework` · `discovery-process` ·
`prd-development` · `roadmap-planning` · `product-strategy-session` · `executive-onboarding-playbook`

**Group B is the more valuable half.** These are the most-used skills in the library, and each one
currently teaches "this is a SaaS technique" by omission.

---

## Carve-outs

Three skills are exempt from the dual-domain half. Forcing a second domain would produce a worse
artifact, not a better one — the standard already allows this.

| Skill | Why | Still needs |
|---|---|---|
| `finance-metrics-quickref` | Definitionally SaaS metrics | `template.md` only |
| `skill-authoring-workflow` | Meta-skill about this repo; a "second domain" would be artificial | `template.md` + one example |
| `product-sense-interview-answer` | The domain *is* the interview | A second example varying **question type**, not industry |

---

## The three universes

Two exist and are in use. The third is approved here with a **scoped job** — it is not a general
fallback.

### 1. Fieldlight — B2B SaaS (field service management)

Fast-cycle software, direct sales, annual contracts, no regulatory surface. Products: Classic
Dispatch (retired in the EOL suite), Next Scheduling, Invoicing, Parts, SMS Alerts.
**Use for:** the default SaaS half of any pairing.

### 2. Northfield Automation — industrial (retrofit control systems)

Capital equipment, 8 channel partners, service contracts, UL/CE certification, spare parts,
multi-year horizons. Products: NFA-200 (at End of Sale), NFA-500, SmartLink gateway. Investigates
Helix / Corvid / Meridian in the market-intel suite.
**Use for:** the non-SaaS half — hardware, channel, long cycles, physical constraints.

### 3. Brightwater Biologics — life sciences (clinical trial operations) — NEW

Already in canon as a name in `company-intel` from the July 16 fictionalization pass. Now given a
charter.

**Who they are:** a clinical-stage biotech running multi-site trials. Its internal product team
builds and operates **Trialpath**, the platform used by study coordinators, CRA monitors, and CRO
partners to run those trials.

That split gives the universe two registers:

- **Product artifacts** (`user-story`, `prd-development`, `proto-persona`) → Trialpath's users:
  study coordinators, monitors, site staff
- **Strategy and evidence skills** (`pestel-analysis`, `product-strategy-session`,
  `company-research`) → the trial program itself, its regulatory environment, and reimbursement

**Its distinct job — the reason it exists:** *evidence before revenue.* Proving something works
before anyone pays, selling to a payer who is not the user, and horizons measured in years. This is
the axis neither other universe has.

**What it must NOT become:** "the regulated one." Northfield already carries UL/CE, validated
processes, and change-control documentation. If Brightwater is only "regulated," it is a second
flavor of an existing axis and does not earn its place.

#### Anonymization guardrail — read before writing any Brightwater example

This is the **highest-risk domain in the repo.** Real client work sits in life sciences, so the
customer-anonymization protocol needs *more* care here, not equal care.

**Positive constraint: stay inside clinical trial operations.** Trial site management, protocol
amendments, patient recruitment, monitoring workflows, study close-out. That corner was chosen
deliberately, and staying in it is what keeps examples clear of anything drawn from real
engagements.

**Do not build an example by adapting the shape of a source document** — not the subject matter,
not the section structure, not the scenario. Invent the situation from the framework being taught,
then check it reads as fiction.

Per the anonymization protocol, the specific out-of-bounds topics are **not enumerated here**. A
denylist in a public repo points at the very thing it excludes. Session memory holds the detail;
if you are unsure whether a scenario is too close, ask rather than guess.

---

## When to use which domain

| Skill type | Domain pairing |
|---|---|
| Core artifacts — `user-story`, `problem-statement`, `proto-persona`, `press-release`, `storyboard` | Fieldlight + Northfield. **Keep the second domain instantly legible** — these are the highest-traffic skills, and a domain requiring vocabulary setup competes with the lesson |
| Regulated / evidence / long-cycle is the lesson — `pestel-analysis`, `discovery-process`, `product-strategy-session`, `company-research`, `recommendation-canvas` | Fieldlight + **Brightwater** |
| Hardware, channel, supply chain is the lesson | Fieldlight + Northfield |
| Career and leadership skills | Domain-light; vary the **company stage and org shape** rather than the industry |

If Fieldlight and Northfield both contort and the lesson is not about evidence or regulation, reach
for a low-context neutral setting (municipal services, school operations, logistics) rather than
forcing a universe. Legibility beats continuity for core artifacts.

---

## Sequencing — four waves

Land each wave as its own reviewable commit. Nothing here is validator-enforced — "fully adorned"
is a quality bar in CLAUDE.md, not a rule in `check-skill-metadata.py` (a deliberate v0.83
decision, worth keeping) — so **the checklist is the only guard.** One bulk drop would be
unreviewable.

### Wave 1 — template-only fixes (4 skills)

`altitude-horizon-framework` · `company-intel` · `executive-onboarding-playbook` ·
`finance-metrics-quickref`

Smallest unit of real value. `company-intel` matters most — it is suite-adjacent, already has
examples, and only lacks the schema.

### Wave 2 — core artifacts (7 skills)

`user-story` · `problem-statement` · `positioning-statement` · `proto-persona` · `press-release` ·
`epic-hypothesis` · `storyboard`

Highest traffic in the library; biggest pedagogic return per file. **Fieldlight + Northfield, kept
legible.**

### Wave 3 — workflows (4 skills)

`prd-development` · `roadmap-planning` · `discovery-process` · `product-strategy-session`

Longer examples, more effort each, but these are the skills people run end to end. `discovery-process`
and `product-strategy-session` are the first natural Brightwater candidates.

### Wave 4 — the tail (13 skills)

Remaining Group B, plus the three Group A skills needing both files
(`skill-authoring-workflow`, `stakeholder-identification`, `stakeholder-mapping`).

---

## Definition of done, per skill

- [ ] `template.md` — the output schema as a copy/paste fill-in, with quality checks at the bottom
- [ ] Two worked examples, second suffixed by domain (`sample-industrial.md`,
      `sample-lifesciences.md`)
- [ ] Each example ends with a "what to notice" section — reasoning, not just output
- [ ] Universe details consistent with what is already shipped (dates, counts, product names)
- [ ] `bash scripts/test-a-skill.sh --smoke <path>` passes
- [ ] No hard-excluded Brightwater topics (see guardrail above)

## After each wave

```bash
python3 scripts/generate-catalog.py
bash scripts/build-dist.sh
python3 scripts/check-dist-freshness.py
```

Adding example files does not change skill counts, but the `dist/` ZIPs carry the example files —
so the shelf goes stale on every wave, and CI will now catch it.
