#!/usr/bin/env python3
"""
multi_framework_scorer.py — Score compliance readiness across multiple frameworks.

Reads controls YAML; emits per-framework score + cross-framework efficiency analysis
+ recommendations for sequencing or shared evidence opportunities.

Stdlib only. Markdown or JSON.

Usage:
    python3 multi_framework_scorer.py --config controls.yaml
    python3 multi_framework_scorer.py --config controls.yaml --frameworks SOC2,ISO27001,GDPR
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


# Per-framework requirements (high-level; not exhaustive)
FRAMEWORK_REQUIREMENTS = {
    "SOC2": {
        "info_security_policy": 10,
        "access_controls": 10,
        "encryption_at_rest": 8,
        "encryption_in_transit": 8,
        "logging_monitoring": 10,
        "incident_response": 10,
        "vulnerability_management": 10,
        "change_management": 8,
        "vendor_management": 8,
        "backup_dr_tested": 8,
        "risk_assessment_annual": 10,
    },
    "ISO27001": {
        "info_security_policy": 8,
        "access_controls": 10,
        "encryption_at_rest": 8,
        "encryption_in_transit": 8,
        "logging_monitoring": 8,
        "incident_response": 10,
        "vulnerability_management": 8,
        "change_management": 8,
        "vendor_management": 8,
        "backup_dr_tested": 8,
        "risk_assessment_annual": 10,
        "isms_internal_audit": 8,
    },
    "NIST_CSF": {
        "info_security_policy": 8,
        "access_controls": 10,
        "encryption_at_rest": 8,
        "encryption_in_transit": 8,
        "logging_monitoring": 10,
        "incident_response": 12,
        "vulnerability_management": 10,
        "change_management": 8,
        "vendor_management": 10,
        "backup_dr_tested": 8,
        "risk_assessment_annual": 8,
    },
    "GDPR": {
        "ropa_current": 15,
        "privacy_notice_current": 10,
        "dpia_for_high_risk": 15,
        "dpa_with_processors": 15,
        "data_subject_rights_process": 15,
        "breach_notification_capability": 10,
        "international_transfers_mechanism": 10,
        "encryption_in_transit": 5,
        "encryption_at_rest": 5,
    },
    "HIPAA": {
        "info_security_policy": 8,
        "access_controls": 12,
        "encryption_at_rest": 10,
        "encryption_in_transit": 10,
        "logging_monitoring": 10,
        "incident_response": 10,
        "vulnerability_management": 8,
        "vendor_management": 12,  # BAAs
        "backup_dr_tested": 10,
        "risk_assessment_annual": 10,
    },
    "PCI_DSS": {
        "access_controls": 12,
        "encryption_at_rest": 12,
        "encryption_in_transit": 12,
        "logging_monitoring": 12,
        "incident_response": 8,
        "vulnerability_management": 12,  # quarterly ASV
        "change_management": 8,
        "physical_security": 8,
        "training": 8,
        "annual_audit": 8,
    },
}


@dataclass
class FrameworkScore:
    framework: str
    score: int
    missing_controls: list[str]


@dataclass
class Report:
    frameworks: list[FrameworkScore]
    shared_controls_count: int
    framework_specific_controls: dict[str, list[str]]
    cross_framework_efficiency_pct: int
    recommendations: list[str]


def score_framework(framework: str, controls: dict[str, Any]) -> FrameworkScore:
    reqs = FRAMEWORK_REQUIREMENTS.get(framework, {})
    if not reqs:
        return FrameworkScore(framework=framework, score=0, missing_controls=[f"Unknown framework: {framework}"])
    earned = 0
    missing = []
    for control, weight in reqs.items():
        if controls.get(control, False):
            earned += weight
        else:
            missing.append(control)
    return FrameworkScore(framework=framework, score=earned, missing_controls=missing)


def analyze(controls: dict[str, Any], frameworks: list[str]) -> Report:
    scores = [score_framework(fw, controls) for fw in frameworks]

    # Shared controls
    all_required = set()
    per_framework_reqs = {}
    for fw in frameworks:
        reqs = set(FRAMEWORK_REQUIREMENTS.get(fw, {}).keys())
        per_framework_reqs[fw] = reqs
        all_required |= reqs

    # Controls shared across >= 2 frameworks
    counts: dict[str, int] = {}
    for fw, reqs in per_framework_reqs.items():
        for c in reqs:
            counts[c] = counts.get(c, 0) + 1
    shared_count = sum(1 for c, n in counts.items() if n >= 2)

    # Framework-specific (only in one framework)
    fw_specific: dict[str, list[str]] = {}
    for fw, reqs in per_framework_reqs.items():
        unique = [c for c in reqs if counts.get(c, 0) == 1]
        if unique:
            fw_specific[fw] = unique

    efficiency = int(100 * shared_count / len(all_required)) if all_required else 0

    recommendations = []
    if efficiency >= 60:
        recommendations.append(f"High framework overlap ({efficiency}%) — shared-evidence strategy highly valuable")
    if any(s.score < 60 for s in scores):
        low_fw = [s.framework for s in scores if s.score < 60]
        recommendations.append(f"Low readiness in: {', '.join(low_fw)}. Address before parallel pursuit.")
    if "SOC2" in [s.framework for s in scores] and "ISO27001" in [s.framework for s in scores]:
        s2 = next((s for s in scores if s.framework == "SOC2"), None)
        i2 = next((s for s in scores if s.framework == "ISO27001"), None)
        if s2 and i2 and s2.score > 75 and i2.score > 75:
            recommendations.append("SOC 2 + ISO 27001 both >75 — pursue in parallel for cost efficiency")
    if "GDPR" in [s.framework for s in scores]:
        recommendations.append("GDPR is ongoing not certification; integrate with continuous compliance program")
    if not recommendations:
        recommendations.append("Solid baseline; continue framework-by-framework remediation")

    return Report(
        frameworks=scores,
        shared_controls_count=shared_count,
        framework_specific_controls=fw_specific,
        cross_framework_efficiency_pct=efficiency,
        recommendations=recommendations,
    )


def render_markdown(r: Report) -> str:
    out = ["# Multi-Framework Compliance Readiness", ""]
    out.append("## Per-Framework Scores")
    out.append("")
    out.append("| Framework | Score | Missing Controls |")
    out.append("|-----------|-------|------------------|")
    for s in r.frameworks:
        out.append(f"| {s.framework} | {s.score}/100 | {len(s.missing_controls)} items |")
    out.append("")
    out.append(f"## Shared Controls Analysis")
    out.append("")
    out.append(f"- **Shared controls (>=2 frameworks)**: {r.shared_controls_count}")
    out.append(f"- **Cross-framework efficiency**: {r.cross_framework_efficiency_pct}% (higher = more overlap)")
    out.append("")
    if r.framework_specific_controls:
        out.append("## Framework-Specific Controls (single-framework requirements)")
        out.append("")
        for fw, controls in r.framework_specific_controls.items():
            out.append(f"### {fw}-only")
            for c in controls:
                out.append(f"- {c}")
            out.append("")
    out.append("## Per-Framework Gaps")
    out.append("")
    for s in r.frameworks:
        if s.missing_controls:
            out.append(f"### {s.framework}")
            for m in s.missing_controls:
                out.append(f"- [ ] {m}")
            out.append("")
    out.append("## Recommendations")
    out.append("")
    for rec in r.recommendations:
        out.append(f"- {rec}")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Score multi-framework compliance readiness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--config", required=True, help="Controls YAML")
    p.add_argument(
        "--frameworks",
        default="SOC2,ISO27001",
        help="Comma-separated frameworks (SOC2, ISO27001, NIST_CSF, GDPR, HIPAA, PCI_DSS)",
    )
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
    frameworks = [f.strip() for f in args.frameworks.split(",")]
    controls = doc.get("controls", {}) or {}
    r = analyze(controls, frameworks)
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
