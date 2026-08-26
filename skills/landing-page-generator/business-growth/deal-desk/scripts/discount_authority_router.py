#!/usr/bin/env python3
"""
discount_authority_router.py — Determine required approvers and routing for a deal.

Reads a deal spec YAML + optional approval matrix YAML; emits the required
approver(s), routing order (serial vs parallel), and SLA-aware schedule.

Stdlib only. Markdown or JSON output.

Usage:
    python3 discount_authority_router.py --deal deal.yaml
    python3 discount_authority_router.py --deal deal.yaml --matrix matrix.yaml --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any


# Reuse minimal YAML parser
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
class ApprovalRoute:
    approvers_financial: list[str]
    approvers_legal: list[str]
    approvers_operational: list[str]
    routing_mode: str   # serial / parallel / hybrid
    sla_business_days: float
    rationale: list[str]


# Default approval matrix (overridable via --matrix file)
DEFAULT_MATRIX = {
    "discount_tiers": [
        (50, "CEO"),
        (40, "CRO"),
        (30, "VP Sales"),
        (20, "Director"),
        (10, "Sales Manager"),
        (0, None),
    ],
    "acv_tiers": [
        (5_000_000, "CEO"),
        (1_000_000, "VP Sales"),
        (250_000, "Director"),
        (100_000, "Sales Manager"),
        (0, None),
    ],
    "contract_length_tiers": [
        (37, "VP Sales"),
        (25, "Director"),
        (13, "Sales Manager"),
        (0, None),
    ],
    "payment_terms_thresholds": {
        "Net 0": None,
        "Net 30": None,
        "Net 45": "Director",
        "Net 60": "Sales Manager",
        "Net 90": "CFO",
        "Custom": "CFO",
    },
    "ranking": ["Sales Manager", "Director", "VP Sales", "CRO", "CFO", "CEO"],
}


def route(deal: dict[str, Any], matrix: dict[str, Any]) -> ApprovalRoute:
    financial: list[str] = []
    legal: list[str] = []
    operational: list[str] = []
    rationale: list[str] = []

    discount = float(deal.get("discount_pct", 0))
    acv = float(deal.get("requested_acv", 0))
    contract_months = int(deal.get("contract_length_months", 12))
    payment_terms = str(deal.get("payment_terms", "Net 30"))

    # Discount tier
    for threshold, approver in matrix.get("discount_tiers", DEFAULT_MATRIX["discount_tiers"]):
        if discount > threshold and approver:
            financial.append(approver)
            rationale.append(f"Discount {discount}% > {threshold}% → {approver}")
            break

    # ACV tier
    for threshold, approver in matrix.get("acv_tiers", DEFAULT_MATRIX["acv_tiers"]):
        if acv > threshold and approver:
            if approver not in financial:
                financial.append(approver)
                rationale.append(f"ACV ${acv:,.0f} > ${threshold:,.0f} → {approver}")
            break

    # Contract length
    for threshold, approver in matrix.get("contract_length_tiers", DEFAULT_MATRIX["contract_length_tiers"]):
        if contract_months >= threshold and approver:
            if approver not in financial:
                financial.append(approver)
                rationale.append(f"Contract length {contract_months}mo → {approver}")
            break

    # Payment terms
    pt_map = matrix.get("payment_terms_thresholds", DEFAULT_MATRIX["payment_terms_thresholds"])
    pt_approver = pt_map.get(payment_terms)
    if pt_approver and pt_approver not in financial:
        financial.append(pt_approver)
        rationale.append(f"Payment terms {payment_terms} → {pt_approver}")

    # Legal
    if deal.get("custom_legal_terms"):
        legal.append("General Counsel")
        rationale.append("Custom legal terms → General Counsel")
    if deal.get("mfn_requested"):
        legal.append("General Counsel")
        if "CFO" not in financial:
            financial.append("CFO")
        rationale.append("MFN requested → CFO + General Counsel")
    if deal.get("liability_cap_multiplier", 1) > 1:
        legal.append("General Counsel")
        if "CFO" not in financial:
            financial.append("CFO")
        rationale.append(f"Liability cap {deal.get('liability_cap_multiplier')}x → CFO + General Counsel")

    # Operational
    if deal.get("custom_sla"):
        operational.append("VP Customer Success")
        operational.append("VP Engineering")
        rationale.append("Custom SLA → CS + Engineering concurrence")
    if deal.get("custom_security_commitments"):
        operational.append("CISO")
        rationale.append("Custom security commitments → CISO concurrence")
    if deal.get("custom_integration_required"):
        operational.append("VP Engineering")
        rationale.append("Custom integration → Engineering concurrence")

    # Dedupe (preserve order)
    seen = set()
    financial = [x for x in financial if not (x in seen or seen.add(x))]
    seen = set()
    legal = [x for x in legal if not (x in seen or seen.add(x))]
    seen = set()
    operational = [x for x in operational if not (x in seen or seen.add(x))]

    # Routing mode
    has_cross_functional = bool(legal) or bool(operational)
    routing_mode = "hybrid" if has_cross_functional else "serial"

    # Highest approver in financial chain determines base SLA
    ranking = matrix.get("ranking", DEFAULT_MATRIX["ranking"])
    highest_rank = -1
    for a in financial:
        try:
            highest_rank = max(highest_rank, ranking.index(a))
        except ValueError:
            pass
    if "CEO" in financial:
        sla = 5.0
    elif "CFO" in financial or "CRO" in financial:
        sla = 2.0
    elif highest_rank >= 0:
        sla = 1.0
    else:
        sla = 0.5  # rep authority

    if not financial and not legal and not operational:
        rationale.append("No approvers required — deal within standard rep authority")

    return ApprovalRoute(
        approvers_financial=financial,
        approvers_legal=legal,
        approvers_operational=operational,
        routing_mode=routing_mode,
        sla_business_days=sla,
        rationale=rationale,
    )


def render_markdown(route_obj: ApprovalRoute, deal: dict[str, Any]) -> str:
    out: list[str] = []
    out.append("# Approval Routing")
    out.append("")
    out.append(f"**Deal**: {deal.get('deal_id', 'unknown')} | Customer: {deal.get('customer', {}).get('name', '')}")
    out.append("")
    out.append("## Required Approvers")
    out.append("")
    if route_obj.approvers_financial:
        out.append("**Financial (sequential per ranking):**")
        for i, a in enumerate(route_obj.approvers_financial, 1):
            out.append(f"  {i}. {a}")
        out.append("")
    if route_obj.approvers_legal:
        out.append("**Legal (parallel):**")
        for a in route_obj.approvers_legal:
            out.append(f"  - {a}")
        out.append("")
    if route_obj.approvers_operational:
        out.append("**Operational concurrence (parallel):**")
        for a in route_obj.approvers_operational:
            out.append(f"  - {a}")
        out.append("")
    out.append(f"**Routing mode**: {route_obj.routing_mode}")
    out.append(f"**Target SLA**: {route_obj.sla_business_days} business days")
    out.append("")
    out.append("## Rationale")
    out.append("")
    for r in route_obj.rationale:
        out.append(f"- {r}")
    out.append("")
    if route_obj.routing_mode == "hybrid":
        out.append("## Routing instructions")
        out.append("")
        out.append("1. Submit packet to legal + operational approvers in parallel (concurrence required)")
        out.append("2. Once concurrences in, route to financial approvers in sequential order (lowest → highest)")
        out.append("3. Final approval = signed by highest financial approver after all concurrences")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Determine required approvers for a deal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--deal", required=True, help="Path to deal spec YAML")
    p.add_argument("--matrix", help="Optional approval matrix YAML (uses default if omitted)")
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
    matrix = DEFAULT_MATRIX
    if args.matrix:
        try:
            matrix = parse_yaml(Path(args.matrix).read_text())
        except OSError as e:
            print(f"error loading matrix: {e}", file=sys.stderr)
            return 2
    r = route(deal, matrix)
    if args.format == "json":
        out = json.dumps(asdict(r), indent=2, default=str)
    else:
        out = render_markdown(r, deal)
    if args.output:
        Path(args.output).write_text(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
