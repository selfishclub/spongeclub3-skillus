#!/usr/bin/env python3
"""
readiness_roadmap_generator.py — Generate a multi-framework readiness roadmap.

Given target frameworks + current scores, emit a quarter-by-quarter roadmap
with sequencing, parallel pursuits, milestones, and cumulative cost estimates.

Stdlib only. Markdown or JSON.

Usage:
    python3 readiness_roadmap_generator.py --target-frameworks SOC2,ISO27001
    python3 readiness_roadmap_generator.py --target-frameworks SOC2,ISO27001,GDPR --current-scores '{"SOC2":40,"ISO27001":20,"GDPR":60}' --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any


# Per-framework: weeks to certify from baseline + cost estimate
FRAMEWORK_TIMING = {
    "SOC2_TYPE_I": {"weeks_from_zero": 16, "min_score_to_audit": 75, "audit_cost_usd": 50000},
    "SOC2_TYPE_II": {"weeks_from_zero": 36, "min_score_to_audit": 80, "audit_cost_usd": 100000},  # 6mo observation + audit
    "ISO27001": {"weeks_from_zero": 28, "min_score_to_audit": 75, "audit_cost_usd": 60000},
    "NIST_CSF": {"weeks_from_zero": 12, "min_score_to_audit": 70, "audit_cost_usd": 20000},
    "GDPR": {"weeks_from_zero": 20, "min_score_to_audit": 70, "audit_cost_usd": 0},  # No certification; ongoing
    "HIPAA": {"weeks_from_zero": 16, "min_score_to_audit": 75, "audit_cost_usd": 0},  # Self-attestation
    "PCI_DSS": {"weeks_from_zero": 24, "min_score_to_audit": 80, "audit_cost_usd": 150000},
    "NIS2": {"weeks_from_zero": 20, "min_score_to_audit": 75, "audit_cost_usd": 0},  # Self-attestation; enforcement-only
    "DORA": {"weeks_from_zero": 20, "min_score_to_audit": 75, "audit_cost_usd": 0},  # Self-attestation
    "ISO42001": {"weeks_from_zero": 28, "min_score_to_audit": 75, "audit_cost_usd": 50000},
}


@dataclass
class Phase:
    quarter: str  # Q1-2026, etc.
    start_date: str
    end_date: str
    frameworks_in_progress: list[str]
    frameworks_audited: list[str]
    cumulative_cost_usd: int
    milestones: list[str]


@dataclass
class Roadmap:
    target_frameworks: list[str]
    current_scores: dict[str, int]
    start_date: str
    estimated_completion_date: str
    total_estimated_cost_usd: int
    phases: list[Phase]
    notes: list[str]


def generate(target_frameworks: list[str], current_scores: dict[str, int], start_date: datetime) -> Roadmap:
    # Order frameworks by typical sequencing
    sequencing_priority = ["SOC2_TYPE_I", "ISO27001", "SOC2_TYPE_II", "GDPR", "HIPAA",
                           "NIST_CSF", "PCI_DSS", "NIS2", "DORA", "ISO42001"]
    sorted_frameworks = sorted(target_frameworks, key=lambda fw: sequencing_priority.index(fw) if fw in sequencing_priority else 99)

    phases: list[Phase] = []
    cumulative_cost = 0
    notes: list[str] = []
    in_progress: set[str] = set()
    audited: set[str] = set()
    current_week = 0
    completion_date = start_date

    # Process each framework in priority order
    for fw in sorted_frameworks:
        timing = FRAMEWORK_TIMING.get(fw, {"weeks_from_zero": 24, "min_score_to_audit": 75, "audit_cost_usd": 30000})
        current_score = current_scores.get(fw, 0)
        weeks_needed = timing["weeks_from_zero"]
        if current_score > 0:
            # Scale weeks based on starting score
            weeks_needed = max(4, int(weeks_needed * (1 - current_score / 100)))

        start = start_date + timedelta(weeks=current_week)
        end = start + timedelta(weeks=weeks_needed)

        in_progress.add(fw)
        audited.add(fw)
        cumulative_cost += timing["audit_cost_usd"]

        quarter = f"Q{(start.month - 1) // 3 + 1}-{start.year}"
        phase = Phase(
            quarter=quarter,
            start_date=start.date().isoformat(),
            end_date=end.date().isoformat(),
            frameworks_in_progress=sorted(in_progress),
            frameworks_audited=sorted(audited),
            cumulative_cost_usd=cumulative_cost,
            milestones=[
                f"Begin {fw} readiness work",
                f"Complete {fw} audit at end of phase",
                f"Estimated weeks: {weeks_needed}",
            ],
        )
        phases.append(phase)

        # Some frameworks run in parallel with prior ones
        if fw in ("GDPR", "HIPAA", "NIST_CSF"):  # ongoing or self-assessed
            notes.append(f"{fw}: continuous; can run in parallel with other certifications")
            current_week += weeks_needed // 2  # half-time overlap
        else:
            current_week += weeks_needed
        completion_date = end

    if "SOC2_TYPE_II" in sorted_frameworks and "SOC2_TYPE_I" in sorted_frameworks:
        notes.append("SOC 2 Type II requires 6-12 month observation period after Type I; plan accordingly")
    if "ISO27001" in sorted_frameworks and "SOC2_TYPE_II" in sorted_frameworks:
        notes.append("SOC 2 + ISO 27001 have 60-80% control overlap; pursue in parallel")
    if "GDPR" in sorted_frameworks:
        notes.append("GDPR is ongoing; integrate with continuous compliance program from day 1")
    if any(s < 50 for s in current_scores.values()):
        notes.append("Some frameworks at very low baseline; consider phased start vs aggressive multi-track")

    total_cost = sum(FRAMEWORK_TIMING.get(fw, {"audit_cost_usd": 30000})["audit_cost_usd"] for fw in sorted_frameworks)

    return Roadmap(
        target_frameworks=sorted_frameworks,
        current_scores=current_scores,
        start_date=start_date.date().isoformat(),
        estimated_completion_date=completion_date.date().isoformat(),
        total_estimated_cost_usd=total_cost,
        phases=phases,
        notes=notes,
    )


def render_markdown(r: Roadmap) -> str:
    out = ["# Multi-Framework Readiness Roadmap", ""]
    out.append(f"- **Target frameworks**: {', '.join(r.target_frameworks)}")
    out.append(f"- **Start date**: {r.start_date}")
    out.append(f"- **Estimated completion**: {r.estimated_completion_date}")
    out.append(f"- **Total estimated cost (audit only)**: ${r.total_estimated_cost_usd:,}")
    out.append("")
    out.append("## Current Scores")
    out.append("")
    out.append("| Framework | Score |")
    out.append("|-----------|-------|")
    for fw in r.target_frameworks:
        out.append(f"| {fw} | {r.current_scores.get(fw, 0)}/100 |")
    out.append("")
    out.append("## Phases")
    out.append("")
    for p in r.phases:
        out.append(f"### {p.quarter} ({p.start_date} → {p.end_date})")
        out.append("")
        out.append(f"- In progress: {', '.join(p.frameworks_in_progress)}")
        out.append(f"- Audited cumulative: {', '.join(p.frameworks_audited)}")
        out.append(f"- Cumulative cost: ${p.cumulative_cost_usd:,}")
        out.append("- Milestones:")
        for m in p.milestones:
            out.append(f"  - {m}")
        out.append("")
    out.append("## Notes")
    out.append("")
    for n in r.notes:
        out.append(f"- {n}")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate multi-framework readiness roadmap",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--target-frameworks", required=True,
                   help="Comma-separated frameworks (SOC2_TYPE_I, SOC2_TYPE_II, ISO27001, NIST_CSF, GDPR, HIPAA, PCI_DSS, ISO42001)")
    p.add_argument("--current-scores", default="{}", help="JSON map of framework→score (0-100)")
    p.add_argument("--start-date", help="Start date (ISO 8601); default: today")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", help="Output file path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    frameworks = [f.strip() for f in args.target_frameworks.split(",")]
    try:
        scores = json.loads(args.current_scores)
    except json.JSONDecodeError as e:
        print(f"error: invalid --current-scores JSON: {e}", file=sys.stderr)
        return 2
    if args.start_date:
        try:
            start = datetime.fromisoformat(args.start_date.replace("Z", "+00:00"))
        except ValueError:
            print(f"error: invalid --start-date: {args.start_date}", file=sys.stderr)
            return 2
    else:
        start = datetime.now(timezone.utc)
    r = generate(frameworks, scores, start)
    if args.format == "json":
        out = json.dumps(asdict(r), indent=2, default=str)
    else:
        out = render_markdown(r)
    if args.output:
        Path(args.output).write_text(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
