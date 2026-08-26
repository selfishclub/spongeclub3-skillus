#!/usr/bin/env python3
"""
legal_risk_register.py — Build and prioritize a legal risk register across
7 categories: commercial, regulatory, privacy, security, ip, employment,
corporate, litigation.

Reads a JSON of risk entries; scores Exposure = Severity x Likelihood and
adjusts for mitigation strength; assigns suggested owner and review cadence;
emits prioritized register.

Stdlib only. JSON or markdown output.

Usage:
    python3 legal_risk_register.py --input legal_risks.json
    python3 legal_risk_register.py --input legal_risks.json --format markdown
    python3 legal_risk_register.py --input legal_risks.json --top-n 10

Input schema:
{
  "as_of": "2026-05-27",
  "org_name": "Acme",
  "risks": [
      {
          "id": "LR-001",
          "title": "Customer data residency obligations under GDPR",
          "category": "privacy",          # commercial|regulatory|privacy|security|ip|employment|corporate|litigation
          "description": "EU customers requiring data residency in EU; current arch in US-East.",
          "severity": 4,                  # 1-5
          "likelihood": 4,                # 1-5
          "velocity": 2,                  # 1-3
          "detection": 2,                 # 1-3 (lower = harder to detect early)
          "mitigation_strength": 2,       # 0-5
          "current_controls": ["DPAs in place","SCC for transfer"],
          "owner_hint": "DPO + GC"
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


VALID_CATEGORIES = {
    "commercial", "regulatory", "privacy", "security",
    "ip", "employment", "corporate", "litigation",
}


CATEGORY_OWNERS = {
    "commercial": "Commercial counsel",
    "regulatory": "Regulatory counsel + sector lead",
    "privacy": "DPO + Privacy counsel",
    "security": "CISO + Security counsel",
    "ip": "IP counsel + outside IP firm",
    "employment": "Employment counsel + CHRO",
    "corporate": "Corporate counsel + CFO",
    "litigation": "Litigation counsel + GC",
}


@dataclass
class Risk:
    id: str
    title: str
    category: str
    description: str
    severity: int
    likelihood: int
    velocity: int = 2
    detection: int = 2
    mitigation_strength: int = 0
    current_controls: list[str] = field(default_factory=list)
    owner_hint: str = ""
    exposure: int = 0
    adjusted_exposure: float = 0.0
    priority_band: str = ""
    review_cadence_months: int = 6
    suggested_owner: str = ""


def assess(r: dict[str, Any]) -> Risk:
    sev = max(1, min(5, int(r.get("severity", 1) or 1)))
    lik = max(1, min(5, int(r.get("likelihood", 1) or 1)))
    vel = max(1, min(3, int(r.get("velocity", 2) or 2)))
    det = max(1, min(3, int(r.get("detection", 2) or 2)))
    mit = max(0, min(5, int(r.get("mitigation_strength", 0) or 0)))
    cat = (r.get("category") or "commercial").lower()
    if cat not in VALID_CATEGORIES:
        cat = "commercial"

    exposure = sev * lik
    # Velocity multiplier (faster = higher adjusted exposure)
    vel_mult = {1: 0.85, 2: 1.0, 3: 1.2}[vel]
    # Detection multiplier (harder = higher adjusted exposure)
    det_mult = {1: 1.2, 2: 1.0, 3: 0.85}[det]
    # Mitigation discount
    mit_discount = 1.0 - (mit / 10.0)  # 0 = no discount, 5 = 50% discount

    adj = round(exposure * vel_mult * det_mult * mit_discount, 2)

    if adj >= 18:
        band = "critical"
        cadence = 1
    elif adj >= 12:
        band = "high"
        cadence = 3
    elif adj >= 6:
        band = "medium"
        cadence = 6
    else:
        band = "low"
        cadence = 12

    risk = Risk(
        id=r.get("id", ""),
        title=r.get("title", ""),
        category=cat,
        description=r.get("description", ""),
        severity=sev,
        likelihood=lik,
        velocity=vel,
        detection=det,
        mitigation_strength=mit,
        current_controls=list(r.get("current_controls", []) or []),
        owner_hint=r.get("owner_hint", ""),
        exposure=exposure,
        adjusted_exposure=adj,
        priority_band=band,
        review_cadence_months=cadence,
        suggested_owner=r.get("owner_hint") or CATEGORY_OWNERS.get(cat, "GC"),
    )
    return risk


def build_register(raw: dict[str, Any]) -> dict[str, Any]:
    risks = [assess(r) for r in raw.get("risks", [])]
    risks.sort(key=lambda x: x.adjusted_exposure, reverse=True)

    by_cat: dict[str, list[Risk]] = {}
    band_counts: dict[str, int] = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for r in risks:
        by_cat.setdefault(r.category, []).append(r)
        band_counts[r.priority_band] += 1

    return {
        "as_of": raw.get("as_of", ""),
        "org_name": raw.get("org_name", ""),
        "total_risks": len(risks),
        "band_counts": band_counts,
        "category_counts": {k: len(v) for k, v in by_cat.items()},
        "risks": [
            {
                "id": r.id, "title": r.title, "category": r.category,
                "description": r.description,
                "severity": r.severity, "likelihood": r.likelihood,
                "velocity": r.velocity, "detection": r.detection,
                "mitigation_strength": r.mitigation_strength,
                "exposure": r.exposure, "adjusted_exposure": r.adjusted_exposure,
                "priority_band": r.priority_band,
                "review_cadence_months": r.review_cadence_months,
                "current_controls": r.current_controls,
                "suggested_owner": r.suggested_owner,
            }
            for r in risks
        ],
    }


def render_markdown(report: dict[str, Any], top_n: int | None) -> str:
    lines = []
    lines.append(f"# Legal Risk Register — {report.get('org_name','(unnamed)')}")
    lines.append(f"_as of {report['as_of']}_\n")
    lines.append(f"Total risks: {report['total_risks']}")
    b = report["band_counts"]
    lines.append(f"By band: critical {b['critical']} | high {b['high']} | medium {b['medium']} | low {b['low']}")
    cc = report["category_counts"]
    lines.append("By category: " + ", ".join(f"{k} {v}" for k, v in sorted(cc.items())))
    lines.append("")
    risks = report["risks"]
    if top_n:
        risks = risks[:top_n]
        lines.append(f"## Top {top_n} risks by adjusted exposure\n")
    else:
        lines.append("## All risks by adjusted exposure\n")
    lines.append("| ID | Title | Category | Sev | Lik | Adj. Exp | Band | Owner | Review |")
    lines.append("|----|-------|----------|-----|-----|----------|------|-------|--------|")
    for r in risks:
        lines.append(
            f"| {r['id']} | {r['title']} | {r['category']} | {r['severity']} | {r['likelihood']} | "
            f"{r['adjusted_exposure']} | {r['priority_band']} | {r['suggested_owner']} | "
            f"{r['review_cadence_months']}mo |"
        )
    lines.append("")
    lines.append("## Risk detail")
    for r in risks:
        lines.append(f"### {r['id']} — {r['title']}")
        lines.append(f"_{r['category']} | severity {r['severity']} | likelihood {r['likelihood']} | "
                    f"adjusted exposure {r['adjusted_exposure']} ({r['priority_band']})_")
        if r["description"]:
            lines.append(f"\n{r['description']}")
        if r["current_controls"]:
            lines.append("\n**Current controls:**")
            for c in r["current_controls"]:
                lines.append(f"- {c}")
        lines.append(f"\n**Suggested owner:** {r['suggested_owner']}")
        lines.append(f"**Review cadence:** {r['review_cadence_months']} months")
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Build a prioritized legal risk register",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON with risks")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--top-n", type=int, help="Limit register to top N (markdown only)")
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

    report = build_register(raw)
    if args.format == "markdown":
        out = render_markdown(report, args.top_n)
    else:
        if args.top_n:
            report["risks"] = report["risks"][:args.top_n]
        out = json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
