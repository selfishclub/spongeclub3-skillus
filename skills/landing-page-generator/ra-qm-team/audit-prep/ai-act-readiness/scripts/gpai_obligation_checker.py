#!/usr/bin/env python3
"""
gpai_obligation_checker.py — Check GPAI provider obligations (EU AI Act Article 53+).

Reads a model spec YAML; emits GPAI applicability + per-obligation completion
+ systemic-risk applicability (Article 55).

Stdlib only. Markdown or JSON.

Usage:
    python3 gpai_obligation_checker.py --model model.yaml
    python3 gpai_obligation_checker.py --model model.yaml --format json
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


# Standard GPAI obligations (Article 53+)
STANDARD_GPAI_OBLIGATIONS = {
    "technical_documentation_annex_xi": "Technical documentation per Annex XI",
    "training_data_summary_public": "Training data summary (publicly available, sufficiently detailed)",
    "copyright_policy": "Copyright compliance policy (honor text/data mining opt-outs)",
    "information_to_downstream_providers": "Information enabling downstream provider compliance",
}

# Systemic risk additions (Article 55, models > 10^25 FLOPs)
SYSTEMIC_RISK_OBLIGATIONS = {
    "model_evaluations_state_of_the_art": "State-of-the-art model evaluations",
    "adversarial_testing": "Adversarial testing (red-teaming)",
    "systemic_risk_assessment": "Systemic risk assessment + mitigation",
    "serious_incident_reporting": "Serious incident reporting to AI Office",
    "cybersecurity_protection": "Cybersecurity protection at appropriate level",
    "physical_security_protection": "Physical security of model weights",
}

# Code of Practice elements (presumption of conformity if adhered to)
CODE_OF_PRACTICE = {
    "code_of_practice_signed": "Signed Code of Practice on GPAI",
    "transparency_disclosures": "Transparency disclosures per Code of Practice",
    "copyright_chapter_compliance": "Copyright chapter compliance",
}


@dataclass
class ObligationStatus:
    obligation: str
    description: str
    status: str  # complete / missing / partial
    notes: str


@dataclass
class Report:
    model_name: str
    is_gpai: bool
    has_systemic_risk: bool
    training_compute_flops: str
    standard_obligations: list[ObligationStatus]
    systemic_risk_obligations: list[ObligationStatus]
    code_of_practice_status: list[ObligationStatus]
    summary_completion_pct: int
    recommendations: list[str]


def check_obligation(
    name: str, description: str, model: dict[str, Any], evidence_key: str
) -> ObligationStatus:
    evidence = model.get(evidence_key)
    if isinstance(evidence, bool):
        if evidence:
            return ObligationStatus(name, description, "complete", "Confirmed")
        return ObligationStatus(name, description, "missing", "Not confirmed")
    elif isinstance(evidence, dict):
        notes = evidence.get("notes", "")
        if evidence.get("complete", False):
            return ObligationStatus(name, description, "complete", notes or "Confirmed")
        return ObligationStatus(name, description, "partial", notes or "In progress")
    return ObligationStatus(name, description, "missing", "No evidence provided")


def is_systemic_risk(model: dict[str, Any]) -> bool:
    """Per Article 51: systemic risk if training compute > 10^25 FLOPs."""
    if model.get("declared_systemic_risk", False):
        return True
    flops = model.get("training_compute_flops", 0)
    try:
        flops_num = float(flops)
        return flops_num >= 1e25
    except (ValueError, TypeError):
        return False


def report(model: dict[str, Any]) -> Report:
    name = model.get("model_name", "<unnamed>")
    is_gpai = model.get("is_general_purpose", False) or model.get("declared_gpai", False)
    has_systemic = is_systemic_risk(model)
    compute = str(model.get("training_compute_flops", "not specified"))

    if not is_gpai:
        return Report(
            model_name=name,
            is_gpai=False,
            has_systemic_risk=False,
            training_compute_flops=compute,
            standard_obligations=[],
            systemic_risk_obligations=[],
            code_of_practice_status=[],
            summary_completion_pct=0,
            recommendations=["System is not classified as GPAI. GPAI obligations do not apply. If using a GPAI from another provider, downstream-provider obligations may apply per Article 51.2."],
        )

    obligations_data = model.get("obligations", {}) or {}
    standard = [
        check_obligation(name, desc, obligations_data, name)
        for name, desc in STANDARD_GPAI_OBLIGATIONS.items()
    ]
    systemic = []
    if has_systemic:
        systemic = [
            check_obligation(name, desc, obligations_data, name)
            for name, desc in SYSTEMIC_RISK_OBLIGATIONS.items()
        ]
    code = [
        check_obligation(name, desc, obligations_data, name)
        for name, desc in CODE_OF_PRACTICE.items()
    ]

    all_obligations = standard + systemic
    complete_count = sum(1 for o in all_obligations if o.status == "complete")
    pct = int(100 * complete_count / len(all_obligations)) if all_obligations else 0

    recommendations = []
    if has_systemic and any(o.status != "complete" for o in systemic):
        recommendations.append("Systemic risk obligations are MANDATORY for models > 10^25 FLOPs. Prioritize closure.")
    if any(o.status != "complete" for o in standard):
        recommendations.append("Standard GPAI obligations (Article 53) effective Aug 2025; close gaps.")
    if not any(o.status == "complete" for o in code):
        recommendations.append("Consider signing GPAI Code of Practice for presumption of conformity.")
    if not recommendations:
        recommendations.append("All GPAI obligations appear complete. Maintain via periodic review.")

    return Report(
        model_name=name,
        is_gpai=True,
        has_systemic_risk=has_systemic,
        training_compute_flops=compute,
        standard_obligations=standard,
        systemic_risk_obligations=systemic,
        code_of_practice_status=code,
        summary_completion_pct=pct,
        recommendations=recommendations,
    )


def render_markdown(r: Report) -> str:
    out = [f"# GPAI Obligation Report: {r.model_name}", ""]
    out.append(f"- **GPAI**: {'Yes' if r.is_gpai else 'No'}")
    out.append(f"- **Systemic risk (Article 55)**: {'Yes' if r.has_systemic_risk else 'No'}")
    out.append(f"- **Training compute (FLOPs)**: {r.training_compute_flops}")
    out.append(f"- **Overall completion**: {r.summary_completion_pct}%")
    out.append("")
    if not r.is_gpai:
        out.append("## Recommendations")
        out.append("")
        for rec in r.recommendations:
            out.append(f"- {rec}")
        return "\n".join(out)
    out.append("## Standard GPAI Obligations (Article 53)")
    out.append("")
    out.append("| Obligation | Status | Notes |")
    out.append("|------------|--------|-------|")
    for o in r.standard_obligations:
        out.append(f"| {o.description} | {o.status} | {o.notes} |")
    out.append("")
    if r.has_systemic_risk:
        out.append("## Systemic Risk Obligations (Article 55)")
        out.append("")
        out.append("| Obligation | Status | Notes |")
        out.append("|------------|--------|-------|")
        for o in r.systemic_risk_obligations:
            out.append(f"| {o.description} | {o.status} | {o.notes} |")
        out.append("")
    out.append("## Code of Practice (voluntary, presumption of conformity)")
    out.append("")
    out.append("| Item | Status | Notes |")
    out.append("|------|--------|-------|")
    for o in r.code_of_practice_status:
        out.append(f"| {o.description} | {o.status} | {o.notes} |")
    out.append("")
    out.append("## Recommendations")
    out.append("")
    for rec in r.recommendations:
        out.append(f"- {rec}")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Check GPAI obligations per EU AI Act Article 53+",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--model", required=True, help="Model spec YAML")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", help="Output file path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        doc = parse_yaml(Path(args.model).read_text())
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
