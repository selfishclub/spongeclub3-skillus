#!/usr/bin/env python3
"""
deal_review_packet.py — Generate a deal-review packet from a deal spec.

Reads a YAML deal spec; emits a markdown packet covering: summary, standard vs
requested, justification, financial impact, strategic value, risk, required
approvers, recommendation template, and conditions.

Stdlib only. Markdown or JSON output.

Usage:
    python3 deal_review_packet.py --deal deal.yaml
    python3 deal_review_packet.py --deal deal.yaml --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
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
class Packet:
    deal_id: str
    customer: dict[str, Any]
    summary: dict[str, Any]
    standard_vs_requested: list[dict[str, Any]]
    justification: dict[str, Any]
    financial_impact: dict[str, Any]
    strategic_value: dict[str, Any]
    risk: dict[str, Any]
    approvers_needed: list[str]
    recommendation: dict[str, Any]
    conditions: list[str]
    metadata: dict[str, str] = field(default_factory=dict)


def compute_approvers_needed(deal: dict[str, Any]) -> list[str]:
    """Heuristic approver routing — same logic as discount_authority_router for self-contained packet."""
    approvers: list[str] = []
    discount = deal.get("discount_pct", 0)
    acv = deal.get("requested_acv", 0)
    contract_months = deal.get("contract_length_months", 12)
    payment_terms = deal.get("payment_terms", "Net 30").lower()
    custom_legal = deal.get("custom_legal_terms")
    custom_sla = deal.get("custom_sla")
    mfn = deal.get("mfn_requested")

    # Discount tier
    if discount > 50:
        approvers.append("CEO")
    elif discount > 40:
        approvers.append("CRO")
    elif discount > 30:
        approvers.append("VP Sales")
    elif discount > 20:
        approvers.append("Director")
    elif discount > 10:
        approvers.append("Sales Manager")

    # ACV tier
    if acv > 5_000_000:
        if "CEO" not in approvers: approvers.append("CEO")
    elif acv > 1_000_000:
        if "VP Sales" not in approvers and "CRO" not in approvers and "CEO" not in approvers:
            approvers.append("VP Sales")
    elif acv > 250_000:
        if not any(r in approvers for r in ("Director", "VP Sales", "CRO", "CEO")):
            approvers.append("Director")

    # Contract length
    if contract_months > 36:
        if "VP Sales" not in approvers and "CRO" not in approvers and "CEO" not in approvers:
            approvers.append("VP Sales")

    # Payment terms
    if "60" in payment_terms or "90" in payment_terms or "custom" in payment_terms:
        approvers.append("CFO")

    # Legal
    if custom_legal:
        approvers.append("General Counsel")
    if mfn:
        if "CFO" not in approvers:
            approvers.append("CFO")
        if "General Counsel" not in approvers:
            approvers.append("General Counsel")

    # SLA
    if custom_sla:
        approvers.append("VP Customer Success")
        approvers.append("VP Engineering")

    return approvers


def build_packet(deal: dict[str, Any]) -> Packet:
    customer = deal.get("customer", {}) or {}
    std_acv = deal.get("standard_acv", 0)
    req_acv = deal.get("requested_acv", 0)
    discount_pct = round(((std_acv - req_acv) / std_acv) * 100, 1) if std_acv else 0

    return Packet(
        deal_id=deal.get("deal_id", "unknown"),
        customer={
            "name": customer.get("name", "Unknown"),
            "industry": customer.get("industry", ""),
            "size_employees": customer.get("size_employees", 0),
            "region": customer.get("region", ""),
        },
        summary={
            "requested_acv": req_acv,
            "standard_acv": std_acv,
            "discount_pct": discount_pct,
            "contract_length_months": deal.get("contract_length_months", 12),
            "payment_terms": deal.get("payment_terms", "Net 30"),
            "close_by_date": deal.get("close_by_date", ""),
        },
        standard_vs_requested=[
            {"item": "ACV", "standard": f"${std_acv:,.0f}", "requested": f"${req_acv:,.0f}",
             "delta": f"-{discount_pct}%"},
            {"item": "Contract length", "standard": "12 months",
             "requested": f"{deal.get('contract_length_months', 12)} months",
             "delta": f"+{deal.get('contract_length_months', 12) - 12} months"},
            {"item": "Payment terms", "standard": "Net 30",
             "requested": deal.get("payment_terms", "Net 30"), "delta": ""},
            {"item": "SLA", "standard": "Standard 99.5%",
             "requested": deal.get("custom_sla", "Standard 99.5%"), "delta": ""},
            {"item": "Custom legal", "standard": "Standard MSA",
             "requested": deal.get("custom_legal_terms", "Standard MSA"), "delta": ""},
        ],
        justification={
            "customer_reason": deal.get("justification", {}).get("customer_reason", ""),
            "our_reason": deal.get("justification", {}).get("our_reason", ""),
            "alternatives_customer_has": deal.get("justification", {}).get("alternatives", ""),
        },
        financial_impact={
            "standard_arr": std_acv,
            "discounted_arr": req_acv,
            "absolute_discount": std_acv - req_acv,
            "gross_margin_estimate": req_acv * deal.get("gross_margin_pct", 0.75),
            "estimated_ltv": req_acv * deal.get("expected_renewal_years", 3),
            "discount_payback_years": (
                round((std_acv - req_acv) / (req_acv * deal.get("gross_margin_pct", 0.75)), 2)
                if req_acv and deal.get("gross_margin_pct", 0.75) > 0 else None
            ),
        },
        strategic_value={
            "logo_value": deal.get("strategic", {}).get("logo_value", "low"),
            "reference_value": deal.get("strategic", {}).get("reference_value", "low"),
            "vertical_foothold": deal.get("strategic", {}).get("vertical_foothold", ""),
            "competitive_replacement": deal.get("strategic", {}).get("competitive_replacement", ""),
        },
        risk={
            "credit_risk": deal.get("risk", {}).get("credit_risk", "unknown"),
            "compliance_risk": deal.get("risk", {}).get("compliance_risk", "low"),
            "technical_fit_risk": deal.get("risk", {}).get("technical_fit_risk", "low"),
            "concession_follow_through": deal.get("risk", {}).get("concession_follow_through", "unknown"),
        },
        approvers_needed=compute_approvers_needed(deal),
        recommendation={
            "deal_desk_recommendation": "<approve | counter | decline>",
            "rationale": "<reasoning — fill in before submitting>",
            "counter_terms": "<if counter — what would we accept?>",
            "alternatives": "<if decline — what else can we offer customer?>",
        },
        conditions=[
            f"Discount expires {deal.get('close_by_date', '<date>')}",
            "Customer agrees this is a single-instance arrangement (not precedent)",
            f"Payment must close by {deal.get('close_by_date', '<date>')}",
            "Customer commitments (case study, reference, etc.) per signed terms",
        ],
        metadata={
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
    )


def render_markdown(p: Packet) -> str:
    out: list[str] = []
    out.append(f"# Deal Review: {p.customer['name']}")
    out.append("")
    out.append(f"_Deal ID: `{p.deal_id}` | Generated: {p.metadata['generated_at']}_")
    out.append("")
    out.append("## Summary")
    out.append("")
    s = p.summary
    out.append(f"- **Customer**: {p.customer['name']} | {p.customer['industry']} | {p.customer['size_employees']} employees | {p.customer['region']}")
    out.append(f"- **Requested ACV**: ${s['requested_acv']:,.0f} (standard ${s['standard_acv']:,.0f}, -{s['discount_pct']}%)")
    out.append(f"- **Contract**: {s['contract_length_months']} months, {s['payment_terms']}")
    out.append(f"- **Decision needed by**: {s['close_by_date']}")
    out.append("")
    out.append("## Standard vs Requested")
    out.append("")
    out.append("| Item | Standard | Requested | Delta |")
    out.append("|------|----------|-----------|-------|")
    for row in p.standard_vs_requested:
        out.append(f"| {row['item']} | {row['standard']} | {row['requested']} | {row['delta']} |")
    out.append("")
    out.append("## Justification")
    out.append("")
    out.append(f"- **Customer reason**: {p.justification['customer_reason']}")
    out.append(f"- **Our strategic reason**: {p.justification['our_reason']}")
    out.append(f"- **Customer alternatives**: {p.justification['alternatives_customer_has']}")
    out.append("")
    out.append("## Financial Impact")
    out.append("")
    fi = p.financial_impact
    out.append(f"- **Standard ARR**: ${fi['standard_arr']:,.0f}")
    out.append(f"- **Discounted ARR**: ${fi['discounted_arr']:,.0f}")
    out.append(f"- **Absolute discount**: ${fi['absolute_discount']:,.0f}")
    out.append(f"- **Est. gross margin**: ${fi['gross_margin_estimate']:,.0f}")
    out.append(f"- **Est. LTV**: ${fi['estimated_ltv']:,.0f}")
    if fi['discount_payback_years']:
        out.append(f"- **Discount payback**: {fi['discount_payback_years']} years")
    out.append("")
    out.append("## Strategic Value")
    out.append("")
    sv = p.strategic_value
    out.append(f"- **Logo value**: {sv['logo_value']}")
    out.append(f"- **Reference value**: {sv['reference_value']}")
    out.append(f"- **Vertical foothold**: {sv['vertical_foothold']}")
    out.append(f"- **Competitive replacement**: {sv['competitive_replacement']}")
    out.append("")
    out.append("## Risk")
    out.append("")
    r = p.risk
    out.append(f"- **Credit risk**: {r['credit_risk']}")
    out.append(f"- **Compliance risk**: {r['compliance_risk']}")
    out.append(f"- **Technical fit risk**: {r['technical_fit_risk']}")
    out.append(f"- **Concession follow-through risk**: {r['concession_follow_through']}")
    out.append("")
    out.append("## Required Approvers")
    out.append("")
    if p.approvers_needed:
        for a in p.approvers_needed:
            out.append(f"- [ ] {a}")
    else:
        out.append("- No additional approvers required beyond rep authority")
    out.append("")
    out.append("## Deal Desk Recommendation")
    out.append("")
    rec = p.recommendation
    out.append(f"**Decision**: {rec['deal_desk_recommendation']}")
    out.append("")
    out.append(f"**Rationale**: {rec['rationale']}")
    out.append("")
    out.append(f"**Counter terms** (if applicable): {rec['counter_terms']}")
    out.append("")
    out.append(f"**Alternatives** (if declining): {rec['alternatives']}")
    out.append("")
    out.append("## Conditions if Approved")
    out.append("")
    for c in p.conditions:
        out.append(f"- {c}")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate a deal-review packet from a deal spec YAML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--deal", required=True, help="Path to deal spec YAML")
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
    packet = build_packet(deal)
    if args.format == "json":
        out = json.dumps(asdict(packet), indent=2, default=str)
    else:
        out = render_markdown(packet)
    if args.output:
        Path(args.output).write_text(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
