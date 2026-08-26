#!/usr/bin/env python3
"""
fact_inference_separator.py — Classify dossier statements as fact /
inference / speculation; flag unsupported inferences + over-confident
speculation.

Reads a JSON of statements; rates each + flags issues based on
declared classification, supporting evidence, language patterns.

Stdlib only. JSON or markdown output.

Usage:
    python3 fact_inference_separator.py --input dossier_statements.json
    python3 fact_inference_separator.py --input dossier_statements.json --format markdown

Input schema:
{
  "dossier_subject": "Acme Inc",
  "statements": [
      {
          "id": "S-001",
          "text": "Smith joined as CEO in March 2026.",
          "claimed_category": "fact",       # fact|inference|speculation
          "sources_count": 2,
          "explicitly_labeled": true,
          "uses_hedging_language": false
      }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


# Phrases that hint at inference (should be labeled)
INFERENCE_HINTS = [
    "likely", "appears", "suggests", "indicates", "implies",
    "probably", "may be", "could be", "seems",
]

# Phrases that hint at speculation (should be labeled)
SPECULATION_HINTS = [
    "might", "may pivot", "could become", "possibly", "perhaps",
    "rumored", "reportedly considering",
]

# Over-confident language that should be hedged for non-facts
OVERCONFIDENT_HINTS = [
    "certainly", "definitely", "absolutely", "without question",
    "guarantees", "always", "never", "must",
]


@dataclass
class Issue:
    severity: str
    statement_id: str
    message: str


def detect_language(text: str) -> dict[str, list[str]]:
    text_lower = text.lower()
    found_inf = [w for w in INFERENCE_HINTS if w in text_lower]
    found_spec = [w for w in SPECULATION_HINTS if w in text_lower]
    found_overcon = [w for w in OVERCONFIDENT_HINTS if w in text_lower]
    return {
        "inference_hints": found_inf,
        "speculation_hints": found_spec,
        "overconfident_hints": found_overcon,
    }


def check_statement(s: dict[str, Any]) -> tuple[list[Issue], dict[str, Any]]:
    sid = s.get("id", "")
    text = s.get("text", "")
    claimed = (s.get("claimed_category") or "fact").lower()
    src_count = int(s.get("sources_count", 0) or 0)
    explicit_label = bool(s.get("explicitly_labeled", False))
    hedging = bool(s.get("uses_hedging_language", False))
    issues: list[Issue] = []

    lang = detect_language(text)

    # Fact requires sources
    if claimed == "fact" and src_count == 0:
        issues.append(Issue("fail", sid, "fact-category statement with no sources"))

    # Inference requires explicit labeling
    if claimed == "inference" and not explicit_label:
        issues.append(Issue("warn", sid,
                          "inference not explicitly labeled — use 'Inference:' prefix"))

    # Speculation requires explicit labeling
    if claimed == "speculation" and not explicit_label:
        issues.append(Issue("warn", sid,
                          "speculation not explicitly labeled — use 'Speculation:' prefix"))

    # Speculation requires hedging language
    if claimed == "speculation" and not hedging and not lang["speculation_hints"]:
        issues.append(Issue("warn", sid,
                          "speculation should use hedging ('may', 'possibly', 'could')"))

    # Over-confident language in non-facts
    if claimed != "fact" and lang["overconfident_hints"]:
        issues.append(Issue("warn", sid,
                          f"non-fact statement uses overconfident language: "
                          f"{', '.join(lang['overconfident_hints'])}"))

    # Inference language in fact-labeled
    if claimed == "fact" and lang["inference_hints"]:
        issues.append(Issue("warn", sid,
                          f"fact-labeled statement contains inference language: "
                          f"{', '.join(lang['inference_hints'])} — re-classify or rephrase"))

    # Speculation language in non-speculation
    if claimed != "speculation" and lang["speculation_hints"]:
        issues.append(Issue("warn", sid,
                          f"statement contains speculation language: "
                          f"{', '.join(lang['speculation_hints'])} — re-classify"))

    return issues, {
        "statement_id": sid,
        "text": text,
        "claimed_category": claimed,
        "sources_count": src_count,
        "explicitly_labeled": explicit_label,
        "language_signals": lang,
    }


def separate(state: dict[str, Any]) -> dict[str, Any]:
    statements = state.get("statements", []) or []
    all_issues: list[Issue] = []
    summaries: list[dict[str, Any]] = []
    cat_counts = {"fact": 0, "inference": 0, "speculation": 0}
    for s in statements:
        issues, summary = check_statement(s)
        all_issues.extend(issues)
        summaries.append(summary)
        cat_counts[summary["claimed_category"]] = cat_counts.get(summary["claimed_category"], 0) + 1

    sev = {"fail": 0, "warn": 0, "info": 0}
    for i in all_issues:
        sev[i.severity] = sev.get(i.severity, 0) + 1

    return {
        "dossier_subject": state.get("dossier_subject", ""),
        "statement_count": len(statements),
        "category_counts": cat_counts,
        "severity_counts": sev,
        "statements": summaries,
        "issues": [
            {"severity": i.severity, "statement_id": i.statement_id, "message": i.message}
            for i in all_issues
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Fact / Inference / Speculation Audit — {report.get('dossier_subject','')}\n")
    lines.append(f"**Statements:** {report['statement_count']}")
    cc = report["category_counts"]
    lines.append(f"**Categories:** fact: {cc['fact']} | inference: {cc['inference']} | speculation: {cc['speculation']}")
    sc = report["severity_counts"]
    lines.append(f"**Severity:** fail {sc['fail']} | warn {sc['warn']} | info {sc['info']}\n")
    sev_order = {"fail": 0, "warn": 1, "info": 2}
    sorted_issues = sorted(report["issues"], key=lambda i: sev_order.get(i["severity"], 9))
    lines.append("## Issues")
    if not sorted_issues:
        lines.append("_No issues detected._")
    else:
        lines.append("| Severity | Statement | Message |")
        lines.append("|----------|-----------|---------|")
        for i in sorted_issues:
            lines.append(f"| {i['severity']} | {i['statement_id']} | {i['message']} |")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Classify statements + flag fact/inference discipline issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of statements")
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

    report = separate(state)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
