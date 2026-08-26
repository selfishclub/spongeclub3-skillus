#!/usr/bin/env python3
"""
partner_tier_economics.py — Model partner tier economics.

Reads a tier definition YAML; emits per-tier: gross margin to us, gross margin
to partner, partner break-even revenue, tier graduation incentive analysis.

Stdlib only. Markdown or JSON output.

Usage:
    python3 partner_tier_economics.py --tiers tiers.yaml
    python3 partner_tier_economics.py --tiers tiers.yaml --partner-cost-pct 0.35 --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


def parse_yaml(text: str) -> dict[str, Any]:
    lines: list[tuple[int, str]] = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        lines.append((indent, line[indent:]))
    result, _ = _parse_block(lines, 0, 0)
    return result if isinstance(result, dict) else {}


def _parse_block(lines, idx, indent):
    if idx >= len(lines):
        return None, idx
    first_indent = lines[idx][0]
    if first_indent < indent:
        return None, idx
    first_line = lines[idx][1]
    if first_line.startswith("- "):
        return _parse_seq(lines, idx, first_indent)
    return _parse_map(lines, idx, first_indent)


def _parse_map(lines, idx, indent):
    out: dict[str, Any] = {}
    while idx < len(lines):
        cur_indent, content = lines[idx]
        if cur_indent < indent:
            break
        if cur_indent > indent:
            idx += 1
            continue
        if ":" not in content:
            idx += 1
            continue
        key, _, rest = content.partition(":")
        key = key.strip().strip('"').strip("'")
        rest = rest.strip()
        if rest:
            out[key] = _scalar(rest)
            idx += 1
        else:
            idx += 1
            if idx < len(lines) and lines[idx][0] > indent:
                value, idx = _parse_block(lines, idx, lines[idx][0])
                out[key] = value if value is not None else {}
            else:
                out[key] = {}
    return out, idx


def _parse_seq(lines, idx, indent):
    out: list[Any] = []
    while idx < len(lines):
        cur_indent, content = lines[idx]
        if cur_indent < indent:
            break
        if not content.startswith("- "):
            break
        rest = content[2:].strip()
        if not rest:
            idx += 1
            if idx < len(lines) and lines[idx][0] > indent:
                value, idx = _parse_block(lines, idx, lines[idx][0])
                out.append(value if value is not None else {})
            else:
                out.append(None)
        elif ":" in rest:
            synth = [(indent + 2, rest)]
            j = idx + 1
            while j < len(lines) and lines[j][0] > indent:
                synth.append(lines[j])
                j += 1
            value, _ = _parse_map(synth, 0, indent + 2)
            out.append(value)
            idx = j
        else:
            out.append(_scalar(rest))
            idx += 1
    return out, idx


def _scalar(s: str):
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1]
    if s.lower() in ("true", "yes"):
        return True
    if s.lower() in ("false", "no"):
        return False
    if s.lower() in ("null", "~", ""):
        return None
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


@dataclass
class TierAnalysis:
    tier_name: str
    threshold_revenue: float
    discount_pct: float
    rebate_pct: float
    total_partner_margin_pct: float
    vendor_margin_pct: float
    partner_gross_margin_per_deal: float
    vendor_gross_margin_per_deal: float
    partner_break_even_deals: float
    graduation_incentive: dict[str, Any]


def analyze_tiers(tiers: list[dict[str, Any]], partner_cost_pct: float, deal_size: float, vendor_cogs_pct: float) -> list[TierAnalysis]:
    analyses: list[TierAnalysis] = []
    sorted_tiers = sorted(tiers, key=lambda t: t.get("threshold_revenue", 0))
    for i, tier in enumerate(sorted_tiers):
        threshold = float(tier.get("threshold_revenue", 0))
        discount = float(tier.get("discount_pct", 0))
        rebate = float(tier.get("rebate_pct", 0))
        total_margin = discount + rebate

        partner_gross = deal_size * total_margin
        partner_cost = deal_size * total_margin * partner_cost_pct  # partner's COGS to fulfill
        partner_net = partner_gross - partner_cost
        partner_be_deals = round(threshold / deal_size, 1) if deal_size else 0

        vendor_revenue_per_deal = deal_size * (1 - total_margin)
        vendor_cogs = vendor_revenue_per_deal * vendor_cogs_pct
        vendor_gross = vendor_revenue_per_deal - vendor_cogs

        # Graduation incentive: marginal benefit of jumping to next tier
        graduation: dict[str, Any] = {}
        if i + 1 < len(sorted_tiers):
            next_tier = sorted_tiers[i + 1]
            next_total_margin = float(next_tier.get("discount_pct", 0)) + float(next_tier.get("rebate_pct", 0))
            margin_increase_pct = next_total_margin - total_margin
            margin_increase_per_deal = deal_size * margin_increase_pct
            graduation = {
                "next_tier": next_tier.get("name", "next"),
                "next_threshold": float(next_tier.get("threshold_revenue", 0)),
                "additional_deals_needed": round((float(next_tier.get("threshold_revenue", 0)) - threshold) / deal_size, 1) if deal_size else 0,
                "additional_margin_per_deal": round(margin_increase_per_deal, 2),
                "marginal_incentive_per_$_revenue": round(margin_increase_pct, 4),
            }

        analyses.append(TierAnalysis(
            tier_name=tier.get("name", f"Tier-{i+1}"),
            threshold_revenue=threshold,
            discount_pct=discount,
            rebate_pct=rebate,
            total_partner_margin_pct=round(total_margin, 4),
            vendor_margin_pct=round(1 - total_margin, 4),
            partner_gross_margin_per_deal=round(partner_net, 2),
            vendor_gross_margin_per_deal=round(vendor_gross, 2),
            partner_break_even_deals=partner_be_deals,
            graduation_incentive=graduation,
        ))
    return analyses


def render_markdown(analyses: list[TierAnalysis], deal_size: float, partner_cost_pct: float, vendor_cogs_pct: float) -> str:
    out = ["# Partner Tier Economics Analysis", ""]
    out.append(f"_Modeled at deal size ${deal_size:,.0f}, partner internal cost {partner_cost_pct*100}% of margin, vendor COGS {vendor_cogs_pct*100}%_")
    out.append("")
    out.append("## Per-Tier Summary")
    out.append("")
    out.append("| Tier | Threshold | Discount % | Rebate % | Total Margin % | Partner Net/Deal | Vendor Net/Deal | BE Deals |")
    out.append("|------|-----------|-----------|---------|----------------|------------------|------------------|----------|")
    for a in analyses:
        out.append(f"| {a.tier_name} | ${a.threshold_revenue:,.0f} | {a.discount_pct*100:.1f}% | {a.rebate_pct*100:.1f}% | {a.total_partner_margin_pct*100:.1f}% | ${a.partner_gross_margin_per_deal:,.0f} | ${a.vendor_gross_margin_per_deal:,.0f} | {a.partner_break_even_deals} |")
    out.append("")
    out.append("## Graduation Incentives")
    out.append("")
    for a in analyses:
        if a.graduation_incentive:
            g = a.graduation_incentive
            out.append(f"### {a.tier_name} → {g['next_tier']}")
            out.append(f"- Additional revenue needed: ${g['next_threshold'] - a.threshold_revenue:,.0f}")
            out.append(f"- Additional deals: {g['additional_deals_needed']}")
            out.append(f"- Additional margin per deal: ${g['additional_margin_per_deal']:,.2f}")
            out.append(f"- Marginal incentive: {g['marginal_incentive_per_$_revenue']*100:.2f}% of every $ revenue")
            out.append("")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Model partner tier economics from tier definitions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--tiers", required=True, help="Tier definitions YAML")
    p.add_argument("--deal-size", type=float, default=50000, help="Typical deal size (default: $50k)")
    p.add_argument("--partner-cost-pct", type=float, default=0.40,
                   help="Partner's internal cost as %% of their margin (default: 40%%)")
    p.add_argument("--vendor-cogs-pct", type=float, default=0.15,
                   help="Vendor COGS as %% of vendor revenue (default: 15%%)")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", help="Output file path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        doc = parse_yaml(Path(args.tiers).read_text())
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    tiers = doc.get("tiers", []) or []
    if not tiers:
        print("error: no tiers found in input (expected 'tiers:' list)", file=sys.stderr)
        return 2
    analyses = analyze_tiers(tiers, args.partner_cost_pct, args.deal_size, args.vendor_cogs_pct)
    if args.format == "json":
        out = json.dumps(
            {
                "deal_size": args.deal_size,
                "partner_cost_pct": args.partner_cost_pct,
                "vendor_cogs_pct": args.vendor_cogs_pct,
                "tiers": [asdict(a) for a in analyses],
            },
            indent=2,
        )
    else:
        out = render_markdown(analyses, args.deal_size, args.partner_cost_pct, args.vendor_cogs_pct)
    if args.output:
        Path(args.output).write_text(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
