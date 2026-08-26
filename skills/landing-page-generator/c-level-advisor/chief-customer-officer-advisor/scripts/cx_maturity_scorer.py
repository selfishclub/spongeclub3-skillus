#!/usr/bin/env python3
"""
cx_maturity_scorer.py — Score CX maturity across 6 dimensions (0-100):
strategy, segmentation, journey, voice, operations, talent.

Stdlib only. JSON or markdown output.

Usage:
    python3 cx_maturity_scorer.py --input cx_state.json
    python3 cx_maturity_scorer.py --input cx_state.json --format markdown

Input schema:
{
  "org_name": "Acme",
  "as_of": "2026-05-27",
  "strategy": {
      "written_cx_strategy": true|false,
      "primary_outcome_defined": true|false,
      "owner_clarity_score": 0-10,                # CCO scope clarity
      "renewals_owner_named": true|false,
      "expansion_owner_named": true|false,
      "board_review_cadence_months": 0-12
  },
  "segmentation": {
      "segment_count": 0-6,
      "segment_coverage_models_defined": true|false,
      "csm_ratio_in_band": true|false,
      "exec_sponsorship_on_top20": true|false
  },
  "journey": {
      "journey_mapped": true|false,
      "stages_count": 0-10,
      "handoffs_documented": true|false,
      "stage_owners_assigned_pct": 0-100,
      "instrumentation_per_stage": "none|partial|comprehensive"
  },
  "voice": {
      "nps_relationship_running": true|false,
      "nps_transactional_running": true|false,
      "interview_program_running": true|false,
      "behavioral_voc_in_use": true|false,
      "closed_loop_pct": 0-100,
      "quarterly_synthesis_published": true|false
  },
  "operations": {
      "health_score_in_use": true|false,
      "renewal_motion_documented": true|false,
      "save_room_active": true|false,
      "qbr_standard_in_use": true|false,
      "trailing_nrr_pct": 0-200,
      "trailing_grr_pct": 0-100,
      "logo_churn_pct": 0-100
  },
  "talent": {
      "cco_or_head_of_cx_filled": true|false,
      "csm_count": 0,
      "support_lead_in_place": true|false,
      "renewals_team_in_place": true|false,
      "csm_ladder_defined": true|false,
      "literacy_program": "none|partial|all-tiers"
  }
}
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DIMENSIONS = ["strategy", "segmentation", "journey", "voice", "operations", "talent"]

MATURITY_BANDS = [
    (0, 24, "Ad hoc", "CX activity is reactive; few standards; high CSM dependency."),
    (25, 49, "Emerging", "Some foundations exist; segmentation partial; VoC inconsistent."),
    (50, 74, "Defined", "Operating model is articulated; instrumentation in place; standardized motions."),
    (75, 89, "Managed", "Quantitative goals tracked; CSM allocation tuned; action loops closed."),
    (90, 100, "Optimizing", "Continuous improvement; CX is a competitive advantage."),
]


@dataclass
class DimScore:
    name: str
    score: int
    findings: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)


def _g(d: dict[str, Any] | None, k: str, default: Any = None) -> Any:
    return (d or {}).get(k, default)


def _b(v: Any, w: int) -> int:
    return w if bool(v) else 0


def _tri(v: Any, m: dict[str, int]) -> int:
    return m.get(str(v).lower().strip(), 0) if isinstance(v, str) else 0


def score_strategy(d: dict[str, Any] | None) -> DimScore:
    s = DimScore("strategy", 0)
    if not d:
        s.gaps.append("publish a written CX strategy + define primary outcome")
        return s

    if _g(d, "written_cx_strategy"):
        s.score += 25
        s.findings.append("written CX strategy in place")
    else:
        s.gaps.append("publish written CX strategy")

    if _g(d, "primary_outcome_defined"):
        s.score += 20
        s.findings.append("primary customer outcome defined")
    else:
        s.gaps.append("define the primary customer outcome (specific, measurable)")

    owner = int(_g(d, "owner_clarity_score", 0) or 0)
    s.score += min(15, owner * 2)
    if owner < 7:
        s.gaps.append(f"clarify CCO scope (currently {owner}/10 clarity)")

    if _g(d, "renewals_owner_named"):
        s.score += 10
        s.findings.append("renewals owner named")
    else:
        s.gaps.append("explicitly name the renewals owner (CCO or CRO)")

    if _g(d, "expansion_owner_named"):
        s.score += 10
        s.findings.append("expansion owner named (usage vs cross-sell)")
    else:
        s.gaps.append("split expansion ownership (usage-driven vs cross-sell)")

    cadence = int(_g(d, "board_review_cadence_months", 0) or 0)
    if 1 <= cadence <= 3:
        s.score += 20
    elif cadence > 0:
        s.score += 10
        s.gaps.append("tighten board review to quarterly")
    else:
        s.gaps.append("establish a board review cadence for CX")

    s.score = min(100, s.score)
    return s


def score_segmentation(d: dict[str, Any] | None) -> DimScore:
    s = DimScore("segmentation", 0)
    if not d:
        s.gaps.append("define 3-4 customer segments with differentiated coverage")
        return s

    seg_count = int(_g(d, "segment_count", 0) or 0)
    if 3 <= seg_count <= 5:
        s.score += 25
        s.findings.append(f"{seg_count} segments (well-bounded)")
    elif seg_count > 0:
        s.score += 12
        s.gaps.append(f"target 3-5 segments (currently {seg_count})")
    else:
        s.gaps.append("define customer segments")

    if _g(d, "segment_coverage_models_defined"):
        s.score += 25
        s.findings.append("coverage models per segment defined")
    else:
        s.gaps.append("define coverage models per segment (CSM, ratio, cadence)")

    if _g(d, "csm_ratio_in_band"):
        s.score += 25
        s.findings.append("CSM ratios within benchmark band")
    else:
        s.gaps.append("right-size CSM ratios per segment")

    if _g(d, "exec_sponsorship_on_top20"):
        s.score += 25
        s.findings.append("exec sponsorship on top-20 accounts")
    else:
        s.gaps.append("assign exec sponsors to top-20 accounts")

    s.score = min(100, s.score)
    return s


def score_journey(d: dict[str, Any] | None) -> DimScore:
    s = DimScore("journey", 0)
    if not d:
        s.gaps.append("map the customer journey end-to-end")
        return s

    if _g(d, "journey_mapped"):
        s.score += 25
        s.findings.append("journey mapped")
    else:
        s.gaps.append("map the customer journey (5-7 stages)")

    stages = int(_g(d, "stages_count", 0) or 0)
    if 5 <= stages <= 7:
        s.score += 15
    elif stages > 0:
        s.score += 7
        s.gaps.append(f"target 5-7 stages (currently {stages})")

    if _g(d, "handoffs_documented"):
        s.score += 20
        s.findings.append("stage handoffs documented")
    else:
        s.gaps.append("document handoffs between stages with named owners")

    coverage = int(_g(d, "stage_owners_assigned_pct", 0) or 0)
    s.score += min(20, coverage // 5)
    if coverage < 80:
        s.gaps.append(f"assign owners to remaining stages (currently {coverage}%)")

    inst = _tri(_g(d, "instrumentation_per_stage"),
               {"none": 0, "partial": 10, "comprehensive": 20})
    s.score += inst
    if inst < 20:
        s.gaps.append("instrument each stage with a measurable success criterion")

    s.score = min(100, s.score)
    return s


def score_voice(d: dict[str, Any] | None) -> DimScore:
    s = DimScore("voice", 0)
    if not d:
        s.gaps.append("stand up a starter VoC stack")
        return s

    if _g(d, "nps_relationship_running"):
        s.score += 15
        s.findings.append("relationship NPS running")
    else:
        s.gaps.append("start quarterly relationship NPS by segment")

    if _g(d, "nps_transactional_running"):
        s.score += 15
        s.findings.append("transactional NPS running")
    else:
        s.gaps.append("add transactional NPS (onboarding, milestone)")

    if _g(d, "interview_program_running"):
        s.score += 20
        s.findings.append("interview program running (churn / win-loss)")
    else:
        s.gaps.append("stand up churn + win/loss interview program")

    if _g(d, "behavioral_voc_in_use"):
        s.score += 15
        s.findings.append("behavioral VoC in use")
    else:
        s.gaps.append("instrument behavioral VoC (analytics, support, search)")

    closed = int(_g(d, "closed_loop_pct", 0) or 0)
    s.score += min(20, closed // 5)
    if closed < 80:
        s.gaps.append(f"raise closed-loop response rate (currently {closed}%)")

    if _g(d, "quarterly_synthesis_published"):
        s.score += 15
        s.findings.append("quarterly synthesis published")
    else:
        s.gaps.append("publish quarterly VoC synthesis to product + GTM")

    s.score = min(100, s.score)
    return s


def score_operations(d: dict[str, Any] | None) -> DimScore:
    s = DimScore("operations", 0)
    if not d:
        s.gaps.append("instrument health score + renewal motion")
        return s

    if _g(d, "health_score_in_use"):
        s.score += 15
        s.findings.append("health score in use")
    else:
        s.gaps.append("implement a starter health-score model (6 components)")

    if _g(d, "renewal_motion_documented"):
        s.score += 15
        s.findings.append("renewal motion documented")
    else:
        s.gaps.append("publish the 90/60/30 renewal motion")

    if _g(d, "save_room_active"):
        s.score += 15
        s.findings.append("save room active")
    else:
        s.gaps.append("stand up weekly save room")

    if _g(d, "qbr_standard_in_use"):
        s.score += 10
        s.findings.append("QBR standard in use")
    else:
        s.gaps.append("define the QBR / EBR standard for enterprise segment")

    nrr = int(_g(d, "trailing_nrr_pct", 0) or 0)
    if nrr >= 120:
        s.score += 20
        s.findings.append(f"NRR {nrr}% (top quartile)")
    elif nrr >= 110:
        s.score += 15
        s.findings.append(f"NRR {nrr}% (above median)")
    elif nrr >= 100:
        s.score += 10
        s.findings.append(f"NRR {nrr}% (around median)")
    elif nrr > 0:
        s.score += 4
        s.gaps.append(f"raise NRR (currently {nrr}%)")

    grr = int(_g(d, "trailing_grr_pct", 0) or 0)
    if grr >= 95:
        s.score += 15
        s.findings.append(f"GRR {grr}% (strong)")
    elif grr >= 90:
        s.score += 10
        s.findings.append(f"GRR {grr}% (acceptable)")
    elif grr > 0:
        s.score += 3
        s.gaps.append(f"raise GRR (currently {grr}%)")

    churn = int(_g(d, "logo_churn_pct", 0) or 0)
    if churn > 15:
        s.score -= 10
        s.gaps.append(f"logo churn at {churn}% — investigate top drivers")
    elif churn > 10:
        s.score -= 5
        s.gaps.append(f"logo churn at {churn}% — above target band")
    elif churn > 0:
        s.findings.append(f"logo churn {churn}% (within range)")

    s.score = max(0, min(100, s.score))
    return s


def score_talent(d: dict[str, Any] | None) -> DimScore:
    s = DimScore("talent", 0)
    if not d:
        s.gaps.append("hire CCO + critical CX leadership")
        return s

    if _g(d, "cco_or_head_of_cx_filled"):
        s.score += 25
        s.findings.append("CCO / head of CX filled")
    else:
        s.gaps.append("hire / promote a head of CX")

    csm = int(_g(d, "csm_count", 0) or 0)
    if csm >= 5:
        s.score += 15
    elif csm >= 2:
        s.score += 9
    elif csm >= 1:
        s.score += 5
    if csm < 2:
        s.gaps.append("grow CS to at least 2 CSMs to cover hand-offs")

    if _g(d, "support_lead_in_place"):
        s.score += 15
        s.findings.append("support lead in place")
    else:
        s.gaps.append("hire / assign a dedicated support lead")

    if _g(d, "renewals_team_in_place"):
        s.score += 15
        s.findings.append("renewals team / lead in place")
    else:
        s.gaps.append("hire or assign a renewals lead (or merge with CS lead)")

    if _g(d, "csm_ladder_defined"):
        s.score += 15
        s.findings.append("CSM career ladder defined")
    else:
        s.gaps.append("define CSM career ladder (IC + manager track)")

    lit = _tri(_g(d, "literacy_program"), {"none": 0, "partial": 8, "all-tiers": 15})
    s.score += lit
    if lit < 15:
        s.gaps.append("build customer-centric literacy program (sales, product, eng tiers)")

    s.score = min(100, s.score)
    return s


SCORERS = {
    "strategy": score_strategy,
    "segmentation": score_segmentation,
    "journey": score_journey,
    "voice": score_voice,
    "operations": score_operations,
    "talent": score_talent,
}


def band_for(score: int) -> tuple[str, str]:
    for lo, hi, label, desc in MATURITY_BANDS:
        if lo <= score <= hi:
            return label, desc
    return "Unknown", ""


def overall_score(dims: list[DimScore]) -> int:
    return round(sum(d.score for d in dims) / len(dims)) if dims else 0


def prioritized_gaps(dims: list[DimScore], top_n: int) -> list[dict[str, str]]:
    gaps = []
    for d in sorted(dims, key=lambda x: x.score):
        priority = "high" if d.score < 40 else ("medium" if d.score < 70 else "low")
        for g in d.gaps:
            gaps.append({"dimension": d.name, "gap": g, "priority": priority})
            if len(gaps) >= top_n:
                return gaps
    return gaps


def render_markdown(result: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# CX Maturity Assessment — {result.get('org_name','(unnamed)')}")
    lines.append(f"_as of {result.get('as_of','(no date)')}_\n")
    o = result["overall"]
    lines.append(f"## Overall: **{o['score']}/100 — {o['band']}**")
    lines.append(o["description"])
    lines.append("")
    lines.append("## Dimension scores\n")
    lines.append("| Dimension | Score | Band |")
    lines.append("|-----------|-------|------|")
    for d in result["dimensions"]:
        lines.append(f"| {d['name']} | {d['score']}/100 | {d['band']} |")
    lines.append("")
    lines.append("## Findings by dimension\n")
    for d in result["dimensions"]:
        if d["findings"]:
            lines.append(f"### {d['name'].title()}")
            for f in d["findings"]:
                lines.append(f"- {f}")
            lines.append("")
    lines.append("## Prioritized gap list\n")
    lines.append("| Priority | Dimension | Gap |")
    lines.append("|----------|-----------|-----|")
    for g in result["prioritized_gaps"]:
        lines.append(f"| {g['priority']} | {g['dimension']} | {g['gap']} |")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Score CX maturity across 6 dimensions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON file with current CX state")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--top-gaps", type=int, default=12)
    p.add_argument("--output", help="Write to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"error: cannot read input: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 2

    dims = [SCORERS[name](raw.get(name)) for name in DIMENSIONS]
    total = overall_score(dims)
    band, desc = band_for(total)

    result = {
        "org_name": raw.get("org_name", ""),
        "as_of": raw.get("as_of", ""),
        "overall": {"score": total, "band": band, "description": desc},
        "dimensions": [
            {"name": d.name, "score": d.score, "band": band_for(d.score)[0],
             "findings": d.findings, "gaps": d.gaps}
            for d in dims
        ],
        "prioritized_gaps": prioritized_gaps(dims, args.top_gaps),
    }

    out = render_markdown(result) if args.format == "markdown" else json.dumps(result, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
