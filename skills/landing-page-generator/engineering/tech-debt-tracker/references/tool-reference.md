# Tool Reference & Troubleshooting

Read this when running the scanner, prioritizer, or dashboard scripts, configuring their flags, interpreting their JSON/text output, or debugging unexpected results.

## Debt Scanner (`scripts/debt_scanner.py`)

**Purpose:** Scans a codebase directory for technical debt signals using AST parsing (Python files) and regex pattern matching (all languages). Detects code smells, large functions, high complexity, duplicate code, TODO comments, and common anti-patterns. Produces a structured JSON inventory and a human-readable text report.

**Usage:**
```bash
python scripts/debt_scanner.py <directory> [options]
```

**Parameters:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `directory` | positional, required | -- | Path to the directory to scan. |
| `--config` | string | None | Path to a JSON configuration file that overrides default thresholds (e.g., `max_function_length`, `max_complexity`, `ignore_patterns`). |
| `--output` | string | None | Output file path. When set, writes report to file instead of stdout. JSON output appends `.json`, text output appends `.txt`. |
| `--format` | choice | `both` | Output format: `json`, `text`, or `both`. |

**Example:**
```bash
python scripts/debt_scanner.py ./src --config custom_thresholds.json --output scan_results --format both
```

**Output Formats:**
- **JSON:** Contains `scan_metadata`, `summary` (files scanned, lines scanned, health score, debt density, priority/type breakdowns), `debt_items` (array of debt objects with id, type, description, file_path, severity, metadata, priority_score, priority), `file_statistics`, and `recommendations`.
- **Text:** Human-readable report with header, summary statistics, priority breakdown, top 10 debt items, and numbered recommendations.

---

## Debt Prioritizer (`scripts/debt_prioritizer.py`)

**Purpose:** Takes a debt inventory (from the scanner or a manual JSON file) and enriches each item with effort estimates, business impact scores, interest rate calculations, and cost-of-delay values. Produces a prioritized backlog with sprint allocation recommendations using one of three frameworks: cost-of-delay, WSJF, or RICE.

**Usage:**
```bash
python scripts/debt_prioritizer.py <inventory_file> [options]
```

**Parameters:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `inventory_file` | positional, required | -- | Path to debt inventory JSON file (scanner output, prioritizer output, or raw array of debt items). |
| `--output` | string | None | Output file path. JSON output appends `.json`, text output appends `.txt`. |
| `--format` | choice | `both` | Output format: `json`, `text`, or `both`. |
| `--framework` | choice | `cost_of_delay` | Prioritization framework: `cost_of_delay`, `wsjf`, or `rice`. |
| `--team-size` | integer | `5` | Number of developers on the team. Affects interest rate team impact multiplier and RICE reach calculation. |
| `--sprint-capacity` | integer | `80` | Total sprint capacity in hours. 20% is allocated to debt work by default. Used for sprint allocation planning. |

**Example:**
```bash
python scripts/debt_prioritizer.py scan_results.json --framework wsjf --team-size 8 --sprint-capacity 120 --output prioritized --format json
```

**Output Formats:**
- **JSON:** Contains `metadata` (analysis date, framework, team size, sprint capacity), `prioritized_backlog` (enriched items sorted by priority score, each with `effort_estimate`, `business_impact`, `interest_rate`, `cost_of_delay`, `category`, `impact_tags`), `sprint_allocation` (total debt hours, capacity per sprint, sprint plan with item assignments), `insights` (category distribution, effort breakdown, quick wins count, cost totals), `charts_data` (scatter, pie, timeline, interest trend arrays), and `recommendations`.
- **Text:** Executive summary with total effort and cost-of-delay, sprint allocation plan (first 3 sprints with top items), top 10 priority items with scores and tags, and numbered recommendations.

---

## Debt Dashboard (`scripts/debt_dashboard.py`)

**Purpose:** Takes one or more historical debt inventory files (from the scanner or prioritizer) and generates trend analysis, debt velocity tracking (accruing vs. paying down), health score timelines, forecasts, and an executive summary. Supports loading files individually or from a directory.

**Usage:**
```bash
python scripts/debt_dashboard.py [files...] [options]
```

**Parameters:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `files` | positional, optional | -- | One or more debt inventory JSON file paths. Accepts scanner output, prioritizer output, or raw arrays. |
| `--input-dir` | string | None | Directory containing debt inventory JSON files. All `*.json` files in the directory are loaded. Mutually exclusive usage with positional `files`. |
| `--output` | string | None | Output file path. JSON output appends `.json`, text output appends `.txt`. |
| `--format` | choice | `both` | Output format: `json`, `text`, or `both`. |
| `--period` | choice | `monthly` | Analysis period for trend grouping: `weekly`, `monthly`, or `quarterly`. |
| `--team-size` | integer | `5` | Number of developers on the team. Used for velocity impact estimation. |

**Example:**
```bash
python scripts/debt_dashboard.py --input-dir ./debt_scans/ --period quarterly --team-size 10 --output dashboard --format both
```

**Output Formats:**
- **JSON:** Contains `metadata` (generated date, period, snapshot count, date range, team size), `executive_summary` (overall status, health score, status message, key insights, total debt items, effort hours, high priority count, velocity impact percent), `current_health` (overall score, debt density, velocity impact, quality score, maintainability score, technical risk score), `trend_analysis` (per-metric trend direction, change rate, correlation strength, forecast, confidence interval), `debt_velocity` (per-period new/resolved items, net change, velocity ratio, effort hours added/resolved), `forecasts` (3-month and 6-month projections for health, debt count, risk), `recommendations` (prioritized strategic actions with category, impact, effort), `visualizations` (health timeline, debt accumulation, category distribution, velocity chart, effort trend arrays), and `detailed_metrics`.
- **Text:** Executive summary with status and key metrics, current health metrics, trend analysis with directional indicators, and top 5 strategic recommendations with priority, impact, and effort ratings.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Scanner finds zero debt items | Target directory contains no recognized file extensions, or all files match ignore patterns | Verify the directory path is correct and contains source files. Check `--config` to ensure `file_extensions` and `ignore_patterns` are appropriate for your stack. |
| AST parsing errors on valid Python files | Files use syntax from a newer Python version than the runtime executing the scanner | Run the scanner with the same Python version the target codebase requires (e.g., `python3.12 scripts/debt_scanner.py`). |
| Duplicate code detection is slow on large repos | The scanner hashes every N-line sliding window across all files, which scales quadratically with file count | Reduce scope by scanning one service directory at a time, or increase `min_duplicate_lines` in the config to reduce candidate blocks. |
| Prioritizer produces all-zero cost-of-delay scores | Input inventory lacks `severity` or `type` fields that the enrichment step depends on | Ensure the inventory JSON was produced by `debt_scanner.py` or follows the Debt Item Data Structure documented in methodology.md. Manual inventories must include `type` and `severity` per item. |
| Dashboard shows "No valid data files loaded" | Files passed as arguments are not valid JSON, or the JSON structure is unrecognized | The dashboard accepts scanner output (`debt_items` key), prioritizer output (`prioritized_backlog` key), or a raw JSON array of debt items. Validate file contents with `python -m json.tool <file>`. |
| Health score is unexpectedly low despite few critical items | High debt density (items per file) dominates the health formula even when individual severities are low | Review the density contribution: health penalizes 10 points per item-per-file. Break large files into smaller modules or resolve low-severity bulk items like `todo_comment` and `missing_docstring`. |
| Sprint allocation plan shows hundreds of sprints | Default debt capacity is 20% of `--sprint-capacity`, which may be too low for a large backlog | Increase `--sprint-capacity` to reflect actual team hours, or filter the inventory to high-priority items before running the prioritizer. |
