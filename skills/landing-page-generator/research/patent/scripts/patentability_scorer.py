#!/usr/bin/env python3
"""
patentability_scorer.py — Score an invention's patentability across 5
dimensions: novelty, non-obviousness, utility, subject matter eligibility,
enablement.

Reads a JSON describing the invention + closest prior art; rates each
dimension and provides recommendation + risks.

Stdlib only. JSON or markdown output.

Usage:
    python3 patentability_scorer.py --input patentability.json
    python3 patentability_scorer.py --input patentability.json --format markdown

Input schema:
{
  "invention_title": "...",
  "novel_elements": ["element 1","element 2"],
  "closest_prior_art": [
      {
          "reference": "Smith 2018",
          "discloses_elements": ["element 1"],
          "publication_date": "2018-03-15"
      }
  ],
  "filing_jurisdiction": "US",
  "subject_matter_category": "method",  # method|system|composition|software|diagnostic|business|other
  "would_be_obvious_to_skilled_artisan": false,
  "useful_for_stated_purpose": true,
  "specification_enables_construction": true,
  "commercial_success_evidence": "low",  # low|medium|high
  "long_felt_need_evidence": "low"
}
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class DimScore:
    dimension: str
    score: int
    max_score: int
    verdict: str
    notes: list[str]


def score_novelty(state: dict[str, Any]) -> DimScore:
    elements = set(state.get("novel_elements", []) or [])
    prior_art = state.get("closest_prior_art", []) or []
    notes: list[str] = []

    if not elements:
        return DimScore("novelty", 0, 25, "no novel elements declared",
                       ["state the novel elements claimed"])

    # Check if any single ref discloses all elements
    for ref in prior_art:
        disclosed = set(ref.get("discloses_elements", []) or [])
        if elements.issubset(disclosed):
            return DimScore("novelty", 0, 25, "anticipated by prior art",
                          [f"{ref.get('reference')} discloses all claimed novel elements"])

    # Count how many elements are disclosed across all refs
    all_disclosed = set()
    for ref in prior_art:
        all_disclosed.update(set(ref.get("discloses_elements", []) or []))
    novel_remaining = elements - all_disclosed

    if not novel_remaining:
        return DimScore("novelty", 8, 25, "elements split across prior art; check obviousness",
                      [f"{len(elements)} novel elements; all disclosed across {len(prior_art)} references"])

    novel_pct = len(novel_remaining) / len(elements)
    score = int(25 * novel_pct)
    notes.append(f"{len(novel_remaining)} of {len(elements)} novel elements NOT in any prior art")
    return DimScore("novelty", score, 25,
                   "novel" if novel_pct >= 0.5 else "partly novel; review obviousness",
                   notes)


def score_obviousness(state: dict[str, Any]) -> DimScore:
    obvious = bool(state.get("would_be_obvious_to_skilled_artisan", False))
    long_felt = (state.get("long_felt_need_evidence") or "low").lower()
    commercial = (state.get("commercial_success_evidence") or "low").lower()

    if obvious:
        # Secondary considerations may rescue
        score = 0
        notes = ["obvious to skilled artisan per applicant"]
        bonus = 0
        if long_felt == "high":
            bonus += 4
            notes.append("strong long-felt need partially rescues")
        if commercial == "high":
            bonus += 4
            notes.append("commercial success partially rescues")
        score = bonus
        verdict = "obvious (secondary considerations only partial)"
    else:
        score = 20
        notes = ["not obvious per applicant"]
        if long_felt in ("medium", "high"):
            score += 2
            notes.append(f"long-felt need ({long_felt}) supports non-obviousness")
        if commercial in ("medium", "high"):
            score += 3
            notes.append(f"commercial success ({commercial}) supports non-obviousness")
        verdict = "non-obvious"

    return DimScore("non-obviousness", min(25, score), 25, verdict, notes)


def score_utility(state: dict[str, Any]) -> DimScore:
    if state.get("useful_for_stated_purpose"):
        return DimScore("utility", 15, 15, "useful (US: low bar)",
                       ["practical utility stated"])
    return DimScore("utility", 0, 15, "not useful for stated purpose",
                   ["claim utility or risk §101 rejection"])


def score_subject_matter(state: dict[str, Any]) -> DimScore:
    category = (state.get("subject_matter_category") or "").lower()
    jur = (state.get("filing_jurisdiction") or "US").upper()
    notes: list[str] = []

    if category == "software":
        if jur == "US":
            return DimScore("subject matter eligibility", 8, 20,
                          "software in US — Alice/Mayo risk",
                          ["must show specific technical improvement; "
                           "not merely automate known process"])
        return DimScore("subject matter eligibility", 15, 20,
                       "software in EU/etc — technical character generally OK",
                       ["EU/UK require technical character; usually achievable"])

    if category == "diagnostic":
        return DimScore("subject matter eligibility", 5, 20,
                       "diagnostic — high §101 risk in US (Mayo)",
                       ["pure diagnostic methods often unpatentable; "
                        "consider adding actionable step"])

    if category == "business":
        return DimScore("subject matter eligibility", 3, 20,
                       "business method — high Alice risk",
                       ["business methods generally unpatentable post-Alice"])

    return DimScore("subject matter eligibility", 18, 20,
                   "subject matter likely eligible",
                   [f"category '{category}' typically eligible"])


def score_enablement(state: dict[str, Any]) -> DimScore:
    if state.get("specification_enables_construction"):
        return DimScore("enablement", 15, 15, "specification enables",
                       ["skilled artisan can make + use the invention"])
    return DimScore("enablement", 5, 15, "enablement unclear",
                   ["expand specification with sufficient implementation detail"])


def assess(state: dict[str, Any]) -> dict[str, Any]:
    scores = [
        score_novelty(state),
        score_obviousness(state),
        score_utility(state),
        score_subject_matter(state),
        score_enablement(state),
    ]
    total = sum(s.score for s in scores)
    max_total = sum(s.max_score for s in scores)
    pct = round((total / max_total) * 100, 1) if max_total > 0 else 0

    if total == 0 and scores[0].verdict.startswith("anticipated"):
        recommendation = "NOT PATENTABLE — invention is anticipated"
    elif pct >= 75:
        recommendation = "STRONG patentability — proceed with filing"
    elif pct >= 55:
        recommendation = "MODERATE patentability — address weakest dimensions"
    elif pct >= 35:
        recommendation = "WEAK patentability — major revisions needed"
    else:
        recommendation = "POOR patentability — reconsider whether to file"

    risks: list[str] = []
    for s in scores:
        if s.score < s.max_score * 0.5:
            risks.append(f"{s.dimension}: {s.verdict}")

    return {
        "invention_title": state.get("invention_title", ""),
        "filing_jurisdiction": state.get("filing_jurisdiction", "US"),
        "total_score": total,
        "max_score": max_total,
        "patentability_pct": pct,
        "recommendation": recommendation,
        "major_risks": risks,
        "dimensions": [
            {"dimension": s.dimension, "score": s.score, "max": s.max_score,
             "verdict": s.verdict, "notes": s.notes}
            for s in scores
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Patentability Assessment — {report.get('invention_title','')}\n")
    lines.append(f"**Filing jurisdiction:** {report['filing_jurisdiction']}")
    lines.append(f"\n## Total: **{report['total_score']}/{report['max_score']} ({report['patentability_pct']}%)**\n")
    lines.append(f"### Recommendation: **{report['recommendation']}**\n")
    if report["major_risks"]:
        lines.append("### Major risks")
        for r in report["major_risks"]:
            lines.append(f"- {r}")
        lines.append("")
    lines.append("## Dimension scores")
    lines.append("| Dimension | Score | Max | Verdict |")
    lines.append("|-----------|-------|-----|---------|")
    for d in report["dimensions"]:
        lines.append(f"| {d['dimension']} | {d['score']} | {d['max']} | {d['verdict']} |")
    lines.append("")
    lines.append("## Notes per dimension")
    for d in report["dimensions"]:
        lines.append(f"### {d['dimension']}")
        for n in d["notes"]:
            lines.append(f"- {n}")
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Score patentability of an invention",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of invention + prior art")
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

    report = assess(state)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
