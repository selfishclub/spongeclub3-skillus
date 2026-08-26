# Visibility-First Report Template

The goal: a non-expert can grasp the whole market in one scroll. Lead with the
most legible artifacts; put depth below. Use these visibility devices:

- **Rating dots** for quick comparison: ●●●●● (strong) … ○○○○○ (weak).
- **Confidence tags** on every number: ✅ confirmed / 🟡 third-party / ⚠️ unverified.
- **Quadrant maps** to show white space visually.
- **Compact cards** for per-competitor depth (scannable, not paragraphs).

Assemble in this order:

```markdown
# {Category} Market Recon — {N direct + M adjacent}
*Goal: {interview}. Scope: {category / geo}. As of {date}.*

## ⭐ One-screen summary  ← the single most important artifact, always first
- **Market:** TAM {x} / SAM {y} / SOM {z}  — attractiveness: {verdict}
- **The job customers hire this for:** {JTBD one-liner}
- **Where the white space is:** {one sentence}
- **Our recommended positioning:** {STP positioning statement}
- **Top 3 moves:** 1) … 2) … 3) …

## 1. Competitor scorecard (heatmap-style)
| Brand | Positioning | Selling point | Price | Target | Brand power | Growth engine |
|-------|-------------|---------------|-------|--------|-------------|---------------|
| A | ... | ... | $x ✅ | ... | ●●●●○ | blind-box+collab |
(rating dots make strength scannable; every number tagged)

## 2. Positioning map
Quadrant on the 2 axes that matter for this decision. White space marked.

## 3. Market framing
TAM/SAM/SOM (sourced) + Porter's Five Forces rating table + verdict.

## 4. Jobs-To-Be-Done
The 1–3 jobs, each mapped to the competitor that owns it.

## 5. Rise-to-fame cards  ← for the 2–3 breakout brands
Compact card each (see rise-to-fame.md): emotional core, lever sequence,
timeline, 🔁 repeatable vs 🎲 can't-copy. **Embed the brand's actual campaign
images** (downloaded via `fc.py images`) inline so the creative is visible:

```markdown
![Nike Dream Crazy key visual](recon/nike/campaign/img_02.jpg)
*Nike — "Dream Crazy" (2018). Source: nike.com/... · 🟡 third-party · accessed {date}*
```
Show only the few most illustrative per brand; caption + source + confidence tag each.

## 6. Per-competitor teardown (4P/7P)
One compact card per competitor. Product / Price / Place / Promotion, sourced.

## 7. Gaps & opportunities
White space from the map + JTBD nobody serves → concrete directions.

## 8. SWOT for YOUR venture
4 quadrants tied to evidence + 3 "so-what" moves.

## 9. Sources & confidence
Every data point → URL + ✅/🟡/⚠️. List anything unverified honestly.

## 10. Reference library
Saved screenshots + markdown paths.
```

## Legibility rules
- Nothing important hidden in prose — if it's a comparison, it's a table or map.
- Every table cell that's a number carries a confidence tag.
- Cards over paragraphs for per-competitor depth.
- The one-screen summary must stand alone: someone reading only that section
  should still get the decision-useful answer.
