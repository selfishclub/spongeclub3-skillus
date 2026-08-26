# Tools, System Integrations, Troubleshooting & Success Criteria

Read this when running the three scripts (full flag/output reference), wiring into Prometheus/Grafana/Jaeger/PagerDuty, diagnosing observability failures, or checking work against success-criteria targets.

## Scripts

### SLO Designer (`slo_designer.py`)
Generates SLI/SLO frameworks from service description JSON. Outputs SLI definitions, SLO targets, error budgets, burn-rate alerts, and SLA recommendations.

### Alert Optimizer (`alert_optimizer.py`)
Analyzes existing alert configurations for noise, coverage gaps, and duplicate rules. Outputs an optimization report with improved thresholds.

### Dashboard Generator (`dashboard_generator.py`)
Creates Grafana-compatible dashboard JSON from service/system descriptions. Covers golden signals, RED/USE methods, and role-based views.

## Integration Points (Systems)

| System | Integration |
|--------|------------|
| Prometheus | Metric collection and alerting rules |
| Grafana | Dashboard creation and visualization |
| Elasticsearch/Kibana | Log analysis and search |
| Jaeger/Zipkin | Distributed tracing |
| PagerDuty/VictorOps | Alert routing and escalation |
| Slack/Teams | Notification delivery |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Burn-rate alerts never fire | SLO target set too low or error budget too generous for actual traffic | Tighten SLO target incrementally (e.g., 99.5% to 99.9%) and verify metric expressions return non-zero values using `rate()` over a short window |
| Alert storm during deployments | No suppression rules for planned rollouts; alerts lack hysteresis | Add deployment-aware silence windows in Alertmanager and configure `for:` clauses of at least 2-5 minutes on all alerts |
| Dashboard panels show "No Data" | Metric names or label selectors do not match what the exporter publishes | Run `curl localhost:9090/api/v1/label/__name__/values` to list available metrics and cross-check label filters in panel queries |
| High cardinality causing Prometheus OOM | Unbounded labels (user ID, request ID) on metrics | Remove high-cardinality labels from instrumentation; use `metric_relabel_configs` to drop offending series and set a cardinality alert at 10K unique combinations |
| Error budget drains faster than expected | SLI numerator counts partial failures (e.g., retried requests counted twice) | Ensure good/total event counters use the same request scope; deduplicate at the instrumentation layer, not the query layer |
| Trace sampling misses critical errors | Head-based sampling drops error spans at the same rate as success spans | Switch to tail-based sampling in production so 100% of error and slow spans are retained regardless of base sample rate |
| Runbooks go stale after service changes | No ownership or review cadence tied to alerts | Link each alert YAML to a runbook file in version control; add a CI check that fails if an alert references a missing or outdated runbook |

## Success Criteria

- Alert noise ratio below 10% -- fewer than 1 in 10 pages should be false positives or non-actionable.
- SLO compliance above 99.5% across all Tier-1 services measured over a rolling 30-day window.
- Mean time to detect (MTTD) under 5 minutes for Tier-1 service degradations via burn-rate alerts.
- Every critical alert has an associated runbook that was reviewed within the last 90 days.
- Dashboard load time under 2 seconds with default time range for all role-based views.
- Trace coverage spans 100% of Tier-1 service boundaries with tail-based sampling retaining all error and P99+ latency spans.
- Error budget consumption is reviewed weekly by the owning team with documented decisions on whether to freeze or proceed with deployments.

## Tool Reference

### SLO Designer (`scripts/slo_designer.py`)

**Purpose:** Generates complete SLI/SLO frameworks from service definitions, including SLI metric expressions, SLO targets, error budgets, multi-window burn-rate alerts, and SLA recommendations.

**Usage:**
```bash
python slo_designer.py --input service_definition.json --output slo_framework.json
python slo_designer.py --service-type api --criticality high --user-facing true
python slo_designer.py --service-type web --criticality critical --user-facing true --summary-only
```

**Flags/Parameters:**

| Flag | Short | Required | Description |
|------|-------|----------|-------------|
| `--input` | `-i` | No* | Input service definition JSON file |
| `--output` | `-o` | No | Output framework JSON file (defaults to `{service_name}_slo_framework.json`) |
| `--service-type` | -- | No* | Service type: `api`, `web`, `database`, `queue`, `batch`, `ml` |
| `--criticality` | -- | No* | Service criticality level: `critical`, `high`, `medium`, `low` |
| `--user-facing` | -- | No* | Whether service is user-facing: `true`, `false` |
| `--service-name` | -- | No | Service name (defaults to `{service_type}_service`) |
| `--summary-only` | -- | No | Only display summary, do not save JSON |

*Either `--input` or all three of `--service-type`, `--criticality`, and `--user-facing` are required.

**Example:**
```bash
python slo_designer.py --service-type api --criticality high --user-facing true --service-name payment-api --output payment_slo.json
```

**Output Formats:** JSON file containing `metadata`, `slis`, `slos`, `error_budgets`, `sla_recommendations`, `monitoring_recommendations`, and `implementation_guide`. Also prints a human-readable summary to stdout.

---

### Alert Optimizer (`scripts/alert_optimizer.py`)

**Purpose:** Analyzes existing alert configurations to identify noisy alerts, coverage gaps, duplicate rules, poor thresholds, missing runbooks, and routing issues. Generates an optimization report and optionally an improved configuration.

**Usage:**
```bash
python alert_optimizer.py --input alerts.json --analyze-only
python alert_optimizer.py --input alerts.json --output optimized_alerts.json
python alert_optimizer.py --input alerts.json --report report.html --format html
```

**Flags/Parameters:**

| Flag | Short | Required | Description |
|------|-------|----------|-------------|
| `--input` | `-i` | Yes | Input alert configuration JSON file |
| `--output` | `-o` | No | Output optimized configuration JSON file (defaults to `optimized_alerts.json`) |
| `--report` | `-r` | No | Generate analysis report to specified file path |
| `--format` | -- | No | Report format: `json` (default), `html` |
| `--analyze-only` | -- | No | Only perform analysis, do not generate optimized config |

**Example:**
```bash
python alert_optimizer.py --input prod_alerts.json --analyze-only --report analysis.json --format json
```

**Output Formats:** JSON or HTML report containing noise analysis (scored alerts with reasons and recommendations), coverage gap analysis (missing categories and golden signals), duplicate detection (exact and semantic duplicates), and optimization recommendations. When not using `--analyze-only`, also outputs a rewritten alert configuration file.

---

### Dashboard Generator (`scripts/dashboard_generator.py`)

**Purpose:** Creates Grafana-compatible dashboard JSON specifications from service definitions. Covers golden signals, RED/USE methods, role-based views (SRE, Developer, Executive, Ops), and drill-down paths for troubleshooting workflows.

**Usage:**
```bash
python dashboard_generator.py --input service_definition.json --output dashboard_spec.json
python dashboard_generator.py --service-type api --name "Payment Service" --output payment_dashboard.json
python dashboard_generator.py --service-type web --name "Frontend" --role developer --format grafana
```

**Flags/Parameters:**

| Flag | Short | Required | Description |
|------|-------|----------|-------------|
| `--input` | `-i` | No* | Input service definition JSON file |
| `--output` | `-o` | No | Output dashboard specification file (defaults to `{service_name}_dashboard.json`) |
| `--service-type` | -- | No* | Service type: `api`, `web`, `database`, `queue`, `batch`, `ml` |
| `--name` | -- | No* | Service name |
| `--criticality` | -- | No | Service criticality level: `critical`, `high`, `medium` (default), `low` |
| `--role` | -- | No | Target role for dashboard optimization: `sre` (default), `developer`, `executive`, `ops` |
| `--format` | -- | No | Output format: `json` (default), `grafana` |
| `--doc-output` | -- | No | Generate documentation file at specified path |
| `--summary-only` | -- | No | Only display summary, do not save files |

*Either `--input` or both `--service-type` and `--name` are required.

**Example:**
```bash
python dashboard_generator.py --service-type database --name "orders-db" --criticality high --role sre --format grafana --output orders_db_dashboard.json
```

**Output Formats:** JSON specification or Grafana-compatible JSON containing `metadata`, `configuration`, `layout`, `panels` (with Prometheus query expressions, visualization types, grid positions), `variables`, `alerts_integration`, and `drill_down_paths`. Optionally generates a Markdown documentation file via `--doc-output`.
