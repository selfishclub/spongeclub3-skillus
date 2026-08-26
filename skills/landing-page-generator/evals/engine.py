#!/usr/bin/env python3
"""
engine.py — Deterministic check evaluator for PM skill output rubrics.

Stdlib only. See evals/README.md for the supported check types.

Public API:
    evaluate_artifact(rubric: dict, artifact_text: str) -> dict
    extract_section(text, heading, level=2) -> str | None
    check_passes(check: dict, text: str) -> tuple[bool, str]
"""

import re
from typing import Any


# ---------------------------------------------------------------------------
# Section extraction (markdown)
# ---------------------------------------------------------------------------

def _heading_regex(heading: str, level: int = 2) -> re.Pattern:
    """Match a markdown heading like '## <heading>' (allowing 'Section N:' prefix)."""
    hashes = "#" * max(1, min(level, 6))
    # allow optional "Section N:" or numeric prefix
    h = re.escape(heading).replace(r"\ ", r"\s+")
    return re.compile(
        rf"^{hashes}\s+(?:Section\s+\d+:\s+|\d+\.\s+)?{h}\s*$",
        re.MULTILINE | re.IGNORECASE,
    )


def extract_section(text: str, heading: str, level: int = 2) -> str | None:
    """Extract the body of a section starting with the given heading.

    Returns the text from after the heading line until the next heading of
    the same or higher level, or end of file. Returns None if not found.
    """
    pat = _heading_regex(heading, level)
    m = pat.search(text)
    if not m:
        return None
    start = m.end()
    # Find next heading at same or higher level
    boundary = re.compile(
        rf"^#{{1,{level}}}\s+",
        re.MULTILINE,
    )
    rest = text[start:]
    nxt = boundary.search(rest)
    return rest[:nxt.start()] if nxt else rest


def _sentences(text: str) -> list[str]:
    """Naive sentence splitter — splits on . ? ! followed by space + capital."""
    chunks = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'])", text.strip())
    return [c.strip() for c in chunks if c.strip()]


def _words(text: str) -> list[str]:
    return [w for w in re.split(r"\s+", text) if w]


# ---------------------------------------------------------------------------
# Check evaluators
# ---------------------------------------------------------------------------

def _flag_to_re(flags: str) -> int:
    f = 0
    if "i" in flags: f |= re.IGNORECASE
    if "m" in flags: f |= re.MULTILINE
    if "s" in flags: f |= re.DOTALL
    return f


def check_regex(params: dict, text: str) -> tuple[bool, str]:
    pat = params.get("pattern", "")
    flags = _flag_to_re(params.get("flags", "im"))
    if not pat:
        return False, "missing 'pattern'"
    found = bool(re.search(pat, text, flags))
    return (found, "matched" if found else "pattern not found")


def check_regex_not(params: dict, text: str) -> tuple[bool, str]:
    pat = params.get("pattern", "")
    flags = _flag_to_re(params.get("flags", "im"))
    if not pat:
        return False, "missing 'pattern'"
    found = bool(re.search(pat, text, flags))
    return (not found, "absent (good)" if not found else "forbidden pattern found")


def check_section_present(params: dict, text: str) -> tuple[bool, str]:
    h = params.get("heading", "")
    lvl = int(params.get("level", 2))
    if not h: return False, "missing 'heading'"
    found = extract_section(text, h, lvl) is not None
    return (found, "found" if found else f"section '{h}' not found")


def check_section_word_count(params: dict, text: str) -> tuple[bool, str]:
    h = params.get("heading", "")
    lvl = int(params.get("level", 2))
    mn = int(params.get("min", 0))
    mx = int(params.get("max", 10**6))
    body = extract_section(text, h, lvl)
    if body is None:
        return False, f"section '{h}' not found"
    n = len(_words(body))
    ok = mn <= n <= mx
    return (ok, f"{n} words (need {mn}-{mx})")


def check_section_sentence_count(params: dict, text: str) -> tuple[bool, str]:
    h = params.get("heading", "")
    lvl = int(params.get("level", 2))
    mn = int(params.get("min", 0))
    mx = int(params.get("max", 10**6))
    body = extract_section(text, h, lvl)
    if body is None:
        return False, f"section '{h}' not found"
    # Strip tables and code blocks from sentence count
    body_clean = re.sub(r"```.*?```", " ", body, flags=re.DOTALL)
    body_clean = re.sub(r"^\|.*\|\s*$", " ", body_clean, flags=re.MULTILINE)
    n = len(_sentences(body_clean))
    ok = mn <= n <= mx
    return (ok, f"{n} sentences (need {mn}-{mx})")


def check_keyword_any(params: dict, text: str) -> tuple[bool, str]:
    kws = params.get("keywords", [])
    if not kws: return False, "no keywords"
    low = text.lower()
    matched = [k for k in kws if k.lower() in low]
    return (len(matched) > 0, f"matched: {matched[:3]}" if matched else "none of " + ", ".join(kws[:5]))


def check_keyword_all(params: dict, text: str) -> tuple[bool, str]:
    kws = params.get("keywords", [])
    if not kws: return False, "no keywords"
    low = text.lower()
    missing = [k for k in kws if k.lower() not in low]
    return (len(missing) == 0, "all present" if not missing else f"missing: {missing}")


def check_keyword_none(params: dict, text: str) -> tuple[bool, str]:
    kws = params.get("keywords", [])
    if not kws: return False, "no keywords"
    low = text.lower()
    found = [k for k in kws if k.lower() in low]
    return (len(found) == 0, "clean" if not found else f"found forbidden: {found}")


def check_has_table(params: dict, text: str) -> tuple[bool, str]:
    rows = re.findall(r"^\|.+\|\s*$", text, re.MULTILINE)
    # subtract separator rows
    real_rows = [r for r in rows if not re.match(r"^\|\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|\s*$", r)]
    min_rows = int(params.get("min_rows", 2))
    n = len(real_rows)
    ok = n >= min_rows
    return (ok, f"{n} rows (need >= {min_rows})")


def check_has_list(params: dict, text: str) -> tuple[bool, str]:
    items = re.findall(r"^\s*(?:[-*+]\s+|\d+\.\s+)", text, re.MULTILINE)
    min_items = int(params.get("min_items", 3))
    n = len(items)
    ok = n >= min_items
    return (ok, f"{n} list items (need >= {min_items})")


def check_url_count(params: dict, text: str) -> tuple[bool, str]:
    urls = re.findall(r"https?://\S+", text)
    mn = int(params.get("min", 0))
    mx = int(params.get("max", 10**6))
    n = len(urls)
    ok = mn <= n <= mx
    return (ok, f"{n} URLs (need {mn}-{mx})")


def check_length_in_range(params: dict, text: str) -> tuple[bool, str]:
    n = len(text)
    mn = int(params.get("min", 0))
    mx = int(params.get("max", 10**6))
    ok = mn <= n <= mx
    return (ok, f"{n} chars (need {mn}-{mx})")


def check_line_count_range(params: dict, text: str) -> tuple[bool, str]:
    n = text.count("\n") + 1
    mn = int(params.get("min", 0))
    mx = int(params.get("max", 10**6))
    ok = mn <= n <= mx
    return (ok, f"{n} lines (need {mn}-{mx})")


CHECKS = {
    "regex": check_regex,
    "regex_not": check_regex_not,
    "section_present": check_section_present,
    "section_word_count": check_section_word_count,
    "section_sentence_count": check_section_sentence_count,
    "keyword_any": check_keyword_any,
    "keyword_all": check_keyword_all,
    "keyword_none": check_keyword_none,
    "has_table": check_has_table,
    "has_list": check_has_list,
    "url_count": check_url_count,
    "length_in_range": check_length_in_range,
    "line_count_range": check_line_count_range,
}


# ---------------------------------------------------------------------------
# Rubric evaluation
# ---------------------------------------------------------------------------

def check_passes(check: dict, text: str) -> tuple[bool, str]:
    ctype = check.get("type", "")
    fn = CHECKS.get(ctype)
    if not fn:
        return False, f"unknown check type: {ctype}"
    try:
        return fn(check, text)
    except Exception as exc:
        return False, f"check error: {exc}"


def evaluate_artifact(rubric: dict, artifact_text: str) -> dict:
    """Run a rubric against an artifact. Returns a structured result.

    Result shape:
        {
            "skill": str,
            "max_score": int,
            "raw_score": int,
            "score": int,         # 0-100, weight-normalized
            "passed": int,
            "failed": int,
            "results": [
                {"id", "name", "weight", "passed", "detail"}
            ]
        }
    """
    criteria = rubric.get("criteria", []) or []
    raw_max = sum(int(c.get("weight", 1)) for c in criteria) or 1
    rows: list[dict] = []
    raw_score = 0
    for c in criteria:
        w = int(c.get("weight", 1))
        passed, detail = check_passes(c.get("check", {}), artifact_text)
        if passed:
            raw_score += w
        rows.append({
            "id": c.get("id", ""),
            "name": c.get("name", c.get("id", "")),
            "weight": w,
            "passed": passed,
            "detail": detail,
        })
    score = round(100 * raw_score / raw_max) if raw_max > 0 else 0
    return {
        "skill": rubric.get("skill", ""),
        "rubric_version": rubric.get("version", ""),
        "max_score": raw_max,
        "raw_score": raw_score,
        "score": score,
        "passed": sum(1 for r in rows if r["passed"]),
        "failed": sum(1 for r in rows if not r["passed"]),
        "results": rows,
    }
