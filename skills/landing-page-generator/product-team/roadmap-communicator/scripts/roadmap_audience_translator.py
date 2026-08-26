#!/usr/bin/env python3
"""
roadmap_audience_translator.py — Translate a master roadmap into
audience-appropriate format.

Reads a JSON master roadmap (themes + initiatives + confidence bands)
and an audience tag; produces a tailored output for that audience.

Stdlib only. JSON or markdown output.

Usage:
    python3 roadmap_audience_translator.py --input roadmap.json --audience customer
    python3 roadmap_audience_translator.py --input roadmap.json --audience board --format markdown

Audiences: board, customer, sales, engineering, partner, internal

Input schema:
{
  "as_of": "2026-05-27",
  "company": "Acme",
  "quarter": "Q3-2026",
  "themes": [
      {
          "name": "Better collaboration",
          "outcome_metric": "Multi-user file editing rate",
          "rationale": "Customer-validated as top differentiator",
          "initiatives": [
              {
                  "name": "Real-time editing",
                  "outcome": "Multiple users can edit a file simultaneously",
                  "ship_window": "Now",
                  "confidence": "commit",
                  "target_date": "2026-06-15",
                  "internal_feature_name": "WS-edit-v2",
                  "ticket_id": "PROJ-1234",
                  "customer_visible": true,
                  "api_change": false
              }
          ]
      }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


WINDOW_ORDER = {"Now": 0, "Next": 1, "Later": 2}


def visible_initiatives(theme: dict[str, Any], audience: str) -> list[dict[str, Any]]:
    """Filter initiatives appropriate for audience."""
    inits = theme.get("initiatives", []) or []
    out = []
    for i in inits:
        if audience == "customer" and not i.get("customer_visible", True):
            continue
        if audience == "partner" and not i.get("api_change", False) and not i.get("partner_relevant", False):
            continue
        if audience == "sales" and not i.get("customer_visible", True):
            continue
        out.append(i)
    return out


def render_board(roadmap: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Product Roadmap — {roadmap.get('company','')} {roadmap.get('quarter','')}\n")
    lines.append("## Strategic themes")
    for t in roadmap.get("themes", []):
        outcome = t.get("outcome_metric", "")
        lines.append(f"\n### {t.get('name','')}")
        if outcome:
            lines.append(f"_KPI: {outcome}_")
        rationale = t.get("rationale", "")
        if rationale:
            lines.append(f"\n**Why:** {rationale}")
        lines.append("\n**Initiatives:**")
        for i in t.get("initiatives", []):
            conf = i.get("confidence", "")
            window = i.get("ship_window", "")
            lines.append(f"- {i.get('outcome', i.get('name',''))} — *{conf}*, {window}")
    lines.append("")
    return "\n".join(lines)


def render_customer(roadmap: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# What's Coming in {roadmap.get('company','')}\n")
    lines.append("_We update this regularly. Have a request? Reach out to your account team._\n")
    by_window: dict[str, list[str]] = {"Now": [], "Next": [], "Later": []}
    for t in roadmap.get("themes", []):
        for i in visible_initiatives(t, "customer"):
            window = i.get("ship_window", "Later")
            line = f"- **{i.get('outcome', i.get('name',''))}** — {t.get('name','')}"
            by_window.setdefault(window, []).append(line)
    for window in ("Now", "Next", "Later"):
        items = by_window.get(window, [])
        if not items:
            continue
        label = {"Now": "Now shipping", "Next": "In development",
                "Later": "Exploring"}[window]
        lines.append(f"\n## {label}")
        for it in items:
            lines.append(it)
    lines.append("")
    return "\n".join(lines)


def render_sales(roadmap: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Sales-Facing Roadmap — {roadmap.get('quarter','')}\n")
    lines.append("## What you CAN promise (confidence: commit, Now)")
    for t in roadmap.get("themes", []):
        for i in visible_initiatives(t, "sales"):
            if i.get("confidence") == "commit" and i.get("ship_window") == "Now":
                lines.append(f"- **{i.get('outcome', i.get('name',''))}** "
                            f"({t.get('name','')}) — target {i.get('target_date','TBD')}")
    lines.append("\n## What you can mention with caveats (plan, Next)")
    for t in roadmap.get("themes", []):
        for i in visible_initiatives(t, "sales"):
            if i.get("confidence") == "plan" and i.get("ship_window") == "Next":
                lines.append(f"- {i.get('outcome', i.get('name',''))} "
                            f"({t.get('name','')}) — planning {i.get('target_date','TBD')}")
    lines.append("\n## DO NOT commit to customers (aspire, Later)")
    for t in roadmap.get("themes", []):
        for i in visible_initiatives(t, "sales"):
            if i.get("confidence") in ("aspire", "strategic"):
                lines.append(f"- {i.get('outcome', i.get('name',''))} "
                            f"({t.get('name','')}) — exploring; no commit")
    lines.append("")
    return "\n".join(lines)


def render_engineering(roadmap: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Engineering Roadmap — {roadmap.get('quarter','')}\n")
    for t in roadmap.get("themes", []):
        outcome = t.get("outcome_metric", "")
        lines.append(f"## Theme: {t.get('name','')}")
        if outcome:
            lines.append(f"_Outcome metric: {outcome}_")
        for i in t.get("initiatives", []):
            internal_name = i.get("internal_feature_name", i.get("name", ""))
            ticket = i.get("ticket_id", "")
            conf = i.get("confidence", "")
            window = i.get("ship_window", "")
            target = i.get("target_date", "")
            lines.append(f"\n### {internal_name}")
            lines.append(f"- Status: *{conf}*, ship window: {window}, target: {target}")
            if ticket:
                lines.append(f"- Ticket: {ticket}")
            if i.get("outcome"):
                lines.append(f"- User outcome: {i.get('outcome')}")
    lines.append("")
    return "\n".join(lines)


def render_partner(roadmap: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Partner Roadmap — {roadmap.get('quarter','')}\n")
    lines.append("## API + integration-relevant changes")
    found = False
    for t in roadmap.get("themes", []):
        for i in visible_initiatives(t, "partner"):
            found = True
            lines.append(f"- **{i.get('outcome', i.get('name',''))}** "
                        f"({t.get('name','')}, {i.get('ship_window','')}, *{i.get('confidence','')}*)")
    if not found:
        lines.append("_No API or integration-relevant changes this quarter._")
    lines.append("")
    return "\n".join(lines)


def render_internal(roadmap: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Company-Wide Roadmap — {roadmap.get('quarter','')}\n")
    for t in roadmap.get("themes", []):
        lines.append(f"## {t.get('name','')}")
        rationale = t.get("rationale", "")
        if rationale:
            lines.append(f"_{rationale}_")
        for i in t.get("initiatives", []):
            lines.append(f"- {i.get('outcome', i.get('name',''))} — "
                        f"*{i.get('confidence','')}*, {i.get('ship_window','')}")
    lines.append("")
    return "\n".join(lines)


RENDERERS = {
    "board": render_board,
    "customer": render_customer,
    "sales": render_sales,
    "engineering": render_engineering,
    "partner": render_partner,
    "internal": render_internal,
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Translate roadmap for a specific audience",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON master roadmap")
    p.add_argument("--audience", required=True,
                  choices=["board", "customer", "sales", "engineering", "partner", "internal"])
    p.add_argument("--format", choices=["json", "markdown"], default="markdown")
    p.add_argument("--output", help="Write to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        roadmap = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"error: cannot read input: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 2

    renderer = RENDERERS[args.audience]
    md = renderer(roadmap)

    if args.format == "json":
        out = json.dumps({"audience": args.audience, "markdown": md}, indent=2)
    else:
        out = md

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
