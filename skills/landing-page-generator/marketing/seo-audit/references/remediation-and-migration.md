# Remediation, Migration, Outputs & Success Criteria

Read this when turning findings into action: the migration audit checklist (pre/during/post), the prioritized remediation framework and plan template, output artifact definitions, the troubleshooting table, and the success criteria that define a passing audit.

## Migration Audit Checklist

### Pre-Migration (2-4 weeks before)

- [ ] Crawl entire current site and export all URLs
- [ ] Map every old URL to its new URL (1:1 redirect mapping)
- [ ] Export current rankings and organic traffic baseline
- [ ] Document all existing 301 redirects (chain them to new destinations)
- [ ] Verify robots.txt will be correct on new site
- [ ] Verify XML sitemap will be updated
- [ ] Test new site in staging environment
- [ ] Verify all schema markup transfers to new templates

### During Migration

- [ ] Implement all 301 redirects
- [ ] Submit updated XML sitemap to GSC
- [ ] Verify robots.txt is not blocking critical pages
- [ ] Test 50 sample redirects for correctness
- [ ] Monitor server errors in real-time

### Post-Migration (2-8 weeks after)

- [ ] Monitor GSC Coverage report daily for 2 weeks
- [ ] Track organic traffic vs. baseline daily
- [ ] Check for crawl errors in GSC
- [ ] Verify old URLs redirect correctly (batch test)
- [ ] Monitor rankings for top 50 keywords
- [ ] Check for broken internal links on new site
- [ ] Verify analytics tracking is firing correctly

---

## Prioritized Remediation Plan

### Priority Framework

Every finding gets classified:

| Priority | Criteria | Timeline |
|----------|----------|----------|
| P0 Emergency | Blocking indexation or causing active ranking loss | Fix today |
| P1 Critical | Major negative impact on rankings or traffic | Fix this week |
| P2 High | Significant improvement potential | Fix this month |
| P3 Medium | Moderate improvement, standard best practice | Fix this quarter |
| P4 Low | Minor improvement or nice-to-have | Backlog |

### Remediation Plan Template

| # | Finding | Dimension | Severity | Current State | Recommended Fix | Expected Impact | Effort |
|---|---------|-----------|----------|--------------|----------------|-----------------|--------|
| 1 | | | | | | | |
| 2 | | | | | | | |

---

## Output Artifacts

| Artifact | Format | Description |
|----------|--------|-------------|
| Executive Summary | 3-5 bullet points | Overall grade, top issues, quick wins |
| Full Audit Report | 85-point checklist | Pass/fail per check with evidence |
| Severity Scorecard | Weighted score table | Per-dimension scores and overall grade |
| Prioritized Fix List | Ranked table | Every finding with severity, fix, effort, impact |
| Keyword Cannibalization Map | Table | Pages competing for same keywords with resolution action |
| Competitive Gap Report | Comparison matrix | Your site vs. 3 competitors across 8 dimensions |
| Migration Checklist | Checkbox list | Pre/during/post migration tasks |

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Sitewide traffic drop after algorithm update | Core update changed quality thresholds or E-E-A-T weight | Run full E-E-A-T audit, compare content against newly ranking competitors, add experience signals |
| Pages indexed but receiving zero impressions | Keyword cannibalization or content quality below ranking threshold | Run cannibalization detection, consolidate or differentiate competing pages |
| Core Web Vitals failing on mobile only | Third-party scripts or unoptimized images loading on mobile viewport | Defer non-critical JS, serve responsive images, audit third-party script impact |
| Crawl budget exhausted on low-value pages | Parameter URLs, tag archives, or pagination consuming crawl resources | Noindex thin pages, consolidate parameters, block faceted navigation in robots.txt |
| Manual action in Search Console | Unnatural links, thin content, or structured data misuse detected | Follow Google's reconsideration process — fix all flagged issues, document changes, submit review |
| Rankings dropped for specific pages only | Competitor published stronger content or lost key backlinks | Check backlink profile changes, compare content depth against new page 1 results |
| INP failing despite fast server response | Long JavaScript tasks blocking main thread on user interaction | Break JS into smaller tasks, defer non-critical scripts, audit event handler performance |

---

## Success Criteria

- **Overall audit score**: Achieve grade B (80+) or higher on the severity-weighted scoring system
- **Zero critical failures**: All Critical-severity checks passing across all 8 dimensions
- **Core Web Vitals pass rate**: All three metrics (LCP < 2.5s, INP < 200ms, CLS < 0.1) passing at 75th percentile — benchmark: only 47-55% of sites pass as of 2026
- **Indexation coverage**: 95%+ of target pages indexed with zero conflicting signals (canonical vs noindex vs sitemap)
- **Crawl error rate**: Zero 5xx errors and fewer than 0.5% 4xx errors in the indexed page set
- **Organic CTR**: Position 1 pages achieving 25%+ CTR, position 2-3 achieving 10%+ (2026 benchmarks: pos 1 avg 27.6%, pos 2 avg 15.8%)
- **Remediation velocity**: All P0 emergency findings fixed within 24 hours, P1 critical within 7 days
