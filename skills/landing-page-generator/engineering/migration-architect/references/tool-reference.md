# Tool Reference

Read this when running, configuring, or debugging the three scripts — full purpose, usage, flag tables, input formats, and output structures.

## migration_planner.py

**Purpose:** Generates comprehensive, phased migration plans with risk assessment, rollback strategies, timeline estimates, and stakeholder communication structures from a JSON migration specification.

**Usage:**
```bash
python scripts/migration_planner.py --input <spec.json> [--output <plan.json>] [--format <format>] [--validate]
```

**Flags/Parameters:**

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--input`, `-i` | Yes | -- | Input migration specification file (JSON). Must contain `type`, `source`, and `target` fields. |
| `--output`, `-o` | No | stdout | Output file path for the migration plan (JSON). Text output saved to same path with `.txt` extension when format includes text. |
| `--format`, `-f` | No | `both` | Output format. Choices: `json`, `text`, `both`. |
| `--validate` | No | false | Validate the migration specification without generating a plan. Exits with 0 if valid. |

**Input Specification Fields:**
- `type` (required): Migration type -- `database`, `service`, `infrastructure`, `data`, or `api`.
- `source` (required): Source system identifier.
- `target` (required): Target system identifier.
- `pattern`: Migration pattern (e.g., `schema_change`, `data_migration`, `strangler_fig`, `parallel_run`, `cloud_migration`, `on_prem_to_cloud`).
- `constraints.data_volume_gb`: Data volume in GB (affects complexity scoring).
- `constraints.dependencies`: List of dependent systems.
- `constraints.max_downtime_minutes`: Maximum allowed downtime in minutes.
- `constraints.special_requirements`: List of additional requirements that increase complexity.
- `constraints.compliance_requirements`: List of compliance frameworks that apply.

**Example:**
```bash
python scripts/migration_planner.py --input migration_spec.json --output plan.json --format both
```

**Output Formats:**
- **JSON:** Complete `MigrationPlan` object with `migration_id`, `phases` (each with tasks, validation criteria, rollback triggers), `risks` (categorized by severity), `rollback_plan`, `success_criteria`, and `stakeholders`.
- **Text:** Human-readable report with sections for phases, risk assessment, rollback strategy, success criteria, and stakeholders.

---

## compatibility_checker.py

**Purpose:** Analyzes schema and API compatibility between two versions, identifies breaking changes, data type mismatches, constraint violations, and generates migration script suggestions with rollback counterparts.

**Usage:**
```bash
python scripts/compatibility_checker.py --before <old.json> --after <new.json> [--type <schema_type>] [--output <report.json>] [--format <format>]
```

**Flags/Parameters:**

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--before` | Yes | -- | Path to the before/old schema file (JSON). |
| `--after` | Yes | -- | Path to the after/new schema file (JSON). |
| `--type` | No | `database` | Schema type to analyze. Choices: `database`, `api`. |
| `--output`, `-o` | No | stdout | Output file path for the compatibility report (JSON). |
| `--format`, `-f` | No | `both` | Output format. Choices: `json`, `text`, `both`. |

**Input Schema Format (database):** JSON with a `tables` object where each key is a table name containing `columns` (with `type`, `nullable`, `length`, `default` per column) and `constraints` (with `primary_key`, `foreign_key`, `unique`, `check`, `index` arrays).

**Input Schema Format (api):** OpenAPI-style JSON with `paths` (keyed by route, containing HTTP methods) and `components.schemas` (keyed by model name with `properties`, `required` arrays, and field `type` definitions).

**Example:**
```bash
python scripts/compatibility_checker.py --before v1_schema.json --after v2_schema.json --type database --format json
```

**Output Formats:**
- **JSON:** `CompatibilityReport` with `overall_compatibility` level, counts by change type (`breaking_changes_count`, `potentially_breaking_count`, `non_breaking_changes_count`, `additive_changes_count`), detailed `issues` list (each with severity, impact, suggested migration), `migration_scripts` (with rollback scripts and validation queries), `risk_assessment`, and `recommendations`.
- **Text:** Human-readable report with color-coded severity sections, issue details, and migration script listings.

---

## rollback_generator.py

**Purpose:** Takes a migration plan (typically the JSON output of `migration_planner.py`) and generates a comprehensive rollback runbook with phase-by-phase reversal steps, automated trigger conditions, data recovery plans, escalation matrices, and communication templates.

**Usage:**
```bash
python scripts/rollback_generator.py --input <plan.json> [--output <runbook.json>] [--format <format>]
```

**Flags/Parameters:**

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--input`, `-i` | Yes | -- | Input migration plan file (JSON). Expects output from `migration_planner.py` or any JSON with `migration_id`, `migration_type`, and `phases` fields. |
| `--output`, `-o` | No | stdout | Output file path for the rollback runbook (JSON). |
| `--format`, `-f` | No | `both` | Output format. Choices: `json`, `text`, `both`. |

**Example:**
```bash
python scripts/migration_planner.py --input spec.json --output plan.json --format json
python scripts/rollback_generator.py --input plan.json --output runbook.json --format both
```

**Output Formats:**
- **JSON:** `RollbackRunbook` object with `runbook_id`, `rollback_phases` (each containing ordered `steps` with script content, validation commands, success criteria, and failure escalation), `trigger_conditions` (with metric thresholds and auto-execute flags), `data_recovery_plan` (backup location, recovery scripts, estimated recovery time), `communication_templates` (for technical, business, and executive audiences), `escalation_matrix`, `validation_checklist`, `post_rollback_procedures`, and `emergency_contacts`.
- **Text:** Human-readable runbook with phase-by-phase rollback instructions, trigger condition summaries, communication templates, and a post-rollback checklist.
