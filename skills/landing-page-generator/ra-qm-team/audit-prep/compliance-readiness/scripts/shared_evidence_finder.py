#!/usr/bin/env python3
"""
shared_evidence_finder.py — Identify controls shared across multiple compliance frameworks.

For specified frameworks, emit list of overlapping controls and the evidence
that satisfies multiple frameworks simultaneously. Output is a shared-control
catalog to guide GRC platform mapping or manual evidence organization.

Stdlib only. Markdown or JSON.

Usage:
    python3 shared_evidence_finder.py --frameworks SOC2,ISO27001,NIST_CSF
    python3 shared_evidence_finder.py --frameworks SOC2,GDPR --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import Any


# Shared-control catalog: control name → frameworks it satisfies + evidence type
SHARED_CONTROLS = {
    "info_security_policy_signed": {
        "frameworks": ["SOC2:CC1.1", "ISO27001:5.2", "NIST_CSF:GV.PO", "HIPAA:§164.308(a)(1)", "PCI_DSS:12.1"],
        "evidence_type": "Signed policy document with approval signatures",
        "cadence": "Annual review",
        "owner": "CISO / Information Security Manager",
    },
    "annual_risk_assessment": {
        "frameworks": ["SOC2:CC3.1", "ISO27001:6.1.2", "NIST_CSF:ID.RA", "HIPAA:§164.308(a)(1)", "GDPR:Art.35"],
        "evidence_type": "Risk assessment report; risk register",
        "cadence": "Annual",
        "owner": "Risk Manager / Compliance",
    },
    "access_review_quarterly": {
        "frameworks": ["SOC2:CC6.3", "ISO27001:A.5.18", "NIST_CSF:PR.AA-04", "HIPAA:§164.308(a)(4)", "PCI_DSS:7.2.4"],
        "evidence_type": "Quarterly access review records with sign-off",
        "cadence": "Quarterly",
        "owner": "IT Security",
    },
    "mfa_universal_production": {
        "frameworks": ["SOC2:CC6.1", "ISO27001:A.8.5", "NIST_CSF:PR.AA-02", "PCI_DSS:8.4", "DORA:Art.9"],
        "evidence_type": "IdP MFA enforcement screenshot + exception register",
        "cadence": "Continuous",
        "owner": "IT Security",
    },
    "encryption_at_rest_in_transit": {
        "frameworks": ["SOC2:CC6.7", "ISO27001:A.8.24", "NIST_CSF:PR.DS-01/02", "HIPAA:§164.312(a)(2)(iv)", "PCI_DSS:3.4/4.1", "GDPR:Art.32"],
        "evidence_type": "Encryption configuration evidence per system; KMS access logs",
        "cadence": "Continuous; annual review",
        "owner": "IT Security",
    },
    "vulnerability_scanning_with_remediation": {
        "frameworks": ["SOC2:CC7.1", "ISO27001:A.8.8", "NIST_CSF:ID.RA-01", "PCI_DSS:11.3"],
        "evidence_type": "Scan reports + remediation tracking",
        "cadence": "Monthly minimum; weekly preferred",
        "owner": "Security Operations",
    },
    "annual_pen_test": {
        "frameworks": ["SOC2:CC4.1", "ISO27001:A.5.7", "PCI_DSS:11.4"],
        "evidence_type": "Pen test report from qualified 3rd party",
        "cadence": "Annual",
        "owner": "Security",
    },
    "incident_response_runbook": {
        "frameworks": ["SOC2:CC7.3", "ISO27001:A.5.24", "NIST_CSF:RS.MA", "HIPAA:§164.308(a)(6)", "PCI_DSS:12.10", "GDPR:Art.33", "NIS2:Art.23"],
        "evidence_type": "IR runbook + past-period incident records",
        "cadence": "Quarterly review; per-incident records",
        "owner": "Security Operations / SRE",
    },
    "vendor_due_diligence_records": {
        "frameworks": ["SOC2:CC9.2", "ISO27001:A.5.19", "NIST_CSF:GV.SC-04", "HIPAA:§164.308(b)", "PCI_DSS:12.8", "DORA:Art.28", "GDPR:Art.28"],
        "evidence_type": "Vendor SOC 2 reports, DPAs, BAAs, qualification records",
        "cadence": "Annual per vendor",
        "owner": "Vendor Manager / Procurement",
    },
    "code_review_and_change_approval": {
        "frameworks": ["SOC2:CC8.1", "ISO27001:A.5.36/A.8.32", "NIST_CSF:PR.PS-06", "PCI_DSS:6.5"],
        "evidence_type": "PR records + production deploy approvals",
        "cadence": "Per change",
        "owner": "Engineering Lead",
    },
    "dr_test_results": {
        "frameworks": ["SOC2:A1.3", "ISO27001:A.5.30", "NIST_CSF:RC.RP", "HIPAA:§164.308(a)(7)", "NIS2:Art.21.2(c)", "DORA:Art.11"],
        "evidence_type": "Annual DR test report",
        "cadence": "Annual",
        "owner": "DR Coordinator / IT Ops",
    },
    "backup_restore_testing": {
        "frameworks": ["SOC2:A1.2", "ISO27001:A.8.13", "NIST_CSF:PR.DS-11", "HIPAA:§164.308(a)(7)(ii)(A)"],
        "evidence_type": "Quarterly restore test records",
        "cadence": "Quarterly",
        "owner": "IT Ops",
    },
    "security_awareness_training": {
        "frameworks": ["SOC2:CC1.4", "ISO27001:A.6.3", "NIST_CSF:PR.AT-01", "HIPAA:§164.308(a)(5)", "PCI_DSS:12.6", "NIS2:Art.21.2(g)", "DORA:Art.13", "GDPR:Art.39"],
        "evidence_type": "Training completion records (annual)",
        "cadence": "Annual",
        "owner": "HR + Security",
    },
    "background_checks": {
        "frameworks": ["SOC2:CC1.1", "ISO27001:A.6.1"],
        "evidence_type": "Background check records per hire",
        "cadence": "Per hire",
        "owner": "HR",
    },
    "management_review_annual": {
        "frameworks": ["SOC2:CC1.2", "ISO27001:9.3", "ISO42001:9.3"],
        "evidence_type": "Annual management review minutes + actions",
        "cadence": "Annual",
        "owner": "Compliance / Quality",
    },
    "internal_audit": {
        "frameworks": ["SOC2:CC4.1", "ISO27001:9.2", "ISO42001:9.2"],
        "evidence_type": "Internal audit reports + finding closures",
        "cadence": "Annual",
        "owner": "Internal Audit",
    },
}


@dataclass
class SharedControl:
    control: str
    frameworks_satisfied: list[str]
    evidence_type: str
    cadence: str
    owner: str
    framework_count: int


@dataclass
class Report:
    target_frameworks: list[str]
    total_shared_controls: int
    fully_shared_controls_count: int
    shared_controls: list[SharedControl]
    summary_by_owner: dict[str, int]


def find_shared_controls(target_frameworks: list[str]) -> Report:
    shared: list[SharedControl] = []
    fully_shared = 0
    by_owner: dict[str, int] = {}
    for control_name, info in SHARED_CONTROLS.items():
        # Check which target frameworks this control satisfies
        frameworks_list = info["frameworks"]
        satisfies_targets = []
        for fw in target_frameworks:
            for entry in frameworks_list:
                if entry.startswith(fw + ":") or entry.startswith(fw + ".") or entry == fw:
                    satisfies_targets.append(entry)
                    break
        if len(satisfies_targets) >= 2:
            sc = SharedControl(
                control=control_name,
                frameworks_satisfied=satisfies_targets,
                evidence_type=str(info["evidence_type"]),
                cadence=str(info["cadence"]),
                owner=str(info["owner"]),
                framework_count=len(satisfies_targets),
            )
            shared.append(sc)
            if len(satisfies_targets) == len(target_frameworks):
                fully_shared += 1
            by_owner[str(info["owner"])] = by_owner.get(str(info["owner"]), 0) + 1
    return Report(
        target_frameworks=target_frameworks,
        total_shared_controls=len(shared),
        fully_shared_controls_count=fully_shared,
        shared_controls=sorted(shared, key=lambda x: -x.framework_count),
        summary_by_owner=by_owner,
    )


def render_markdown(r: Report) -> str:
    out = ["# Shared-Control Catalog", ""]
    out.append(f"_Target frameworks: {', '.join(r.target_frameworks)}_")
    out.append("")
    out.append(f"- **Shared controls (across >=2 target frameworks)**: {r.total_shared_controls}")
    out.append(f"- **Controls satisfying ALL target frameworks**: {r.fully_shared_controls_count}")
    out.append("")
    out.append("## Shared Controls (sorted by framework coverage)")
    out.append("")
    out.append("| Control | Frameworks Satisfied | Evidence | Cadence | Owner |")
    out.append("|---------|----------------------|----------|---------|-------|")
    for sc in r.shared_controls:
        frameworks = ", ".join(sc.frameworks_satisfied)
        out.append(f"| {sc.control} | {frameworks} | {sc.evidence_type[:60]} | {sc.cadence} | {sc.owner} |")
    out.append("")
    out.append("## Workload by Owner")
    out.append("")
    out.append("| Owner | Shared Controls |")
    out.append("|-------|-----------------|")
    for owner, count in sorted(r.summary_by_owner.items(), key=lambda x: -x[1]):
        out.append(f"| {owner} | {count} |")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Find shared controls across compliance frameworks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--frameworks", required=True, help="Comma-separated framework codes (SOC2, ISO27001, NIST_CSF, GDPR, HIPAA, PCI_DSS, DORA, NIS2)")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", help="Output file path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    frameworks = [f.strip() for f in args.frameworks.split(",")]
    r = find_shared_controls(frameworks)
    if args.format == "json":
        out = json.dumps(asdict(r), indent=2)
    else:
        out = render_markdown(r)
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
