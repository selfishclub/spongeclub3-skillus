#!/usr/bin/env python3
"""
qsr_readiness_score.py — Score FDA QSR / QMSR audit readiness per Subpart.

Reads a controls YAML; emits per-subpart score + overall + sprint recommendation.

Stdlib only. Markdown or JSON.

Usage:
    python3 qsr_readiness_score.py --config qsr-controls.yaml
    python3 qsr_readiness_score.py --config qsr-controls.yaml --format json
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


QSR_CHECKLIST = {
    "Subpart_B_Management_Responsibility": {
        "quality_policy_signed": 20,
        "quality_objectives_measurable": 15,
        "annual_management_review": 25,
        "management_representative_appointed": 15,
        "internal_audit_schedule_followed": 25,
    },
    "Subpart_C_Design_Controls": {
        "design_planning_per_project": 15,
        "design_inputs_documented": 15,
        "design_outputs_traceable": 10,
        "design_reviews_at_stages": 15,
        "design_verification_documented": 10,
        "design_validation_documented": 10,
        "design_transfer_controlled": 10,
        "design_changes_controlled": 5,
        "dhf_complete_per_device": 10,
    },
    "Subpart_D_Document_Controls": {
        "document_approval_procedure": 30,
        "documents_approved_before_issue": 30,
        "obsolete_documents_removed": 20,
        "document_changes_controlled": 20,
    },
    "Subpart_E_Purchasing_Controls": {
        "supplier_qualification_process": 30,
        "per_supplier_records": 30,
        "supplier_agreements_signed": 20,
        "annual_supplier_evaluation": 20,
    },
    "Subpart_G_Production_Process_Controls": {
        "process_validation_complete": 30,
        "equipment_calibration_current": 25,
        "equipment_pm_current": 20,
        "environmental_monitoring": 25,
    },
    "Subpart_I_Nonconforming_Product": {
        "nonconforming_identification": 35,
        "disposition_documented": 35,
        "authority_matrix": 30,
    },
    "Subpart_J_CAPA": {
        "capa_log_current": 20,
        "rca_per_capa": 25,
        "corrective_action_completed": 20,
        "effectiveness_verification_per_capa": 25,
        "capa_trend_analysis": 10,
    },
    "Subpart_M_Records": {
        "dmr_per_device_complete": 30,
        "dhr_per_lot_complete": 30,
        "records_retention_policy": 20,
        "records_accessible_for_inspection": 20,
    },
    "MDR_Compliance": {
        "mdr_procedure_documented": 30,
        "reportable_events_identified": 30,
        "5_day_reporting_capability": 20,
        "30_day_reporting_capability": 20,
    },
    "Complaint_Handling": {
        "complaint_log_current": 25,
        "investigation_per_complaint": 25,
        "mdr_review_per_complaint": 25,
        "complaint_trend_analysis": 25,
    },
}


@dataclass
class SubpartScore:
    subpart: str
    score: int
    missing_items: list[str]


@dataclass
class Report:
    overall_score: int
    subpart_scores: list[SubpartScore]
    recommended_sprint_weeks: int
    sprint_reasoning: str
    high_risk_subparts: list[str]


def score_subpart(subpart: str, controls: dict[str, Any]) -> SubpartScore:
    checklist = QSR_CHECKLIST.get(subpart, {})
    earned = 0
    missing = []
    for item, weight in checklist.items():
        if controls.get(item, False):
            earned += weight
        else:
            missing.append(item)
    return SubpartScore(subpart=subpart, score=earned, missing_items=missing)


def recommend_sprint(overall: int, high_risk: list[str]) -> tuple[int, str]:
    if overall >= 90:
        return 2, "Highly ready; 2-week sprint for inspection prep"
    if overall >= 75:
        return 8, "Moderate gaps; 8-week sprint"
    if overall >= 60:
        if "Subpart_J_CAPA" in high_risk or "Subpart_C_Design_Controls" in high_risk:
            return 12, "Significant gaps in high-risk areas (CAPA / Design); 12-week sprint mandatory"
        return 12, "Significant gaps; 12-week sprint"
    return 0, "Substantial gaps; defer inspection if possible; multi-quarter remediation"


def report(doc: dict[str, Any]) -> Report:
    subparts_data = doc.get("subparts", {}) or {}
    scores: list[SubpartScore] = []
    for subpart in QSR_CHECKLIST:
        controls = subparts_data.get(subpart, {}) or {}
        scores.append(score_subpart(subpart, controls))
    overall = sum(s.score for s in scores) // len(scores) if scores else 0
    # High-risk = score < 60 in critical subparts
    critical = ["Subpart_J_CAPA", "Subpart_C_Design_Controls", "Complaint_Handling", "MDR_Compliance"]
    high_risk = [s.subpart for s in scores if s.subpart in critical and s.score < 60]
    weeks, reasoning = recommend_sprint(overall, high_risk)
    return Report(
        overall_score=overall,
        subpart_scores=scores,
        recommended_sprint_weeks=weeks,
        sprint_reasoning=reasoning,
        high_risk_subparts=high_risk,
    )


def render_markdown(r: Report) -> str:
    out = ["# QSR / QMSR Readiness Score", ""]
    out.append(f"## Overall: {r.overall_score}/100")
    out.append("")
    out.append(f"**Recommendation**: {r.sprint_reasoning}")
    out.append("")
    if r.high_risk_subparts:
        out.append(f"**⚠️ High-risk subparts** (most-cited 483 areas with low score): {', '.join(r.high_risk_subparts)}")
        out.append("")
    out.append("## Per-Subpart Scores")
    out.append("")
    out.append("| Subpart | Score | Missing Items |")
    out.append("|---------|-------|---------------|")
    for s in r.subpart_scores:
        out.append(f"| {s.subpart} | {s.score}/100 | {len(s.missing_items)} items |")
    out.append("")
    out.append("## Gaps")
    out.append("")
    for s in r.subpart_scores:
        if s.missing_items:
            out.append(f"### {s.subpart}")
            for m in s.missing_items:
                out.append(f"- [ ] {m}")
            out.append("")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Score FDA QSR/QMSR audit readiness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--config", required=True, help="QSR controls YAML")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", help="Output file path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        doc = parse_yaml(Path(args.config).read_text())
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    r = report(doc)
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
