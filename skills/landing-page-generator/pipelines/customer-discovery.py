#!/usr/bin/env python3
"""
customer-discovery.py -- discovery flow from interview to north-star metric.

Pipeline stages:
  1. interview-synthesis        (discovery/interview-synthesis)   -> opportunity tree
  2. identify-assumptions       (discovery/identify-assumptions)  -> assumption map
  3. brainstorm-experiments     (discovery/brainstorm-experiments) -> experiment plan
  4. north-star-metric          (execution/north-star-metric)     -> NSM tree

Reads an interviews JSON; produces four artifacts (one per stage) plus a
summary connecting them.

Usage:
    python customer-discovery.py --demo --output ./out
    python customer-discovery.py --input interviews.json --output ./out
    python customer-discovery.py --demo --format json

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


SCHEMA = "pm/pipelines/customer-discovery/v1"
ROOT = Path(__file__).resolve().parent.parent
PM = ROOT / "project-management"


STAGES: list[dict[str, Any]] = [
    {
        "name": "interview-synthesis",
        "skill": PM / "discovery" / "interview-synthesis",
        "tool": "scripts/interview_synthesizer.py",
        "artifact": "01-opportunity-tree.md",
        "purpose": "Cluster interview signals into Torres-style opportunity solution tree.",
    },
    {
        "name": "identify-assumptions",
        "skill": PM / "discovery" / "identify-assumptions",
        "tool": "scripts/assumption_tracker.py",
        "artifact": "02-assumption-map.md",
        "purpose": "Map assumptions across 4-8 risk categories with Impact x Risk scoring.",
    },
    {
        "name": "brainstorm-experiments",
        "skill": PM / "discovery" / "brainstorm-experiments",
        "tool": "scripts/experiment_designer.py",
        "artifact": "03-experiment-plan.md",
        "purpose": "Design lean experiments against the highest-risk assumptions.",
    },
    {
        "name": "north-star-metric",
        "skill": PM / "execution" / "north-star-metric",
        "tool": "scripts/metric_tree_builder.py",
        "artifact": "04-nsm-tree.md",
        "purpose": "Operationalize the chosen opportunity into NSM + input metric tree.",
    },
]


DEMO_INTERVIEWS: dict[str, Any] = {
    "study_name": "Recruiter Discovery Q2 2026",
    "interviews": [
        {
            "id": "INT-001",
            "persona": "enterprise recruiter",
            "company_size": "500-2000",
            "quotes": [
                "I edit 30+ candidates a day; most are the same change.",
                "I'd pay extra not to do this one at a time.",
                "When I bulk-import I lose the tags I set manually.",
            ],
            "jobs_to_be_done": ["update candidate state quickly", "preserve manually-added tags"],
        },
        {
            "id": "INT-002",
            "persona": "agency recruiter",
            "company_size": "10-50",
            "quotes": [
                "I work across 4 clients; I need to keep their data separate.",
                "I do not need bulk-edit but I do need bulk-export.",
            ],
            "jobs_to_be_done": ["keep client data isolated", "bulk export to client tool"],
        },
        {
            "id": "INT-003",
            "persona": "high-volume sourcer",
            "company_size": "200-500",
            "quotes": [
                "Selecting 20 candidates is painful: no shift-click, no select-all.",
                "If I have to scroll, I lose my selection.",
            ],
            "jobs_to_be_done": ["select many candidates without losing scroll state"],
        },
    ],
}


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
            f"Replace with real tool output. Generated {now_iso()}.\n",
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


def derive_opportunities(interviews: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Cluster JTBD strings across interviews to surface candidate opportunities."""
    counts: dict[str, list[str]] = {}
    for i in interviews:
        for j in i.get("jobs_to_be_done", []):
            key = j.strip().lower()
            counts.setdefault(key, []).append(i["id"])
    opps = [
        {"opportunity": k, "evidence_count": len(v), "interviews": v}
        for k, v in counts.items()
    ]
    opps.sort(key=lambda o: o["evidence_count"], reverse=True)
    return opps


def fmt_markdown(
    ctx: dict[str, Any], opps: list[dict[str, Any]], results: list[dict[str, Any]]
) -> str:
    lines = [
        "# Pipeline: customer-discovery",
        "",
        f"**Study**: {ctx.get('study_name','(unspecified)')}",
        f"**Interviews**: {ctx.get('interview_count', 0)}",
        f"**Run at**: {now_iso()}",
        "",
        "## Top opportunities (clustered from JTBD)",
        "",
        "| Rank | Opportunity | Evidence | Interviews |",
        "|---|---|---|---|",
    ]
    for r, o in enumerate(opps[:8], 1):
        lines.append(
            f"| {r} | {o['opportunity']} | {o['evidence_count']} | {', '.join(o['interviews'])} |"
        )
    lines += [
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
        "## Cross-references",
        "",
        "- discovery/interview-synthesis -- opportunity tree",
        "- discovery/identify-assumptions -- assumption map",
        "- discovery/brainstorm-experiments -- experiment plan",
        "- execution/north-star-metric -- NSM tree",
    ]
    return "\n".join(lines)


def fmt_json(
    ctx: dict[str, Any], opps: list[dict[str, Any]], results: list[dict[str, Any]]
) -> str:
    return json.dumps(
        {
            "schema": SCHEMA,
            "generated_at": now_iso(),
            "context": ctx,
            "opportunities": opps,
            "stages": results,
        },
        indent=2,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="customer-discovery pipeline.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--input", help="Path to interviews JSON")
    g.add_argument("--demo", action="store_true", help="Use built-in sample interviews")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", default="./pipeline-output")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.demo:
        data = DEMO_INTERVIEWS
    else:
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERROR: cannot read input: {exc}", file=sys.stderr)
            return 2

    interviews = data.get("interviews", [])
    ctx = {
        "study_name": data.get("study_name", "(unspecified)"),
        "interview_count": len(interviews),
    }
    opps = derive_opportunities(interviews)

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "opportunities.json").write_text(
        json.dumps({"opportunities": opps}, indent=2), encoding="utf-8"
    )

    results = [run_stage(stage, out_dir) for stage in STAGES]
    out = fmt_json(ctx, opps, results) if args.format == "json" else fmt_markdown(
        ctx, opps, results
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
