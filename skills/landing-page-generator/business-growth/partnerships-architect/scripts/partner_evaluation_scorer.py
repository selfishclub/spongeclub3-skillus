#!/usr/bin/env python3
"""
partner_evaluation_scorer.py — Score a potential partner against 6 evaluation dimensions.

Reads a partner spec YAML; emits per-dimension score (1-5), total, recommendation
(green-light / yellow / red), and rationale.

Stdlib only. Markdown or JSON output.

Usage:
    python3 partner_evaluation_scorer.py --partner partner.yaml
    python3 partner_evaluation_scorer.py --partner partner.yaml --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


# Minimal YAML parser
def parse_yaml(text: str) -> dict[str, Any]:
    lines: list[tuple[int, str]] = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        lines.append((indent, line[indent:]))
    result, _ = _parse_block(lines, 0, 0)
    return result if isinstance(result, dict) else {}


def _parse_block(lines, idx, indent):
    if idx >= len(lines):
        return None, idx
    first_indent = lines[idx][0]
    if first_indent < indent:
        return None, idx
    first_line = lines[idx][1]
    if first_line.startswith("- "):
        return _parse_seq(lines, idx, first_indent)
    return _parse_map(lines, idx, first_indent)


def _parse_map(lines, idx, indent):
    out: dict[str, Any] = {}
    while idx < len(lines):
        cur_indent, content = lines[idx]
        if cur_indent < indent:
            break
        if cur_indent > indent:
            idx += 1
            continue
        if ":" not in content:
            idx += 1
            continue
        key, _, rest = content.partition(":")
        key = key.strip().strip('"').strip("'")
        rest = rest.strip()
        if rest:
            out[key] = _scalar(rest)
            idx += 1
        else:
            idx += 1
            if idx < len(lines) and lines[idx][0] > indent:
                value, idx = _parse_block(lines, idx, lines[idx][0])
                out[key] = value if value is not None else {}
            else:
                out[key] = {}
    return out, idx


def _parse_seq(lines, idx, indent):
    out: list[Any] = []
    while idx < len(lines):
        cur_indent, content = lines[idx]
        if cur_indent < indent:
            break
        if not content.startswith("- "):
            break
        rest = content[2:].strip()
        if not rest:
            idx += 1
            if idx < len(lines) and lines[idx][0] > indent:
                value, idx = _parse_block(lines, idx, lines[idx][0])
                out.append(value if value is not None else {})
            else:
                out.append(None)
        elif ":" in rest:
            synth = [(indent + 2, rest)]
            j = idx + 1
            while j < len(lines) and lines[j][0] > indent:
                synth.append(lines[j])
                j += 1
            value, _ = _parse_map(synth, 0, indent + 2)
            out.append(value)
            idx = j
        else:
            out.append(_scalar(rest))
            idx += 1
    return out, idx


def _scalar(s: str):
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1]
    if s.lower() in ("true", "yes"):
        return True
    if s.lower() in ("false", "no"):
        return False
    if s.lower() in ("null", "~", ""):
        return None
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


@dataclass
class DimensionScore:
    dimension: str
    score: int
    rationale: str


@dataclass
class Evaluation:
    partner_name: str
    dimension_scores: list[DimensionScore]
    total: int
    recommendation: str
    recommendation_reasoning: str


def score_strategic_fit(p: dict[str, Any]) -> DimensionScore:
    fit_attrs = [
        p.get("ideal_customer_overlap", False),
        p.get("vertical_alignment", False),
        p.get("geographic_alignment", False),
        p.get("technology_alignment", False),
    ]
    score = max(1, min(5, sum(1 for x in fit_attrs if x) + 1))
    if p.get("strategic_alignment_explicit"):
        score = min(5, score + 1)
    rationale = f"{sum(1 for x in fit_attrs if x)}/4 fit attributes; explicit alignment: {p.get('strategic_alignment_explicit', False)}"
    return DimensionScore("Strategic fit", score, rationale)


def score_economic_potential(p: dict[str, Any]) -> DimensionScore:
    pipeline_24mo = float(p.get("realistic_pipeline_24mo", 0))
    if pipeline_24mo >= 5_000_000:
        score = 5
    elif pipeline_24mo >= 1_000_000:
        score = 4
    elif pipeline_24mo >= 250_000:
        score = 3
    elif pipeline_24mo >= 50_000:
        score = 2
    else:
        score = 1
    return DimensionScore("Economic potential", score, f"24-month pipeline estimate: ${pipeline_24mo:,.0f}")


def score_partner_credibility(p: dict[str, Any]) -> DimensionScore:
    cred_attrs = [
        p.get("partner_age_years", 0) > 5,
        p.get("partner_revenue_annual", 0) > 1_000_000,
        p.get("named_customers_count", 0) > 5,
        bool(p.get("technical_capability")),
        bool(p.get("brand_recognition")),
    ]
    score = max(1, min(5, sum(1 for x in cred_attrs if x)))
    rationale = f"Age > 5yr: {cred_attrs[0]}, revenue: ${p.get('partner_revenue_annual', 0):,.0f}, customers: {p.get('named_customers_count', 0)}"
    return DimensionScore("Partner credibility", score, rationale)


def score_mutual_commitment(p: dict[str, Any]) -> DimensionScore:
    commitment = p.get("partner_commitment", {}) or {}
    attrs = [
        commitment.get("dedicated_fte_count", 0) >= 1,
        commitment.get("executive_sponsor_named", False),
        commitment.get("budget_committed", 0) > 0,
        commitment.get("specific_targets_agreed", False),
    ]
    score = max(1, min(5, sum(1 for x in attrs if x) + 1))
    rationale = f"FTEs: {commitment.get('dedicated_fte_count', 0)}, exec sponsor: {commitment.get('executive_sponsor_named', False)}, budget: ${commitment.get('budget_committed', 0):,.0f}"
    return DimensionScore("Mutual commitment", score, rationale)


def score_operational_fit(p: dict[str, Any]) -> DimensionScore:
    ops = p.get("operational_fit", {}) or {}
    attrs = [
        ops.get("crm_integration_feasible", True),
        ops.get("cultural_match", True),
        ops.get("process_compatibility", True),
        ops.get("timezone_overlap_acceptable", True),
        ops.get("language_compatible", True),
    ]
    score = max(1, min(5, sum(1 for x in attrs if x)))
    rationale = f"{sum(1 for x in attrs if x)}/5 operational fit attributes positive"
    return DimensionScore("Operational fit", score, rationale)


def score_exit_ability(p: dict[str, Any]) -> DimensionScore:
    """Higher score = easier exit (less locked-in)."""
    exit_attrs = [
        not p.get("creates_customer_lock_in", False),
        not p.get("requires_irreversible_engineering", False),
        not p.get("exclusive_arrangement", False),
        bool(p.get("clear_exit_terms_in_term_sheet", True)),
    ]
    score = max(1, min(5, sum(1 for x in exit_attrs if x) + 1))
    rationale = f"Customer lock-in: {p.get('creates_customer_lock_in', False)}, irreversible eng: {p.get('requires_irreversible_engineering', False)}, exclusive: {p.get('exclusive_arrangement', False)}"
    return DimensionScore("Exit-ability", score, rationale)


def evaluate(partner: dict[str, Any]) -> Evaluation:
    dims = [
        score_strategic_fit(partner),
        score_economic_potential(partner),
        score_partner_credibility(partner),
        score_mutual_commitment(partner),
        score_operational_fit(partner),
        score_exit_ability(partner),
    ]
    total = sum(d.score for d in dims)
    if total >= 25:
        rec = "GREEN-LIGHT"
        reason = "Strong across dimensions; invest with confidence."
    elif total >= 18:
        rec = "YELLOW"
        reason = "Mixed signal; pilot scope first; structure carefully before full commitment."
    else:
        rec = "RED"
        reason = "Weak signal; decline or substantially restructure before proceeding."
    return Evaluation(
        partner_name=partner.get("name", "unknown"),
        dimension_scores=dims,
        total=total,
        recommendation=rec,
        recommendation_reasoning=reason,
    )


def render_markdown(e: Evaluation) -> str:
    out = [f"# Partner Evaluation: {e.partner_name}", ""]
    out.append("## Per-Dimension Scores")
    out.append("")
    out.append("| Dimension | Score | Rationale |")
    out.append("|-----------|-------|-----------|")
    for d in e.dimension_scores:
        out.append(f"| {d.dimension} | {d.score}/5 | {d.rationale} |")
    out.append("")
    out.append(f"## Total: {e.total}/30")
    out.append("")
    emoji = "🟢" if e.recommendation == "GREEN-LIGHT" else ("🟡" if e.recommendation == "YELLOW" else "🔴")
    out.append(f"## Recommendation: {emoji} **{e.recommendation}**")
    out.append("")
    out.append(e.recommendation_reasoning)
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Score a potential partner on 6 evaluation dimensions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--partner", required=True, help="Partner spec YAML")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", help="Output file path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        partner = parse_yaml(Path(args.partner).read_text())
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    evaluation = evaluate(partner)
    if args.format == "json":
        out = json.dumps(asdict(evaluation), indent=2)
    else:
        out = render_markdown(evaluation)
    if args.output:
        Path(args.output).write_text(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
