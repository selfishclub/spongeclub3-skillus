#!/usr/bin/env python3
"""
metric_tree_designer.py — Analyze and validate a product metric tree.

Reads a JSON describing a candidate metric tree (NS + inputs + drivers +
guardrails). Validates structure, surfaces anti-patterns (too many inputs,
unowned metrics, vanity NSM, missing guardrails), and emits a structured
report.

Stdlib only. JSON or markdown output.

Usage:
    python3 metric_tree_designer.py --input metric_tree.json
    python3 metric_tree_designer.py --input metric_tree.json --format markdown

Input schema:
{
  "product_name": "Acme",
  "as_of": "2026-05-27",
  "north_star": {
      "name": "Messages sent per WAU per company",
      "definition": "Sum(message_sent) / company / week, filtered to WAU companies",
      "owner": "VP Product",
      "value_aligned": true,
      "single_number": true,
      "can_move_weekly": true,
      "hard_to_game": true,
      "is_revenue_or_count_metric": false
  },
  "inputs": [
      {
          "name": "Activation rate (7-day)",
          "definition": "% of new signups that send ≥10 messages within 7 days",
          "owner": "Growth PM",
          "drivers": [
              {"name": "Signup completion rate", "owner": "Growth PM"},
              {"name": "Time-to-first-message median", "owner": "Onboarding PM"},
              {"name": "Onboarding step completion", "owner": "Onboarding PM"}
          ]
      }
  ],
  "guardrails": [
      {"name": "Spam rate", "owner": "Trust & Safety"},
      {"name": "User-reported complaints", "owner": "T&S"}
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


VANITY_KEYWORDS = ["signup", "view", "click", "download", "session", "page",
                   "follower", "share", "open"]


@dataclass
class Finding:
    severity: str   # info|warn|fail
    component: str
    message: str


def analyze_north_star(ns: dict[str, Any]) -> tuple[int, list[Finding]]:
    findings: list[Finding] = []
    score = 0

    if not ns:
        findings.append(Finding("fail", "north-star", "no North Star defined"))
        return 0, findings

    name = ns.get("name", "").strip()
    if name:
        score += 10
    else:
        findings.append(Finding("fail", "north-star", "name missing"))

    if ns.get("definition", "").strip():
        score += 10
    else:
        findings.append(Finding("fail", "north-star",
                              "definition missing — metrics without definitions diverge"))

    if ns.get("owner", "").strip():
        score += 10
    else:
        findings.append(Finding("warn", "north-star", "no owner assigned"))

    if ns.get("value_aligned"):
        score += 15
    else:
        findings.append(Finding("warn", "north-star",
                              "not marked value_aligned — consider whether this measures value"))

    if ns.get("single_number"):
        score += 10
    else:
        findings.append(Finding("warn", "north-star",
                              "not a single number — a North Star should be one metric"))

    if ns.get("can_move_weekly"):
        score += 15
    else:
        findings.append(Finding("warn", "north-star",
                              "doesn't move weekly — hard to steer a product on"))

    if ns.get("hard_to_game"):
        score += 10
    else:
        findings.append(Finding("warn", "north-star",
                              "easy to game — verify guardrails"))

    if ns.get("is_revenue_or_count_metric"):
        findings.append(Finding("warn", "north-star",
                              "revenue or top-line count metric — usually a vanity NSM; "
                              "consider a value-driven metric instead"))
    else:
        score += 10

    # Vanity keyword detection
    name_lower = name.lower()
    for kw in VANITY_KEYWORDS:
        if kw in name_lower:
            findings.append(Finding("warn", "north-star",
                                  f"name contains potential vanity keyword '{kw}' — "
                                  "verify this measures realized value"))
            break

    return min(80, score), findings


def analyze_inputs(inputs: list[dict[str, Any]]) -> tuple[int, list[Finding]]:
    findings: list[Finding] = []
    score = 0

    if not inputs:
        findings.append(Finding("fail", "inputs", "no input metrics defined"))
        return 0, findings

    n = len(inputs)
    if 3 <= n <= 5:
        score += 20
    elif n < 3:
        findings.append(Finding("warn", "inputs",
                              f"only {n} input metrics — usually too few to decompose NS"))
        score += 8
    else:
        findings.append(Finding("warn", "inputs",
                              f"{n} input metrics — typically 3-5 is more focused"))
        score += 10

    inputs_with_drivers = 0
    inputs_with_owners = 0
    inputs_with_definitions = 0

    for inp in inputs:
        if inp.get("owner", "").strip():
            inputs_with_owners += 1
        else:
            findings.append(Finding("warn", "inputs",
                                  f"input '{inp.get('name','(unnamed)')}' has no owner"))
        if inp.get("definition", "").strip():
            inputs_with_definitions += 1
        else:
            findings.append(Finding("warn", "inputs",
                                  f"input '{inp.get('name','(unnamed)')}' has no definition"))
        drivers = inp.get("drivers", []) or []
        if 3 <= len(drivers) <= 5:
            inputs_with_drivers += 1
        elif drivers:
            findings.append(Finding("info", "inputs",
                                  f"input '{inp.get('name','(unnamed)')}' has {len(drivers)} drivers "
                                  "(typical 3-5)"))
        else:
            findings.append(Finding("warn", "inputs",
                                  f"input '{inp.get('name','(unnamed)')}' has no driver metrics"))

    if inputs_with_owners == n:
        score += 10
    if inputs_with_definitions == n:
        score += 10

    return min(50, score), findings


def analyze_guardrails(guardrails: list[dict[str, Any]],
                       inputs: list[dict[str, Any]]) -> tuple[int, list[Finding]]:
    findings: list[Finding] = []
    score = 0

    if not guardrails:
        findings.append(Finding("fail", "guardrails",
                              "no guardrails / counter-metrics — risk of gaming"))
        return 0, findings

    n = len(guardrails)
    if n >= 3:
        score += 30
    elif n >= 1:
        score += 15
        findings.append(Finding("warn", "guardrails",
                              f"only {n} guardrail(s); typically 3-5 needed"))

    for g in guardrails:
        if not g.get("owner", "").strip():
            findings.append(Finding("warn", "guardrails",
                                  f"guardrail '{g.get('name','(unnamed)')}' has no owner"))

    return min(40, score), findings


def overall_band(score: int) -> str:
    if score >= 130:
        return "Mature"
    if score >= 100:
        return "Healthy"
    if score >= 70:
        return "Workable"
    if score >= 40:
        return "Needs work"
    return "Critical"


def analyze(tree: dict[str, Any]) -> dict[str, Any]:
    ns = tree.get("north_star", {}) or {}
    inputs = tree.get("inputs", []) or []
    guardrails = tree.get("guardrails", []) or []

    ns_score, ns_findings = analyze_north_star(ns)
    inp_score, inp_findings = analyze_inputs(inputs)
    gr_score, gr_findings = analyze_guardrails(guardrails, inputs)

    findings = ns_findings + inp_findings + gr_findings
    score = ns_score + inp_score + gr_score
    band = overall_band(score)

    summary = {
        "north_star_score": ns_score,
        "inputs_score": inp_score,
        "guardrails_score": gr_score,
        "total_score": score,
        "band": band,
        "input_count": len(inputs),
        "guardrail_count": len(guardrails),
        "driver_count": sum(len(i.get("drivers", []) or []) for i in inputs),
    }

    return {
        "product_name": tree.get("product_name", ""),
        "as_of": tree.get("as_of", ""),
        "summary": summary,
        "findings": [
            {"severity": f.severity, "component": f.component, "message": f.message}
            for f in findings
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Metric Tree Review — {report.get('product_name','(unnamed)')}")
    lines.append(f"_as of {report['as_of']}_\n")
    s = report["summary"]
    lines.append(f"## Overall: **{s['total_score']}/170 — {s['band']}**\n")
    lines.append("| Component | Score | Max |")
    lines.append("|-----------|-------|-----|")
    lines.append(f"| North Star | {s['north_star_score']} | 80 |")
    lines.append(f"| Inputs | {s['inputs_score']} | 50 |")
    lines.append(f"| Guardrails | {s['guardrails_score']} | 40 |")
    lines.append("")
    lines.append(f"Counts: {s['input_count']} inputs, {s['driver_count']} drivers, "
                f"{s['guardrail_count']} guardrails\n")

    severity_order = {"fail": 0, "warn": 1, "info": 2}
    sorted_findings = sorted(report["findings"], key=lambda f: severity_order.get(f["severity"], 9))

    lines.append("## Findings")
    if not sorted_findings:
        lines.append("_No issues detected._")
    else:
        lines.append("| Severity | Component | Message |")
        lines.append("|----------|-----------|---------|")
        for f in sorted_findings:
            lines.append(f"| {f['severity']} | {f['component']} | {f['message']} |")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Analyze a product metric tree",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON metric tree")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--output", help="Write to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        tree = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"error: cannot read input: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 2

    report = analyze(tree)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
