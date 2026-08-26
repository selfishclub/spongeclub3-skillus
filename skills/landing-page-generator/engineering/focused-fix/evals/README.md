# Evals — focused-fix

Drop-in eval harness for the `focused-fix` skill. See `../../../templates/evals-template/README.md` for the general pattern.

## What these cases cover

| Case | Tests |
|------|-------|
| `minimal-scope-basic` | Skill identifies a minimal change set and requires a regression test, doesn't pivot to a refactor |
| `reject-scope-creep` | Skill holds the line on the "while I'm here" anti-pattern, recommends a separate PR |
| `structural-fix-escalation` | Skill treats analyzer-reported "structural" scope as a halt condition, not advice |
| `missing-regression-test` | Skill refuses to skip the regression test on a one-line fix |

## Running

```bash
# Static validation (no model needed)
python evals/runner.py --skill ../

# Graded mode (after an external harness captures outputs)
python evals/grader.py --candidate candidate.json --format text
```

`runner.py` and `grader.py` are copied from `templates/evals-template/evals/` and not modified for this skill — keep them in sync with the template.
