# Indexation, Launch & Post-Launch Optimization

Read this when planning crawl budget and indexation priority, sequencing the phased rollout, building the post-launch metrics dashboard, diagnosing problems via the troubleshooting table, or checking deliverables against output artifacts and success criteria.

## Indexation Strategy

### Crawl Budget Management

| Page Set Size | Strategy |
|--------------|----------|
| < 500 pages | Single XML sitemap, submit all |
| 500-5,000 | Segmented sitemaps by category |
| 5,000-50,000 | Segmented sitemaps + priority scoring + IndexNow |
| 50,000+ | Programmatic sitemap generation + crawl budget monitoring + strategic noindex |

### Indexation Priority

| Priority | Pages | Action |
|----------|-------|--------|
| P0 | Hub pages | Submit immediately, internal link from homepage |
| P1 | Head-volume spokes (top 10%) | Submit in first sitemap batch |
| P2 | Torso-volume spokes | Submit in second batch, 1-2 weeks later |
| P3 | Long-tail spokes | Submit gradually over 4-6 weeks |
| P4 | Zero-volume pages | Noindex unless data is uniquely valuable |

### IndexNow Integration

For large-scale updates, use IndexNow to notify search engines immediately:

```
POST https://api.indexnow.org/indexnow
{
  "host": "yoursite.com",
  "key": "your-api-key",
  "urlList": ["https://yoursite.com/page1", "https://yoursite.com/page2"]
}
```

---

## Launch Sequence

### Phase 1: Pilot (Week 1-2)
- Deploy 20-50 pages from head-volume tier
- Submit sitemap with pilot pages only
- Monitor indexation rate daily
- Check for crawl errors in Search Console

### Phase 2: Scale (Week 3-6)
- Deploy remaining torso-volume pages in batches of 100-500
- Add cross-links between deployed pages
- Monitor thin content warnings
- Track impressions in Search Console

### Phase 3: Long-Tail (Week 7-12)
- Deploy long-tail pages
- Noindex zero-volume pages (keep them crawlable but not indexed)
- Begin link acquisition outreach for hub pages

### Phase 4: Optimization (Ongoing)
- A/B test template variations on head-volume pages
- Refresh stale data quarterly
- Add conditional content blocks based on engagement data
- Monitor for keyword cannibalization across the set

---

## Post-Launch Optimization

### Metrics Dashboard

| Metric | Frequency | Target |
|--------|-----------|--------|
| Indexation rate | Weekly | > 90% of submitted pages indexed within 60 days |
| Organic impressions | Weekly | Trending up month-over-month |
| Average position (by tier) | Bi-weekly | Head pages: top 10; Torso: top 30 |
| Click-through rate | Monthly | > 3% for head pages |
| Bounce rate | Monthly | < 70% |
| Conversion rate | Monthly | > 1% for transactional intent |
| Pages per session | Monthly | > 1.5 |

### Optimization Playbook

| Signal | Diagnosis | Action |
|--------|-----------|--------|
| Indexed but not ranking | Content quality or authority gap | Enrich content, build links to hub |
| Ranking but low CTR | Title/description not compelling | A/B test meta titles |
| Ranking but high bounce | Intent mismatch or thin content | Audit against search intent, add data |
| Deindexed after initial indexing | Thin content penalty | Improve uniqueness, reduce similarity |
| Crawled but not indexed | Quality threshold not met | Add more unique content per page |

---

## Output Artifacts

| Artifact | Format | Description |
|----------|--------|-------------|
| Opportunity Analysis | Markdown table | Keyword patterns x volume x data source x difficulty x business alignment |
| Playbook Recommendation | Decision matrix | If/then mapping with rationale and real-world examples |
| Page Template Specification | Annotated wireframe (markdown) | URL pattern, zone structure, uniqueness sources, conditional logic |
| Data Pipeline Spec | Flow diagram (text) | Source > extraction > transformation > validation > publication |
| Quality Scorecard | Checklist + thresholds | Pre-publication QA gates with pass/fail criteria |
| Indexation Plan | Phased timeline | Priority tiers, sitemap structure, crawl budget allocation |
| Post-Launch Dashboard | Metric table | KPIs, targets, review cadence, optimization triggers |

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Google deindexed 90%+ of pSEO pages | Thin content — pages have insufficient unique content (<300 words) or >80% similarity | Increase unique content per page to 500+ words; ensure 30-40% differentiation between pages |
| Pages indexed but getting zero traffic | Pages target zero-volume keywords or content does not match search intent | Validate demand before generating; noindex zero-volume pages; verify intent alignment |
| "Doorway pages" manual action in GSC | Template pages with only variable substitution (city name swap) and no unique value | Add genuinely unique data per page — local stats, specific recommendations, conditional content blocks |
| Hub page ranks but spokes do not | Spokes missing inbound internal links or hub not linking down to spokes | Verify bidirectional hub-spoke linking; add contextual cross-links between related spokes |
| Crawl budget exhausted before all pages indexed | Too many pages submitted at once or low-value pages consuming crawl resources | Phase deployment in batches of 100-500; use tiered indexation with strategic noindex |
| Content similarity too high across page set | Template lacks conditional content blocks; only variable substitution used | Add 3-5 conditional content sections per template that change based on data attributes |
| AI content detection flagging pSEO pages | Over-reliance on AI generation without human editorial review | Use AI for data enrichment only, not full content generation; sample 5-10% for quality review |

---

## Success Criteria

- **Indexation rate**: 90%+ of submitted pages indexed within 60 days of deployment
- **Content uniqueness**: Every page has 500+ unique words with <40% similarity to any other page in the set (2026 Google threshold)
- **Head keyword rankings**: Top 10% of pages (by volume) ranking in top 30 within 90 days
- **Organic traffic growth**: Page set generating measurable organic traffic within 60 days of full deployment
- **Thin content rate**: Zero pages flagged as thin content in Google Search Console
- **Bounce rate**: Below 70% average across the page set (indicating intent match)
- **Conversion rate**: 1%+ for transactional intent pages, measurable lead capture for informational pages
