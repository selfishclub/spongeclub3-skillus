#!/usr/bin/env python3
"""
confidence_band_generator.py — Assign confidence bands to roadmap items
based on lead-time, dependency, history, and discovery signals.

Reads a JSON of roadmap items with attributes (specified, designed,
prototyped, dependency_risk, team_velocity_history, etc.); returns
recommended band (commit / plan / aspire / strategic) with reasoning.

Stdlib only. JSON or markdown output.

Usage:
    python3 confidence_band_generator.py --input items.json
    python3 confidence_band_generator.py --input items.json --format markdown

Input schema:
{
  "as_of": "2026-05-27",
  "items": [
      {
          "id": "I-001",
          "name": "Real-time editing",
          "ship_target_date": "2026-06-15",
          "spec_complete": true,
          "design_complete": true,
          "prototype_built": true,
          "estimated_eng_weeks": 8,
          "team_capacity_eng_weeks_per_qtr": 24,
          "dependency_risk": "low",         # low|medium|high
          "history_team_estimate_accuracy": "good",   # good|fair|poor
          "scope_changes_last_month": 0,
          "external_dependencies": []
      }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any


def parse_date(s: str | None) -> date | None:
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def days_until(target: date | None, today: date) -> int:
    return (target - today).days if target else 9999


@dataclass
class Assessment:
    id: str
    name: str
    band: str
    band_reason: str
    confidence_score: int
    deductions: list[str]


def assess(item: dict[str, Any], today: date) -> Assessment:
    name = item.get("name", "")
    iid = item.get("id", "")
    target = parse_date(item.get("ship_target_date"))
    days = days_until(target, today)

    # Start from "commit" and deduct as risk factors appear
    score = 100
    deductions: list[str] = []

    if not item.get("spec_complete"):
        score -= 25
        deductions.append("spec not complete")

    if not item.get("design_complete"):
        score -= 15
        deductions.append("design not complete")

    if not item.get("prototype_built"):
        score -= 10
        deductions.append("no prototype")

    cap = float(item.get("team_capacity_eng_weeks_per_qtr", 0) or 0)
    eng_weeks = float(item.get("estimated_eng_weeks", 0) or 0)
    if cap > 0 and eng_weeks > 0:
        utilization = eng_weeks / cap
        if utilization > 0.5:
            score -= 15
            deductions.append(f"high capacity utilization ({utilization:.0%}) — risk")
        elif utilization > 0.3:
            score -= 5
            deductions.append(f"moderate capacity ({utilization:.0%})")

    dep_risk = (item.get("dependency_risk") or "low").lower()
    if dep_risk == "high":
        score -= 20
        deductions.append("high dependency risk")
    elif dep_risk == "medium":
        score -= 10
        deductions.append("medium dependency risk")

    history = (item.get("history_team_estimate_accuracy") or "fair").lower()
    if history == "poor":
        score -= 15
        deductions.append("team estimate history poor")
    elif history == "fair":
        score -= 5
        deductions.append("team estimate history fair (not strong)")

    scope_changes = int(item.get("scope_changes_last_month", 0) or 0)
    if scope_changes >= 2:
        score -= 15
        deductions.append(f"{scope_changes} scope changes in last month — unstable")
    elif scope_changes == 1:
        score -= 5

    ext_deps = item.get("external_dependencies", []) or []
    if ext_deps:
        score -= min(15, len(ext_deps) * 5)
        deductions.append(f"{len(ext_deps)} external dependency(ies)")

    # Time pressure
    if 0 < days < 30 and score < 80:
        score -= 10
        deductions.append("target date <30 days but score not strong")

    score = max(0, score)

    if score >= 80:
        band = "commit"
        reason = "Strong: spec/design/prototype done; capacity OK; low risk"
    elif score >= 55:
        band = "plan"
        reason = "Solid plan but with risks; will probably ship; not yet committable"
    elif score >= 30:
        band = "aspire"
        reason = "Exploration / aspiration; do not commit externally"
    else:
        band = "strategic intent"
        reason = "Direction only; significant unknowns"

    return Assessment(
        id=iid, name=name, band=band, band_reason=reason,
        confidence_score=score, deductions=deductions,
    )


def generate(state: dict[str, Any]) -> dict[str, Any]:
    today = parse_date(state.get("as_of")) or date.today()
    items = state.get("items", []) or []
    assessments = [assess(i, today) for i in items]
    band_counts: dict[str, int] = {}
    for a in assessments:
        band_counts[a.band] = band_counts.get(a.band, 0) + 1
    return {
        "as_of": state.get("as_of", ""),
        "item_count": len(items),
        "band_counts": band_counts,
        "assessments": [
            {
                "id": a.id, "name": a.name,
                "confidence_score": a.confidence_score,
                "band": a.band, "band_reason": a.band_reason,
                "deductions": a.deductions,
            }
            for a in assessments
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append("# Confidence Band Recommendations\n")
    lines.append(f"_{report['item_count']} items, as of {report['as_of']}_\n")
    bc = report["band_counts"]
    lines.append("## Distribution")
    for band in ("commit", "plan", "aspire", "strategic intent"):
        lines.append(f"- {band}: {bc.get(band, 0)}")
    lines.append("")
    lines.append("## Per item")
    lines.append("| ID | Item | Score | Band |")
    lines.append("|----|------|-------|------|")
    for a in report["assessments"]:
        lines.append(f"| {a['id']} | {a['name']} | {a['confidence_score']}/100 | {a['band']} |")
    lines.append("")
    lines.append("## Detail")
    for a in report["assessments"]:
        lines.append(f"### {a['id']} — {a['name']}")
        lines.append(f"_band: **{a['band']}** ({a['confidence_score']}/100)_")
        lines.append(f"_{a['band_reason']}_")
        if a["deductions"]:
            lines.append("\n**Deductions:**")
            for d in a["deductions"]:
                lines.append(f"- {d}")
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Recommend confidence bands for roadmap items",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of roadmap items")
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

    report = generate(state)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
