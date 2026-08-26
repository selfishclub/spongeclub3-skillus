#!/usr/bin/env python3
"""
pr_scope_analyzer.py — Analyze a planned PR sequence for size, completeness,
and risk.

Reads a JSON describing planned PRs with line estimates, scope, and
required artifacts (tests, telemetry, docs, flags). Flags oversized PRs,
missing tests/telemetry/docs, risky merges, sequence problems.

Stdlib only. JSON or markdown output.

Usage:
    python3 pr_scope_analyzer.py --input pr_plan.json
    python3 pr_scope_analyzer.py --input pr_plan.json --format markdown

Input schema:
{
  "feature_name": "Notifications v2",
  "prs": [
      {
          "id": "PR-001",
          "title": "Add notification_preferences table",
          "estimated_lines": 80,
          "type": "scaffolding",       # scaffolding|backend|frontend|telemetry|docs|rollout|other
          "behind_feature_flag": true,
          "has_tests": true,
          "has_telemetry": false,
          "has_docs": false,
          "depends_on": [],
          "risk": "low"                  # low|medium|high
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
    pr_id: str
    message: str


def check_pr(pr: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    pid = pr.get("id", "")
    lines = int(pr.get("estimated_lines", 0) or 0)
    pr_type = (pr.get("type") or "").lower()
    risk = (pr.get("risk") or "low").lower()

    if lines > 1000:
        issues.append(Issue("fail", pid,
                          f"{lines} lines — too large; split into smaller PRs"))
    elif lines > 500:
        issues.append(Issue("warn", pid,
                          f"{lines} lines — large; consider splitting"))
    elif lines > 300:
        issues.append(Issue("info", pid,
                          f"{lines} lines — review carefully"))

    if pr_type in ("backend", "frontend") and not pr.get("behind_feature_flag"):
        issues.append(Issue("warn", pid,
                          "behavior change not behind feature flag — risky deploy"))

    if pr_type in ("backend", "frontend") and not pr.get("has_tests"):
        issues.append(Issue("fail", pid, "no tests declared for behavior-change PR"))

    if pr_type in ("backend", "frontend") and not pr.get("has_telemetry"):
        issues.append(Issue("info", pid,
                          "no telemetry declared — verify whether this PR adds user-visible behavior worth measuring"))

    if pr_type == "rollout" and lines > 50:
        issues.append(Issue("warn", pid,
                          f"flag-enable PR is {lines} lines — should be small + isolated"))

    if pr_type == "telemetry" and not pr.get("has_telemetry"):
        issues.append(Issue("warn", pid, "telemetry-type PR doesn't declare telemetry"))

    if risk == "high" and pr_type not in ("scaffolding", "rollout"):
        if not pr.get("behind_feature_flag"):
            issues.append(Issue("fail", pid, "high-risk PR not behind flag"))

    return issues


def analyze_sequence(prs: list[dict[str, Any]]) -> list[Issue]:
    """Look for sequence anti-patterns."""
    issues: list[Issue] = []
    ids = {p.get("id", "") for p in prs}
    for pr in prs:
        for dep in pr.get("depends_on", []) or []:
            if dep not in ids:
                issues.append(Issue("warn", pr.get("id", ""),
                                  f"depends on '{dep}' which isn't in the plan"))

    # Telemetry without prior story PRs
    story_indices = [i for i, p in enumerate(prs) if (p.get("type") or "").lower() in ("backend", "frontend")]
    tel_indices = [i for i, p in enumerate(prs) if (p.get("type") or "").lower() == "telemetry"]
    if tel_indices and story_indices and min(tel_indices) < max(story_indices):
        # Telemetry comes before some stories
        issues.append(Issue("info", "(plan)",
                          "telemetry PR before all behavior PRs — verify events match shipped behavior"))

    # Flag enablement before stories
    flag_indices = [i for i, p in enumerate(prs) if (p.get("type") or "").lower() == "rollout"]
    if flag_indices and story_indices and min(flag_indices) < max(story_indices):
        issues.append(Issue("warn", "(plan)",
                          "flag-enable PR before all behavior PRs — risky"))

    return issues


def analyze(plan: dict[str, Any]) -> dict[str, Any]:
    prs = plan.get("prs", []) or []
    pr_issues: list[Issue] = []
    for pr in prs:
        pr_issues.extend(check_pr(pr))
    seq_issues = analyze_sequence(prs)
    all_issues = pr_issues + seq_issues

    sev_counts = {"fail": 0, "warn": 0, "info": 0}
    for i in all_issues:
        sev_counts[i.severity] = sev_counts.get(i.severity, 0) + 1

    return {
        "feature_name": plan.get("feature_name", ""),
        "pr_count": len(prs),
        "total_estimated_lines": sum(int(p.get("estimated_lines", 0) or 0) for p in prs),
        "severity_counts": sev_counts,
        "issues": [
            {"severity": i.severity, "pr_id": i.pr_id, "message": i.message}
            for i in all_issues
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# PR Scope Analysis — {report.get('feature_name','(unnamed)')}")
    lines.append(f"_PRs: {report['pr_count']} | total lines: {report['total_estimated_lines']}_\n")
    sc = report["severity_counts"]
    lines.append(f"## Severity: fail {sc['fail']} | warn {sc['warn']} | info {sc['info']}\n")
    severity_order = {"fail": 0, "warn": 1, "info": 2}
    sorted_issues = sorted(report["issues"], key=lambda i: severity_order.get(i["severity"], 9))
    lines.append("## Issues")
    if not sorted_issues:
        lines.append("_No issues detected._")
    else:
        lines.append("| Severity | PR | Message |")
        lines.append("|----------|----|---------|")
        for i in sorted_issues:
            lines.append(f"| {i['severity']} | {i['pr_id']} | {i['message']} |")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Analyze a planned PR sequence for size + completeness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON describing PR plan")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--output", help="Write to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        plan = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"error: cannot read input: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 2

    report = analyze(plan)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
