#!/usr/bin/env python3
"""
channel_margin_calculator.py — Compute per-channel net contribution margin.

Reads a deal spec YAML + channel type; emits cost-line breakdown and compares
across channels (direct / reseller / vAR / marketplace / OEM / MSP).

Stdlib only. Markdown or JSON output.

Usage:
    python3 channel_margin_calculator.py --deal deal.yaml --channel reseller
    python3 channel_margin_calculator.py --deal deal.yaml --channel all  # compare all channels
    python3 channel_margin_calculator.py --deal deal.yaml --channel marketplace --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any


# Default channel cost model (overridable in deal YAML)
CHANNEL_DEFAULTS = {
    "direct": {
        "partner_margin_pct": 0,
        "sales_cost_pct": 0.25,
        "marketing_cost_pct": 0.10,
        "csm_cost_pct": 0.05,
        "enablement_cost_pct": 0,
        "channel_ops_pct": 0,
        "support_cost_pct": 0.03,
    },
    "reseller": {
        "partner_margin_pct": 0.25,
        "sales_cost_pct": 0.05,
        "marketing_cost_pct": 0.05,
        "csm_cost_pct": 0.02,
        "enablement_cost_pct": 0.025,
        "channel_ops_pct": 0.015,
        "support_cost_pct": 0.015,
    },
    "var": {
        "partner_margin_pct": 0.35,
        "sales_cost_pct": 0.05,
        "marketing_cost_pct": 0.05,
        "csm_cost_pct": 0.015,
        "enablement_cost_pct": 0.025,
        "channel_ops_pct": 0.015,
        "support_cost_pct": 0.015,
    },
    "marketplace": {
        "partner_margin_pct": 0.03,
        "sales_cost_pct": 0.08,
        "marketing_cost_pct": 0.05,
        "csm_cost_pct": 0.03,
        "enablement_cost_pct": 0.015,
        "channel_ops_pct": 0.01,
        "support_cost_pct": 0.02,
    },
    "oem": {
        "partner_margin_pct": 0.45,
        "sales_cost_pct": 0.05,
        "marketing_cost_pct": 0.01,
        "csm_cost_pct": 0.005,
        "enablement_cost_pct": 0.05,
        "channel_ops_pct": 0.03,
        "support_cost_pct": 0.05,
    },
    "msp": {
        "partner_margin_pct": 0.35,
        "sales_cost_pct": 0.05,
        "marketing_cost_pct": 0.04,
        "csm_cost_pct": 0.015,
        "enablement_cost_pct": 0.03,
        "channel_ops_pct": 0.02,
        "support_cost_pct": 0.04,
    },
}

DEFAULT_COGS_PCT = 0.15


# Minimal YAML parser
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
class ChannelMargin:
    channel: str
    customer_payment: float
    partner_margin: float
    revenue_to_us: float
    cogs: float
    sales_cost: float
    marketing_cost: float
    csm_cost: float
    enablement_cost: float
    channel_ops_cost: float
    support_cost: float
    net_contribution: float
    net_contribution_pct: float


def compute(deal: dict[str, Any], channel: str) -> ChannelMargin:
    if channel not in CHANNEL_DEFAULTS:
        raise ValueError(f"Unknown channel: {channel}. Available: {list(CHANNEL_DEFAULTS.keys())}")
    cust_payment = float(deal.get("customer_payment", deal.get("acv", 0)))
    cogs_pct = float(deal.get("cogs_pct", DEFAULT_COGS_PCT))
    overrides = deal.get("channel_overrides", {}) or {}
    cfg = {**CHANNEL_DEFAULTS[channel], **(overrides.get(channel, {}) or {})}

    partner_margin = cust_payment * cfg["partner_margin_pct"]
    revenue_to_us = cust_payment - partner_margin
    cogs = revenue_to_us * cogs_pct
    sales = cust_payment * cfg["sales_cost_pct"]
    marketing = cust_payment * cfg["marketing_cost_pct"]
    csm = cust_payment * cfg["csm_cost_pct"]
    enable = cust_payment * cfg["enablement_cost_pct"]
    ops = cust_payment * cfg["channel_ops_pct"]
    support = cust_payment * cfg["support_cost_pct"]
    net = revenue_to_us - cogs - sales - marketing - csm - enable - ops - support
    net_pct = round(100 * net / cust_payment, 1) if cust_payment else 0

    return ChannelMargin(
        channel=channel,
        customer_payment=round(cust_payment, 2),
        partner_margin=round(partner_margin, 2),
        revenue_to_us=round(revenue_to_us, 2),
        cogs=round(cogs, 2),
        sales_cost=round(sales, 2),
        marketing_cost=round(marketing, 2),
        csm_cost=round(csm, 2),
        enablement_cost=round(enable, 2),
        channel_ops_cost=round(ops, 2),
        support_cost=round(support, 2),
        net_contribution=round(net, 2),
        net_contribution_pct=net_pct,
    )


def render_markdown(margins: list[ChannelMargin], deal: dict[str, Any]) -> str:
    out: list[str] = []
    out.append("# Channel Margin Comparison")
    out.append("")
    out.append(f"**Deal**: {deal.get('deal_id', '<n/a>')} | Customer payment: ${float(deal.get('customer_payment', deal.get('acv', 0))):,.0f}")
    out.append("")
    if len(margins) == 1:
        m = margins[0]
        out.append(f"## {m.channel.upper()}")
        out.append("")
        out.append("| Line | Amount |")
        out.append("|------|--------|")
        out.append(f"| Customer payment | ${m.customer_payment:,.0f} |")
        out.append(f"| Partner margin / fee | -${m.partner_margin:,.0f} |")
        out.append(f"| **Revenue to us** | **${m.revenue_to_us:,.0f}** |")
        out.append(f"| COGS | -${m.cogs:,.0f} |")
        out.append(f"| Sales cost | -${m.sales_cost:,.0f} |")
        out.append(f"| Marketing cost | -${m.marketing_cost:,.0f} |")
        out.append(f"| CSM cost | -${m.csm_cost:,.0f} |")
        out.append(f"| Enablement (amortized) | -${m.enablement_cost:,.0f} |")
        out.append(f"| Channel ops (amortized) | -${m.channel_ops_cost:,.0f} |")
        out.append(f"| Support cost | -${m.support_cost:,.0f} |")
        out.append(f"| **Net contribution** | **${m.net_contribution:,.0f} ({m.net_contribution_pct}%)** |")
    else:
        out.append("| Line | " + " | ".join(m.channel.upper() for m in margins) + " |")
        out.append("|------|" + "|".join("-------" for _ in margins) + "|")
        for label, attr in [
            ("Customer payment", "customer_payment"),
            ("Partner margin", "partner_margin"),
            ("Revenue to us", "revenue_to_us"),
            ("COGS", "cogs"),
            ("Sales cost", "sales_cost"),
            ("Marketing cost", "marketing_cost"),
            ("CSM cost", "csm_cost"),
            ("Enablement", "enablement_cost"),
            ("Channel ops", "channel_ops_cost"),
            ("Support cost", "support_cost"),
            ("**Net contribution**", "net_contribution"),
        ]:
            row = f"| {label} | "
            for m in margins:
                v = getattr(m, attr)
                row += f"${v:,.0f} | "
            out.append(row.rstrip(" "))
        out.append("| **Net contribution %** | " + " | ".join(f"**{m.net_contribution_pct}%**" for m in margins) + " |")
        best = max(margins, key=lambda m: m.net_contribution)
        out.append("")
        out.append(f"**Best per-deal contribution**: `{best.channel}` at ${best.net_contribution:,.0f} ({best.net_contribution_pct}%)")
        out.append("")
        out.append("> Note: per-deal margin is only one factor. Channel volume potential matters too — high per-deal margin × low volume can underperform low per-deal × high volume.")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Compute per-channel net contribution margin",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--deal", required=True, help="Deal spec YAML")
    p.add_argument("--channel", required=True,
                   help="Channel: direct / reseller / var / marketplace / oem / msp / all")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", help="Output file path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        deal = parse_yaml(Path(args.deal).read_text())
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if args.channel == "all":
        channels = list(CHANNEL_DEFAULTS.keys())
    else:
        channels = [args.channel]
    margins: list[ChannelMargin] = []
    for c in channels:
        try:
            margins.append(compute(deal, c))
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
    if args.format == "json":
        out = json.dumps({"deal_id": deal.get("deal_id", ""), "margins": [asdict(m) for m in margins]}, indent=2)
    else:
        out = render_markdown(margins, deal)
    if args.output:
        Path(args.output).write_text(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
