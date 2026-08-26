#!/usr/bin/env python3
"""
source_quality_scorer.py — Score literature sources on quality + relevance.

Reads a JSON of sources with metadata; rates each on 6 quality dimensions
(methodology, sample, peer review, reproducibility, recency, citation
impact) + relevance to research question; triages as include / exclude /
read-in-full.

Stdlib only. JSON or markdown output.

Usage:
    python3 source_quality_scorer.py --input sources.json
    python3 source_quality_scorer.py --input sources.json --format markdown

Input schema:
{
  "as_of": "2026-05-27",
  "research_question": "...",
  "sources": [
      {
          "id": "S-001",
          "title": "Effects of X on Y in Z",
          "authors": ["Smith J","Lee A"],
          "year": 2023,
          "venue": "Journal Name",
          "venue_tier": "tier1",        # tier1|tier2|tier3|tier4|tier5
          "peer_reviewed": true,
          "method_described": true,
          "sample_size_adequate": true,
          "data_or_code_available": false,
          "study_type": "RCT",          # RCT|cohort|case-control|review|case-study|theoretical|other
          "citation_count": 47,
          "preprint": false,
          "retracted": false,
          "relevance_to_question": "high"   # high|medium|low
      }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


VENUE_TIER_SCORES = {"tier1": 20, "tier2": 15, "tier3": 10, "tier4": 5, "tier5": 2}
STUDY_TYPE_SCORES = {
    "systematic-review": 15, "meta-analysis": 15, "rct": 15,
    "cohort": 12, "case-control": 10, "case-study": 7,
    "review": 8, "theoretical": 8, "other": 5,
}


@dataclass
class Assessment:
    id: str
    title: str
    quality_score: int
    relevance_score: int
    total_score: int
    decision: str
    notes: list[str]


def score_source(s: dict[str, Any], current_year: int) -> Assessment:
    notes: list[str] = []
    quality = 0

    # Methodology
    if s.get("method_described"):
        quality += 10
    else:
        notes.append("method not described")

    study = (s.get("study_type") or "other").lower().replace(" ", "-")
    quality += STUDY_TYPE_SCORES.get(study, 5)
    notes.append(f"study type: {study}")

    # Sample
    if s.get("sample_size_adequate"):
        quality += 8
    else:
        notes.append("sample adequacy unclear")

    # Peer review
    if s.get("peer_reviewed"):
        quality += 10
    elif s.get("preprint"):
        quality += 3
        notes.append("preprint (not peer-reviewed)")
    else:
        quality += 1
        notes.append("not peer-reviewed")

    # Reproducibility
    if s.get("data_or_code_available"):
        quality += 8
    else:
        notes.append("data/code not available")

    # Recency
    year = int(s.get("year", 0) or 0)
    if year > 0:
        age = max(0, current_year - year)
        if age <= 2:
            quality += 10
        elif age <= 5:
            quality += 7
        elif age <= 10:
            quality += 4
        else:
            quality += 1
            notes.append(f"older source ({year})")

    # Venue
    tier = (s.get("venue_tier") or "tier3").lower()
    quality += VENUE_TIER_SCORES.get(tier, 5)

    # Citation impact
    cites = int(s.get("citation_count", 0) or 0)
    age = max(1, current_year - year) if year > 0 else 1
    cites_per_year = cites / age
    if cites_per_year >= 30:
        quality += 10
        notes.append(f"high citation impact ({cites_per_year:.1f}/yr)")
    elif cites_per_year >= 10:
        quality += 7
    elif cites_per_year >= 3:
        quality += 4
    else:
        quality += 1

    # Penalties
    if s.get("retracted"):
        quality -= 100
        notes.append("RETRACTED — exclude")

    quality = max(0, min(100, quality))

    relevance = {"high": 100, "medium": 60, "low": 25}.get(
        (s.get("relevance_to_question") or "medium").lower(), 50,
    )

    total = round(quality * 0.6 + relevance * 0.4)

    if s.get("retracted"):
        decision = "exclude (retracted)"
    elif total >= 75:
        decision = "include (read in full)"
    elif total >= 55:
        decision = "candidate (read in full to decide)"
    elif total >= 35:
        decision = "marginal (skim first; exclude unless surprising)"
    else:
        decision = "exclude"

    return Assessment(
        id=s.get("id", ""),
        title=s.get("title", ""),
        quality_score=quality,
        relevance_score=relevance,
        total_score=total,
        decision=decision,
        notes=notes,
    )


def score_all(state: dict[str, Any]) -> dict[str, Any]:
    sources = state.get("sources", []) or []
    current_year = date.today().year
    results = [score_source(s, current_year) for s in sources]
    results.sort(key=lambda r: r.total_score, reverse=True)
    decision_counts: dict[str, int] = {}
    for r in results:
        decision_counts[r.decision] = decision_counts.get(r.decision, 0) + 1
    return {
        "as_of": state.get("as_of", ""),
        "research_question": state.get("research_question", ""),
        "source_count": len(sources),
        "decision_counts": decision_counts,
        "sources": [
            {
                "id": r.id, "title": r.title,
                "quality_score": r.quality_score,
                "relevance_score": r.relevance_score,
                "total_score": r.total_score,
                "decision": r.decision,
                "notes": r.notes,
            }
            for r in results
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append("# Source Quality Assessment\n")
    if report.get("research_question"):
        lines.append(f"**Question:** {report['research_question']}\n")
    lines.append(f"**Sources:** {report['source_count']}\n")
    lines.append("## Decision counts")
    for d, n in report["decision_counts"].items():
        lines.append(f"- {d}: {n}")
    lines.append("")
    lines.append("## Sources (ranked by total score)")
    lines.append("| ID | Quality | Relevance | Total | Decision | Title |")
    lines.append("|----|---------|-----------|-------|----------|-------|")
    for r in report["sources"]:
        title = (r["title"][:60] + "…") if len(r["title"]) > 60 else r["title"]
        lines.append(f"| {r['id']} | {r['quality_score']}/100 | {r['relevance_score']}/100 | "
                    f"{r['total_score']} | {r['decision']} | {title} |")
    lines.append("")
    lines.append("## Per-source notes")
    for r in report["sources"]:
        if r["notes"]:
            lines.append(f"### {r['id']} — {r['title']}")
            for n in r["notes"]:
                lines.append(f"- {n}")
            lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Score literature sources on quality + relevance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of sources")
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

    report = score_all(state)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
