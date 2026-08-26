#!/usr/bin/env python3
"""
ai_maturity_assessor.py — Score AI maturity across 5 dimensions (0-100).

Reads a populated JSON describing the AI organization's current state, scores
each of 5 dimensions (strategy, data, mlops, governance, people), produces
an overall maturity score, identifies prioritized gaps, and emits either
JSON or markdown.

Stdlib only.

Usage:
    python3 ai_maturity_assessor.py --input company_ai_state.json
    python3 ai_maturity_assessor.py --input company_ai_state.json --format markdown
    python3 ai_maturity_assessor.py --input company_ai_state.json --output report.md

Input schema (top-level keys, all optional but missing keys score 0 for that dim):
{
  "org_name": "Acme",
  "as_of": "2026-05-27",
  "strategy": {
      "written_strategy": true|false,
      "themes_count": 0-10,
      "kpis_count": 0-10,
      "board_review_cadence_months": 0-12,
      "ties_to_business_outcomes": "none|partial|strong",
      "horizon_months": 12
  },
  "data": {
      "lineage_coverage_pct": 0-100,
      "dq_program": "none|partial|mature",
      "consent_management": "none|partial|mature",
      "data_residency_documented": true|false,
      "labeling_capability": "none|outsourced|in-house+qa"
  },
  "mlops": {
      "model_registry": "none|partial|full",
      "eval_harness": "none|adhoc|shared",
      "ci_for_models": true|false,
      "production_monitoring": "none|partial|full",
      "drift_detection": true|false,
      "rollback_supported": true|false,
      "ft_model_count": 0,
      "production_systems": 0
  },
  "governance": {
      "ai_policy_published": true|false,
      "council_active": true|false,
      "model_review_board": true|false,
      "risk_register_count": 0,
      "aiia_template_in_use": true|false,
      "incident_response_runbook": true|false,
      "vendor_review_process": "none|partial|mature",
      "frameworks_aligned": ["nist-ai-rmf","iso-42001","eu-ai-act","sr-11-7"]
  },
  "people": {
      "head_of_ai_role_filled": true|false,
      "applied_ml_engineers": 0,
      "platform_engineers": 0,
      "governance_lead": true|false,
      "literacy_program": "none|partial|all-tiers",
      "ladder_supports_ai": true|false
  }
}
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DIMENSIONS = ["strategy", "data", "mlops", "governance", "people"]

MATURITY_BANDS = [
    (0, 24, "Ad hoc",
     "AI activity exists but is uncoordinated. Most work is exploratory or in shadow."),
    (25, 49, "Emerging",
     "Some foundations are in place; governance is partial; few production systems."),
    (50, 74, "Defined",
     "Operating model is articulated; platform and governance exist; production scale is meaningful."),
    (75, 89, "Managed",
     "Quantitative goals are tracked; risk is actively managed; consistent delivery across BUs."),
    (90, 100, "Optimizing",
     "Continuous improvement loop is operational; AI is a core competency."),
]


@dataclass
class DimScore:
    name: str
    score: int
    max_score: int = 100
    findings: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)


def _safe(d: dict[str, Any] | None, key: str, default: Any = None) -> Any:
    if not d:
        return default
    return d.get(key, default)


def _bool_score(val: Any, weight: int) -> int:
    return weight if bool(val) else 0


def _tri_score(val: Any, mapping: dict[str, int]) -> int:
    if not isinstance(val, str):
        return 0
    return mapping.get(val.lower().strip(), 0)


def score_strategy(d: dict[str, Any] | None) -> DimScore:
    s = DimScore(name="strategy", score=0)
    if not d:
        s.findings.append("no strategy data provided")
        s.gaps.extend([
            "publish a written AI strategy with 3-5 themes",
            "tie themes to business outcomes (revenue, cost, risk)",
            "define 3-5 KPIs and a board review cadence",
        ])
        return s

    written = _bool_score(_safe(d, "written_strategy"), 25)
    s.score += written
    if not written:
        s.gaps.append("publish a written, signed AI strategy")
    else:
        s.findings.append("written strategy in place")

    themes = int(_safe(d, "themes_count", 0) or 0)
    if 3 <= themes <= 6:
        s.score += 15
        s.findings.append(f"{themes} themes (well-bounded)")
    elif themes > 0:
        s.score += 8
        s.gaps.append(f"narrow themes to 3-6 (currently {themes})")
    else:
        s.gaps.append("no strategic themes defined")

    kpis = int(_safe(d, "kpis_count", 0) or 0)
    if 3 <= kpis <= 6:
        s.score += 15
        s.findings.append(f"{kpis} KPIs (right range)")
    elif kpis > 0:
        s.score += 6
        s.gaps.append(f"target 3-6 KPIs (currently {kpis})")
    else:
        s.gaps.append("define 3-5 KPIs (attributable, not vanity)")

    ties = _tri_score(_safe(d, "ties_to_business_outcomes"),
                     {"none": 0, "partial": 10, "strong": 25})
    s.score += ties
    if ties < 25:
        s.gaps.append("strengthen P&L attribution per theme")

    cadence = int(_safe(d, "board_review_cadence_months", 0) or 0)
    if 1 <= cadence <= 3:
        s.score += 20
        s.findings.append(f"board review every {cadence} months")
    elif cadence <= 6:
        s.score += 10
        s.gaps.append("increase board review cadence to quarterly")
    else:
        s.gaps.append("establish a board review cadence (quarterly is healthy)")

    s.score = min(100, s.score)
    return s


def score_data(d: dict[str, Any] | None) -> DimScore:
    s = DimScore(name="data", score=0)
    if not d:
        s.gaps.extend([
            "measure data lineage coverage",
            "establish a data quality program",
            "document consent + residency",
        ])
        return s

    lineage = int(_safe(d, "lineage_coverage_pct", 0) or 0)
    s.score += min(25, lineage // 4)
    if lineage < 60:
        s.gaps.append(f"raise data lineage coverage (currently {lineage}%)")
    elif lineage >= 80:
        s.findings.append(f"strong lineage coverage ({lineage}%)")

    dq = _tri_score(_safe(d, "dq_program"),
                   {"none": 0, "partial": 10, "mature": 25})
    s.score += dq
    if dq < 25:
        s.gaps.append("mature the data quality program (see data-quality-auditor skill)")

    consent = _tri_score(_safe(d, "consent_management"),
                        {"none": 0, "partial": 10, "mature": 20})
    s.score += consent
    if consent < 20:
        s.gaps.append("formalize consent management end-to-end")

    if _safe(d, "data_residency_documented"):
        s.score += 15
        s.findings.append("data residency documented")
    else:
        s.gaps.append("document data residency and cross-border transfer posture")

    labeling = _tri_score(_safe(d, "labeling_capability"),
                         {"none": 0, "outsourced": 8, "in-house+qa": 15})
    s.score += labeling
    if labeling < 15:
        s.gaps.append("build labeling QA layer over outsourced annotation")

    s.score = min(100, s.score)
    return s


def score_mlops(d: dict[str, Any] | None) -> DimScore:
    s = DimScore(name="mlops", score=0)
    if not d:
        s.gaps.extend([
            "stand up model registry + shared eval harness",
            "add production monitoring + drift detection",
        ])
        return s

    reg = _tri_score(_safe(d, "model_registry"),
                    {"none": 0, "partial": 8, "full": 20})
    s.score += reg
    if reg < 20:
        s.gaps.append("complete the model registry (every production model registered)")

    evalh = _tri_score(_safe(d, "eval_harness"),
                      {"none": 0, "adhoc": 8, "shared": 20})
    s.score += evalh
    if evalh < 20:
        s.gaps.append("consolidate to a shared, versioned eval harness")

    if _safe(d, "ci_for_models"):
        s.score += 10
        s.findings.append("CI pipeline runs on model changes")
    else:
        s.gaps.append("add CI checks on model changes (eval, smoke, perf)")

    mon = _tri_score(_safe(d, "production_monitoring"),
                    {"none": 0, "partial": 8, "full": 20})
    s.score += mon
    if mon < 20:
        s.gaps.append("complete production monitoring (quality, latency, cost)")

    if _safe(d, "drift_detection"):
        s.score += 10
        s.findings.append("drift detection in place")
    else:
        s.gaps.append("add drift detection on inputs and outputs")

    if _safe(d, "rollback_supported"):
        s.score += 10
        s.findings.append("model rollback supported")
    else:
        s.gaps.append("verify model rollback path (one-flag disable)")

    prod_count = int(_safe(d, "production_systems", 0) or 0)
    if prod_count >= 10:
        s.score += 10
        s.findings.append(f"{prod_count} production AI systems")
    elif prod_count >= 3:
        s.score += 5
        s.findings.append(f"{prod_count} production AI systems")

    s.score = min(100, s.score)
    return s


def score_governance(d: dict[str, Any] | None) -> DimScore:
    s = DimScore(name="governance", score=0)
    if not d:
        s.gaps.extend([
            "publish AI policy + stand up council",
            "establish risk register + AIIA process",
        ])
        return s

    if _safe(d, "ai_policy_published"):
        s.score += 15
        s.findings.append("AI policy published")
    else:
        s.gaps.append("publish a signed AI policy (AUP + governance)")

    if _safe(d, "council_active"):
        s.score += 10
        s.findings.append("AI council is active")
    else:
        s.gaps.append("stand up an AI council (exec, monthly/quarterly)")

    if _safe(d, "model_review_board"):
        s.score += 15
        s.findings.append("model review board operational")
    else:
        s.gaps.append("establish model review board (technical, biweekly)")

    rr = int(_safe(d, "risk_register_count", 0) or 0)
    if rr >= 20:
        s.score += 15
        s.findings.append(f"risk register has {rr} entries")
    elif rr > 0:
        s.score += 8
        s.gaps.append("grow risk register coverage to all production + planned systems")
    else:
        s.gaps.append("seed the risk register (use ai_risk_register_generator.py)")

    if _safe(d, "aiia_template_in_use"):
        s.score += 10
        s.findings.append("AIIA template in use")
    else:
        s.gaps.append("adopt an AIIA template (3-5 pages with appendices)")

    if _safe(d, "incident_response_runbook"):
        s.score += 10
        s.findings.append("AI incident runbook exists")
    else:
        s.gaps.append("write the AI incident response runbook + tabletop annually")

    vendor = _tri_score(_safe(d, "vendor_review_process"),
                       {"none": 0, "partial": 8, "mature": 15})
    s.score += vendor
    if vendor < 15:
        s.gaps.append("mature third-party AI vendor review (no-training, residency, indemnity)")

    frameworks = _safe(d, "frameworks_aligned", []) or []
    if isinstance(frameworks, list) and len(frameworks) >= 2:
        s.score += 10
        s.findings.append(f"aligned to: {', '.join(frameworks)}")
    elif frameworks:
        s.score += 5

    s.score = min(100, s.score)
    return s


def score_people(d: dict[str, Any] | None) -> DimScore:
    s = DimScore(name="people", score=0)
    if not d:
        s.gaps.extend([
            "hire a head of AI",
            "build literacy program for all employees",
        ])
        return s

    if _safe(d, "head_of_ai_role_filled"):
        s.score += 20
        s.findings.append("head of AI / CAIO role filled")
    else:
        s.gaps.append("hire/promote a head of AI with shipping experience")

    appml = int(_safe(d, "applied_ml_engineers", 0) or 0)
    if appml >= 5:
        s.score += 20
    elif appml >= 2:
        s.score += 12
    elif appml >= 1:
        s.score += 6
    if appml < 2:
        s.gaps.append("grow applied ML engineering to at least 2 to cover oncall + delivery")

    plat = int(_safe(d, "platform_engineers", 0) or 0)
    if plat >= 2:
        s.score += 15
    elif plat == 1:
        s.score += 8
    if plat < 1:
        s.gaps.append("hire a platform engineer for gateway/eval/observability")

    if _safe(d, "governance_lead"):
        s.score += 15
        s.findings.append("governance lead in place")
    else:
        s.gaps.append("hire/assign a dedicated AI governance lead")

    lit = _tri_score(_safe(d, "literacy_program"),
                    {"none": 0, "partial": 10, "all-tiers": 20})
    s.score += lit
    if lit < 20:
        s.gaps.append("expand AI literacy to all four tiers (all-eng-product-exec)")

    if _safe(d, "ladder_supports_ai"):
        s.score += 10
        s.findings.append("engineering ladder supports AI examples")
    else:
        s.gaps.append("update engineering ladder with AI-specific examples (avoid a separate AI ladder)")

    s.score = min(100, s.score)
    return s


SCORERS = {
    "strategy": score_strategy,
    "data": score_data,
    "mlops": score_mlops,
    "governance": score_governance,
    "people": score_people,
}


def band_for(score: int) -> tuple[str, str]:
    for lo, hi, label, desc in MATURITY_BANDS:
        if lo <= score <= hi:
            return label, desc
    return "Unknown", ""


def overall_score(dims: list[DimScore]) -> int:
    if not dims:
        return 0
    return round(sum(d.score for d in dims) / len(dims))


def prioritized_gaps(dims: list[DimScore], top_n: int = 10) -> list[dict[str, str]]:
    gaps: list[dict[str, str]] = []
    sorted_dims = sorted(dims, key=lambda d: d.score)
    for d in sorted_dims:
        priority = "high" if d.score < 40 else ("medium" if d.score < 70 else "low")
        for g in d.gaps:
            gaps.append({"dimension": d.name, "gap": g, "priority": priority})
            if len(gaps) >= top_n:
                return gaps
    return gaps


def render_markdown(result: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# AI Maturity Assessment — {result.get('org_name','(unnamed org)')}")
    lines.append(f"_as of {result.get('as_of','(no date)')}_\n")
    band = result["overall"]["band"]
    score = result["overall"]["score"]
    lines.append(f"## Overall: **{score}/100 — {band}**")
    lines.append(result["overall"]["description"])
    lines.append("")
    lines.append("## Dimension scores\n")
    lines.append("| Dimension | Score | Band |")
    lines.append("|-----------|-------|------|")
    for d in result["dimensions"]:
        lines.append(f"| {d['name']} | {d['score']}/100 | {d['band']} |")
    lines.append("")
    lines.append("## Findings by dimension\n")
    for d in result["dimensions"]:
        if d["findings"]:
            lines.append(f"### {d['name'].title()}")
            for f in d["findings"]:
                lines.append(f"- {f}")
            lines.append("")
    lines.append("## Prioritized gap list\n")
    lines.append("| Priority | Dimension | Gap |")
    lines.append("|----------|-----------|-----|")
    for g in result["prioritized_gaps"]:
        lines.append(f"| {g['priority']} | {g['dimension']} | {g['gap']} |")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Score AI maturity across 5 dimensions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON file with current AI state")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--top-gaps", type=int, default=12)
    p.add_argument("--output", help="Write to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"error: cannot read input: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 2

    dims: list[DimScore] = []
    for name in DIMENSIONS:
        scorer = SCORERS[name]
        dims.append(scorer(raw.get(name)))

    total = overall_score(dims)
    band, desc = band_for(total)

    result: dict[str, Any] = {
        "org_name": raw.get("org_name", ""),
        "as_of": raw.get("as_of", ""),
        "overall": {"score": total, "band": band, "description": desc},
        "dimensions": [
            {
                "name": d.name,
                "score": d.score,
                "band": band_for(d.score)[0],
                "findings": d.findings,
                "gaps": d.gaps,
            }
            for d in dims
        ],
        "prioritized_gaps": prioritized_gaps(dims, top_n=args.top_gaps),
    }

    out = render_markdown(result) if args.format == "markdown" else json.dumps(result, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
