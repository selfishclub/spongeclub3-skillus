#!/usr/bin/env python3
"""
churn_intervention_planner.py — Prioritize at-risk accounts and recommend
interventions matched to risk driver and segment tier.

Reads a JSON of at-risk accounts; scores priority by ARR x risk x recoverability;
picks intervention(s) from a catalog keyed by primary driver and segment;
emits ordered list with owner and SLA.

Stdlib only. JSON or markdown output.

Usage:
    python3 churn_intervention_planner.py --input at_risk_accounts.json
    python3 churn_intervention_planner.py --input at_risk_accounts.json --format markdown

Input schema:
{
  "as_of": "2026-05-27",
  "accounts": [
      {
          "id": "ACC-001",
          "name": "Acme Inc",
          "segment": "enterprise",          # enterprise|mid-market|smb|plg
          "arr_usd": 250000,
          "health": "red",                  # red|yellow|green
          "risk_drivers": ["adoption-decline","sponsor-change"],
          "days_to_renewal": 75,
          "last_touch_days_ago": 28,
          "exec_sponsor_engaged": false,
          "support_open_p1": 0
      }
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


SEGMENT_TIER_FACTOR = {
    "enterprise": 1.0,
    "mid-market": 0.8,
    "smb": 0.5,
    "plg": 0.3,
}

HEALTH_FACTOR = {"red": 1.0, "yellow": 0.6, "green": 0.2}


# Intervention catalog — keyed by driver
INTERVENTIONS: dict[str, list[dict[str, Any]]] = {
    "adoption-decline": [
        {"action": "Adoption deep-dive workshop with power users", "owner": "CSM",
         "sla_days": 14, "applicable_segments": ["enterprise", "mid-market"]},
        {"action": "Triggered in-product campaign + email series to dormant users",
         "owner": "Lifecycle marketing", "sla_days": 7,
         "applicable_segments": ["smb", "plg", "mid-market"]},
        {"action": "Re-baseline success plan with the customer", "owner": "CSM",
         "sla_days": 21, "applicable_segments": ["enterprise"]},
    ],
    "sponsor-change": [
        {"action": "Multi-thread: identify and engage new sponsor + 2 backup contacts",
         "owner": "CSM", "sla_days": 14, "applicable_segments": ["enterprise", "mid-market"]},
        {"action": "Executive-to-executive intro from CCO to new sponsor",
         "owner": "CCO", "sla_days": 21, "applicable_segments": ["enterprise"]},
    ],
    "technical-gap": [
        {"action": "Engineering escalation + interim workaround + roadmap commitment",
         "owner": "Technical CSM + Eng", "sla_days": 14, "applicable_segments": ["enterprise", "mid-market"]},
        {"action": "Surface workaround in knowledge base; tag as theme",
         "owner": "Support + Product Marketing", "sla_days": 7,
         "applicable_segments": ["smb", "plg"]},
    ],
    "commercial-pressure": [
        {"action": "Pricing review + tier engineering proposal",
         "owner": "Renewals + Deal Desk", "sla_days": 21,
         "applicable_segments": ["enterprise", "mid-market"]},
        {"action": "Multi-year commitment exchange for stability",
         "owner": "Renewals", "sla_days": 30, "applicable_segments": ["enterprise"]},
    ],
    "competitive-threat": [
        {"action": "Win-loss style discovery + competitive battlecard refresh",
         "owner": "CSM + Product Marketing", "sla_days": 14,
         "applicable_segments": ["enterprise", "mid-market"]},
        {"action": "Demonstrated differentiator workshop with technical buyer",
         "owner": "Solutions / SE", "sla_days": 21,
         "applicable_segments": ["enterprise", "mid-market"]},
    ],
    "low-engagement": [
        {"action": "Executive check-in from CCO; cadence reset",
         "owner": "CCO", "sla_days": 14, "applicable_segments": ["enterprise"]},
        {"action": "Triggered automated outreach + persona re-segmentation",
         "owner": "Lifecycle marketing", "sla_days": 7,
         "applicable_segments": ["smb", "plg", "mid-market"]},
    ],
    "support-pain": [
        {"action": "Support escalation to senior engineer; root-cause within 5 days",
         "owner": "Support lead", "sla_days": 5,
         "applicable_segments": ["enterprise", "mid-market"]},
        {"action": "Compensation conversation if SLA breaches were material",
         "owner": "Renewals", "sla_days": 14,
         "applicable_segments": ["enterprise"]},
    ],
    "consolidation": [
        {"action": "Engage CFO + procurement directly with consolidation TCO scenario",
         "owner": "CCO + CFO partner", "sla_days": 21,
         "applicable_segments": ["enterprise"]},
        {"action": "Compete against the chosen consolidator with ROI proof",
         "owner": "Sales + CSM", "sla_days": 30,
         "applicable_segments": ["enterprise", "mid-market"]},
    ],
    "outcome-not-met": [
        {"action": "Joint outcome diagnostic with customer; reset success plan",
         "owner": "CSM + customer sponsor", "sla_days": 14,
         "applicable_segments": ["enterprise", "mid-market"]},
        {"action": "Services engagement to accelerate first value",
         "owner": "Services lead", "sla_days": 30,
         "applicable_segments": ["enterprise"]},
    ],
}


@dataclass
class Account:
    id: str
    name: str
    segment: str
    arr_usd: float
    health: str
    risk_drivers: list[str]
    days_to_renewal: int
    last_touch_days_ago: int
    exec_sponsor_engaged: bool
    support_open_p1: int
    priority_score: float = 0.0
    recoverability: float = 0.0
    interventions: list[dict[str, Any]] = field(default_factory=list)


def compute_recoverability(acct: Account) -> float:
    """0-1; higher = more recoverable based on time + sponsor + support state."""
    base = 0.5
    if acct.days_to_renewal > 90:
        base += 0.2
    elif acct.days_to_renewal > 60:
        base += 0.1
    elif acct.days_to_renewal < 30:
        base -= 0.2
    if acct.exec_sponsor_engaged:
        base += 0.15
    else:
        base -= 0.1
    if acct.last_touch_days_ago > 60:
        base -= 0.15
    if acct.support_open_p1 > 0:
        base -= 0.1
    return max(0.0, min(1.0, base))


def compute_priority(acct: Account) -> float:
    """Higher = more urgent."""
    tier = SEGMENT_TIER_FACTOR.get(acct.segment, 0.5)
    health = HEALTH_FACTOR.get(acct.health, 0.5)
    urgency = 1.0
    if acct.days_to_renewal <= 30:
        urgency = 1.5
    elif acct.days_to_renewal <= 60:
        urgency = 1.2
    elif acct.days_to_renewal <= 90:
        urgency = 1.0
    else:
        urgency = 0.8
    arr_score = min(1.0, acct.arr_usd / 500_000.0)
    return round(tier * health * urgency * (0.3 + 0.7 * arr_score) * acct.recoverability, 4)


def pick_interventions(acct: Account) -> list[dict[str, Any]]:
    picks: list[dict[str, Any]] = []
    for driver in acct.risk_drivers:
        candidates = INTERVENTIONS.get(driver, [])
        for c in candidates:
            if acct.segment in c["applicable_segments"]:
                picks.append({**c, "driver": driver})
    # Dedupe by action text
    seen = set()
    deduped = []
    for p in picks:
        if p["action"] not in seen:
            seen.add(p["action"])
            deduped.append(p)
    return deduped


def plan(accounts: list[dict[str, Any]]) -> list[Account]:
    out: list[Account] = []
    for r in accounts:
        a = Account(
            id=r.get("id", ""),
            name=r.get("name", ""),
            segment=r.get("segment", "smb").lower(),
            arr_usd=float(r.get("arr_usd", 0)),
            health=r.get("health", "yellow").lower(),
            risk_drivers=list(r.get("risk_drivers", []) or []),
            days_to_renewal=int(r.get("days_to_renewal", 365) or 365),
            last_touch_days_ago=int(r.get("last_touch_days_ago", 30) or 30),
            exec_sponsor_engaged=bool(r.get("exec_sponsor_engaged", False)),
            support_open_p1=int(r.get("support_open_p1", 0) or 0),
        )
        a.recoverability = compute_recoverability(a)
        a.priority_score = compute_priority(a)
        a.interventions = pick_interventions(a)
        out.append(a)
    out.sort(key=lambda x: x.priority_score, reverse=True)
    return out


def render_markdown(as_of: str, accounts: list[Account]) -> str:
    lines = []
    lines.append(f"# Churn Intervention Plan — {as_of or '(no date)'}")
    lines.append(f"\nTotal at-risk accounts: {len(accounts)}\n")
    total_arr = sum(a.arr_usd for a in accounts)
    lines.append(f"ARR at risk: ${total_arr:,.0f}\n")
    lines.append("## Prioritized account list")
    lines.append("| Rank | Account | Segment | ARR | Health | DTR | Priority | Recoverability |")
    lines.append("|------|---------|---------|-----|--------|-----|----------|----------------|")
    for i, a in enumerate(accounts, start=1):
        lines.append(
            f"| {i} | {a.name} | {a.segment} | ${a.arr_usd:,.0f} | {a.health} | "
            f"{a.days_to_renewal}d | {a.priority_score:.3f} | {a.recoverability:.2f} |"
        )
    lines.append("")
    lines.append("## Recommended interventions per account")
    for a in accounts:
        lines.append(f"### {a.name} ({a.id}) — priority {a.priority_score:.3f}")
        lines.append(f"_segment: {a.segment} | ARR: ${a.arr_usd:,.0f} | "
                    f"health: {a.health} | renewal in {a.days_to_renewal} days_")
        lines.append(f"Risk drivers: {', '.join(a.risk_drivers) or '(none provided)'}")
        if a.interventions:
            lines.append("\n**Interventions:**")
            for iv in a.interventions:
                lines.append(
                    f"- ({iv['driver']}) {iv['action']} — owner: {iv['owner']}, SLA: {iv['sla_days']} days"
                )
        else:
            lines.append("\n_No interventions matched; consider executive review._")
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Prioritize at-risk accounts and recommend interventions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON file with at-risk accounts")
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

    accounts = plan(raw.get("accounts", []))

    if args.format == "markdown":
        out = render_markdown(raw.get("as_of", ""), accounts)
    else:
        out = json.dumps({
            "as_of": raw.get("as_of", ""),
            "total_accounts": len(accounts),
            "total_arr_at_risk_usd": sum(a.arr_usd for a in accounts),
            "accounts": [
                {
                    "id": a.id, "name": a.name, "segment": a.segment,
                    "arr_usd": a.arr_usd, "health": a.health,
                    "days_to_renewal": a.days_to_renewal,
                    "last_touch_days_ago": a.last_touch_days_ago,
                    "exec_sponsor_engaged": a.exec_sponsor_engaged,
                    "support_open_p1": a.support_open_p1,
                    "risk_drivers": a.risk_drivers,
                    "priority_score": a.priority_score,
                    "recoverability": a.recoverability,
                    "interventions": a.interventions,
                }
                for a in accounts
            ],
        }, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
