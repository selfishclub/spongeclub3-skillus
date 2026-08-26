# SLO Framework & Alerting Design

Read this when designing the observability strategy itself: the end-to-end workflow, SLI/SLO definitions, error-budget math, multi-window burn-rate alerts, alert classification, and alert-fatigue prevention.

## Workflow

1. **Catalogue services** -- List every service in scope with its type (request-driven, pipeline, storage), criticality tier (T1-T3), and owning team. Validate that at least one T1 service exists before proceeding.
2. **Define SLIs per service** -- For each service, select SLIs from the Golden Signals table. Map each SLI to a concrete Prometheus/InfluxDB metric expression.
3. **Set SLO targets** -- Assign SLO targets based on criticality tier and user expectations. Calculate the corresponding error budget (e.g., 99.9% = 43.8 min/month).
4. **Design burn-rate alerts** -- Create multi-window burn-rate alert rules for each SLO. Validate that every alert has a clear runbook link and response action.
5. **Build dashboards** -- Generate dashboard specs following the hierarchy: Overview > Service > Component > Instance. Cap each screen at 7 panels. Include SLO target reference lines.
6. **Configure log aggregation** -- Define structured log format, set log levels, assign correlation IDs, and configure retention policies per tier.
7. **Instrument traces** -- Set up distributed tracing with sampling strategy (head-based for dev, tail-based for production). Define span boundaries at service and database call points.
8. **Validate coverage** -- Confirm every T1 service has metrics, logs, and traces. Confirm every alert has a runbook. Confirm dashboard load time is under 2 seconds.

## SLI/SLO Quick Reference

| SLI Type | Metric Expression (Prometheus) | Typical SLO |
|----------|-------------------------------|-------------|
| Availability | `1 - (sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m])))` | 99.9% |
| Latency (P99) | `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))` | < 500ms |
| Error rate | `sum(rate(grpc_server_handled_total{grpc_code!="OK"}[5m])) / sum(rate(grpc_server_handled_total[5m]))` | < 0.1% |
| Throughput | `sum(rate(http_requests_total[5m]))` | > baseline |

## Error Budget Calculation

```
Error Budget = 1 - SLO target

Example (99.9% availability):
  Monthly budget = 30d x 24h x 60m x 0.001 = 43.2 minutes
  If 20 minutes consumed, remaining = 23.2 minutes (53.7% left)
```

## Burn-Rate Alert Design

| Window | Burn Rate | Severity | Budget Consumed |
|--------|-----------|----------|-----------------|
| 5 min / 1 hr | 14.4x | Critical (page) | 2% in 1 hour |
| 30 min / 6 hr | 6x | Warning (ticket) | 5% in 6 hours |
| 2 hr / 3 day | 1x | Info (dashboard) | 10% in 3 days |

**Rule**: Every critical alert must have an actionable runbook. If no clear action exists, downgrade to warning.

## Alert Classification

| Severity | Meaning | Response | Routing |
|----------|---------|----------|---------|
| Critical | Service down or SLO burn rate high | Page on-call immediately | PagerDuty escalation |
| Warning | Approaching threshold, non-user-facing | Create ticket, fix in business hours | Slack channel |
| Info | Deployment notification, capacity trend | Review in next standup | Dashboard only |

## Alert Fatigue Prevention

- **Hysteresis**: Set different thresholds for firing (e.g., > 90% CPU for 5 min) and resolving (e.g., < 80% CPU for 10 min).
- **Suppression**: Suppress dependent alerts during known outages (e.g., suppress pod alerts when node is down).
- **Grouping**: Group related alerts into a single notification (e.g., all pods in one deployment).
- **Precision over recall**: A missed alert that would self-resolve is better than 50 false pages per week.

## Golden Signals

| Signal | What to Monitor | Key Metrics |
|--------|----------------|-------------|
| Latency | Request duration | P50, P95, P99 response time; queue wait; DB query time |
| Traffic | Request volume | RPS with burst detection; active sessions; bandwidth |
| Errors | Failure rate | 4xx/5xx rates; error budget consumption; silent failures |
| Saturation | Resource pressure | CPU/memory/disk utilization; queue depth; connection pool usage |
