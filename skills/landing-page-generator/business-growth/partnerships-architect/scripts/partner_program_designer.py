#!/usr/bin/env python3
"""
partner_program_designer.py — Generate a baseline partner program design.

Reads an org spec YAML (company stage, ICP, target partner volume); emits
recommended program structure: tiers, benefits, requirements, channel manager
headcount, enablement plan, maturity model.

Stdlib only. Markdown or JSON output.

Usage:
    python3 partner_program_designer.py --org-spec org.yaml
    python3 partner_program_designer.py --org-spec org.yaml --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any


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
class Tier:
    name: str
    revenue_threshold: float
    discount_pct: float
    rebate_pct: float
    certifications_required: int
    customers_required: int
    mdf_pct_of_revenue: float
    cm_engagement: str
    benefits: list[str]


@dataclass
class ProgramDesign:
    org_name: str
    stage: str
    recommended_partner_types: list[str]
    target_active_partners: int
    tiers: list[Tier]
    channel_manager_count: int
    year1_focus: list[str]
    year2_focus: list[str]
    year3_focus: list[str]
    investment_total_y1: float
    rationale: list[str]


def design_program(org: dict[str, Any]) -> ProgramDesign:
    name = org.get("name", "Unnamed Org")
    stage = org.get("stage", "growth")  # seed / growth / scale / mature
    arr = float(org.get("arr", 5_000_000))
    target_partners = int(org.get("target_active_partners", 20))
    icp = (org.get("icp_segment") or "mid-market").lower()
    geography = org.get("geography", "US/EU")

    rationale: list[str] = []

    # Partner types based on stage + ICP
    types: list[str] = []
    if stage in ("seed", "growth"):
        types = ["Tech / Integration", "Marketplace"]
        rationale.append("Early stage: start with tech partnerships + marketplace listings (low-investment, high-leverage)")
    elif icp == "smb":
        types = ["Reseller", "Affiliate", "Marketplace"]
        rationale.append("SMB ICP: high-volume / lower-touch channels — reseller, affiliate, marketplace")
    elif icp == "enterprise":
        types = ["Strategic Alliance", "VAR / SI", "Co-sell with cloud providers", "Tech / Integration"]
        rationale.append("Enterprise ICP: strategic alliances + VARs/SIs + cloud co-sell")
    else:  # mid-market
        types = ["Reseller", "VAR", "Tech / Integration", "Marketplace"]
        rationale.append("Mid-market ICP: balanced mix of reseller, VAR, tech, marketplace")

    # Tier structure based on target partner count
    if target_partners < 15:
        tiers = [
            Tier("Authorized", 0, 0.10, 0, 1, 0, 0, "Shared pool",
                 ["Standard partner portal access", "Standard support", "Self-paced training"]),
            Tier("Preferred", 100_000, 0.15, 0, 3, 2, 0.01, "Shared pool with quarterly QBR",
                 ["MDF eligible", "Co-marketing", "Deal registration priority"]),
        ]
        rationale.append("Small program: start with 2 tiers; expand later")
    elif target_partners < 50:
        tiers = [
            Tier("Authorized", 0, 0.10, 0, 1, 0, 0, "Shared pool", ["Portal access", "Standard support"]),
            Tier("Silver", 100_000, 0.15, 0, 3, 2, 0.01, "Shared pool + QBR", ["MDF eligible", "Co-marketing"]),
            Tier("Gold", 500_000, 0.20, 0.05, 5, 5, 0.02, "Dedicated CM",
                 ["Priority deal-reg", "Lead sharing", "QBR cadence", "Joint roadmap input"]),
        ]
        rationale.append("Medium program: 3 tiers")
    else:
        tiers = [
            Tier("Authorized", 0, 0.10, 0, 1, 0, 0, "Shared pool", ["Portal access", "Standard support"]),
            Tier("Silver", 100_000, 0.15, 0, 3, 2, 0.01, "Shared pool + QBR", ["MDF eligible", "Co-marketing"]),
            Tier("Gold", 500_000, 0.20, 0.05, 5, 5, 0.02, "Dedicated CM",
                 ["Priority deal-reg", "Lead sharing", "Active co-sell"]),
            Tier("Platinum", 2_000_000, 0.25, 0.07, 10, 10, 0.03, "Dedicated Sr. Strategic CM",
                 ["Joint roadmap (quarterly)", "Advisory board seat", "Featured at events", "Press release rights"]),
        ]
        rationale.append("Large program: 4 tiers with strategic partner segment")

    cm_count = max(1, target_partners // 12)
    rationale.append(f"Channel manager headcount: {cm_count} (1 per ~12 active partners)")

    # Maturity model
    year1_focus = [
        "Build partner agreement (legal-reviewed)",
        "Stand up minimum partner portal (deal-reg + standard docs)",
        "Recruit 3-5 pilot partners (high-touch)",
        "Run self-paced training (1 course minimum)",
        "Hire 1 channel manager",
        "Standard MDF process",
    ]
    year2_focus = [
        "Add certification program (test-validated competency)",
        "Add Gold tier (if not already; differentiate top performers)",
        "Quarterly Business Reviews for Gold partners",
        "Recruit 20-30 more partners",
        "Add 2-4 channel managers (one per ~12 partners)",
        "Lead-sharing process active",
        "First annual partner conference (small)",
    ]
    year3_focus = [
        "Add Platinum tier (if not already)",
        "Advisory board with top partners",
        "Specialization programs (vertical, technology)",
        "Robust partner portal (LMS, marketing co-op, MDF self-service)",
        "100+ active partners; ramp to 40-50% partner-attributed revenue",
        "Channel team: 8-15 FTEs depending on scale",
    ]

    # Year-1 investment estimate
    cm_cost = cm_count * 200_000  # base + benefits + commission
    portal_dev = 100_000  # year 1 build
    enablement_content = 50_000
    legal = 30_000
    travel_events = 50_000
    pilot_mdf = 25_000  # year 1 limited MDF
    investment_y1 = cm_cost + portal_dev + enablement_content + legal + travel_events + pilot_mdf

    return ProgramDesign(
        org_name=name,
        stage=stage,
        recommended_partner_types=types,
        target_active_partners=target_partners,
        tiers=tiers,
        channel_manager_count=cm_count,
        year1_focus=year1_focus,
        year2_focus=year2_focus,
        year3_focus=year3_focus,
        investment_total_y1=investment_y1,
        rationale=rationale,
    )


def render_markdown(d: ProgramDesign) -> str:
    out = [f"# Partner Program Design: {d.org_name}", ""]
    out.append(f"_Stage: {d.stage} | Target active partners: {d.target_active_partners}_")
    out.append("")
    out.append("## Recommended Partner Types")
    out.append("")
    for t in d.recommended_partner_types:
        out.append(f"- {t}")
    out.append("")
    out.append("## Tier Structure")
    out.append("")
    out.append("| Tier | Revenue Threshold | Discount | Rebate | Certs | Customers | MDF | CM Engagement |")
    out.append("|------|---------------------|----------|--------|-------|-----------|-----|---------------|")
    for t in d.tiers:
        out.append(f"| {t.name} | ${t.revenue_threshold:,.0f} | {t.discount_pct*100:.0f}% | {t.rebate_pct*100:.0f}% | {t.certifications_required} | {t.customers_required} | {t.mdf_pct_of_revenue*100:.0f}% | {t.cm_engagement} |")
    out.append("")
    for t in d.tiers:
        out.append(f"### {t.name} benefits")
        for b in t.benefits:
            out.append(f"- {b}")
        out.append("")
    out.append("## Resourcing")
    out.append("")
    out.append(f"- **Channel managers needed**: {d.channel_manager_count}")
    out.append(f"- **Year-1 investment estimate**: ${d.investment_total_y1:,.0f}")
    out.append("")
    out.append("## Maturity Model")
    out.append("")
    out.append("### Year 1 — Foundation")
    for item in d.year1_focus:
        out.append(f"- {item}")
    out.append("")
    out.append("### Year 2 — Scale")
    for item in d.year2_focus:
        out.append(f"- {item}")
    out.append("")
    out.append("### Year 3 — Mature")
    for item in d.year3_focus:
        out.append(f"- {item}")
    out.append("")
    out.append("## Design Rationale")
    out.append("")
    for r in d.rationale:
        out.append(f"- {r}")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate a partner program design from org spec",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--org-spec", required=True, help="Org spec YAML")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", help="Output file path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        org = parse_yaml(Path(args.org_spec).read_text())
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    design = design_program(org)
    if args.format == "json":
        out = json.dumps(asdict(design), indent=2)
    else:
        out = render_markdown(design)
    if args.output:
        Path(args.output).write_text(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
