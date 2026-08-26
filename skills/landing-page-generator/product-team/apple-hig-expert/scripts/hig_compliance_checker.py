#!/usr/bin/env python3
"""
hig_compliance_checker.py — Audit a screen inventory for HIG violations.

Reads a JSON of screens with described UI elements; checks against a
catalog of common HIG violations (hardcoded sizes, non-semantic colors,
custom navigation, missing safe area handling, small touch targets, etc.);
emits issues with severity.

Stdlib only. JSON or markdown output.

Usage:
    python3 hig_compliance_checker.py --input screens.json
    python3 hig_compliance_checker.py --input screens.json --format markdown

Input schema:
{
  "as_of": "2026-05-27",
  "app_name": "Acme",
  "platforms": ["iOS", "iPadOS"],
  "screens": [
      {
          "id": "home",
          "name": "Home",
          "navigation_type": "tab|push|sheet|fullscreen|custom",
          "uses_dynamic_type": true|false,
          "uses_semantic_colors": true|false,
          "respects_safe_area": true|false,
          "smallest_touch_target_pt": 44,
          "dark_mode_tested": true|false,
          "rtl_tested": true|false,
          "haptics_used": true|false,
          "uses_native_components": true|false,
          "custom_back_gesture": true|false,
          "hamburger_menu_on_iphone": true|false,
          "uses_sf_symbols": true|false,
          "blocks_system_gestures": true|false,
          "notes": "free text"
      }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Issue:
    severity: str  # fail|warn|info
    screen: str
    category: str
    message: str


def check_screen(s: dict[str, Any], platforms: list[str]) -> list[Issue]:
    issues: list[Issue] = []
    name = s.get("name") or s.get("id") or "(unnamed)"

    if s.get("navigation_type") == "custom":
        issues.append(Issue("warn", name, "navigation",
                          "custom navigation type — users expect system nav"))

    if not s.get("uses_dynamic_type"):
        issues.append(Issue("fail", name, "typography",
                          "Dynamic Type not used; accessibility + DT users will see broken layout"))

    if not s.get("uses_semantic_colors"):
        issues.append(Issue("warn", name, "color",
                          "non-semantic colors; dark mode parity likely missing"))

    if not s.get("respects_safe_area"):
        issues.append(Issue("fail", name, "layout",
                          "doesn't respect safe area; content will be clipped"))

    tt = int(s.get("smallest_touch_target_pt", 0) or 0)
    if 0 < tt < 44:
        issues.append(Issue("fail", name, "touch-targets",
                          f"smallest touch target {tt}pt below 44pt minimum"))

    if not s.get("dark_mode_tested"):
        issues.append(Issue("warn", name, "dark-mode",
                          "dark mode not tested — likely contrast or color issues"))

    if not s.get("rtl_tested"):
        issues.append(Issue("info", name, "rtl",
                          "RTL not tested — risk if app is localized to Arabic / Hebrew"))

    if "iOS" in platforms and not s.get("haptics_used"):
        issues.append(Issue("info", name, "haptics",
                          "no haptic feedback noted — adds polish on iOS"))

    if not s.get("uses_native_components"):
        issues.append(Issue("warn", name, "components",
                          "custom components instead of native — verify accessibility + behavior"))

    if s.get("custom_back_gesture"):
        issues.append(Issue("fail", name, "gestures",
                          "back gesture overridden — users will be frustrated"))

    if "iOS" in platforms and s.get("hamburger_menu_on_iphone"):
        issues.append(Issue("warn", name, "navigation",
                          "hamburger menu on iPhone — tab bar is more discoverable"))

    if not s.get("uses_sf_symbols"):
        issues.append(Issue("info", name, "icons",
                          "not using SF Symbols — consider for consistency + Dynamic Type"))

    if s.get("blocks_system_gestures"):
        issues.append(Issue("fail", name, "gestures",
                          "blocks system gestures (notification center, control center) — never do this"))

    return issues


def audit(state: dict[str, Any]) -> dict[str, Any]:
    platforms = list(state.get("platforms", ["iOS"]))
    screens = state.get("screens", []) or []
    all_issues: list[Issue] = []
    for s in screens:
        all_issues.extend(check_screen(s, platforms))

    severity_counts = {"fail": 0, "warn": 0, "info": 0}
    for i in all_issues:
        severity_counts[i.severity] = severity_counts.get(i.severity, 0) + 1

    per_screen_score: dict[str, int] = {}
    for s in screens:
        name = s.get("name") or s.get("id") or "(unnamed)"
        screen_issues = [i for i in all_issues if i.screen == name]
        penalty = sum({"fail": 10, "warn": 4, "info": 1}.get(i.severity, 0) for i in screen_issues)
        per_screen_score[name] = max(0, 100 - penalty)

    return {
        "as_of": state.get("as_of", ""),
        "app_name": state.get("app_name", ""),
        "platforms": platforms,
        "screen_count": len(screens),
        "severity_counts": severity_counts,
        "per_screen_score": per_screen_score,
        "issues": [
            {"severity": i.severity, "screen": i.screen,
             "category": i.category, "message": i.message}
            for i in all_issues
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# HIG Compliance Audit — {report.get('app_name','(unnamed)')}")
    lines.append(f"_as of {report['as_of']} | platforms: {', '.join(report['platforms'])} | "
                f"screens: {report['screen_count']}_\n")
    sc = report["severity_counts"]
    lines.append(f"## Severity: fail {sc['fail']} | warn {sc['warn']} | info {sc['info']}\n")
    lines.append("## Per-screen scores")
    lines.append("| Screen | Score |")
    lines.append("|--------|-------|")
    for name, score in sorted(report["per_screen_score"].items(), key=lambda x: x[1]):
        lines.append(f"| {name} | {score}/100 |")
    lines.append("")
    severity_order = {"fail": 0, "warn": 1, "info": 2}
    sorted_issues = sorted(report["issues"], key=lambda i: severity_order.get(i["severity"], 9))
    lines.append("## Issues")
    if not sorted_issues:
        lines.append("_No issues detected._")
    else:
        lines.append("| Severity | Screen | Category | Message |")
        lines.append("|----------|--------|----------|---------|")
        for i in sorted_issues:
            lines.append(f"| {i['severity']} | {i['screen']} | {i['category']} | {i['message']} |")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Audit screens for HIG compliance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of screen inventory")
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

    report = audit(state)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
