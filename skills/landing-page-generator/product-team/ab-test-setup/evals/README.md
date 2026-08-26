# Evals — ab-test-setup

Drop-in eval harness for the `ab-test-setup` skill. See `../../../templates/evals-template/README.md` for the general pattern.

## What these cases cover

| Case | Tests |
|------|-------|
| `sample-size-basics` | Skill computes (or asks for) baseline, MDE, power, alpha; produces a realistic sample size |
| `no-peeking` | Skill refuses early stopping on interim significance and names the statistical reason |
| `metric-selection-multiple-primary` | Skill enforces a single primary metric / OEC and demotes the rest to guardrails |
| `underpowered-test-warning` | Skill flags an n=500/arm test as underpowered rather than greenlighting it |

## Running

```bash
# Static validation (no model needed)
python evals/runner.py --skill ../

# Graded mode (after an external harness captures outputs)
python evals/grader.py --candidate candidate.json --format text
```

`runner.py` and `grader.py` are copied from `templates/evals-template/evals/` and not modified for this skill — keep them in sync with the template.
