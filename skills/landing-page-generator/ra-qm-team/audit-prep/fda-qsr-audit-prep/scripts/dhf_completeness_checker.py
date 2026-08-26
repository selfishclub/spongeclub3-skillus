#!/usr/bin/env python3
"""
dhf_completeness_checker.py — Validate Design History File (DHF) completeness
per 21 CFR 820.30.

Reads a DHF YAML; emits per-section completeness check, missing components,
warnings for incomplete or stale items.

Stdlib only. Markdown or JSON.

Usage:
    python3 dhf_completeness_checker.py --dhf device-dhf.yaml
    python3 dhf_completeness_checker.py --dhf device-dhf.yaml --format json
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


# Required DHF sections per 21 CFR 820.30
DHF_SECTIONS = {
    "design_plan": {
        "required": ["plan_document", "responsibilities_defined", "interfaces_identified"],
        "weight": 10,
    },
    "design_inputs": {
        "required": ["user_needs", "intended_use", "regulatory_requirements", "performance_requirements", "safety_requirements"],
        "weight": 15,
    },
    "design_outputs": {
        "required": ["specifications_documented", "outputs_traceable_to_inputs", "approved_for_release"],
        "weight": 15,
    },
    "design_reviews": {
        "required": ["preliminary_review", "intermediate_review", "final_review", "review_records_with_attendance"],
        "weight": 15,
    },
    "design_verification": {
        "required": ["verification_protocols", "verification_reports", "outputs_meet_inputs"],
        "weight": 15,
    },
    "design_validation": {
        "required": ["validation_protocols", "validation_reports", "intended_use_validated", "actual_or_simulated_use"],
        "weight": 15,
    },
    "design_transfer": {
        "required": ["transfer_procedures", "production_readiness", "transfer_acceptance"],
        "weight": 5,
    },
    "design_changes": {
        "required": ["change_control_process", "all_changes_documented", "changes_reviewed_and_approved"],
        "weight": 5,
    },
    "risk_management": {
        "required": ["iso_14971_risk_analysis", "risk_management_file_present", "risks_mitigated_or_accepted"],
        "weight": 5,
    },
}


@dataclass
class SectionCheck:
    section: str
    score: int
    missing_items: list[str]
    warnings: list[str]


@dataclass
class DHFReport:
    device_name: str
    overall_completeness: int
    section_checks: list[SectionCheck]
    qmsr_ready: bool
    qmsr_gaps: list[str]


def check_section(section_name: str, section_data: dict[str, Any]) -> SectionCheck:
    spec = DHF_SECTIONS.get(section_name, {})
    required = spec.get("required", [])
    weight = spec.get("weight", 1)
    missing = [r for r in required if not section_data.get(r, False)]
    warnings = []
    earned = (len(required) - len(missing)) * weight / len(required) if required else 0
    if section_data.get("last_updated"):
        try:
            d = datetime.fromisoformat(str(section_data["last_updated"]).replace("Z", "+00:00"))
            age = (datetime.now(timezone.utc) - d).days
            if age > 365 and section_name in ("design_inputs", "design_outputs"):
                warnings.append(f"Section last updated {age} days ago (>365); may be stale")
        except ValueError:
            warnings.append(f"Invalid last_updated date: {section_data['last_updated']}")
    return SectionCheck(
        section=section_name,
        score=int(earned),
        missing_items=missing,
        warnings=warnings,
    )


def check_dhf(dhf: dict[str, Any]) -> DHFReport:
    device_name = dhf.get("device_name", "<unnamed device>")
    sections_data = dhf.get("sections", {}) or {}
    checks: list[SectionCheck] = []
    total_possible = 0
    earned = 0
    for section_name, spec in DHF_SECTIONS.items():
        section_data = sections_data.get(section_name, {}) or {}
        check = check_section(section_name, section_data)
        checks.append(check)
        total_possible += spec.get("weight", 1)
        earned += check.score
    completeness = int(100 * earned / total_possible) if total_possible else 0

    qmsr_gaps = []
    rm = sections_data.get("risk_management", {}) or {}
    if not rm.get("iso_14971_risk_analysis"):
        qmsr_gaps.append("ISO 14971 risk analysis required for QMSR")
    sw = sections_data.get("software_lifecycle", {}) or {}
    if dhf.get("contains_software", False) and not sw.get("iec_62304_compliance"):
        qmsr_gaps.append("IEC 62304 software lifecycle required for QMSR (software device)")
    us = sections_data.get("usability_engineering", {}) or {}
    if not us.get("iec_62366_usability"):
        qmsr_gaps.append("IEC 62366 usability engineering recommended for QMSR")

    return DHFReport(
        device_name=device_name,
        overall_completeness=completeness,
        section_checks=checks,
        qmsr_ready=not qmsr_gaps,
        qmsr_gaps=qmsr_gaps,
    )


def render_markdown(r: DHFReport) -> str:
    out = [f"# DHF Completeness: {r.device_name}", ""]
    out.append(f"## Overall completeness: {r.overall_completeness}/100")
    out.append("")
    out.append(f"## QMSR readiness: {'✓ Ready' if r.qmsr_ready else '⚠️ Gaps exist'}")
    if r.qmsr_gaps:
        out.append("")
        for g in r.qmsr_gaps:
            out.append(f"- [ ] {g}")
    out.append("")
    out.append("## Per-Section Completeness")
    out.append("")
    out.append("| Section | Score | Missing |")
    out.append("|---------|-------|---------|")
    for c in r.section_checks:
        spec = DHF_SECTIONS.get(c.section, {})
        max_weight = spec.get("weight", 1)
        out.append(f"| {c.section} | {c.score}/{max_weight} | {len(c.missing_items)} items |")
    out.append("")
    out.append("## Detailed Gaps")
    out.append("")
    for c in r.section_checks:
        if c.missing_items or c.warnings:
            out.append(f"### {c.section}")
            for m in c.missing_items:
                out.append(f"- [ ] Missing: {m}")
            for w in c.warnings:
                out.append(f"- ⚠️ {w}")
            out.append("")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Check DHF completeness per 21 CFR 820.30",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--dhf", required=True, help="DHF YAML")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", help="Output file path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        doc = parse_yaml(Path(args.dhf).read_text())
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    r = check_dhf(doc)
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
