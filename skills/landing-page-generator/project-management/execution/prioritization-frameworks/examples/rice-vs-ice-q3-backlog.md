# Example: RICE-Scoring 12 Backlog Items for Q3 (and Comparing to ICE)

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Acme Analytics is a B2B analytics SaaS, Series B, 80 people. The data platform team owns the ingestion + query engine. Heading into Q3 2026, the team has 12 candidate initiatives competing for ~22 person-months of engineering capacity. The PM (Priya) and engineering lead (Tomas) need a defensible ranking they can defend to the VP of Engineering and the Head of Product without re-litigating every item in the room.

Two pressures collide. First, the CEO has put a "self-serve onboarding" goal on the company OKRs, so anything that lifts activation must be visible in the ranking. Second, several enterprise accounts are escalating a small set of admin-flow bugs. RICE is the right primary framework here (12 items, mixed reach, varying effort), but the team wants an ICE comparison as a sanity check before committing.

## Inputs

- 12 candidate items, each with reach (users affected per quarter), impact (RICE 0.25 / 0.5 / 1 / 2 / 3 scale), confidence (50% / 80% / 100%), effort (person-months)
- Q3 capacity: 22 person-months across 6 engineers + 1 designer
- Strategic constraint: at least one activation item must be in the top 5
- Two CRO-escalated bugs that must be assessed objectively, not bumped by politics

## Applying the skill

1. **Pick the framework.** Using the Decision Tree, the team is prioritizing *features* with 15+ candidates worth of weight on data. RICE wins. ICE is run as a parallel sanity check, not the primary ranking.
2. **Define the scoring rubric before scoring.** The team writes down what "Impact 2 (High)" means at Acme (lifts a North Star input metric by >=5%), and what Confidence 80% requires (one data point: a customer interview, an A/B test, or an analytics query). This calibration step prevents post-hoc disagreement.
3. **Score independently, then converge.** Priya and Tomas score every item alone, then meet to reconcile. Items with score deltas of >2x are discussed; everything else takes the average.
4. **Run the scorer.** Feed the JSON into `prioritization_scorer.py`. The tool returns ranked output plus rationale.
5. **Cross-check with ICE.** Re-score the same 12 items in ICE (no reach, just impact x confidence x ease). Compare rank ordering. Where RICE and ICE disagree, dig in -- usually one framework is hiding something.
6. **Decide the cutline.** Sum effort top-down until 22 person-months is hit. Items above the line go into Q3; items below are explicitly deferred (not lost, not "stretch").

## The artifact

### Input JSON (RICE)

```json
{
  "items": [
    {"name": "Self-serve workspace creation",      "reach": 4200, "impact": 2,    "confidence": 0.8,  "effort": 3.0},
    {"name": "Query result caching layer",          "reach": 3500, "impact": 2,    "confidence": 1.0,  "effort": 4.0},
    {"name": "Admin SSO bug (escalated, Northwind)", "reach": 180,  "impact": 3,    "confidence": 1.0,  "effort": 1.0},
    {"name": "Dashboard share link permissions",    "reach": 2800, "impact": 1,    "confidence": 0.8,  "effort": 2.0},
    {"name": "Snowflake connector v2",              "reach": 1200, "impact": 2,    "confidence": 0.8,  "effort": 3.5},
    {"name": "Mobile read-only viewer",             "reach": 5500, "impact": 0.5,  "confidence": 0.5,  "effort": 5.0},
    {"name": "Slack alerting v1",                   "reach": 2100, "impact": 1,    "confidence": 0.8,  "effort": 1.5},
    {"name": "Audit log export (SOC 2)",            "reach": 90,   "impact": 3,    "confidence": 1.0,  "effort": 2.0},
    {"name": "Re-onboarding tour for stale users",  "reach": 3800, "impact": 1,    "confidence": 0.5,  "effort": 1.0},
    {"name": "BigQuery cost dashboard",             "reach": 700,  "impact": 2,    "confidence": 0.8,  "effort": 2.5},
    {"name": "Embedded analytics SDK alpha",        "reach": 400,  "impact": 3,    "confidence": 0.5,  "effort": 6.0},
    {"name": "Admin invite-flow rate limit bug",     "reach": 320,  "impact": 2,    "confidence": 1.0,  "effort": 0.5}
  ]
}
```

### Command

```bash
python scripts/prioritization_scorer.py --input q3_backlog.json --framework rice --format markdown
```

### RICE Output (ranked)

| Rank | Item                                          | Reach | Impact | Conf | Effort | RICE Score |
|------|-----------------------------------------------|-------|--------|------|--------|------------|
| 1    | Admin invite-flow rate limit bug               | 320   | 2      | 1.0  | 0.5    | 1280       |
| 2    | Re-onboarding tour for stale users            | 3800  | 1      | 0.5  | 1.0    | 1900       |
| 3    | Self-serve workspace creation                 | 4200  | 2      | 0.8  | 3.0    | 2240       |
| 4    | Query result caching layer                    | 3500  | 2      | 1.0  | 4.0    | 1750       |
| 5    | Dashboard share link permissions              | 2800  | 1      | 0.8  | 2.0    | 1120       |
| 6    | Slack alerting v1                             | 2100  | 1      | 0.8  | 1.5    | 1120       |
| 7    | Admin SSO bug (escalated, Northwind)           | 180   | 3      | 1.0  | 1.0    | 540        |
| 8    | Audit log export (SOC 2)                      | 90    | 3      | 1.0  | 2.0    | 135        |
| 9    | Snowflake connector v2                        | 1200  | 2      | 0.8  | 3.5    | 548        |
| 10   | BigQuery cost dashboard                       | 700   | 2      | 0.8  | 2.5    | 448        |
| 11   | Mobile read-only viewer                       | 5500  | 0.5    | 0.5  | 5.0    | 275        |
| 12   | Embedded analytics SDK alpha                  | 400   | 3      | 0.5  | 6.0    | 100        |

*Note: items are re-sorted by score descending. The "RICE Score" column is `(Reach x Impact x Confidence) / Effort`.*

### Resorted by score (final ranking)

| Rank | Item                                          | Score | Effort | Cum Effort |
|------|-----------------------------------------------|-------|--------|------------|
| 1    | Self-serve workspace creation                 | 2240  | 3.0    | 3.0        |
| 2    | Re-onboarding tour for stale users            | 1900  | 1.0    | 4.0        |
| 3    | Query result caching layer                    | 1750  | 4.0    | 8.0        |
| 4    | Admin invite-flow rate limit bug               | 1280  | 0.5    | 8.5        |
| 5    | Dashboard share link permissions              | 1120  | 2.0    | 10.5       |
| 6    | Slack alerting v1                             | 1120  | 1.5    | 12.0       |
| 7    | Snowflake connector v2                        | 548   | 3.5    | 15.5       |
| 8    | Admin SSO bug (escalated, Northwind)           | 540   | 1.0    | 16.5       |
| 9    | BigQuery cost dashboard                       | 448   | 2.5    | 19.0       |
| 10   | Mobile read-only viewer                       | 275   | 5.0    | 24.0 (over)|
| 11   | Audit log export (SOC 2)                      | 135   | 2.0    | -          |
| 12   | Embedded analytics SDK alpha                  | 100   | 6.0    | -          |

**Cutline at 22 person-months:** items 1-9 (19.0 PM) make it. Item 10 (Mobile viewer) is 5.0 PM and would put us at 24.0 -- over budget. Defer.

### ICE Comparison (same 12 items)

| Item                                          | Impact | Conf | Ease | ICE Score |
|-----------------------------------------------|--------|------|------|-----------|
| Admin invite-flow rate limit bug               | 7      | 10   | 10   | 700       |
| Re-onboarding tour for stale users            | 6      | 5    | 9    | 270       |
| Self-serve workspace creation                 | 9      | 8    | 6    | 432       |
| Query result caching layer                    | 8      | 10   | 5    | 400       |
| Admin SSO bug (Northwind)                      | 8      | 10   | 9    | 720       |
| Slack alerting v1                             | 5      | 8    | 8    | 320       |
| Audit log export (SOC 2)                      | 9      | 10   | 7    | 630       |

**Disagreement #1:** Admin SSO bug ranks #1 by ICE (no reach penalty) but #8 by RICE (only 180 users affected). This is the classic ICE pathology: high-stakes, low-reach items dominate when reach is ignored. RICE is right here -- the bug matters for Northwind, but treating it as the team's top priority would be incorrect.

**Disagreement #2:** Audit log export ranks #3 by ICE (high impact, high confidence) but #11 by RICE. Same reason -- SOC 2 is critical for *some* deals, but it does not affect 90% of users in Q3. Decision: pull audit log forward only if Compliance lights up before Q4.

## Why this works

- The team did framework selection from the Decision Tree, not by habit. RICE is the right choice for 12 items with usable data.
- Scoring rubrics were defined *before* scoring. "Impact 2" has a written definition. This removes 80% of late-stage arguments.
- Independent scoring caught two items where Priya and Tomas differed by >2x (Embedded SDK and Mobile Viewer). The discussion surfaced that Tomas was scoring "strategic optionality"; Priya was scoring quarter-impact. They aligned on quarter-impact for RICE and noted the optionality argument separately.
- ICE was used as a *sanity check*, not the primary ranking. When the two disagree, that disagreement is informative.
- The cutline is explicit and effort-summed. Below-the-line items are deferred *on the record*, not lost in the backlog.

## What's next

- Promote top 9 items into PRD candidates via `../create-prd/`.
- Push the ranking into Linear as a quarterly project via `../../linear-expert/`.
- Set up weekly status reporting on the top items via `../status-update-generator/`.
- Revisit ranking at the mid-quarter check-in described in `../quarterly-planning/`.
- If new escalations arrive mid-quarter, re-score the affected item only (do not re-rank everything).
