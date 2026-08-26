# Diagnostic Deep Dives & Analysis Frameworks

Read this when investigating a specific problem area: Core Web Vitals optimization, crawl/indexation gaps, traffic-drop diagnosis, on-page issues (cannibalization, intent mismatch), content quality (AI markers, E-E-A-T), and competitive gap analysis.

## Core Web Vitals Deep Dive

### LCP Optimization Priority Stack

| Cause | Detection | Fix | Impact |
|-------|-----------|-----|--------|
| Slow server response | TTFB > 600ms | CDN, server upgrade, caching | High |
| Render-blocking CSS/JS | PageSpeed Insights flags | Inline critical CSS, defer JS | High |
| Large hero image | LCP element is an image > 500KB | WebP/AVIF, responsive sizes, preload | High |
| Client-side rendering | LCP requires JS execution | SSR or prerendering | Medium |
| Web font blocking | FOUT delays LCP text | font-display: swap, preload fonts | Medium |

### INP Optimization Priority Stack

| Cause | Detection | Fix | Impact |
|-------|-----------|-----|--------|
| Long JavaScript tasks | Chrome DevTools Performance tab | Break into smaller tasks, use requestIdleCallback | High |
| Heavy event handlers | Slow click/scroll responses | Debounce, optimize handler code | High |
| Main thread blocking | Third-party scripts | Defer or lazy-load third-party JS | Medium |
| Layout thrashing | Forced reflows on interaction | Batch DOM reads/writes | Medium |

### CLS Optimization Priority Stack

| Cause | Detection | Fix | Impact |
|-------|-----------|-----|--------|
| Images without dimensions | CLS in PageSpeed Insights | Add width/height attributes | High |
| Dynamic content injection | Ads, embeds loading late | Reserve space with CSS aspect-ratio | High |
| Web fonts causing reflow | Text shifts when font loads | font-display: optional or swap | Medium |
| Late-loading CSS | Styles applied after render | Inline critical CSS | Medium |

---

## Crawl and Indexation Analysis

### Indexation Gap Analysis

Compare these three data sets to find gaps:

```
Set A: Pages in XML sitemap (your intended index)
Set B: Pages indexed in Google (site: query + GSC Coverage)
Set C: Pages receiving organic traffic (GSC Performance)

A - B = Submitted but not indexed (quality or crawl issue)
B - A = Indexed but not in sitemap (orphan or forgotten pages)
B - C = Indexed but receiving zero traffic (rank 100+ or deindexed from results)
```

### Traffic Drop Decision Tree

```
Traffic dropped →
  ├── Sitewide drop?
  │   ├── Yes → Check for manual action in GSC
  │   │         Check for algorithm update (timeline match?)
  │   │         Check for robots.txt or noindex changes
  │   │         Check server uptime/5xx errors
  │   └── No (specific pages/sections) →
  │       ├── Check for cannibalization (new page stealing from old)
  │       ├── Check for content freshness (competitor updated, you didn't)
  │       ├── Check for lost backlinks to those pages
  │       └── Check for SERP feature changes (new featured snippet, AI overview)
  └── Gradual decline vs sudden drop?
      ├── Sudden → Technical issue or algorithm update
      └── Gradual → Content decay, competitive pressure, or authority erosion
```

---

## On-Page SEO Analysis

### Keyword Cannibalization Detection

Two or more pages targeting the same keyword compete with each other. Detection method:

1. Export all pages + their primary keyword from GSC (queries with most impressions per page)
2. Group by keyword -- any keyword assigned to 2+ pages is cannibalized
3. Check which page ranks higher for each cannibalized keyword
4. Action: Consolidate (merge into one page), differentiate (change one page's target), or canonical (point one to the other)

### Intent Match Scoring

For each target keyword, verify that your page type matches what Google actually ranks:

| Google Ranks | Your Page Type | Match? | Action |
|-------------|---------------|--------|--------|
| Listicles | Single product page | No | Create a listicle targeting this keyword |
| How-to guides | Blog opinion piece | No | Restructure as how-to |
| Comparison tables | Feature page | Partial | Add comparison elements |
| Videos | Text-only page | No | Add video or target a different keyword |

---

## Content Quality Assessment

### AI Content Detection Signals

Watch for these patterns that signal low-quality AI-generated content:

| Signal | Example | Fix |
|--------|---------|-----|
| Excessive em dashes | "The tool -- which is powerful -- delivers results" | Use commas or periods |
| Filler hedging | "It's important to note that..." | Delete and get to the point |
| Generic superlatives | "This groundbreaking, cutting-edge solution" | Use specific, evidence-based language |
| Perfect paragraph symmetry | Every section has exactly 3 paragraphs of 4 sentences | Vary structure naturally |
| No first-person experience | Zero personal anecdotes or experience markers | Add genuine experience signals |
| Overused transitions | "Furthermore", "Moreover", "Additionally" at every paragraph | Vary connectors or remove them |

### E-E-A-T Scoring

| Signal | Weight | Check |
|--------|--------|-------|
| Author byline with credentials | High | Named author with bio and expertise |
| Author page with sameAs links | High | Links to LinkedIn, publications |
| Original research or data | High | First-party data, surveys, experiments |
| Experience evidence | High | Screenshots, photos, personal narrative |
| Citations to authoritative sources | Medium | Links to primary sources |
| Publication date and update date | Medium | Visible and accurate |
| About page with team credentials | Medium | Company expertise established |
| External reviews and mentions | Low | Third-party validation |

---

## Competitive Gap Analysis

### Framework

For each of your top 3 competitors, compare:

| Dimension | Your Site | Competitor 1 | Competitor 2 | Competitor 3 |
|-----------|----------|-------------|-------------|-------------|
| Domain Rating | | | | |
| Indexed pages | | | | |
| Organic keywords (top 100) | | | | |
| Estimated organic traffic | | | | |
| Content publishing frequency | | | | |
| Avg content depth (word count) | | | | |
| Referring domains | | | | |
| Top-performing content types | | | | |

### Keyword Gap Priority Matrix

| Gap Type | Description | Priority |
|----------|-------------|----------|
| Uncontested | Keyword with volume, no competitor ranks | Highest |
| Weak competition | You could realistically rank page 1 | High |
| Content gap | Competitor has content, you don't | Medium |
| Quality gap | Both have content, theirs ranks better | Medium |
| Authority gap | Competitor's DR advantage is the barrier | Lower (long-term) |
