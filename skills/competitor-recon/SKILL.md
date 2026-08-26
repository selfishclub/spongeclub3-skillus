---
name: competitor-recon
description: "Run a professional-grade market-research process — interview, market sizing, competitor teardown, framework analysis (STP, Five Forces, JTBD, SWOT), and 'why it blew up' growth deconstruction — then deliver a source-backed, high-visibility report a non-expert can act on. Use whenever the user wants market research, a competitive landscape, to benchmark competitors, research before starting a business or campaign, compare products/pricing/positioning, understand how a competitor got popular, or prep the 'competition' section of a pitch, plan, or brief. Triggers on market research, competitor analysis, competitive landscape, market sizing, benchmarking, positioning research, go-to-market research, 시장조사, 경쟁사 분석, 경쟁사 데이터, 벤치마킹, 포지셔닝, 리서치."
allowed-tools: ["Bash", "Read", "Write", "WebSearch"]
---

# Competitor Recon

Runs the market-research process a professional strategy/insights team actually
uses — **interview → market framing → competitor collection → framework analysis
→ growth deconstruction → a high-visibility, source-backed report** — so a
non-expert gets a pro-quality result by following one path.

It merges a reliable web-collection layer (Firecrawl) with the standard analyst
toolkit. Three things make it professional rather than a scrape: it **frames the
market with real frameworks**, it **verifies every number**, and it **explains
how competitors actually rose**, not just what they sell.

## Operating principles
- **Interview before researching.** Understand the decision first (Step 0).
- **Follow the frameworks — they're the "must-do" of the profession.** Don't
  improvise the analysis; run the named frameworks in `references/frameworks.md`.
- **Breadth:** 5–7 direct + 2–3 adjacent competitors.
- **Every number is sourced and confidence-tagged** (✅/🟡/⚠️).
- **Visibility is a feature, not a nicety.** Lead with a one-screen summary,
  use scorecards/maps/cards. Follow `references/report-template.md`.

Bundled references — read the relevant one when you reach that stage:
- `references/frameworks.md` — TAM/SAM/SOM, JTBD, Five Forces, STP, 4P/7P, positioning map, SWOT.
- `references/rise-to-fame.md` — how to reverse-engineer why a brand blew up.
- `references/report-template.md` — the visibility-first output structure.

---

## STEP 0 — Interview (always first)
Even if the user gave a one-liner, ask a short focused set before spending
credits. Adapt to what's already answered:
1. **Goal / decision** this research informs (enter market? price? position? pitch?).
2. **Category & geography** (exact product + market).
3. **Competitors** already in mind (you'll expand to 5–7 + adjacent).
4. **Dimensions** that matter most (offer defaults: positioning, pricing, audience, channel, messaging, visual, growth story).
5. **Depth & format** (one-pager vs deep teardown; table/slide/doc).

Reflect back a one-paragraph research plan, then proceed. If told "just go," use
sensible defaults but state your assumptions.

## STEP 1 — Frame the market (secondary research the pros never skip)
Before competitors, establish the playing field using `references/frameworks.md`:
- **TAM / SAM / SOM** — size the opportunity with sourced numbers.
- **Jobs-To-Be-Done** — what customers actually hire this category for.
- **Porter's Five Forces** — is the market attractive or brutal?

Use `WebSearch` + the `search` command for industry size, trends, and reports.
This is what makes the later competitor data *mean* something.

## STEP 2 — Build the competitor set
Assemble **5–7 direct** (same job, same buyer) + **2–3 adjacent/indirect**
(different form, same need). Discover missing ones via `WebSearch`
("top [category] brands", "alternatives to X"). List them for a quick veto
before scraping.

## STEP 3 — Collect (Firecrawl layer)
Uses the bundled script; needs `FIRECRAWL_API_KEY` (see README) — if missing,
stop and tell the user how to set it. **Record the source URL + access date for
every page** (needed for the credibility layer).

```bash
# clean page text
python3 ~/.claude/skills/competitor-recon/scripts/fc.py markdown "URL" --main-only
# screenshot (always grab visuals)
python3 ~/.claude/skills/competitor-recon/scripts/fc.py screenshot "URL" -o recon/<brand>/home.png
# campaign/creative images — pull actual campaign visuals + captions and download them
python3 ~/.claude/skills/competitor-recon/scripts/fc.py images "URL" --limit 8 --output recon/<brand>/campaign
# find pages/prices you don't have
python3 ~/.claude/skills/competitor-recon/scripts/fc.py search "brand price positioning" --limit 5
# structured fields via JSON schema
python3 ~/.claude/skills/competitor-recon/scripts/fc.py extract "URL" --schema schema.json --prompt "..."
# breadth crawl (1 credit/page — set --limit)
python3 ~/.claude/skills/competitor-recon/scripts/fc.py crawl "URL" --limit 30 --output recon/<brand>/
```
Save under `recon/<brand>/` as a reusable library.

**Collect visual evidence, not just text.** When a competitor's creative matters —
their campaigns, key visuals, product shots — use the `images` command to pull the
actual campaign imagery (e.g. researching Nike → grab the "Just Do It" / Dream
Crazy campaign visuals). Download them so the report can *show* the creative, not
just describe it. Always record each image's source page + caption for the
credibility layer. Prefer real campaign/creative imagery over UI chrome (the
command already skips logos/icons).

## STEP 4 — Analyze with the frameworks
Run these (details in `references/frameworks.md`) — this is the professional core:
- **STP** — segment the market, pick the winnable target, draft a positioning statement.
- **4P / 7P teardown** — one comparable row per competitor.
- **Positioning map** — plot on the 2 axes that matter for THIS decision; mark white space.

**Verify as you go (non-negotiable):** cite each data point's URL; tag ✅ confirmed
(official page) / 🟡 third-party (marketplace/press) / ⚠️ unverified; cross-check
anything surprising with a second source; prefer primary sources; never invent —
write "not found" instead.

## STEP 5 — Deconstruct the winners' rise
For the 2–3 breakout competitors, run `references/rise-to-fame.md`: trace the 6
growth levers (origin spark → ignition channel → scarcity mechanic → community →
collab → emotional core), lay them on a dated timeline, and separate 🔁 repeatable
moves from 🎲 luck. This turns "what they sell" into "how you could rise too."

## STEP 6 — Report (visibility-first)
Assemble per `references/report-template.md`. Non-negotiables:
- **One-screen summary first** — market size, the job, the white space, recommended
  positioning, top-3 moves. It must stand alone.
- **Scorecard table** with rating dots (●●●●○) and confidence tags.
- **Positioning map** showing the gap.
- **Rise-to-fame cards** for the breakout brands.
- **Embed real campaign imagery.** Where a competitor's creative is part of the
  story, show the downloaded campaign images inline (markdown `![caption](path)`)
  with a caption + source URL + date — so the user *sees* what a competitor ran,
  not just reads about it. Keep to the few most illustrative per brand.
- **SWOT + 3 "so-what" moves** for the user's own venture.
- **Sources & confidence** section listing every data point.

The payoff is **Gaps & opportunities**: the point of all this is to find the space
competitors left open and hand the user a defensible move — never to copy them.

## Legal & ethical guardrails
Research and inspiration only. Study patterns, adapt into original work — never
copy competitor copy, characters, or designs verbatim (major toy/character IP is
strongly protected). The deliverable is *direction for original work*, not a clone.

---
**Credits / inspiration:** collection layer built on the public
[Firecrawl](https://www.firecrawl.dev) SDK; analysis framework inspired by
ComposioHQ's `competitive-ads-extractor` and Sumant Subrahmanya's competitor-ads
use case (Lenny's Newsletter), extended with standard market-research frameworks.
Rewritten as original work for this skill.
