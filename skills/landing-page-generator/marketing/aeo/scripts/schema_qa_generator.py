#!/usr/bin/env python3
"""
schema_qa_generator.py — Generate JSON-LD FAQ / QAPage / HowTo schema from content.

Reads a markdown or HTML file; extracts Q&A pairs (or how-to steps); emits
JSON-LD schema ready to embed in <head>.

Detection patterns:
  - FAQ: Q&A patterns (Q: ... A: ...) or heading-followed-by-paragraph
  - QAPage: single Q&A
  - HowTo: numbered steps under # How to ... heading

Stdlib only. JSON-LD output or JSON wrapper.

Usage:
    python3 schema_qa_generator.py --content article.md
    python3 schema_qa_generator.py --content article.md --schema-type FAQPage
    python3 schema_qa_generator.py --content faq.md --schema-type FAQPage --output schema.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any


# Q&A heading patterns: H2/H3 questions followed by content
RE_HEADING_QA = re.compile(
    r"^#{2,3}\s+(.+\?)\s*$\n+([^\n#].+?)(?=\n#{1,3}\s+|\Z)",
    re.MULTILINE | re.DOTALL,
)
# Q: / A: pattern
RE_QA_PATTERN = re.compile(
    r"(?:^|\n)(?:\*\*)?Q(?:uestion)?:?\s*[:\-]?\s*(.+?)(?:\*\*)?\n+(?:\*\*)?A(?:nswer)?:?\s*[:\-]?\s*(.+?)(?=\n+(?:Q(?:uestion)?:|\n#|\Z))",
    re.IGNORECASE | re.DOTALL,
)
# How-to step heading
RE_HOWTO_STEP = re.compile(
    r"^#{2,4}\s+Step\s+\d+:?\s*(.+?)\s*$\n+(.+?)(?=\n#{1,4}\s+|\Z)",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)
# How-to overall heading
RE_HOWTO_HEADING = re.compile(r"^#\s+How\s+to\s+(.+?)\s*$", re.IGNORECASE | re.MULTILINE)


@dataclass
class QAPair:
    question: str
    answer: str


@dataclass
class HowToStep:
    name: str
    text: str


def clean_text(text: str) -> str:
    """Strip markdown formatting; trim whitespace."""
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)  # bold
    text = re.sub(r"\*([^*]+)\*", r"\1", text)  # italic
    text = re.sub(r"`([^`]+)`", r"\1", text)  # inline code
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)  # links
    text = re.sub(r"\s+", " ", text)  # collapse whitespace
    return text.strip()


def extract_qa_pairs(text: str) -> list[QAPair]:
    pairs: list[QAPair] = []
    # Pattern 1: H2/H3 questions
    for m in RE_HEADING_QA.finditer(text):
        question = clean_text(m.group(1))
        answer = clean_text(m.group(2)[:500])  # cap answer at 500 chars
        if question and answer and len(question) < 200:
            pairs.append(QAPair(question=question, answer=answer))
    # Pattern 2: Q: / A:
    for m in RE_QA_PATTERN.finditer(text):
        question = clean_text(m.group(1).rstrip("?") + "?")
        answer = clean_text(m.group(2)[:500])
        if question and answer and len(question) < 200:
            # Avoid duplicates
            if not any(p.question.lower() == question.lower() for p in pairs):
                pairs.append(QAPair(question=question, answer=answer))
    return pairs


def extract_howto_steps(text: str) -> tuple[str, list[HowToStep]]:
    """Returns (howto_title, steps)."""
    howto_match = RE_HOWTO_HEADING.search(text)
    if not howto_match:
        return "", []
    title = clean_text(howto_match.group(1))
    steps: list[HowToStep] = []
    for m in RE_HOWTO_STEP.finditer(text):
        name = clean_text(m.group(1))
        step_text = clean_text(m.group(2)[:400])
        steps.append(HowToStep(name=name, text=step_text))
    return title, steps


def build_faq_schema(pairs: list[QAPair]) -> dict[str, Any]:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": p.question,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": p.answer,
                },
            }
            for p in pairs
        ],
    }


def build_qapage_schema(pair: QAPair) -> dict[str, Any]:
    return {
        "@context": "https://schema.org",
        "@type": "QAPage",
        "mainEntity": {
            "@type": "Question",
            "name": pair.question,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": pair.answer,
            },
        },
    }


def build_howto_schema(title: str, steps: list[HowToStep]) -> dict[str, Any]:
    return {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": f"How to {title}",
        "step": [
            {
                "@type": "HowToStep",
                "name": s.name,
                "text": s.text,
            }
            for s in steps
        ],
    }


def auto_detect_schema_type(pairs: list[QAPair], howto_steps: list[HowToStep]) -> str:
    if len(howto_steps) >= 3:
        return "HowTo"
    if len(pairs) >= 3:
        return "FAQPage"
    if len(pairs) == 1:
        return "QAPage"
    if len(pairs) == 2:
        return "FAQPage"
    return "none"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate JSON-LD schema from content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--content", required=True, help="Markdown or HTML content file")
    p.add_argument("--schema-type", choices=["FAQPage", "QAPage", "HowTo", "auto"], default="auto")
    p.add_argument("--format", choices=["json-ld", "html", "wrapped-json"], default="json-ld",
                   help="json-ld: just the schema; html: wrapped in <script> tag; wrapped-json: with metadata")
    p.add_argument("--output", help="Output file path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        text = Path(args.content).read_text(encoding="utf-8", errors="ignore")
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    pairs = extract_qa_pairs(text)
    howto_title, howto_steps = extract_howto_steps(text)

    schema_type = args.schema_type
    if schema_type == "auto":
        schema_type = auto_detect_schema_type(pairs, howto_steps)
        if schema_type == "none":
            print("error: no Q&A pairs or how-to steps detected in content", file=sys.stderr)
            return 1

    if schema_type == "FAQPage":
        if not pairs:
            print("error: no Q&A pairs detected for FAQPage schema", file=sys.stderr)
            return 1
        schema = build_faq_schema(pairs)
    elif schema_type == "QAPage":
        if not pairs:
            print("error: no Q&A pair detected for QAPage schema", file=sys.stderr)
            return 1
        schema = build_qapage_schema(pairs[0])
    elif schema_type == "HowTo":
        if not howto_steps:
            print("error: no how-to steps detected", file=sys.stderr)
            return 1
        schema = build_howto_schema(howto_title, howto_steps)
    else:
        print(f"error: unknown schema type: {schema_type}", file=sys.stderr)
        return 2

    if args.format == "html":
        out = f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'
    elif args.format == "wrapped-json":
        out = json.dumps({
            "schema_type": schema_type,
            "extracted_qa_count": len(pairs),
            "extracted_howto_step_count": len(howto_steps),
            "schema": schema,
        }, indent=2)
    else:
        out = json.dumps(schema, indent=2)

    if args.output:
        Path(args.output).write_text(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
