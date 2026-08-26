#!/usr/bin/env python3
"""
aims_readiness_score.py — Score ISO 42001 AIMS readiness per clause + Annex A.

Reads controls YAML; emits per-area score + recommendation.

Stdlib only. Markdown or JSON.

Usage:
    python3 aims_readiness_score.py --config aims-controls.yaml
    python3 aims_readiness_score.py --config aims-controls.yaml --format json
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


AIMS_CHECKLIST = {
    "Clause_4_Context": {
        "scope_documented": 25,
        "interested_parties_identified": 25,
        "context_factors_documented": 25,
        "aims_structure_defined": 25,
    },
    "Clause_5_Leadership": {
        "leadership_commitment_evident": 25,
        "ai_policy_signed_recent": 30,
        "roles_responsibilities_defined": 25,
        "communication_internal_external": 20,
    },
    "Clause_6_Planning": {
        "ai_risk_register_current": 25,
        "risk_treatment_plans": 25,
        "aiia_per_system": 25,
        "ai_objectives_measurable": 25,
    },
    "Clause_7_Support": {
        "resources_allocated": 20,
        "competence_records": 20,
        "awareness_training": 20,
        "communication_procedures": 20,
        "documented_information_controlled": 20,
    },
    "Clause_8_Operation": {
        "lifecycle_process_documented": 30,
        "lifecycle_records_per_system": 30,
        "supplier_relationships_managed": 20,
        "aiia_applied_to_changes": 20,
    },
    "Clause_9_Performance": {
        "monitoring_per_system": 30,
        "internal_audit_completed": 35,
        "management_review_held": 35,
    },
    "Clause_10_Improvement": {
        "nc_log_current": 35,
        "corrective_actions_with_effectiveness": 35,
        "continual_improvement_evidence": 30,
    },
    "AnnexA_2_Policies": {
        "ai_policy_in_place": 50,
        "policy_aligns_with_org_policies": 25,
        "policy_reviewed_annually": 25,
    },
    "AnnexA_5_Impact_Assessment": {
        "aiia_process_documented": 30,
        "aiia_per_in_scope_system": 35,
        "societal_impact_assessed": 35,
    },
    "AnnexA_6_Lifecycle": {
        "objectives_for_responsible_dev": 15,
        "design_dev_process_documented": 15,
        "system_requirements_per_system": 10,
        "design_dev_documented": 10,
        "vv_per_system": 15,
        "deployment_controlled": 10,
        "monitoring_per_system": 15,
        "tech_documentation_per_system": 10,
    },
    "AnnexA_7_Data": {
        "data_sources_documented_per_system": 25,
        "data_quality_assessed": 25,
        "data_lineage_tracked": 25,
        "sensitive_data_protected": 25,
    },
    "AnnexA_10_Third_Party": {
        "third_party_ai_inventory": 30,
        "vendor_ai_assessment": 35,
        "contract_terms_ai_specific": 35,
    },
}


@dataclass
class AreaScore:
    area: str
    score: int
    missing_items: list[str]


@dataclass
class Report:
    overall_score: int
    area_scores: list[AreaScore]
    recommended_sprint_weeks: int
    sprint_reasoning: str


def score_area(area: str, controls: dict[str, Any]) -> AreaScore:
    checklist = AIMS_CHECKLIST.get(area, {})
    earned = 0
    missing = []
    for item, weight in checklist.items():
        if controls.get(item, False):
            earned += weight
        else:
            missing.append(item)
    return AreaScore(area=area, score=earned, missing_items=missing)


def recommend_sprint(overall: int) -> tuple[int, str]:
    if overall >= 90:
        return 4, "Strong AIMS readiness; 4-week sprint for surveillance audit"
    if overall >= 75:
        return 8, "Moderate gaps; 8-week sprint for Stage 1 + Stage 2 prep"
    if overall >= 60:
        return 12, "Significant gaps; 12-week sprint"
    return 0, "Substantial gaps; defer certification; AIMS build-out needed"


def report(doc: dict[str, Any]) -> Report:
    areas_data = doc.get("areas", {}) or {}
    scores: list[AreaScore] = []
    for area in AIMS_CHECKLIST:
        controls = areas_data.get(area, {}) or {}
        scores.append(score_area(area, controls))
    overall = sum(s.score for s in scores) // len(scores) if scores else 0
    weeks, reasoning = recommend_sprint(overall)
    return Report(overall_score=overall, area_scores=scores,
                  recommended_sprint_weeks=weeks, sprint_reasoning=reasoning)


def render_markdown(r: Report) -> str:
    out = ["# AIMS Readiness Score (ISO 42001)", ""]
    out.append(f"## Overall: {r.overall_score}/100")
    out.append("")
    out.append(f"**Recommendation**: {r.sprint_reasoning}")
    out.append("")
    out.append("## Per-Area Scores")
    out.append("")
    out.append("| Area | Score | Missing |")
    out.append("|------|-------|---------|")
    for s in r.area_scores:
        out.append(f"| {s.area} | {s.score}/100 | {len(s.missing_items)} items |")
    out.append("")
    out.append("## Gaps")
    out.append("")
    for s in r.area_scores:
        if s.missing_items:
            out.append(f"### {s.area}")
            for m in s.missing_items:
                out.append(f"- [ ] {m}")
            out.append("")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Score ISO 42001 AIMS readiness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--config", required=True, help="AIMS controls YAML")
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
