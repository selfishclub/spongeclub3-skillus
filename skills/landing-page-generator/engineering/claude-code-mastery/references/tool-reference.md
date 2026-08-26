# Tool Reference

Read this for the full parameter tables and output formats of the three Python tools. Quick commands live in the SKILL.md Tools table.

## Tools (summary)

### Skill Scaffolder

Generates a skill directory with SKILL.md template, scripts/, references/,
assets/ directories, and YAML frontmatter.

```bash
python scripts/skill_scaffolder.py my-skill --domain engineering --description "Does X"
```

| Parameter | Description |
|-----------|-------------|
| `skill_name` | Name for the skill (kebab-case) |
| `--domain, -d` | Domain category |
| `--description` | Brief description for frontmatter |
| `--version` | Semantic version (default: 1.0.0) |
| `--license` | License type (default: MIT) |
| `--output, -o` | Parent directory for skill folder |
| `--json` | Output as JSON |

### CLAUDE.md Optimizer

Analyzes a CLAUDE.md file and produces optimization recommendations.

```bash
python scripts/claudemd_optimizer.py CLAUDE.md --token-limit 4000 --json
```

**Output includes:** line count, token estimate, section completeness,
redundancy detection, missing sections, scored recommendations.

### Context Analyzer

Scans a project to estimate context window consumption by file category.

```bash
python scripts/context_analyzer.py /path/to/project --max-depth 4 --json
```

**Output includes:** token estimates per category, percentage of context
consumed, largest files, budget breakdown, reduction recommendations.

## Detailed Tool Reference

### 1. Skill Scaffolder (`scripts/skill_scaffolder.py`)

**Purpose:** Generate a complete skill package directory with SKILL.md template, starter Python script, reference document, and proper YAML frontmatter.

**Usage:**

```bash
python scripts/skill_scaffolder.py <skill_name> [options]
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `skill_name` | positional | Yes | -- | Name for the skill in kebab-case (e.g., `my-new-skill`) |
| `--domain, -d` | string | No | `engineering` | Domain category. Options: `engineering`, `marketing`, `product`, `project-management`, `c-level`, `ra-qm`, `business-growth`, `finance`, `standards`, `development-tools` |
| `--description` | string | No | auto-generated | Brief description for YAML frontmatter, optimized for auto-discovery |
| `--version` | string | No | `1.0.0` | Semantic version for metadata |
| `--license` | string | No | `MIT` | License type for frontmatter |
| `--category` | string | No | same as domain | Skill category for metadata |
| `--output, -o` | string | No | `.` (current dir) | Parent directory for the skill folder |
| `--json` | flag | No | off | Output results in JSON format |

**Example:**

```bash
python scripts/skill_scaffolder.py api-analyzer -d engineering --description "API analysis and optimization" --json
```

**Output Formats:**

- **Human-readable (default):** Prints skill name, domain, version, location, directory tree, and next-steps checklist.
- **JSON (`--json`):** Returns `{ success, path, name, domain, version, directories_created, files_created }`.

---

### 2. CLAUDE.md Optimizer (`scripts/claudemd_optimizer.py`)

**Purpose:** Analyze a CLAUDE.md file for structure completeness, token efficiency, redundancy, and verbosity. Produces a scored report with prioritized optimization recommendations.

**Usage:**

```bash
python scripts/claudemd_optimizer.py <file_path> [options]
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file_path` | positional | Yes | -- | Path to the CLAUDE.md file to analyze |
| `--token-limit` | integer | No | `6000` | Maximum recommended token count for the file |
| `--json` | flag | No | off | Output results in JSON format |

**Example:**

```bash
python scripts/claudemd_optimizer.py path/to/CLAUDE.md --token-limit 4000
```

**Output Formats:**

- **Human-readable (default):** Displays score (0-100), file metrics (lines, words, tokens), section breakdown with per-section token estimates, section completeness checklist (critical/high/medium), redundancy issues, and prioritized recommendations (HIGH/MEDIUM/LOW).
- **JSON (`--json`):** Returns `{ success, file, metrics, sections, completeness, redundancies, recommendations, score }`.

---

### 3. Context Analyzer (`scripts/context_analyzer.py`)

**Purpose:** Scan a project directory to estimate how much of Claude Code's context window is consumed by CLAUDE.md files, skill definitions, source code, and configuration. Produces a token budget breakdown with reduction recommendations.

**Usage:**

```bash
python scripts/context_analyzer.py <project_path> [options]
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `project_path` | positional | Yes | -- | Path to the project directory to analyze |
| `--max-depth` | integer | No | `5` | Maximum directory traversal depth |
| `--context-window` | integer | No | `200000` | Total context window size in tokens |
| `--json` | flag | No | off | Output results in JSON format |

**Example:**

```bash
python scripts/context_analyzer.py /path/to/project --max-depth 3 --context-window 200000 --json
```

**Output Formats:**

- **Human-readable (default):** Displays project summary (files scanned, total tokens, auto-loaded tokens), context budget breakdown with visual bar chart, per-category breakdown (Claude Configuration, Skill Definitions, Reference Documents, Source Code, Config & Build, Documentation) with largest files listed, top 20 largest files, and prioritized recommendations.
- **JSON (`--json`):** Returns `{ success, project_path, context_window, summary, categories, budget, largest_files, recommendations }`.
