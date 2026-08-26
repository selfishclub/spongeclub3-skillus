#!/usr/bin/env python3
"""
eng_productivity_dashboard.py — Classify engineering teams by DORA + DevEx
performance and surface intervention candidates.

Reads a JSON of teams with per-team metrics; classifies each team into a
band (Elite / High / Medium / Low / Needs intervention); identifies the
top 3 dimensions to focus on per team; emits org rollup + per-team detail.

Stdlib only. JSON or markdown output.

Usage:
    python3 eng_productivity_dashboard.py --input team_metrics.json
    python3 eng_productivity_dashboard.py --input team_metrics.json --format markdown

Input schema:
{
  "as_of": "2026-05-27",
  "org_name": "Acme",
  "teams": [
      {
          "id": "team-payments",
          "name": "Payments",
          "engineers": 8,
          "deploys_per_week": 12,
          "lead_time_hours_median": 6,
          "mttr_hours_median": 2,
          "change_fail_rate_pct": 12,
          "uptime_pct": 99.95,
          "sev1_quarter": 0,
          "on_call_pages_per_week": 3,
          "after_hours_page_pct": 15,
          "ci_minutes_median": 9,
          "pr_review_hours_median": 5,
          "devex_score": 75,
          "test_flake_pct": 0.5,
          "platform_adoption_pct": 85
      }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def _band_deploy(deploys_per_week: float) -> tuple[str, int]:
    if deploys_per_week >= 7:
        return ("elite", 25)
    if deploys_per_week >= 1:
        return ("high", 18)
    if deploys_per_week >= 0.25:
        return ("medium", 10)
    return ("low", 3)


def _band_lead_time(hours: float) -> tuple[str, int]:
    if hours < 1:
        return ("elite", 25)
    if hours <= 168:
        return ("high", 18)
    if hours <= 720:
        return ("medium", 10)
    return ("low", 3)


def _band_mttr(hours: float) -> tuple[str, int]:
    if hours < 1:
        return ("elite", 25)
    if hours <= 24:
        return ("high", 18)
    if hours <= 168:
        return ("medium", 10)
    return ("low", 3)


def _band_cfr(pct: float) -> tuple[str, int]:
    if pct <= 15:
        return ("elite", 25)
    if pct <= 30:
        return ("high", 18)
    if pct <= 45:
        return ("medium", 10)
    return ("low", 3)


OVERALL_BANDS = [
    (88, "Elite"),
    (65, "High"),
    (40, "Medium"),
    (20, "Low"),
    (0, "Needs intervention"),
]


@dataclass
class TeamReport:
    id: str
    name: str
    engineers: int
    dora_score: int
    health_score: int
    overall_band: str
    deploy_band: str
    lead_time_band: str
    mttr_band: str
    cfr_band: str
    findings: list[str] = field(default_factory=list)
    interventions: list[dict[str, Any]] = field(default_factory=list)


def overall_band(score: int) -> str:
    for threshold, label in OVERALL_BANDS:
        if score >= threshold:
            return label
    return "Unknown"


def assess_team(t: dict[str, Any]) -> TeamReport:
    name = t.get("name", "")
    tid = t.get("id", "")
    engineers = int(t.get("engineers", 0) or 0)

    deploys = float(t.get("deploys_per_week", 0) or 0)
    lt = float(t.get("lead_time_hours_median", 99999) or 99999)
    mttr = float(t.get("mttr_hours_median", 99999) or 99999)
    cfr = float(t.get("change_fail_rate_pct", 100) or 100)

    df_band, df_score = _band_deploy(deploys)
    lt_band, lt_score = _band_lead_time(lt)
    mttr_band, mttr_score = _band_mttr(mttr)
    cfr_band, cfr_score = _band_cfr(cfr)
    dora_score = df_score + lt_score + mttr_score + cfr_score  # max 100

    health_score = dora_score
    findings: list[str] = []
    interventions: list[dict[str, Any]] = []

    # Adjust health for non-DORA signals
    uptime = float(t.get("uptime_pct", 100) or 100)
    sev1 = int(t.get("sev1_quarter", 0) or 0)
    if uptime < 99.9:
        health_score -= 5
        interventions.append({"area": "reliability",
                              "action": f"uptime {uptime}% — drill into top incident drivers"})
    if sev1 > 1:
        health_score -= sev1 * 2
        interventions.append({"area": "reliability",
                              "action": f"{sev1} SEV1 this quarter — postmortem trends"})

    on_call = float(t.get("on_call_pages_per_week", 0) or 0)
    if on_call > 10:
        health_score -= 5
        interventions.append({"area": "on-call",
                              "action": f"{on_call} pages/wk — noisy alerts; reduce paging"})
    elif on_call > 5:
        interventions.append({"area": "on-call",
                              "action": f"{on_call} pages/wk — review alert hygiene"})

    after_hours = float(t.get("after_hours_page_pct", 0) or 0)
    if after_hours > 30:
        health_score -= 5
        interventions.append({"area": "on-call",
                              "action": f"{after_hours}% after-hours pages — sleep disruption"})

    ci = float(t.get("ci_minutes_median", 0) or 0)
    if ci > 20:
        health_score -= 5
        interventions.append({"area": "productivity",
                              "action": f"CI {ci}min — flow killer; optimize pipeline"})

    pr_hours = float(t.get("pr_review_hours_median", 0) or 0)
    if pr_hours > 24:
        health_score -= 3
        interventions.append({"area": "productivity",
                              "action": f"PR review median {pr_hours}h — set review SLA"})

    devex = int(t.get("devex_score", 0) or 0)
    if devex and devex < 60:
        health_score -= 5
        interventions.append({"area": "devex",
                              "action": f"DevEx score {devex} — interview top 3 friction"})

    flake = float(t.get("test_flake_pct", 0) or 0)
    if flake > 2:
        interventions.append({"area": "quality",
                              "action": f"test flake {flake}% — quarantine flakies"})

    plat = int(t.get("platform_adoption_pct", 0) or 0)
    if plat and plat < 60:
        interventions.append({"area": "platform",
                              "action": f"platform adoption {plat}% — identify blockers"})

    if df_band in ("elite", "high"):
        findings.append(f"deploy frequency: {df_band}")
    if lt_band in ("elite", "high"):
        findings.append(f"lead time: {lt_band}")
    if mttr_band in ("elite", "high"):
        findings.append(f"MTTR: {mttr_band}")
    if cfr_band in ("elite", "high"):
        findings.append(f"change fail rate: {cfr_band}")

    health_score = max(0, min(100, health_score))

    return TeamReport(
        id=tid, name=name, engineers=engineers,
        dora_score=dora_score, health_score=health_score,
        overall_band=overall_band(health_score),
        deploy_band=df_band, lead_time_band=lt_band,
        mttr_band=mttr_band, cfr_band=cfr_band,
        findings=findings, interventions=interventions[:5],
    )


def rollup(reports: list[TeamReport]) -> dict[str, Any]:
    if not reports:
        return {"avg_dora": 0, "avg_health": 0, "band_counts": {}}
    avg_dora = round(sum(r.dora_score for r in reports) / len(reports), 1)
    avg_health = round(sum(r.health_score for r in reports) / len(reports), 1)
    bands: dict[str, int] = {}
    for r in reports:
        bands[r.overall_band] = bands.get(r.overall_band, 0) + 1
    return {"avg_dora": avg_dora, "avg_health": avg_health, "band_counts": bands}


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Engineering Productivity Dashboard — {report.get('org_name','(unnamed)')}")
    lines.append(f"_as of {report['as_of']}_\n")
    ro = report["rollup"]
    lines.append("## Org rollup")
    lines.append(f"- Avg DORA score: **{ro['avg_dora']}/100**")
    lines.append(f"- Avg health score: **{ro['avg_health']}/100**")
    lines.append("- Band distribution: " +
                ", ".join(f"{k} ({v})" for k, v in ro["band_counts"].items()))
    lines.append("")
    lines.append("## Per-team summary")
    lines.append("| Team | Engineers | Deploy | Lead | MTTR | CFR | DORA | Health | Band |")
    lines.append("|------|-----------|--------|------|------|-----|------|--------|------|")
    for t in report["teams"]:
        lines.append(
            f"| {t['name']} | {t['engineers']} | {t['deploy_band']} | {t['lead_time_band']} | "
            f"{t['mttr_band']} | {t['cfr_band']} | {t['dora_score']} | {t['health_score']} | "
            f"{t['overall_band']} |"
        )
    lines.append("")
    lines.append("## Team detail")
    for t in report["teams"]:
        lines.append(f"### {t['name']} ({t['id']}) — {t['overall_band']}")
        lines.append(f"_engineers: {t['engineers']} | DORA: {t['dora_score']}/100 | "
                    f"health: {t['health_score']}/100_")
        if t["findings"]:
            lines.append("\n**Strengths:**")
            for f in t["findings"]:
                lines.append(f"- {f}")
        if t["interventions"]:
            lines.append("\n**Suggested interventions:**")
            for iv in t["interventions"]:
                lines.append(f"- ({iv['area']}) {iv['action']}")
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Classify teams by DORA + DevEx; surface interventions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of team metrics")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
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

    reports = [assess_team(t) for t in raw.get("teams", [])]
    # Sort by health (low first; most need attention)
    reports.sort(key=lambda r: r.health_score)
    ro = rollup(reports)

    out_data = {
        "as_of": raw.get("as_of", ""),
        "org_name": raw.get("org_name", ""),
        "rollup": ro,
        "teams": [
            {
                "id": r.id, "name": r.name, "engineers": r.engineers,
                "dora_score": r.dora_score, "health_score": r.health_score,
                "overall_band": r.overall_band,
                "deploy_band": r.deploy_band, "lead_time_band": r.lead_time_band,
                "mttr_band": r.mttr_band, "cfr_band": r.cfr_band,
                "findings": r.findings, "interventions": r.interventions,
            }
            for r in reports
        ],
    }

    out = render_markdown(out_data) if args.format == "markdown" else json.dumps(out_data, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
