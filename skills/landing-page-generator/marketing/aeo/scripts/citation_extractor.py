#!/usr/bin/env python3
"""
citation_extractor.py — Extract brand citations + URLs from LLM response transcripts.

Reads a JSON or text file containing LLM responses; identifies:
  - URL citations (cited sources)
  - Brand mentions (from a provided brand list)
  - Sentiment context (positive/neutral/negative around each mention)
  - Share of voice across brands

Stdlib only. Markdown or JSON.

Input format (JSON):
    [
      {
        "query": "What is the best CRM?",
        "llm": "ChatGPT",
        "response": "The most popular CRM tools include Salesforce, HubSpot, ...",
        "citations": ["https://example.com/source1"]
      },
      ...
    ]

Or plain-text file with one response per double-newline-separated block.

Usage:
    python3 citation_extractor.py --responses responses.json --brands "Your Brand,Competitor A,Competitor B"
    python3 citation_extractor.py --responses transcripts.txt --brands "Acme,Globex" --format json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any


URL_RE = re.compile(r"https?://[^\s\)\]\}\>\"]+")


# Sentiment indicator words (basic heuristic; not a replacement for proper sentiment analysis)
POSITIVE_WORDS = {
    "best", "leading", "top", "excellent", "recommended", "favorite", "preferred",
    "outstanding", "superior", "winning", "first", "trusted", "popular", "premier",
    "proven", "powerful", "robust", "reliable", "successful", "innovative",
}
NEGATIVE_WORDS = {
    "worst", "poor", "bad", "weak", "outdated", "deprecated", "lagging",
    "inferior", "failing", "questionable", "unreliable", "abandoned", "discontinued",
    "criticized", "controversial", "lawsuit", "scandal",
}


@dataclass
class Mention:
    query: str
    llm: str
    brand: str
    context_snippet: str
    sentiment: str  # positive / neutral / negative
    cited_with_url: bool


@dataclass
class Report:
    total_responses: int
    brand_mentions_count: int
    per_brand_mentions: dict[str, int]
    per_brand_sentiment: dict[str, dict[str, int]]
    per_llm_mentions: dict[str, int]
    share_of_voice_pct: dict[str, float]
    mentions: list[Mention]
    cited_urls: list[str]


def classify_sentiment(context: str, brand: str) -> str:
    """Naive sentiment based on nearby positive/negative words."""
    context_lower = context.lower()
    pos = sum(1 for w in POSITIVE_WORDS if w in context_lower)
    neg = sum(1 for w in NEGATIVE_WORDS if w in context_lower)
    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    return "neutral"


def extract_mentions(query: str, llm: str, response: str, brands: list[str], citations: list[str]) -> list[Mention]:
    """Find brand mentions in response with context."""
    mentions: list[Mention] = []
    for brand in brands:
        pattern = re.compile(r"\b" + re.escape(brand) + r"\b", re.IGNORECASE)
        for match in pattern.finditer(response):
            # Get context around mention (50 chars before + 100 chars after)
            start = max(0, match.start() - 50)
            end = min(len(response), match.end() + 100)
            context = response[start:end].strip()
            sentiment = classify_sentiment(context, brand)
            # Check if any citation URL contains brand domain (rough proxy)
            cited = any(brand.lower().replace(" ", "") in c.lower() for c in citations)
            mentions.append(Mention(
                query=query,
                llm=llm,
                brand=brand,
                context_snippet=context[:200],
                sentiment=sentiment,
                cited_with_url=cited,
            ))
    return mentions


def parse_responses(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    suffix = path.suffix.lower()
    if suffix == ".json":
        data = json.loads(text)
        if isinstance(data, list):
            return data
        return [data]
    # Plain text: split by double-newline; each block is one response
    blocks = [b.strip() for b in text.split("\n\n\n") if b.strip()]
    return [{"query": "<unknown>", "llm": "<unknown>", "response": b, "citations": []} for b in blocks]


def analyze(responses: list[dict[str, Any]], brands: list[str]) -> Report:
    all_mentions: list[Mention] = []
    per_brand: dict[str, int] = defaultdict(int)
    per_brand_sentiment: dict[str, dict[str, int]] = defaultdict(lambda: {"positive": 0, "neutral": 0, "negative": 0})
    per_llm: dict[str, int] = defaultdict(int)
    cited_urls_set: set[str] = set()

    for r in responses:
        query = r.get("query", "<unknown>")
        llm = r.get("llm", "<unknown>")
        response_text = r.get("response", "")
        citations = r.get("citations", []) or []
        # Extract URLs from response text too
        extracted_urls = URL_RE.findall(response_text)
        all_citations = list(set(citations + extracted_urls))
        cited_urls_set.update(all_citations)

        mentions = extract_mentions(query, llm, response_text, brands, all_citations)
        all_mentions.extend(mentions)
        for m in mentions:
            per_brand[m.brand] += 1
            per_brand_sentiment[m.brand][m.sentiment] += 1
            per_llm[m.llm] += 1

    total_mentions = sum(per_brand.values())
    sov: dict[str, float] = {}
    if total_mentions > 0:
        for brand, count in per_brand.items():
            sov[brand] = round(100 * count / total_mentions, 1)

    return Report(
        total_responses=len(responses),
        brand_mentions_count=total_mentions,
        per_brand_mentions=dict(per_brand),
        per_brand_sentiment={k: dict(v) for k, v in per_brand_sentiment.items()},
        per_llm_mentions=dict(per_llm),
        share_of_voice_pct=sov,
        mentions=all_mentions,
        cited_urls=sorted(cited_urls_set),
    )


def render_markdown(r: Report) -> str:
    out = ["# LLM Citation Extraction Report", ""]
    out.append(f"_Responses analyzed: {r.total_responses}_")
    out.append(f"_Total brand mentions: {r.brand_mentions_count}_")
    out.append("")
    out.append("## Share of Voice")
    out.append("")
    out.append("| Brand | Mentions | SOV % |")
    out.append("|-------|----------|-------|")
    for brand, count in sorted(r.per_brand_mentions.items(), key=lambda x: -x[1]):
        sov = r.share_of_voice_pct.get(brand, 0)
        out.append(f"| {brand} | {count} | {sov}% |")
    out.append("")
    out.append("## Sentiment by Brand")
    out.append("")
    out.append("| Brand | Positive | Neutral | Negative |")
    out.append("|-------|----------|---------|----------|")
    for brand, sentiments in r.per_brand_sentiment.items():
        out.append(f"| {brand} | {sentiments['positive']} | {sentiments['neutral']} | {sentiments['negative']} |")
    out.append("")
    out.append("## Mentions by LLM")
    out.append("")
    out.append("| LLM | Mentions |")
    out.append("|-----|----------|")
    for llm, count in sorted(r.per_llm_mentions.items(), key=lambda x: -x[1]):
        out.append(f"| {llm} | {count} |")
    out.append("")
    if r.cited_urls:
        out.append(f"## Cited URLs ({len(r.cited_urls)})")
        out.append("")
        for url in r.cited_urls[:50]:
            out.append(f"- {url}")
        if len(r.cited_urls) > 50:
            out.append(f"... and {len(r.cited_urls) - 50} more")
        out.append("")
    # Sample negative mentions (worth investigation)
    negative = [m for m in r.mentions if m.sentiment == "negative"]
    if negative:
        out.append(f"## ⚠️ Negative Mentions ({len(negative)}) — investigate")
        out.append("")
        for m in negative[:20]:
            out.append(f"- **{m.brand}** ({m.llm}): \"{m.context_snippet}\"")
        out.append("")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Extract brand citations + mentions from LLM responses",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--responses", required=True, help="JSON or text file with LLM responses")
    p.add_argument("--brands", required=True, help="Comma-separated brand names to track")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", help="Output file path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        responses = parse_responses(Path(args.responses))
    except (OSError, json.JSONDecodeError) as e:
        print(f"error loading responses: {e}", file=sys.stderr)
        return 2
    brands = [b.strip() for b in args.brands.split(",") if b.strip()]
    r = analyze(responses, brands)
    if args.format == "json":
        out = json.dumps(asdict(r), indent=2, default=str)
    else:
        out = render_markdown(r)
    if args.output:
        Path(args.output).write_text(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
