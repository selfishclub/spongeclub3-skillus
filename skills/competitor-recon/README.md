# Competitor Recon 🔍

A single Claude Code skill that runs the whole competitive-creative loop:
**collect competitors' real ads & landing pages → analyze what's working → report benchmarks you can act on.**

It merges two ideas into one skill:
- a reliable **web-collection layer** (built on the public [Firecrawl](https://www.firecrawl.dev) SDK), and
- a **creative-analysis framework** for reading competitor messaging, hooks, visual patterns, and positioning.

Built for art directors, strategists, and marketers prepping campaign direction, pitch decks, or briefs.

## Install

```bash
git clone https://github.com/Koo-bon/competitor-recon
cp -r competitor-recon ~/.claude/skills/
pip install -r ~/.claude/skills/competitor-recon/requirements.txt
```

Restart Claude Code so the skill loads.

## Setup: Firecrawl API key (required)

The collection scripts call Firecrawl, so you need a free API key.

1. Get a key at https://www.firecrawl.dev (free tier available).
2. Make it available to the skill — either export it:
   ```bash
   export FIRECRAWL_API_KEY="fc-your-key-here"
   ```
   or put it in a `.env` file in your home directory (`~/.env`):
   ```
   FIRECRAWL_API_KEY=fc-your-key-here
   ```

⚠️ **Never commit your API key or a `.env` file to GitHub.** The `.gitignore` in this repo already excludes `.env`.

## Use

Just talk to Claude Code naturally, e.g.:

- "Benchmark Notion, Coda, and ClickUp's Meta ads — what messaging is working and where's the gap for us?"
- "Scrape these 3 competitor landing pages and give me a positioning teardown for my pitch."

Claude will collect the pages, analyze them, and return a report ending in **Gaps & opportunities** — the open angles you can own.

## Credits

- Collection layer built on the public **Firecrawl** SDK (https://www.firecrawl.dev).
- The ad-analysis framework is **inspired by** ComposioHQ's `competitive-ads-extractor`
  skill and Sumant Subrahmanya's competitor-ads use case (Lenny's Newsletter).
  All code and text in this repo is original work written for this skill.

## License

MIT — see [LICENSE](LICENSE).
