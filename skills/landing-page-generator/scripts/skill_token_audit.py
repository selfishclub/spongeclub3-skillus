#!/usr/bin/env python3
"""Audit every skill for token economics and progressive disclosure.

This is a *complement* to skill_quality_scorer.py.  That tool grades skills
against the authoring standard (frontmatter, structure, prose quality).  This
tool answers a different question: **how many tokens does each skill cost the
model, and is it structured for cheap, on-demand loading?**

It measures the three tiers of the Anthropic Agent Skills loading model:

  Tier 1  description        -> ALWAYS in context (discovery cost)
  Tier 2  SKILL.md body      -> loaded when the skill triggers
  Tier 3  references/*.md     -> should load only when the task needs them

A well-built skill keeps Tier 1 tiny, Tier 2 lean (a map + quick start), and
pushes deep knowledge into Tier 3.  A skill that inlines everything into a
700-line SKILL.md pays the full Tier-2 cost on every invocation.

Token counts are *estimates* (chars / 4) -- no external tokenizer dependency,
consistent with this repo's stdlib-only rule.  Use them for ranking and
relative comparison, not for billing.

Usage:
    python scripts/skill_token_audit.py                 # ranked worklist (table)
    python scripts/skill_token_audit.py --top 20        # 20 worst offenders
    python scripts/skill_token_audit.py --domain engineering
    python scripts/skill_token_audit.py --format json   # machine-readable
    python scripts/skill_token_audit.py --format summary # aggregate totals only
    python scripts/skill_token_audit.py --no-color
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Folders that contain SKILL.md files but are not skill content we want to flag.
SKIP_PARTS = {".git", "node_modules", "__pycache__", "templates", ".cache"}

# Heuristic: ~4 characters per token for English prose + light markdown.
CHARS_PER_TOKEN = 4

# Tier-2 thresholds (body tokens). Tuned to the Agent Skills guidance that a
# SKILL.md should be a lean map, not a manual.
BODY_LEAN = 800        # <= this is healthy
BODY_HEAVY = 2000      # >= this is a strong refactor candidate

# Tier-1 thresholds (description tokens). Descriptions are always resident.
DESC_LEAN = 60
DESC_HEAVY = 120

_USE_COLOR = True


def _c(code: str, text: str) -> str:
    return text if not _USE_COLOR else f"\033[{code}m{text}\033[0m"


def red(t: str) -> str:
    return _c("31", t)


def yellow(t: str) -> str:
    return _c("33", t)


def green(t: str) -> str:
    return _c("32", t)


def dim(t: str) -> str:
    return _c("2", t)


def bold(t: str) -> str:
    return _c("1", t)


def est_tokens(text: str) -> int:
    return round(len(text) / CHARS_PER_TOKEN)


def split_frontmatter(raw: str) -> tuple[str, str]:
    """Return (frontmatter, body). Frontmatter is the text between the first
    pair of `---` fences; body is everything after."""
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) == 3:
            return parts[1], parts[2]
    return "", raw


def extract_description(frontmatter: str) -> str:
    """Pull the description value, handling single-line, quoted, and folded
    (`>` / `|`) multi-line YAML scalars -- no yaml dependency."""
    lines = frontmatter.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^description:\s*(.*)$", line)
        if not m:
            continue
        first = m.group(1).strip()
        if first and first not in (">", "|", ">-", "|-", ">+", "|+"):
            return first.strip("'\"")
        # Folded/literal block: gather subsequent indented lines.
        collected = []
        for nxt in lines[i + 1:]:
            if nxt.strip() == "":
                continue
            if re.match(r"^\S", nxt):  # next top-level key -> stop
                break
            collected.append(nxt.strip())
        return " ".join(collected)
    return ""


def find_skill_files() -> list[Path]:
    out = []
    for path in REPO_ROOT.rglob("SKILL.md"):
        if SKIP_PARTS.intersection(path.parts):
            continue
        out.append(path)
    return sorted(out)


def audit_skill(skill_md: Path) -> dict:
    raw = skill_md.read_text(encoding="utf-8", errors="replace")
    frontmatter, body = split_frontmatter(raw)
    description = extract_description(frontmatter)

    body_tokens = est_tokens(body)
    desc_tokens = est_tokens(description)

    skill_dir = skill_md.parent
    ref_dir = skill_dir / "references"
    ref_files = sorted(ref_dir.glob("*.md")) if ref_dir.is_dir() else []
    ref_tokens = sum(est_tokens(f.read_text(encoding="utf-8", errors="replace"))
                     for f in ref_files)

    # Does the body actually point the model at references/ (Tier 3 hand-off)?
    links_references = "references/" in body
    has_references = len(ref_files) > 0
    progressive = has_references and links_references

    # Inline ratio: how much knowledge sits in the always-on-trigger body vs.
    # the load-on-demand references. High body share = poor disclosure.
    total_knowledge = body_tokens + ref_tokens
    body_share = body_tokens / total_knowledge if total_knowledge else 1.0

    flags = []
    if body_tokens >= BODY_HEAVY:
        flags.append("heavy-body")
    elif body_tokens > BODY_LEAN:
        flags.append("large-body")
    if desc_tokens >= DESC_HEAVY:
        flags.append("bloated-desc")
    elif desc_tokens > DESC_LEAN:
        flags.append("long-desc")
    if not description:
        flags.append("no-desc")
    if body_tokens > BODY_LEAN and not has_references:
        flags.append("no-references")
    if has_references and not links_references:
        flags.append("orphan-references")
    if body_tokens > BODY_LEAN and body_share > 0.7 and has_references:
        flags.append("inline-heavy")

    # Refactor priority: dominated by Tier-2 over-spend, with a bump for
    # missing progressive disclosure since that is the structural fix.
    priority = max(0, body_tokens - BODY_LEAN)
    if not progressive and body_tokens > BODY_LEAN:
        priority = int(priority * 1.5)
    priority += max(0, desc_tokens - DESC_LEAN) * 5  # Tier-1 cost recurs forever

    try:
        rel = skill_md.relative_to(REPO_ROOT)
    except ValueError:
        rel = skill_md
    domain = rel.parts[0] if len(rel.parts) > 1 else "(root)"

    return {
        "skill": str(skill_md.parent.relative_to(REPO_ROOT)),
        "domain": domain,
        "desc_tokens": desc_tokens,
        "body_tokens": body_tokens,
        "ref_files": len(ref_files),
        "ref_tokens": ref_tokens,
        "body_share": round(body_share, 2),
        "progressive": progressive,
        "flags": flags,
        "priority": priority,
    }


def render_table(rows: list[dict], limit: int | None) -> None:
    shown = rows[:limit] if limit else rows
    print(bold(f"\n  Skill token audit -- {len(rows)} skills "
               f"(showing {len(shown)} by refactor priority)\n"))
    header = f"  {'PRIO':>6}  {'BODY':>6}  {'DESC':>5}  {'REFS':>4}  {'BODY%':>5}  PD  SKILL"
    print(dim(header))
    print(dim("  " + "-" * (len(header) - 2)))
    for r in shown:
        prio = r["priority"]
        if prio >= 2000:
            pc = red
        elif prio >= 600:
            pc = yellow
        else:
            pc = green
        pd = green(" Y") if r["progressive"] else red(" N")
        body_pct = f"{int(r['body_share'] * 100)}%"
        flagstr = dim(" ".join(r["flags"])) if r["flags"] else ""
        print(f"  {pc(f'{prio:>6}')}  {r['body_tokens']:>6}  {r['desc_tokens']:>5}  "
              f"{r['ref_files']:>4}  {body_pct:>5}  {pd}  {r['skill']}  {flagstr}")
    print()


def render_summary(rows: list[dict]) -> None:
    n = len(rows)
    total_desc = sum(r["desc_tokens"] for r in rows)
    total_body = sum(r["body_tokens"] for r in rows)
    total_ref = sum(r["ref_tokens"] for r in rows)
    no_pd = [r for r in rows if not r["progressive"]]
    heavy = [r for r in rows if "heavy-body" in r["flags"]]
    bloated = [r for r in rows if "bloated-desc" in r["flags"] or "long-desc" in r["flags"]]
    inline = [r for r in rows if "inline-heavy" in r["flags"] or "no-references" in r["flags"]]

    print(bold("\n  === Skill Token Audit: Summary ===\n"))
    print(f"  Skills audited                 {n}")
    print(f"  Tier-1 discovery cost (all desc)  {bold(f'{total_desc:>8,}')} tokens  "
          + dim("(always resident)"))
    print(f"  Tier-2 body cost (sum)            {total_body:>8,} tokens  "
          + dim("(loaded per trigger)"))
    print(f"  Tier-3 reference cost (sum)       {total_ref:>8,} tokens  "
          + dim("(load on demand)"))
    print()
    print(f"  Avg body per skill             {round(total_body / n):>6,} tokens")
    print(f"  Avg description per skill      {round(total_desc / n):>6,} tokens")
    print()
    print(f"  {red(str(len(no_pd)))} skills WITHOUT progressive disclosure")
    print(f"  {red(str(len(heavy)))} skills with heavy bodies (>= {BODY_HEAVY} tokens)")
    print(f"  {yellow(str(len(inline)))} skills inlining knowledge that belongs in references/")
    print(f"  {yellow(str(len(bloated)))} skills with oversized descriptions (> {DESC_LEAN} tokens)")
    print()
    top = sorted(rows, key=lambda r: r["priority"], reverse=True)[:10]
    print(bold("  Top 10 refactor targets:"))
    for r in top:
        print(f"    {r['priority']:>6}  {r['skill']}")
    print()


def main() -> int:
    global _USE_COLOR
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--domain", help="Limit to one top-level domain folder")
    ap.add_argument("--top", type=int, help="Show only the N worst offenders")
    ap.add_argument("--format", choices=["table", "json", "summary"],
                    default="table")
    ap.add_argument("--no-color", action="store_true")
    args = ap.parse_args()

    if args.no_color or args.format == "json" or not sys.stdout.isatty():
        _USE_COLOR = False

    files = find_skill_files()
    if args.domain:
        files = [f for f in files
                 if f.relative_to(REPO_ROOT).parts[0] == args.domain]
        if not files:
            print(f"No skills found in domain '{args.domain}'", file=sys.stderr)
            return 1

    rows = [audit_skill(f) for f in files]
    rows.sort(key=lambda r: r["priority"], reverse=True)

    if args.format == "json":
        print(json.dumps(rows, indent=2))
    elif args.format == "summary":
        render_summary(rows)
    else:
        render_table(rows, args.top)
        render_summary(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
