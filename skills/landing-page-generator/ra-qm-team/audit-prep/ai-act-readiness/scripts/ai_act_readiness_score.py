#!/usr/bin/env python3
"""
ai_act_readiness_score.py — Score EU AI Act readiness per article.

Reads AI system spec YAML; emits per-article score + risk class confirmation
+ sprint recommendation.

Stdlib only. Markdown or JSON.

Usage:
    python3 ai_act_readiness_score.py --config ai-system.yaml
    python3 ai_act_readiness_score.py --config ai-system.yaml --format json
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


# High-risk requirements (Articles 9-17)
HIGH_RISK_CHECKLIST = {
    "Art9_Risk_Management": {
        "risk_management_system_documented": 25,
        "continuous_risk_identification": 25,
        "mitigation_measures_implemented": 25,
        "post_market_risk_integration": 25,
    },
    "Art10_Data_Governance": {
        "training_data_documented": 20,
        "data_quality_metrics": 20,
        "representativeness_analysis": 20,
        "bias_examination": 20,
        "data_preparation_documented": 20,
    },
    "Art11_Technical_Documentation": {
        "annex_iv_documentation": 50,
        "documentation_current": 25,
        "system_architecture_documented": 25,
    },
    "Art12_Record_Keeping": {
        "automatic_logging_enabled": 40,
        "log_retention_period_defined": 30,
        "authority_access_procedure": 30,
    },
    "Art13_Transparency_Deployers": {
        "instructions_for_use": 30,
        "performance_characteristics_documented": 25,
        "limitations_documented": 25,
        "input_output_specified": 20,
    },
    "Art14_Human_Oversight": {
        "oversight_measures_designed": 30,
        "oversight_personnel_trained": 25,
        "intervention_tested": 25,
        "stop_mechanism_tested": 20,
    },
    "Art15_Accuracy_Robustness_Cyber": {
        "accuracy_metrics_declared": 25,
        "adversarial_testing_performed": 25,
        "cybersecurity_documented": 25,
        "data_poisoning_resilience": 25,
    },
    "Art17_QMS": {
        "qms_documented": 30,
        "compliance_strategy": 25,
        "techniques_documented": 25,
        "testing_strategy": 20,
    },
    "Art72_Post_Market_Monitoring": {
        "monitoring_plan_documented": 30,
        "active_monitoring": 30,
        "drift_detection": 20,
        "periodic_reviews": 20,
    },
    "Art73_Serious_Incident_Reporting": {
        "incident_identification_process": 40,
        "15_day_reporting_capability": 30,
        "incident_log_maintained": 30,
    },
    "Art4_AI_Literacy": {
        "training_provided": 50,
        "role_based_content": 30,
        "periodic_refresh": 20,
    },
}


@dataclass
class ArticleScore:
    article: str
    score: int
    missing_items: list[str]


@dataclass
class Report:
    system_name: str
    declared_risk_class: str
    high_risk_score: int
    article_scores: list[ArticleScore]
    recommended_sprint_weeks: int
    sprint_reasoning: str
    annex_iii_flag_warnings: list[str]


def score_article(article: str, controls: dict[str, Any]) -> ArticleScore:
    checklist = HIGH_RISK_CHECKLIST.get(article, {})
    earned = 0
    missing = []
    for item, weight in checklist.items():
        if controls.get(item, False):
            earned += weight
        else:
            missing.append(item)
    return ArticleScore(article=article, score=earned, missing_items=missing)


def annex_iii_classification_warnings(system: dict[str, Any]) -> list[str]:
    warnings = []
    annex_areas = system.get("annex_iii_areas", []) or []
    declared_class = system.get("risk_class", "unknown")
    if annex_areas and declared_class != "high-risk":
        warnings.append(
            f"System claims '{declared_class}' but is used in Annex III area(s): {annex_areas}. "
            "Reconfirm Article 6.3 exemption rationale or treat as high-risk."
        )
    return warnings


def recommend_sprint(overall: int) -> tuple[int, str]:
    if overall >= 90:
        return 4, "Strong readiness; 4-week sprint for periodic review"
    if overall >= 75:
        return 8, "Moderate gaps; 8-week sprint for conformity assessment prep"
    if overall >= 60:
        return 12, "Significant gaps; 12-week sprint"
    return 0, "Substantial gaps; defer assessment if possible; multi-quarter remediation"


def report(doc: dict[str, Any]) -> Report:
    system_name = doc.get("system_name", "<unnamed>")
    declared_class = doc.get("risk_class", "unknown")
    articles_data = doc.get("articles", {}) or {}
    scores: list[ArticleScore] = []
    for article in HIGH_RISK_CHECKLIST:
        controls = articles_data.get(article, {}) or {}
        scores.append(score_article(article, controls))
    overall = sum(s.score for s in scores) // len(scores) if scores else 0
    weeks, reasoning = recommend_sprint(overall)
    warnings = annex_iii_classification_warnings(doc)
    return Report(
        system_name=system_name,
        declared_risk_class=declared_class,
        high_risk_score=overall,
        article_scores=scores,
        recommended_sprint_weeks=weeks,
        sprint_reasoning=reasoning,
        annex_iii_flag_warnings=warnings,
    )


def render_markdown(r: Report) -> str:
    out = [f"# EU AI Act Readiness: {r.system_name}", ""]
    out.append(f"**Declared risk class**: {r.declared_risk_class}")
    out.append("")
    if r.annex_iii_flag_warnings:
        for w in r.annex_iii_flag_warnings:
            out.append(f"⚠️ {w}")
        out.append("")
    out.append(f"## Overall high-risk-requirements score: {r.high_risk_score}/100")
    out.append("")
    out.append(f"**Recommendation**: {r.sprint_reasoning}")
    out.append("")
    out.append("## Per-Article Scores")
    out.append("")
    out.append("| Article | Score | Missing |")
    out.append("|---------|-------|---------|")
    for s in r.article_scores:
        out.append(f"| {s.article} | {s.score}/100 | {len(s.missing_items)} items |")
    out.append("")
    out.append("## Gaps")
    out.append("")
    for s in r.article_scores:
        if s.missing_items:
            out.append(f"### {s.article}")
            for m in s.missing_items:
                out.append(f"- [ ] {m}")
            out.append("")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Score EU AI Act readiness per article",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--config", required=True, help="AI system YAML")
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
