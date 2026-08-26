#!/usr/bin/env python3
"""
contract_portfolio_analyzer.py — Analyze a contract portfolio for
concentration, exposure, deviation rate, and upcoming renewals.

Reads a JSON of contracts; computes counterparty concentration, aggregate
liability exposure, deviation rate by tier/type, expiring-soon list, and
renewal pipeline; outputs JSON or markdown.

Stdlib only.

Usage:
    python3 contract_portfolio_analyzer.py --input contracts.json
    python3 contract_portfolio_analyzer.py --input contracts.json --format markdown
    python3 contract_portfolio_analyzer.py --input contracts.json --renewal-window-days 90

Input schema:
{
  "as_of": "2026-05-27",
  "contracts": [
      {
          "id": "CON-001",
          "counterparty": "Acme",
          "counterparty_type": "customer",   # customer|vendor|partner|other
          "type": "MSA",                     # MSA|order_form|SOW|DPA|NDA|partnership|reseller|other
          "tier": 2,                         # 1-4 (1 = strategic, 4 = self-serve)
          "tcv_usd": 1500000,
          "acv_usd": 500000,
          "effective_date": "2024-01-01",
          "expiration_date": "2026-12-31",
          "auto_renew": true,
          "liability_cap_label": "12mo_fees",  # 12mo_fees|24mo_fees|fixed_amount|uncapped
          "liability_cap_usd": 500000,
          "uncapped_exclusions": ["IP indemnity","confidentiality breach"],
          "governing_law": "Delaware",
          "deviations_from_standard": ["MFN clause","extended audit rights"],
          "renewal_status": "active"          # active|in_negotiation|expiring|expired
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


def days_until(target: date | None, today: date) -> int | None:
    if not target:
        return None
    return (target - today).days


@dataclass
class Bucket:
    count: int = 0
    tcv: float = 0.0
    acv: float = 0.0
    liability_exposure_usd: float = 0.0
    uncapped_count: int = 0


def empty_bucket() -> Bucket:
    return Bucket()


def analyze(state: dict[str, Any], renewal_window_days: int) -> dict[str, Any]:
    as_of_str = state.get("as_of", "")
    today = parse_date(as_of_str) or date.today()
    contracts = state.get("contracts", [])

    total = Bucket()
    by_type: dict[str, Bucket] = defaultdict(empty_bucket)
    by_counterparty_type: dict[str, Bucket] = defaultdict(empty_bucket)
    by_tier: dict[int, Bucket] = defaultdict(empty_bucket)
    by_counterparty: dict[str, Bucket] = defaultdict(empty_bucket)

    deviation_count = 0
    deviation_by_tier: dict[int, int] = defaultdict(int)
    deviation_examples: list[dict[str, Any]] = []

    expiring_soon: list[dict[str, Any]] = []
    auto_renew_no_review: list[dict[str, Any]] = []
    uncapped_or_high_exposure: list[dict[str, Any]] = []

    for c in contracts:
        tier = int(c.get("tier", 4) or 4)
        ctype = c.get("type", "other")
        cp = c.get("counterparty", "")
        cptype = c.get("counterparty_type", "other")
        tcv = float(c.get("tcv_usd", 0) or 0)
        acv = float(c.get("acv_usd", 0) or 0)
        cap_label = c.get("liability_cap_label", "12mo_fees")
        cap_amount = float(c.get("liability_cap_usd", 0) or 0)
        uncapped_excl = c.get("uncapped_exclusions", []) or []
        deviations = c.get("deviations_from_standard", []) or []
        exp_date = parse_date(c.get("expiration_date"))
        auto = bool(c.get("auto_renew", False))
        renewal_status = c.get("renewal_status", "active")

        # Liability exposure approximation
        if cap_label == "uncapped":
            exposure = max(tcv, cap_amount, acv * 5)
        else:
            exposure = cap_amount or acv

        for bucket in (total, by_type[ctype], by_counterparty_type[cptype],
                      by_tier[tier], by_counterparty[cp]):
            bucket.count += 1
            bucket.tcv += tcv
            bucket.acv += acv
            bucket.liability_exposure_usd += exposure
            if cap_label == "uncapped":
                bucket.uncapped_count += 1

        if deviations:
            deviation_count += 1
            deviation_by_tier[tier] += 1
            if len(deviation_examples) < 20:
                deviation_examples.append({
                    "id": c.get("id"),
                    "counterparty": cp,
                    "tier": tier,
                    "deviations": deviations,
                })

        days_left = days_until(exp_date, today)
        if days_left is not None and 0 <= days_left <= renewal_window_days:
            expiring_soon.append({
                "id": c.get("id"),
                "counterparty": cp,
                "type": ctype,
                "tier": tier,
                "expires_in_days": days_left,
                "acv_usd": acv,
                "auto_renew": auto,
                "renewal_status": renewal_status,
            })

        if auto and renewal_status == "active" and days_left is not None and days_left <= 60:
            auto_renew_no_review.append({
                "id": c.get("id"),
                "counterparty": cp,
                "expires_in_days": days_left,
                "acv_usd": acv,
            })

        if cap_label == "uncapped" or exposure > 1_000_000:
            uncapped_or_high_exposure.append({
                "id": c.get("id"),
                "counterparty": cp,
                "cap_label": cap_label,
                "exposure_usd": exposure,
                "uncapped_exclusions": uncapped_excl,
            })

    # Counterparty concentration (top 10)
    cp_concentration = sorted(
        [{"counterparty": k,
          "count": v.count,
          "acv_usd": v.acv,
          "acv_pct": round((v.acv / total.acv) * 100, 1) if total.acv else 0}
         for k, v in by_counterparty.items()],
        key=lambda x: x["acv_usd"], reverse=True,
    )[:10]

    deviation_rate = round((deviation_count / total.count) * 100, 1) if total.count else 0
    expiring_soon.sort(key=lambda x: x["expires_in_days"])

    return {
        "as_of": as_of_str,
        "total": {
            "count": total.count, "tcv_usd": total.tcv, "acv_usd": total.acv,
            "liability_exposure_usd": total.liability_exposure_usd,
            "uncapped_count": total.uncapped_count,
        },
        "by_type": {
            k: {"count": v.count, "tcv_usd": v.tcv, "acv_usd": v.acv,
                "exposure_usd": v.liability_exposure_usd, "uncapped_count": v.uncapped_count}
            for k, v in by_type.items()
        },
        "by_counterparty_type": {
            k: {"count": v.count, "tcv_usd": v.tcv, "acv_usd": v.acv,
                "exposure_usd": v.liability_exposure_usd, "uncapped_count": v.uncapped_count}
            for k, v in by_counterparty_type.items()
        },
        "by_tier": {
            str(k): {"count": v.count, "tcv_usd": v.tcv, "acv_usd": v.acv,
                     "exposure_usd": v.liability_exposure_usd, "uncapped_count": v.uncapped_count}
            for k, v in by_tier.items()
        },
        "deviation_summary": {
            "count": deviation_count,
            "rate_pct": deviation_rate,
            "by_tier": {str(k): v for k, v in deviation_by_tier.items()},
            "examples": deviation_examples,
        },
        "counterparty_concentration_top10": cp_concentration,
        "expiring_within_window": {
            "window_days": renewal_window_days,
            "count": len(expiring_soon),
            "contracts": expiring_soon,
        },
        "auto_renew_at_risk": auto_renew_no_review,
        "high_exposure_or_uncapped": uncapped_or_high_exposure,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Contract Portfolio Analysis")
    lines.append(f"_as of {report['as_of']}_\n")
    t = report["total"]
    lines.append("## Summary")
    lines.append(f"- Total contracts: {t['count']}")
    lines.append(f"- TCV: ${t['tcv_usd']:,.0f}")
    lines.append(f"- ACV: ${t['acv_usd']:,.0f}")
    lines.append(f"- Aggregate liability exposure: ${t['liability_exposure_usd']:,.0f}")
    lines.append(f"- Uncapped contracts: {t['uncapped_count']}")
    lines.append("")

    lines.append("## By tier")
    lines.append("| Tier | Count | ACV | Exposure | Uncapped |")
    lines.append("|------|-------|-----|----------|----------|")
    for tier, v in sorted(report["by_tier"].items()):
        lines.append(
            f"| {tier} | {v['count']} | ${v['acv_usd']:,.0f} | "
            f"${v['exposure_usd']:,.0f} | {v['uncapped_count']} |"
        )
    lines.append("")

    lines.append("## By type")
    lines.append("| Type | Count | ACV |")
    lines.append("|------|-------|-----|")
    for k, v in sorted(report["by_type"].items()):
        lines.append(f"| {k} | {v['count']} | ${v['acv_usd']:,.0f} |")
    lines.append("")

    ds = report["deviation_summary"]
    lines.append("## Deviations")
    lines.append(f"- Contracts with deviations: {ds['count']} ({ds['rate_pct']}%)")
    if ds["by_tier"]:
        lines.append("- By tier: " + ", ".join(f"tier {k}: {v}" for k, v in ds["by_tier"].items()))
    if ds["examples"]:
        lines.append("\n### Examples")
        for e in ds["examples"][:10]:
            lines.append(f"- {e['id']} ({e['counterparty']}, tier {e['tier']}): "
                        f"{', '.join(e['deviations'])}")
    lines.append("")

    lines.append("## Counterparty concentration (top 10 by ACV)")
    lines.append("| Counterparty | Count | ACV | % of total |")
    lines.append("|--------------|-------|-----|-----------|")
    for cp in report["counterparty_concentration_top10"]:
        lines.append(f"| {cp['counterparty']} | {cp['count']} | ${cp['acv_usd']:,.0f} | {cp['acv_pct']}% |")
    lines.append("")

    es = report["expiring_within_window"]
    lines.append(f"## Expiring within {es['window_days']} days ({es['count']} contracts)")
    if es["contracts"]:
        lines.append("| ID | Counterparty | Type | Tier | Expires (d) | ACV | Auto | Status |")
        lines.append("|----|--------------|------|------|-------------|-----|------|--------|")
        for c in es["contracts"][:30]:
            lines.append(
                f"| {c['id']} | {c['counterparty']} | {c['type']} | {c['tier']} | "
                f"{c['expires_in_days']} | ${c['acv_usd']:,.0f} | "
                f"{'yes' if c['auto_renew'] else 'no'} | {c['renewal_status']} |"
            )
    lines.append("")

    if report["auto_renew_at_risk"]:
        lines.append("## Auto-renew at risk (active status, ≤60 days, auto-renew=true)")
        for c in report["auto_renew_at_risk"][:20]:
            lines.append(f"- {c['id']} {c['counterparty']}: in {c['expires_in_days']} days, "
                        f"${c['acv_usd']:,.0f} ACV — trigger review now")
        lines.append("")

    if report["high_exposure_or_uncapped"]:
        lines.append("## High exposure or uncapped")
        for c in report["high_exposure_or_uncapped"][:20]:
            lines.append(f"- {c['id']} {c['counterparty']}: {c['cap_label']}, "
                        f"exposure ${c['exposure_usd']:,.0f}")
        lines.append("")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Analyze contract portfolio for concentration, exposure, renewals",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of contracts")
    p.add_argument("--renewal-window-days", type=int, default=120,
                  help="Days ahead to flag as expiring (default 120)")
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

    report = analyze(state, args.renewal_window_days)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
