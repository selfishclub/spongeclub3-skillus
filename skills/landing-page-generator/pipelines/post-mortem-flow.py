#!/usr/bin/env python3
"""
post-mortem-flow.py -- given an incident JSON, run a blameless post-mortem
and create follow-up Risk items via the pre-mortem framework.

Pipeline stages:
  1. post-mortem      (execution/post-mortem)        -> fill the post-mortem template
  2. pre-mortem       (discovery/pre-mortem)         -> classify follow-up risks
                                                       (Tiger / Paper Tiger / Elephant)
  3. dependency-map   (execution/dependency-map)     -> capture inter-team mitigations

Outputs:
  - 01-post-mortem.md
  - 02-followup-risks.md
  - 03-cross-team-mitigations.md
  - summary.md / summary.json

Usage:
    python post-mortem-flow.py --demo --output ./out
    python post-mortem-flow.py --input incident.json --output ./out

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


SCHEMA = "pm/pipelines/post-mortem-flow/v1"
ROOT = Path(__file__).resolve().parent.parent
PM = ROOT / "project-management"


STAGES: list[dict[str, Any]] = [
    {
        "name": "post-mortem",
        "skill": PM / "execution" / "post-mortem",
        "tool": "scripts/postmortem_scaffolder.py",
        "artifact": "01-post-mortem.md",
        "purpose": "Blameless incident RCA (Google SRE, Allspaw, Dekker patterns).",
    },
    {
        "name": "pre-mortem",
        "skill": PM / "discovery" / "pre-mortem",
        "tool": "scripts/risk_categorizer.py",
        "artifact": "02-followup-risks.md",
        "purpose": "Classify follow-up risks: Tiger / Paper Tiger / Elephant.",
    },
    {
        "name": "dependency-map",
        "skill": PM / "execution" / "dependency-map",
        "tool": "scripts/dependency_graph.py",
        "artifact": "03-cross-team-mitigations.md",
        "purpose": "Capture cross-team mitigations + critical path of fixes.",
    },
]


DEMO_INCIDENT: dict[str, Any] = {
    "incident_id": "INC-2026-0319",
    "title": "Database connection pool exhaustion during peak (Friday Mar 19)",
    "severity": "SEV-2",
    "started_at": "2026-03-19T14:22:00Z",
    "detected_at": "2026-03-19T14:31:00Z",
    "resolved_at": "2026-03-19T16:08:00Z",
    "customer_impact": "~3,400 users saw 5xx errors over 106 minutes; ~8% p99 latency degradation.",
    "summary": (
        "A traffic spike combined with a slow background job exhausted the "
        "Postgres connection pool. New requests waited indefinitely; circuit "
        "breaker did not trip because timeouts were configured to 0."
    ),
    "timeline": [
        {"at": "14:22Z", "event": "Latency p99 jumps to 4s"},
        {"at": "14:31Z", "event": "PagerDuty fires for SLO breach"},
        {"at": "14:45Z", "event": "On-call narrows to DB pool exhaustion"},
        {"at": "15:20Z", "event": "Increase pool size from 50 to 200; symptoms ease"},
        {"at": "16:08Z", "event": "Background job paused; service returns to baseline"},
    ],
    "contributing_factors": [
        "Background job lacks query timeout",
        "Connection pool tuned for last year's traffic",
        "Circuit breaker timeout misconfigured to 0",
        "Runbook for pool exhaustion is 18 months old",
    ],
    "action_items": [
        {"action": "Add per-query timeouts to background job framework", "owner": "platform", "due": "2026-04-02"},
        {"action": "Re-tune connection pool against current peak traffic", "owner": "platform", "due": "2026-03-26"},
        {"action": "Audit circuit-breaker config across services", "owner": "infra", "due": "2026-04-09"},
        {"action": "Refresh pool-exhaustion runbook + run a game-day", "owner": "sre", "due": "2026-04-16"},
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


def derive_followup_risks(incident: dict[str, Any]) -> list[dict[str, Any]]:
    """Turn contributing factors into pre-mortem-style risk records."""
    risks: list[dict[str, Any]] = []
    for f in incident.get("contributing_factors", []):
        # Heuristic classification: timeouts/circuit-breakers/runbook -> Tiger
        # (likely + high impact); pool tuning -> Paper Tiger (looks scary,
        # easy to mitigate).
        low = f.lower()
        if "timeout" in low or "circuit" in low or "runbook" in low:
            classification = "Tiger"
        elif "pool" in low or "tune" in low:
            classification = "Paper Tiger"
        else:
            classification = "Elephant"
        risks.append(
            {
                "risk": f,
                "classification": classification,
                "mitigation": "see action item",
                "owner": None,
                "tripwire": "next traffic peak",
            }
        )
    return risks


def fmt_markdown(
    incident: dict[str, Any], risks: list[dict[str, Any]], results: list[dict[str, Any]]
) -> str:
    lines = [
        "# Pipeline: post-mortem-flow",
        "",
        f"**Incident**: {incident.get('incident_id','(unknown)')} -- {incident.get('title','(no title)')}",
        f"**Severity**: {incident.get('severity','(unknown)')}",
        f"**Duration**: {incident.get('started_at','?')} -> {incident.get('resolved_at','?')}",
        f"**Customer impact**: {incident.get('customer_impact','(unknown)')}",
        f"**Run at**: {now_iso()}",
        "",
        "## Follow-up risks (pre-mortem framing)",
        "",
        "| Risk | Classification | Tripwire |",
        "|---|---|---|",
    ]
    for r in risks:
        lines.append(f"| {r['risk']} | {r['classification']} | {r['tripwire']} |")
    lines += [
        "",
        "## Action items",
        "",
    ]
    for a in incident.get("action_items", []):
        lines.append(
            f"- {a.get('action','(no action)')} -- owner: {a.get('owner','?')}, due: {a.get('due','?')}"
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
        "- execution/post-mortem -- the blameless RCA template",
        "- discovery/pre-mortem -- Tiger / Paper Tiger / Elephant",
        "- execution/dependency-map -- cross-team mitigations",
    ]
    return "\n".join(lines)


def fmt_json(
    incident: dict[str, Any], risks: list[dict[str, Any]], results: list[dict[str, Any]]
) -> str:
    return json.dumps(
        {
            "schema": SCHEMA,
            "generated_at": now_iso(),
            "incident": incident,
            "followup_risks": risks,
            "stages": results,
        },
        indent=2,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="post-mortem-flow pipeline.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--input", help="Path to incident JSON")
    g.add_argument("--demo", action="store_true", help="Use built-in sample incident")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", default="./pipeline-output")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.demo:
        incident = DEMO_INCIDENT
    else:
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                incident = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERROR: cannot read input: {exc}", file=sys.stderr)
            return 2

    risks = derive_followup_risks(incident)

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "followup-risks.json").write_text(
        json.dumps({"risks": risks}, indent=2), encoding="utf-8"
    )

    results = [run_stage(stage, out_dir) for stage in STAGES]
    out = fmt_json(incident, risks, results) if args.format == "json" else fmt_markdown(
        incident, risks, results
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
