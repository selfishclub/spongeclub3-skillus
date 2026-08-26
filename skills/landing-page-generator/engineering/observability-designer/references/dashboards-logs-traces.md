# Dashboards, Logs, Traces & a Worked Example

Read this when building dashboards, defining structured logs, choosing trace sampling, authoring runbooks, or you want a complete worked observability spec plus cost-optimization guidance.

## Dashboard Design Rules

- **Hierarchy**: Overview (all services) > Service (one service) > Component (e.g., database) > Instance
- **Panel limit**: Maximum 7 panels per screen to manage cognitive load
- **Reference lines**: Always show SLO targets and capacity thresholds
- **Time defaults**: 4 hours for incident investigation, 7 days for trend analysis
- **Role-based views**: SRE (operational), Developer (debug), Executive (reliability summary)

## Structured Log Format

```json
{
  "timestamp": "2025-11-05T14:30:00Z",
  "level": "ERROR",
  "service": "payment-api",
  "trace_id": "abc123def456",
  "span_id": "789ghi",
  "message": "Payment processing failed",
  "error_code": "PAYMENT_TIMEOUT",
  "duration_ms": 5023,
  "customer_id": "cust_42",
  "environment": "production"
}
```

**Log levels**: DEBUG (local dev only), INFO (request lifecycle), WARN (degraded but functional), ERROR (failed operation), FATAL (service cannot continue).

## Trace Sampling Strategies

| Strategy | When to Use | Trade-off |
|----------|------------|-----------|
| Head-based (10%) | Development, low-traffic services | Misses rare errors |
| Tail-based | Production, high-traffic | Captures errors/slow requests; higher resource cost |
| Adaptive | Variable traffic patterns | Adjusts rate based on load; more complex to configure |

## Runbook Template

```markdown
# Alert: [Alert Name]

## What It Means
[One sentence explaining the alert condition]

## Impact
[User-facing vs internal; affected services]

## Investigation Steps
1. Check dashboard: [link]  (1 min)
2. Review recent deploys: [link]  (2 min)
3. Check dependent services: [list]  (2 min)
4. Review logs: [query]  (3 min)

## Resolution Actions
- If [condition A]: [action]
- If [condition B]: [action]
- If unclear: Escalate to [team] via [channel]

## Post-Incident
- [ ] Update incident timeline
- [ ] File post-mortem if > 5 min user impact
```

## Example: E-Commerce Payment Service Observability

```yaml
service: payment-api
tier: T1 (revenue-critical)
owner: payments-team

slis:
  availability:
    metric: "1 - rate(http_5xx) / rate(http_total)"
    slo: 99.95%
    error_budget: 21.6 min/month
  latency_p99:
    metric: "histogram_quantile(0.99, http_duration_seconds)"
    slo: < 800ms
  error_rate:
    metric: "rate(payment_failures) / rate(payment_attempts)"
    slo: < 0.5%

alerts:
  - name: PaymentHighErrorRate
    expr: "rate(payment_failures[5m]) / rate(payment_attempts[5m]) > 0.01"
    for: 2m
    severity: critical
    runbook: "https://wiki.internal/runbooks/payment-errors"

dashboard_panels:
  - Payment success rate (gauge)
  - Transaction volume (time series)
  - P50/P95/P99 latency (time series)
  - Error breakdown by type (stacked bar)
  - Downstream dependency health (status map)
  - Error budget remaining (gauge)
```

## Cost Optimization

- **Metric retention**: 15-day full resolution, 90-day downsampled, 1-year aggregated
- **Log sampling**: Sample DEBUG/INFO at 10% in high-throughput services; always keep ERROR/FATAL at 100%
- **Trace sampling**: Tail-based sampling retains only errors and slow requests (> P99)
- **Cardinality management**: Alert on any metric with > 10K unique label combinations
