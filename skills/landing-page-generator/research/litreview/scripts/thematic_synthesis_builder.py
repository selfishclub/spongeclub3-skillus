#!/usr/bin/env python3
"""
thematic_synthesis_builder.py — Build an evidence table by clustering
sources by theme and surfacing strength + gaps.

Reads a JSON of sources tagged with themes and findings; builds a
theme-by-source evidence table; identifies well-supported themes,
contested themes, gap themes.

Stdlib only. JSON or markdown output.

Usage:
    python3 thematic_synthesis_builder.py --input tagged_sources.json
    python3 thematic_synthesis_builder.py --input tagged_sources.json --format markdown

Input schema:
{
  "as_of": "2026-05-27",
  "review_name": "X on Y in Z",
  "themes": ["theme1","theme2","theme3"],
  "sources": [
      {
          "id": "S-001",
          "citation": "Smith et al. 2023",
          "quality": "high",                # high|medium|low
          "theme_findings": [
              {"theme": "theme1", "stance": "supports", "note": "..."},
              {"theme": "theme2", "stance": "disconfirms", "note": "..."}
          ]
      }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ThemeRow:
    theme: str
    supports_high: int = 0
    supports_med: int = 0
    supports_low: int = 0
    disconfirms_high: int = 0
    disconfirms_med: int = 0
    disconfirms_low: int = 0
    partial: int = 0
    not_addressed: int = 0
    total_sources_addressing: int = 0
    evidence_strength: str = ""
    classification: str = ""


def classify_theme(row: ThemeRow) -> tuple[str, str]:
    sup_total = row.supports_high + row.supports_med + row.supports_low
    dis_total = row.disconfirms_high + row.disconfirms_med + row.disconfirms_low
    sup_high_total = row.supports_high
    dis_high_total = row.disconfirms_high

    if sup_total == 0 and dis_total == 0 and row.partial == 0:
        return ("none", "gap (not addressed by any included source)")
    if sup_total >= 3 and sup_high_total >= 2 and dis_total <= 1:
        return ("strong", "well-supported (multiple high-quality sources)")
    if sup_total >= 2 and sup_high_total >= 1 and dis_total <= 1:
        return ("moderate", "supported but thin (needs more evidence)")
    if sup_total > 0 and dis_total > 0:
        return ("contested", "contested (mixed evidence)")
    if dis_total > 0:
        return ("disconfirmed", "disconfirming evidence dominant")
    if sup_total >= 1:
        return ("anecdotal", "anecdotal (single source) — needs replication")
    return ("unclear", "evidence unclear")


def build_table(state: dict[str, Any]) -> dict[str, Any]:
    sources = state.get("sources", []) or []
    declared_themes = state.get("themes", []) or []

    # Discover themes from data if not declared
    discovered = set()
    for s in sources:
        for tf in s.get("theme_findings", []) or []:
            discovered.add(tf.get("theme", ""))
    all_themes = list(dict.fromkeys(declared_themes + sorted(discovered)))

    rows: dict[str, ThemeRow] = {t: ThemeRow(theme=t) for t in all_themes}
    source_quality_map = {s.get("id", ""): (s.get("quality") or "medium").lower()
                         for s in sources}
    by_theme_sources: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for s in sources:
        sid = s.get("id", "")
        quality = (s.get("quality") or "medium").lower()
        themes_seen = set()
        for tf in s.get("theme_findings", []) or []:
            t = tf.get("theme", "")
            stance = (tf.get("stance") or "supports").lower()
            if t not in rows:
                continue
            themes_seen.add(t)
            row = rows[t]
            row.total_sources_addressing += 1
            if stance == "supports":
                if quality == "high":
                    row.supports_high += 1
                elif quality == "medium":
                    row.supports_med += 1
                else:
                    row.supports_low += 1
            elif stance == "disconfirms":
                if quality == "high":
                    row.disconfirms_high += 1
                elif quality == "medium":
                    row.disconfirms_med += 1
                else:
                    row.disconfirms_low += 1
            elif stance == "partial":
                row.partial += 1
            by_theme_sources[t].append({
                "source_id": sid,
                "citation": s.get("citation", ""),
                "quality": quality,
                "stance": stance,
                "note": tf.get("note", ""),
            })
        for t in rows:
            if t not in themes_seen:
                rows[t].not_addressed += 1

    for row in rows.values():
        strength, classification = classify_theme(row)
        row.evidence_strength = strength
        row.classification = classification

    return {
        "as_of": state.get("as_of", ""),
        "review_name": state.get("review_name", ""),
        "total_sources": len(sources),
        "total_themes": len(rows),
        "themes": [
            {
                "theme": r.theme,
                "evidence_strength": r.evidence_strength,
                "classification": r.classification,
                "supports_high": r.supports_high,
                "supports_med": r.supports_med,
                "supports_low": r.supports_low,
                "disconfirms_high": r.disconfirms_high,
                "disconfirms_med": r.disconfirms_med,
                "disconfirms_low": r.disconfirms_low,
                "partial": r.partial,
                "not_addressed": r.not_addressed,
                "sources_addressing": r.total_sources_addressing,
                "source_detail": by_theme_sources.get(r.theme, []),
            }
            for r in rows.values()
        ],
        "gaps": [r.theme for r in rows.values() if r.evidence_strength in ("none", "anecdotal")],
        "well_supported": [r.theme for r in rows.values() if r.evidence_strength == "strong"],
        "contested": [r.theme for r in rows.values() if r.evidence_strength == "contested"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Thematic Synthesis — {report.get('review_name','(unnamed)')}\n")
    lines.append(f"_Sources: {report['total_sources']} | Themes: {report['total_themes']}_\n")
    lines.append("## Evidence summary")
    lines.append(f"- Well-supported themes: {len(report['well_supported'])}")
    lines.append(f"- Contested themes: {len(report['contested'])}")
    lines.append(f"- Gaps (no / weak evidence): {len(report['gaps'])}\n")
    lines.append("## Theme strength table")
    lines.append("| Theme | Strength | Sup (H/M/L) | Disconf (H/M/L) | Partial | Not addr. |")
    lines.append("|-------|----------|-------------|------------------|---------|-----------|")
    for t in report["themes"]:
        lines.append(
            f"| {t['theme']} | {t['evidence_strength']} | "
            f"{t['supports_high']}/{t['supports_med']}/{t['supports_low']} | "
            f"{t['disconfirms_high']}/{t['disconfirms_med']}/{t['disconfirms_low']} | "
            f"{t['partial']} | {t['not_addressed']} |"
        )
    lines.append("")
    lines.append("## Per-theme detail")
    for t in report["themes"]:
        lines.append(f"### {t['theme']} — {t['classification']}")
        if t["source_detail"]:
            lines.append("| Source | Quality | Stance | Note |")
            lines.append("|--------|---------|--------|------|")
            for sd in t["source_detail"]:
                note = (sd["note"][:60] + "…") if len(sd["note"]) > 60 else sd["note"]
                lines.append(f"| {sd['citation']} | {sd['quality']} | {sd['stance']} | {note} |")
        else:
            lines.append("_No sources addressed this theme._")
        lines.append("")
    if report["gaps"]:
        lines.append("## Identified gaps")
        for g in report["gaps"]:
            lines.append(f"- {g}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Build thematic synthesis from tagged sources",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of tagged sources")
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

    report = build_table(state)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
