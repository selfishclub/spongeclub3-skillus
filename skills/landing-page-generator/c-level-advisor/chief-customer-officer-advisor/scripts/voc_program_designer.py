#!/usr/bin/env python3
"""
voc_program_designer.py — Assess current VoC program and recommend a target
state + 12-month rollout sequence.

Reads a JSON describing existing feedback instruments, action loops, and
governance; scores the VoC program (0-100); produces a target architecture
and phased rollout aligned to maturity.

Stdlib only. JSON or markdown output.

Usage:
    python3 voc_program_designer.py --input voc_state.json
    python3 voc_program_designer.py --input voc_state.json --format markdown

Input schema:
{
  "org_name": "Acme",
  "as_of": "2026-05-27",
  "company_stage": "series-c",       # informational; suggests instrument set
  "instruments_in_use": {
      "nps_relationship": true|false,
      "nps_transactional": true|false,
      "csat_post_ticket": true|false,
      "ces": true|false,
      "in_app_micro_surveys": true|false,
      "win_loss_interviews": true|false,
      "churn_interviews": true|false,
      "renewal_interviews": true|false,
      "behavioral_voc": true|false,
      "support_ticket_taxonomy": true|false,
      "community_listening": true|false,
      "product_analytics": true|false,
      "advisory_board": true|false
  },
  "action_loop": {
      "closed_loop_pct": 0-100,
      "synthesis_cadence_months": 0-12,
      "synthesis_recipients_count": 0-50,
      "detractor_followup_sla_days": 0-30,
      "external_response_cadence_months": 0-12
  },
  "governance": {
      "owner_named": true|false,
      "monthly_committee_active": true|false,
      "instrument_review_cadence_months": 0-12
  }
}
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


STARTER_INSTRUMENTS = [
    "nps_relationship",
    "nps_transactional",
    "csat_post_ticket",
    "churn_interviews",
    "win_loss_interviews",
    "product_analytics",
]

MATURE_INSTRUMENTS = STARTER_INSTRUMENTS + [
    "ces",
    "in_app_micro_surveys",
    "renewal_interviews",
    "behavioral_voc",
    "support_ticket_taxonomy",
    "community_listening",
    "advisory_board",
]


def score_instruments(active: dict[str, bool]) -> tuple[int, list[str], list[str]]:
    score = 0
    have: list[str] = []
    missing: list[str] = []
    for inst in MATURE_INSTRUMENTS:
        if active.get(inst):
            have.append(inst)
            score += 5 if inst in STARTER_INSTRUMENTS else 3
        else:
            missing.append(inst)
    return min(60, score), have, missing


def score_action_loop(al: dict[str, Any]) -> tuple[int, list[str]]:
    score = 0
    gaps: list[str] = []

    closed = int(al.get("closed_loop_pct", 0) or 0)
    if closed >= 90:
        score += 12
    elif closed >= 70:
        score += 8
    elif closed >= 50:
        score += 4
        gaps.append(f"raise closed-loop response rate (currently {closed}%)")
    else:
        gaps.append(f"closed-loop discipline lacking ({closed}%)")

    cad = int(al.get("synthesis_cadence_months", 0) or 0)
    if 1 <= cad <= 3:
        score += 8
    elif cad <= 6:
        score += 4
        gaps.append("tighten synthesis cadence to quarterly")
    else:
        gaps.append("publish quarterly VoC synthesis report")

    recipients = int(al.get("synthesis_recipients_count", 0) or 0)
    if recipients >= 10:
        score += 5
    elif recipients > 0:
        score += 2
        gaps.append("expand synthesis distribution (target ≥10 leaders)")
    else:
        gaps.append("identify named synthesis recipients")

    sla = int(al.get("detractor_followup_sla_days", 99) or 99)
    if sla <= 5:
        score += 8
    elif sla <= 10:
        score += 4
        gaps.append("tighten detractor follow-up SLA to ≤5 days")
    else:
        gaps.append("define detractor follow-up SLA (target ≤5 days)")

    ext = int(al.get("external_response_cadence_months", 0) or 0)
    if 1 <= ext <= 6:
        score += 5
    else:
        gaps.append("establish external 'you said / we did' cadence (quarterly or biannual)")

    return min(25, score), gaps


def score_governance(g: dict[str, Any]) -> tuple[int, list[str]]:
    score = 0
    gaps: list[str] = []

    if g.get("owner_named"):
        score += 6
    else:
        gaps.append("name a VoC program owner (CCO direct report)")

    if g.get("monthly_committee_active"):
        score += 5
    else:
        gaps.append("stand up monthly VoC committee with cross-functional members")

    cad = int(g.get("instrument_review_cadence_months", 0) or 0)
    if 6 <= cad <= 12:
        score += 4
    elif cad > 0:
        score += 2
        gaps.append("review instrument set annually (sunset / add)")
    else:
        gaps.append("schedule annual instrument review")

    return min(15, score), gaps


def overall_band(score: int) -> str:
    if score >= 90:
        return "Optimizing"
    if score >= 75:
        return "Managed"
    if score >= 50:
        return "Defined"
    if score >= 25:
        return "Emerging"
    return "Ad hoc"


def build_rollout(missing: list[str], gaps: list[str]) -> list[dict[str, Any]]:
    """Return a 12-month phased rollout: 0-3 mo / 3-6 mo / 6-12 mo."""
    starter_missing = [m for m in missing if m in STARTER_INSTRUMENTS]
    advanced_missing = [m for m in missing if m not in STARTER_INSTRUMENTS]

    return [
        {
            "phase": "Months 0-3 — Foundation",
            "focus": "Stand up starter instruments + close the basic action loop",
            "actions": (
                [f"adopt: {m}" for m in starter_missing[:4]]
                + [g for g in gaps if "closed-loop" in g or "synthesis" in g or "detractor" in g][:4]
            ),
        },
        {
            "phase": "Months 3-6 — Action discipline",
            "focus": "Make the action loop enforceable; expand to next-tier instruments",
            "actions": (
                [f"adopt: {m}" for m in starter_missing[4:] + advanced_missing[:2]]
                + [g for g in gaps if "owner" in g or "committee" in g or "external" in g][:3]
            ),
        },
        {
            "phase": "Months 6-12 — Maturation",
            "focus": "Adopt mature instruments + tune governance + external communication",
            "actions": (
                [f"adopt: {m}" for m in advanced_missing[2:6]]
                + [g for g in gaps if "review" in g or "cadence" in g][:3]
            ),
        },
    ]


def design(state: dict[str, Any]) -> dict[str, Any]:
    instruments_in_use = state.get("instruments_in_use", {}) or {}
    action_loop = state.get("action_loop", {}) or {}
    governance = state.get("governance", {}) or {}

    inst_score, have, missing = score_instruments(instruments_in_use)
    al_score, al_gaps = score_action_loop(action_loop)
    gov_score, gov_gaps = score_governance(governance)
    total = inst_score + al_score + gov_score

    target = {
        "starter_instruments": STARTER_INSTRUMENTS,
        "mature_instruments_to_add_after_starter": [
            i for i in MATURE_INSTRUMENTS if i not in STARTER_INSTRUMENTS
        ],
        "action_loop_targets": {
            "closed_loop_pct": "≥80%",
            "synthesis_cadence_months": "quarterly",
            "detractor_followup_sla_days": "≤5",
            "external_response_cadence_months": "biannual minimum",
        },
        "governance_targets": {
            "owner": "Head of CX Operations (reports to CCO)",
            "committee": "monthly VoC committee with CCO, CPO, CMO, head of support",
            "instrument_review": "annual",
        },
    }

    rollout = build_rollout(missing, al_gaps + gov_gaps)

    return {
        "org_name": state.get("org_name", ""),
        "as_of": state.get("as_of", ""),
        "company_stage": state.get("company_stage", ""),
        "score": total,
        "band": overall_band(total),
        "breakdown": {
            "instruments": inst_score,
            "action_loop": al_score,
            "governance": gov_score,
        },
        "instruments_in_use": have,
        "missing_instruments": missing,
        "action_loop_gaps": al_gaps,
        "governance_gaps": gov_gaps,
        "target_architecture": target,
        "rollout_plan": rollout,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# VoC Program Design — {report.get('org_name','(unnamed)')}")
    lines.append(f"_as of {report['as_of']}_\n")
    lines.append(f"## Current state: **{report['score']}/100 — {report['band']}**")
    b = report["breakdown"]
    lines.append(f"- Instruments: {b['instruments']}/60")
    lines.append(f"- Action loop: {b['action_loop']}/25")
    lines.append(f"- Governance: {b['governance']}/15\n")

    lines.append("## Instruments")
    lines.append("**In use:** " + (", ".join(report["instruments_in_use"]) or "(none)"))
    lines.append("\n**Missing:** " + (", ".join(report["missing_instruments"]) or "(none)") + "\n")

    if report["action_loop_gaps"]:
        lines.append("## Action loop gaps")
        for g in report["action_loop_gaps"]:
            lines.append(f"- {g}")
        lines.append("")

    if report["governance_gaps"]:
        lines.append("## Governance gaps")
        for g in report["governance_gaps"]:
            lines.append(f"- {g}")
        lines.append("")

    lines.append("## Target architecture")
    t = report["target_architecture"]
    lines.append(f"**Starter instruments:** {', '.join(t['starter_instruments'])}")
    lines.append(f"\n**Mature additions:** {', '.join(t['mature_instruments_to_add_after_starter'])}\n")
    lines.append("**Action loop targets:**")
    for k, v in t["action_loop_targets"].items():
        lines.append(f"- {k}: {v}")
    lines.append("\n**Governance targets:**")
    for k, v in t["governance_targets"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")

    lines.append("## 12-month rollout plan")
    for phase in report["rollout_plan"]:
        lines.append(f"### {phase['phase']}")
        lines.append(f"_focus: {phase['focus']}_\n")
        for a in phase["actions"]:
            lines.append(f"- {a}")
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Design a VoC program from current state",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON with current VoC state")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--output", help="Write to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        state = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"error: cannot read input: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 2

    report = design(state)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
