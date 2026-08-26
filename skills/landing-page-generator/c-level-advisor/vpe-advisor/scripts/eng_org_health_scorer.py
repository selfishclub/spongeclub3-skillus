#!/usr/bin/env python3
"""
eng_org_health_scorer.py — Score engineering org health across 6 dimensions
(0-100): structure, delivery, quality, productivity, culture, talent.

Stdlib only. JSON or markdown output.

Usage:
    python3 eng_org_health_scorer.py --input eng_state.json
    python3 eng_org_health_scorer.py --input eng_state.json --format markdown

Input schema:
{
  "org_name": "Acme",
  "as_of": "2026-05-27",
  "structure": {
      "squad_count": 0,
      "avg_squad_size": 0,                       # engineers per squad
      "platform_team_size_pct": 0-30,             # % of total engineering
      "em_ic_ratio": 1.0,                         # IC per EM
      "missions_published": true|false,
      "cross_team_dependency_friction": 1-5       # 5 = high friction
  },
  "delivery": {
      "deploy_frequency_band": "elite|high|medium|low",
      "lead_time_band": "elite|high|medium|low",
      "mttr_band": "elite|high|medium|low",
      "change_fail_rate_pct": 0-100,
      "release_safety_practices": ["feature-flags","canaries","auto-rollback"]
  },
  "quality": {
      "slo_coverage_pct": 0-100,                  # % critical services with SLOs
      "uptime_pct": 0-100,                        # last quarter
      "sev1_incidents_quarter": 0,
      "blameless_postmortems_pct": 0-100,
      "test_flake_rate_pct": 0-100
  },
  "productivity": {
      "ci_pipeline_median_minutes": 0,
      "pr_review_median_hours": 0,
      "devex_survey_score": 0-100,                # eNPS or composite
      "platform_adoption_pct": 0-100,
      "meetings_per_week_per_engineer": 0
  },
  "culture": {
      "blameless_culture": true|false,
      "psych_safety_score": 0-100,                # from survey
      "code_review_norms_published": true|false,
      "career_ladder_published": true|false,
      "ic_track_real": true|false,
      "ladders_calibrated": true|false
  },
  "talent": {
      "headcount": 0,
      "open_reqs": 0,
      "time_to_hire_days": 0,
      "regrettable_attrition_pct_annual": 0-100,
      "diverse_panel_pct": 0-100,
      "promotion_cycle_run": true|false
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


DIMENSIONS = ["structure", "delivery", "quality", "productivity", "culture", "talent"]

MATURITY_BANDS = [
    (0, 24, "Ad hoc", "Engineering org is reactive; few standards; high founder dependency."),
    (25, 49, "Emerging", "Foundations exist; squad model present; quality + productivity inconsistent."),
    (50, 74, "Defined", "Operating model articulated; DORA in medium-high; talent processes work."),
    (75, 89, "Managed", "DORA elite/high; SLOs enforced; on-call sustainable; talent retained."),
    (90, 100, "Optimizing", "Continuous improvement loop; eng is a strategic advantage."),
]


DORA_BAND_SCORE = {"elite": 25, "high": 18, "medium": 10, "low": 3}


@dataclass
class DimScore:
    name: str
    score: int
    findings: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)


def _g(d: dict[str, Any] | None, k: str, default: Any = None) -> Any:
    return (d or {}).get(k, default)


def _b(v: Any, w: int) -> int:
    return w if bool(v) else 0


def score_structure(d: dict[str, Any] | None) -> DimScore:
    s = DimScore("structure", 0)
    if not d:
        s.gaps.append("define squad structure + EM/IC ratios")
        return s

    squads = int(_g(d, "squad_count", 0) or 0)
    avg_size = float(_g(d, "avg_squad_size", 0) or 0)
    if squads > 0 and 4 <= avg_size <= 8:
        s.score += 20
        s.findings.append(f"{squads} squads avg {avg_size:.1f} engineers (healthy)")
    elif squads > 0 and avg_size > 0:
        s.score += 10
        if avg_size < 4:
            s.gaps.append(f"squads small (avg {avg_size:.1f}); bus risk + on-call burden")
        elif avg_size > 8:
            s.gaps.append(f"squads large (avg {avg_size:.1f}); split candidates")
    else:
        s.gaps.append("no clear squad structure")

    plat_pct = int(_g(d, "platform_team_size_pct", 0) or 0)
    if 8 <= plat_pct <= 20:
        s.score += 20
        s.findings.append(f"platform team {plat_pct}% (healthy band)")
    elif plat_pct > 0:
        s.score += 10
        s.gaps.append(f"platform team {plat_pct}% (target 10-15%)")
    else:
        s.gaps.append("no dedicated platform team (consider at 30+ engineers)")

    ratio = float(_g(d, "em_ic_ratio", 0) or 0)
    if 5 <= ratio <= 8:
        s.score += 20
        s.findings.append(f"EM:IC ratio 1:{ratio:.0f} (healthy)")
    elif ratio > 0:
        s.score += 10
        if ratio < 4:
            s.gaps.append(f"EM:IC 1:{ratio:.0f} (managers under-loaded)")
        else:
            s.gaps.append(f"EM:IC 1:{ratio:.0f} (managers overloaded)")
    else:
        s.gaps.append("EM:IC ratio not measured")

    if _g(d, "missions_published"):
        s.score += 20
        s.findings.append("squad missions published")
    else:
        s.gaps.append("publish 1-page mission per squad")

    fric = int(_g(d, "cross_team_dependency_friction", 0) or 0)
    if fric <= 2:
        s.score += 20
    elif fric == 3:
        s.score += 10
        s.gaps.append("cross-team dependency friction medium; review boundaries")
    elif fric >= 4:
        s.gaps.append(f"cross-team dependency friction high ({fric}/5); urgent")

    s.score = min(100, s.score)
    return s


def score_delivery(d: dict[str, Any] | None) -> DimScore:
    s = DimScore("delivery", 0)
    if not d:
        s.gaps.append("instrument DORA: deploy freq, lead time, MTTR, change fail rate")
        return s

    df = (_g(d, "deploy_frequency_band") or "low").lower()
    lt = (_g(d, "lead_time_band") or "low").lower()
    mttr = (_g(d, "mttr_band") or "low").lower()
    cfr = float(_g(d, "change_fail_rate_pct", 100) or 100)

    s.score += DORA_BAND_SCORE.get(df, 3)
    s.score += DORA_BAND_SCORE.get(lt, 3)
    s.score += DORA_BAND_SCORE.get(mttr, 3)
    if df in ("elite", "high"):
        s.findings.append(f"deploy frequency band: {df}")
    else:
        s.gaps.append(f"raise deploy frequency (currently {df})")
    if lt in ("elite", "high"):
        s.findings.append(f"lead time band: {lt}")
    else:
        s.gaps.append(f"shorten lead time (currently {lt})")
    if mttr in ("elite", "high"):
        s.findings.append(f"MTTR band: {mttr}")
    else:
        s.gaps.append(f"improve MTTR (currently {mttr})")

    if cfr <= 15:
        s.score += 15
        s.findings.append(f"change fail rate {cfr}% (elite)")
    elif cfr <= 30:
        s.score += 10
        s.findings.append(f"change fail rate {cfr}% (high)")
    elif cfr <= 45:
        s.score += 5
        s.gaps.append(f"change fail rate {cfr}% (medium); target ≤15%")
    else:
        s.gaps.append(f"change fail rate {cfr}% (low); urgent")

    safety = _g(d, "release_safety_practices", []) or []
    if "feature-flags" in safety:
        s.score += 4
    if "canaries" in safety:
        s.score += 3
    if "auto-rollback" in safety:
        s.score += 3
    if len(safety) < 2:
        s.gaps.append("adopt release safety practices (flags, canaries, auto-rollback)")

    s.score = min(100, s.score)
    return s


def score_quality(d: dict[str, Any] | None) -> DimScore:
    s = DimScore("quality", 0)
    if not d:
        s.gaps.append("define SLOs on critical services + run blameless postmortems")
        return s

    slo = int(_g(d, "slo_coverage_pct", 0) or 0)
    s.score += min(25, slo // 4)
    if slo < 80:
        s.gaps.append(f"raise SLO coverage on critical services (currently {slo}%)")

    uptime = float(_g(d, "uptime_pct", 0) or 0)
    if uptime >= 99.95:
        s.score += 25
        s.findings.append(f"uptime {uptime}%")
    elif uptime >= 99.9:
        s.score += 18
    elif uptime >= 99.5:
        s.score += 10
        s.gaps.append(f"raise uptime to 99.9%+ (currently {uptime}%)")
    elif uptime > 0:
        s.score += 3
        s.gaps.append(f"uptime {uptime}% — investigate top incident drivers")

    sev1 = int(_g(d, "sev1_incidents_quarter", 0) or 0)
    if sev1 == 0:
        s.score += 15
        s.findings.append("0 SEV1 incidents this quarter")
    elif sev1 <= 2:
        s.score += 8
    else:
        s.gaps.append(f"{sev1} SEV1 incidents this quarter — drill into systemic causes")

    pm = int(_g(d, "blameless_postmortems_pct", 0) or 0)
    s.score += min(20, pm // 5)
    if pm < 90:
        s.gaps.append(f"raise blameless postmortem completion (currently {pm}%)")

    flake = float(_g(d, "test_flake_rate_pct", 0) or 0)
    if flake < 1:
        s.score += 15
        s.findings.append(f"test flake rate {flake}% (healthy)")
    elif flake < 3:
        s.score += 8
        s.gaps.append(f"reduce test flake rate (currently {flake}%)")
    else:
        s.gaps.append(f"flaky tests {flake}% — kill or quarantine")

    s.score = min(100, s.score)
    return s


def score_productivity(d: dict[str, Any] | None) -> DimScore:
    s = DimScore("productivity", 0)
    if not d:
        s.gaps.append("instrument CI time + PR cycle + DevEx survey")
        return s

    ci = float(_g(d, "ci_pipeline_median_minutes", 999) or 999)
    if ci <= 10:
        s.score += 20
        s.findings.append(f"CI pipeline {ci}min (fast)")
    elif ci <= 20:
        s.score += 12
        s.gaps.append(f"shorten CI pipeline (currently {ci}min)")
    elif ci <= 30:
        s.score += 6
        s.gaps.append(f"CI pipeline {ci}min — optimization needed")
    else:
        s.gaps.append(f"CI pipeline {ci}min — critical; flow-killer")

    pr = float(_g(d, "pr_review_median_hours", 999) or 999)
    if pr <= 8:
        s.score += 20
        s.findings.append(f"PR review median {pr}h")
    elif pr <= 24:
        s.score += 12
    elif pr <= 48:
        s.score += 6
        s.gaps.append(f"PR review median {pr}h — target ≤24")
    else:
        s.gaps.append(f"PR review median {pr}h — establish SLA")

    devex = int(_g(d, "devex_survey_score", 0) or 0)
    if devex >= 70:
        s.score += 25
        s.findings.append(f"DevEx score {devex} (strong)")
    elif devex >= 50:
        s.score += 15
    elif devex > 0:
        s.score += 5
        s.gaps.append(f"DevEx score {devex} — investigate top friction")
    else:
        s.gaps.append("DevEx survey not run; start quarterly")

    plat_adopt = int(_g(d, "platform_adoption_pct", 0) or 0)
    s.score += min(20, plat_adopt // 5)
    if plat_adopt < 60:
        s.gaps.append(f"platform adoption {plat_adopt}% — investigate gaps")

    meetings = float(_g(d, "meetings_per_week_per_engineer", 0) or 0)
    if meetings <= 8:
        s.score += 15
        s.findings.append(f"meetings {meetings}/wk per engineer (sustainable)")
    elif meetings <= 12:
        s.score += 8
    else:
        s.gaps.append(f"meetings {meetings}/wk per engineer — flow-killer")

    s.score = min(100, s.score)
    return s


def score_culture(d: dict[str, Any] | None) -> DimScore:
    s = DimScore("culture", 0)
    if not d:
        s.gaps.append("publish career ladder + code review norms + run psych safety survey")
        return s

    if _g(d, "blameless_culture"):
        s.score += 15
        s.findings.append("blameless culture practiced")
    else:
        s.gaps.append("commit to blameless postmortems; publish protocol")

    psych = int(_g(d, "psych_safety_score", 0) or 0)
    s.score += min(25, psych // 4)
    if psych < 70:
        s.gaps.append(f"psych safety score {psych} — leader behavior + manager training")

    if _g(d, "code_review_norms_published"):
        s.score += 15
    else:
        s.gaps.append("publish code review norms (kindness + rigor)")

    if _g(d, "career_ladder_published"):
        s.score += 15
        s.findings.append("career ladder published")
    else:
        s.gaps.append("publish career ladder (IC + EM tracks)")

    if _g(d, "ic_track_real"):
        s.score += 15
        s.findings.append("IC track real (paid + promoted)")
    else:
        s.gaps.append("invest in real IC track (parity with EM)")

    if _g(d, "ladders_calibrated"):
        s.score += 15
        s.findings.append("calibration sessions run")
    else:
        s.gaps.append("run calibration sessions across managers each cycle")

    s.score = min(100, s.score)
    return s


def score_talent(d: dict[str, Any] | None) -> DimScore:
    s = DimScore("talent", 0)
    if not d:
        s.gaps.append("instrument time-to-hire + attrition + promotion cycles")
        return s

    headcount = int(_g(d, "headcount", 0) or 0)
    open_reqs = int(_g(d, "open_reqs", 0) or 0)
    if headcount > 0:
        s.score += 10
        if open_reqs / max(1, headcount) > 0.25:
            s.gaps.append(f"open req ratio high ({open_reqs}/{headcount})")
        else:
            s.findings.append(f"headcount {headcount} | open reqs {open_reqs}")

    ttf = int(_g(d, "time_to_hire_days", 0) or 0)
    if 0 < ttf <= 45:
        s.score += 20
        s.findings.append(f"time-to-hire {ttf} days (fast)")
    elif ttf <= 75:
        s.score += 12
    elif ttf > 0:
        s.score += 5
        s.gaps.append(f"time-to-hire {ttf} days — investigate pipeline + bar")
    else:
        s.gaps.append("instrument time-to-hire")

    attr = float(_g(d, "regrettable_attrition_pct_annual", 0) or 0)
    if attr <= 5:
        s.score += 25
        s.findings.append(f"regrettable attrition {attr}% (low)")
    elif attr <= 10:
        s.score += 15
        s.findings.append(f"regrettable attrition {attr}% (acceptable)")
    elif attr <= 15:
        s.score += 8
        s.gaps.append(f"regrettable attrition {attr}% — investigate top causes")
    else:
        s.gaps.append(f"regrettable attrition {attr}% — urgent")

    panel = int(_g(d, "diverse_panel_pct", 0) or 0)
    s.score += min(25, panel // 4)
    if panel < 80:
        s.gaps.append(f"raise diverse interview panel coverage (currently {panel}%)")

    if _g(d, "promotion_cycle_run"):
        s.score += 20
        s.findings.append("promotion cycle running on schedule")
    else:
        s.gaps.append("establish predictable promotion cycle (twice yearly)")

    s.score = min(100, s.score)
    return s


SCORERS = {
    "structure": score_structure,
    "delivery": score_delivery,
    "quality": score_quality,
    "productivity": score_productivity,
    "culture": score_culture,
    "talent": score_talent,
}


def band_for(score: int) -> tuple[str, str]:
    for lo, hi, label, desc in MATURITY_BANDS:
        if lo <= score <= hi:
            return label, desc
    return "Unknown", ""


def overall_score(dims: list[DimScore]) -> int:
    return round(sum(d.score for d in dims) / len(dims)) if dims else 0


def prioritized_gaps(dims: list[DimScore], top_n: int) -> list[dict[str, str]]:
    gaps = []
    for d in sorted(dims, key=lambda x: x.score):
        priority = "high" if d.score < 40 else ("medium" if d.score < 70 else "low")
        for g in d.gaps:
            gaps.append({"dimension": d.name, "gap": g, "priority": priority})
            if len(gaps) >= top_n:
                return gaps
    return gaps


def render_markdown(result: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Engineering Org Health — {result.get('org_name','(unnamed)')}")
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
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Score engineering org health across 6 dimensions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of engineering state")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--top-gaps", type=int, default=15)
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
