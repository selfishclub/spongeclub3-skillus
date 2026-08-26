#!/usr/bin/env python3
"""
roadmap_diff_reporter.py — Compute the diff between two roadmap snapshots
and generate a what-changed memo.

Reads two roadmap JSONs (previous + current) of the same shape used by
roadmap_audience_translator.py; identifies added, removed, slipped,
re-prioritized, confidence-changed items; emits diff memo.

Stdlib only. JSON or markdown output.

Usage:
    python3 roadmap_diff_reporter.py --previous q1.json --current q2.json
    python3 roadmap_diff_reporter.py --previous q1.json --current q2.json --format markdown
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def index_initiatives(roadmap: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Index by initiative name (with theme as fallback for disambiguation)."""
    idx: dict[str, dict[str, Any]] = {}
    for theme in roadmap.get("themes", []) or []:
        theme_name = theme.get("name", "")
        for i in theme.get("initiatives", []) or []:
            key = f"{theme_name}::{i.get('name','')}"
            i_copy = dict(i)
            i_copy["_theme"] = theme_name
            idx[key] = i_copy
    return idx


def diff(prev: dict[str, Any], curr: dict[str, Any]) -> dict[str, Any]:
    prev_idx = index_initiatives(prev)
    curr_idx = index_initiatives(curr)
    prev_keys = set(prev_idx.keys())
    curr_keys = set(curr_idx.keys())

    added = []
    removed = []
    slipped = []
    accelerated = []
    confidence_changed = []
    scope_changed = []

    for key in curr_keys - prev_keys:
        i = curr_idx[key]
        added.append({
            "theme": i["_theme"],
            "name": i.get("name", ""),
            "confidence": i.get("confidence", ""),
            "ship_window": i.get("ship_window", ""),
            "target_date": i.get("target_date", ""),
        })

    for key in prev_keys - curr_keys:
        i = prev_idx[key]
        removed.append({
            "theme": i["_theme"],
            "name": i.get("name", ""),
            "previous_confidence": i.get("confidence", ""),
            "previous_target": i.get("target_date", ""),
        })

    for key in prev_keys & curr_keys:
        p = prev_idx[key]
        c = curr_idx[key]
        p_target = p.get("target_date", "")
        c_target = c.get("target_date", "")
        if p_target and c_target and p_target != c_target:
            if c_target > p_target:
                slipped.append({
                    "theme": c["_theme"],
                    "name": c.get("name", ""),
                    "from_date": p_target,
                    "to_date": c_target,
                })
            else:
                accelerated.append({
                    "theme": c["_theme"],
                    "name": c.get("name", ""),
                    "from_date": p_target,
                    "to_date": c_target,
                })

        if p.get("confidence") != c.get("confidence"):
            confidence_changed.append({
                "theme": c["_theme"],
                "name": c.get("name", ""),
                "from_confidence": p.get("confidence", ""),
                "to_confidence": c.get("confidence", ""),
            })

        if p.get("ship_window") != c.get("ship_window"):
            scope_changed.append({
                "theme": c["_theme"],
                "name": c.get("name", ""),
                "from_window": p.get("ship_window", ""),
                "to_window": c.get("ship_window", ""),
            })

    return {
        "previous_quarter": prev.get("quarter", ""),
        "current_quarter": curr.get("quarter", ""),
        "added": added,
        "removed": removed,
        "slipped": slipped,
        "accelerated": accelerated,
        "confidence_changed": confidence_changed,
        "ship_window_changed": scope_changed,
        "summary": {
            "added_count": len(added),
            "removed_count": len(removed),
            "slipped_count": len(slipped),
            "accelerated_count": len(accelerated),
            "confidence_changes_count": len(confidence_changed),
            "ship_window_changes_count": len(scope_changed),
        },
    }


def render_markdown(d: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Roadmap Diff — {d.get('previous_quarter','')} → {d.get('current_quarter','')}\n")
    s = d["summary"]
    lines.append("## Summary")
    lines.append(f"- Added: {s['added_count']}")
    lines.append(f"- Removed: {s['removed_count']}")
    lines.append(f"- Slipped: {s['slipped_count']}")
    lines.append(f"- Accelerated: {s['accelerated_count']}")
    lines.append(f"- Confidence changes: {s['confidence_changes_count']}")
    lines.append(f"- Ship-window changes: {s['ship_window_changes_count']}")
    lines.append("")

    if d["added"]:
        lines.append("## Added")
        for i in d["added"]:
            lines.append(f"- **{i['name']}** ({i['theme']}) — {i['confidence']}, {i['ship_window']}, target {i['target_date'] or 'TBD'}")
        lines.append("")
    if d["removed"]:
        lines.append("## Removed")
        for i in d["removed"]:
            lines.append(f"- {i['name']} ({i['theme']}) — was {i['previous_confidence']}, target {i['previous_target']}")
        lines.append("")
    if d["slipped"]:
        lines.append("## Slipped (later than before)")
        for i in d["slipped"]:
            lines.append(f"- {i['name']} ({i['theme']}): {i['from_date']} → {i['to_date']}")
        lines.append("")
    if d["accelerated"]:
        lines.append("## Accelerated")
        for i in d["accelerated"]:
            lines.append(f"- {i['name']} ({i['theme']}): {i['from_date']} → {i['to_date']}")
        lines.append("")
    if d["confidence_changed"]:
        lines.append("## Confidence changed")
        for i in d["confidence_changed"]:
            lines.append(f"- {i['name']} ({i['theme']}): {i['from_confidence']} → {i['to_confidence']}")
        lines.append("")
    if d["ship_window_changed"]:
        lines.append("## Ship window changed")
        for i in d["ship_window_changed"]:
            lines.append(f"- {i['name']} ({i['theme']}): {i['from_window']} → {i['to_window']}")
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Compute roadmap diff between two snapshots",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--previous", required=True, help="Previous roadmap JSON")
    p.add_argument("--current", required=True, help="Current roadmap JSON")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--output", help="Write to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        prev = json.loads(Path(args.previous).read_text(encoding="utf-8"))
        curr = json.loads(Path(args.current).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"error: cannot read input: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 2

    d = diff(prev, curr)
    out = render_markdown(d) if args.format == "markdown" else json.dumps(d, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
