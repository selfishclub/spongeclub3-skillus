#!/usr/bin/env python3
"""
proposal_structure_validator.py — Validate proposal structure against
funder-type expectations.

Reads a JSON of proposal section list with page counts; checks for missing
sections, page-limit violations, and funder-specific structural problems.

Stdlib only. JSON or markdown output.

Usage:
    python3 proposal_structure_validator.py --input proposal_structure.json \\
        --funder-type nih
    python3 proposal_structure_validator.py --input proposal_structure.json \\
        --funder-type nsf --format markdown

Funder types: nih, nsf, sbir, foundation, darpa, generic

Input schema:
{
  "proposal_title": "...",
  "sections": [
      {"name": "Specific Aims", "pages": 1, "drafted": true},
      {"name": "Research Strategy", "pages": 12, "drafted": false},
      ...
  ]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


FUNDER_EXPECTATIONS = {
    "nih": {
        "required": [
            "Specific Aims", "Research Strategy", "Bibliography",
            "Biosketches", "Budget", "Budget Justification",
        ],
        "recommended": ["Resources / Environment", "Letters of Support"],
        "page_limits": {
            "Specific Aims": 1,
            "Research Strategy": 12,  # R01; varies by mechanism
            "Biosketches": 5,
        },
        "notes": [
            "R01: 12 pages Research Strategy; R21/R03: 6 pages",
            "Specific Aims is THE most-important page",
            "Public Project Summary required separately",
        ],
    },
    "nsf": {
        "required": [
            "Project Summary", "Project Description", "References Cited",
            "Biographical Sketches", "Budget", "Budget Justification",
            "Current and Pending Support", "Data Management Plan",
        ],
        "recommended": ["Facilities, Equipment, and Other Resources",
                       "Postdoc Mentoring Plan"],
        "page_limits": {
            "Project Summary": 1,
            "Project Description": 15,
            "Biographical Sketches": 3,
            "Data Management Plan": 2,
            "Postdoc Mentoring Plan": 1,
        },
        "notes": [
            "Project Summary must include: Overview, Intellectual Merit, Broader Impacts",
            "Project Description must address Intellectual Merit + Broader Impacts",
            "Postdoc Mentoring Plan REQUIRED if postdocs in budget",
        ],
    },
    "sbir": {
        "required": [
            "Cover Sheet", "Project Summary", "Technical Narrative",
            "Commercialization Plan", "Key Personnel", "Budget",
            "Budget Justification",
        ],
        "recommended": ["Facilities", "Letters of Support"],
        "page_limits": {"Technical Narrative": 12, "Commercialization Plan": 12},
        "notes": [
            "Commercialization Plan is 50% of the eval — invest accordingly",
            "Phase I: ~6 months, ~$300K; Phase II: ~2 years, ~$1.5M",
        ],
    },
    "foundation": {
        "required": [
            "Cover Letter", "Executive Summary", "Problem Statement",
            "Project Description", "Goals and Measurable Outcomes",
            "Timeline", "Team", "Budget",
        ],
        "recommended": [
            "Sustainability Plan", "Logic Model / Theory of Change",
            "Letters of Support",
        ],
        "page_limits": {"Executive Summary": 1},
        "notes": [
            "Foundations love measurable outcomes + sustainability",
            "Indirect cost cap is often 10-15%",
        ],
    },
    "darpa": {
        "required": [
            "Title Page", "Executive Summary", "Heilmeier Catechism",
            "Technical Approach", "Schedule + Milestones",
            "Personnel + Capabilities", "Budget", "Budget Justification",
        ],
        "recommended": ["Statement of Work", "Risk Assessment"],
        "page_limits": {"Executive Summary": 2},
        "notes": [
            "Answer all 7 Heilmeier questions explicitly",
            "DARPA likes moonshots; incremental work is wrong-funder",
        ],
    },
    "generic": {
        "required": [
            "Summary", "Problem", "Approach", "Team", "Budget", "Timeline",
        ],
        "recommended": ["Outcomes", "Risks", "References"],
        "page_limits": {},
        "notes": [],
    },
}


@dataclass
class Issue:
    severity: str
    section: str
    message: str


def validate(structure: dict[str, Any], funder_type: str) -> dict[str, Any]:
    spec = FUNDER_EXPECTATIONS.get(funder_type, FUNDER_EXPECTATIONS["generic"])
    sections = structure.get("sections", []) or []
    section_names = {s.get("name", "") for s in sections}
    issues: list[Issue] = []

    # Required sections present?
    for req in spec["required"]:
        if req not in section_names:
            issues.append(Issue("fail", req, f"required section missing"))

    # Recommended sections
    for rec in spec["recommended"]:
        if rec not in section_names:
            issues.append(Issue("warn", rec, f"recommended section not present"))

    # Page limits
    for s in sections:
        name = s.get("name", "")
        pages = float(s.get("pages", 0) or 0)
        limit = spec["page_limits"].get(name)
        if limit and pages > limit:
            issues.append(Issue("fail", name,
                              f"{pages} pages exceeds limit of {limit}"))
        elif limit and pages == 0:
            issues.append(Issue("info", name, "page count not declared"))

    # Drafted status
    undrafted = [s.get("name") for s in sections if not s.get("drafted", False)]
    if undrafted:
        issues.append(Issue("info", "(all)",
                          f"{len(undrafted)} sections marked not-drafted: "
                          f"{', '.join(undrafted[:5])}{'...' if len(undrafted) > 5 else ''}"))

    sev_counts = {"fail": 0, "warn": 0, "info": 0}
    for i in issues:
        sev_counts[i.severity] += 1

    return {
        "proposal_title": structure.get("proposal_title", ""),
        "funder_type": funder_type,
        "section_count": len(sections),
        "issues": [
            {"severity": i.severity, "section": i.section, "message": i.message}
            for i in issues
        ],
        "severity_counts": sev_counts,
        "funder_notes": spec["notes"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Proposal Structure Validation — {report.get('proposal_title','(unnamed)')}\n")
    lines.append(f"**Funder type:** {report['funder_type']}")
    lines.append(f"**Sections declared:** {report['section_count']}")
    sc = report["severity_counts"]
    lines.append(f"**Severity:** fail {sc['fail']} | warn {sc['warn']} | info {sc['info']}\n")
    if report["funder_notes"]:
        lines.append("## Funder-specific notes")
        for n in report["funder_notes"]:
            lines.append(f"- {n}")
        lines.append("")
    sev_order = {"fail": 0, "warn": 1, "info": 2}
    sorted_issues = sorted(report["issues"], key=lambda i: sev_order.get(i["severity"], 9))
    lines.append("## Issues")
    if not sorted_issues:
        lines.append("_No issues detected._")
    else:
        lines.append("| Severity | Section | Message |")
        lines.append("|----------|---------|---------|")
        for i in sorted_issues:
            lines.append(f"| {i['severity']} | {i['section']} | {i['message']} |")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Validate proposal structure against funder expectations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of proposal structure")
    p.add_argument("--funder-type",
                  choices=["nih", "nsf", "sbir", "foundation", "darpa", "generic"],
                  default="generic")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--output", help="Write to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        structure = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"error: cannot read input: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 2

    report = validate(structure, args.funder_type)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
