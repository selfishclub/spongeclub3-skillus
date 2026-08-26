#!/usr/bin/env python3
"""
eng_capacity_planner.py — Project engineering capacity over the next N
quarters, allowing for attrition, hiring ramp, and overhead tax. Surfaces
bottleneck teams and over/undersupply against demand.

Reads a JSON with teams, current headcount, hiring plan, demand (in
engineer-quarters) by theme; outputs quarter-by-quarter projection.

Stdlib only. JSON or markdown output.

Usage:
    python3 eng_capacity_planner.py --input capacity_inputs.json
    python3 eng_capacity_planner.py --input capacity_inputs.json --format markdown
    python3 eng_capacity_planner.py --input capacity_inputs.json --quarters 4

Input schema:
{
  "starting_quarter": "Q3-2026",
  "horizon_quarters": 4,
  "overhead_pct": 35,                   # PTO + on-call + meetings + recruiting + support
  "ramp_curve": [0.3, 0.6, 0.9, 1.0],   # quarter 1, 2, 3, 4+ multipliers for new hires
  "regrettable_attrition_pct_annual": 8,
  "teams": [
      {
          "id": "team-payments",
          "name": "Payments",
          "current_engineers": 8,
          "hires_planned_by_quarter": [1, 2, 0, 0],
          "demand_eng_quarters_per_quarter": [9, 10, 11, 11],
          "investment_bucket_mix": {"run": 50, "grow": 35, "transform": 15}
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


@dataclass
class QuarterReport:
    quarter_index: int
    quarter_label: str
    headcount_start: float
    hires: int
    attrition: float
    headcount_end: float
    raw_eng_quarters: float
    useful_eng_quarters: float
    demand_eng_quarters: float
    surplus_deficit: float
    utilization_pct: float


@dataclass
class TeamProjection:
    id: str
    name: str
    starting_headcount: int
    quarters: list[QuarterReport] = field(default_factory=list)
    total_useful: float = 0.0
    total_demand: float = 0.0
    total_surplus: float = 0.0
    is_bottleneck: bool = False


def quarter_labels(start: str, n: int) -> list[str]:
    # Simple Qx-YYYY arithmetic
    out = []
    try:
        prefix, year = start.split("-")
        q = int(prefix[1])
        y = int(year)
    except (ValueError, IndexError):
        return [f"Q{i+1}" for i in range(n)]
    for _ in range(n):
        out.append(f"Q{q}-{y}")
        q += 1
        if q > 4:
            q = 1
            y += 1
    return out


def ramp_multiplier(curve: list[float], qtrs_since_hire: int) -> float:
    if qtrs_since_hire < 0:
        return 0.0
    if qtrs_since_hire >= len(curve):
        return curve[-1]
    return curve[qtrs_since_hire]


def project_team(team: dict[str, Any], horizon: int, labels: list[str],
                 overhead_pct: float, ramp_curve: list[float],
                 attrition_annual_pct: float) -> TeamProjection:
    start_hc = int(team.get("current_engineers", 0) or 0)
    name = team.get("name", "")
    tid = team.get("id", "")
    hires_plan = list(team.get("hires_planned_by_quarter", []) or [])
    demand = list(team.get("demand_eng_quarters_per_quarter", []) or [])

    # Pad to horizon
    while len(hires_plan) < horizon:
        hires_plan.append(0)
    while len(demand) < horizon:
        demand.append(0)

    proj = TeamProjection(id=tid, name=name, starting_headcount=start_hc)

    # Track each hire's ramp (record hires by quarter they were added)
    hire_cohorts: list[tuple[int, int]] = []  # (added_quarter_index, count)

    hc = float(start_hc)
    overhead_factor = 1.0 - (overhead_pct / 100.0)
    q_attrition = attrition_annual_pct / 100.0 / 4.0

    for q in range(horizon):
        # Apply attrition at quarter start (subtract from existing tenured pool)
        attrition_loss = hc * q_attrition
        hc = max(0.0, hc - attrition_loss)
        # Add new hires
        added = int(hires_plan[q])
        hire_cohorts.append((q, added))
        hc_after_hires = hc + added

        # Compute useful eng-quarters: tenured at full * overhead + new cohorts at ramp
        # Tenured = hc (pre-add, post-attrition)
        useful_tenured = hc * overhead_factor
        # Each cohort contributes based on ramp multiplier in current quarter
        useful_cohorts = 0.0
        for added_q, count in hire_cohorts:
            qtrs_since = q - added_q
            mult = ramp_multiplier(ramp_curve, qtrs_since)
            useful_cohorts += count * mult * overhead_factor

        # Tenured count excludes the cohorts (already counted)
        useful = useful_tenured + useful_cohorts
        raw_eq = hc_after_hires  # 1 engineer-quarter per engineer
        d = float(demand[q])
        surplus = useful - d
        util = round((d / useful) * 100, 1) if useful > 0 else 0

        proj.quarters.append(QuarterReport(
            quarter_index=q,
            quarter_label=labels[q] if q < len(labels) else f"Q+{q}",
            headcount_start=hc + attrition_loss,
            hires=added,
            attrition=round(attrition_loss, 1),
            headcount_end=round(hc_after_hires, 1),
            raw_eng_quarters=round(raw_eq, 1),
            useful_eng_quarters=round(useful, 1),
            demand_eng_quarters=d,
            surplus_deficit=round(surplus, 1),
            utilization_pct=util,
        ))

        proj.total_useful += useful
        proj.total_demand += d
        proj.total_surplus += surplus

        hc = hc_after_hires

    proj.total_useful = round(proj.total_useful, 1)
    proj.total_demand = round(proj.total_demand, 1)
    proj.total_surplus = round(proj.total_surplus, 1)
    proj.is_bottleneck = proj.total_surplus < 0
    return proj


def org_rollup(team_reports: list[TeamProjection]) -> dict[str, Any]:
    total_useful = round(sum(t.total_useful for t in team_reports), 1)
    total_demand = round(sum(t.total_demand for t in team_reports), 1)
    total_surplus = round(total_useful - total_demand, 1)
    bottlenecks = [t.name for t in team_reports if t.is_bottleneck]
    return {
        "total_useful_eng_quarters": total_useful,
        "total_demand_eng_quarters": total_demand,
        "surplus_deficit": total_surplus,
        "bottleneck_team_count": len(bottlenecks),
        "bottleneck_teams": bottlenecks,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Engineering Capacity Plan — starting {report['starting_quarter']}")
    lines.append(f"_horizon: {report['horizon_quarters']} quarters | "
                f"overhead: {report['overhead_pct']}% | "
                f"attrition: {report['attrition_pct_annual']}% annual_\n")
    ro = report["rollup"]
    lines.append("## Org rollup")
    lines.append(f"- Useful capacity: **{ro['total_useful_eng_quarters']:.1f}** engineer-quarters")
    lines.append(f"- Demand: **{ro['total_demand_eng_quarters']:.1f}** engineer-quarters")
    lines.append(f"- Surplus / deficit: **{ro['surplus_deficit']:.1f}**")
    lines.append(f"- Bottleneck teams: {ro['bottleneck_team_count']}")
    if ro["bottleneck_teams"]:
        lines.append("  - " + ", ".join(ro["bottleneck_teams"]))
    lines.append("")
    lines.append("## Per-team projection")
    for t in report["teams"]:
        flag = " (BOTTLENECK)" if t["is_bottleneck"] else ""
        lines.append(f"### {t['name']}{flag}")
        lines.append(f"_starting headcount: {t['starting_headcount']} | "
                    f"total useful: {t['total_useful']} | total demand: {t['total_demand']} | "
                    f"surplus/deficit: {t['total_surplus']}_\n")
        lines.append("| Quarter | HC start | Hires | Attrition | HC end | Useful | Demand | Δ | Util |")
        lines.append("|---------|----------|-------|-----------|--------|--------|--------|---|------|")
        for q in t["quarters"]:
            lines.append(
                f"| {q['quarter_label']} | {q['headcount_start']:.1f} | {q['hires']} | "
                f"{q['attrition']:.1f} | {q['headcount_end']:.1f} | "
                f"{q['useful_eng_quarters']:.1f} | {q['demand_eng_quarters']:.1f} | "
                f"{q['surplus_deficit']:.1f} | {q['utilization_pct']}% |"
            )
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Project engineering capacity over upcoming quarters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of capacity inputs")
    p.add_argument("--quarters", type=int, help="Override horizon (default from JSON)")
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

    horizon = args.quarters or int(raw.get("horizon_quarters", 4) or 4)
    overhead = float(raw.get("overhead_pct", 35) or 35)
    ramp = list(raw.get("ramp_curve", [0.3, 0.6, 0.9, 1.0]) or [0.3, 0.6, 0.9, 1.0])
    attrition = float(raw.get("regrettable_attrition_pct_annual", 8) or 8)
    starting_q = raw.get("starting_quarter", "Q1-2026")
    labels = quarter_labels(starting_q, horizon)

    team_reports = [
        project_team(t, horizon, labels, overhead, ramp, attrition)
        for t in raw.get("teams", [])
    ]
    ro = org_rollup(team_reports)

    out_data = {
        "starting_quarter": starting_q,
        "horizon_quarters": horizon,
        "overhead_pct": overhead,
        "ramp_curve": ramp,
        "attrition_pct_annual": attrition,
        "rollup": ro,
        "teams": [
            {
                "id": t.id, "name": t.name, "starting_headcount": t.starting_headcount,
                "total_useful": t.total_useful, "total_demand": t.total_demand,
                "total_surplus": t.total_surplus, "is_bottleneck": t.is_bottleneck,
                "quarters": [
                    {
                        "quarter_label": q.quarter_label,
                        "headcount_start": round(q.headcount_start, 1),
                        "hires": q.hires, "attrition": q.attrition,
                        "headcount_end": q.headcount_end,
                        "raw_eng_quarters": q.raw_eng_quarters,
                        "useful_eng_quarters": q.useful_eng_quarters,
                        "demand_eng_quarters": q.demand_eng_quarters,
                        "surplus_deficit": q.surplus_deficit,
                        "utilization_pct": q.utilization_pct,
                    }
                    for q in t.quarters
                ],
            }
            for t in team_reports
        ],
    }

    out = render_markdown(out_data) if args.format == "markdown" else json.dumps(out_data, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
