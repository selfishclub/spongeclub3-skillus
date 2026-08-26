#!/usr/bin/env python3
"""
research_synthesis_organizer.py — Organize raw research items into themes
via tag clustering, with segment cross-cuts and quality flags.

Reads a JSON of research items (each with source, date, tags, segment,
quote/observation, sentiment); produces theme clusters grouped by tag,
frequency, cross-segment breakdown, and quality-flag findings (e.g.,
single-session theme = anecdotal).

Stdlib only. JSON or markdown output.

Usage:
    python3 research_synthesis_organizer.py --input research_items.json
    python3 research_synthesis_organizer.py --input research_items.json --format markdown

Input schema:
{
  "as_of": "2026-05-27",
  "study_name": "Onboarding interviews Q2",
  "items": [
      {
          "id": "I-001",
          "source": "interview-007",        # interview-id / survey-row / ticket-id
          "date": "2026-05-10",
          "segment": "smb",                  # any segmentation key
          "tags": ["onboarding-friction","missing-feature","sentiment-negative"],
          "observation": "User couldn't find import option on first try",
          "quote": "I looked everywhere for an Import button.",
          "sentiment": "negative",           # positive|negative|neutral
          "weight": 1                        # optional, default 1
      }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ThemeCluster:
    tag: str
    item_count: int
    unique_source_count: int
    segments: dict[str, int]
    sentiments: dict[str, int]
    confidence: str  # high|medium|low
    quality_flag: str
    sample_quotes: list[str]


def confidence_band(unique_sources: int) -> str:
    if unique_sources >= 5:
        return "high"
    if unique_sources >= 3:
        return "medium"
    return "low"


def quality_flag(unique_sources: int, segments_covered: int) -> str:
    if unique_sources < 2:
        return "anecdotal (single source) — needs more data"
    if unique_sources < 3:
        return "thin (2 sources) — could be selection bias"
    if segments_covered < 2:
        return "single-segment — may not generalize"
    return ""


def organize(state: dict[str, Any]) -> dict[str, Any]:
    items = state.get("items", []) or []
    by_tag: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        for tag in item.get("tags", []) or []:
            by_tag[tag].append(item)

    clusters: list[ThemeCluster] = []
    for tag, tag_items in by_tag.items():
        item_count = sum(int(i.get("weight", 1) or 1) for i in tag_items)
        unique_sources = len({i.get("source", "") for i in tag_items})
        seg_counter: Counter[str] = Counter()
        sent_counter: Counter[str] = Counter()
        for i in tag_items:
            seg = i.get("segment") or "(unsegmented)"
            seg_counter[seg] += 1
            sent_counter[i.get("sentiment", "neutral")] += 1
        sample_quotes = []
        for i in tag_items[:3]:
            q = i.get("quote") or i.get("observation") or ""
            if q:
                sample_quotes.append(q)
        clusters.append(ThemeCluster(
            tag=tag,
            item_count=item_count,
            unique_source_count=unique_sources,
            segments=dict(seg_counter),
            sentiments=dict(sent_counter),
            confidence=confidence_band(unique_sources),
            quality_flag=quality_flag(unique_sources, len(seg_counter)),
            sample_quotes=sample_quotes,
        ))
    clusters.sort(key=lambda c: (c.unique_source_count, c.item_count), reverse=True)

    # Surface anecdotes (single-source items)
    source_counts = Counter(i.get("source", "") for i in items)
    anecdote_count = sum(1 for s, c in source_counts.items() if c >= 5)

    # Segment representation across study
    all_segments = Counter(i.get("segment") or "(unsegmented)" for i in items)

    return {
        "as_of": state.get("as_of", ""),
        "study_name": state.get("study_name", ""),
        "summary": {
            "total_items": len(items),
            "unique_sources": len({i.get("source", "") for i in items}),
            "unique_tags": len(by_tag),
            "vocal_source_count": anecdote_count,
            "segments_in_study": dict(all_segments),
        },
        "theme_clusters": [
            {
                "tag": c.tag,
                "item_count": c.item_count,
                "unique_source_count": c.unique_source_count,
                "segments": c.segments,
                "sentiments": c.sentiments,
                "confidence": c.confidence,
                "quality_flag": c.quality_flag,
                "sample_quotes": c.sample_quotes,
            }
            for c in clusters
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Research Synthesis — {report.get('study_name','(unnamed)')}")
    lines.append(f"_as of {report['as_of']}_\n")
    s = report["summary"]
    lines.append("## Summary")
    lines.append(f"- Items: {s['total_items']}")
    lines.append(f"- Unique sources: {s['unique_sources']}")
    lines.append(f"- Unique tags: {s['unique_tags']}")
    lines.append(f"- Sources contributing ≥5 items (vocal): {s['vocal_source_count']}")
    lines.append("- Segments: " + ", ".join(f"{k} ({v})" for k, v in s["segments_in_study"].items()))
    lines.append("")
    lines.append("## Theme clusters")
    lines.append("| Tag | Items | Sources | Confidence | Flag |")
    lines.append("|-----|-------|---------|------------|------|")
    for c in report["theme_clusters"]:
        lines.append(
            f"| {c['tag']} | {c['item_count']} | {c['unique_source_count']} | "
            f"{c['confidence']} | {c['quality_flag'] or '—'} |"
        )
    lines.append("")
    lines.append("## Cluster detail")
    for c in report["theme_clusters"]:
        lines.append(f"### {c['tag']} ({c['confidence']} confidence)")
        lines.append(f"_items: {c['item_count']} | unique sources: {c['unique_source_count']}_")
        if c["quality_flag"]:
            lines.append(f"\n_flag: {c['quality_flag']}_")
        lines.append("\n**Segments:** " + ", ".join(f"{k} ({v})" for k, v in c["segments"].items()))
        lines.append("**Sentiments:** " + ", ".join(f"{k} ({v})" for k, v in c["sentiments"].items()))
        if c["sample_quotes"]:
            lines.append("\n**Sample quotes:**")
            for q in c["sample_quotes"]:
                lines.append(f"- \"{q}\"")
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Organize raw research items into theme clusters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of research items")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--output", help="Write to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        state = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"error: cannot read input: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 2

    report = organize(state)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
