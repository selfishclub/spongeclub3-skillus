#!/usr/bin/env python3
"""
ai_risk_register_generator.py — Seed an AI risk register from a list of
AI systems, aligned to NIST AI RMF, ISO 42001, or EU AI Act.

Reads a JSON of AI systems (production + planned), enumerates relevant
risks per system based on attributes (modality, data sensitivity, criticality,
risk tier), maps each risk to framework controls, suggests owners, and
emits the register as JSON or markdown.

Stdlib only.

Usage:
    python3 ai_risk_register_generator.py --input ai_systems.json
    python3 ai_risk_register_generator.py --input ai_systems.json --framework nist-ai-rmf
    python3 ai_risk_register_generator.py --input ai_systems.json --framework iso-42001 --format markdown
    python3 ai_risk_register_generator.py --input ai_systems.json --framework eu-ai-act --output register.md

Input schema:
{
  "as_of": "2026-05-27",
  "systems": [
      {
          "id": "AIS-001",
          "name": "Customer support copilot",
          "owner": "Product Support",
          "modality": ["text"],                 # text|vision|audio|multimodal|tabular
          "model_type": "llm-via-vendor",       # llm-via-vendor|llm-fine-tuned|classical-ml|cv|asr|other
          "data_sensitivity": "high",           # low|medium|high
          "pii": true,
          "criticality": "medium",              # low|medium|high
          "user_population": "external-customers",  # internal|external-customers|public
          "uses_agent_tools": false,
          "automated_decision": false,
          "annex_iii_category": null,           # eu-ai-act Annex III category if applicable
          "deployment": "production"            # planned|pilot|production
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


# Risk catalog — each entry has trigger predicates (functions) and content.
# We avoid lambdas in the JSON-serializable layer by representing triggers as
# a list of (attr, predicate) tuples evaluated in Python.

@dataclass
class Risk:
    risk_id: str
    category: str
    title: str
    description: str
    severity: str            # low|medium|high|critical
    likelihood: str          # low|medium|high
    mitigations: list[str] = field(default_factory=list)
    nist_ai_rmf: list[str] = field(default_factory=list)
    iso_42001: list[str] = field(default_factory=list)
    eu_ai_act: list[str] = field(default_factory=list)
    suggested_owner: str = ""


def base_risks() -> list[Risk]:
    return [
        Risk(
            risk_id="R-MODEL-HALLUC",
            category="model",
            title="Inaccurate or fabricated output (hallucination)",
            description="Model returns confident but factually wrong content.",
            severity="high", likelihood="high",
            mitigations=[
                "RAG with cited sources",
                "Eval set with adversarial prompts",
                "Confidence threshold + abstain path",
                "Human-in-the-loop for high-stakes responses",
            ],
            nist_ai_rmf=["Measure 2.3", "Measure 2.5", "Manage 1.3"],
            iso_42001=["Annex A.6.2.4 (system performance)", "Annex A.6.2.6 (oversight)"],
            eu_ai_act=["Art. 15 (accuracy/robustness)"],
        ),
        Risk(
            risk_id="R-MODEL-BIAS",
            category="model",
            title="Bias / unfair subgroup performance",
            description="Quality varies materially across protected subgroups.",
            severity="high", likelihood="medium",
            mitigations=[
                "Subgroup eval set",
                "Pre-deployment fairness review",
                "Ongoing subgroup metric monitoring",
            ],
            nist_ai_rmf=["Measure 2.11", "Manage 2.1"],
            iso_42001=["Annex A.6.2.4", "Annex A.7.4"],
            eu_ai_act=["Art. 10 (data governance)", "Art. 15"],
        ),
        Risk(
            risk_id="R-MODEL-DRIFT",
            category="model",
            title="Distribution shift / drift",
            description="Inputs or world change such that the model degrades silently.",
            severity="medium", likelihood="high",
            mitigations=[
                "Input + output drift detectors",
                "Scheduled re-eval against frozen test set",
                "Re-train / re-prompt cadence",
            ],
            nist_ai_rmf=["Measure 2.7", "Manage 4.1"],
            iso_42001=["Annex A.6.2.4"],
            eu_ai_act=["Art. 15", "Art. 72 (post-market monitoring)"],
        ),
        Risk(
            risk_id="R-DATA-LINEAGE",
            category="data",
            title="Incomplete data lineage",
            description="Cannot prove provenance of training or retrieval data.",
            severity="medium", likelihood="medium",
            mitigations=[
                "Source register per dataset",
                "Lineage tooling (e.g., column-level)",
                "Quarterly audit",
            ],
            nist_ai_rmf=["Map 2.2", "Govern 1.4"],
            iso_42001=["Annex A.7.2 (data acquisition)", "Annex A.7.3"],
            eu_ai_act=["Art. 10 (data governance)"],
        ),
    ]


def llm_risks() -> list[Risk]:
    return [
        Risk(
            risk_id="R-SEC-PROMPT-INJ",
            category="security",
            title="Prompt injection (direct + indirect)",
            description="Untrusted text overrides system intent.",
            severity="high", likelihood="high",
            mitigations=[
                "Treat retrieved content as untrusted",
                "Output filter on tool calls",
                "Allow-list of tools per agent role",
                "Red team for jailbreaks (continuous)",
            ],
            nist_ai_rmf=["Measure 2.6", "Manage 2.3"],
            iso_42001=["Annex A.8 (security)", "Annex A.6.2.4"],
            eu_ai_act=["Art. 15 (cybersecurity)"],
        ),
        Risk(
            risk_id="R-SEC-DATA-EXFIL",
            category="security",
            title="Sensitive data exfiltration via model",
            description="Confidential data leaves the boundary in outputs or vendor logs.",
            severity="critical", likelihood="medium",
            mitigations=[
                "DLP on inputs and outputs",
                "No-training contract terms with vendor",
                "Tenant isolation for foundation-model traffic",
            ],
            nist_ai_rmf=["Manage 2.2", "Manage 4.3"],
            iso_42001=["Annex A.8", "Annex A.9 (supplier)"],
            eu_ai_act=["Art. 15", "Art. 26 (deployer obligations)"],
        ),
    ]


def pii_risks() -> list[Risk]:
    return [
        Risk(
            risk_id="R-PRIV-LEAK",
            category="privacy",
            title="PII disclosure in outputs or logs",
            description="Personal data is revealed via outputs or persisted in logs without basis.",
            severity="critical", likelihood="medium",
            mitigations=[
                "PII redaction on input/output",
                "Log retention policy + access control",
                "Privacy review at intake",
            ],
            nist_ai_rmf=["Measure 2.10", "Manage 2.2"],
            iso_42001=["Annex A.7.4", "Annex A.8"],
            eu_ai_act=["Art. 10", "interaction with GDPR Art. 5/32/35"],
        ),
    ]


def agent_risks() -> list[Risk]:
    return [
        Risk(
            risk_id="R-OPS-AGENT-LOOP",
            category="operational",
            title="Agent loop / cost runaway",
            description="Agent gets stuck or makes excessive tool calls.",
            severity="medium", likelihood="medium",
            mitigations=[
                "Per-session step + cost cap",
                "Anomaly alert on token usage",
                "Kill switch tied to spend budget",
            ],
            nist_ai_rmf=["Manage 1.2", "Manage 4.1"],
            iso_42001=["Annex A.6.2.4"],
            eu_ai_act=["Art. 15 (robustness)"],
        ),
        Risk(
            risk_id="R-OPS-AGENT-ACTION",
            category="operational",
            title="Unauthorized agent action in systems of record",
            description="Agent takes a side-effecting action it shouldn't.",
            severity="high", likelihood="medium",
            mitigations=[
                "Allow-list of tools per role",
                "Human approval for irreversible actions",
                "Dry-run mode and audit trail",
            ],
            nist_ai_rmf=["Manage 3.2"],
            iso_42001=["Annex A.6.2.6 (oversight)"],
            eu_ai_act=["Art. 14 (human oversight)"],
        ),
    ]


def auto_decision_risks() -> list[Risk]:
    return [
        Risk(
            risk_id="R-COMP-AUTO-DECISION",
            category="compliance",
            title="Automated decision affecting individuals without recourse",
            description="System makes a decision impacting rights/access without human review or appeal path.",
            severity="high", likelihood="medium",
            mitigations=[
                "Human review path on negative decisions",
                "Explanation surfaced to affected user",
                "Documented appeal process",
            ],
            nist_ai_rmf=["Govern 1.5", "Manage 3.2"],
            iso_42001=["Annex A.6.2.6"],
            eu_ai_act=["Art. 14", "Art. 86 (right to explanation)"],
        ),
    ]


def high_risk_eu_aiact_risks() -> list[Risk]:
    return [
        Risk(
            risk_id="R-COMP-EU-CONFORMITY",
            category="compliance",
            title="High-risk system without conformity assessment",
            description="System falls under Annex III; conformity assessment and CE mark required.",
            severity="critical", likelihood="medium",
            mitigations=[
                "Run conformity assessment workflow",
                "Maintain technical documentation (Annex IV)",
                "Stand up post-market monitoring",
                "Define serious-incident reporting path (15 days; immediate for fundamental rights)",
            ],
            nist_ai_rmf=["Govern 2.1", "Map 1.1"],
            iso_42001=["Clauses 6.1, 8.2"],
            eu_ai_act=["Art. 16-29 (provider obligations)", "Art. 43 (conformity)", "Art. 72-73"],
        ),
    ]


def assemble_risks_for_system(system: dict[str, Any]) -> list[Risk]:
    risks: list[Risk] = list(base_risks())
    model_type = (system.get("model_type") or "").lower()
    modalities = [m.lower() for m in (system.get("modality") or [])]
    if "llm" in model_type or "text" in modalities or "multimodal" in modalities:
        risks.extend(llm_risks())
    if system.get("pii") or (system.get("data_sensitivity") or "").lower() == "high":
        risks.extend(pii_risks())
    if system.get("uses_agent_tools"):
        risks.extend(agent_risks())
    if system.get("automated_decision"):
        risks.extend(auto_decision_risks())
    if system.get("annex_iii_category"):
        risks.extend(high_risk_eu_aiact_risks())
    return risks


def suggest_owner(system: dict[str, Any], risk: Risk) -> str:
    if risk.category == "security":
        return "CISO"
    if risk.category == "privacy":
        return "DPO / Privacy"
    if risk.category == "compliance":
        return "GC + AI Governance"
    return system.get("owner") or "AI System Owner"


def filter_for_framework(risk: Risk, framework: str) -> dict[str, Any]:
    base = {
        "risk_id": risk.risk_id,
        "category": risk.category,
        "title": risk.title,
        "description": risk.description,
        "severity": risk.severity,
        "likelihood": risk.likelihood,
        "mitigations": risk.mitigations,
    }
    if framework == "nist-ai-rmf":
        base["nist_ai_rmf"] = risk.nist_ai_rmf
    elif framework == "iso-42001":
        base["iso_42001"] = risk.iso_42001
    elif framework == "eu-ai-act":
        base["eu_ai_act"] = risk.eu_ai_act
    else:
        base["nist_ai_rmf"] = risk.nist_ai_rmf
        base["iso_42001"] = risk.iso_42001
        base["eu_ai_act"] = risk.eu_ai_act
    return base


def build_register(systems: list[dict[str, Any]], framework: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seq = 0
    for sys_ in systems:
        risks = assemble_risks_for_system(sys_)
        for risk in risks:
            seq += 1
            r = filter_for_framework(risk, framework)
            r["entry_id"] = f"AIRR-{seq:04d}"
            r["system_id"] = sys_.get("id", "")
            r["system_name"] = sys_.get("name", "")
            r["system_deployment"] = sys_.get("deployment", "")
            r["suggested_owner"] = suggest_owner(sys_, risk)
            r["review_cadence_months"] = 3 if r["severity"] in ("high", "critical") else 6
            rows.append(r)
    return rows


def render_markdown(register: list[dict[str, Any]], framework: str, as_of: str) -> str:
    lines = []
    lines.append(f"# AI Risk Register — framework: {framework}")
    lines.append(f"_as of {as_of}_\n")
    lines.append(f"Total entries: {len(register)}\n")
    by_system: dict[str, list[dict[str, Any]]] = {}
    for r in register:
        by_system.setdefault(r["system_name"] or r["system_id"], []).append(r)
    for name, rows in by_system.items():
        lines.append(f"## System: {name}")
        lines.append(f"_{len(rows)} risks identified_\n")
        lines.append("| Entry | Risk | Category | Severity | Likelihood | Owner | Review |")
        lines.append("|-------|------|----------|----------|------------|-------|--------|")
        for r in rows:
            lines.append(
                f"| {r['entry_id']} | {r['title']} | {r['category']} | "
                f"{r['severity']} | {r['likelihood']} | {r['suggested_owner']} | "
                f"{r['review_cadence_months']}mo |"
            )
        lines.append("")
        for r in rows:
            lines.append(f"### {r['entry_id']} — {r['title']}")
            lines.append(f"**Description:** {r['description']}")
            lines.append("")
            lines.append("**Mitigations:**")
            for m in r["mitigations"]:
                lines.append(f"- {m}")
            framework_keys = [k for k in ("nist_ai_rmf", "iso_42001", "eu_ai_act") if k in r]
            for fk in framework_keys:
                if r[fk]:
                    label = {"nist_ai_rmf": "NIST AI RMF",
                             "iso_42001": "ISO 42001",
                             "eu_ai_act": "EU AI Act"}[fk]
                    lines.append(f"**{label}:** {', '.join(r[fk])}")
            lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Seed an AI risk register aligned to a chosen framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON file with AI systems")
    p.add_argument("--framework",
                  choices=["nist-ai-rmf", "iso-42001", "eu-ai-act", "all"],
                  default="all")
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

    systems = raw.get("systems", [])
    register = build_register(systems, args.framework)

    if args.format == "markdown":
        out = render_markdown(register, args.framework, raw.get("as_of", "(no date)"))
    else:
        out = json.dumps({
            "as_of": raw.get("as_of", ""),
            "framework": args.framework,
            "total_entries": len(register),
            "register": register,
        }, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
