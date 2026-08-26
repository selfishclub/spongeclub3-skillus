#!/usr/bin/env python3
"""
budget_realism_checker.py — Audit a grant budget for realism + common
errors.

Reads a JSON of budget line items; checks personnel effort percentages,
PI effort sum, equipment/supplies balance, travel reasonability,
indirect rate, justification coverage; flags issues.

Stdlib only. JSON or markdown output.

Usage:
    python3 budget_realism_checker.py --input budget.json
    python3 budget_realism_checker.py --input budget.json --format markdown

Input schema:
{
  "project_title": "...",
  "duration_years": 4,
  "indirect_rate_pct": 60,
  "personnel": [
      {
          "name": "Smith, J", "role": "PI",
          "annual_salary_usd": 220000,
          "effort_pct_by_year": [25, 25, 25, 25],
          "fringe_pct": 28,
          "justification_present": true
      }
  ],
  "non_personnel": {
      "equipment_usd_by_year": [50000, 0, 0, 0],
      "supplies_usd_by_year": [40000, 40000, 40000, 40000],
      "travel_usd_by_year": [8000, 8000, 8000, 8000],
      "publications_usd_by_year": [0, 0, 4000, 8000],
      "computing_usd_by_year": [10000, 10000, 10000, 10000],
      "subawards_usd_by_year": [100000, 100000, 100000, 100000],
      "other_usd_by_year": [0, 0, 0, 0]
  }
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
    severity: str
    line: str
    message: str


def check_pi_effort(personnel: list[dict[str, Any]]) -> list[Issue]:
    issues: list[Issue] = []
    pi = next((p for p in personnel if (p.get("role") or "").lower() == "pi"), None)
    if not pi:
        issues.append(Issue("fail", "PI", "No PI identified in personnel"))
        return issues
    effort_by_year = pi.get("effort_pct_by_year", []) or []
    avg = sum(effort_by_year) / max(1, len(effort_by_year))
    if avg < 10:
        issues.append(Issue("fail", "PI",
                          f"PI effort averages {avg:.0f}% — too thin for major grant"))
    elif avg < 15:
        issues.append(Issue("warn", "PI",
                          f"PI effort averages {avg:.0f}% — review whether lead-able"))
    if avg > 70:
        issues.append(Issue("warn", "PI",
                          f"PI effort averages {avg:.0f}% — verify sum of all sources ≤ 100%"))
    return issues


def check_personnel_general(personnel: list[dict[str, Any]]) -> list[Issue]:
    issues: list[Issue] = []
    for p in personnel:
        name = p.get("name", "(unnamed)")
        effort = p.get("effort_pct_by_year", []) or []
        if any(e > 100 for e in effort):
            issues.append(Issue("fail", name, "effort >100% in some year"))
        if any(e < 0 for e in effort):
            issues.append(Issue("fail", name, "negative effort in some year"))
        if not p.get("justification_present"):
            issues.append(Issue("warn", name, "no justification narrative declared"))
        salary = float(p.get("annual_salary_usd", 0) or 0)
        if salary > 250000:
            issues.append(Issue("info", name,
                              f"salary ${salary:,.0f} likely above NIH salary cap; institution must cover difference"))
        fringe = float(p.get("fringe_pct", 0) or 0)
        if fringe == 0:
            issues.append(Issue("warn", name, "fringe % not declared — use institutional rate"))
        elif fringe > 50:
            issues.append(Issue("info", name, f"fringe {fringe}% unusually high — verify"))
    return issues


def check_non_personnel(np: dict[str, Any], duration_years: int) -> list[Issue]:
    issues: list[Issue] = []
    eq = np.get("equipment_usd_by_year", []) or []
    if any(e > 100000 for e in eq):
        issues.append(Issue("warn", "equipment",
                          "year with equipment > $100K — justify against institutional shared resources"))
    if duration_years >= 4 and eq and eq[0] > sum(eq[1:]):
        # OK if year 1 needs scaffolding; flag if year-2+ is empty
        if all(e == 0 for e in eq[1:]):
            issues.append(Issue("info", "equipment",
                              "all equipment in year 1 — amortization assumed"))
    supplies = np.get("supplies_usd_by_year", []) or []
    if supplies and any(s > 200000 for s in supplies):
        issues.append(Issue("info", "supplies",
                          "high supplies budget — verify itemization in justification"))
    travel = np.get("travel_usd_by_year", []) or []
    if travel and all(t == 0 for t in travel):
        issues.append(Issue("info", "travel",
                          "no travel budgeted — verify whether conferences / collaborator visits planned"))
    if travel and any(t > 30000 for t in travel):
        issues.append(Issue("warn", "travel",
                          "travel >$30K/year unusual; justify trip count"))
    subs = np.get("subawards_usd_by_year", []) or []
    if subs and any(s > 0 for s in subs):
        issues.append(Issue("info", "subawards",
                          "subawards present — confirm subaward institutional approval + letters"))
    return issues


def check_indirect_rate(rate: float) -> list[Issue]:
    issues: list[Issue] = []
    if rate <= 0:
        issues.append(Issue("warn", "indirect",
                          "indirect rate is 0% — confirm institutional / funder policy"))
    elif rate > 75:
        issues.append(Issue("info", "indirect",
                          f"indirect rate {rate}% high — confirm institutional negotiated rate"))
    elif 30 <= rate <= 65:
        issues.append(Issue("info", "indirect",
                          f"indirect rate {rate}% in typical range"))
    return issues


def total_direct(np: dict[str, Any], personnel: list[dict[str, Any]],
                duration_years: int) -> float:
    total = 0.0
    for p in personnel:
        salary = float(p.get("annual_salary_usd", 0) or 0)
        fringe_rate = float(p.get("fringe_pct", 0) or 0) / 100.0
        effort = p.get("effort_pct_by_year", []) or []
        for e in effort:
            total += salary * (e / 100.0) * (1 + fringe_rate)
    for category in ("equipment", "supplies", "travel", "publications",
                    "computing", "subawards", "other"):
        years = np.get(f"{category}_usd_by_year", []) or []
        total += sum(years)
    return total


def audit(budget: dict[str, Any]) -> dict[str, Any]:
    personnel = budget.get("personnel", []) or []
    np = budget.get("non_personnel", {}) or {}
    duration = int(budget.get("duration_years", 1) or 1)
    indirect_rate = float(budget.get("indirect_rate_pct", 0) or 0)

    issues = []
    issues.extend(check_pi_effort(personnel))
    issues.extend(check_personnel_general(personnel))
    issues.extend(check_non_personnel(np, duration))
    issues.extend(check_indirect_rate(indirect_rate))

    direct = total_direct(np, personnel, duration)
    indirect = direct * (indirect_rate / 100.0)
    total = direct + indirect

    sev_counts = {"fail": 0, "warn": 0, "info": 0}
    for i in issues:
        sev_counts[i.severity] += 1

    return {
        "project_title": budget.get("project_title", ""),
        "duration_years": duration,
        "indirect_rate_pct": indirect_rate,
        "total_direct_usd_approx": round(direct, 0),
        "total_indirect_usd_approx": round(indirect, 0),
        "total_usd_approx": round(total, 0),
        "issues": [
            {"severity": i.severity, "line": i.line, "message": i.message}
            for i in issues
        ],
        "severity_counts": sev_counts,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Budget Realism Audit — {report.get('project_title','(unnamed)')}\n")
    lines.append(f"**Duration:** {report['duration_years']} years")
    lines.append(f"**Indirect rate:** {report['indirect_rate_pct']}%")
    lines.append(f"**Total direct (approx):** ${report['total_direct_usd_approx']:,.0f}")
    lines.append(f"**Total indirect (approx):** ${report['total_indirect_usd_approx']:,.0f}")
    lines.append(f"**Total (approx):** ${report['total_usd_approx']:,.0f}\n")
    sc = report["severity_counts"]
    lines.append(f"**Severity:** fail {sc['fail']} | warn {sc['warn']} | info {sc['info']}\n")
    sev_order = {"fail": 0, "warn": 1, "info": 2}
    sorted_issues = sorted(report["issues"], key=lambda i: sev_order.get(i["severity"], 9))
    lines.append("## Issues")
    if not sorted_issues:
        lines.append("_No issues detected._")
    else:
        lines.append("| Severity | Line | Message |")
        lines.append("|----------|------|---------|")
        for i in sorted_issues:
            lines.append(f"| {i['severity']} | {i['line']} | {i['message']} |")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Audit grant budget for realism + common errors",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of budget")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--output", help="Write to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        budget = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"error: cannot read input: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 2

    report = audit(budget)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
