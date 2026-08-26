#!/usr/bin/env python3
"""
soc2_readiness_score.py — Rapid SOC 2 readiness score (0-100) per TSC.

Reads a controls YAML; emits score per Trust Services Criterion + overall +
recommended sprint length.

Stdlib only. Markdown or JSON output.

Usage:
    python3 soc2_readiness_score.py --config controls.yaml
    python3 soc2_readiness_score.py --config controls.yaml --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


# Minimal YAML parser (shared pattern)
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


# Per-TSC control checklist with weights (sum = 100 per criterion)
TSC_CHECKLIST = {
    "CC1": {
        "policy_approved_recent": 15,
        "background_checks": 10,
        "code_of_conduct_signed": 10,
        "training_completion": 15,
        "org_chart_current": 10,
        "security_in_performance": 10,
        "segregation_of_duties": 15,
        "ethics_hotline": 15,
    },
    "CC2": {
        "security_policy_published": 25,
        "incident_communication_paths": 25,
        "customer_security_docs": 25,
        "subservice_org_communication": 25,
    },
    "CC3": {
        "annual_risk_assessment": 30,
        "risk_register_current": 25,
        "risk_treatment_plans": 25,
        "fraud_risk_addressed": 20,
    },
    "CC4": {
        "internal_audit_or_review": 20,
        "pen_test_annual": 20,
        "vuln_scans_with_remediation": 30,
        "findings_tracked_to_closure": 30,
    },
    "CC5": {
        "control_catalog_exists": 30,
        "controls_mapped_to_risks": 30,
        "procedures_support_policies": 40,
    },
    "CC6": {
        "sso_enforced": 15,
        "mfa_universal": 20,
        "quarterly_access_review": 15,
        "privileged_access_management": 10,
        "encryption_at_rest": 10,
        "encryption_in_transit": 10,
        "access_revoked_on_termination": 10,
        "physical_access_controls": 10,
    },
    "CC7": {
        "siem_deployed": 15,
        "monitoring_dashboards": 10,
        "incident_response_plan": 15,
        "past_incidents_documented": 15,
        "vulnerability_management": 15,
        "dr_plan_with_testing": 15,
        "backup_with_restore_testing": 15,
    },
    "CC8": {
        "code_review_on_changes": 30,
        "production_deploy_approvals": 30,
        "emergency_change_process": 20,
        "pre_production_testing": 20,
    },
    "CC9": {
        "vendor_inventory_current": 25,
        "vendor_due_diligence": 30,
        "vendor_soc2_reports_collected": 25,
        "annual_vendor_reviews": 20,
    },
    "A1": {  # if in scope
        "capacity_planning": 25,
        "sla_monitoring": 25,
        "dr_testing_evidence": 25,
        "backup_restore_testing": 25,
    },
    "PI1": {  # if in scope
        "data_validation_controls": 35,
        "error_handling_evidence": 30,
        "reconciliation_evidence": 35,
    },
    "C1": {  # if in scope
        "data_classification": 35,
        "encryption_per_classification": 35,
        "disposal_procedures": 30,
    },
    "P1": {  # if in scope
        "privacy_notice_published": 20,
        "consent_management": 20,
        "data_subject_rights_process": 25,
        "retention_policy_enforced": 20,
        "data_subject_rights_records": 15,
    },
}


@dataclass
class TSCScore:
    tsc: str
    score: int
    in_scope: bool
    checklist_results: dict[str, bool]
    missing_items: list[str]


@dataclass
class ReadinessReport:
    overall_score: int
    in_scope_tscs: list[str]
    tsc_scores: list[TSCScore]
    recommended_sprint_weeks: int
    sprint_reasoning: str


def score_tsc(tsc: str, controls: dict[str, Any]) -> TSCScore:
    checklist = TSC_CHECKLIST.get(tsc, {})
    in_scope = controls.get("in_scope", True)
    results = {}
    earned = 0
    missing = []
    for item, weight in checklist.items():
        present = bool(controls.get(item, False))
        results[item] = present
        if present:
            earned += weight
        else:
            missing.append(item)
    return TSCScore(tsc=tsc, score=earned, in_scope=in_scope, checklist_results=results, missing_items=missing)


def recommend_sprint(overall: int) -> tuple[int, str]:
    if overall >= 90:
        return 4, "Highly ready; 4-week sprint sufficient (Type I)"
    if overall >= 75:
        return 8, "Moderate gaps; 8-week sprint (Type I)"
    if overall >= 60:
        return 12, "Significant gaps; 12-week sprint OR postpone audit"
    return 0, "Substantial gaps; postpone audit; multi-quarter remediation needed"


def report(controls_doc: dict[str, Any]) -> ReadinessReport:
    in_scope_tscs = controls_doc.get("in_scope_tscs", ["CC1", "CC2", "CC3", "CC4", "CC5", "CC6", "CC7", "CC8", "CC9"])
    tsc_data = controls_doc.get("tsc", {}) or {}
    scores: list[TSCScore] = []
    for tsc in in_scope_tscs:
        tsc_controls = tsc_data.get(tsc, {}) or {}
        s = score_tsc(tsc, tsc_controls)
        scores.append(s)
    if scores:
        overall = sum(s.score for s in scores) // len(scores)
    else:
        overall = 0
    sprint_weeks, reasoning = recommend_sprint(overall)
    return ReadinessReport(
        overall_score=overall,
        in_scope_tscs=in_scope_tscs,
        tsc_scores=scores,
        recommended_sprint_weeks=sprint_weeks,
        sprint_reasoning=reasoning,
    )


def render_markdown(r: ReadinessReport) -> str:
    out = ["# SOC 2 Readiness Score", ""]
    out.append(f"## Overall Score: {r.overall_score}/100")
    out.append("")
    out.append(f"**Recommendation**: {r.sprint_reasoning}")
    out.append("")
    out.append("## Per-TSC Scores")
    out.append("")
    out.append("| TSC | Score | Missing Items |")
    out.append("|-----|-------|---------------|")
    for s in r.tsc_scores:
        missing_summary = f"{len(s.missing_items)} items" if s.missing_items else "All covered"
        out.append(f"| {s.tsc} | {s.score}/100 | {missing_summary} |")
    out.append("")
    out.append("## Gap Details")
    out.append("")
    for s in r.tsc_scores:
        if s.missing_items:
            out.append(f"### {s.tsc}")
            for m in s.missing_items:
                out.append(f"- [ ] {m}")
            out.append("")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Score SOC 2 readiness per TSC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--config", required=True, help="Controls YAML")
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
