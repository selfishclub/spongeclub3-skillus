# Keyword Pattern Mining & Data Pipeline

Read this when extracting the repeating keyword pattern, mapping search-volume distribution, classifying intent, or designing the data pipeline that feeds page generation (extraction, transformation, quality gates, update cadence).

## Keyword Pattern Mining

### Step 1: Pattern Identification

Extract the repeating structure from seed keywords:

```
Seed: "react developer salary san francisco"
Pattern: [role] salary [city]
Variables: role (200+ options), city (500+ options)
Max pages: 200 x 500 = 100,000
```

### Step 2: Volume Distribution Analysis

Not all variable combinations have search volume. Map the distribution:

| Tier | Volume Range | Typical % of Total Pages | Strategy |
|------|-------------|-------------------------|----------|
| Head | 1,000+ monthly | 2-5% | Priority indexation, highest content quality |
| Torso | 100-999 monthly | 15-25% | Standard template, full deployment |
| Long-tail | 10-99 monthly | 40-50% | Template with conditional content blocks |
| Zero-volume | < 10 monthly | 20-40% | Noindex OR skip unless data is uniquely valuable |

### Step 3: Intent Classification

For each pattern, verify intent consistency:

| Intent Type | Template Implications | CTA Strategy |
|------------|----------------------|--------------|
| Informational | Data-heavy, educational content | Newsletter, related content |
| Commercial investigation | Comparison tables, pros/cons | Free trial, demo |
| Transactional | Pricing, availability, features | Buy now, sign up |
| Navigational | Brand-specific, direct answer | Product page link |

---

## Data Pipeline Architecture

### Pipeline Design

```
[Data Source] → [Extraction] → [Transformation] → [Enrichment] → [Validation] → [Template Population] → [Quality Check] → [Publish]
```

### Data Quality Gates

Every record must pass these gates before page generation:

| Gate | Check | Failure Action |
|------|-------|---------------|
| Completeness | All required fields populated | Skip page, log for manual review |
| Accuracy | Data matches source, no staleness > 90 days | Flag for refresh |
| Uniqueness | No duplicate records | Merge or deduplicate |
| Minimum richness | Page will have > 300 words of unique content | Skip or enrich |
| Legal compliance | Data usage rights verified | Block publication |

### Update Cadence

| Data Type | Recommended Update Frequency | Staleness Penalty |
|-----------|------------------------------|-------------------|
| Pricing data | Weekly | High (users notice immediately) |
| Company/product data | Monthly | Medium |
| Statistical data | Quarterly | Low if year-tagged |
| Glossary/educational | Semi-annually | Very low |
| Location data | Monthly | Medium (closures, address changes) |
