#!/usr/bin/env python3
"""
source_triangulation_validator.py — Validate that each claim in a
dossier has adequate source triangulation.

Reads a JSON of claims with supporting sources (and source reliability);
checks: single-source claims, low-reliability sources, non-independent
sources; flags issues.

Stdlib only. JSON or markdown output.

Usage:
    python3 source_triangulation_validator.py --input claims_with_sources.json
    python3 source_triangulation_validator.py --input claims_with_sources.json --format markdown

Input schema:
{
  "dossier_subject": "Acme Inc",
  "claims": [
      {
          "id": "C-001",
          "statement": "Company raised $50M Series B in March 2026.",
          "significance": "high",        # high|medium|low
          "sources": [
              {
                  "name": "TechCrunch article 2026-03-15",
                  "type": "news",
                  "reliability_code": "B",       # A|B|C|D|E|F
                  "independent_from": []          # source IDs / names this is NOT independent of
              },
              {
                  "name": "SEC Form D filing",
                  "type": "regulatory_filing",
                  "reliability_code": "A",
                  "independent_from": []
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
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Issue:
    severity: str
    claim_id: str
    message: str


RELIABILITY_RANK = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}


def check_claim(claim: dict[str, Any]) -> tuple[list[Issue], dict[str, Any]]:
    cid = claim.get("id", "")
    significance = (claim.get("significance") or "medium").lower()
    sources = claim.get("sources", []) or []
    issues: list[Issue] = []

    # Single-source for significant claim
    if len(sources) == 0:
        issues.append(Issue("fail", cid, "claim has NO source — unsupported"))
    elif len(sources) == 1 and significance in ("high", "medium"):
        issues.append(Issue("warn" if significance == "medium" else "fail", cid,
                          f"single source for {significance}-significance claim — triangulate"))

    # Reliability assessment
    reliability_codes = [s.get("reliability_code", "F") for s in sources]
    if reliability_codes:
        max_rel = max(RELIABILITY_RANK.get(c, 0) for c in reliability_codes)
        if max_rel <= 1 and significance == "high":  # E or below
            issues.append(Issue("fail", cid,
                              "high-significance claim with only E-tier sources"))
        elif max_rel <= 2 and significance == "high":  # D or below
            issues.append(Issue("warn", cid,
                              "high-significance claim relies on D-tier sources — find better"))
        if all(RELIABILITY_RANK.get(c, 0) == 0 for c in reliability_codes):
            issues.append(Issue("warn", cid,
                              "all sources rated F (unknown reliability)"))

    # Independence
    source_names = [s.get("name", "") for s in sources]
    not_independent_count = 0
    for s in sources:
        nip = s.get("independent_from", []) or []
        for other_name in source_names:
            if other_name == s.get("name"):
                continue
            if other_name in nip:
                not_independent_count += 1
                break
    independent_sources = len(sources) - not_independent_count
    if len(sources) >= 2 and independent_sources < 2 and significance in ("high", "medium"):
        issues.append(Issue("warn", cid,
                          f"sources may not be independent — effective triangulation ~{independent_sources}"))

    # Source count by reliability
    by_reliability = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}
    for c in reliability_codes:
        by_reliability[c] = by_reliability.get(c, 0) + 1

    return issues, {
        "claim_id": cid,
        "statement": claim.get("statement", ""),
        "significance": significance,
        "source_count": len(sources),
        "independent_source_count_approx": independent_sources,
        "max_reliability": "A" if "A" in reliability_codes else (
                          "B" if "B" in reliability_codes else (
                          "C" if "C" in reliability_codes else (
                          "D" if "D" in reliability_codes else (
                          "E" if "E" in reliability_codes else "F")))) if reliability_codes else "none",
        "by_reliability": by_reliability,
    }


def validate(state: dict[str, Any]) -> dict[str, Any]:
    claims = state.get("claims", []) or []
    all_issues: list[Issue] = []
    claim_summaries: list[dict[str, Any]] = []
    for c in claims:
        issues, summary = check_claim(c)
        all_issues.extend(issues)
        claim_summaries.append(summary)

    sev = {"fail": 0, "warn": 0, "info": 0}
    for i in all_issues:
        sev[i.severity] = sev.get(i.severity, 0) + 1

    return {
        "dossier_subject": state.get("dossier_subject", ""),
        "claim_count": len(claims),
        "severity_counts": sev,
        "claim_summaries": claim_summaries,
        "issues": [
            {"severity": i.severity, "claim_id": i.claim_id, "message": i.message}
            for i in all_issues
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Source Triangulation Validation — {report.get('dossier_subject','')}\n")
    lines.append(f"**Claims:** {report['claim_count']}")
    sc = report["severity_counts"]
    lines.append(f"**Severity:** fail {sc['fail']} | warn {sc['warn']} | info {sc['info']}\n")
    lines.append("## Claim summary")
    lines.append("| Claim | Significance | Sources | Indep ≈ | Max Rel |")
    lines.append("|-------|--------------|---------|---------|---------|")
    for c in report["claim_summaries"]:
        lines.append(f"| {c['claim_id']} | {c['significance']} | {c['source_count']} | "
                    f"{c['independent_source_count_approx']} | {c['max_reliability']} |")
    lines.append("")
    sev_order = {"fail": 0, "warn": 1, "info": 2}
    sorted_issues = sorted(report["issues"], key=lambda i: sev_order.get(i["severity"], 9))
    lines.append("## Issues")
    if not sorted_issues:
        lines.append("_No issues detected._")
    else:
        lines.append("| Severity | Claim | Message |")
        lines.append("|----------|-------|---------|")
        for i in sorted_issues:
            lines.append(f"| {i['severity']} | {i['claim_id']} | {i['message']} |")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Validate source triangulation per claim",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of claims with sources")
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

    report = validate(state)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
