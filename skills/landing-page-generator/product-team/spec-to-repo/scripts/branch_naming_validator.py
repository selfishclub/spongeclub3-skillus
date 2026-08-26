#!/usr/bin/env python3
"""
branch_naming_validator.py — Lint branch names against a convention.

Reads a text file of branch names (one per line) or JSON list; validates
against a configurable pattern; flags issues.

Stdlib only. JSON or markdown output.

Usage:
    python3 branch_naming_validator.py --input branches.txt
    python3 branch_naming_validator.py --input branches.json --format markdown
    python3 branch_naming_validator.py --input branches.txt \\
        --pattern "^(feature|fix|chore|hotfix|refactor|docs|test)/[A-Z]+-[0-9]+-[a-z0-9-]+$"

Input formats:
- .txt: one branch name per line, # comments allowed
- .json: ["branch-1","branch-2"] OR {"branches": [...]}
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_PATTERN = r"^(feature|fix|chore|hotfix|refactor|docs|test)/[A-Z]+-[0-9]+-[a-z0-9-]+$"
RESERVED = {"main", "master", "dev", "develop", "staging", "production", "release", "HEAD"}


def load_branches(path: Path) -> list[str]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [str(x) for x in data]
        if isinstance(data, dict):
            return [str(x) for x in (data.get("branches") or [])]
        return []
    branches: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Strip "* " from `git branch` output
        if line.startswith("* "):
            line = line[2:].strip()
        branches.append(line)
    return branches


def validate(branches: list[str], pattern: str) -> list[dict[str, Any]]:
    rx = re.compile(pattern)
    results: list[dict[str, Any]] = []
    for b in branches:
        issues: list[str] = []
        if b in RESERVED:
            results.append({"branch": b, "status": "reserved", "issues": ["reserved branch (main/dev/etc)"]})
            continue
        if " " in b:
            issues.append("contains whitespace")
        if any(c in b for c in ("..", "~", "^", ":", "?", "*", "[", "\\")):
            issues.append("contains invalid characters")
        if len(b) > 70:
            issues.append(f"too long ({len(b)} chars; target ≤70)")
        if b != b.lower():
            issues.append("contains uppercase characters (convention prefers lowercase)")
        if not rx.match(b):
            issues.append(f"does not match pattern: {pattern}")
        if "_" in b:
            issues.append("contains underscore (convention prefers hyphens)")

        if issues:
            results.append({"branch": b, "status": "fail", "issues": issues})
        else:
            results.append({"branch": b, "status": "pass", "issues": []})
    return results


def render_markdown(results: list[dict[str, Any]], pattern: str) -> str:
    lines = []
    lines.append("# Branch Naming Validation\n")
    lines.append(f"Pattern: `{pattern}`\n")
    pass_count = sum(1 for r in results if r["status"] == "pass")
    fail_count = sum(1 for r in results if r["status"] == "fail")
    reserved_count = sum(1 for r in results if r["status"] == "reserved")
    lines.append(f"Total: {len(results)} | pass: {pass_count} | fail: {fail_count} | reserved: {reserved_count}\n")
    lines.append("## Results")
    lines.append("| Status | Branch | Issues |")
    lines.append("|--------|--------|--------|")
    for r in results:
        issues = "; ".join(r["issues"]) if r["issues"] else "—"
        lines.append(f"| {r['status']} | {r['branch']} | {issues} |")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Validate git branch names against a convention",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--input", required=True, help="Branches file (txt or json)")
    p.add_argument("--pattern", default=DEFAULT_PATTERN,
                  help="Regex pattern branches must match")
    p.add_argument("--format", choices=["json", "markdown"], default="json")
    p.add_argument("--output", help="Write to file instead of stdout")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        branches = load_branches(Path(args.input))
    except OSError as e:
        print(f"error: cannot read input: {e}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 2

    results = validate(branches, args.pattern)

    if args.format == "markdown":
        out = render_markdown(results, args.pattern)
    else:
        out = json.dumps({"pattern": args.pattern, "results": results}, indent=2)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
