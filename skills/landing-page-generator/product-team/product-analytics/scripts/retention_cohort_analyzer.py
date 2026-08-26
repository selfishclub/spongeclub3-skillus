#!/usr/bin/env python3
"""
retention_cohort_analyzer.py — Compute retention rates from cohort tables,
classify curve shape, and surface cohort-level alerts.

Reads a JSON of cohort tables (raw counts per cohort week per offset);
computes percentage retention, identifies trend (improving / stable /
deteriorating), classifies curve shape (smile, slow-decay, leaky bucket,
steep, rising); flags alerts.

Stdlib only. JSON or markdown output.

Usage:
    python3 retention_cohort_analyzer.py --input retention.json
    python3 retention_cohort_analyzer.py --input retention.json --format markdown

Input schema:
{
  "as_of": "2026-05-27",
  "product_name": "Acme",
  "cohort_unit": "week",            # week|day|month
  "anchor_offsets": [0, 1, 2, 4, 8, 12],
  "cohorts": [
      {
          "cohort_label": "2026-01-01",
          "size": 1000,
          "counts_by_offset": [1000, 400, 320, 240, 220, 200]
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
class CohortResult:
    cohort_label: str
    size: int
    rates_by_offset: dict[int, float] = field(default_factory=dict)


def compute_rates(cohort: dict[str, Any], offsets: list[int]) -> CohortResult:
    size = int(cohort.get("size", 0) or 0)
    counts = cohort.get("counts_by_offset", []) or []
    rates: dict[int, float] = {}
    for i, off in enumerate(offsets):
        if i < len(counts) and size > 0:
            rates[off] = round((counts[i] / size) * 100, 1)
        else:
            rates[off] = -1  # sentinel for "not yet observed"
    return CohortResult(
        cohort_label=cohort.get("cohort_label", ""),
        size=size,
        rates_by_offset=rates,
    )


def classify_shape(rates: dict[int, float]) -> tuple[str, str]:
    """Return (shape_label, diagnosis)."""
    sorted_offsets = sorted(o for o, r in rates.items() if r >= 0)
    if len(sorted_offsets) < 3:
        return ("insufficient_data", "Need at least 3 observation points")

    values = [rates[o] for o in sorted_offsets]
    first = values[0]
    last = values[-1]
    mid_idx = len(values) // 2
    mid = values[mid_idx]
    second_half = values[mid_idx:]

    # Rising: last > mid by meaningful amount
    if last > mid + 5 and last > first * 0.5:
        return ("rising", "Network effects or rising engagement; rare and healthy")

    # Smile / power-law: drops fast then flattens
    drop_pct_first_half = ((first - mid) / max(first, 1)) * 100
    if drop_pct_first_half > 50 and last >= mid * 0.85:
        return ("smile", "Power-law smile; strong PMF in retained users")

    # Linear / leaky bucket
    if last < first * 0.2 and all(values[i] > values[i+1] for i in range(len(values)-1)):
        return ("leaky_bucket", "Linear decline; users keep churning; no flatten")

    # Steep then near zero
    if last < first * 0.05:
        return ("steep_to_zero", "Novelty product; few find lasting value")

    # Slow decay then flat
    if last > first * 0.2 and drop_pct_first_half < 50:
        return ("slow_decay_flat", "Slow decay then flat; healthy partial PMF")

    return ("ambiguous", "Curve shape ambiguous; investigate per-segment")


def trend_across_cohorts(cohort_results: list[CohortResult], anchor_offset: int) -> str:
    rates = []
    for c in cohort_results:
        v = c.rates_by_offset.get(anchor_offset, -1)
        if v >= 0:
            rates.append(v)
    if len(rates) < 3:
        return "insufficient_data"
    first_third = rates[:max(1, len(rates) // 3)]
    last_third = rates[-max(1, len(rates) // 3):]
    avg_first = sum(first_third) / len(first_third)
    avg_last = sum(last_third) / len(last_third)
    delta = avg_last - avg_first
    if delta > 3:
        return "improving"
    if delta < -3:
        return "deteriorating"
    return "stable"


def cohort_alerts(cohort_results: list[CohortResult], anchor_offset: int) -> list[dict[str, Any]]:
    alerts: list[dict[str, Any]] = []
    if not cohort_results:
        return alerts
    rates = [(c, c.rates_by_offset.get(anchor_offset, -1)) for c in cohort_results]
    valid = [(c, r) for c, r in rates if r >= 0]
    if not valid:
        return alerts
    median = sorted(r for _, r in valid)[len(valid) // 2]
    for c, r in valid:
        if r < median - 5:
            alerts.append({
                "cohort_label": c.cohort_label,
                "offset": anchor_offset,
                "rate_pct": r,
                "median_pct": median,
                "deficit_pp": round(median - r, 1),
                "note": f"cohort {c.cohort_label} below median at W{anchor_offset}",
            })
    return alerts


def analyze(state: dict[str, Any]) -> dict[str, Any]:
    offsets = list(state.get("anchor_offsets", [0, 1, 2, 4, 8, 12]))
    cohorts = state.get("cohorts", []) or []
    results = [compute_rates(c, offsets) for c in cohorts]

    # Use the latest fully-observed cohort to classify shape
    fully_observed = [r for r in results if all(v >= 0 for v in r.rates_by_offset.values())]
    if fully_observed:
        shape, diagnosis = classify_shape(fully_observed[-1].rates_by_offset)
        shape_cohort = fully_observed[-1].cohort_label
    else:
        shape, diagnosis = ("insufficient_data", "no fully-observed cohort yet")
        shape_cohort = ""

    # Anchor offset for trend: max stable offset (skip 0)
    anchor = sorted(offsets)[len(offsets) // 2] if offsets else 4
    trend = trend_across_cohorts(results, anchor)
    alerts = cohort_alerts(results, anchor)

    return {
        "as_of": state.get("as_of", ""),
        "product_name": state.get("product_name", ""),
        "cohort_unit": state.get("cohort_unit", "week"),
        "anchor_offsets": offsets,
        "trend_anchor_offset": anchor,
        "trend": trend,
        "latest_curve_shape": {
            "cohort_label": shape_cohort,
            "shape": shape,
            "diagnosis": diagnosis,
        },
        "cohorts": [
            {
                "cohort_label": r.cohort_label,
                "size": r.size,
                "rates_by_offset": {str(o): v for o, v in r.rates_by_offset.items()},
            }
            for r in results
        ],
        "alerts": alerts,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Retention Cohort Analysis — {report.get('product_name','(unnamed)')}")
    lines.append(f"_as of {report['as_of']} | unit: {report['cohort_unit']}_\n")
    sh = report["latest_curve_shape"]
    lines.append(f"## Latest curve shape: **{sh['shape']}**")
    lines.append(f"_{sh['diagnosis']}_  (based on cohort {sh['cohort_label'] or '—'})\n")
    lines.append(f"## Trend at W{report['trend_anchor_offset']}: **{report['trend']}**\n")

    offsets = report["anchor_offsets"]
    lines.append("## Cohort table")
    header = "| Cohort | Size | " + " | ".join(f"W{o}" for o in offsets) + " |"
    sep = "|--------|------|" + "|".join("------" for _ in offsets) + "|"
    lines.append(header)
    lines.append(sep)
    for c in report["cohorts"]:
        rates = c["rates_by_offset"]
        row = f"| {c['cohort_label']} | {c['size']} | " + " | ".join(
            f"{rates.get(str(o), -1)}%" if rates.get(str(o), -1) >= 0 else "—"
            for o in offsets
        ) + " |"
        lines.append(row)
    lines.append("")
    if report["alerts"]:
        lines.append("## Alerts (cohorts below median)")
        lines.append(f"| Cohort | W{report['trend_anchor_offset']} | Median | Deficit |")
        lines.append("|--------|---------|--------|---------|")
        for a in report["alerts"]:
            lines.append(f"| {a['cohort_label']} | {a['rate_pct']}% | {a['median_pct']}% | "
                        f"{a['deficit_pp']}pp |")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Analyze cohort retention; classify curve shape + trend",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of cohort data")
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

    report = analyze(state)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
