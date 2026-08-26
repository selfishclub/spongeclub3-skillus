#!/usr/bin/env python3
"""
search_strategy_builder.py — Build a literature search strategy from a
framed research question.

Reads a JSON describing the research question (PICO-style), suggested
synonyms per term, and target databases; produces Boolean query strings
per database, applicable filters, and a PRISMA-style log template.

Stdlib only. JSON or markdown output.

Usage:
    python3 search_strategy_builder.py --input question.json
    python3 search_strategy_builder.py --input question.json --format markdown

Input schema:
{
  "research_question": "Does X reduce Y in population Z?",
  "frame": "pico",                              # pico|peo|spider
  "terms": {
      "population": ["adults with diabetes","T2DM patients"],
      "intervention": ["intermittent fasting","time-restricted eating"],
      "comparator": ["caloric restriction","standard diet"],
      "outcome": ["HbA1c","glycemic control"]
  },
  "filters": {
      "year_min": 2018,
      "year_max": 2026,
      "languages": ["English"],
      "study_types": ["RCT","systematic review"]
  },
  "databases": ["PubMed","Web of Science","Scopus","Embase"]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DATABASE_SYNTAX = {
    "PubMed": {
        "and": "AND", "or": "OR", "field_title": "[Title]",
        "field_tiab": "[Title/Abstract]", "trunc": "*",
    },
    "Web of Science": {
        "and": "AND", "or": "OR", "field_title": "TI=",
        "field_tiab": "TS=", "trunc": "*",
    },
    "Scopus": {
        "and": "AND", "or": "OR", "field_title": "TITLE",
        "field_tiab": "TITLE-ABS-KEY", "trunc": "*",
    },
    "Embase": {
        "and": "AND", "or": "OR", "field_title": ":ti",
        "field_tiab": ":ab,ti,kw", "trunc": "*",
    },
    "Google Scholar": {
        "and": "AND", "or": "OR", "field_title": "intitle:",
        "field_tiab": "", "trunc": "",
    },
    "IEEE Xplore": {
        "and": "AND", "or": "OR", "field_title": "\"Document Title\":",
        "field_tiab": "\"Abstract\":", "trunc": "*",
    },
    "ACM Digital Library": {
        "and": "AND", "or": "OR", "field_title": "Title:",
        "field_tiab": "Abstract:", "trunc": "*",
    },
    "JSTOR": {
        "and": "AND", "or": "OR", "field_title": "ti:",
        "field_tiab": "ab:", "trunc": "*",
    },
    "PsycInfo": {
        "and": "AND", "or": "OR", "field_title": ".ti",
        "field_tiab": ".ti,ab,id", "trunc": "*",
    },
    "arXiv": {
        "and": "AND", "or": "OR", "field_title": "ti:",
        "field_tiab": "abs:", "trunc": "",
    },
    "SSRN": {
        "and": "AND", "or": "OR", "field_title": "",
        "field_tiab": "", "trunc": "",
    },
}


def build_term_group(terms: list[str], syntax: dict[str, str]) -> str:
    if not terms:
        return ""
    quoted = [f'"{t}"' if " " in t else t for t in terms]
    return "(" + f" {syntax['or']} ".join(quoted) + ")"


def build_query(terms_by_concept: dict[str, list[str]],
                database: str) -> str:
    syntax = DATABASE_SYNTAX.get(database, DATABASE_SYNTAX["PubMed"])
    parts = []
    for concept, term_list in terms_by_concept.items():
        if not term_list:
            continue
        parts.append(build_term_group(term_list, syntax))
    if not parts:
        return ""
    return f" {syntax['and']} ".join(parts)


def build_filters(filters: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    yr_min = filters.get("year_min")
    yr_max = filters.get("year_max")
    if yr_min and yr_max:
        out["date_range"] = f"{yr_min}-{yr_max}"
    elif yr_min:
        out["date_range"] = f"≥{yr_min}"
    elif yr_max:
        out["date_range"] = f"≤{yr_max}"
    langs = filters.get("languages") or []
    if langs:
        out["languages"] = ", ".join(langs)
    types = filters.get("study_types") or []
    if types:
        out["study_types"] = ", ".join(types)
    return out


def prisma_log_template(databases: list[str]) -> dict[str, Any]:
    return {
        "records_per_database": {db: 0 for db in databases},
        "additional_sources_added": 0,
        "after_deduplication": 0,
        "title_abstract_screened": 0,
        "title_abstract_excluded": 0,
        "full_text_assessed": 0,
        "full_text_excluded": 0,
        "included_in_synthesis": 0,
    }


def build(spec: dict[str, Any]) -> dict[str, Any]:
    terms = spec.get("terms", {}) or {}
    databases = spec.get("databases", []) or ["PubMed"]
    queries = {}
    for db in databases:
        queries[db] = build_query(terms, db)

    return {
        "research_question": spec.get("research_question", ""),
        "frame": spec.get("frame", "pico"),
        "queries": queries,
        "filters": build_filters(spec.get("filters", {}) or {}),
        "databases": databases,
        "prisma_log_template": prisma_log_template(databases),
        "notes": [
            "Run searches on same date across all databases; record date.",
            "Deduplicate using DOI; manually verify ambiguous matches.",
            "Document any database that has unusual syntax requirements.",
            "Capture screening decisions per record (include/exclude + reason).",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append("# Literature Search Strategy\n")
    lines.append(f"**Question:** {report['research_question']}")
    lines.append(f"**Frame:** {report['frame']}")
    lines.append(f"**Databases:** {', '.join(report['databases'])}\n")
    lines.append("## Filters")
    for k, v in report["filters"].items():
        lines.append(f"- {k}: {v}")
    lines.append("\n## Search queries per database")
    for db, q in report["queries"].items():
        lines.append(f"\n### {db}")
        lines.append(f"```\n{q}\n```")
    lines.append("\n## PRISMA log template")
    log = report["prisma_log_template"]
    lines.append("### Records per database")
    for db, count in log["records_per_database"].items():
        lines.append(f"- {db}: ___")
    lines.append(f"\n- Additional sources added (snowballing, gray lit): ___")
    lines.append(f"- After deduplication: ___")
    lines.append(f"- Title/abstract screened: ___")
    lines.append(f"  - Excluded: ___")
    lines.append(f"- Full-text assessed: ___")
    lines.append(f"  - Excluded (with reasons): ___")
    lines.append(f"- Included in synthesis: ___")
    lines.append("\n## Notes")
    for n in report["notes"]:
        lines.append(f"- {n}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Build a literature search strategy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of question + terms")
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

    report = build(spec)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
