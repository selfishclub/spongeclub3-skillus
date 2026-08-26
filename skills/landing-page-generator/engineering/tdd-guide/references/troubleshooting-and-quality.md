# Troubleshooting, Anti-Patterns & Success Criteria

Diagnostics and quality bars for TDD work. Read this when tests behave unexpectedly, when reviewing for TDD anti-patterns, or when defining the definition of done for test quality.

## Anti-Patterns

- **Tests that pass immediately** -- a test with no real assertion or `assert True` skips the RED phase; every test must fail before implementation
- **Testing implementation details** -- coupling tests to internal method names makes refactoring break tests; test behavior and outputs, not internals
- **Non-deterministic fixtures** -- random data without a seed produces different failures across CI runs; always pass `seed=<int>` to `FixtureGenerator`
- **Skipping the refactor phase** -- GREEN code that works but is messy accumulates; refactoring is not optional in TDD
- **Coverage theater** -- writing tests that hit lines without meaningful assertions; use `metrics_calculator.py` to detect low assertion density
- **Conditional test logic** -- `if/else` inside tests masks failures; each test should have a single clear path

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Generated tests pass immediately (no RED phase) | Test has no real assertion or asserts a trivially true value | Ensure every test contains an assertion against the actual unit under test; remove placeholder `assert True` stubs before running |
| Coverage report fails to parse | Report format does not match the expected LCOV, JSON, or XML structure | Run `format_detector.py` first to verify the detected format; convert non-standard reports (e.g., Clover) to Cobertura XML |
| Framework adapter produces wrong import style | Source and target framework were swapped, or language/framework mismatch | Verify the `framework` and `language` arguments match your project; use `detect_framework()` on existing test code to auto-detect |
| Fixture generator produces non-deterministic data | No random seed was supplied, so each run yields different values | Pass `seed=<int>` to `FixtureGenerator()` for reproducible fixtures across CI runs |
| Metrics calculator reports 0 test functions | Test code uses an unsupported naming convention (e.g., `spec_` prefix) | Rename tests to follow `test_*` / `it()` / `@Test` conventions, or extend the regex patterns in `_count_test_functions()` |
| TDD workflow validates GREEN phase but tests still fail locally | Test result dict passed to `validate_green_phase()` has `status` not set to `"passed"` | Ensure your test runner output is normalized to `{"status": "passed"}` or `{"status": "failed"}` before passing it in |
| Coverage gaps list is empty despite low overall coverage | All individual files meet the threshold even though the aggregate does not | Lower the `threshold` argument in `identify_gaps()` or inspect per-file coverage with `get_file_coverage()` |

---

## Success Criteria

- **Test-first ratio above 80%** -- at least 4 out of every 5 features begin with a failing test before any implementation code is written.
- **Red-green-refactor cycle under 10 minutes** -- each TDD micro-cycle (write failing test, make it pass, refactor) completes within a single focused interval.
- **Line coverage at or above 80%** -- measured by `coverage_analyzer.py` against LCOV/JSON/XML reports, with branch coverage at or above 70%.
- **Test quality score at or above 75/100** -- as reported by `metrics_calculator.py`, combining assertion density, isolation, naming quality, and absence of test smells.
- **Zero P0 coverage gaps in critical paths** -- business-critical modules (auth, payments, data persistence) have no files flagged P0 by `identify_gaps()`.
- **Test smell count of zero for high-severity items** -- no `missing_assertions`, `sleepy_test`, or `conditional_test_logic` smells detected at high severity.
- **Fixture reproducibility across CI** -- all generated fixtures use a fixed seed and produce identical output on every pipeline run.
