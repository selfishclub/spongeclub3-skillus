#!/usr/bin/env python3
"""
evidence_gap_finder.py — Identify SOC 2 evidence gaps.

Reads an evidence YAML (what evidence we have collected) + required-evidence
mapping; emits gap list with severity + sprint week to address.

Stdlib only. Markdown or JSON output.

Usage:
    python3 evidence_gap_finder.py --evidence evidence.yaml
    python3 evidence_gap_finder.py --evidence evidence.yaml --tsc CC6
    python3 evidence_gap_finder.py --evidence evidence.yaml --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
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


# Required evidence per TSC (selected high-priority)
REQUIRED_EVIDENCE = {
    "CC1": [
        ("information_security_policy_signed", "critical", 1),
        ("background_check_records", "warning", 2),
        ("training_completion_records", "warning", 2),
        ("code_of_conduct_signatures", "info", 3),
    ],
    "CC3": [
        ("annual_risk_assessment", "critical", 1),
        ("risk_register_with_owners", "warning", 2),
        ("risk_treatment_evidence", "warning", 2),
    ],
    "CC4": [
        ("vulnerability_scan_reports", "critical", 1),
        ("vulnerability_remediation_tracking", "critical", 1),
        ("pen_test_report", "warning", 2),
    ],
    "CC6": [
        ("mfa_enforcement_proof", "critical", 1),
        ("sso_configuration", "critical", 1),
        ("quarterly_access_review_records", "critical", 1),
        ("encryption_configuration", "critical", 1),
        ("termination_access_revocation_logs", "warning", 2),
    ],
    "CC7": [
        ("incident_response_runbook", "critical", 1),
        ("past_period_incident_records", "critical", 2),
        ("dr_test_results", "critical", 2),
        ("backup_restore_test_results", "critical", 2),
        ("siem_configuration", "warning", 2),
    ],
    "CC8": [
        ("code_review_evidence", "critical", 1),
        ("production_deploy_approvals", "critical", 1),
        ("emergency_change_records", "warning", 3),
    ],
    "CC9": [
        ("vendor_inventory", "critical", 1),
        ("vendor_due_diligence_records", "critical", 2),
        ("vendor_soc2_reports", "warning", 2),
    ],
}


@dataclass
class GapItem:
    tsc: str
    evidence_item: str
    severity: str  # critical / warning / info
    sprint_week_to_address: int
    status: str  # missing / stale / present
    notes: str


def find_gaps(evidence: dict[str, Any], tsc_filter: str | None) -> list[GapItem]:
    gaps: list[GapItem] = []
    evidence_data = evidence.get("evidence", {}) or {}
    now = datetime.now(timezone.utc)

    for tsc, items in REQUIRED_EVIDENCE.items():
        if tsc_filter and tsc != tsc_filter:
            continue
        tsc_evidence = evidence_data.get(tsc, {}) or {}
        for item_name, severity, sprint_week in items:
            item_data = tsc_evidence.get(item_name)
            if item_data is None:
                gaps.append(GapItem(
                    tsc=tsc,
                    evidence_item=item_name,
                    severity=severity,
                    sprint_week_to_address=sprint_week,
                    status="missing",
                    notes="No evidence on file",
                ))
            elif isinstance(item_data, dict):
                date_str = item_data.get("date")
                if date_str:
                    try:
                        evidence_date = datetime.fromisoformat(str(date_str).replace("Z", "+00:00"))
                        age_days = (now - evidence_date).days
                        if age_days > 365:
                            gaps.append(GapItem(
                                tsc=tsc,
                                evidence_item=item_name,
                                severity=severity,
                                sprint_week_to_address=sprint_week,
                                status="stale",
                                notes=f"Evidence is {age_days} days old (> 365)",
                            ))
                    except ValueError:
                        gaps.append(GapItem(
                            tsc=tsc,
                            evidence_item=item_name,
                            severity="warning",
                            sprint_week_to_address=sprint_week,
                            status="missing",
                            notes=f"Invalid date format: {date_str}",
                        ))
    return gaps


def render_markdown(gaps: list[GapItem], tsc_filter: str | None) -> str:
    out = ["# SOC 2 Evidence Gap Report", ""]
    if tsc_filter:
        out.append(f"_Filtered to TSC: {tsc_filter}_")
        out.append("")
    out.append(f"_Total gaps: {len(gaps)}_")
    out.append("")
    by_sev: dict[str, list[GapItem]] = {}
    for g in gaps:
        by_sev.setdefault(g.severity, []).append(g)
    for sev in ["critical", "warning", "info"]:
        items = by_sev.get(sev, [])
        if not items:
            continue
        out.append(f"## {sev.upper()} ({len(items)})")
        out.append("")
        out.append("| TSC | Evidence | Status | Sprint Week | Notes |")
        out.append("|-----|----------|--------|-------------|-------|")
        for g in sorted(items, key=lambda x: (x.tsc, x.evidence_item)):
            out.append(f"| {g.tsc} | {g.evidence_item} | {g.status} | W{g.sprint_week_to_address} | {g.notes} |")
        out.append("")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Find SOC 2 evidence gaps",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--evidence", required=True, help="Evidence YAML")
    p.add_argument("--tsc", help="Filter to one TSC (CC1, CC2, ..., A1, PI1, C1, P1)")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", help="Output file path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        ev = parse_yaml(Path(args.evidence).read_text())
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    gaps = find_gaps(ev, args.tsc)
    if args.format == "json":
        out = json.dumps({"gaps": [asdict(g) for g in gaps]}, indent=2, default=str)
    else:
        out = render_markdown(gaps, args.tsc)
    if args.output:
        Path(args.output).write_text(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
