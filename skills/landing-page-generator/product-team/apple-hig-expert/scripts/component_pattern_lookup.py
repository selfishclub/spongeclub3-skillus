#!/usr/bin/env python3
"""
component_pattern_lookup.py — Suggest Apple-platform component patterns
for a stated UX goal.

Given a goal description and target platform, returns the candidate
native components with use-cases, trade-offs, and platform notes.

Stdlib only. JSON or markdown output.

Usage:
    python3 component_pattern_lookup.py --platform ios --goal "show options without leaving context"
    python3 component_pattern_lookup.py --platform ipados --goal "browse hierarchical content" --format markdown
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Any


@dataclass
class Pattern:
    name: str
    use_cases: list[str]
    trade_offs: str
    platforms: list[str]
    notes: dict[str, str]


PATTERNS: list[Pattern] = [
    Pattern(
        name="Tab Bar",
        use_cases=["top-level navigation between sections", "primary section switching"],
        trade_offs="Visible always; limits to ~5 sections; consumes vertical space",
        platforms=["ios"],
        notes={
            "ios": "Bottom; persistent across nav stack pushes",
            "ipados": "Sidebar usually preferred at large widths",
        },
    ),
    Pattern(
        name="Sidebar (NavigationSplitView)",
        use_cases=["browsable hierarchy", "primary nav with persistent secondary"],
        trade_offs="Requires width; collapses on compact",
        platforms=["ipados", "macos", "visionos"],
        notes={
            "ipados": "Collapses to nav stack on compact width",
            "macos": "Resizable; user can collapse",
            "visionos": "Familiar pattern adapted to spatial",
        },
    ),
    Pattern(
        name="Navigation Stack (push)",
        use_cases=["hierarchical drill-in", "master-detail flows"],
        trade_offs="Deep stacks become hard to navigate; preserves back gesture",
        platforms=["ios", "ipados"],
        notes={"ios": "Don't override back gesture; users rely on it"},
    ),
    Pattern(
        name="Sheet",
        use_cases=["modal task", "secondary task without losing primary context"],
        trade_offs="Detents (medium/large) on iOS; swipe-to-dismiss expected",
        platforms=["ios", "ipados", "macos", "visionos"],
        notes={"ios": "Detents added in iOS 16+; default is large"},
    ),
    Pattern(
        name="Full-Screen Cover",
        use_cases=["immersive task", "distinct mode", "onboarding flow"],
        trade_offs="No surrounding context; explicit close required",
        platforms=["ios", "ipados"],
        notes={},
    ),
    Pattern(
        name="Popover",
        use_cases=["context-anchored options", "brief secondary content"],
        trade_offs="On iPhone (compact width) auto-becomes a sheet",
        platforms=["ipados", "macos"],
        notes={
            "ios": "Becomes a sheet on iPhone; design for both",
            "ipados": "Anchored to source view",
        },
    ),
    Pattern(
        name="Menu (Button)",
        use_cases=["hidden options on a row or button", "compact secondary actions"],
        trade_offs="Discoverability lower than visible button group",
        platforms=["ios", "ipados", "macos", "visionos"],
        notes={"all": "Use system menu; supports SF Symbols + nested menus"},
    ),
    Pattern(
        name="Action Sheet (Confirmation Dialog)",
        use_cases=["destructive choice", "complex multi-option pick"],
        trade_offs="Modal; should be reserved for cases requiring confirmation",
        platforms=["ios", "ipados"],
        notes={"ios": "Use sparingly; menu is often better for non-destructive"},
    ),
    Pattern(
        name="Inspector",
        use_cases=["persistent secondary content", "properties / metadata pane"],
        trade_offs="Requires room; not ideal on iPhone",
        platforms=["ipados", "macos"],
        notes={"ipados": "iPadOS 17+; user can collapse"},
    ),
    Pattern(
        name="Toolbar",
        use_cases=["primary actions on current context", "view options"],
        trade_offs="Limited space; align leading vs trailing carefully",
        platforms=["ios", "ipados", "macos"],
        notes={"macos": "Customizable by user; place key actions here"},
    ),
    Pattern(
        name="List",
        use_cases=["scrollable rows", "settings", "drill-in hierarchy"],
        trade_offs="Standard but heavy visual; LazyVStack lighter",
        platforms=["ios", "ipados", "macos"],
        notes={"all": "Built-in swipe actions, selection, accessibility"},
    ),
    Pattern(
        name="LazyVGrid / LazyHGrid",
        use_cases=["2D layout of items", "photo grids", "card layouts"],
        trade_offs="Less affordance for swipe actions",
        platforms=["ios", "ipados", "macos", "visionos"],
        notes={},
    ),
    Pattern(
        name="Searchable Modifier",
        use_cases=["search bar in navigation", "filtering content"],
        trade_offs="Standard search UX; place at expected location",
        platforms=["ios", "ipados", "macos"],
        notes={"all": "Use scopes for category-filtering"},
    ),
    Pattern(
        name="ShareLink",
        use_cases=["share content with system share sheet"],
        trade_offs="System sheet only — accept all extensions",
        platforms=["ios", "ipados", "macos", "visionos"],
        notes={"all": "Don't build custom sharing"},
    ),
    Pattern(
        name="Widget (Home Screen / Lock Screen / Standby)",
        use_cases=["glanceable info", "quick entry to deep link"],
        trade_offs="Strict size + content limits; battery-conscious",
        platforms=["ios", "ipados", "macos", "watchos"],
        notes={
            "ios": "Multiple sizes; Lock Screen widgets in iOS 16+",
            "watchos": "Smart Stack in watchOS 10+",
        },
    ),
    Pattern(
        name="Complication",
        use_cases=["watch face data point", "always-glanceable info"],
        trade_offs="Highly constrained content; battery- and update-rate-bounded",
        platforms=["watchos"],
        notes={},
    ),
    Pattern(
        name="Live Activity",
        use_cases=["ongoing event status", "Dynamic Island and Lock Screen"],
        trade_offs="Update budget per hour; strict content + size limits",
        platforms=["ios"],
        notes={"ios": "iOS 16.1+; Dynamic Island on supported iPhones"},
    ),
    Pattern(
        name="App Intent",
        use_cases=["expose actions to Shortcuts / Siri / Spotlight / Apple Intelligence"],
        trade_offs="Requires careful intent design; tested across surfaces",
        platforms=["ios", "ipados", "macos", "watchos"],
        notes={"all": "Critical for power users + ecosystem integration"},
    ),
    Pattern(
        name="Volume (visionOS)",
        use_cases=["3D bounded object", "model viewer"],
        trade_offs="Spatial-only; users must position",
        platforms=["visionos"],
        notes={},
    ),
    Pattern(
        name="Immersive Space (visionOS)",
        use_cases=["full-environment content", "VR-like experience"],
        trade_offs="Maximum immersion; lower user agency over space",
        platforms=["visionos"],
        notes={},
    ),
]


GOAL_KEYWORDS = {
    "options": ["Menu (Button)", "Popover", "Action Sheet (Confirmation Dialog)", "Sheet"],
    "navigation": ["Tab Bar", "Sidebar (NavigationSplitView)", "Navigation Stack (push)"],
    "hierarchical": ["Navigation Stack (push)", "Sidebar (NavigationSplitView)", "List"],
    "hierarchy": ["Navigation Stack (push)", "Sidebar (NavigationSplitView)", "List"],
    "search": ["Searchable Modifier"],
    "modal": ["Sheet", "Full-Screen Cover", "Action Sheet (Confirmation Dialog)"],
    "share": ["ShareLink"],
    "context": ["Popover", "Menu (Button)", "Inspector"],
    "without leaving": ["Popover", "Sheet", "Menu (Button)"],
    "glance": ["Widget (Home Screen / Lock Screen / Standby)", "Complication", "Live Activity"],
    "glanceable": ["Widget (Home Screen / Lock Screen / Standby)", "Complication", "Live Activity"],
    "list": ["List", "LazyVGrid / LazyHGrid"],
    "grid": ["LazyVGrid / LazyHGrid"],
    "watch": ["Complication", "Widget (Home Screen / Lock Screen / Standby)"],
    "shortcut": ["App Intent"],
    "siri": ["App Intent"],
    "shortcuts": ["App Intent"],
    "tabs": ["Tab Bar", "Sidebar (NavigationSplitView)"],
    "sidebar": ["Sidebar (NavigationSplitView)"],
    "browse": ["Sidebar (NavigationSplitView)", "List"],
    "immersive": ["Full-Screen Cover", "Immersive Space (visionOS)"],
    "spatial": ["Volume (visionOS)", "Immersive Space (visionOS)"],
    "3d": ["Volume (visionOS)", "Immersive Space (visionOS)"],
    "live": ["Live Activity"],
    "dynamic island": ["Live Activity"],
    "ongoing": ["Live Activity"],
    "delete": ["Action Sheet (Confirmation Dialog)", "Menu (Button)"],
    "confirm": ["Action Sheet (Confirmation Dialog)"],
    "destructive": ["Action Sheet (Confirmation Dialog)"],
}


def lookup(goal: str, platform: str) -> list[Pattern]:
    goal_lower = goal.lower()
    matched_names: list[str] = []
    seen = set()
    for kw, names in GOAL_KEYWORDS.items():
        if kw in goal_lower:
            for n in names:
                if n not in seen:
                    matched_names.append(n)
                    seen.add(n)

    if not matched_names:
        # Generic fallback: pick most-applicable to platform
        defaults = {
            "ios": ["Sheet", "Navigation Stack (push)", "Menu (Button)"],
            "ipados": ["Sidebar (NavigationSplitView)", "Inspector", "Popover"],
            "macos": ["Sidebar (NavigationSplitView)", "Toolbar", "Inspector"],
            "watchos": ["Complication", "Widget (Home Screen / Lock Screen / Standby)"],
            "tvos": ["List", "Navigation Stack (push)"],
            "visionos": ["Sidebar (NavigationSplitView)", "Volume (visionOS)", "Immersive Space (visionOS)"],
        }
        matched_names = defaults.get(platform.lower(), defaults["ios"])

    results: list[Pattern] = []
    for name in matched_names:
        for p in PATTERNS:
            if p.name == name and platform.lower() in p.platforms:
                results.append(p)
                break
    if not results:
        # Loosen: include patterns not strictly on platform but tag note
        for name in matched_names:
            for p in PATTERNS:
                if p.name == name:
                    results.append(p)
                    break
    return results


def render_markdown(goal: str, platform: str, patterns: list[Pattern]) -> str:
    lines = []
    lines.append(f"# Component pattern suggestions")
    lines.append(f"_platform: {platform} | goal: {goal}_\n")
    if not patterns:
        lines.append("_No clear matches found. Re-state the goal more specifically._")
        return "\n".join(lines)
    for p in patterns:
        lines.append(f"## {p.name}")
        lines.append(f"_platforms: {', '.join(p.platforms)}_\n")
        lines.append("**Use cases:**")
        for u in p.use_cases:
            lines.append(f"- {u}")
        lines.append(f"\n**Trade-offs:** {p.trade_offs}")
        note = p.notes.get(platform.lower()) or p.notes.get("all")
        if note:
            lines.append(f"\n**Note for {platform}:** {note}")
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Look up Apple-platform component patterns for a stated goal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--platform",
                  choices=["ios", "ipados", "macos", "watchos", "tvos", "visionos"],
                  default="ios")
    p.add_argument("--goal", required=True, help="UX goal description")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--output", help="Write to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    patterns = lookup(args.goal, args.platform)
    if args.format == "markdown":
        out = render_markdown(args.goal, args.platform, patterns)
    else:
        out = json.dumps({
            "platform": args.platform,
            "goal": args.goal,
            "patterns": [
                {
                    "name": p.name, "use_cases": p.use_cases, "trade_offs": p.trade_offs,
                    "platforms": p.platforms,
                    "platform_note": p.notes.get(args.platform.lower()) or p.notes.get("all", ""),
                }
                for p in patterns
            ],
        }, indent=2)

    if args.output:
        from pathlib import Path
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
