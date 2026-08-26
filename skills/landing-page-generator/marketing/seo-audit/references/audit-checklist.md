# Audit Scoping & The 85-Point Checklist

Read this when starting an audit: it covers initial scoping questions, the full 85-point checklist across all 8 dimensions, and the severity-weighted scoring formula used to produce an overall grade.

## Initial Assessment

### Required Context

| Question | Why It Matters |
|----------|---------------|
| What type of site? (SaaS, e-commerce, blog, local business) | Determines which audit dimensions to weight |
| What is the primary SEO goal? | Focuses the audit on business-relevant outcomes |
| What is the current organic traffic baseline? | Establishes the benchmark for measuring improvement |
| Any recent changes? (migration, redesign, content update, algorithm update) | Identifies potential cause of current issues |
| Do you have Google Search Console access? | Essential for indexation and performance data |
| Who are 3 organic competitors? | For competitive gap analysis |

### Scope Definition

| Scope | Pages to Audit | Recommended When |
|-------|---------------|-----------------|
| Full site | All indexed pages + sample of non-indexed | Annual audit, new client onboarding |
| Section audit | One directory or content type | Known problem area |
| Top pages | Top 50 by traffic + top 50 by impressions | Quick wins identification |
| New pages | Pages published in last 90 days | Content quality check |

---

## The 85-Point Audit Checklist

### Dimension 1: Crawlability (12 points)

| # | Check | Severity | Pass Criteria |
|---|-------|----------|---------------|
| 1.1 | robots.txt accessible and valid | Critical | 200 response, no syntax errors |
| 1.2 | Important pages not blocked by robots.txt | Critical | No disallow rules for key pages |
| 1.3 | XML sitemap exists and is valid | High | Submitted in GSC, < 50K URLs per file |
| 1.4 | Sitemap reflects actual site structure | High | No 404s, no redirects, no noindex pages in sitemap |
| 1.5 | Crawl depth < 4 clicks from homepage | Medium | 95%+ of pages within 3 clicks |
| 1.6 | No infinite crawl traps | Critical | No parameter-based infinite loops |
| 1.7 | Internal links use crawlable HTML | High | No JavaScript-only navigation |
| 1.8 | Pagination uses rel=next/prev or load-more | Medium | Paginated content is crawlable |
| 1.9 | No orphan pages (indexed but no internal links) | High | 0 orphan pages in indexed set |
| 1.10 | Crawl budget not wasted on low-value pages | Medium | < 10% crawl budget on utility pages |
| 1.11 | Server response time < 500ms | High | TTFB < 500ms for 95% of pages |
| 1.12 | No 5xx errors in crawl | Critical | 0% server errors |

### Dimension 2: Indexation (10 points)

| # | Check | Severity | Pass Criteria |
|---|-------|----------|---------------|
| 2.1 | Target pages are indexed | Critical | > 95% of target pages in Google index |
| 2.2 | No duplicate content issues | High | No duplicate titles, no near-duplicate content |
| 2.3 | Canonical tags implemented correctly | High | Self-referencing on unique pages, cross-domain where needed |
| 2.4 | No conflicting signals (canonical vs noindex vs sitemap) | Critical | No page that is both noindex and in sitemap |
| 2.5 | Hreflang tags correct (if multilingual) | High | Valid hreflang with return tags |
| 2.6 | No index bloat (unnecessary pages indexed) | Medium | Utility pages not indexed |
| 2.7 | Thin content pages identified | High | No pages with < 200 words of unique content |
| 2.8 | Parameter handling configured | Medium | URL parameters handled in GSC or via canonical |
| 2.9 | JavaScript-rendered content indexable | High | Key content visible in cached/rendered version |
| 2.10 | New pages getting indexed within 7 days | Medium | Using IndexNow or manual submission |

### Dimension 3: Core Web Vitals (10 points)

| # | Check | Severity | Pass Criteria |
|---|-------|----------|---------------|
| 3.1 | LCP < 2.5s | High | 75th percentile of page loads |
| 3.2 | INP < 200ms | High | 75th percentile of interactions |
| 3.3 | CLS < 0.1 | High | 75th percentile of page loads |
| 3.4 | Mobile CWV passing | Critical | Mobile scores meeting thresholds |
| 3.5 | Desktop CWV passing | Medium | Desktop scores meeting thresholds |
| 3.6 | No render-blocking resources | Medium | CSS/JS delivery optimized |
| 3.7 | Images optimized (WebP/AVIF, lazy loading) | Medium | All above-fold images preloaded |
| 3.8 | Font loading optimized | Low | No FOUT/FOIT, font-display: swap |
| 3.9 | Third-party script impact measured | Medium | No third-party scripts adding > 500ms |
| 3.10 | HTTPS with no mixed content | Critical | All resources served over HTTPS |

### Dimension 4: On-Page SEO (15 points)

| # | Check | Severity | Pass Criteria |
|---|-------|----------|---------------|
| 4.1 | Unique title tags on every page | Critical | No duplicates, < 60 chars |
| 4.2 | Title includes primary keyword | High | Keyword in first 60 chars |
| 4.3 | Unique meta descriptions | High | No duplicates, < 155 chars, includes keyword |
| 4.4 | H1 tag present and unique per page | High | One H1 per page with primary keyword |
| 4.5 | Heading hierarchy logical (H1 > H2 > H3) | Medium | No skipped levels |
| 4.6 | Internal links with descriptive anchor text | High | No "click here" or naked URLs |
| 4.7 | Images have alt text | Medium | Descriptive alt text on all meaningful images |
| 4.8 | URL structure is clean and descriptive | Medium | No IDs, parameters, or excessive depth |
| 4.9 | Primary keyword in first 100 words | Medium | Natural inclusion in opening |
| 4.10 | Content matches search intent | Critical | Page type matches what Google ranks for query |
| 4.11 | No keyword cannibalization | High | No two pages targeting the same primary keyword |
| 4.12 | Open Graph and Twitter Card tags | Low | Social sharing metadata present |
| 4.13 | Structured data implemented | Medium | Relevant schema types present |
| 4.14 | Internal links to relevant pages | High | 3-5 contextual internal links per content page |
| 4.15 | Breadcrumbs present | Medium | Functional breadcrumbs with schema |

### Dimension 5: Content Quality (12 points)

| # | Check | Severity | Pass Criteria |
|---|-------|----------|---------------|
| 5.1 | Content provides unique value | Critical | Not available elsewhere in same form |
| 5.2 | Content depth matches intent | High | Comprehensive coverage of the topic |
| 5.3 | Content freshness appropriate | Medium | Updated within last 12 months for evergreen |
| 5.4 | No AI-generated content markers | High | No generic filler, overused phrases, or em-dash patterns |
| 5.5 | E-E-A-T signals present | High | Author attribution, credentials, experience evidence |
| 5.6 | Content readability appropriate | Medium | Matches target audience reading level |
| 5.7 | No thin content pages | High | All pages > 300 words of unique content |
| 5.8 | No content duplication across pages | High | Jaccard similarity < 50% between any two pages |
| 5.9 | Content supports conversion goal | Medium | Clear CTA aligned with page intent |
| 5.10 | Visual content present | Medium | Images, charts, or videos enhance understanding |
| 5.11 | Content organized with subheadings | Medium | Scannable structure with clear sections |
| 5.12 | External references and citations | Low | Links to authoritative sources where relevant |

### Dimension 6: Technical Infrastructure (10 points)

| # | Check | Severity | Pass Criteria |
|---|-------|----------|---------------|
| 6.1 | HTTPS properly configured | Critical | Valid certificate, no mixed content |
| 6.2 | Proper redirects (301 not 302) | High | Permanent redirects for permanent moves |
| 6.3 | No redirect chains (> 2 hops) | Medium | Direct redirect from origin to destination |
| 6.4 | No broken internal links (404s) | High | 0 broken internal links |
| 6.5 | No broken external links | Low | < 5% broken outbound links |
| 6.6 | Mobile-responsive design | Critical | Passes Google's mobile-friendly test |
| 6.7 | Proper 404 page | Low | Custom 404 with navigation and search |
| 6.8 | Server uptime > 99.9% | Critical | Monitoring in place |
| 6.9 | CDN configured for global audience | Medium | If international traffic > 20% |
| 6.10 | Security headers present | Low | HSTS, CSP, X-Frame-Options |

### Dimension 7: Off-Page Signals (8 points)

| # | Check | Severity | Pass Criteria |
|---|-------|----------|---------------|
| 7.1 | Backlink profile health | High | No toxic link patterns |
| 7.2 | Referring domain diversity | Medium | > 50 unique referring domains |
| 7.3 | Anchor text distribution natural | Medium | < 30% exact-match anchors |
| 7.4 | No manual actions in GSC | Critical | Clean manual actions report |
| 7.5 | Google Business Profile (if local) | High | Claimed, verified, complete |
| 7.6 | Social profiles linked | Low | Active profiles on major platforms |
| 7.7 | Brand mentions without links | Low | Unlinked mentions as link opportunities |
| 7.8 | Competitor link gap identified | Medium | Top competitors' link sources mapped |

### Dimension 8: Analytics and Tracking (8 points)

| # | Check | Severity | Pass Criteria |
|---|-------|----------|---------------|
| 8.1 | Google Search Console verified | Critical | All properties verified |
| 8.2 | GA4 properly configured | High | Events tracking, no duplicate tags |
| 8.3 | Conversion tracking in place | High | Key conversions tracked |
| 8.4 | GSC and GA4 linked | Medium | Data flowing between tools |
| 8.5 | Bing Webmaster Tools configured | Low | Verified and sitemap submitted |
| 8.6 | Search Console coverage report clean | High | No unexpected errors |
| 8.7 | Core Web Vitals field data available | Medium | Enough traffic for CrUX data |
| 8.8 | UTM parameter strategy | Low | Consistent campaign tracking |

---

## Severity-Weighted Scoring

### Scoring Formula

```
Total Score = Sum of (Dimension Weight x Dimension Pass Rate)

Dimension Pass Rate = (Passed Checks x Severity Multiplier) / (Total Checks x Severity Multiplier)

Severity Multipliers:
  Critical = 4x
  High = 3x
  Medium = 2x
  Low = 1x
```

### Overall Health Grades

| Score | Grade | Assessment |
|-------|-------|-----------|
| 90-100 | A | Excellent -- focus on competitive edge |
| 80-89 | B | Good -- fix remaining high-priority items |
| 70-79 | C | Fair -- significant improvements available |
| 60-69 | D | Poor -- critical issues blocking performance |
| < 60 | F | Failing -- foundational problems require immediate attention |
