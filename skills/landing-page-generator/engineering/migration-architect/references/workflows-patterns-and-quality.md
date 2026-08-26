# Migration Workflows, Patterns & Quality

Read this when planning a migration: quick-start commands, the three core workflows with validation checkpoints, the migration-pattern catalog table, anti-patterns, troubleshooting, and success criteria.

## Quick Start

```bash
# Generate a phased migration plan
python scripts/migration_planner.py --input migration_spec.json --output plan.json --format both

# Check schema compatibility between versions
python scripts/compatibility_checker.py --before v1_schema.json --after v2_schema.json --type database

# Generate rollback runbook from a migration plan
python scripts/rollback_generator.py --input plan.json --output runbook.json --format both
```

## Core Workflows

### Workflow 1: Plan a Database Migration

1. Create migration spec JSON with `type: "database"`, source, target, constraints (data volume, max downtime, dependencies)
2. Run `migration_planner.py` to generate phased plan with risk assessment
3. Run `compatibility_checker.py` to detect breaking schema changes
4. Review generated phases -- each should have validation criteria and rollback triggers
5. **Validation checkpoint:** Zero unaddressed breaking changes; every phase has rollback steps; downtime within `max_downtime_minutes` constraint

```bash
python scripts/compatibility_checker.py --before v1.json --after v2.json --type database --format json
python scripts/migration_planner.py --input spec.json --output plan.json
python scripts/rollback_generator.py --input plan.json --output runbook.json
```

### Workflow 2: Plan a Service Migration (Strangler Fig)

1. Define spec with `type: "service"`, `pattern: "strangler_fig"`, source/target services, and dependencies
2. Generate migration plan with traffic routing phases (10% -> 50% -> 100%)
3. Review rollback triggers at each traffic percentage gate
4. **Validation checkpoint:** Circuit breaker thresholds defined; monitoring configured; feature flags lock rollout percentage between phases

### Workflow 3: Validate Migration Compatibility

1. Export before/after schemas as JSON (database or OpenAPI format)
2. Run `compatibility_checker.py` to identify breaking changes, type mismatches, and constraint violations
3. Review generated migration scripts and their rollback counterparts
4. **Validation checkpoint:** All breaking changes have migration scripts; rollback scripts verified; validation queries pass

## Migration Patterns

| Pattern | Type | Best For |
|---------|------|----------|
| Expand-Contract | Database | Zero-downtime schema evolution with backfill |
| Dual-Write | Database | Maintaining consistency during transition |
| Change Data Capture | Database | Large dataset migration with eventual consistency |
| Strangler Fig | Service | Incremental service replacement via gateway routing |
| Parallel Run | Service | Shadow traffic for correctness validation |
| Canary Deployment | Service | Gradual traffic shift with metric monitoring |
| Blue-Green | Infrastructure | Instant cutover with full rollback capability |

## Anti-Patterns

- **Big bang migration** -- migrating everything at once maximizes blast radius; always use phased execution with validation gates
- **Stale backups** -- taking backups at plan creation instead of immediately before execution; always create fresh backup as first execution task
- **Skipping staging** -- production-only migration attempts have no safety net; run the full process in a staging environment first
- **No data reconciliation** -- row counts match but data differs; use checksum validation and business logic queries on critical tables
- **Ignoring dependent systems** -- breaking downstream consumers during cutover; map all dependencies and coordinate migration windows
- **Feature flag drift** -- changing rollout percentage mid-phase causes inconsistent user experience; lock flags during each phase

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Compatibility checker reports false positives on type changes | Source and target schemas use vendor-specific type aliases (e.g., `serial` vs `int`) that are not in the built-in type compatibility matrix | Normalize type aliases to canonical SQL/JSON types in both schema files before running the checker |
| Migration planner generates unrealistic duration estimates | Complexity multiplier does not account for organizational factors like change-board approvals or cross-team coordination | Adjust the `constraints` block in your input spec to include `special_requirements` entries for each non-technical blocker |
| Rollback generator produces empty rollback steps for a phase | The phase name in the migration plan does not match any of the recognized keywords (`migration`, `cutover`, `preparation`) | Use standard phase names from the planner output, or ensure custom phase names contain one of the recognized keywords |
| Data validation fails after migration but row counts match | Soft deletes, filtered records, or computed columns cause hash/checksum mismatches even when primary data is intact | Use business logic validation (aggregate queries on key columns) instead of full-row checksums for tables with soft deletes or generated columns |
| Dual-write pattern causes write conflicts during cutover | Race conditions between source and target systems when replication lag exceeds the write interval | Implement idempotent writes with conflict-resolution timestamps, and increase the delta-sync frequency before the cutover window |
| Rollback triggered but legacy database backup is stale | Backup was taken at plan creation time rather than immediately before the migration execution phase | Always create a fresh backup as the first task of the migration execution phase; reference `migration_planner.py` preparation-phase tasks |
| Feature flag rollout causes inconsistent user experience | Hash-based routing sends the same user to different paths across sessions when the flag name or rollout percentage changes mid-migration | Lock the flag name and rollout percentage during each migration phase; only adjust between validated phase gates |

## Success Criteria

- **Data Integrity:** 100% of records pass post-migration checksum and referential-integrity validation with zero data loss or corruption.
- **Downtime Within Budget:** Actual service unavailability stays within the `max_downtime_minutes` constraint defined in the migration spec (target: zero-downtime for critical systems).
- **Performance Parity:** P95 latency and throughput on the target system are within 10% of pre-migration baseline measurements during the first 72 hours after cutover.
- **Rollback Readiness:** Every migration phase has a tested rollback procedure that can restore the previous state within 25% of the original phase duration.
- **Stakeholder Sign-off:** All stakeholders listed in the migration plan confirm acceptance criteria are met before legacy decommission begins.
- **Zero Critical Defects:** No severity-critical or severity-high issues remain unresolved 48 hours after cutover; all issues are tracked with owners and ETAs.
- **Compliance Continuity:** All regulatory and compliance controls (audit logging, access controls, encryption) remain fully operational throughout the migration and are validated in the target environment.
