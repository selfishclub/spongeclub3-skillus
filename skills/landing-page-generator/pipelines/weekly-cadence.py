#!/usr/bin/env python3
"""
weekly-cadence.py -- the weekly Friday/Monday PM cadence pipeline.

Pulls Jira or Linear ticket data (via tools/adapters/), then chains:
  1. status-update-generator   (execution/status-update-generator)
  2. cycle-time-analyzer       (execution/cycle-time-analyzer/flow_metrics.py)
  3. dependency-map            (execution/dependency-map/dependency_graph.py)

Produces:
  - status.md   (Highlights / Blockers / Risks / Asks / What's Next)
  - flow.md     (cycle time, throughput, WIP, CFD)
  - deps.md     (dependency graph + critical path)
  - summary.md  (top-of-funnel for the sponsor: traffic light + 3 metrics + asks)

Usage:
    python weekly-cadence.py --demo --output ./out
    python weekly-cadence.py --input jira-export.json --source jira --output ./out
    python weekly-cadence.py --input linear-export.json --source linear --output ./out
    python weekly-cadence.py --demo --format json

Date: 2026-05-22
Standard library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


SCHEMA = "pm/pipelines/weekly-cadence/v1"
ROOT = Path(__file__).resolve().parent.parent
PM = ROOT / "project-management"

STAGES: list[dict[str, Any]] = [
    {
        "name": "status-update-generator",
        "skill": PM / "execution" / "status-update-generator",
        "tool": "scripts/status_generator.py",
        "artifact": "status.md",
        "purpose": "Weekly exec status (Highlights / Blockers / Risks / Asks / What's Next).",
    },
    {
        "name": "cycle-time-analyzer",
        "skill": PM / "execution" / "cycle-time-analyzer",
        "tool": "scripts/flow_metrics.py",
        "artifact": "flow.md",
        "purpose": "Cycle time, throughput, WIP, aging WIP, CFD.",
    },
    {
        "name": "dependency-map",
        "skill": PM / "execution" / "dependency-map",
        "tool": "scripts/dependency_graph.py",
        "artifact": "deps.md",
        "purpose": "Cross-team dependency graph + critical path.",
    },
]


# ============================================================
# Demo data: ticket-shaped JSON the adapters would produce.
# ============================================================

DEMO_TICKETS: list[dict[str, Any]] = [
    {
        "id": "PROJ-101", "title": "Bulk-edit candidates UI", "type": "story",
        "status": "in_progress", "team": "candidates",
        "created_at": "2026-05-04T09:00:00Z",
    },
    {
        "id": "PROJ-102", "title": "Bulk-edit API", "type": "story",
        "status": "blocked", "team": "platform",
        "created_at": "2026-05-04T09:30:00Z",
    },
    {
        "id": "PROJ-103", "title": "Audit-log per-candidate entry", "type": "story",
        "status": "in_progress", "team": "platform",
        "created_at": "2026-05-04T09:35:00Z",
    },
    {
        "id": "PROJ-104", "title": "Pricing-page redesign", "type": "story",
        "status": "done", "team": "growth",
        "created_at": "2026-05-01T08:00:00Z",
    },
]


# ============================================================
# Adapters (built into this script so it's stdlib-only)
# ============================================================

def adapt_jira(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Reduce a Jira export to the common ticket shape."""
    issues = payload.get("issues", payload.get("data", []))
    out: list[dict[str, Any]] = []
    for it in issues:
        fields = it.get("fields", {})
        out.append(
            {
                "id": it.get("key") or it.get("id"),
                "title": fields.get("summary", ""),
                "type": (fields.get("issuetype") or {}).get("name", "").lower(),
                "status": (fields.get("status") or {}).get("name", "").lower().replace(" ", "_"),
                "team": (fields.get("customfield_team") or fields.get("project", {}).get("key", "")),
                "created_at": fields.get("created", ""),
            }
        )
    return out


def adapt_linear(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Reduce a Linear GraphQL response to the common ticket shape."""
    nodes = (
        payload.get("data", {})
        .get("issues", {})
        .get("nodes", payload.get("issues", []))
    )
    out: list[dict[str, Any]] = []
    for it in nodes:
        out.append(
            {
                "id": it.get("identifier") or it.get("id"),
                "title": it.get("title", ""),
                "type": "story",
                "status": (it.get("state") or {}).get("name", "").lower().replace(" ", "_"),
                "team": (it.get("team") or {}).get("name", ""),
                "created_at": it.get("createdAt", ""),
            }
        )
    return out


ADAPTERS = {"jira": adapt_jira, "linear": adapt_linear}


# ============================================================
# Stage runner
# ============================================================

def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_stage(stage: dict[str, Any], out_dir: Path) -> dict[str, Any]:
    tool_path = stage["skill"] / stage["tool"]
    artifact_path = out_dir / stage["artifact"]
    res: dict[str, Any] = {
        "stage": stage["name"],
        "artifact": stage["artifact"],
        "purpose": stage["purpose"],
        "executed": False,
        "stub": False,
        "rc": None,
    }
    if not tool_path.exists():
        artifact_path.write_text(
            f"# {stage['name']} (stub)\n\n"
            f"Tool `{stage['tool']}` not present at `{tool_path}`.\n"
            f"Generated stub at {now_iso()}.\n",
            encoding="utf-8",
        )
        res["stub"] = True
        return res
    cmd = [
        sys.executable,
        str(tool_path),
        "--demo",
        "--format",
        "markdown",
        "--output",
        str(artifact_path),
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        res["executed"] = True
        res["rc"] = proc.returncode
    except Exception as exc:  # noqa: BLE001
        res["error"] = str(exc)
    return res


# ============================================================
# Summary
# ============================================================

def summarize_tickets(tickets: list[dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for t in tickets:
        counts[t.get("status", "unknown")] = counts.get(t.get("status", "unknown"), 0) + 1
    blocked = counts.get("blocked", 0)
    in_progress = counts.get("in_progress", 0)
    done = counts.get("done", 0)
    traffic = "green"
    if blocked >= 2:
        traffic = "red"
    elif blocked == 1 or in_progress > done * 3:
        traffic = "yellow"
    return {
        "total": len(tickets),
        "by_status": counts,
        "traffic_light": traffic,
    }


def fmt_markdown(ctx: dict[str, Any], results: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    lines = [
        "# Pipeline: weekly-cadence",
        "",
        f"**Source**: {ctx.get('source','demo')}",
        f"**Tickets**: {summary['total']}",
        f"**Traffic light (derived)**: {summary['traffic_light'].upper()}",
        f"**Run at**: {now_iso()}",
        "",
        "## Status counts",
        "",
    ]
    for status, count in sorted(summary["by_status"].items()):
        lines.append(f"- {status}: {count}")
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
        "- execution/status-update-generator -- weekly status",
        "- execution/cycle-time-analyzer -- flow metrics",
        "- execution/dependency-map -- cross-team graph",
        "",
        "See each skill's `references/red-flags.md` for usage patterns.",
    ]
    return "\n".join(lines)


def fmt_json(ctx: dict[str, Any], results: list[dict[str, Any]], summary: dict[str, Any]) -> str:
    return json.dumps(
        {
            "schema": SCHEMA,
            "generated_at": now_iso(),
            "context": ctx,
            "summary": summary,
            "stages": results,
        },
        indent=2,
    )


# ============================================================
# CLI
# ============================================================

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="weekly-cadence pipeline.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--input", help="Path to Jira/Linear export JSON")
    g.add_argument("--demo", action="store_true", help="Use built-in demo data")
    p.add_argument(
        "--source",
        choices=["jira", "linear", "demo"],
        default="demo",
        help="Adapter to use for --input",
    )
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", default="./pipeline-output", help="Output directory")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.demo:
        tickets = DEMO_TICKETS
        ctx = {"source": "demo", "tickets_count": len(tickets)}
    else:
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                payload = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERROR: cannot read input: {exc}", file=sys.stderr)
            return 2
        adapter = ADAPTERS.get(args.source)
        if adapter is None:
            print(f"ERROR: --source {args.source} requires --input + adapter", file=sys.stderr)
            return 2
        tickets = adapter(payload)
        ctx = {"source": args.source, "tickets_count": len(tickets)}

    summary = summarize_tickets(tickets)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Persist the adapted ticket list as a shared input for the stages.
    (out_dir / "tickets.json").write_text(
        json.dumps({"tickets": tickets}, indent=2), encoding="utf-8"
    )

    results = [run_stage(stage, out_dir) for stage in STAGES]

    out = fmt_json(ctx, results, summary) if args.format == "json" else fmt_markdown(
        ctx, results, summary
    )
    name = "summary.json" if args.format == "json" else "summary.md"
    (out_dir / name).write_text(out + "\n", encoding="utf-8")
    sys.stdout.write(out)
    if not out.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
