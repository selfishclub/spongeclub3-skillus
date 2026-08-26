#!/usr/bin/env python3
"""
ai_investment_planner.py — Allocate AI budget across initiatives using
a strategic-fit x value x confidence model with risk penalty.

Reads a JSON file of candidate initiatives (existing + proposed), scores
each on 5 factors, allocates the requested budget greedily by adjusted
score per dollar, and produces a portfolio recommendation. Output is
either JSON or markdown.

Stdlib only.

Usage:
    python3 ai_investment_planner.py --input portfolio.json --budget 5000000
    python3 ai_investment_planner.py --input portfolio.json --budget 5M --format markdown
    python3 ai_investment_planner.py --input portfolio.json --budget 5000000 --reserve-pct 15

Input schema:
{
  "fiscal_period": "FY27",
  "currency": "USD",
  "weights": {                           # optional, defaults shown
      "strategic_fit": 0.25,
      "value": 0.30,
      "confidence": 0.15,
      "risk_penalty": 0.15,
      "time_to_value": 0.15
  },
  "themes": ["productivity","customer-experience","platform","governance"],
  "initiatives": [
      {
          "id": "INIT-001",
          "name": "Search relevance v2",
          "owner": "Platform",
          "theme": "platform",
          "bucket": "grow",                # run|grow|transform
          "annual_cost_usd": 800000,
          "strategic_fit": 4,              # 1-5
          "value": 5,                      # 1-5 (rev/cost impact)
          "confidence": 4,                 # 1-5 (data quality, prior art)
          "risk": 3,                       # 1-5 (higher = more risk; penalty)
          "time_to_value_months": 4,
          "must_fund": false,              # e.g., regulatory, dependency
          "status": "proposed",            # proposed|in-flight|in-eval
          "dependencies": ["INIT-000"]     # optional
      }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DEFAULT_WEIGHTS = {
    "strategic_fit": 0.25,
    "value": 0.30,
    "confidence": 0.15,
    "risk_penalty": 0.15,
    "time_to_value": 0.15,
}

TARGET_MIX_PCT = {"run": 50, "grow": 35, "transform": 15}


@dataclass
class Initiative:
    id: str
    name: str
    owner: str
    theme: str
    bucket: str
    annual_cost_usd: float
    strategic_fit: int
    value: int
    confidence: int
    risk: int
    time_to_value_months: int
    must_fund: bool = False
    status: str = "proposed"
    dependencies: list[str] = field(default_factory=list)
    raw_score: float = 0.0
    adjusted_score: float = 0.0
    score_per_dollar: float = 0.0
    funded: bool = False
    funded_amount: float = 0.0
    reason: str = ""


@dataclass
class Allocation:
    fiscal_period: str
    currency: str
    budget: float
    reserve: float
    funded_total: float
    unspent: float
    funded: list[Initiative]
    deferred: list[Initiative]
    bucket_mix: dict[str, float]
    theme_mix: dict[str, float]
    warnings: list[str]


def parse_amount(amount: str | int | float) -> float:
    if isinstance(amount, (int, float)):
        return float(amount)
    s = str(amount).strip().upper().replace(",", "").replace("$", "")
    m = re.match(r"^(\d+(?:\.\d+)?)([KMB]?)$", s)
    if not m:
        try:
            return float(s)
        except ValueError as e:
            raise ValueError(f"cannot parse amount: {amount}") from e
    num = float(m.group(1))
    suffix = m.group(2)
    if suffix == "K":
        num *= 1_000
    elif suffix == "M":
        num *= 1_000_000
    elif suffix == "B":
        num *= 1_000_000_000
    return num


def load_initiatives(raw: list[dict[str, Any]]) -> list[Initiative]:
    out: list[Initiative] = []
    for r in raw:
        out.append(Initiative(
            id=r.get("id", ""),
            name=r.get("name", ""),
            owner=r.get("owner", ""),
            theme=r.get("theme", "(untagged)"),
            bucket=r.get("bucket", "grow"),
            annual_cost_usd=float(r.get("annual_cost_usd", 0)),
            strategic_fit=int(r.get("strategic_fit", 0)),
            value=int(r.get("value", 0)),
            confidence=int(r.get("confidence", 0)),
            risk=int(r.get("risk", 0)),
            time_to_value_months=int(r.get("time_to_value_months", 12)),
            must_fund=bool(r.get("must_fund", False)),
            status=r.get("status", "proposed"),
            dependencies=list(r.get("dependencies", []) or []),
        ))
    return out


def normalize_weights(weights: dict[str, float] | None) -> dict[str, float]:
    if not weights:
        return dict(DEFAULT_WEIGHTS)
    w = dict(DEFAULT_WEIGHTS)
    w.update({k: float(v) for k, v in weights.items() if k in DEFAULT_WEIGHTS})
    total = sum(w.values())
    if total <= 0:
        return dict(DEFAULT_WEIGHTS)
    return {k: v / total for k, v in w.items()}


def score_initiative(init: Initiative, weights: dict[str, float]) -> tuple[float, float, float]:
    """Return (raw_score, adjusted_score, score_per_dollar)."""
    # Normalize 1-5 to 0-1
    sf = max(0.0, min(1.0, init.strategic_fit / 5.0))
    val = max(0.0, min(1.0, init.value / 5.0))
    conf = max(0.0, min(1.0, init.confidence / 5.0))
    risk = max(0.0, min(1.0, init.risk / 5.0))

    # Time-to-value: faster is better. 1 month = 1.0, 12+ months = 0.2
    ttv_months = max(1, init.time_to_value_months)
    ttv = max(0.2, min(1.0, 12.0 / (ttv_months + 6)))

    raw = (
        weights["strategic_fit"] * sf
        + weights["value"] * val
        + weights["confidence"] * conf
        + weights["time_to_value"] * ttv
        - weights["risk_penalty"] * risk
    )
    adjusted = max(0.0, raw)

    cost = max(1.0, init.annual_cost_usd)
    spd = adjusted / (cost / 1_000_000.0)  # score per $1M
    return raw, adjusted, spd


def allocate(
    initiatives: list[Initiative],
    budget: float,
    reserve_pct: float,
) -> Allocation:
    warnings: list[str] = []
    reserve = budget * (reserve_pct / 100.0)
    spend_budget = budget - reserve
    funded_total = 0.0
    funded: list[Initiative] = []
    deferred: list[Initiative] = []

    # First pass: fund all must_fund items (even if they go over budget; warn)
    for init in initiatives:
        if init.must_fund:
            init.funded = True
            init.funded_amount = init.annual_cost_usd
            init.reason = "must-fund (regulatory / dependency)"
            funded.append(init)
            funded_total += init.annual_cost_usd

    if funded_total > spend_budget:
        warnings.append(
            f"must-fund spend ({funded_total:,.0f}) exceeds non-reserve budget "
            f"({spend_budget:,.0f}); reduce reserve or grow budget."
        )

    # Second pass: greedy by score per dollar
    discretionary = [i for i in initiatives if not i.must_fund]
    discretionary.sort(key=lambda x: x.score_per_dollar, reverse=True)
    funded_ids = {i.id for i in funded}

    for init in discretionary:
        # Honor dependencies — defer if any unmet
        unmet = [d for d in init.dependencies if d not in funded_ids]
        if unmet:
            init.reason = f"deferred: dependency unmet ({', '.join(unmet)})"
            deferred.append(init)
            continue
        if funded_total + init.annual_cost_usd <= spend_budget:
            init.funded = True
            init.funded_amount = init.annual_cost_usd
            init.reason = f"funded (score/$M: {init.score_per_dollar:.3f})"
            funded.append(init)
            funded_ids.add(init.id)
            funded_total += init.annual_cost_usd
        else:
            init.reason = "deferred: budget exhausted"
            deferred.append(init)

    # Compute mixes
    bucket_mix = {b: 0.0 for b in TARGET_MIX_PCT}
    theme_mix: dict[str, float] = {}
    for init in funded:
        bucket_mix[init.bucket] = bucket_mix.get(init.bucket, 0.0) + init.funded_amount
        theme_mix[init.theme] = theme_mix.get(init.theme, 0.0) + init.funded_amount
    if funded_total > 0:
        bucket_mix = {k: round(v / funded_total * 100, 1) for k, v in bucket_mix.items()}
        theme_mix = {k: round(v / funded_total * 100, 1) for k, v in theme_mix.items()}

    # Warn on bucket drift > 15 pts from target
    for bucket, target in TARGET_MIX_PCT.items():
        actual = bucket_mix.get(bucket, 0.0)
        if abs(actual - target) > 15:
            warnings.append(
                f"bucket '{bucket}' allocation {actual}% vs target {target}% — drift > 15pts"
            )

    unspent = budget - funded_total
    return Allocation(
        fiscal_period="",
        currency="USD",
        budget=budget,
        reserve=reserve,
        funded_total=funded_total,
        unspent=unspent,
        funded=funded,
        deferred=deferred,
        bucket_mix=bucket_mix,
        theme_mix=theme_mix,
        warnings=warnings,
    )


def render_markdown(alloc: Allocation) -> str:
    lines = []
    lines.append(f"# AI Investment Plan — {alloc.fiscal_period or '(unspecified)'}")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- Total budget: **${alloc.budget:,.0f}** ({alloc.currency})")
    lines.append(f"- Reserve held: ${alloc.reserve:,.0f}")
    lines.append(f"- Allocated: ${alloc.funded_total:,.0f}")
    lines.append(f"- Unspent: ${alloc.unspent:,.0f}")
    lines.append("")
    lines.append("## Bucket mix (vs target)")
    lines.append("| Bucket | Actual % | Target % |")
    lines.append("|--------|----------|----------|")
    for bucket, target in TARGET_MIX_PCT.items():
        lines.append(f"| {bucket} | {alloc.bucket_mix.get(bucket, 0)}% | {target}% |")
    lines.append("")
    lines.append("## Theme mix")
    lines.append("| Theme | % of funded |")
    lines.append("|-------|-------------|")
    for theme, pct in sorted(alloc.theme_mix.items(), key=lambda x: -x[1]):
        lines.append(f"| {theme} | {pct}% |")
    lines.append("")
    lines.append("## Funded initiatives")
    lines.append("| ID | Name | Owner | Bucket | Cost | Score/$M |")
    lines.append("|----|------|-------|--------|------|----------|")
    for init in alloc.funded:
        lines.append(
            f"| {init.id} | {init.name} | {init.owner} | {init.bucket} | "
            f"${init.funded_amount:,.0f} | {init.score_per_dollar:.3f} |"
        )
    lines.append("")
    if alloc.deferred:
        lines.append("## Deferred initiatives")
        lines.append("| ID | Name | Cost | Reason |")
        lines.append("|----|------|------|--------|")
        for init in alloc.deferred:
            lines.append(
                f"| {init.id} | {init.name} | ${init.annual_cost_usd:,.0f} | {init.reason} |"
            )
        lines.append("")
    if alloc.warnings:
        lines.append("## Warnings")
        for w in alloc.warnings:
            lines.append(f"- {w}")
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Allocate AI budget across initiatives",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON file with initiatives")
    p.add_argument("--budget", required=True, help="Total budget (e.g., 5000000, 5M)")
    p.add_argument("--reserve-pct", type=float, default=10.0,
                  help="Percent of budget to hold in reserve (default 10)")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--output", help="Write to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"error: cannot read input: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 2

    try:
        budget = parse_amount(args.budget)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    weights = normalize_weights(raw.get("weights"))
    initiatives = load_initiatives(raw.get("initiatives", []))
    for init in initiatives:
        init.raw_score, init.adjusted_score, init.score_per_dollar = score_initiative(init, weights)

    alloc = allocate(initiatives, budget, args.reserve_pct)
    alloc.fiscal_period = raw.get("fiscal_period", "")
    alloc.currency = raw.get("currency", "USD")

    if args.format == "markdown":
        out = render_markdown(alloc)
    else:
        out = json.dumps({
            "fiscal_period": alloc.fiscal_period,
            "currency": alloc.currency,
            "budget": alloc.budget,
            "reserve": alloc.reserve,
            "funded_total": alloc.funded_total,
            "unspent": alloc.unspent,
            "bucket_mix": alloc.bucket_mix,
            "theme_mix": alloc.theme_mix,
            "weights_used": weights,
            "funded": [
                {
                    "id": i.id, "name": i.name, "owner": i.owner, "theme": i.theme,
                    "bucket": i.bucket, "annual_cost_usd": i.annual_cost_usd,
                    "raw_score": round(i.raw_score, 4),
                    "adjusted_score": round(i.adjusted_score, 4),
                    "score_per_dollar": round(i.score_per_dollar, 4),
                    "reason": i.reason,
                } for i in alloc.funded
            ],
            "deferred": [
                {
                    "id": i.id, "name": i.name, "annual_cost_usd": i.annual_cost_usd,
                    "reason": i.reason,
                } for i in alloc.deferred
            ],
            "warnings": alloc.warnings,
        }, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
