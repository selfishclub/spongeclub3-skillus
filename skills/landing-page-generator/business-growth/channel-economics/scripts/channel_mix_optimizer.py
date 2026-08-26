#!/usr/bin/env python3
"""
channel_mix_optimizer.py — Analyze channel mix and recommend rebalancing.

Reads a CSV of revenue + cost per channel per period; emits:
  - Revenue share by channel
  - Contribution margin share by channel
  - ROI per channel (contribution / investment)
  - Rebalancing recommendations

Stdlib only. Markdown or JSON output.

Usage:
    python3 channel_mix_optimizer.py --revenue revenue.csv
    python3 channel_mix_optimizer.py --revenue revenue.csv --format json

CSV format (header required):
    channel,period,revenue,partner_margin,sales_cost,marketing_cost,other_cost
    direct,2026-Q1,2000000,0,500000,200000,150000
    reseller,2026-Q1,800000,200000,40000,50000,40000
    marketplace,2026-Q1,500000,15000,40000,25000,15000
    ...
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class ChannelSnapshot:
    channel: str
    revenue: float
    partner_margin: float
    sales_cost: float
    marketing_cost: float
    other_cost: float
    contribution: float
    contribution_pct: float
    investment: float  # sales + marketing + other (cost of running the channel)
    roi: float


def load_csv(path: Path) -> list[dict[str, str]]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def aggregate_by_channel(rows: list[dict[str, str]]) -> dict[str, dict[str, float]]:
    by_channel: dict[str, dict[str, float]] = defaultdict(lambda: {
        "revenue": 0.0, "partner_margin": 0.0, "sales_cost": 0.0,
        "marketing_cost": 0.0, "other_cost": 0.0,
    })
    for r in rows:
        c = r["channel"]
        for key in ("revenue", "partner_margin", "sales_cost", "marketing_cost", "other_cost"):
            try:
                by_channel[c][key] += float(r.get(key, 0) or 0)
            except ValueError:
                pass
    return by_channel


def build_snapshots(agg: dict[str, dict[str, float]]) -> list[ChannelSnapshot]:
    out: list[ChannelSnapshot] = []
    for ch, vals in agg.items():
        contribution = vals["revenue"] - vals["partner_margin"] - vals["sales_cost"] - vals["marketing_cost"] - vals["other_cost"]
        contribution_pct = round(100 * contribution / vals["revenue"], 1) if vals["revenue"] else 0
        investment = vals["sales_cost"] + vals["marketing_cost"] + vals["other_cost"]
        roi = round(contribution / investment, 2) if investment > 0 else 0
        out.append(ChannelSnapshot(
            channel=ch,
            revenue=round(vals["revenue"], 2),
            partner_margin=round(vals["partner_margin"], 2),
            sales_cost=round(vals["sales_cost"], 2),
            marketing_cost=round(vals["marketing_cost"], 2),
            other_cost=round(vals["other_cost"], 2),
            contribution=round(contribution, 2),
            contribution_pct=contribution_pct,
            investment=round(investment, 2),
            roi=roi,
        ))
    return out


def recommendations(snapshots: list[ChannelSnapshot]) -> list[str]:
    recs: list[str] = []
    total_rev = sum(s.revenue for s in snapshots)
    total_contrib = sum(s.contribution for s in snapshots)
    sorted_by_roi = sorted(snapshots, key=lambda s: -s.roi)
    for s in snapshots:
        rev_share = round(100 * s.revenue / total_rev, 1) if total_rev else 0
        contrib_share = round(100 * s.contribution / total_contrib, 1) if total_contrib else 0
        if rev_share > contrib_share + 10:
            recs.append(f"[REBALANCE] `{s.channel}` is {rev_share}% of revenue but only {contrib_share}% of contribution — reduce investment or improve channel efficiency.")
        elif contrib_share > rev_share + 10:
            recs.append(f"[INVEST] `{s.channel}` is {contrib_share}% of contribution but only {rev_share}% of revenue — consider increasing investment.")
        if s.roi < 1 and s.investment > 100000:
            recs.append(f"[REVIEW] `{s.channel}` has ROI {s.roi} — investment exceeds contribution; investigate or wind down.")
        elif s.roi > 5:
            recs.append(f"[ACCELERATE] `{s.channel}` has ROI {s.roi} — highest-leverage channel; scale investment.")
    if not recs:
        recs.append("Channel mix appears balanced. No major rebalancing recommended.")
    return recs


def render_markdown(snapshots: list[ChannelSnapshot]) -> str:
    out = ["# Channel Mix Analysis", ""]
    total_rev = sum(s.revenue for s in snapshots)
    total_contrib = sum(s.contribution for s in snapshots)
    out.append(f"_Total revenue: ${total_rev:,.0f}_  ")
    out.append(f"_Total contribution: ${total_contrib:,.0f} ({round(100*total_contrib/total_rev,1) if total_rev else 0}%)_")
    out.append("")
    out.append("## Per-Channel Summary")
    out.append("")
    out.append("| Channel | Revenue | Rev Share | Contribution | Contrib Share | Contrib % | Investment | ROI |")
    out.append("|---------|---------|-----------|--------------|---------------|-----------|------------|-----|")
    for s in sorted(snapshots, key=lambda x: -x.revenue):
        rs = round(100 * s.revenue / total_rev, 1) if total_rev else 0
        cs = round(100 * s.contribution / total_contrib, 1) if total_contrib else 0
        out.append(f"| {s.channel} | ${s.revenue:,.0f} | {rs}% | ${s.contribution:,.0f} | {cs}% | {s.contribution_pct}% | ${s.investment:,.0f} | {s.roi}x |")
    out.append("")
    out.append("## Recommendations")
    out.append("")
    for r in recommendations(snapshots):
        out.append(f"- {r}")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Analyze channel mix and recommend rebalancing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--revenue", required=True, help="CSV of channel revenue + costs")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", help="Output file path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        rows = load_csv(Path(args.revenue))
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    agg = aggregate_by_channel(rows)
    snapshots = build_snapshots(agg)
    if args.format == "json":
        out = json.dumps(
            {"snapshots": [asdict(s) for s in snapshots], "recommendations": recommendations(snapshots)},
            indent=2,
        )
    else:
        out = render_markdown(snapshots)
    if args.output:
        Path(args.output).write_text(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
