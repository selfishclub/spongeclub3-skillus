#!/usr/bin/env python3
"""
data_platform_evaluator.py — Score and compare data platform options against
a weighted criteria set (TCO, time-to-value, openness, governance fit,
AI readiness, vendor risk, ecosystem).

Reads a JSON with current platform, candidate alternatives, and per-option
attribute scores. Produces a comparison matrix with weighted total scores
and a recommendation.

Stdlib only.

Usage:
    python3 data_platform_evaluator.py --input platform_eval.json
    python3 data_platform_evaluator.py --input platform_eval.json --format markdown

Input schema:
{
  "scope": "Replace legacy data warehouse — FY27",
  "evaluator": "Data platform working group",
  "weights": {                          # optional, defaults shown
      "tco": 0.20,
      "time_to_value": 0.15,
      "openness": 0.10,
      "governance_fit": 0.15,
      "ai_readiness": 0.15,
      "vendor_risk": 0.10,
      "ecosystem": 0.15
  },
  "options": [
      {
          "name": "Snowflake-anchored",
          "annual_tco_usd": 1400000,
          "migration_cost_usd": 800000,
          "scores": {              # 1-5; vendor_risk: higher = MORE risk (penalty)
              "tco": 3,
              "time_to_value": 5,
              "openness": 3,
              "governance_fit": 5,
              "ai_readiness": 4,
              "vendor_risk": 3,
              "ecosystem": 5
          },
          "notes": "Strong SQL ergonomics; weaker for ML training workloads."
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


DEFAULT_WEIGHTS = {
    "tco": 0.20,
    "time_to_value": 0.15,
    "openness": 0.10,
    "governance_fit": 0.15,
    "ai_readiness": 0.15,
    "vendor_risk": 0.10,
    "ecosystem": 0.15,
}

PENALTY_CRITERIA = {"vendor_risk"}  # higher input value = larger penalty


@dataclass
class Option:
    name: str
    annual_tco_usd: float
    migration_cost_usd: float
    scores: dict[str, float]
    notes: str = ""
    weighted_score: float = 0.0
    per_criterion: dict[str, float] = field(default_factory=dict)


def normalize_weights(weights: dict[str, float] | None) -> dict[str, float]:
    if not weights:
        return dict(DEFAULT_WEIGHTS)
    w = dict(DEFAULT_WEIGHTS)
    w.update({k: float(v) for k, v in weights.items() if k in DEFAULT_WEIGHTS})
    total = sum(w.values())
    if total <= 0:
        return dict(DEFAULT_WEIGHTS)
    return {k: v / total for k, v in w.items()}


def score_option(opt: Option, weights: dict[str, float]) -> Option:
    total = 0.0
    per = {}
    for criterion, w in weights.items():
        raw = float(opt.scores.get(criterion, 0))
        # Normalize 1-5 to 0-1
        normalized = max(0.0, min(1.0, raw / 5.0))
        contribution = w * normalized
        if criterion in PENALTY_CRITERIA:
            # Penalty: invert (higher raw = lower contribution)
            contribution = w * (1.0 - normalized)
        per[criterion] = round(contribution, 4)
        total += contribution
    opt.weighted_score = round(total, 4)
    opt.per_criterion = per
    return opt


def total_3yr_cost(opt: Option) -> float:
    return opt.migration_cost_usd + opt.annual_tco_usd * 3.0


def make_recommendation(options: list[Option]) -> dict[str, Any]:
    if not options:
        return {"recommendation": "no options provided", "tier_1": [], "tier_2": []}
    sorted_opts = sorted(options, key=lambda o: o.weighted_score, reverse=True)
    top = sorted_opts[0]
    runner = sorted_opts[1] if len(sorted_opts) > 1 else None
    gap = (top.weighted_score - runner.weighted_score) if runner else 1.0
    tier_1 = [top.name]
    tier_2: list[str] = []
    if runner and gap < 0.05:
        tier_1.append(runner.name)
        verdict = (f"Recommend **{top.name}** with **{runner.name}** as a close runner-up "
                   f"(gap {gap:.3f}). Run a 30-day proof to break the tie.")
    elif runner:
        tier_2.append(runner.name)
        verdict = (f"Recommend **{top.name}** (clear leader; gap {gap:.3f} over {runner.name}).")
    else:
        verdict = f"Only one option provided; **{top.name}** wins by default."

    return {
        "recommendation": verdict,
        "tier_1": tier_1,
        "tier_2": tier_2,
        "winner": top.name,
        "winner_score": top.weighted_score,
        "winner_3yr_cost_usd": total_3yr_cost(top),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Data Platform Evaluation — {report['scope']}")
    lines.append(f"_evaluator: {report['evaluator']}_\n")
    lines.append("## Weights used")
    lines.append("| Criterion | Weight |")
    lines.append("|-----------|--------|")
    for k, v in report["weights"].items():
        lines.append(f"| {k} | {v:.0%} |")
    lines.append("")
    lines.append("## Comparison")
    weights = list(report["weights"].keys())
    header = "| Option | " + " | ".join(weights) + " | Weighted total | 3-yr TCO |"
    sep = "|--------|" + "---|" * len(weights) + "----------------|----------|"
    lines.append(header)
    lines.append(sep)
    for o in report["options"]:
        per = o["per_criterion"]
        row = f"| {o['name']} | "
        row += " | ".join(f"{per.get(k, 0):.3f}" for k in weights)
        row += f" | **{o['weighted_score']:.3f}** | ${o['three_yr_cost_usd']:,.0f} |"
        lines.append(row)
    lines.append("")
    lines.append("## Recommendation")
    lines.append(report["recommendation_block"]["recommendation"])
    lines.append("")
    lines.append("## Per-option notes")
    for o in report["options"]:
        lines.append(f"### {o['name']}")
        lines.append(f"- Annual TCO: ${o['annual_tco_usd']:,.0f}")
        lines.append(f"- Migration cost: ${o['migration_cost_usd']:,.0f}")
        lines.append(f"- 3-yr cost: ${o['three_yr_cost_usd']:,.0f}")
        if o.get("notes"):
            lines.append(f"- Notes: {o['notes']}")
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Evaluate data platform options against weighted criteria",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON file with options")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
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

    weights = normalize_weights(raw.get("weights"))
    options: list[Option] = []
    for r in raw.get("options", []):
        options.append(Option(
            name=r.get("name", ""),
            annual_tco_usd=float(r.get("annual_tco_usd", 0)),
            migration_cost_usd=float(r.get("migration_cost_usd", 0)),
            scores={k: float(v) for k, v in (r.get("scores") or {}).items()},
            notes=r.get("notes", ""),
        ))

    for opt in options:
        score_option(opt, weights)

    rec = make_recommendation(options)
    report = {
        "scope": raw.get("scope", ""),
        "evaluator": raw.get("evaluator", ""),
        "weights": weights,
        "options": [
            {
                "name": o.name,
                "annual_tco_usd": o.annual_tco_usd,
                "migration_cost_usd": o.migration_cost_usd,
                "three_yr_cost_usd": total_3yr_cost(o),
                "scores": o.scores,
                "per_criterion": o.per_criterion,
                "weighted_score": o.weighted_score,
                "notes": o.notes,
            }
            for o in sorted(options, key=lambda x: x.weighted_score, reverse=True)
        ],
        "recommendation_block": rec,
    }

    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
