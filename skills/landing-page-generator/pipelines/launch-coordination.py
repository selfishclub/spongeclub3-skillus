#!/usr/bin/env python3
"""
launch-coordination.py -- orchestrates a coordinated launch sequence.

Pipeline stages:
  1. beta-program            (execution/beta-program)
  2. feature-flag-strategy   (execution/feature-flag-strategy)
  3. launch-playbook         (execution/launch-playbook)
  4. release-notes           (execution/release-notes)

Outputs (one per stage) + a launch readiness summary with a go/no-go
checklist.

Usage:
    python launch-coordination.py --demo --output ./out
    python launch-coordination.py --input launch.json --output ./out
    python launch-coordination.py --demo --format json

Date: 2026-05-22
Standard library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SCHEMA = "pm/pipelines/launch-coordination/v1"
ROOT = Path(__file__).resolve().parent.parent
PM = ROOT / "project-management"


STAGES: list[dict[str, Any]] = [
    {
        "name": "beta-program",
        "skill": PM / "execution" / "beta-program",
        "tool": "scripts/beta_program_planner.py",
        "artifact": "01-beta-program.md",
        "purpose": "Closed beta playbook (recruit, brief, observe, iterate, GA gate).",
    },
    {
        "name": "feature-flag-strategy",
        "skill": PM / "execution" / "feature-flag-strategy",
        "tool": "scripts/flag_strategist.py",
        "artifact": "02-flag-strategy.md",
        "purpose": "Phased rollouts, kill-switches, flag debt (Fowler taxonomy).",
    },
    {
        "name": "launch-playbook",
        "skill": PM / "execution" / "launch-playbook",
        "tool": "scripts/launch_planner.py",
        "artifact": "03-launch-playbook.md",
        "purpose": "Internal + external launch coordination, T-minus checklist.",
    },
    {
        "name": "release-notes",
        "skill": PM / "execution" / "release-notes",
        "tool": "scripts/release_notes_generator.py",
        "artifact": "04-release-notes.md",
        "purpose": "Audience-segmented release notes (customer / admin / API).",
    },
]


DEMO_LAUNCH: dict[str, Any] = {
    "feature_name": "Bulk-edit Candidates",
    "owner": "Jane Doe (PM)",
    "target_ga_date": "2026-07-15",
    "beta": {
        "target_participants": 24,
        "criteria": "enterprise tier, >= 200 candidates / month",
        "duration_weeks": 4,
        "success_gate_metric": "candidate-edit time reduction >= 50% in beta cohort",
    },
    "feature_flag": {
        "name": "bulk_edit_v1",
        "type": "release",
        "rollout_phases": [
            {"phase": "internal_dogfood", "percent": 100, "audience": "engineering + product"},
            {"phase": "closed_beta", "percent": 100, "audience": "24 design partners"},
            {"phase": "ramp_5", "percent": 5, "audience": "enterprise tier only"},
            {"phase": "ramp_25", "percent": 25, "audience": "enterprise + growth tier"},
            {"phase": "GA", "percent": 100, "audience": "all customers"},
        ],
        "kill_switch": True,
        "retire_by": "2026-Q4",
    },
    "launch": {
        "internal_announcement_date": "2026-07-08",
        "external_announcement_date": "2026-07-15",
        "channels": ["in-product banner", "blog post", "email to admins", "sales enablement deck"],
    },
    "release_notes_audiences": ["admin", "customer", "api"],
}


GO_NOGO_CHECKLIST = [
    ("Beta success metric met", "beta.success_gate_metric"),
    ("Feature flag kill-switch tested", "feature_flag.kill_switch"),
    ("Security review signed off", None),
    ("Customer-success enablement complete", None),
    ("Sales enablement complete", None),
    ("Release notes drafted for all audiences", "release_notes_audiences"),
    ("SLO dashboards instrumented for new code paths", None),
    ("Rollback runbook in place", None),
]


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_stage(stage: dict[str, Any], out_dir: Path) -> dict[str, Any]:
    tool = stage["skill"] / stage["tool"]
    art = out_dir / stage["artifact"]
    res: dict[str, Any] = {
        "stage": stage["name"],
        "artifact": stage["artifact"],
        "purpose": stage["purpose"],
        "stub": False,
        "executed": False,
        "rc": None,
    }
    if not tool.exists():
        art.write_text(
            f"# {stage['name']} (stub)\n\nTool `{stage['tool']}` not found at `{tool}`.\n"
            f"Generated {now_iso()}.\n",
            encoding="utf-8",
        )
        res["stub"] = True
        return res
    cmd = [sys.executable, str(tool), "--demo", "--format", "markdown", "--output", str(art)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        res["executed"] = True
        res["rc"] = proc.returncode
    except Exception as exc:  # noqa: BLE001
        res["error"] = str(exc)
    return res


def evaluate_checklist(launch: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item, path in GO_NOGO_CHECKLIST:
        present: Any = None
        if path:
            ref: Any = launch
            try:
                for seg in path.split("."):
                    ref = ref[seg]
                present = ref
            except (KeyError, TypeError):
                present = None
        out.append({"item": item, "evidence_path": path, "present": present is not None})
    return out


def fmt_markdown(
    launch: dict[str, Any], checklist: list[dict[str, Any]], results: list[dict[str, Any]]
) -> str:
    lines = [
        "# Pipeline: launch-coordination",
        "",
        f"**Feature**: {launch.get('feature_name','(unspecified)')}",
        f"**Owner**: {launch.get('owner','(unspecified)')}",
        f"**Target GA**: {launch.get('target_ga_date','(unspecified)')}",
        f"**Run at**: {now_iso()}",
        "",
        "## Stage outputs",
        "",
        "| Stage | Artifact | Mode | rc |",
        "|---|---|---|---|",
    ]
    for r in results:
        mode = "stub" if r["stub"] else ("ran" if r["executed"] else "skipped")
        lines.append(f"| {r['stage']} | {r['artifact']} | {mode} | {r['rc']} |")
    lines += [
        "",
        "## Go / No-Go checklist (evidence-based)",
        "",
        "| Item | Evidence found? |",
        "|---|---|",
    ]
    for c in checklist:
        marker = "yes" if c["present"] else "no"
        lines.append(f"| {c['item']} | {marker} |")
    not_ready = [c for c in checklist if not c["present"]]
    lines += [
        "",
        f"**Readiness**: {'GO' if not not_ready else f'NOT READY ({len(not_ready)} unchecked)'}",
        "",
        "## Cross-references",
        "",
        "- execution/beta-program -- closed beta playbook",
        "- execution/feature-flag-strategy -- phased rollout + kill-switch",
        "- execution/launch-playbook -- T-minus coordination",
        "- execution/release-notes -- audience-segmented notes",
    ]
    return "\n".join(lines)


def fmt_json(
    launch: dict[str, Any], checklist: list[dict[str, Any]], results: list[dict[str, Any]]
) -> str:
    return json.dumps(
        {
            "schema": SCHEMA,
            "generated_at": now_iso(),
            "launch": launch,
            "checklist": checklist,
            "stages": results,
        },
        indent=2,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="launch-coordination pipeline.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--input", help="Path to launch JSON")
    g.add_argument("--demo", action="store_true", help="Use built-in sample launch")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", default="./pipeline-output")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.demo:
        launch = DEMO_LAUNCH
    else:
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                launch = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERROR: cannot read input: {exc}", file=sys.stderr)
            return 2

    checklist = evaluate_checklist(launch)

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "checklist.json").write_text(
        json.dumps({"checklist": checklist}, indent=2), encoding="utf-8"
    )

    results = [run_stage(stage, out_dir) for stage in STAGES]
    out = fmt_json(launch, checklist, results) if args.format == "json" else fmt_markdown(
        launch, checklist, results
    )
    (out_dir / ("summary.json" if args.format == "json" else "summary.md")).write_text(
        out + "\n", encoding="utf-8"
    )
    sys.stdout.write(out)
    if not out.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
