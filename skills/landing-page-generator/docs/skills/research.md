---
title: Research Skills
description: Structured research workflows for academic, R&D, IP, and intelligence work. Literature review (PRISMA), grant proposals (NIH/NSF/SBIR), patent landscape, and intelligence dossiers — each with stdlib Python validators and source-discipline enforcement.
---

# Research Skills

**4 skills** with **12 stdlib-only Python tools** for structured research workflows.

This domain covers research that's distinct from user research (`product-team/`) and competitive analysis (`marketing/`). Focus: academic depth, IP rigor, grant discipline, and intelligence-grade dossiers — with the source-quality and fact/inference discipline that separates real research from confident guesses.

!!! info "New domain (May 2026)"
    Added in v4.8.0. All skills follow the deep pattern: `SKILL.md` + 3 references + 3 stdlib Python tools.

## Skills

### litreview — Literature review (PRISMA-aligned)

[:material-folder-open: Browse on GitHub](https://github.com/borghei/Claude-Skills/tree/main/research/litreview){ .md-button }

For academic and R&D literature reviews. PRISMA-adapted protocol for non-medical fields, plus 6-dimension source quality scoring and thematic synthesis.

**Workflows:**

- Plan the search → `search_strategy_builder.py` (databases, Boolean queries, filters, PRISMA log template)
- Score source quality → `source_quality_scorer.py` (6 dimensions: methodology, sample, peer review, reproducibility, recency, citation impact)
- Synthesize themes → `thematic_synthesis_builder.py` (evidence table, gap identification, contested-theme detection)

**Use when:** systematic literature review, R&D grounded report, scoping review, dissertation prep, audit of existing review for bias / methodological flaws.

### grants — Grant writing & proposal architecture

[:material-folder-open: Browse on GitHub](https://github.com/borghei/Claude-Skills/tree/main/research/grants){ .md-button }

For NIH, NSF, SBIR/STTR, foundation, corporate, and DARPA proposals. Funder-fit scoring before you commit weeks, structural validation per funder type, budget realism audit.

**Workflows:**

- Score funder fit → `funder_fit_scorer.py` (7 dimensions: topic, mechanism, stage, geo, team, budget envelope, competitive density)
- Validate proposal structure → `proposal_structure_validator.py` (NIH / NSF / SBIR / foundation / DARPA templates)
- Audit budget realism → `budget_realism_checker.py` (PI effort, fringe, equipment, indirect rate, common red flags)

**Use when:** writing a grant proposal, evaluating funder fit before applying, auditing a draft for competitiveness, planning a budget that survives review.

### patent — Patent research & IP landscape

[:material-folder-open: Browse on GitHub](https://github.com/borghei/Claude-Skills/tree/main/research/patent){ .md-button }

For prior-art search, IP landscape mapping, freedom-to-operate, and patentability scoring. Research-focused (not legal filing — work with a patent attorney for prosecution).

**Workflows:**

- Plan prior-art search → `prior_art_search_planner.py` (CPC/IPC classifications, multi-database queries, non-patent prior art, citation walking)
- Map IP landscape → `claim_landscape_mapper.py` (clusters by owner / classification / year / claim type; white space + crowded zones)
- Score patentability → `patentability_scorer.py` (5 dimensions: novelty, non-obviousness, utility, subject-matter eligibility, enablement)

**Use when:** prior-art search before provisional, FTO analysis before product launch, patentability assessment, competitive IP landscape mapping.

### dossier — Intelligence dossiers

[:material-folder-open: Browse on GitHub](https://github.com/borghei/Claude-Skills/tree/main/research/dossier){ .md-button }

For structured intelligence dossiers on companies, people, markets, or domains. Outline generation tailored to subject + purpose, Admiralty Code source reliability scoring, fact / inference / speculation discipline.

**Workflows:**

- Generate dossier outline → `dossier_outline_generator.py` (subject type: company / person / market / domain; purpose: briefing / deal-prep / due-diligence / market-entry / investment)
- Validate source triangulation → `source_triangulation_validator.py` (Admiralty Code A-F reliability + 1-6 credibility; flag single-source significant claims)
- Separate facts from inferences → `fact_inference_separator.py` (classify each statement; flag overconfident speculation, hidden inferences)

**Use when:** deal-prep dossier before major partnership, executive briefing, market-entry analysis, due-diligence overview, competitor profile, board-ready intelligence document.

## Quality standard

Each skill in this domain:

- Uses stdlib-only Python (no external dependencies)
- Supports both JSON and human-readable output (`--format` flag)
- Distinguishes facts from inferences explicitly
- Includes source reliability / quality scoring
- Rejects inflation, hallucination, and unsubstantiated claims

## Related skills

- **[Project Management](project-management.md)** — `discovery/customer-interview-script` and `discovery/interview-synthesis` for user research
- **[Product Team](product.md)** — `research-summarizer` for synthesizing user research
- **[C-Level Advisory](c-level.md)** — `general-counsel-advisor` for strategic legal context (patent skill is research, not filing)
- **[Business & Growth](business.md)** — `competitive-teardown` for competitive intelligence (different lens than `dossier`)
