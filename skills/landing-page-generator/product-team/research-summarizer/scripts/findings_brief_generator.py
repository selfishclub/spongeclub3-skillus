#!/usr/bin/env python3
"""
findings_brief_generator.py — Generate a structured findings brief from
research synthesis inputs.

Reads a JSON describing the study, top insights, recommendations, and
methodology; produces a one-pager + extended memo + quote bank in markdown.

Stdlib only. JSON or markdown output.

Usage:
    python3 findings_brief_generator.py --input findings.json
    python3 findings_brief_generator.py --input findings.json --format markdown
    python3 findings_brief_generator.py --input findings.json --section one-pager

Input schema:
{
  "study_name": "Onboarding interviews Q2",
  "research_question": "Why are trial users not activating?",
  "headline_answer": "Users miss the import option because it's hidden in a sub-menu.",
  "methodology": {
      "n": 8, "dates": "Apr 12 – May 6, 2026",
      "segments": ["SMB trial users"],
      "format": "60-min semi-structured interviews",
      "interviewer": "Jane (UX research)"
  },
  "insights": [
      {
          "id": "INS-001",
          "statement": "Users abandon onboarding when import options are hidden.",
          "evidence": "6 of 8 users",
          "confidence": "high",
          "quote": "I looked everywhere for an Import button."
      }
  ],
  "recommendations": [
      {"action": "Surface import on first onboarding step", "owner": "Onboarding PM", "priority": "high"}
  ],
  "open_questions": ["Does this affect enterprise too?"],
  "quote_bank": [
      {"quote": "...", "source": "P-007", "segment": "SMB", "theme": "onboarding-friction"}
  ]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def render_one_pager(data: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# {data.get('study_name','(study)')}")
    lines.append("")
    lines.append("## Question")
    lines.append(data.get("research_question", ""))
    lines.append("")
    lines.append("## Answer")
    lines.append(f"**{data.get('headline_answer','')}**")
    lines.append("")
    lines.append("## Top insights")
    for i in data.get("insights", []):
        lines.append(f"- **{i.get('statement','')}** "
                    f"(evidence: {i.get('evidence','')}; confidence: {i.get('confidence','')})")
    lines.append("")
    lines.append("## What we recommend")
    for r in data.get("recommendations", []):
        lines.append(f"- {r.get('action','')} — owner: {r.get('owner','—')} | "
                    f"priority: {r.get('priority','—')}")
    lines.append("")
    lines.append("## What we don't know yet")
    for q in data.get("open_questions", []):
        lines.append(f"- {q}")
    lines.append("")
    m = data.get("methodology", {}) or {}
    lines.append(f"## Methodology")
    lines.append(
        f"N={m.get('n','?')}, conducted {m.get('dates','')}, "
        f"segments: {', '.join(m.get('segments', []))}, "
        f"format: {m.get('format','')}, interviewer: {m.get('interviewer','')}"
    )
    return "\n".join(lines)


def render_memo(data: dict[str, Any]) -> str:
    lines = []
    lines.append(render_one_pager(data))
    lines.append("\n---\n")
    lines.append("## Full findings detail")
    for i in data.get("insights", []):
        lines.append(f"### {i.get('id','')} — {i.get('statement','')}")
        lines.append(f"_evidence: {i.get('evidence','')} | confidence: {i.get('confidence','')}_")
        q = i.get("quote") or ""
        if q:
            lines.append(f"\n> {q}")
        lines.append("")
    return "\n".join(lines)


def render_quote_bank(data: dict[str, Any]) -> str:
    lines = []
    lines.append(f"# Quote bank — {data.get('study_name','(study)')}\n")
    lines.append("| Source | Segment | Theme | Quote |")
    lines.append("|--------|---------|-------|-------|")
    for q in data.get("quote_bank", []):
        lines.append(f"| {q.get('source','')} | {q.get('segment','')} | {q.get('theme','')} | "
                    f"{q.get('quote','')} |")
    return "\n".join(lines)


def render_full(data: dict[str, Any]) -> str:
    parts = [render_one_pager(data), "\n---\n",
             render_memo(data).split("---\n", 1)[1] if "---" in render_memo(data) else "",
             "\n---\n", render_quote_bank(data)]
    return "\n".join(parts)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate findings brief from research synthesis inputs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="JSON of findings")
    p.add_argument("--section",
                  choices=["one-pager", "memo", "quote-bank", "full"],
                  default="full")
    p.add_argument("--format", choices=["json", "markdown"], default="markdown")
    p.add_argument("--output", help="Write to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except OSError as e:
        print(f"error: cannot read input: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 2

    if args.section == "one-pager":
        out = render_one_pager(data)
    elif args.section == "memo":
        out = render_memo(data)
    elif args.section == "quote-bank":
        out = render_quote_bank(data)
    else:
        out = render_full(data)

    if args.format == "json":
        out = json.dumps({"section": args.section, "markdown": out}, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
