# Playbook, Troubleshooting & Success Criteria

Read this when refining how you curate and execute ideas, diagnosing why ideas are underperforming, or defining what "good" looks like for an idea-selection cycle.

## Best Practices

1. **Curate ruthlessly** — Never dump all 139 ideas on someone. Match 3-5 to their specific stage, budget, and goal.

2. **Focus beats breadth** — A team of 1-2 should master 1-2 channels before expanding. Spreading across 5+ channels dilutes impact.

3. **Validate before scaling** — Test every idea at minimum viable effort before committing significant resources.

4. **Build owned audience first** — Before investing in paid or social channels, establish an email list or community. Owned audience compounds.

5. **Match timeline to expectations** — Content and SEO take 3-6 months. Paid ads produce results in days. Set expectations correctly.

6. **Document what works** — Every test, campaign, and experiment should be documented. Institutional knowledge compounds.

7. **Differentiate, do not copy** — Copying a competitor's entire playbook guarantees second place. Find what they are missing.

8. **Layer tactics** — The most effective strategies combine 2-3 complementary tactics (e.g., content + email + social repurposing).

9. **Kill what is not working** — Review all active channels quarterly. Stop investing in channels that do not produce results after a fair test period.

10. **Customer insight drives everything** — The best marketing idea comes from understanding what your customer needs, not from a tactics list.

---

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| Team overwhelmed by too many ideas, nothing gets executed | No prioritization framework applied; all ideas treated equally | Use idea_scorer.py to filter by stage, budget, and goal; select top 3-5 only |
| Implemented ideas do not produce expected results | Ideas selected without validating fit for current stage and audience | Match ideas to ICP and marketing context before execution; validate with small test first |
| Content ideas generate traffic but zero leads | Targeting top-of-funnel informational keywords without conversion path | Add lead magnets, CTAs, and gated content to every content piece; create bottom-of-funnel companion pages |
| Paid ads burn budget with poor ROAS in first month | No testing phase; full budget deployed on unvalidated targeting | Start at 20% budget for 2 weeks to test, then scale winners; kill ads below 1.5x ROAS after testing period |
| Campaign briefs lack clarity, causing rework | Brief missing key sections (audience, budget, timeline, KPIs) | Use campaign_brief_generator.py to create structured briefs with all required fields before execution |
| Trend-chasing produces off-brand content | Trend adopted without evaluating brand alignment or resource fit | Run trend_evaluator.py before committing; only pursue trends scoring above 55% on evaluation |

---

## Success Criteria

- Ideas curated to 3-5 maximum per cycle, matched to stage, budget, and goal constraints
- Each implemented idea has a documented hypothesis, success metric, and evaluation date
- 60%+ of implemented ideas produce measurable results within their expected timeline
- Campaign briefs generated for every idea before execution begins
- Trends evaluated systematically before adoption; only "PURSUE" or "EXPERIMENT" rated trends get resources
- Idea backlog maintained and reviewed quarterly; stale ideas pruned
- Focus on 1-2 channels mastered before expanding to additional channels
