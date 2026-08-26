# Strategy, Assessment & Playbooks

Read this when scoping a new pSEO opportunity, choosing which page-set pattern to build, or making the final build/skip call. Covers initial validation, the 14 playbooks, the playbook selection matrix, and the weighted build-vs-skip decision matrix.

## Initial Assessment

Before designing any pSEO strategy, answer these questions. Skip nothing.

### 1. Opportunity Validation

| Question | Why It Matters | Red Flag |
|----------|---------------|----------|
| What is the repeating keyword pattern? | Defines the template structure | Pattern is vague or inconsistent |
| What is the aggregate monthly search volume? | Determines ROI ceiling | < 5,000 aggregate monthly searches |
| How many unique pages can you generate? | Scope the project | < 50 pages (too few) or > 50K without data infrastructure |
| What does the SERP look like for sample queries? | Competitive feasibility | Page 1 dominated by DR 80+ editorial content |
| Is intent informational, navigational, or transactional? | Template design | Mixed intent across the same pattern |

### 2. Data Source Evaluation

Rate your data source on this scale:

| Tier | Source Type | Defensibility | Example |
|------|-----------|---------------|---------|
| S | Proprietary first-party | Unbeatable | Your product usage data, internal benchmarks |
| A | Product-derived | Strong | Aggregated user analytics, customer outcomes |
| B | User-generated | Moderate | Community reviews, submitted content |
| C | Licensed exclusive | Moderate | Paid data feed no competitor has |
| D | Public aggregated | Weak | Government data, public APIs |
| F | Scraped commodity | None | Wikipedia rewrites, copied listings |

**Rule: Do not build pSEO on Tier F data.** Google penalizes commodity rewrites. If your only data source is public and easily replicable, invest in acquiring Tier A-C data first.

### 3. Competitive Moat Assessment

For 5 sample queries in your pattern, analyze page 1 results:

- What is the average Domain Rating of ranking pages?
- Are existing results programmatic or editorial?
- What unique data do ranking pages provide?
- What is the content depth (word count, data richness, UX quality)?

**Go/No-Go threshold:** If the average DR gap between you and page 1 is > 30 AND existing results have proprietary data, the opportunity requires either a differentiated approach or domain authority building first.

---

## The 14 Playbooks

| # | Playbook | Pattern | Example | Data Requirement |
|---|----------|---------|---------|-----------------|
| 1 | Templates | "[Type] template" | "resume template", "invoice template" | Template files + metadata |
| 2 | Curation | "best [category]" | "best CRM for startups" | Product/service reviews + ratings |
| 3 | Conversions | "[X] to [Y]" | "100 USD to EUR" | Conversion logic/API |
| 4 | Comparisons | "[X] vs [Y]" | "Notion vs Confluence" | Feature data for both products |
| 5 | Examples | "[type] examples" | "landing page examples" | Curated example collection |
| 6 | Locations | "[service] in [city]" | "coworking in Austin" | Location-specific data |
| 7 | Personas | "[product] for [audience]" | "CRM for real estate" | Audience-specific use cases |
| 8 | Integrations | "[A] + [B] integration" | "Slack Asana integration" | Integration documentation |
| 9 | Glossary | "what is [term]" | "what is churn rate" | Domain expertise |
| 10 | Translations | Content in N languages | Localized guides | Translation + localization data |
| 11 | Directory | "[category] tools" | "AI writing tools" | Tool listings + evaluations |
| 12 | Profiles | "[entity name]" | "Stripe company profile" | Entity-level data |
| 13 | Statistics | "[topic] statistics" | "SaaS churn statistics 2026" | Verified statistical data |
| 14 | Calculators | "[topic] calculator" | "LTV calculator" | Calculation logic + inputs |

---

## Playbook Selection Matrix

| If you have... | Primary Playbook | Secondary Layer |
|----------------|-----------------|-----------------|
| A product with many integrations | Integrations | Comparisons |
| A design/creative tool | Templates + Examples | Personas |
| A multi-segment audience | Personas | Comparisons |
| Local/regional presence | Locations | Directory |
| A tool/utility product | Calculators + Conversions | Glossary |
| Deep domain expertise | Glossary + Statistics | Curation |
| A competitor landscape to exploit | Comparisons + Curation | Directory |
| User-generated content | Examples + Directory | Profiles |

**Layering rule:** Combine up to 2 playbooks per page set. Example: "Best coworking spaces in [city]" = Curation + Locations.

---

## Decision Matrix: Build vs Skip

Score each dimension 1-5, then apply the threshold.

| Dimension | Weight | 1 (Skip) | 5 (Build) |
|-----------|--------|----------|-----------|
| Search demand | 30% | < 1K aggregate monthly | > 50K aggregate monthly |
| Data quality | 25% | Public/scraped, easily replicated | Proprietary, defensible |
| Competitive gap | 20% | DR gap > 40, strong incumbents | DR gap < 15, weak/no incumbents |
| Template feasibility | 15% | Each page needs unique editorial | Clean template fits all variations |
| Business alignment | 10% | No conversion path from these pages | Direct path to core product |

**Scoring guide:**
- 4.0+ weighted average: Build immediately
- 3.0-3.9: Build if resources allow, validate with pilot first
- 2.0-2.9: Invest in data quality or authority first
- < 2.0: Do not build
