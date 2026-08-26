# Template Design, Quality Control & Linking

Read this when designing the page template (zones, uniqueness sources, URL structure), running pre-publication QA, detecting thin content, building hub-and-spoke internal linking, or avoiding penalty-triggering anti-patterns.

## Template Design System

### Page Architecture

Every programmatic page must have these zones:

```
┌─────────────────────────────────────┐
│ Zone 1: Unique Header               │  H1 with target keyword, unique intro paragraph
├─────────────────────────────────────┤
│ Zone 2: Primary Data Section         │  The core data/content for this specific page
├─────────────────────────────────────┤
│ Zone 3: Contextual Analysis          │  Insights, comparisons, trends specific to this entity
├─────────────────────────────────────┤
│ Zone 4: Related Data                 │  Adjacent data points that add depth
├─────────────────────────────────────┤
│ Zone 5: Internal Navigation          │  Related pages, breadcrumbs, category links
├─────────────────────────────────────┤
│ Zone 6: CTA                         │  Conversion element matched to intent
└─────────────────────────────────────┘
```

### Uniqueness Requirements

Each page MUST have at least 3 of these 5 uniqueness sources:

1. **Unique data points** -- Numbers, facts, or attributes specific to this entity
2. **Conditional content blocks** -- Sections that appear/disappear based on data attributes
3. **Calculated insights** -- Derived metrics (percentages, comparisons, rankings)
4. **Contextual recommendations** -- "If X, then Y" advice blocks based on the data
5. **User-generated content** -- Reviews, comments, or community contributions

### URL Structure

**Always use subfolders.** Never subdomains for pSEO.

| Pattern | URL Template | Example |
|---------|-------------|---------|
| Location | `/[service]/[city]/` | `/coworking/austin/` |
| Comparison | `/compare/[a]-vs-[b]/` | `/compare/notion-vs-confluence/` |
| Integration | `/integrations/[partner]/` | `/integrations/slack/` |
| Glossary | `/glossary/[term]/` | `/glossary/churn-rate/` |
| Persona | `/[product]-for-[audience]/` | `/crm-for-real-estate/` |

---

## Quality Control Framework

### Pre-Publication QA Checklist

**Content Quality:**
- [ ] Each page has > 300 words of unique content (not counting shared template elements)
- [ ] H1 is unique and contains the target keyword
- [ ] Meta title is unique (< 60 chars) and meta description is unique (< 155 chars)
- [ ] No broken data references (empty fields rendered as "N/A" or blank)
- [ ] At least 2 conditional content blocks triggered per page
- [ ] No duplicate pages targeting the same keyword

**Technical SEO:**
- [ ] Canonical tag points to self
- [ ] Hreflang tags if multilingual
- [ ] Schema markup renders without errors
- [ ] Page loads in < 3 seconds
- [ ] Mobile responsive

**Internal Linking:**
- [ ] Breadcrumb trail is complete
- [ ] 3-5 related pages linked contextually
- [ ] Hub page links to this page
- [ ] No orphan pages in the set

### Thin Content Detection

Run this check against every generated page:

| Signal | Threshold | Action |
|--------|-----------|--------|
| Unique word count | < 200 unique words | Block publication |
| Content similarity to another page in set | > 80% Jaccard similarity | Merge or differentiate |
| Data fields populated | < 60% of template fields | Skip or enrich |
| User time-on-page (post-launch) | < 15 seconds average | Review and improve |
| Bounce rate (post-launch) | > 85% | Review intent match |

---

## Internal Linking Architecture

### Hub-and-Spoke Model

```
                    ┌─────────┐
                    │  HUB    │  /coworking/
                    │  PAGE   │  (ranks for "coworking spaces")
                    └────┬────┘
          ┌──────────────┼──────────────┐
     ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
     │ SPOKE 1 │    │ SPOKE 2 │    │ SPOKE 3 │
     │ /austin/│    │ /denver/│    │ /seattle/│
     └────┬────┘    └────┬────┘    └────┬────┘
          │              │              │
     Cross-links between related spokes
```

**Linking rules:**
- Hub links DOWN to every spoke (or top 50 spokes if > 200 pages)
- Every spoke links UP to the hub
- Spokes link ACROSS to 3-5 related spokes (geographic proximity, thematic similarity)
- Deep pages link UP to their spoke AND the hub
- Cross-silo links only when contextually genuine

### Pagination for Large Sets

If a hub page has > 50 spokes, implement paginated sub-hubs:

```
/coworking/                     → Top cities + browse by state
/coworking/california/          → All California cities
/coworking/california/page/2/   → Paginated if > 25 cities
```

---

## Anti-Patterns and Penalty Avoidance

| Anti-Pattern | Why It Fails | Prevention |
|-------------|-------------|------------|
| City-name swapping | Same content + different city = doorway page penalty | Each location page needs unique local data |
| Keyword stuffing in templates | Unnatural density triggers spam filters | Keep keyword density 1-2%, write naturally |
| Generating pages for zero-demand queries | Wastes crawl budget, signals low quality | Validate demand before generating |
| No internal links to pSEO pages | Orphan pages get deprioritized | Connect every page to the hub-spoke structure |
| Stale data never refreshed | Users lose trust, Google notices | Set update cadence per data type |
| All pages identical structure | Lack of variation signals automation to Google | Use 3-5 template variants |
