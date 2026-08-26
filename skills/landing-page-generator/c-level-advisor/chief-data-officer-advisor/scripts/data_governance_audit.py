#!/usr/bin/env python3
"""
data_governance_audit.py — Audit a data governance program against a
DAMA-DMBOK-aligned control catalog.

Reads a JSON describing the current governance state, evaluates ~25 controls
across 6 areas (Governance / Architecture / Quality / Security / Privacy /
Operations), assigns a pass/partial/fail per control, and emits a
remediation plan with owners and due dates.

Stdlib only.

Usage:
    python3 data_governance_audit.py --input governance_state.json
    python3 data_governance_audit.py --input governance_state.json --format markdown
    python3 data_governance_audit.py --input governance_state.json --output audit.md

Input schema (flat dict of control_id -> boolean or string):
{
  "as_of": "2026-05-27",
  "scope": "Acme Group — global data org",
  "auditor": "Internal audit",
  "controls": {
      "GOV-01-policy-published": true,
      "GOV-02-council-active": true,
      "GOV-03-working-group-active": true,
      ...
  },
  "evidence": {
      "GOV-01-policy-published": "link to policy v2.3 dated 2026-04-10"
  },
  "owners": {
      "GOV-01-policy-published": "CDO"
  }
}
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any


@dataclass
class Control:
    control_id: str
    area: str
    title: str
    description: str
    weight: int = 1
    default_owner: str = "Data governance lead"
    remediation_days: int = 60


CONTROL_CATALOG: list[Control] = [
    # GOVERNANCE
    Control("GOV-01-policy-published", "governance", "Data governance policy published and signed",
            "A signed policy exists and is communicated to all employees.", weight=2,
            default_owner="CDO", remediation_days=45),
    Control("GOV-02-council-active", "governance", "Data council meets at least quarterly",
            "Executive council with documented agenda, decisions, and attendance.", weight=2,
            default_owner="CDO"),
    Control("GOV-03-working-group-active", "governance", "Governance working group meets at least monthly",
            "Technical working group with stewards, platform, privacy, security.", weight=1,
            default_owner="Head of data governance"),
    Control("GOV-04-roles-published", "governance", "Owners, stewards, custodians documented",
            "RACI per critical domain; ownership coverage ≥80% of in-scope domains.", weight=2,
            default_owner="Head of data governance"),
    Control("GOV-05-classification-scheme", "governance", "Classification scheme published and wired to access",
            "4-tier (or equivalent) scheme; classification drives access controls.", weight=2,
            default_owner="CISO + CDO"),
    Control("GOV-06-internal-audit-quarterly", "governance", "Internal audit runs at least quarterly",
            "Findings logged with owner and due date; resolution tracked.", weight=2,
            default_owner="Internal audit"),
    # ARCHITECTURE / METADATA
    Control("ARC-01-catalog-coverage", "architecture", "Catalog covers top 50 datasets",
            "Catalog certified for ≥50 datasets with owner, classification, lineage.", weight=2,
            default_owner="Head of data platform"),
    Control("ARC-02-lineage-critical", "architecture", "Lineage exists on critical datasets",
            "Column-level or dataset-level lineage on top critical datasets.", weight=1,
            default_owner="Head of data platform"),
    Control("ARC-03-reference-data", "architecture", "Reference data managed as code",
            "Country codes, currency, units, and equivalent maintained in versioned repo.", weight=1,
            default_owner="Head of data platform"),
    Control("ARC-04-master-data", "architecture", "MDM for customer or product (if needed)",
            "If MDM was identified as needed, an MDM process is operational.", weight=1,
            default_owner="Head of data governance"),
    # QUALITY
    Control("QUA-01-critical-slas", "quality", "Critical datasets have published SLAs",
            "SLA includes freshness, completeness, accuracy, owner, on-call.", weight=2,
            default_owner="Head of data governance"),
    Control("QUA-02-sla-hit-rate", "quality", "Critical-dataset SLA hit rate ≥95%",
            "Rolling 90-day hit rate.", weight=2,
            default_owner="Head of data platform"),
    Control("QUA-03-automated-tests", "quality", "Quality tests automated in pipelines",
            "Tests run in CI / orchestrator; failures fail the run.", weight=2,
            default_owner="Head of data platform"),
    Control("QUA-04-incident-runbook", "quality", "Data incident runbook exists and is tested",
            "Runbook + at least one annual tabletop.", weight=2,
            default_owner="Head of data platform"),
    Control("QUA-05-postmortems", "quality", "Postmortems completed within 5 business days",
            "Action items tracked to closure.", weight=1,
            default_owner="Head of data platform"),
    # SECURITY
    Control("SEC-01-access-rbac", "security", "RBAC enforced for analytic platforms",
            "Roles tied to job function; reviewed at least annually.", weight=2,
            default_owner="CISO + CDO"),
    Control("SEC-02-abac-sensitive", "security", "ABAC for restricted data",
            "Row/column policies enforced for restricted scope.", weight=2,
            default_owner="CISO + CDO"),
    Control("SEC-03-access-logging", "security", "Access to restricted data is logged",
            "Audit logs centralized; anomaly alerts active.", weight=2,
            default_owner="CISO"),
    Control("SEC-04-jit-elevation", "security", "Just-in-time elevation supported",
            "Time-bound elevation with auto-expiry.", weight=1,
            default_owner="CISO"),
    Control("SEC-05-encryption", "security", "Encryption at rest and in transit",
            "Keys managed; rotation policy in effect.", weight=2,
            default_owner="CISO"),
    # PRIVACY
    Control("PRI-01-dsar-process", "privacy", "DSAR fulfillment automated",
            "Subject access requests fulfilled within statutory window (≤30 days for GDPR).",
            weight=2, default_owner="DPO / Privacy"),
    Control("PRI-02-retention", "privacy", "Retention policies enforced automatically",
            "Deletion on schedule; verifiable.", weight=2,
            default_owner="DPO / Privacy"),
    Control("PRI-03-consent", "privacy", "Consent records durable and queryable",
            "Consent records linked to processing activities.", weight=2,
            default_owner="DPO / Privacy"),
    Control("PRI-04-cross-border", "privacy", "Cross-border transfer posture documented",
            "SCCs / adequacy / residency choices documented and enforced.", weight=1,
            default_owner="DPO / Privacy"),
    Control("PRI-05-dpia", "privacy", "DPIAs completed for high-risk processing",
            "DPIA register exists; high-risk activities have DPIAs.", weight=1,
            default_owner="DPO / Privacy"),
    # OPERATIONS
    Control("OPS-01-change-mgmt", "operations", "Change management for production pipelines",
            "Schema and contract changes go through review with consumer notice ≥14 days.",
            weight=2, default_owner="Head of data platform"),
    Control("OPS-02-cost-attribution", "operations", "Cost attributed per data product",
            "Spend allocated to owning team / domain.", weight=1,
            default_owner="Head of data platform"),
    Control("OPS-03-on-call", "operations", "On-call rotation for critical pipelines",
            "Documented escalation path; pager configured.", weight=2,
            default_owner="Head of data platform"),
    Control("OPS-04-vendor-mgmt", "operations", "Third-party data vendor reviews documented",
            "Active vendor list reviewed annually; DPAs in place.", weight=1,
            default_owner="DPO / Privacy + procurement"),
]


def evaluate_status(control: Control, value: Any) -> str:
    if isinstance(value, bool):
        return "pass" if value else "fail"
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ("pass", "compliant", "true", "yes"):
            return "pass"
        if v in ("partial", "in-progress", "in_progress", "remediation"):
            return "partial"
        if v in ("fail", "non-compliant", "false", "no"):
            return "fail"
    return "fail"


def audit(state: dict[str, Any]) -> dict[str, Any]:
    controls_state = state.get("controls", {}) or {}
    evidence = state.get("evidence", {}) or {}
    owners = state.get("owners", {}) or {}

    today = date.today()
    results: list[dict[str, Any]] = []
    area_totals: dict[str, dict[str, int]] = {}
    total_weight = 0
    earned_weight = 0
    remediation: list[dict[str, Any]] = []

    for c in CONTROL_CATALOG:
        val = controls_state.get(c.control_id)
        status = evaluate_status(c, val)
        earned = c.weight if status == "pass" else (c.weight * 0.5 if status == "partial" else 0)
        total_weight += c.weight
        earned_weight += earned

        area_totals.setdefault(c.area, {"max": 0, "earned": 0, "fail": 0, "partial": 0, "pass": 0})
        area_totals[c.area]["max"] += c.weight
        area_totals[c.area]["earned"] += earned
        area_totals[c.area][status] += 1

        row = {
            "control_id": c.control_id,
            "area": c.area,
            "title": c.title,
            "description": c.description,
            "status": status,
            "weight": c.weight,
            "evidence": evidence.get(c.control_id, ""),
            "owner": owners.get(c.control_id, c.default_owner),
        }
        results.append(row)

        if status in ("fail", "partial"):
            due = (today + timedelta(days=c.remediation_days)).isoformat()
            remediation.append({
                "control_id": c.control_id,
                "area": c.area,
                "title": c.title,
                "current_status": status,
                "owner": owners.get(c.control_id, c.default_owner),
                "target_due_date": due,
                "priority": "high" if status == "fail" and c.weight >= 2 else "medium",
            })

    score = round((earned_weight / total_weight) * 100) if total_weight else 0
    area_scores = {
        area: round((d["earned"] / d["max"]) * 100) if d["max"] else 0
        for area, d in area_totals.items()
    }

    return {
        "as_of": state.get("as_of", ""),
        "scope": state.get("scope", ""),
        "auditor": state.get("auditor", ""),
        "overall_score": score,
        "area_scores": area_scores,
        "area_breakdown": area_totals,
        "controls": results,
        "remediation_plan": sorted(remediation,
                                  key=lambda r: (0 if r["priority"] == "high" else 1,
                                                 r["target_due_date"])),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Data Governance Audit — {report['scope'] or '(no scope)'}")
    lines.append(f"_as of {report['as_of']} | auditor: {report['auditor'] or '(unspecified)'}_\n")
    lines.append(f"## Overall score: **{report['overall_score']}/100**\n")
    lines.append("## Area scores")
    lines.append("| Area | Score | Pass | Partial | Fail |")
    lines.append("|------|-------|------|---------|------|")
    for area, score in report["area_scores"].items():
        b = report["area_breakdown"][area]
        lines.append(f"| {area} | {score}/100 | {b['pass']} | {b['partial']} | {b['fail']} |")
    lines.append("")
    lines.append("## Control results")
    lines.append("| Control | Area | Status | Owner |")
    lines.append("|---------|------|--------|-------|")
    for c in report["controls"]:
        status_icon = {"pass": "PASS", "partial": "PARTIAL", "fail": "FAIL"}[c["status"]]
        lines.append(f"| {c['control_id']} — {c['title']} | {c['area']} | {status_icon} | {c['owner']} |")
    lines.append("")
    if report["remediation_plan"]:
        lines.append("## Remediation plan")
        lines.append("| Priority | Control | Owner | Due |")
        lines.append("|----------|---------|-------|-----|")
        for r in report["remediation_plan"]:
            lines.append(
                f"| {r['priority']} | {r['control_id']} — {r['title']} | "
                f"{r['owner']} | {r['target_due_date']} |"
            )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Audit a data governance program against DAMA-DMBOK-aligned controls",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON file with governance state")
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

    report = audit(state)
    out = render_markdown(report) if args.format == "markdown" else json.dumps(report, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
