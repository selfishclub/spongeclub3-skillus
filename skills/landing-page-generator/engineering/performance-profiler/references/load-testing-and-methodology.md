# Load Testing and Methodology

Read this when writing k6 load tests, documenting a before/after optimization, running the quick-win checklist, or you need the pitfalls / best-practices / troubleshooting / success-criteria reference.

## Load Testing with k6

```javascript
// load-test.k6.js
import http from 'k6/http'
import { check, sleep } from 'k6'
import { Trend, Rate } from 'k6/metrics'

const apiLatency = new Trend('api_latency')
const errorRate = new Rate('errors')

export const options = {
  stages: [
    { duration: '1m', target: 20 },    // ramp up
    { duration: '3m', target: 100 },   // sustain
    { duration: '1m', target: 0 },     // ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200', 'p(99)<500'],
    errors: ['rate<0.01'],
    api_latency: ['p(95)<150'],
  },
}

export default function () {
  const res = http.get(`${__ENV.BASE_URL}/api/v1/projects?limit=20`, {
    headers: { Authorization: `Bearer ${__ENV.TOKEN}` },
  })

  apiLatency.add(res.timings.duration)
  check(res, {
    'status 200': (r) => r.status === 200,
    'body has data': (r) => JSON.parse(r.body).data !== undefined,
  }) || errorRate.add(1)

  sleep(1)
}
```

```bash
# Run locally
k6 run load-test.k6.js -e BASE_URL=http://localhost:3000 -e TOKEN=$TOKEN

# Run with cloud reporting
k6 cloud load-test.k6.js
```

## Before/After Measurement Template

```markdown
## Performance Optimization: [What You Fixed]

**Date:** YYYY-MM-DD
**Ticket:** PROJ-123

### Problem
[1-2 sentences: what was slow, how it was observed]

### Root Cause
[What the profiler revealed — include flamegraph link or screenshot]

### Baseline (Before)
| Metric | Value |
|--------|-------|
| P50 latency | XXms |
| P95 latency | XXms |
| P99 latency | XXms |
| Throughput (RPS) | XX |
| DB queries/request | XX |
| Bundle size | XXkB |

### Fix Applied
[Brief description + link to PR]

### After
| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| P50 | XXms | XXms | -XX% |
| P95 | XXms | XXms | -XX% |
| P99 | XXms | XXms | -XX% |
| RPS | XX | XX | +XX% |
| DB queries/req | XX | XX | -XX% |

### Verification
[Link to k6 output, CI run, or monitoring dashboard]
```

## Quick-Win Optimization Checklist

```
DATABASE
[ ] Missing indexes on WHERE/ORDER BY columns
[ ] N+1 queries (check query count per request)
[ ] SELECT * when only 2-3 columns needed
[ ] No LIMIT on unbounded queries
[ ] Missing connection pool (new connection per request)
[ ] Stale statistics (run ANALYZE on busy tables)

NODE.JS
[ ] Sync I/O (fs.readFileSync) in request handlers
[ ] JSON.parse/stringify of large objects in hot loops
[ ] Missing response compression (gzip/brotli)
[ ] Dependencies loaded inside request handlers (move to module level)
[ ] Sequential awaits that could be Promise.all

BUNDLE
[ ] Full lodash/moment import instead of specific functions
[ ] Static imports of heavy components (use dynamic import)
[ ] Images not optimized / not using next/image
[ ] No code splitting on routes

API
[ ] No pagination on list endpoints
[ ] No Cache-Control headers on stable responses
[ ] Serial fetches that could run in parallel
[ ] Fetching related data in loops instead of JOINs
```

## Common Pitfalls

- **Optimizing without measuring** — you will optimize the wrong thing
- **Testing with development data** — 10 rows in dev vs millions in prod reveals different bottlenecks
- **Ignoring P99** — P50 can look fine while P99 is catastrophic for some users
- **Premature optimization** — fix correctness first, then measure and optimize
- **Not re-measuring after the fix** — always verify the fix actually improved the metrics
- **Load testing production** — use staging with production-sized data volumes instead

## Best Practices

1. **Baseline first, always** — record P50/P95/P99, RPS, and error rate before touching anything
2. **One change at a time** — isolate the variable to confirm causation, not correlation
3. **Profile with realistic data volumes** — performance characteristics change dramatically with scale
4. **Set performance budgets** — `p(95) < 200ms` as a CI gate with k6
5. **Monitor continuously** — add Datadog/Prometheus/Grafana metrics for key code paths
6. **Cache aggressively, invalidate precisely** — cache is the fastest optimization but hardest to debug
7. **Document the win** — before/after in the PR description motivates the team and creates institutional knowledge

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Flamegraph shows only `(idle)` frames | Profiling during low-load period; no meaningful CPU work captured | Apply realistic load with autocannon or k6 during profiling, target the specific endpoint under investigation |
| Heap snapshot comparison shows no growth but memory still climbs | Native memory leak outside V8 heap (e.g., native addon, file descriptor leak) | Use `process.memoryUsage().rss` tracking alongside heap snapshots; profile with Valgrind or `memray` for native allocations |
| `EXPLAIN ANALYZE` shows Index Scan but query is still slow | Index exists but is not selective enough, or query returns too many rows for index to help | Check index selectivity with `SELECT count(DISTINCT col)/count(*) FROM table`; consider composite index or partial index |
| k6 load test passes locally but fails in CI | CI runner has limited CPU/memory; network latency differs from local | Run k6 against a dedicated staging environment, not localhost in CI; adjust thresholds for CI-specific baselines |
| Bundle analyzer shows expected size but app still loads slowly | Large bundle is code-split but critical path has render-blocking resources | Audit the critical rendering path separately with Lighthouse; check for synchronous scripts and unoptimized images |
| `py-spy` cannot attach to running process | Insufficient permissions or SIP (System Integrity Protection) on macOS | Run with `sudo py-spy record --pid <PID>`; on macOS, disable SIP or use `--subprocesses` flag with a fresh process |
| N+1 detection middleware reports false positives | Legitimate batch operations trigger high query counts per request | Add endpoint-level allowlists to the detection middleware; distinguish between N+1 patterns and intentional batch queries by checking for repeated identical query templates |

## Success Criteria

- **Baseline coverage:** Every optimization PR includes documented before/after metrics with P50, P95, and P99 latency values
- **Latency targets met:** P95 API response time stays below 200ms and P99 below 500ms as validated by k6 threshold checks in CI
- **Memory stability:** No heap growth exceeding 10% over a 24-hour soak test under sustained load
- **Bundle budget enforced:** JavaScript bundle size for initial page load remains under 200kB gzipped, verified by CI gate
- **N+1 elimination:** Query count per API request stays below 10 for all critical endpoints, validated by request-level query logging
- **Load test confidence:** Staging load tests demonstrate the system handles 2x expected peak traffic with error rate below 1%
- **Regression detection:** Performance regressions are caught within one CI cycle, not discovered in production monitoring
