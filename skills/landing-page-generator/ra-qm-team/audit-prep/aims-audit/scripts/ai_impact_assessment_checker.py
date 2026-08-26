#!/usr/bin/env python3
"""
ai_impact_assessment_checker.py — Validate AI Impact Assessment (AIIA) completeness
per ISO 42001 Annex A.5.

Reads an AIIA YAML; emits per-section check + completeness score.

Stdlib only. Markdown or JSON.

Usage:
    python3 ai_impact_assessment_checker.py --aiia system-aiia.yaml
    python3 ai_impact_assessment_checker.py --aiia system-aiia.yaml --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
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


# AIIA required sections (per ISO 42001 Annex A.5 + good practice)
AIIA_SECTIONS = {
    "system_overview": [
        "system_name", "purpose", "intended_use", "deployment_context",
        "system_owner", "developer",
    ],
    "stakeholder_identification": [
        "individuals_affected", "organizational_stakeholders",
        "societal_stakeholders", "stakeholder_engagement_record",
    ],
    "potential_impacts": [
        "individual_impacts_identified", "societal_impacts_identified",
        "environmental_impacts_identified", "positive_impacts",
        "negative_impacts", "magnitude_assessment", "likelihood_assessment",
    ],
    "risk_assessment": [
        "risks_identified", "risk_ratings", "risk_owners",
        "treatment_decisions", "residual_risk_acceptance",
    ],
    "mitigations": [
        "technical_mitigations", "organizational_mitigations",
        "mitigation_owners", "mitigation_effectiveness_planned",
    ],
    "human_oversight": [
        "oversight_role_defined", "intervention_mechanism",
        "stop_mechanism", "explainability_mechanism",
    ],
    "monitoring_plan": [
        "monitoring_metrics", "monitoring_frequency",
        "drift_detection", "incident_response_link",
    ],
    "review_and_approval": [
        "reviewed_by_ai_governance", "approved_by_authorized_person",
        "approval_date", "next_review_date",
    ],
}


@dataclass
class SectionCheck:
    section: str
    items_present: int
    items_required: int
    completeness_pct: int
    missing: list[str]


@dataclass
class AIIAReport:
    system_name: str
    section_checks: list[SectionCheck]
    overall_completeness: int
    is_current: bool
    warnings: list[str]


def check_aiia(aiia: dict[str, Any]) -> AIIAReport:
    name = aiia.get("system_name", "<unnamed>")
    sections_data = aiia.get("sections", {}) or {}
    checks: list[SectionCheck] = []
    total_present = 0
    total_required = 0
    for section_name, required_items in AIIA_SECTIONS.items():
        section_data = sections_data.get(section_name, {}) or {}
        present_count = sum(1 for item in required_items if section_data.get(item))
        missing = [item for item in required_items if not section_data.get(item)]
        completeness = int(100 * present_count / len(required_items)) if required_items else 0
        checks.append(SectionCheck(
            section=section_name,
            items_present=present_count,
            items_required=len(required_items),
            completeness_pct=completeness,
            missing=missing,
        ))
        total_present += present_count
        total_required += len(required_items)
    overall = int(100 * total_present / total_required) if total_required else 0

    # Currency check
    warnings = []
    is_current = True
    review_section = sections_data.get("review_and_approval", {}) or {}
    next_review = review_section.get("next_review_date")
    if next_review:
        try:
            nr = datetime.fromisoformat(str(next_review).replace("Z", "+00:00"))
            if nr < datetime.now(timezone.utc):
                is_current = False
                warnings.append(f"Next review date ({next_review}) is in the past")
        except ValueError:
            warnings.append(f"Invalid next_review_date format: {next_review}")
    else:
        warnings.append("No next review date set")

    return AIIAReport(
        system_name=name,
        section_checks=checks,
        overall_completeness=overall,
        is_current=is_current,
        warnings=warnings,
    )


def render_markdown(r: AIIAReport) -> str:
    out = [f"# AIIA Completeness Check: {r.system_name}", ""]
    out.append(f"**Overall completeness**: {r.overall_completeness}%")
    out.append(f"**Current**: {'✓ Yes' if r.is_current else '⚠️ No (next review past or missing)'}")
    out.append("")
    if r.warnings:
        out.append("## Warnings")
        for w in r.warnings:
            out.append(f"- ⚠️ {w}")
        out.append("")
    out.append("## Section Completeness")
    out.append("")
    out.append("| Section | Items | Complete % |")
    out.append("|---------|-------|------------|")
    for c in r.section_checks:
        out.append(f"| {c.section} | {c.items_present}/{c.items_required} | {c.completeness_pct}% |")
    out.append("")
    out.append("## Missing Items")
    out.append("")
    for c in r.section_checks:
        if c.missing:
            out.append(f"### {c.section}")
            for m in c.missing:
                out.append(f"- [ ] {m}")
            out.append("")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Validate AI Impact Assessment completeness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--aiia", required=True, help="AIIA YAML")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", help="Output file path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        doc = parse_yaml(Path(args.aiia).read_text())
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    r = check_aiia(doc)
    if args.format == "json":
        out = json.dumps(asdict(r), indent=2, default=str)
    else:
        out = render_markdown(r)
    if args.output:
        Path(args.output).write_text(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
