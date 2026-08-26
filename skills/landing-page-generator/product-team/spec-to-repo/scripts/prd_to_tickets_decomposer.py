#!/usr/bin/env python3
"""
prd_to_tickets_decomposer.py — Decompose a PRD into a candidate ticket tree
with size estimates, dependencies, and decomposition health checks.

Reads a JSON describing the PRD as: user_capabilities + technical_notes +
team. Produces an Epic → Story → Ticket tree, flags oversized items,
identifies cross-team dependencies, and emits sequence recommendations.

Stdlib only. JSON or markdown output.

Usage:
    python3 prd_to_tickets_decomposer.py --input prd.json
    python3 prd_to_tickets_decomposer.py --input prd.json --format markdown

Input schema:
{
  "epic_name": "Notifications v2",
  "ship_target": "2026-07-15",
  "team": {"backend": 2, "frontend": 2, "infra": 1},
  "user_capabilities": [
      {
          "id": "C-001",
          "story": "As a user, I can mute notifications by channel",
          "components_touched": ["backend", "frontend"],
          "estimated_days": 4,
          "feature_flag_required": true,
          "cross_team_dependencies": [],
          "telemetry_events_added": 2,
          "docs_required": true,
          "tests_required": true
      }
  ],
  "technical_notes": [
      {
          "id": "T-001",
          "description": "Database migration to add notification_preferences table",
          "blocking_for_capabilities": ["C-001","C-002"],
          "estimated_days": 1,
          "type": "scaffolding"        # scaffolding|telemetry|infra|rollout|docs
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


@dataclass
class Ticket:
    id: str
    parent: str
    title: str
    component: str
    type: str
    estimated_days: float
    notes: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)


def decompose_capability(cap: dict[str, Any]) -> list[Ticket]:
    cap_id = cap.get("id", "C-?")
    story = cap.get("story", "")
    components = list(cap.get("components_touched", []) or [])
    days = float(cap.get("estimated_days", 0) or 0)
    tickets: list[Ticket] = []
    seq = 0

    def next_id(suffix: str) -> str:
        nonlocal seq
        seq += 1
        return f"{cap_id}-{seq:02d}-{suffix}"

    per_component_days = days / max(1, len(components))

    for comp in components:
        seq_id = next_id(comp[:3])
        notes = []
        flags = []
        if per_component_days > 3:
            flags.append(f"size:L — {per_component_days:.1f} days; consider splitting")
        elif per_component_days > 5:
            flags.append(f"size:XL — {per_component_days:.1f} days; MUST split")
        if not cap.get("tests_required", False):
            flags.append("tests not declared")
        tickets.append(Ticket(
            id=seq_id, parent=cap_id, title=f"[{comp}] {story[:60]}",
            component=comp, type="story",
            estimated_days=per_component_days, notes=notes, flags=flags,
        ))

    if cap.get("telemetry_events_added", 0) > 0:
        tickets.append(Ticket(
            id=next_id("tel"), parent=cap_id,
            title=f"[telemetry] {cap.get('telemetry_events_added',0)} events for {story[:40]}",
            component="telemetry", type="telemetry",
            estimated_days=0.5,
        ))

    if cap.get("docs_required"):
        tickets.append(Ticket(
            id=next_id("doc"), parent=cap_id,
            title=f"[docs] User-facing docs for {story[:40]}",
            component="docs", type="docs", estimated_days=0.5,
        ))

    if cap.get("feature_flag_required"):
        tickets.append(Ticket(
            id=next_id("flag"), parent=cap_id,
            title=f"[flag] Enable flag for {story[:40]}",
            component="rollout", type="rollout", estimated_days=0.5,
            notes=["enable AFTER all story tickets merged + telemetry verified"],
        ))

    return tickets


def decompose_technical(tech: dict[str, Any]) -> Ticket:
    return Ticket(
        id=tech.get("id", "T-?"),
        parent="",
        title=tech.get("description", "")[:80],
        component="infra",
        type=tech.get("type", "scaffolding"),
        estimated_days=float(tech.get("estimated_days", 0) or 0),
        notes=[],
    )


def sequence_recommendation(
    technical: list[Ticket],
    cap_tickets_by_cap: dict[str, list[Ticket]],
    capabilities: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    seq: list[dict[str, Any]] = []
    # Scaffolding first
    for t in technical:
        if t.type == "scaffolding":
            seq.append({"step": len(seq) + 1, "ticket": t.id, "reason": "scaffolding (no behavior change)"})
    # Then capability stories
    for cap in capabilities:
        cap_id = cap.get("id", "")
        for t in cap_tickets_by_cap.get(cap_id, []):
            if t.type == "story":
                seq.append({"step": len(seq) + 1, "ticket": t.id, "reason": "behind feature flag"})
    # Then telemetry
    for cap in capabilities:
        cap_id = cap.get("id", "")
        for t in cap_tickets_by_cap.get(cap_id, []):
            if t.type == "telemetry":
                seq.append({"step": len(seq) + 1, "ticket": t.id, "reason": "telemetry"})
    # Then docs
    for cap in capabilities:
        cap_id = cap.get("id", "")
        for t in cap_tickets_by_cap.get(cap_id, []):
            if t.type == "docs":
                seq.append({"step": len(seq) + 1, "ticket": t.id, "reason": "documentation"})
    # Then rollout (flags)
    for cap in capabilities:
        cap_id = cap.get("id", "")
        for t in cap_tickets_by_cap.get(cap_id, []):
            if t.type == "rollout":
                seq.append({"step": len(seq) + 1, "ticket": t.id, "reason": "flag enablement"})
    return seq


def cross_team_warnings(capabilities: list[dict[str, Any]]) -> list[dict[str, Any]]:
    warnings = []
    for cap in capabilities:
        deps = cap.get("cross_team_dependencies", []) or []
        for d in deps:
            warnings.append({
                "capability_id": cap.get("id", ""),
                "dependency": d,
                "action": "create explicit coordination ticket BEFORE sprint start",
            })
    return warnings


def decompose(prd: dict[str, Any]) -> dict[str, Any]:
    capabilities = prd.get("user_capabilities", []) or []
    technical = prd.get("technical_notes", []) or []

    technical_tickets = [decompose_technical(t) for t in technical]
    cap_tickets_by_cap: dict[str, list[Ticket]] = {}
    all_cap_tickets: list[Ticket] = []
    for cap in capabilities:
        tt = decompose_capability(cap)
        cap_tickets_by_cap[cap.get("id", "")] = tt
        all_cap_tickets.extend(tt)

    sequence = sequence_recommendation(technical_tickets, cap_tickets_by_cap, capabilities)
    warnings = cross_team_warnings(capabilities)

    all_tickets = technical_tickets + all_cap_tickets
    total_days = sum(t.estimated_days for t in all_tickets)
    oversized = [t for t in all_tickets if t.estimated_days > 3]

    return {
        "epic_name": prd.get("epic_name", ""),
        "ship_target": prd.get("ship_target", ""),
        "team": prd.get("team", {}),
        "summary": {
            "total_tickets": len(all_tickets),
            "total_estimated_days": round(total_days, 1),
            "oversized_count": len(oversized),
        },
        "tickets": [
            {
                "id": t.id, "parent": t.parent, "title": t.title,
                "component": t.component, "type": t.type,
                "estimated_days": round(t.estimated_days, 1),
                "notes": t.notes, "flags": t.flags,
            }
            for t in all_tickets
        ],
        "sequence_recommendation": sequence,
        "cross_team_warnings": warnings,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Ticket Decomposition — {report.get('epic_name','(epic)')}")
    lines.append(f"_ship target: {report.get('ship_target','(unset)')}_\n")
    s = report["summary"]
    lines.append(f"## Summary: {s['total_tickets']} tickets, "
                f"~{s['total_estimated_days']} engineer-days, "
                f"{s['oversized_count']} oversized\n")
    lines.append("## Tickets")
    lines.append("| ID | Type | Component | Title | Days | Flags |")
    lines.append("|----|------|-----------|-------|------|-------|")
    for t in report["tickets"]:
        lines.append(f"| {t['id']} | {t['type']} | {t['component']} | {t['title']} | "
                    f"{t['estimated_days']} | {', '.join(t['flags']) or '—'} |")
    lines.append("")
    lines.append("## Sequence recommendation")
    for s in report["sequence_recommendation"]:
        lines.append(f"{s['step']}. {s['ticket']} — {s['reason']}")
    lines.append("")
    if report["cross_team_warnings"]:
        lines.append("## Cross-team coordination needed")
        for w in report["cross_team_warnings"]:
            lines.append(f"- {w['capability_id']} depends on {w['dependency']}: {w['action']}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Decompose a PRD into a ticket tree",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON describing the PRD")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--output", help="Write to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        prd = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"error: cannot read input: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 2

    report = decompose(prd)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
