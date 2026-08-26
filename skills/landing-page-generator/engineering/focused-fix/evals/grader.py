#!/usr/bin/env python3
"""Score a candidate output against test_cases.json.

Stdlib-only. No LLM calls. The candidate output is whatever an external harness
captures from running the skill against each test case; this grader checks the
captured outputs against the deterministic part of the rubric
(must_contain / must_not_contain / schema). LLM-as-judge scoring is left to the
external harness.

Usage:
    python evals/grader.py --candidate candidate.json --cases evals/test_cases.json

candidate.json schema:
    {
      "skill": "skill-name",
      "outputs": [
        {"case_id": "case-001", "output": "candidate text or JSON string"}
      ]
    }
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def grade_case(case: dict, candidate_output: str) -> dict:
    expected = case.get("expected", {})
    must_contain = expected.get("must_contain", []) or []
    must_not_contain = expected.get("must_not_contain", []) or []

    missing = []
    for needle in must_contain:
        if not _matches(candidate_output, needle):
            missing.append(needle)

    forbidden_hits = []
    for needle in must_not_contain:
        if _matches(candidate_output, needle):
            forbidden_hits.append(needle)

    schema_ok = True
    schema_err: str | None = None
    schema = expected.get("schema")
    if schema and expected.get("format") == "json":
        try:
            parsed = json.loads(candidate_output)
            schema_ok, schema_err = _check_schema(parsed, schema)
        except json.JSONDecodeError as e:
            schema_ok = False
            schema_err = f"candidate is not valid JSON: {e}"

    passed = not missing and not forbidden_hits and schema_ok
    return {
        "case_id": case["id"],
        "weight": case.get("weight", 1.0),
        "passed": passed,
        "missing_required": missing,
        "forbidden_matches": forbidden_hits,
        "schema_ok": schema_ok,
        "schema_error": schema_err,
    }


def _matches(haystack: str, needle: str) -> bool:
    """needle can be a plain substring or, if it starts and ends with '/', a regex."""
    if len(needle) >= 2 and needle.startswith("/") and needle.endswith("/"):
        try:
            return re.search(needle[1:-1], haystack) is not None
        except re.error:
            return needle in haystack
    return needle in haystack


def _check_schema(value, schema: dict) -> tuple[bool, str | None]:
    """Minimal JSONSchema subset: type, required, properties."""
    expected_type = schema.get("type")
    py_type = {
        "object": dict,
        "array": list,
        "string": str,
        "number": (int, float),
        "integer": int,
        "boolean": bool,
        "null": type(None),
    }.get(expected_type)
    if py_type and not isinstance(value, py_type):
        return False, f"expected type {expected_type}, got {type(value).__name__}"

    if expected_type == "object":
        for k in schema.get("required", []):
            if k not in value:
                return False, f"missing required key: {k}"
        for k, sub_schema in schema.get("properties", {}).items():
            if k in value:
                ok, err = _check_schema(value[k], sub_schema)
                if not ok:
                    return False, f"{k}: {err}"

    if expected_type == "array":
        item_schema = schema.get("items")
        if item_schema:
            for i, item in enumerate(value):
                ok, err = _check_schema(item, item_schema)
                if not ok:
                    return False, f"[{i}]: {err}"

    return True, None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path(__file__).resolve().parent / "test_cases.json",
    )
    parser.add_argument("--format", choices=("json", "text"), default="json")
    args = parser.parse_args()

    cases = json.loads(args.cases.read_text(encoding="utf-8"))
    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))

    cases_by_id = {c["id"]: c for c in cases.get("cases", [])}
    outputs_by_id = {o["case_id"]: o["output"] for o in candidate.get("outputs", [])}

    results = []
    for case_id, case in cases_by_id.items():
        if case_id not in outputs_by_id:
            results.append(
                {
                    "case_id": case_id,
                    "weight": case.get("weight", 1.0),
                    "passed": False,
                    "missing_required": [],
                    "forbidden_matches": [],
                    "schema_ok": False,
                    "schema_error": "no candidate output for this case",
                }
            )
            continue
        results.append(grade_case(case, outputs_by_id[case_id]))

    total_weight = sum(r["weight"] for r in results) or 1.0
    passed_weight = sum(r["weight"] for r in results if r["passed"])
    summary = {
        "skill": cases.get("skill"),
        "version": cases.get("version"),
        "score": round(passed_weight / total_weight, 4),
        "passed": passed_weight == total_weight,
        "results": results,
    }

    if args.format == "json":
        print(json.dumps(summary, indent=2))
    else:
        status = "PASS" if summary["passed"] else "FAIL"
        print(
            f"[{status}] {summary['skill']} v{summary['version']} — "
            f"score {summary['score']:.2%}"
        )
        for r in results:
            mark = "✓" if r["passed"] else "✗"
            print(f"  {mark} {r['case_id']}")
            for m in r["missing_required"]:
                print(f"      missing: {m}")
            for f in r["forbidden_matches"]:
                print(f"      forbidden: {f}")
            if r["schema_error"]:
                print(f"      schema: {r['schema_error']}")

    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
