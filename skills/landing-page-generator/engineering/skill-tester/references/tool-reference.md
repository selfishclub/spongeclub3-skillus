# Tool Reference

Read this for the full parameter tables, output formats, and exit codes of the three Python tools.

## skill_validator.py

**Purpose:** Validates a skill directory's structure, documentation, and Python scripts against the claude-skills ecosystem standards. Checks required files, YAML frontmatter, required SKILL.md sections, directory layout, script syntax, import compliance, and tier-specific requirements.

**Usage:**
```bash
python skill_validator.py <skill_path> [--tier TIER] [--json] [--verbose]
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `skill_path` | positional | Yes | — | Path to the skill directory to validate |
| `--tier` | option | No | None | Target tier for validation: `BASIC`, `STANDARD`, or `POWERFUL` |
| `--json` | flag | No | Off | Output results in JSON format instead of human-readable text |
| `--verbose` | flag | No | Off | Enable verbose logging to stderr |

**Example:**
```bash
python skill_validator.py engineering/my-skill --tier POWERFUL --json
```

**Output Formats:**
- **Human-readable (default):** Grouped report with STRUCTURE VALIDATION, SCRIPT VALIDATION, ERRORS, WARNINGS, and SUGGESTIONS sections. Displays overall score out of 100 with compliance level (EXCELLENT, GOOD, ACCEPTABLE, NEEDS_IMPROVEMENT, POOR).
- **JSON (`--json`):** Object with keys `skill_path`, `timestamp`, `overall_score`, `compliance_level`, `checks` (dict of check name to pass/message/score), `warnings`, `errors`, `suggestions`.

**Exit codes:** `0` on success (score >= 60 and no errors), `1` on failure.

---

## script_tester.py

**Purpose:** Tests all Python scripts within a skill's `scripts/` directory. Performs syntax validation via AST parsing, import analysis for stdlib compliance, argparse implementation verification, main guard detection, runtime execution with timeout protection, `--help` functionality testing, sample data processing against files in `assets/`, and output format compliance checks.

**Usage:**
```bash
python script_tester.py <skill_path> [--timeout SECONDS] [--json] [--verbose]
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `skill_path` | positional | Yes | — | Path to the skill directory containing scripts to test |
| `--timeout` | option | No | `30` | Timeout in seconds for each script execution test |
| `--json` | flag | No | Off | Output results in JSON format instead of human-readable text |
| `--verbose` | flag | No | Off | Enable verbose logging to stderr |

**Example:**
```bash
python script_tester.py engineering/my-skill --timeout 60 --json
```

**Output Formats:**
- **Human-readable (default):** Report with SUMMARY (total/passed/partial/failed counts), GLOBAL ERRORS, and per-script sections showing status, execution time, individual test results, errors, and warnings.
- **JSON (`--json`):** Object with keys `skill_path`, `timestamp`, `summary` (counts and overall status), `global_errors`, `script_results` (dict per script with `overall_status`, `execution_time`, `tests`, `errors`, `warnings`).

**Exit codes:** `0` on full success, `1` on failure or global errors, `2` on partial success.

---

## quality_scorer.py

**Purpose:** Provides a comprehensive multi-dimensional quality assessment for a skill. Evaluates four equally weighted dimensions — Documentation (25%), Code Quality (25%), Completeness (25%), and Usability (25%) — and produces an overall score, letter grade (A+ through F), tier recommendation, and a prioritized improvement roadmap.

**Usage:**
```bash
python quality_scorer.py <skill_path> [--detailed] [--minimum-score SCORE] [--json] [--verbose]
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `skill_path` | positional | Yes | — | Path to the skill directory to assess |
| `--detailed` | flag | No | Off | Show detailed component scores within each dimension |
| `--minimum-score` | option | No | `0` | Minimum acceptable overall score; exits with error code `1` if the score falls below this threshold |
| `--json` | flag | No | Off | Output results in JSON format instead of human-readable text |
| `--verbose` | flag | No | Off | Enable verbose logging to stderr |

**Example:**
```bash
python quality_scorer.py engineering/my-skill --detailed --minimum-score 75 --json
```

**Output Formats:**
- **Human-readable (default):** Report with overall score and letter grade, per-dimension scores with weights, summary statistics (highest/lowest dimension, dimensions above 70%, dimensions below 50%), and a prioritized improvement roadmap (up to 5 items with HIGH/MEDIUM/LOW priority). When `--detailed` is used, component-level breakdowns appear under each dimension.
- **JSON (`--json`):** Object with keys `skill_path`, `timestamp`, `overall_score`, `letter_grade`, `tier_recommendation`, `summary_stats`, `dimensions` (per-dimension name/weight/score/details/suggestions), `improvement_roadmap` (list of priority/dimension/suggestion/current_score objects).

**Exit codes:** `0` for grades A+ through C-, `1` for grade F or when score is below `--minimum-score`, `2` for grade D.
