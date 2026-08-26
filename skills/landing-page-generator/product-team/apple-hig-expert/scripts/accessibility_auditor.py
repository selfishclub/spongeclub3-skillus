#!/usr/bin/env python3
"""
accessibility_auditor.py — Audit Apple-platform app accessibility state.

Reads a JSON describing screens + interactive elements + per-screen
accessibility characteristics; flags missing labels, hints, traits;
small touch targets; reliance on color alone; missing Dynamic Type;
unrespected Reduce Motion; missing VoiceOver focus order.

Stdlib only. JSON or markdown output.

Usage:
    python3 accessibility_auditor.py --input a11y_state.json
    python3 accessibility_auditor.py --input a11y_state.json --format markdown

Input schema:
{
  "as_of": "2026-05-27",
  "app_name": "Acme",
  "screens": [
      {
          "id": "home",
          "name": "Home",
          "interactive_elements": [
              {
                  "name": "Compose button",
                  "type": "button",
                  "has_a11y_label": true|false,
                  "has_a11y_hint": true|false,
                  "has_a11y_traits": true|false,
                  "touch_target_pt": 44
              }
          ],
          "decorative_images_hidden_from_a11y": true|false,
          "voiceover_focus_order_validated": true|false,
          "color_only_state_indicators": true|false,
          "supports_dynamic_type": true|false,
          "respects_reduce_motion": true|false,
          "respects_reduce_transparency": true|false,
          "supports_voice_control": true|false,
          "supports_switch_control": true|false,
          "max_dynamic_type_tested": true|false
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
    element: str
    category: str
    message: str


def check_element(s_name: str, el: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    name = el.get("name", "(unnamed)")
    el_type = el.get("type", "control")

    if not el.get("has_a11y_label"):
        issues.append(Issue("fail", s_name, name, "label",
                          f"{el_type} '{name}' has no accessibility label"))
    if el_type in ("custom", "icon-button", "image-button") and not el.get("has_a11y_hint"):
        issues.append(Issue("warn", s_name, name, "hint",
                          f"custom element '{name}' has no accessibility hint"))
    if el_type in ("custom", "tab", "toggle") and not el.get("has_a11y_traits"):
        issues.append(Issue("warn", s_name, name, "traits",
                          f"element '{name}' should declare traits "
                          "(button/selected/header/etc.)"))
    tt = int(el.get("touch_target_pt", 44) or 44)
    if tt < 44:
        issues.append(Issue("fail", s_name, name, "touch-target",
                          f"touch target {tt}pt for '{name}' below 44pt minimum"))
    return issues


def check_screen(s: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    name = s.get("name") or s.get("id") or "(unnamed)"

    for el in s.get("interactive_elements", []) or []:
        issues.extend(check_element(name, el))

    if not s.get("decorative_images_hidden_from_a11y"):
        issues.append(Issue("warn", name, "(screen)", "decorative-images",
                          "decorative images not hidden from accessibility — VoiceOver clutter"))

    if not s.get("voiceover_focus_order_validated"):
        issues.append(Issue("warn", name, "(screen)", "focus-order",
                          "VoiceOver focus order not validated — likely incorrect"))

    if s.get("color_only_state_indicators"):
        issues.append(Issue("fail", name, "(screen)", "color",
                          "uses color alone for state — add icon or text"))

    if not s.get("supports_dynamic_type"):
        issues.append(Issue("fail", name, "(screen)", "dynamic-type",
                          "Dynamic Type not supported — breaks at large sizes"))

    if not s.get("respects_reduce_motion"):
        issues.append(Issue("warn", name, "(screen)", "motion",
                          "doesn't respect Reduce Motion setting"))

    if not s.get("respects_reduce_transparency"):
        issues.append(Issue("info", name, "(screen)", "transparency",
                          "doesn't respect Reduce Transparency setting"))

    if not s.get("supports_voice_control"):
        issues.append(Issue("info", name, "(screen)", "voice-control",
                          "Voice Control not validated — verify all interactive elements callable by name"))

    if not s.get("supports_switch_control"):
        issues.append(Issue("info", name, "(screen)", "switch-control",
                          "Switch Control not validated — verify focusable order works"))

    if not s.get("max_dynamic_type_tested"):
        issues.append(Issue("warn", name, "(screen)", "dynamic-type",
                          "max Dynamic Type size not tested — UI likely breaks"))

    return issues


def audit(state: dict[str, Any]) -> dict[str, Any]:
    screens = state.get("screens", []) or []
    issues: list[Issue] = []
    for s in screens:
        issues.extend(check_screen(s))

    severity_counts = {"fail": 0, "warn": 0, "info": 0}
    for i in issues:
        severity_counts[i.severity] = severity_counts.get(i.severity, 0) + 1

    per_screen_score: dict[str, int] = {}
    for s in screens:
        name = s.get("name") or s.get("id") or "(unnamed)"
        s_issues = [i for i in issues if i.screen == name]
        penalty = sum({"fail": 10, "warn": 4, "info": 1}.get(i.severity, 0) for i in s_issues)
        per_screen_score[name] = max(0, 100 - penalty)

    return {
        "as_of": state.get("as_of", ""),
        "app_name": state.get("app_name", ""),
        "screen_count": len(screens),
        "severity_counts": severity_counts,
        "per_screen_score": per_screen_score,
        "issues": [
            {"severity": i.severity, "screen": i.screen, "element": i.element,
             "category": i.category, "message": i.message}
            for i in issues
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Accessibility Audit — {report.get('app_name','(unnamed)')}")
    lines.append(f"_as of {report['as_of']} | screens: {report['screen_count']}_\n")
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
        lines.append("| Severity | Screen | Element | Category | Message |")
        lines.append("|----------|--------|---------|----------|---------|")
        for i in sorted_issues:
            lines.append(f"| {i['severity']} | {i['screen']} | {i['element']} | "
                        f"{i['category']} | {i['message']} |")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Audit Apple-platform accessibility state",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of a11y state")
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
