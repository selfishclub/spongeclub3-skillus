#!/usr/bin/env python3
"""
run.py — Runner for the PM eval harness.

Loads rubrics from evals/<skill>/rubric.json and scores worked-example
artifacts under project-management/**/examples/*.md.

Usage:
    python evals/run.py --all
    python evals/run.py --skill create-prd
    python evals/run.py --skill create-prd --artifact path/to/file.md
    python evals/run.py --all --format json
    python evals/run.py --all --threshold 70
"""

import argparse
import json
import sys
from pathlib import Path

# Local import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine import evaluate_artifact  # noqa: E402


REPO = Path(__file__).resolve().parent.parent
EVALS_DIR = Path(__file__).resolve().parent
PM_DIR = REPO / "project-management"


def find_rubric(skill: str) -> Path | None:
    p = EVALS_DIR / skill / "rubric.json"
    return p if p.exists() else None


def all_rubrics() -> list[tuple[str, Path]]:
    rubrics = []
    for sub in sorted(EVALS_DIR.iterdir()):
        if sub.is_dir() and (sub / "rubric.json").exists():
            rubrics.append((sub.name, sub / "rubric.json"))
    return rubrics


def find_skill_dir(skill_name: str) -> Path | None:
    """Find the skill folder under project-management/ (handles nested sub-areas)."""
    # Direct match
    direct = PM_DIR / skill_name
    if direct.is_dir() and (direct / "SKILL.md").exists():
        return direct
    # Under subareas
    for sub in ("discovery", "execution", "career"):
        candidate = PM_DIR / sub / skill_name
        if candidate.is_dir() and (candidate / "SKILL.md").exists():
            return candidate
    return None


def find_examples(skill_name: str) -> list[Path]:
    skill_dir = find_skill_dir(skill_name)
    if not skill_dir:
        return []
    examples_dir = skill_dir / "examples"
    if not examples_dir.is_dir():
        return []
    return sorted(p for p in examples_dir.glob("*.md") if not p.name.startswith("README"))


def score_one(skill_name: str, rubric_path: Path, artifacts: list[Path]) -> list[dict]:
    rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
    results: list[dict] = []
    for art in artifacts:
        text = art.read_text(encoding="utf-8")
        result = evaluate_artifact(rubric, text)
        result["artifact"] = str(art.relative_to(REPO))
        results.append(result)
    return results


def render_markdown(all_results: list[dict], threshold: int) -> str:
    lines = ["# PM Eval Report", ""]
    if not all_results:
        lines.append("_No results._")
        return "\n".join(lines)

    # Aggregate
    total = len(all_results)
    passed_n = sum(1 for r in all_results if r["score"] >= threshold)
    lines.append(f"**{passed_n}/{total} artifacts at or above threshold ({threshold}/100).**")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Skill | Artifact | Score | Pass? |")
    lines.append("|---|---|---:|:---:|")
    for r in all_results:
        skill = r["skill"]
        path = r["artifact"]
        score = r["score"]
        ok = "✓" if score >= threshold else "✗"
        lines.append(f"| {skill} | `{path}` | {score} | {ok} |")
    lines.append("")

    # Per-artifact detail
    for r in all_results:
        lines.append(f"## {r['skill']} — `{r['artifact']}`")
        lines.append(f"Score: **{r['score']}/100**  (raw {r['raw_score']}/{r['max_score']})  ")
        lines.append(f"Passed {r['passed']}/{r['passed']+r['failed']} criteria.")
        lines.append("")
        if r["failed"]:
            lines.append("### Failed criteria")
            lines.append("")
            for row in r["results"]:
                if not row["passed"]:
                    lines.append(f"- **{row['name']}** (weight {row['weight']}) — {row['detail']}")
            lines.append("")
        if r["passed"]:
            lines.append("<details><summary>Passed criteria</summary>")
            lines.append("")
            for row in r["results"]:
                if row["passed"]:
                    lines.append(f"- {row['name']} (weight {row['weight']}) — {row['detail']}")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Run PM skill output evaluations.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true", help="Run all rubrics")
    g.add_argument("--skill", help="Run a single skill's rubric")
    p.add_argument("--artifact", help="Explicit artifact path (overrides examples/ lookup)")
    p.add_argument("--format", choices=("markdown", "json"), default="markdown")
    p.add_argument("--threshold", type=int, default=70, help="Pass threshold (default 70)")
    p.add_argument("--output", help="Write to file instead of stdout")
    args = p.parse_args()

    all_results: list[dict] = []
    skills_to_run: list[tuple[str, Path]] = []

    if args.all:
        skills_to_run = all_rubrics()
        if not skills_to_run:
            sys.exit("ERROR: no rubrics found under evals/")
    else:
        rubric_path = find_rubric(args.skill)
        if not rubric_path:
            sys.exit(f"ERROR: no rubric for skill '{args.skill}' at evals/{args.skill}/rubric.json")
        skills_to_run = [(args.skill, rubric_path)]

    for skill_name, rubric_path in skills_to_run:
        if args.artifact:
            arts = [Path(args.artifact)]
        else:
            arts = find_examples(skill_name)
        if not arts:
            print(f"[warn] no examples for {skill_name}", file=sys.stderr)
            continue
        results = score_one(skill_name, rubric_path, arts)
        all_results.extend(results)

    if args.format == "json":
        out = json.dumps({"results": all_results, "threshold": args.threshold}, indent=2) + "\n"
    else:
        out = render_markdown(all_results, args.threshold)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
    else:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
