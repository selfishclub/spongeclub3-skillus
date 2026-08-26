#!/usr/bin/env python3
"""
prior_art_search_planner.py — Build a prior-art search plan from an
invention description.

Reads a JSON describing the invention (claim elements, keywords,
classifications, jurisdictions, filing deadline); produces a search
plan with database list, query strings, search log template.

Stdlib only. JSON or markdown output.

Usage:
    python3 prior_art_search_planner.py --input invention.json
    python3 prior_art_search_planner.py --input invention.json --format markdown

Input schema:
{
  "invention_title": "...",
  "novel_elements": ["element 1","element 2"],
  "keywords": [["term1","synonym1"],["term2","synonym2"]],
  "classifications": ["G06N3/04","H04L63/02"],   # CPC/IPC
  "jurisdictions": ["US","EP","JP","CN"],
  "filing_deadline": "2026-08-15",
  "non_patent_search_areas": ["arxiv","github","conference proceedings"]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DATABASE_RECOMMENDATIONS = {
    "US": ["USPTO (patft + appft)", "Google Patents (US filter)"],
    "EP": ["EPO Espacenet", "Google Patents (EP filter)"],
    "JP": ["JPO J-PlatPat", "Espacenet"],
    "CN": ["CNIPA English", "Espacenet"],
    "WO": ["WIPO PatentScope"],
    "GLOBAL": ["Espacenet (worldwide)", "Google Patents (no filter)"],
}


def build_query_keyword(keywords: list[list[str]]) -> str:
    if not keywords:
        return ""
    groups = []
    for syn_group in keywords:
        if not syn_group:
            continue
        quoted = [f'"{s}"' if " " in s else s for s in syn_group]
        groups.append("(" + " OR ".join(quoted) + ")")
    return " AND ".join(groups)


def build_query_classification(classifications: list[str]) -> str:
    if not classifications:
        return ""
    cls_quoted = [f'CPC="{c}"' for c in classifications]
    return "(" + " OR ".join(cls_quoted) + ")"


def build_plan(spec: dict[str, Any]) -> dict[str, Any]:
    keyword_query = build_query_keyword(spec.get("keywords") or [])
    class_query = build_query_classification(spec.get("classifications") or [])
    combined = " AND ".join(q for q in [keyword_query, class_query] if q)

    jurisdictions = spec.get("jurisdictions") or ["US"]
    databases_to_search: list[dict[str, Any]] = []
    seen = set()
    for j in jurisdictions:
        for db in DATABASE_RECOMMENDATIONS.get(j, []):
            if db not in seen:
                databases_to_search.append({
                    "database": db,
                    "for_jurisdiction": j,
                    "primary_query": combined or keyword_query,
                    "filters": {
                        "publication_date_max": spec.get("filing_deadline", ""),
                    },
                })
                seen.add(db)
    # Always add Espacenet worldwide
    if "Espacenet (worldwide)" not in seen:
        databases_to_search.append({
            "database": "Espacenet (worldwide)",
            "for_jurisdiction": "GLOBAL",
            "primary_query": combined or keyword_query,
            "filters": {
                "publication_date_max": spec.get("filing_deadline", ""),
            },
        })

    npl_sources = spec.get("non_patent_search_areas") or ["academic literature"]

    return {
        "invention_title": spec.get("invention_title", ""),
        "filing_deadline": spec.get("filing_deadline", ""),
        "novel_elements": spec.get("novel_elements") or [],
        "patent_searches": databases_to_search,
        "non_patent_searches": [
            {"source": s, "rationale": "non-patent prior art per area"}
            for s in npl_sources
        ],
        "citation_walking": [
            "From each top-3 hit per database, walk backward + forward citations",
            "Note non-patent literature cited",
        ],
        "search_log_template": {
            "date_executed": "YYYY-MM-DD",
            "database": "",
            "query": "",
            "filters": "",
            "total_hits": 0,
            "relevant_hits": 0,
            "notes_per_relevant_hit": [],
        },
        "warnings": _warnings(spec),
    }


def _warnings(spec: dict[str, Any]) -> list[str]:
    out = []
    if not spec.get("classifications"):
        out.append("No CPC/IPC classifications provided — keyword-only search misses art that uses different terms")
    if not spec.get("non_patent_search_areas"):
        out.append("Non-patent prior art not planned — in software/biotech, this is often >50% of relevant art")
    jur = spec.get("jurisdictions") or []
    if len(jur) == 1:
        out.append(f"Searching only {jur[0]} — international art (especially JP/CN/EP) may be missed")
    if not spec.get("filing_deadline"):
        out.append("Filing deadline not set — calibrate search depth accordingly")
    return out


def render_markdown(plan: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Prior-Art Search Plan — {plan.get('invention_title','(unnamed)')}\n")
    lines.append(f"**Filing deadline:** {plan.get('filing_deadline','(not set)')}\n")
    lines.append("## Novel elements claimed")
    for el in plan.get("novel_elements", []):
        lines.append(f"- {el}")
    lines.append("")
    lines.append("## Patent searches")
    for db in plan["patent_searches"]:
        lines.append(f"### {db['database']} (for {db['for_jurisdiction']})")
        lines.append(f"**Query:**\n```\n{db['primary_query']}\n```")
        lines.append(f"**Filters:** publication_date_max: {db['filters']['publication_date_max']}\n")
    lines.append("## Non-patent searches")
    for s in plan["non_patent_searches"]:
        lines.append(f"- {s['source']}")
    lines.append("")
    lines.append("## Citation walking")
    for c in plan["citation_walking"]:
        lines.append(f"- {c}")
    lines.append("")
    if plan["warnings"]:
        lines.append("## Warnings")
        for w in plan["warnings"]:
            lines.append(f"- {w}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Build a prior-art search plan",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of invention spec")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--output", help="Write to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        spec = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"error: cannot read input: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 2

    plan = build_plan(spec)
    out = render_markdown(plan) if args.format == "markdown" else json.dumps(plan, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
