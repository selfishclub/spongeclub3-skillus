# Core Workflows

Step-by-step procedures with validation checkpoints. Read this when starting a TDD cycle, analyzing coverage gaps, or generating tests from requirements.

## Workflow 1: TDD a New Feature

1. Write a failing test for the feature requirement (RED phase)
2. Call `validate_red_phase()` -- confirms test exists and fails
3. Write minimal code to make the test pass (GREEN phase)
4. Call `validate_green_phase()` -- confirms all tests pass
5. Refactor while keeping tests green (REFACTOR phase)
6. Call `validate_refactor_phase()` -- confirms tests still pass after cleanup
7. **Validation checkpoint:** Each cycle completes in under 10 minutes; zero test smells introduced

## Workflow 2: Analyze Coverage Gaps

1. Generate coverage report: `npm test -- --coverage` or `pytest --cov`
2. Detect format with `detect_format()` and parse with `parse_coverage_report()`
3. Run `identify_gaps(threshold=80.0)` to get prioritized file list (P0/P1/P2)
4. Generate test stubs for P0 files (business-critical, lowest coverage)
5. **Validation checkpoint:** Line coverage >= 80%; branch coverage >= 70%; zero P0 gaps in critical paths

## Workflow 3: Generate Tests from Requirements

1. Structure requirements as user stories with acceptance criteria
2. Call `generate_from_requirements()` with target framework
3. Review generated test cases for completeness (happy path, error, edge cases)
4. Generate test file with `generate_test_file()`
5. **Validation checkpoint:** Each acceptance criterion has at least one test; all tests compile
