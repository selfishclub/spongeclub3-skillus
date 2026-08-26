#!/usr/bin/env python3
"""
partnership_roi_modeler.py — Model 3-year partnership ROI.

Reads a partnership spec YAML; emits 3-year P&L, payback period, sensitivity analysis.

Stdlib only. Markdown or JSON output.

Usage:
    python3 partnership_roi_modeler.py --partnership partnership.yaml
    python3 partnership_roi_modeler.py --partnership partnership.yaml --format json
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
class YearP_L:
    year: int
    revenue: float
    costs: dict[str, float]
    total_cost: float
    net: float
    cumulative_net: float


@dataclass
class ROIAnalysis:
    partnership_name: str
    year1: YearP_L
    year2: YearP_L
    year3: YearP_L
    cumulative_3yr_net: float
    payback_year: int | None
    payback_message: str
    sensitivity: dict[str, dict[str, float]]


def compute_year(
    year: int,
    revenue: float,
    cost_components: dict[str, float],
    cumulative_prior: float,
) -> YearP_L:
    total = sum(cost_components.values())
    net = revenue - total
    return YearP_L(
        year=year,
        revenue=round(revenue, 2),
        costs={k: round(v, 2) for k, v in cost_components.items()},
        total_cost=round(total, 2),
        net=round(net, 2),
        cumulative_net=round(cumulative_prior + net, 2),
    )


def model(spec: dict[str, Any]) -> ROIAnalysis:
    name = spec.get("partnership_name", "unknown")

    rev_y1 = float(spec.get("revenue_year1", 0))
    rev_y2 = float(spec.get("revenue_year2", 0))
    rev_y3 = float(spec.get("revenue_year3", 0))

    costs = spec.get("costs", {}) or {}
    base_costs_y1 = {
        "partnership_manager_headcount": float(costs.get("pm_headcount_y1", 200000)),
        "engineering_integration_onetime": float(costs.get("eng_integration_y1", 300000)),
        "marketing_co_launch": float(costs.get("marketing_y1", 50000)),
        "partner_enablement": float(costs.get("enablement_y1", 50000)),
        "travel_events": float(costs.get("travel_events_y1", 30000)),
        "exec_time_allocation": float(costs.get("exec_time_y1", 50000)),
    }
    costs_y2 = {
        "partnership_manager_headcount": float(costs.get("pm_headcount_y2", 200000)),
        "engineering_ongoing": float(costs.get("eng_ongoing_y2", 100000)),
        "marketing": float(costs.get("marketing_y2", 80000)),
        "partner_enablement": float(costs.get("enablement_y2", 30000)),
        "travel_events": float(costs.get("travel_events_y2", 40000)),
        "exec_time_allocation": float(costs.get("exec_time_y2", 30000)),
    }
    costs_y3 = {
        "partnership_manager_headcount": float(costs.get("pm_headcount_y3", 200000)),
        "engineering_ongoing": float(costs.get("eng_ongoing_y3", 80000)),
        "marketing": float(costs.get("marketing_y3", 70000)),
        "partner_enablement": float(costs.get("enablement_y3", 25000)),
        "travel_events": float(costs.get("travel_events_y3", 40000)),
        "exec_time_allocation": float(costs.get("exec_time_y3", 25000)),
    }

    y1 = compute_year(1, rev_y1, base_costs_y1, 0)
    y2 = compute_year(2, rev_y2, costs_y2, y1.cumulative_net)
    y3 = compute_year(3, rev_y3, costs_y3, y2.cumulative_net)

    payback_year = None
    payback_message = ""
    if y1.cumulative_net >= 0:
        payback_year = 1
        payback_message = "Payback in year 1"
    elif y2.cumulative_net >= 0:
        payback_year = 2
        payback_message = "Payback in year 2"
    elif y3.cumulative_net >= 0:
        payback_year = 3
        payback_message = "Payback in year 3"
    else:
        payback_message = f"No payback within 3 years; cumulative deficit ${y3.cumulative_net:,.0f}"

    # Sensitivity: what if revenue is 50% / 75% / 125% / 150%?
    sensitivity: dict[str, dict[str, float]] = {}
    for mult in (0.5, 0.75, 1.0, 1.25, 1.5):
        rev1 = rev_y1 * mult
        rev2 = rev_y2 * mult
        rev3 = rev_y3 * mult
        s_y1 = compute_year(1, rev1, base_costs_y1, 0)
        s_y2 = compute_year(2, rev2, costs_y2, s_y1.cumulative_net)
        s_y3 = compute_year(3, rev3, costs_y3, s_y2.cumulative_net)
        sensitivity[f"{int(mult*100)}%_revenue"] = {
            "3yr_cumulative_net": round(s_y3.cumulative_net, 2),
            "payback_year": (
                1 if s_y1.cumulative_net >= 0
                else (2 if s_y2.cumulative_net >= 0
                      else (3 if s_y3.cumulative_net >= 0 else 0))
            ),
        }

    return ROIAnalysis(
        partnership_name=name,
        year1=y1, year2=y2, year3=y3,
        cumulative_3yr_net=y3.cumulative_net,
        payback_year=payback_year,
        payback_message=payback_message,
        sensitivity=sensitivity,
    )


def render_markdown(a: ROIAnalysis) -> str:
    out = [f"# Partnership ROI: {a.partnership_name}", ""]
    out.append("## 3-Year P&L")
    out.append("")
    out.append("| Year | Revenue | Total Cost | Net | Cumulative Net |")
    out.append("|------|---------|-----------|-----|----------------|")
    for y in (a.year1, a.year2, a.year3):
        out.append(f"| Year {y.year} | ${y.revenue:,.0f} | ${y.total_cost:,.0f} | ${y.net:,.0f} | ${y.cumulative_net:,.0f} |")
    out.append("")
    out.append("## Cost Breakdown")
    out.append("")
    for y in (a.year1, a.year2, a.year3):
        out.append(f"### Year {y.year}")
        out.append("")
        for k, v in y.costs.items():
            out.append(f"- {k}: ${v:,.0f}")
        out.append(f"- **Total: ${y.total_cost:,.0f}**")
        out.append("")
    out.append("## Payback")
    out.append("")
    out.append(f"- **3-year cumulative net**: ${a.cumulative_3yr_net:,.0f}")
    out.append(f"- **Payback**: {a.payback_message}")
    out.append("")
    out.append("## Sensitivity Analysis")
    out.append("")
    out.append("| Scenario | 3yr Cumulative Net | Payback Year |")
    out.append("|----------|---------------------|--------------|")
    for scen, vals in a.sensitivity.items():
        py = vals['payback_year']
        py_display = f"Year {py}" if py else "Beyond 3yr"
        out.append(f"| {scen} | ${vals['3yr_cumulative_net']:,.0f} | {py_display} |")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Model partnership ROI over 3 years",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--partnership", required=True, help="Partnership spec YAML")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", help="Output file path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        spec = parse_yaml(Path(args.partnership).read_text())
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    analysis = model(spec)
    if args.format == "json":
        out = json.dumps(asdict(analysis), indent=2)
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
