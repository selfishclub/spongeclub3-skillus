#!/usr/bin/env python3
"""
aeo_content_auditor.py — Score content for Answer Engine Optimization (AEO) patterns.

Scans markdown/HTML content; emits per-pattern score (definition, table, steps,
stats, list, structure markers) + overall AEO score + remediation recommendations.

Stdlib only. Markdown or JSON.

Usage:
    python3 aeo_content_auditor.py --path ./content
    python3 aeo_content_auditor.py --path article.md --format json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any


# Detection patterns for AEO content properties
RE_HEADING = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
RE_MARKDOWN_TABLE = re.compile(r"^\|.+\|\s*$\n^\|[\s\-:|]+\|\s*$", re.MULTILINE)
RE_HTML_TABLE = re.compile(r"<table\b", re.IGNORECASE)
RE_NUMBERED_LIST = re.compile(r"^\s*\d+\.\s+\S", re.MULTILINE)
RE_BULLET_LIST = re.compile(r"^\s*[-*+]\s+\S", re.MULTILINE)
RE_DEFINITION_TERM = re.compile(r"^([A-Z][\w\s-]{2,40})\s+is\s+", re.MULTILINE)
RE_STATISTIC = re.compile(r"\b\d+(?:\.\d+)?%\s|\b\$\d+\b|\b\d+(?:,\d{3})+\b")
RE_SOURCE_ATTRIBUTION = re.compile(r"\b(?:according to|source:|cited from|per the|\[.*?\]\(.+?\))", re.IGNORECASE)
RE_BOLD = re.compile(r"\*\*[^*]+\*\*|__[^_]+__")
RE_FAQ_HEADING = re.compile(r"^#{1,3}\s+(?:FAQ|Frequently Asked Questions|Q&A|Questions)\s*$", re.IGNORECASE | re.MULTILINE)
RE_QA_PATTERN = re.compile(r"^(?:Q:|Question:)\s+.+\n+(?:A:|Answer:)\s+", re.IGNORECASE | re.MULTILINE)
RE_QA_SCHEMA = re.compile(r'"@type"\s*:\s*"(?:FAQPage|QAPage|Question|HowTo)"')
RE_HOWTO_STEP = re.compile(r"^#{1,4}\s+Step\s+\d+", re.IGNORECASE | re.MULTILINE)
RE_LAST_UPDATED = re.compile(r"\b(?:last updated|updated on|published on|published)\s*[:]\s*\d{4}-\d{2}-\d{2}", re.IGNORECASE)
RE_PDF_LINK = re.compile(r"\.pdf\b", re.IGNORECASE)
RE_IMAGE = re.compile(r"!\[([^\]]*)\]\([^\)]+\)|<img\s[^>]*>", re.IGNORECASE)


@dataclass
class PatternScore:
    pattern: str
    score: int
    max_score: int
    finding: str


@dataclass
class FileScore:
    path: str
    word_count: int
    heading_count: int
    pattern_scores: list[PatternScore]
    overall_score: int
    recommendations: list[str]


def count_words(text: str) -> int:
    # Strip code blocks + HTML tags then count
    stripped = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    stripped = re.sub(r"<[^>]+>", "", stripped)
    return len(stripped.split())


def detect_definitional_content(text: str, headings: list[str]) -> PatternScore:
    """Score: heading with 'What is' or definitional sentence near top."""
    score = 0
    finding = ""
    has_what_is = any(re.search(r"what is\s+\S", h.lower()) for h in headings[:3])
    has_def_sentence = bool(RE_DEFINITION_TERM.search(text[:500]))
    if has_what_is:
        score += 50
        finding += "✓ 'What is' heading near top. "
    if has_def_sentence:
        score += 50
        finding += "✓ Definitional sentence near top. "
    if not finding:
        finding = "✗ No definitional structure detected."
    return PatternScore("Definitional content", score, 100, finding.strip())


def detect_tables(text: str) -> PatternScore:
    md_tables = len(RE_MARKDOWN_TABLE.findall(text))
    html_tables = len(RE_HTML_TABLE.findall(text))
    total = md_tables + html_tables
    if total == 0:
        return PatternScore("Comparative tables", 0, 100, "✗ No tables found")
    score = min(100, total * 30)
    return PatternScore("Comparative tables", score, 100,
                        f"✓ {total} table(s) found ({md_tables} markdown, {html_tables} HTML)")


def detect_step_by_step(text: str) -> PatternScore:
    numbered = len(RE_NUMBERED_LIST.findall(text))
    step_headings = len(RE_HOWTO_STEP.findall(text))
    score = min(100, numbered * 8 + step_headings * 20)
    if score == 0:
        return PatternScore("Step-by-step procedural", 0, 100, "✗ No numbered steps or step headings")
    return PatternScore("Step-by-step procedural", score, 100,
                        f"✓ {numbered} numbered list items + {step_headings} step headings")


def detect_statistics(text: str) -> PatternScore:
    stats = len(RE_STATISTIC.findall(text))
    sources = len(RE_SOURCE_ATTRIBUTION.findall(text))
    score = min(100, stats * 5 + sources * 10)
    if stats == 0:
        return PatternScore("Statistics + attribution", 0, 100, "✗ No statistical claims detected")
    if stats > 0 and sources == 0:
        return PatternScore("Statistics + attribution", min(40, score), 100,
                            f"⚠️ {stats} statistics but no source attributions")
    return PatternScore("Statistics + attribution", score, 100,
                        f"✓ {stats} statistics + {sources} source attributions")


def detect_lists(text: str) -> PatternScore:
    bullets = len(RE_BULLET_LIST.findall(text))
    numbered = len(RE_NUMBERED_LIST.findall(text))
    total = bullets + numbered
    if total < 3:
        return PatternScore("Lists with structure", 0, 100, "✗ Too few list items")
    score = min(100, total * 4)
    return PatternScore("Lists with structure", score, 100,
                        f"✓ {bullets} bullet + {numbered} numbered items")


def detect_structure_markers(text: str, headings: list[str]) -> PatternScore:
    """Headings, bold, FAQ patterns, schema."""
    score = 0
    findings = []
    if len(headings) >= 3:
        score += 25
        findings.append(f"{len(headings)} headings")
    if RE_BOLD.search(text):
        score += 20
        findings.append("bold text used")
    if RE_FAQ_HEADING.search(text) or RE_QA_PATTERN.search(text):
        score += 25
        findings.append("FAQ section present")
    if RE_QA_SCHEMA.search(text):
        score += 30
        findings.append("✓ FAQ/QAPage/HowTo schema found")
    if score == 0:
        return PatternScore("Structure markers", 0, 100, "✗ Weak structural markers")
    return PatternScore("Structure markers", score, 100, "✓ " + ", ".join(findings))


def detect_freshness(text: str) -> PatternScore:
    if RE_LAST_UPDATED.search(text):
        return PatternScore("Freshness indicator", 100, 100, "✓ Last-updated date visible")
    return PatternScore("Freshness indicator", 0, 100, "✗ No last-updated date visible")


def detect_extractability_issues(text: str) -> list[str]:
    issues = []
    if RE_PDF_LINK.search(text):
        issues.append("PDF links present; ensure HTML equivalent exists for LLM extraction")
    img_matches = RE_IMAGE.findall(text)
    if img_matches:
        no_alt = sum(1 for m in img_matches if not m or m == "")
        if no_alt > 0:
            issues.append(f"{no_alt} images may lack alt text (LLM can't extract content)")
    return issues


def score_file(path: Path, text: str) -> FileScore:
    word_count = count_words(text)
    heading_matches = RE_HEADING.findall(text)
    headings = [m[1] for m in heading_matches]

    patterns = [
        detect_definitional_content(text, headings),
        detect_tables(text),
        detect_step_by_step(text),
        detect_statistics(text),
        detect_lists(text),
        detect_structure_markers(text, headings),
        detect_freshness(text),
    ]

    overall = sum(p.score for p in patterns) // len(patterns)

    recommendations = []
    if word_count < 300:
        recommendations.append("Content very short (<300 words); LLMs prefer 1500-2500 words")
    elif word_count > 5000:
        recommendations.append("Content very long (>5000 words); LLMs may miss key sections; consider splitting")
    for p in patterns:
        if p.score < 50:
            recommendations.append(f"Improve {p.pattern}: {p.finding}")
    issues = detect_extractability_issues(text)
    recommendations.extend(issues)

    return FileScore(
        path=str(path),
        word_count=word_count,
        heading_count=len(headings),
        pattern_scores=patterns,
        overall_score=overall,
        recommendations=recommendations,
    )


def scan_path(root: Path) -> list[FileScore]:
    results: list[FileScore] = []
    if root.is_file():
        if root.suffix in (".md", ".html", ".htm"):
            text = root.read_text(encoding="utf-8", errors="ignore")
            results.append(score_file(root, text))
        return results
    for ext in (".md", ".html", ".htm"):
        for p in root.rglob(f"*{ext}"):
            if any(part.startswith(".") for part in p.parts):
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            results.append(score_file(p, text))
    return results


def render_markdown(results: list[FileScore]) -> str:
    out = ["# AEO Content Audit", ""]
    out.append(f"_Files analyzed: {len(results)}_")
    out.append("")
    if results:
        avg = sum(r.overall_score for r in results) // len(results)
        out.append(f"**Average AEO score**: {avg}/100")
        out.append("")
    out.append("## Summary by File")
    out.append("")
    out.append("| File | Words | Overall | Definition | Tables | Steps | Stats | Lists | Structure | Fresh |")
    out.append("|------|-------|---------|------------|--------|-------|-------|-------|-----------|-------|")
    for r in sorted(results, key=lambda x: x.overall_score):
        scores = {p.pattern: p.score for p in r.pattern_scores}
        out.append(
            f"| {r.path} | {r.word_count} | **{r.overall_score}** | "
            f"{scores.get('Definitional content', 0)} | {scores.get('Comparative tables', 0)} | "
            f"{scores.get('Step-by-step procedural', 0)} | {scores.get('Statistics + attribution', 0)} | "
            f"{scores.get('Lists with structure', 0)} | {scores.get('Structure markers', 0)} | "
            f"{scores.get('Freshness indicator', 0)} |"
        )
    out.append("")
    out.append("## Per-File Recommendations")
    out.append("")
    for r in sorted(results, key=lambda x: x.overall_score):
        if r.recommendations:
            out.append(f"### {r.path} (score {r.overall_score}/100)")
            for rec in r.recommendations:
                out.append(f"- {rec}")
            out.append("")
    return "\n".join(out)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Audit content for AEO (Answer Engine Optimization) patterns",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--path", required=True, help="File or directory to audit")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--output", help="Output file path")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.path).resolve()
    if not root.exists():
        print(f"error: path not found: {root}", file=sys.stderr)
        return 2
    results = scan_path(root)
    if args.format == "json":
        out = json.dumps([asdict(r) for r in results], indent=2, default=str)
    else:
        out = render_markdown(results)
    if args.output:
        Path(args.output).write_text(out)
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
