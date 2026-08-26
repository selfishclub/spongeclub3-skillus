#!/usr/bin/env python3
"""
claim_landscape_mapper.py — Cluster patents by owner, technology
subarea, and recency; surface white space + crowded zones.

Reads a JSON of patents (with assignee, classification, date, claim
type); produces clusters + heatmap + white-space identification.

Stdlib only. JSON or markdown output.

Usage:
    python3 claim_landscape_mapper.py --input patents.json
    python3 claim_landscape_mapper.py --input patents.json --format markdown

Input schema:
{
  "landscape_name": "AI agents 2020-2026",
  "as_of": "2026-05-27",
  "patents": [
      {
          "id": "US11111111B1",
          "title": "...",
          "assignee": "Acme Inc",
          "filing_date": "2023-04-15",
          "publication_date": "2024-10-20",
          "issued": true,
          "classifications": ["G06N3/04","H04L67/01"],
          "primary_classification": "G06N3/04",
          "claim_type": "method",         # method|system|apparatus|composition|use|combination
          "independent_claim_count": 2,
          "citation_count": 5,
          "family_size": 3,
          "status": "active"             # active|expired|pending|abandoned
      }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def cluster_by(patents: list[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for p in patents:
        k = p.get(key, "(unknown)") or "(unknown)"
        out[str(k)].append(p)
    return dict(out)


def by_year(patents: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for p in patents:
        date = p.get("filing_date") or ""
        year = date[:4] if len(date) >= 4 else "(unknown)"
        counts[year] += 1
    return dict(counts)


def heatmap(patents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Per primary classification × per assignee, count patents."""
    cells: dict[tuple[str, str], int] = defaultdict(int)
    for p in patents:
        cls = p.get("primary_classification", "(unknown)") or "(unknown)"
        assignee = p.get("assignee", "(unknown)") or "(unknown)"
        cells[(cls, assignee)] += 1
    return [
        {"classification": cls, "assignee": assignee, "count": count}
        for (cls, assignee), count in cells.items()
    ]


def white_space_candidates(patents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Classifications with thin coverage."""
    cls_counts = Counter(p.get("primary_classification") for p in patents)
    candidates = []
    for cls, count in cls_counts.items():
        if count == 0 or cls is None:
            continue
        if count <= 2:
            candidates.append({"classification": cls, "patent_count": count,
                              "note": "thin coverage; potential white space"})
    return candidates


def crowded_zones(patents: list[dict[str, Any]], threshold: int = 5) -> list[dict[str, Any]]:
    cls_counts = Counter(p.get("primary_classification") for p in patents)
    crowded = []
    for cls, count in cls_counts.items():
        if cls is None:
            continue
        if count >= threshold:
            crowded.append({"classification": cls, "patent_count": count,
                          "note": "crowded; high competitive density"})
    crowded.sort(key=lambda x: -x["patent_count"])
    return crowded


def top_assignees(patents: list[dict[str, Any]], top_n: int = 10) -> list[dict[str, Any]]:
    counts = Counter(p.get("assignee") for p in patents if p.get("assignee"))
    return [{"assignee": a, "patent_count": c}
            for a, c in counts.most_common(top_n)]


def map_landscape(state: dict[str, Any]) -> dict[str, Any]:
    patents = state.get("patents", []) or []
    active = [p for p in patents if (p.get("status") or "").lower() == "active"]
    return {
        "landscape_name": state.get("landscape_name", ""),
        "as_of": state.get("as_of", ""),
        "summary": {
            "total_patents": len(patents),
            "active_patents": len(active),
            "expired_patents": sum(1 for p in patents if (p.get("status") or "").lower() == "expired"),
            "pending_patents": sum(1 for p in patents if (p.get("status") or "").lower() == "pending"),
        },
        "by_year": by_year(patents),
        "top_assignees": top_assignees(patents),
        "by_claim_type": dict(Counter(p.get("claim_type") for p in patents)),
        "heatmap": heatmap(patents),
        "white_space_candidates": white_space_candidates(patents),
        "crowded_zones": crowded_zones(patents),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Patent Landscape — {report.get('landscape_name','(unnamed)')}\n")
    lines.append(f"_as of {report['as_of']}_\n")
    s = report["summary"]
    lines.append("## Summary")
    lines.append(f"- Total: {s['total_patents']}")
    lines.append(f"- Active: {s['active_patents']} | Expired: {s['expired_patents']} | Pending: {s['pending_patents']}\n")
    lines.append("## Filings by year")
    lines.append("| Year | Count |")
    lines.append("|------|-------|")
    for year in sorted(report["by_year"].keys()):
        lines.append(f"| {year} | {report['by_year'][year]} |")
    lines.append("")
    lines.append("## Top assignees")
    lines.append("| Assignee | Patents |")
    lines.append("|----------|---------|")
    for a in report["top_assignees"]:
        lines.append(f"| {a['assignee']} | {a['patent_count']} |")
    lines.append("")
    lines.append("## Claim type distribution")
    lines.append("| Type | Count |")
    lines.append("|------|-------|")
    for k, v in report["by_claim_type"].items():
        lines.append(f"| {k} | {v} |")
    lines.append("")
    if report["crowded_zones"]:
        lines.append("## Crowded zones (high density)")
        for c in report["crowded_zones"]:
            lines.append(f"- {c['classification']} — {c['patent_count']} patents")
        lines.append("")
    if report["white_space_candidates"]:
        lines.append("## White space candidates (thin coverage)")
        for w in report["white_space_candidates"]:
            lines.append(f"- {w['classification']} — {w['patent_count']} patents")
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Map patent landscape",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of patents")
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

    report = map_landscape(state)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
