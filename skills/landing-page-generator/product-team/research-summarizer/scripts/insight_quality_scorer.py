#!/usr/bin/env python3
"""
insight_quality_scorer.py — Score insights on confidence, specificity,
bias risk, and decision impact; classify as keep / refine / demote.

Reads a JSON of proposed insights with their evidence count + segment
coverage + statement metadata; rates each insight 0-100; recommends
keep / refine / demote.

Stdlib only. JSON or markdown output.

Usage:
    python3 insight_quality_scorer.py --input insights.json
    python3 insight_quality_scorer.py --input insights.json --format markdown

Input schema:
{
  "as_of": "2026-05-27",
  "study_name": "Onboarding interviews Q2",
  "insights": [
      {
          "id": "INS-001",
          "statement": "Users abandon onboarding when import options are hidden.",
          "actor": "trial users on web",          # who/what
          "behavior_or_need": "abandon onboarding",
          "explanation": "options not visible at first step",
          "evidence_source_count": 6,
          "evidence_segment_count": 2,
          "evidence_recent": true,
          "disconfirming_evidence_checked": true,
          "second_coder_used": false,
          "decision_change": "could change onboarding flow",   # high|medium|low free text
          "decision_impact_high": true|false
      }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def score_confidence(insight: dict[str, Any]) -> tuple[int, list[str]]:
    notes: list[str] = []
    src = int(insight.get("evidence_source_count", 0) or 0)
    seg = int(insight.get("evidence_segment_count", 0) or 0)
    score = 0
    if src >= 5:
        score += 25
        notes.append(f"{src} sources (strong)")
    elif src >= 3:
        score += 15
        notes.append(f"{src} sources (acceptable)")
    elif src >= 1:
        score += 5
        notes.append(f"only {src} source(s) — thin")
    if seg >= 2:
        score += 5
    if insight.get("evidence_recent"):
        score += 5
    else:
        notes.append("evidence not recent — verify still applicable")
    return min(35, score), notes


def score_specificity(insight: dict[str, Any]) -> tuple[int, list[str]]:
    notes: list[str] = []
    score = 0
    if insight.get("actor"):
        score += 8
    else:
        notes.append("no actor specified — to whom does it apply?")
    if insight.get("behavior_or_need"):
        score += 8
    else:
        notes.append("no behavior/need specified")
    if insight.get("explanation"):
        score += 9
    else:
        notes.append("no explanation — observation, not insight")
    return min(25, score), notes


def score_bias_risk_reduction(insight: dict[str, Any]) -> tuple[int, list[str]]:
    notes: list[str] = []
    score = 0
    if insight.get("disconfirming_evidence_checked"):
        score += 12
    else:
        notes.append("disconfirming evidence not checked")
    if insight.get("second_coder_used"):
        score += 8
    else:
        notes.append("no second coder — single-interpreter risk")
    if int(insight.get("evidence_segment_count", 0) or 0) >= 2:
        score += 5
    else:
        notes.append("single-segment — selection bias risk")
    return min(25, score), notes


def score_decision_impact(insight: dict[str, Any]) -> tuple[int, list[str]]:
    notes: list[str] = []
    score = 0
    if insight.get("decision_impact_high"):
        score += 10
    else:
        notes.append("decision impact not marked high — verify it changes anything")
    if (insight.get("decision_change") or "").strip():
        score += 5
    return min(15, score), notes


def assess(insight: dict[str, Any]) -> dict[str, Any]:
    c_score, c_notes = score_confidence(insight)
    s_score, s_notes = score_specificity(insight)
    b_score, b_notes = score_bias_risk_reduction(insight)
    i_score, i_notes = score_decision_impact(insight)
    total = c_score + s_score + b_score + i_score
    if total >= 75:
        verdict = "keep"
    elif total >= 50:
        verdict = "refine"
    else:
        verdict = "demote to open question"
    return {
        "id": insight.get("id", ""),
        "statement": insight.get("statement", ""),
        "confidence_score": c_score,
        "specificity_score": s_score,
        "bias_risk_reduction_score": b_score,
        "decision_impact_score": i_score,
        "total_score": total,
        "verdict": verdict,
        "findings": c_notes + s_notes + b_notes + i_notes,
    }


def grade(state: dict[str, Any]) -> dict[str, Any]:
    insights = state.get("insights", []) or []
    results = [assess(i) for i in insights]
    results.sort(key=lambda r: r["total_score"], reverse=True)
    verdict_counts = {"keep": 0, "refine": 0, "demote to open question": 0}
    for r in results:
        verdict_counts[r["verdict"]] = verdict_counts.get(r["verdict"], 0) + 1
    return {
        "as_of": state.get("as_of", ""),
        "study_name": state.get("study_name", ""),
        "insight_count": len(results),
        "verdict_counts": verdict_counts,
        "insights": results,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Insight Quality Scores — {report.get('study_name','(unnamed)')}")
    lines.append(f"_as of {report['as_of']}_\n")
    vc = report["verdict_counts"]
    lines.append(f"## Summary: {report['insight_count']} insights | "
                f"keep: {vc['keep']} | refine: {vc['refine']} | "
                f"demote: {vc['demote to open question']}\n")
    lines.append("| ID | Score | Verdict | Statement |")
    lines.append("|----|-------|---------|-----------|")
    for i in report["insights"]:
        statement = (i["statement"][:80] + "…") if len(i["statement"]) > 80 else i["statement"]
        lines.append(f"| {i['id']} | {i['total_score']}/100 | {i['verdict']} | {statement} |")
    lines.append("")
    lines.append("## Detail")
    for i in report["insights"]:
        lines.append(f"### {i['id']} — {i['verdict']} ({i['total_score']}/100)")
        lines.append(f"_{i['statement']}_\n")
        lines.append(f"- Confidence: {i['confidence_score']}/35")
        lines.append(f"- Specificity: {i['specificity_score']}/25")
        lines.append(f"- Bias-risk reduction: {i['bias_risk_reduction_score']}/25")
        lines.append(f"- Decision impact: {i['decision_impact_score']}/15")
        if i["findings"]:
            lines.append("\n**Notes:**")
            for n in i["findings"]:
                lines.append(f"- {n}")
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Score insights on confidence, specificity, bias, impact",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of insights")
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

    report = grade(state)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
