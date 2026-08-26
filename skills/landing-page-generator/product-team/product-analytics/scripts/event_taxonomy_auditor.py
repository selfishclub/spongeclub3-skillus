#!/usr/bin/env python3
"""
event_taxonomy_auditor.py — Audit a product event taxonomy for naming
consistency, PII risk, duplication, gaps, undocumented events, and
schema discipline.

Reads a JSON of events with properties; produces issue list + remediation
backlog.

Stdlib only. JSON or markdown output.

Usage:
    python3 event_taxonomy_auditor.py --input event_inventory.json
    python3 event_taxonomy_auditor.py --input event_inventory.json --format markdown

Input schema:
{
  "as_of": "2026-05-27",
  "expected_naming_convention": "snake_case_object_action",   # informational
  "events": [
      {
          "name": "message_sent",
          "category": "core_action",        # lifecycle|core_action|engagement|system|other
          "owner": "Messaging team",
          "documented": true,
          "fired_from": ["server"],         # client, server
          "usage_per_day_p50": 250000,
          "properties": [
              {"name": "user_id", "type": "string", "pii_tier": "internal"},
              {"name": "message_length", "type": "int", "pii_tier": "public"},
              {"name": "channel_type", "type": "string", "pii_tier": "public"}
          ]
      }
  ],
  "expected_events": ["message_sent","user_signed_up","subscription_started"]
}
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


SNAKE_CASE = re.compile(r"^[a-z][a-z0-9_]*[a-z0-9]$")
CAMEL_CASE = re.compile(r"^[a-z][a-zA-Z0-9]*$")
HAS_UPPER = re.compile(r"[A-Z]")
HAS_DASH = re.compile(r"-")
HAS_SPACE = re.compile(r"\s")

PII_RISK_KEYWORDS = {
    "email": "high", "phone": "high", "ssn": "critical", "address": "high",
    "credit": "high", "card": "high", "password": "critical", "secret": "critical",
    "name": "medium", "ip": "medium", "ip_address": "medium",
    "search_query": "medium", "free_text": "medium", "message_content": "medium",
    "first_name": "high", "last_name": "high",
}


@dataclass
class Issue:
    severity: str
    event: str
    issue_type: str
    message: str


def detect_naming_issues(events: list[dict[str, Any]]) -> tuple[list[Issue], str]:
    issues: list[Issue] = []
    naming_styles: Counter[str] = Counter()
    for e in events:
        name = e.get("name", "")
        if HAS_SPACE.search(name):
            issues.append(Issue("fail", name, "naming", "contains whitespace"))
            naming_styles["invalid"] += 1
        elif HAS_DASH.search(name):
            issues.append(Issue("warn", name, "naming", "uses dash (prefer snake_case)"))
            naming_styles["kebab-case"] += 1
        elif SNAKE_CASE.match(name):
            naming_styles["snake_case"] += 1
        elif CAMEL_CASE.match(name) and HAS_UPPER.search(name):
            issues.append(Issue("warn", name, "naming", "camelCase (prefer snake_case)"))
            naming_styles["camelCase"] += 1
        else:
            issues.append(Issue("warn", name, "naming", "unclear naming convention"))
            naming_styles["unknown"] += 1

    # If multiple naming styles in use, that's an issue
    used_styles = [k for k, v in naming_styles.items() if v > 0 and k != "invalid"]
    if len(used_styles) > 1:
        issues.append(Issue("warn", "(taxonomy)", "naming",
                          f"multiple naming styles in use: {', '.join(used_styles)}"))

    dominant = naming_styles.most_common(1)[0][0] if naming_styles else "unknown"
    return issues, dominant


def detect_pii_issues(events: list[dict[str, Any]]) -> list[Issue]:
    issues: list[Issue] = []
    for e in events:
        name = e.get("name", "")
        props = e.get("properties", []) or []
        for p in props:
            pname = (p.get("name") or "").lower()
            tier = (p.get("pii_tier") or "").lower()
            for kw, risk in PII_RISK_KEYWORDS.items():
                if kw in pname and tier in ("public", "internal", ""):
                    issues.append(Issue("fail" if risk == "critical" else "warn",
                                       name, "pii",
                                       f"property '{p.get('name')}' looks like {risk}-risk PII; "
                                       f"current tier '{tier or 'unset'}'"))
                    break
            if tier == "restricted":
                issues.append(Issue("fail", name, "pii",
                                  f"property '{p.get('name')}' marked Restricted "
                                  "— consider whether it should be in analytics at all"))
    return issues


def detect_documentation_issues(events: list[dict[str, Any]]) -> list[Issue]:
    issues: list[Issue] = []
    for e in events:
        name = e.get("name", "")
        if not e.get("documented"):
            issues.append(Issue("warn", name, "documentation",
                              "event not marked documented"))
        if not e.get("owner"):
            issues.append(Issue("warn", name, "documentation",
                              "no owner assigned"))
        if not e.get("category"):
            issues.append(Issue("info", name, "documentation",
                              "no category assigned"))
        props = e.get("properties", []) or []
        if not props:
            issues.append(Issue("info", name, "documentation",
                              "no properties documented"))
        for p in props:
            if not p.get("type"):
                issues.append(Issue("warn", name, "documentation",
                                  f"property '{p.get('name','(unnamed)')}' has no type"))
            if not p.get("pii_tier"):
                issues.append(Issue("warn", name, "documentation",
                                  f"property '{p.get('name','(unnamed)')}' has no PII tier"))
    return issues


def detect_duplication(events: list[dict[str, Any]]) -> list[Issue]:
    issues: list[Issue] = []
    name_counts = Counter(e.get("name", "") for e in events)
    for name, count in name_counts.items():
        if count > 1:
            issues.append(Issue("fail", name, "duplication",
                              f"event name appears {count} times"))

    # Find near-duplicates (similar names)
    names = [e.get("name", "") for e in events]
    seen_pairs = set()
    for i, n1 in enumerate(names):
        n1_norm = n1.replace("_", "")
        for n2 in names[i+1:]:
            n2_norm = n2.replace("_", "")
            if n1 == n2 or (n1, n2) in seen_pairs or (n2, n1) in seen_pairs:
                continue
            if n1_norm == n2_norm:
                issues.append(Issue("warn", f"{n1}/{n2}", "duplication",
                                  "events differ only in underscores; likely duplicates"))
                seen_pairs.add((n1, n2))
            # Action variants like sent/sending/send
            base1 = n1.split("_")[0] if "_" in n1 else n1
            base2 = n2.split("_")[0] if "_" in n2 else n2
            if (base1 == base2 and n1 != n2
                and any(t in n1 for t in ["_sent","_sending","_send"])
                and any(t in n2 for t in ["_sent","_sending","_send"])):
                issues.append(Issue("warn", f"{n1}/{n2}", "duplication",
                                  "tense variation: pick one of past/imperative/present-continuous"))
                seen_pairs.add((n1, n2))
    return issues


def detect_gaps(events: list[dict[str, Any]], expected: list[str]) -> list[Issue]:
    if not expected:
        return []
    actual = {e.get("name", "") for e in events}
    issues: list[Issue] = []
    for exp in expected:
        if exp not in actual:
            issues.append(Issue("warn", exp, "gap",
                              "expected event missing from inventory"))
    return issues


def detect_client_only_critical(events: list[dict[str, Any]]) -> list[Issue]:
    issues: list[Issue] = []
    critical_categories = {"lifecycle", "core_action"}
    for e in events:
        cat = (e.get("category") or "").lower()
        sources = [s.lower() for s in (e.get("fired_from") or [])]
        if cat in critical_categories and sources and "server" not in sources:
            issues.append(Issue("warn", e.get("name", ""), "fragility",
                              f"{cat} event fired only client-side — vulnerable to ad blockers / network"))
    return issues


def analyze(state: dict[str, Any]) -> dict[str, Any]:
    events = state.get("events", []) or []
    expected = state.get("expected_events", []) or []

    naming_issues, dominant_naming = detect_naming_issues(events)
    pii_issues = detect_pii_issues(events)
    doc_issues = detect_documentation_issues(events)
    dup_issues = detect_duplication(events)
    gap_issues = detect_gaps(events, expected)
    fragility_issues = detect_client_only_critical(events)

    all_issues = (naming_issues + pii_issues + doc_issues +
                  dup_issues + gap_issues + fragility_issues)

    sev_counts = Counter(i.severity for i in all_issues)

    type_counts: dict[str, int] = defaultdict(int)
    for i in all_issues:
        type_counts[i.issue_type] += 1

    return {
        "as_of": state.get("as_of", ""),
        "event_count": len(events),
        "dominant_naming_style": dominant_naming,
        "expected_naming_convention": state.get("expected_naming_convention", ""),
        "severity_summary": dict(sev_counts),
        "issue_type_summary": dict(type_counts),
        "issues": [
            {
                "severity": i.severity, "event": i.event,
                "issue_type": i.issue_type, "message": i.message,
            }
            for i in all_issues
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append("# Event Taxonomy Audit")
    lines.append(f"_as of {report['as_of']}_\n")
    lines.append("## Summary")
    lines.append(f"- Events audited: {report['event_count']}")
    lines.append(f"- Dominant naming style: {report['dominant_naming_style']}")
    if report['expected_naming_convention']:
        lines.append(f"- Expected convention: {report['expected_naming_convention']}")
    sev = report["severity_summary"]
    lines.append(f"- Severity: fail {sev.get('fail',0)} | warn {sev.get('warn',0)} | info {sev.get('info',0)}\n")
    types = report["issue_type_summary"]
    if types:
        lines.append("## Issue types")
        lines.append("| Type | Count |")
        lines.append("|------|-------|")
        for k, v in sorted(types.items(), key=lambda x: -x[1]):
            lines.append(f"| {k} | {v} |")
        lines.append("")
    severity_order = {"fail": 0, "warn": 1, "info": 2}
    sorted_issues = sorted(report["issues"],
                          key=lambda i: (severity_order.get(i["severity"], 9), i["issue_type"]))
    lines.append("## Issues")
    if not sorted_issues:
        lines.append("_No issues detected._")
    else:
        lines.append("| Severity | Type | Event | Message |")
        lines.append("|----------|------|-------|---------|")
        for i in sorted_issues:
            lines.append(f"| {i['severity']} | {i['issue_type']} | {i['event']} | {i['message']} |")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Audit an event taxonomy for naming, PII, gaps, duplication",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON event inventory")
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

    report = analyze(state)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
