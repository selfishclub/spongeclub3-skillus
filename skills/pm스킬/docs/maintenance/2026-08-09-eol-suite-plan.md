# EOL Skills Suite — Implementation Plan

## Context

The skills repo has **one** EOL skill (`eol-message`, a Component) covering only customer-facing announcements with a "replacement exists" path. Meanwhile, `product-manager-prompts` has **5 mature EOL prompts** (all Aug 9, 2026) plus Dean's field-experience blog post, two detailed checklists, a webinar deck, and a full 2-day GTM/EOL workshop. The repo is dramatically underserving end-of-life.

**Goal:** Build a 6-skill EOL suite (1 upgrade + 5 new) that covers the full EOL process from go/no-go decision through customer announcement. The governing design principle is **Goldilocks right-sizing** — every skill uses a 3-tier complexity classification (Light/Standard/Heavy) so a feature deprecation gets a punch list while a flagship retirement gets the full cross-functional playbook.

**Theme:** `eol-transition` (new theme for all 6 skills)

---

## The Suite

| # | Skill | Type | Files | Source |
|---|-------|------|-------|--------|
| 1 | `eol-readiness-advisor` | Interactive | SKILL.md only | `eol-readiness-assessment.md` + blog post |
| 2 | `eol-checklist` | Component | SKILL.md, template.md, examples/sample.md, examples/sample-industrial.md | `eol-checklist.md` + two DOCX checklists |
| 3 | `eol-stakeholder-sequence` | Component | SKILL.md, template.md, examples/sample.md, examples/sample-industrial.md | `eol-stakeholder-sequence.md` + blog post + workshop Mendelow/DACI |
| 4 | `eol-internal-enablement` | Component | SKILL.md, template.md, examples/sample.md, examples/sample-industrial.md | `eol-internal-enablement.md` + workshop WIIFM |
| 5 | `eol-message` | Component (UPGRADE) | Modify SKILL.md, replace template.md, replace sample.md, add sample-industrial.md | `eol-for-a-product-message.md` (upgraded) |
| 6 | `eol-process` | Workflow | SKILL.md, template.md, examples/sample.md, examples/sample-industrial.md | All above, orchestrated |

**Total: 22 files (17 new, 5 modified/replaced)**

---

## Goldilocks Tiers (Shared Across Suite)

| Dimension | Tier 1 — Light | Tier 2 — Standard | Tier 3 — Heavy |
|---|---|---|---|
| Scope | Feature, internal tool, API | Commercial product, active customers | Revenue-critical, hardware, regulated |
| Stakeholder stops | 3-4 | 7-8 | 10+ |
| Lifecycle phases | 2-3 (NSC, EOS, EOL) | 4-5 (NSC→EOM→EOL) | All 6 (NSC→EOSRV) |
| Functional areas | Product, Eng, Support, Docs | +Sales, Marketing, CS, Finance, Legal, IT, Data | +Supply Chain, Channel, Regulatory, Org |
| Enablement | Support FAQ only | +Sales talking points, objections, escalation | +Channel brief, account tiers, training |
| Message complexity | Brief notice | Standard w/ phase table | Full w/ compliance section |

Each skill determines the tier in two ways: (a) passed from upstream (e.g. readiness advisor output), or (b) self-classified if invoked standalone.

---

## Fictional Universes for Examples

**SaaS (Tier 2):** Fieldlight Classic — legacy dispatch module in the Fieldlight FSM platform. ~800 accounts, $2.4M ARR. Replaced by Fieldlight Next (AI-powered scheduling). No regulatory, no hardware.

**Industrial (Tier 3):** NFA-200 series retrofit controller by Northfield Automation. ~120 installations, 8 channel partners, active service contracts, UL/CE regulatory, physical hardware + spare parts. Replaced by NFA-500 platform.

---

## Execution Order

### Phase 1 — Foundation (no cross-deps on new skills)

1. **`eol-readiness-advisor`** (Interactive, new) — Entry point. Classifies the tier. References all other EOL skills in its Final Step.
2. **`eol-message`** (Component, upgrade) — Add right-sizing (Brief/Standard/Full), three transition paths (Replacement/Migration/Graceful Exit), lifecycle-phase definitions, theme, adorned frontmatter, replace examples with Fieldlight + NFA-200.

### Phase 2 — Core Components (reference readiness + message)

3. **`eol-checklist`** — Phase-gated operational plan with 15 functional areas filtered by tier.
4. **`eol-stakeholder-sequence`** — Sequenced conversation plan with the canonical order (Legal→Finance→Sales→Marketing→CS→Support→Channel→difficult customers).
5. **`eol-internal-enablement`** — Support FAQ + sales talking points + objection handling (Acknowledge-Reframe-Offer) + channel brief + training outline, tiered.

### Phase 3 — Orchestrator

6. **`eol-process`** (Workflow) — 6-phase orchestrator referencing all 5 above. Decision gates between phases.

### Phase 4 — Catalog & Validation

7. Run `scripts/check-skill-metadata.py` on each new skill
8. Run `scripts/test-a-skill.sh --smoke` on each new skill
9. Note: catalog/marketplace updates are a follow-on step (Dean commits manually)

---

## Key Design Decisions

- **eol-readiness-advisor** follows the `business-health-diagnostic` pattern (Interactive, SKILL.md only, question flow with scoring)
- **eol-process** follows the `discovery-process` pattern (Workflow, phased orchestration, decision gates, workshop-facilitation reference)
- **eol-message upgrade** preserves: skill name, folder, core 9-section framework, 5 pitfalls, positioning-statement cross-ref. Adds: right-sizing, 3 paths, phase definitions, theme, dual-domain examples, suite cross-refs
- Every skill's References section cross-links the other 5 EOL skills plus relevant non-EOL skills (positioning-statement, proto-persona, workshop-facilitation)
- Lifecycle phase definitions (GA→NSC→EOS→EOE→EOR→EOM→EOL→EOSRV) are standardized text shared across all skills that reference phases

---

## Verification

1. `python3 scripts/check-skill-metadata.py` on each of the 6 skill SKILL.md files — must pass
2. `bash scripts/test-a-skill.sh --smoke skills/eol-*/SKILL.md` — must pass with no new failures
3. Manual review: each skill's tier definitions must match the shared table exactly
4. Manual review: Fieldlight/NFA-200 example details must be consistent across all 10 example files
5. Cross-reference check: every `skills/eol-*/SKILL.md` path referenced in References sections must resolve
