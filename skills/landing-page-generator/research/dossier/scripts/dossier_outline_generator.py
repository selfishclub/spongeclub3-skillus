#!/usr/bin/env python3
"""
dossier_outline_generator.py — Generate a dossier outline tailored to
subject type + purpose.

Stdlib only. JSON or markdown output.

Usage:
    python3 dossier_outline_generator.py --subject-type company --purpose deal-prep
    python3 dossier_outline_generator.py --subject-type person --purpose briefing --format markdown
    python3 dossier_outline_generator.py --subject-type market --purpose market-entry --format markdown

Subject types: company, person, market, domain
Purposes: briefing, deal-prep, due-diligence, market-entry, investment
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


BASE_OUTLINE = [
    {"section": "Executive summary", "depth": "1 page"},
    {"section": "Subject overview", "depth": "facts; brief"},
    {"section": "Context", "depth": "environmental / historical"},
    {"section": "Capabilities and assets", "depth": "key strengths + resources"},
    {"section": "People and leadership", "depth": "decision-makers"},
    {"section": "Performance and trajectory", "depth": "numbers + trend"},
    {"section": "Relationships and ecosystem", "depth": "partners + influencers"},
    {"section": "Risks and open questions", "depth": "what's worrying + unknown"},
    {"section": "Implications and recommendations", "depth": "so what"},
    {"section": "Sources and methodology", "depth": "how we know"},
]

SUBJECT_ADJUSTMENTS = {
    "company": {
        "additional_sections": [],
        "section_emphasis": {
            "Subject overview": "founding, HQ, structure, ownership",
            "Capabilities and assets": "products, IP, key infrastructure",
            "People and leadership": "exec team, board, key engineers",
            "Performance and trajectory": "revenue, growth, profitability, runway",
            "Relationships and ecosystem": "customers, partners, channel",
        },
    },
    "person": {
        "additional_sections": [
            {"section": "Background and credentials", "depth": "education + career"},
            {"section": "Public positions and statements", "depth": "what they've said"},
            {"section": "Communication and style preferences", "depth": "how to engage"},
        ],
        "section_emphasis": {
            "Subject overview": "current role + scope",
            "People and leadership": "network + relationships",
            "Performance and trajectory": "career arc + recent moves",
            "Risks and open questions": "sensitivities + privacy considerations",
        },
    },
    "market": {
        "additional_sections": [
            {"section": "Market sizing", "depth": "TAM, SAM, SOM"},
            {"section": "Customer segments", "depth": "who buys, why"},
            {"section": "Competitive landscape", "depth": "incumbents + challengers"},
            {"section": "Regulatory environment", "depth": "rules of the game"},
            {"section": "Entry barriers and economics", "depth": "what's hard"},
        ],
        "section_emphasis": {
            "Context": "macro + technology + regulatory + cultural",
            "Performance and trajectory": "growth + drivers + forecast",
        },
    },
    "domain": {
        "additional_sections": [
            {"section": "Historical context", "depth": "field development"},
            {"section": "Current state of practice", "depth": "what's done today"},
            {"section": "Key debates and open questions", "depth": "field-internal"},
            {"section": "Leading institutions and researchers", "depth": "who matters"},
            {"section": "Funding flows", "depth": "where money is going"},
        ],
        "section_emphasis": {
            "Context": "field maturity, paradigm",
            "Performance and trajectory": "recent developments + outlook",
        },
    },
}

PURPOSE_ADJUSTMENTS = {
    "briefing": {
        "front_load": ["Executive summary", "People and leadership",
                      "Performance and trajectory"],
        "added_focus": "anticipated topics + positions",
        "target_length": "2-4 pages",
    },
    "deal-prep": {
        "front_load": ["Executive summary", "Implications and recommendations",
                      "People and leadership"],
        "added_focus": "decision process, leverage, sensitivities, prior deals",
        "target_length": "5-10 pages",
    },
    "due-diligence": {
        "front_load": ["Executive summary", "Risks and open questions",
                      "Performance and trajectory"],
        "added_focus": "deep financials, legal, IP, customer contracts, employment, environmental",
        "target_length": "20-50 pages + appendices",
    },
    "market-entry": {
        "front_load": ["Executive summary", "Market sizing", "Competitive landscape",
                      "Entry barriers and economics"],
        "added_focus": "entry options compared (direct, partner, acquisition)",
        "target_length": "15-30 pages",
    },
    "investment": {
        "front_load": ["Executive summary", "Performance and trajectory",
                      "Risks and open questions"],
        "added_focus": "investment thesis, unit economics, defensibility, cap table",
        "target_length": "10-20 pages",
    },
}


def generate(subject_type: str, purpose: str) -> dict:
    base = list(BASE_OUTLINE)
    subj_adj = SUBJECT_ADJUSTMENTS.get(subject_type, {})
    purp_adj = PURPOSE_ADJUSTMENTS.get(purpose, {})

    # Add subject-specific sections
    additional = subj_adj.get("additional_sections", [])
    for add in additional:
        if not any(s["section"] == add["section"] for s in base):
            # Insert before "Risks and open questions"
            idx = next((i for i, s in enumerate(base)
                       if s["section"] == "Risks and open questions"), len(base) - 2)
            base.insert(idx, add)

    # Apply emphasis
    emphasis = subj_adj.get("section_emphasis", {})
    for s in base:
        if s["section"] in emphasis:
            s["depth"] = f"{s['depth']} | {emphasis[s['section']]}"

    # Mark front-loaded
    front_load = purp_adj.get("front_load", [])
    for s in base:
        if s["section"] in front_load:
            s["front_load"] = True
        else:
            s["front_load"] = False

    return {
        "subject_type": subject_type,
        "purpose": purpose,
        "target_length": purp_adj.get("target_length", "varies"),
        "added_focus_for_purpose": purp_adj.get("added_focus", ""),
        "front_load_priority_sections": front_load,
        "outline": base,
    }


def render_markdown(plan: dict) -> str:
    lines = []
    lines.append(f"# Dossier Outline — {plan['subject_type'].title()} ({plan['purpose']})\n")
    lines.append(f"**Target length:** {plan['target_length']}")
    lines.append(f"**Purpose-specific focus:** {plan['added_focus_for_purpose']}\n")
    lines.append("## Outline")
    lines.append("| # | Section | Depth + emphasis | Priority |")
    lines.append("|---|---------|-------------------|----------|")
    for i, s in enumerate(plan["outline"], start=1):
        priority = "FRONT-LOAD" if s.get("front_load") else "standard"
        lines.append(f"| {i} | {s['section']} | {s['depth']} | {priority} |")
    lines.append("")
    lines.append("## Front-load priority sections")
    for s in plan["front_load_priority_sections"]:
        lines.append(f"- {s}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate a dossier outline by subject type + purpose",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--subject-type",
                  choices=["company", "person", "market", "domain"], required=True)
    p.add_argument("--purpose",
                  choices=["briefing", "deal-prep", "due-diligence", "market-entry", "investment"],
                  required=True)
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--output", help="Write to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    plan = generate(args.subject_type, args.purpose)
    out = render_markdown(plan) if args.format == "markdown" else json.dumps(plan, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
