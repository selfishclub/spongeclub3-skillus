#!/usr/bin/env python3
"""
data_maturity_assessor.py — Score data maturity across 5 dimensions (0-100).

Reads a populated JSON describing the data organization's current state,
scores each of 5 dimensions (strategy, governance, quality, platform, people),
produces an overall maturity score, and identifies prioritized gaps.

Stdlib only.

Usage:
    python3 data_maturity_assessor.py --input company_data_state.json
    python3 data_maturity_assessor.py --input company_data_state.json --format markdown

Input schema (top-level keys; missing keys score 0 for that dimension):
{
  "org_name": "Acme",
  "as_of": "2026-05-27",
  "strategy": {
      "written_strategy": true|false,
      "themes_count": 0-10,
      "kpis_count": 0-10,
      "board_review_cadence_months": 0-12,
      "ties_to_business_outcomes": "none|partial|strong",
      "monetization_thesis_defined": true|false
  },
  "governance": {
      "policy_published": true|false,
      "council_active": true|false,
      "working_group_active": true|false,
      "data_owners_assigned_pct": 0-100,
      "classification_in_use": true|false,
      "catalog_state": "none|partial|comprehensive",
      "lineage_coverage_pct": 0-100,
      "internal_audit_cadence_months": 0-12,
      "open_audit_findings": 0
  },
  "quality": {
      "critical_datasets_with_sla_pct": 0-100,
      "sla_hit_rate_pct": 0-100,
      "incident_runbook_in_use": true|false,
      "automated_quality_tests": "none|partial|comprehensive",
      "dq_owners_named": true|false,
      "postmortems_completed_pct": 0-100
  },
  "platform": {
      "single_warehouse_or_lakehouse": true|false,
      "orchestration_in_place": true|false,
      "transformation_framework": "none|partial|established",
      "catalog_lineage_tooling": "none|partial|established",
      "observability": "none|partial|comprehensive",
      "cost_attribution": "none|partial|comprehensive",
      "vendor_consolidation_score": 0-10,
      "data_products_count": 0
  },
  "people": {
      "cdo_or_head_of_data_filled": true|false,
      "data_engineers": 0,
      "analytics_engineers": 0,
      "governance_lead": true|false,
      "stewards_assigned": true|false,
      "literacy_program": "none|partial|all-tiers"
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


DIMENSIONS = ["strategy", "governance", "quality", "platform", "people"]

MATURITY_BANDS = [
    (0, 24, "Ad hoc", "Data activity is uncoordinated; pipelines and dashboards proliferate without standards."),
    (25, 49, "Emerging", "Some foundations exist; governance is partial; few certified datasets."),
    (50, 74, "Defined", "Operating model is articulated; platform and governance exist; meaningful production scale."),
    (75, 89, "Managed", "Quantitative goals tracked; quality SLAs enforced; consistent delivery across BUs."),
    (90, 100, "Optimizing", "Continuous improvement is operational; data is a core competency."),
]


@dataclass
class DimScore:
    name: str
    score: int
    findings: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)


def _s(d: dict[str, Any] | None, key: str, default: Any = None) -> Any:
    return (d or {}).get(key, default)


def _bool(val: Any, weight: int) -> int:
    return weight if bool(val) else 0


def _tri(val: Any, mapping: dict[str, int]) -> int:
    return mapping.get(str(val).lower().strip(), 0) if isinstance(val, str) else 0


def score_strategy(d: dict[str, Any] | None) -> DimScore:
    s = DimScore(name="strategy", score=0)
    if not d:
        s.gaps.append("publish a written data strategy with 3-5 themes")
        return s

    if _s(d, "written_strategy"):
        s.score += 25
        s.findings.append("written strategy in place")
    else:
        s.gaps.append("publish a written, signed data strategy")

    themes = int(_s(d, "themes_count", 0) or 0)
    if 3 <= themes <= 5:
        s.score += 15
        s.findings.append(f"{themes} themes (well-bounded)")
    elif themes > 0:
        s.score += 8
        s.gaps.append(f"narrow themes to 3-5 (currently {themes})")
    else:
        s.gaps.append("no strategic themes defined")

    kpis = int(_s(d, "kpis_count", 0) or 0)
    if 3 <= kpis <= 5:
        s.score += 15
    elif kpis > 0:
        s.score += 6
        s.gaps.append(f"target 3-5 KPIs (currently {kpis})")
    else:
        s.gaps.append("define 3-5 data KPIs (attributable, not vanity)")

    ties = _tri(_s(d, "ties_to_business_outcomes"), {"none": 0, "partial": 10, "strong": 20})
    s.score += ties
    if ties < 20:
        s.gaps.append("strengthen P&L attribution per theme")

    cadence = int(_s(d, "board_review_cadence_months", 0) or 0)
    if 1 <= cadence <= 3:
        s.score += 15
    elif cadence <= 6:
        s.score += 8
        s.gaps.append("increase board review cadence to quarterly")
    else:
        s.gaps.append("establish board review cadence (quarterly is healthy)")

    if _s(d, "monetization_thesis_defined"):
        s.score += 10
        s.findings.append("monetization thesis defined")

    s.score = min(100, s.score)
    return s


def score_governance(d: dict[str, Any] | None) -> DimScore:
    s = DimScore(name="governance", score=0)
    if not d:
        s.gaps.append("publish policy + stand up council + assign owners")
        return s

    if _s(d, "policy_published"):
        s.score += 15
        s.findings.append("policy published")
    else:
        s.gaps.append("publish signed data governance policy")

    if _s(d, "council_active"):
        s.score += 10
        s.findings.append("council active")
    else:
        s.gaps.append("stand up data council (executive)")

    if _s(d, "working_group_active"):
        s.score += 10
        s.findings.append("governance working group active")
    else:
        s.gaps.append("stand up governance working group (biweekly)")

    owners_pct = int(_s(d, "data_owners_assigned_pct", 0) or 0)
    s.score += min(15, owners_pct // 7)
    if owners_pct < 80:
        s.gaps.append(f"assign owners to remaining domains (currently {owners_pct}%)")

    if _s(d, "classification_in_use"):
        s.score += 10
        s.findings.append("classification in use")
    else:
        s.gaps.append("publish classification scheme and wire to access controls")

    cat = _tri(_s(d, "catalog_state"), {"none": 0, "partial": 8, "comprehensive": 15})
    s.score += cat
    if cat < 15:
        s.gaps.append("complete catalog coverage on top 50 datasets")

    lineage = int(_s(d, "lineage_coverage_pct", 0) or 0)
    s.score += min(15, lineage // 7)
    if lineage < 60:
        s.gaps.append(f"raise lineage coverage to ≥80% on critical datasets (currently {lineage}%)")

    audit_cad = int(_s(d, "internal_audit_cadence_months", 0) or 0)
    if 1 <= audit_cad <= 3:
        s.score += 10
        s.findings.append(f"internal audit every {audit_cad} months")
    elif audit_cad > 0:
        s.score += 5
        s.gaps.append("tighten internal audit cadence to quarterly")
    else:
        s.gaps.append("establish quarterly internal audit cadence")

    open_findings = int(_s(d, "open_audit_findings", 0) or 0)
    if open_findings == 0:
        s.findings.append("no open audit findings")
    elif open_findings <= 5:
        s.score -= 5
        s.gaps.append(f"resolve {open_findings} open audit findings")
    else:
        s.score -= 10
        s.gaps.append(f"resolve {open_findings} open audit findings (critical backlog)")

    s.score = max(0, min(100, s.score))
    return s


def score_quality(d: dict[str, Any] | None) -> DimScore:
    s = DimScore(name="quality", score=0)
    if not d:
        s.gaps.append("define SLAs on top 20 critical datasets")
        return s

    with_sla = int(_s(d, "critical_datasets_with_sla_pct", 0) or 0)
    s.score += min(25, with_sla // 4)
    if with_sla < 80:
        s.gaps.append(f"publish SLAs on remaining critical datasets ({with_sla}% covered)")

    hit_rate = int(_s(d, "sla_hit_rate_pct", 0) or 0)
    s.score += min(25, hit_rate // 4)
    if hit_rate < 95:
        s.gaps.append(f"raise SLA hit rate to ≥95% (currently {hit_rate}%)")

    if _s(d, "incident_runbook_in_use"):
        s.score += 15
        s.findings.append("incident runbook in use")
    else:
        s.gaps.append("publish data incident runbook and exercise quarterly")

    tests = _tri(_s(d, "automated_quality_tests"), {"none": 0, "partial": 10, "comprehensive": 20})
    s.score += tests
    if tests < 20:
        s.gaps.append("expand automated quality tests across critical datasets")

    if _s(d, "dq_owners_named"):
        s.score += 10
        s.findings.append("DQ owners named per dataset")
    else:
        s.gaps.append("name a DQ owner per critical dataset")

    pm_pct = int(_s(d, "postmortems_completed_pct", 0) or 0)
    s.score += min(5, pm_pct // 20)
    if pm_pct < 80:
        s.gaps.append(f"complete postmortems on data incidents ({pm_pct}% completed)")

    s.score = min(100, s.score)
    return s


def score_platform(d: dict[str, Any] | None) -> DimScore:
    s = DimScore(name="platform", score=0)
    if not d:
        s.gaps.append("consolidate on a single warehouse or lakehouse")
        return s

    if _s(d, "single_warehouse_or_lakehouse"):
        s.score += 20
        s.findings.append("single warehouse / lakehouse")
    else:
        s.gaps.append("consolidate analytic compute on a single primary platform")

    if _s(d, "orchestration_in_place"):
        s.score += 10
        s.findings.append("orchestration in place")
    else:
        s.gaps.append("standardize orchestration (Airflow / Dagster / Prefect)")

    tx = _tri(_s(d, "transformation_framework"), {"none": 0, "partial": 8, "established": 15})
    s.score += tx
    if tx < 15:
        s.gaps.append("standardize transformations (dbt or equivalent)")

    cat = _tri(_s(d, "catalog_lineage_tooling"), {"none": 0, "partial": 8, "established": 15})
    s.score += cat
    if cat < 15:
        s.gaps.append("establish catalog + lineage tooling")

    obs = _tri(_s(d, "observability"), {"none": 0, "partial": 8, "comprehensive": 15})
    s.score += obs
    if obs < 15:
        s.gaps.append("complete observability (pipelines, freshness, drift)")

    cost = _tri(_s(d, "cost_attribution"), {"none": 0, "partial": 5, "comprehensive": 10})
    s.score += cost
    if cost < 10:
        s.gaps.append("instrument cost attribution per data product")

    consol = int(_s(d, "vendor_consolidation_score", 0) or 0)
    s.score += min(10, consol)
    if consol < 7:
        s.gaps.append("reduce vendor sprawl (consolidate to anchor + ≤3 satellites)")

    dp = int(_s(d, "data_products_count", 0) or 0)
    if dp >= 10:
        s.score += 5
        s.findings.append(f"{dp} named data products")

    s.score = min(100, s.score)
    return s


def score_people(d: dict[str, Any] | None) -> DimScore:
    s = DimScore(name="people", score=0)
    if not d:
        s.gaps.append("hire CDO or head of data")
        return s

    if _s(d, "cdo_or_head_of_data_filled"):
        s.score += 20
        s.findings.append("CDO / head of data role filled")
    else:
        s.gaps.append("hire / promote a head of data")

    de = int(_s(d, "data_engineers", 0) or 0)
    if de >= 5:
        s.score += 20
    elif de >= 2:
        s.score += 12
    elif de >= 1:
        s.score += 6
    if de < 2:
        s.gaps.append("grow data engineering to ≥2 for on-call + delivery")

    ae = int(_s(d, "analytics_engineers", 0) or 0)
    if ae >= 2:
        s.score += 15
    elif ae >= 1:
        s.score += 8
    if ae < 1:
        s.gaps.append("hire ≥1 analytics engineer (dbt practitioner)")

    if _s(d, "governance_lead"):
        s.score += 15
        s.findings.append("governance lead in place")
    else:
        s.gaps.append("hire / assign a governance lead")

    if _s(d, "stewards_assigned"):
        s.score += 10
        s.findings.append("data stewards assigned")
    else:
        s.gaps.append("assign data stewards per critical domain")

    lit = _tri(_s(d, "literacy_program"), {"none": 0, "partial": 10, "all-tiers": 20})
    s.score += lit
    if lit < 20:
        s.gaps.append("build data literacy program (all-eng-product-exec tiers)")

    s.score = min(100, s.score)
    return s


SCORERS = {
    "strategy": score_strategy,
    "governance": score_governance,
    "quality": score_quality,
    "platform": score_platform,
    "people": score_people,
}


def band_for(score: int) -> tuple[str, str]:
    for lo, hi, label, desc in MATURITY_BANDS:
        if lo <= score <= hi:
            return label, desc
    return "Unknown", ""


def overall_score(dims: list[DimScore]) -> int:
    return round(sum(d.score for d in dims) / len(dims)) if dims else 0


def prioritized_gaps(dims: list[DimScore], top_n: int) -> list[dict[str, str]]:
    gaps: list[dict[str, str]] = []
    for d in sorted(dims, key=lambda x: x.score):
        priority = "high" if d.score < 40 else ("medium" if d.score < 70 else "low")
        for g in d.gaps:
            gaps.append({"dimension": d.name, "gap": g, "priority": priority})
            if len(gaps) >= top_n:
                return gaps
    return gaps


def render_markdown(result: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Data Maturity Assessment — {result.get('org_name','(unnamed org)')}")
    lines.append(f"_as of {result.get('as_of','(no date)')}_\n")
    o = result["overall"]
    lines.append(f"## Overall: **{o['score']}/100 — {o['band']}**")
    lines.append(o["description"])
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
        description="Score data maturity across 5 dimensions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON file with current data state")
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

    dims = [SCORERS[name](raw.get(name)) for name in DIMENSIONS]
    total = overall_score(dims)
    band, desc = band_for(total)

    result = {
        "org_name": raw.get("org_name", ""),
        "as_of": raw.get("as_of", ""),
        "overall": {"score": total, "band": band, "description": desc},
        "dimensions": [
            {"name": d.name, "score": d.score, "band": band_for(d.score)[0],
             "findings": d.findings, "gaps": d.gaps}
            for d in dims
        ],
        "prioritized_gaps": prioritized_gaps(dims, args.top_gaps),
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
