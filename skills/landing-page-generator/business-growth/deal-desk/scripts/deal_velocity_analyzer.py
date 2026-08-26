#!/usr/bin/env python3
"""
deal_velocity_analyzer.py — Analyze deal-desk velocity from a CRM CSV export.

Reads CSV with columns including: deal_id, submitted_at, decision_at,
approval_status, approver, discount_pct, acv, sla_target_business_days.

Emits:
  - Median, p90 time-to-decision (in business days)
  - Approval rate
  - Per-approver bottleneck identification
  - Aging deals (not decided)
  - Discount distribution / outlier flags

Stdlib only. Markdown or JSON output.

Usage:
    python3 deal_velocity_analyzer.py --deals deals.csv
    python3 deal_velocity_analyzer.py --deals deals.csv --format json
    python3 deal_velocity_analyzer.py --deals deals.csv --as-of '2026-05-27T00:00:00Z'
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from collections import defaultdict
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


@dataclass
class DealRecord:
    deal_id: str
    submitted_at: datetime | None
    decision_at: datetime | None
    approval_status: str  # approved / declined / countered / pending
    approver: str
    discount_pct: float
    acv: float
    sla_target_business_days: float | None


def parse_dt(s: str) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def load_deals(path: Path) -> list[DealRecord]:
    deals: list[DealRecord] = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                discount = float(row.get("discount_pct", 0) or 0)
            except ValueError:
                discount = 0
            try:
                acv = float(row.get("acv", 0) or 0)
            except ValueError:
                acv = 0
            try:
                sla = float(row.get("sla_target_business_days", 0) or 0) or None
            except ValueError:
                sla = None
            deals.append(DealRecord(
                deal_id=str(row.get("deal_id", "")),
                submitted_at=parse_dt(row.get("submitted_at", "")),
                decision_at=parse_dt(row.get("decision_at", "")),
                approval_status=str(row.get("approval_status", "pending")).lower(),
                approver=str(row.get("approver", "")),
                discount_pct=discount,
                acv=acv,
                sla_target_business_days=sla,
            ))
    return deals


def business_days_between(start: datetime, end: datetime) -> float:
    """Rough: actual elapsed days × 5/7 (approximation excluding weekends)."""
    if not start or not end or end <= start:
        return 0
    elapsed_days = (end - start).total_seconds() / 86400
    return round(elapsed_days * 5 / 7, 2)


@dataclass
class VelocityAnalysis:
    total_deals: int
    pending_deals: int
    decided_deals: int
    approved: int
    declined: int
    countered: int
    median_time_to_decision_bd: float
    p90_time_to_decision_bd: float
    p99_time_to_decision_bd: float
    approval_rate_pct: float
    sla_breach_count: int
    sla_breach_pct: float
    approver_breakdown: dict[str, dict[str, Any]]
    aging_deals: list[dict[str, Any]]
    discount_distribution: dict[str, Any]
    discount_outliers: list[dict[str, Any]]


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    k = (len(s) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(s) - 1)
    return s[f] + (s[c] - s[f]) * (k - f)


def analyze(deals: list[DealRecord], as_of: datetime) -> VelocityAnalysis:
    decided = [d for d in deals if d.decision_at and d.submitted_at]
    pending = [d for d in deals if not d.decision_at and d.submitted_at]

    ttd_bd = [business_days_between(d.submitted_at, d.decision_at) for d in decided]
    median_ttd = round(statistics.median(ttd_bd), 2) if ttd_bd else 0.0
    p90_ttd = round(percentile(ttd_bd, 90), 2) if ttd_bd else 0.0
    p99_ttd = round(percentile(ttd_bd, 99), 2) if ttd_bd else 0.0

    approved = sum(1 for d in decided if d.approval_status == "approved")
    declined = sum(1 for d in decided if d.approval_status == "declined")
    countered = sum(1 for d in decided if d.approval_status == "countered")
    approval_rate = round(100 * approved / len(decided), 1) if decided else 0.0

    sla_breaches = [d for d in decided if d.sla_target_business_days
                    and business_days_between(d.submitted_at, d.decision_at) > d.sla_target_business_days]
    sla_breach_pct = round(100 * len(sla_breaches) / len(decided), 1) if decided else 0.0

    # Per-approver
    by_approver: dict[str, list[DealRecord]] = defaultdict(list)
    for d in decided:
        if d.approver:
            by_approver[d.approver].append(d)
    approver_breakdown: dict[str, dict[str, Any]] = {}
    for approver, ds in by_approver.items():
        times = [business_days_between(d.submitted_at, d.decision_at) for d in ds]
        approver_breakdown[approver] = {
            "count": len(ds),
            "median_bd": round(statistics.median(times), 2) if times else 0.0,
            "p90_bd": round(percentile(times, 90), 2) if times else 0.0,
            "is_bottleneck": (
                round(statistics.median(times), 2) if times else 0.0
            ) > median_ttd * 1.5,
        }

    # Aging
    aging = []
    for d in pending:
        age_bd = business_days_between(d.submitted_at, as_of)
        sla_target = d.sla_target_business_days or 2.0
        if age_bd > sla_target:
            aging.append({
                "deal_id": d.deal_id,
                "submitted_at": d.submitted_at.isoformat() if d.submitted_at else "",
                "age_bd": age_bd,
                "sla_target_bd": sla_target,
                "over_sla_by_bd": round(age_bd - sla_target, 2),
                "approver": d.approver,
                "acv": d.acv,
            })
    aging.sort(key=lambda x: -x["over_sla_by_bd"])

    # Discount distribution
    discounts = [d.discount_pct for d in decided if d.discount_pct]
    discount_dist = {
        "count": len(discounts),
        "median": round(statistics.median(discounts), 1) if discounts else 0,
        "mean": round(statistics.mean(discounts), 1) if discounts else 0,
        "p90": round(percentile(discounts, 90), 1) if discounts else 0,
        "p99": round(percentile(discounts, 99), 1) if discounts else 0,
        "stdev": round(statistics.stdev(discounts), 1) if len(discounts) > 1 else 0,
    }

    # Discount outliers (> mean + 2 stdev)
    threshold = discount_dist["mean"] + 2 * discount_dist["stdev"]
    outliers = []
    for d in decided:
        if d.discount_pct > threshold and threshold > 0:
            outliers.append({
                "deal_id": d.deal_id,
                "discount_pct": d.discount_pct,
                "acv": d.acv,
                "approver": d.approver,
                "decision_at": d.decision_at.isoformat() if d.decision_at else "",
            })

    return VelocityAnalysis(
        total_deals=len(deals),
        pending_deals=len(pending),
        decided_deals=len(decided),
        approved=approved,
        declined=declined,
        countered=countered,
        median_time_to_decision_bd=median_ttd,
        p90_time_to_decision_bd=p90_ttd,
        p99_time_to_decision_bd=p99_ttd,
        approval_rate_pct=approval_rate,
        sla_breach_count=len(sla_breaches),
        sla_breach_pct=sla_breach_pct,
        approver_breakdown=approver_breakdown,
        aging_deals=aging[:20],
        discount_distribution=discount_dist,
        discount_outliers=outliers[:20],
    )


def render_markdown(a: VelocityAnalysis) -> str:
    out: list[str] = ["# Deal Desk Velocity Analysis", ""]
    out.append(f"_Total deals analyzed: {a.total_deals}_")
    out.append("")
    out.append("## Summary")
    out.append("")
    out.append(f"- **Total**: {a.total_deals}")
    out.append(f"- **Decided**: {a.decided_deals}")
    out.append(f"- **Pending**: {a.pending_deals}")
    out.append(f"- **Approved**: {a.approved} ({a.approval_rate_pct}%)")
    out.append(f"- **Declined**: {a.declined}")
    out.append(f"- **Countered**: {a.countered}")
    out.append("")
    out.append("## Time-to-Decision (business days)")
    out.append("")
    out.append(f"- **Median**: {a.median_time_to_decision_bd}")
    out.append(f"- **p90**: {a.p90_time_to_decision_bd}")
    out.append(f"- **p99**: {a.p99_time_to_decision_bd}")
    out.append(f"- **SLA breaches**: {a.sla_breach_count} ({a.sla_breach_pct}%)")
    out.append("")
    if a.approver_breakdown:
        out.append("## Per-Approver Performance")
        out.append("")
        out.append("| Approver | Count | Median BD | p90 BD | Bottleneck |")
        out.append("|----------|-------|-----------|--------|------------|")
        for ap, info in sorted(a.approver_breakdown.items(), key=lambda x: -x[1]["count"]):
            bn = "⚠️ YES" if info["is_bottleneck"] else "no"
            out.append(f"| {ap} | {info['count']} | {info['median_bd']} | {info['p90_bd']} | {bn} |")
        out.append("")
    if a.aging_deals:
        out.append(f"## Aging Deals (over SLA)  — top 20")
        out.append("")
        out.append("| Deal ID | Approver | ACV | Age BD | Over SLA By |")
        out.append("|---------|----------|-----|--------|-------------|")
        for d in a.aging_deals:
            out.append(f"| {d['deal_id']} | {d['approver']} | ${d['acv']:,.0f} | {d['age_bd']} | +{d['over_sla_by_bd']} |")
        out.append("")
    out.append("## Discount Distribution")
    out.append("")
    dd = a.discount_distribution
    out.append(f"- **Median**: {dd['median']}%")
    out.append(f"- **Mean**: {dd['mean']}%")
    out.append(f"- **p90**: {dd['p90']}%")
    out.append(f"- **p99**: {dd['p99']}%")
    out.append(f"- **Stdev**: {dd['stdev']}%")
    out.append("")
    if a.discount_outliers:
        out.append("## Discount Outliers (> mean + 2σ)")
        out.append("")
        out.append("| Deal ID | Discount % | ACV | Approver | Decision Date |")
        out.append("|---------|-----------|-----|----------|---------------|")
        for o in a.discount_outliers:
            out.append(f"| {o['deal_id']} | {o['discount_pct']}% | ${o['acv']:,.0f} | {o['approver']} | {o['decision_at'][:10]} |")
        out.append("")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Analyze deal-desk velocity from a CRM CSV export",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--deals", required=True, help="CSV file of deals")
    p.add_argument("--as-of", help="Reference 'now' for aging calc (ISO 8601); default: actual now")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", help="Output file path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        deals = load_deals(Path(args.deals))
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if args.as_of:
        try:
            as_of = datetime.fromisoformat(args.as_of.replace("Z", "+00:00"))
        except ValueError:
            print(f"error: invalid --as-of: {args.as_of}", file=sys.stderr)
            return 2
    else:
        as_of = datetime.now(timezone.utc)
    analysis = analyze(deals, as_of)
    if args.format == "json":
        out = json.dumps(asdict(analysis), indent=2, default=str)
    else:
        out = render_markdown(analysis)
    if args.output:
        Path(args.output).write_text(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
