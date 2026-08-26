# Evals Template

Drop-in evaluation harness for any skill in this library. Stdlib-only Python (matches the repo's no-ML-in-scripts rule). Produces JSON suitable for CI.

## What this gives you

Every skill that ships with `evals/` provides three things to its callers:

1. **`test_cases.json`** — structured prompts the skill is expected to handle correctly, paired with an output schema and a rubric.
2. **`grader.py`** — stdlib grader. Given a candidate output (JSON or markdown), scores it against the rubric and writes a per-case pass/fail.
3. **`runner.py`** — static validator. Verifies the parent `SKILL.md` has the required structure, that every script referenced in `Tools Overview` exists, and that frontmatter is well-formed. Runs in CI without invoking any model.

Together these answer the question competitors are now asking: *does this skill still produce good output when the model behind it changes?* The static runner catches structural regressions for free; the test-case + grader pair plugs into any external LLM eval harness (Anthropic SDK, OpenAI evals, custom) that can pipe candidate outputs back in.

## How to install into a new skill

```bash
# 1. Copy the template into the target skill
cp -r templates/evals-template/evals/ <domain>/<skill-name>/evals/

# 2. Edit test_cases.json — replace the placeholder cases with real prompts for the skill
# 3. Edit grader.py if the skill needs custom scoring logic (most don't)
# 4. Run the static validator
python <domain>/<skill-name>/evals/runner.py --skill <domain>/<skill-name>

# 5. Wire into CI (see .github/workflows/skill-evals.yml in this repo for an example)
```

## Architecture

```
evals/
├── test_cases.json   # input prompts + expected output schema + rubric
├── grader.py         # scores a candidate output against test_cases.json
├── runner.py         # static validator — runs without a model
└── README.md         # what this skill's evals cover
```

### Static mode (no model required)

```bash
python evals/runner.py --skill ../
# → exits 0 if SKILL.md is structurally sound, scripts referenced exist,
#   test_cases.json is valid; exits non-zero with a JSON diagnostic otherwise.
```

### Graded mode (external model harness pipes results in)

```bash
# Pseudocode for an external harness:
# 1. Read evals/test_cases.json
# 2. For each case: run the skill against case.prompt, capture output
# 3. Write outputs to candidate.json
# 4. python evals/grader.py --candidate candidate.json --cases evals/test_cases.json
```

The grader is deliberately model-agnostic. It only knows how to compare a candidate against a rubric; it does not call any LLM itself. This keeps the repo dependency-free and lets the user pick their own evaluation backend.

## test_cases.json schema

```json
{
  "skill": "skill-name",
  "version": "1.0.0",
  "cases": [
    {
      "id": "case-001",
      "prompt": "Plain-English request a user would make of this skill",
      "expected": {
        "format": "markdown | json | code",
        "must_contain": ["substring-or-regex-1", "..."],
        "must_not_contain": ["anti-pattern-1", "..."],
        "schema": { "...optional JSONSchema fragment..." }
      },
      "rubric": {
        "structure": "Output follows the skill's documented workflow",
        "accuracy": "Concrete claim about correctness this case is checking",
        "scope": "Stays inside the skill's stated scope (no scope creep)"
      },
      "weight": 1.0
    }
  ]
}
```

The `must_contain` / `must_not_contain` arrays are the cheapest, most deterministic signal — use them for facts the skill must always state and footguns it must never produce. The `rubric` block is for LLM-as-judge scoring (when an external harness runs one); ignored in static mode.

## Why this design

- **Stdlib-only:** matches `CLAUDE.md`'s portability rule.
- **No LLM calls in repo scripts:** runner and grader are deterministic; LLM-based grading is delegated to whatever harness the user already trusts.
- **CI-ready:** `runner.py` exits with a status code and emits a JSON diagnostic; drop it into any matrix job.
- **Versioned alongside the skill:** the `version` field in `test_cases.json` should track the parent `SKILL.md` `metadata.version`, so eval drift is detectable.

## Pilot skills using this template

- `engineering/focused-fix/evals/`
- `product-team/ab-test-setup/evals/`

Read those for worked examples of `test_cases.json` filled in with real, skill-specific cases.
