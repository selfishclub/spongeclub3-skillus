#!/usr/bin/env python3
"""Static validator for a skill package. Runs without a model.

Verifies:
  - SKILL.md exists and has well-formed frontmatter (name, description, version)
  - Every script referenced in the "Tools Overview" table actually exists
  - test_cases.json (this file's sibling) is valid JSON with the required schema
  - References mentioned in the SKILL.md exist on disk

Exit code 0 = pass. Non-zero = fail, with a JSON diagnostic on stdout.

Usage:
    python evals/runner.py --skill <path-to-skill-dir>
    python evals/runner.py --skill ../  # if called from inside the skill's evals/
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


REQUIRED_FRONTMATTER_KEYS = ("name", "description")
REQUIRED_METADATA_KEYS = ("version",)
REQUIRED_SECTIONS = ("Overview", "Use when")


@dataclass
class Diagnostic:
    skill_path: str
    passed: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, bool] = field(default_factory=dict)

    def fail(self, msg: str) -> None:
        self.passed = False
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def check(self, name: str, ok: bool, err: str | None = None) -> None:
        self.checks[name] = ok
        if not ok and err:
            self.fail(err)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Very small YAML frontmatter parser. Handles flat keys and one-level metadata."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_raw = text[3:end].strip("\n")
    body = text[end + 4 :]

    fm: dict = {}
    current_key: str | None = None
    multiline_buf: list[str] = []
    nested_key: str | None = None

    for line in fm_raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indented = line.startswith(" ") or line.startswith("\t")
        stripped = line.strip()

        # close any open multiline scalar
        if not indented and multiline_buf and current_key:
            fm[current_key] = " ".join(multiline_buf).strip()
            multiline_buf = []

        if not indented:
            nested_key = None
            if ":" in stripped:
                key, _, val = stripped.partition(":")
                key = key.strip()
                val = val.strip()
                if val == ">" or val == "|":
                    current_key = key
                    multiline_buf = []
                elif val == "":
                    nested_key = key
                    fm[key] = {}
                    current_key = None
                else:
                    fm[key] = val
                    current_key = None
            continue

        # indented line
        if nested_key:
            if ":" in stripped:
                k, _, v = stripped.partition(":")
                fm[nested_key][k.strip()] = v.strip()
        elif current_key:
            multiline_buf.append(stripped)

    if multiline_buf and current_key:
        fm[current_key] = " ".join(multiline_buf).strip()

    return fm, body


def referenced_scripts(body: str) -> list[str]:
    """Extract script filenames referenced from the Tools Overview table or Quick Start."""
    candidates: set[str] = set()
    for m in re.finditer(r"scripts/([a-zA-Z0-9_\-/]+\.py)", body):
        candidates.add(m.group(1))
    for m in re.finditer(r"`([a-zA-Z0-9_\-]+\.py)`", body):
        candidates.add(m.group(1))
    return sorted(candidates)


def referenced_docs(body: str) -> list[str]:
    """Extract reference docs linked in the SKILL.md."""
    refs: set[str] = set()
    for m in re.finditer(r"\(references/([a-zA-Z0-9_\-/]+\.md)\)", body):
        refs.add(m.group(1))
    return sorted(refs)


def validate_skill(skill_dir: Path) -> Diagnostic:
    diag = Diagnostic(skill_path=str(skill_dir))

    skill_md = skill_dir / "SKILL.md"
    diag.check("skill_md_present", skill_md.exists(), f"SKILL.md not found at {skill_md}")
    if not skill_md.exists():
        return diag

    text = skill_md.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    for key in REQUIRED_FRONTMATTER_KEYS:
        diag.check(f"frontmatter.{key}", key in fm, f"frontmatter missing '{key}'")

    metadata = fm.get("metadata", {})
    for key in REQUIRED_METADATA_KEYS:
        diag.check(
            f"metadata.{key}",
            isinstance(metadata, dict) and key in metadata,
            f"metadata missing '{key}'",
        )

    for section in REQUIRED_SECTIONS:
        present = f"## {section}" in body or f"# {section}" in body
        diag.check(f"section.{section.lower().replace(' ', '_')}", present)
        if not present:
            diag.warn(f"recommended section '{section}' not found")

    scripts_dir = skill_dir / "scripts"
    for script in referenced_scripts(body):
        rel = script if script.startswith("scripts/") else f"scripts/{script}"
        path = skill_dir / rel if rel.startswith("scripts/") else scripts_dir / script
        ok = path.exists() or (scripts_dir / Path(script).name).exists()
        diag.check(f"script.{Path(script).name}", ok, f"referenced script missing: {script}")

    for doc in referenced_docs(body):
        path = skill_dir / "references" / doc
        ok = path.exists()
        diag.check(f"reference.{doc}", ok)
        if not ok:
            diag.warn(f"referenced doc missing: references/{doc}")

    cases_path = skill_dir / "evals" / "test_cases.json"
    if cases_path.exists():
        try:
            cases = json.loads(cases_path.read_text(encoding="utf-8"))
            diag.check("test_cases.valid_json", True)
            ok_schema = (
                isinstance(cases, dict)
                and "cases" in cases
                and isinstance(cases["cases"], list)
                and len(cases["cases"]) >= 1
            )
            diag.check("test_cases.schema", ok_schema, "test_cases.json schema invalid")
            skill_version = (
                metadata.get("version") if isinstance(metadata, dict) else None
            )
            cases_version = cases.get("version")
            if skill_version and cases_version and skill_version != cases_version:
                diag.warn(
                    f"version drift: SKILL.md={skill_version} vs test_cases.json={cases_version}"
                )
        except json.JSONDecodeError as e:
            diag.fail(f"test_cases.json invalid JSON: {e}")
    else:
        diag.warn("no evals/test_cases.json found")

    return diag


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skill",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Path to the skill directory (default: parent of this script)",
    )
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Output format",
    )
    args = parser.parse_args()

    skill_dir = args.skill.resolve()
    diag = validate_skill(skill_dir)

    if args.format == "json":
        out = {
            "skill_path": diag.skill_path,
            "passed": diag.passed,
            "errors": diag.errors,
            "warnings": diag.warnings,
            "checks": diag.checks,
        }
        print(json.dumps(out, indent=2))
    else:
        status = "PASS" if diag.passed else "FAIL"
        print(f"[{status}] {diag.skill_path}")
        for e in diag.errors:
            print(f"  error:   {e}")
        for w in diag.warnings:
            print(f"  warning: {w}")

    return 0 if diag.passed else 1


if __name__ == "__main__":
    sys.exit(main())
