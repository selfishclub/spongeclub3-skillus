# GCP Cost Optimization

Reference catalog of cost levers for GCP workloads: per-service optimization patterns, detection heuristics, and a prioritization rubric. Pairs with `scripts/gcp_cost_estimator.py` for quantification.

---

## Cost optimization framework

Three stages: **detect** (find waste), **prioritize** (biggest ROI first), **act** (implement).

### Detect — common waste signals

| Signal | Where to look | Likely waste |
|--------|---------------|--------------|
| Resources tagged `env: dev` running 24×7 | Billing reports / labels | Schedule shutdown: 65-70% savings |
| Static external IPs not attached | Compute API / Asset Inventory | Each costs $3-7/mo; orphans common |
| Snapshots > 90 days old | Compute API | Likely forgotten; verify, delete |
| Idle persistent disks | Compute API | Orphaned; delete |
| BigQuery on-demand > $5k/mo | Billing reports | Switch to Editions slots |
| GKE Standard with < 30% utilization | GKE metrics | Switch to Autopilot or right-size |
| Cloud SQL with < 30% CPU 30 days | Cloud SQL metrics | Right-size or use serverless tier |
| Cloud Logging > 500 GB/mo | Logging usage | Filter at source; sink long-term to BQ |
| Memorystore with low memory utilization | Memorystore metrics | Right-size tier |
| Cloud Functions calls scaling unexpectedly | Functions metrics + billing | Audit for runaway loops |
| Egress > 30% of bill | Billing reports | Cloud CDN; private peering |

### Prioritize

80/20 rule: 20% of resources are typically 80% of spend. Identify top 20 cost lines from Billing → optimize those first.

ROI per item = `monthly_savings × (1 - effort_score)`. Pick highest-ROI first.

---

## Compute optimization

### Right-sizing VMs

**Detection:** Cloud Recommender → Right-Sizing recommendations. Or query Monitoring for CPU < 25% over 30 days.

**Action:** Step down machine type. Don't size for peak; autoscale handles bursts. **Savings: 30-50% per right-sized VM.**

### Sustained Use Discounts (SUDs)

**Free automatic discount** for VMs running > 25% of the month. No commitment required.

- 0-25% usage: full price
- 25-50%: small discount
- 50-75%: medium discount
- 75-100%: up to 30% off

This applies to N1, N2, N2D, etc. Built-in; nothing to configure.

### Committed Use Discounts (CUDs)

**Two flavors:**
- **Resource-based CUDs** — commit to specific machine type + region; up to 70% off (3yr)
- **Spend-based CUDs** — commit to monthly spend on a service; more flexible; ~25-40% off

**When to buy:**
- Workload runs > 6 months at predictable size
- Can commit 1 or 3 years

### Preemptible / Spot VMs

**Savings:** up to 91% off normal price.

**When:**
- Batch jobs that can checkpoint
- CI runners
- Stateless web with on-demand baseline
- Fault-tolerant work (Dataflow autoscaling, Spark on Dataproc)

**Constraints:** Can be evicted with 30-second warning; max 24-hour lifetime; not for stateful.

### GKE Autopilot vs Standard

**Autopilot:**
- Per-pod billing (you pay for what pods request)
- Google manages nodes (lower ops)
- Often cheaper for sparse / variable workloads

**Standard:**
- Per-node billing (you pay for nodes whether full or not)
- Full control of node config (special hardware, sidecars)
- Often cheaper for dense workloads at consistent high utilization

**Tip:** Profile your actual utilization. If sustained pod-density is > 70%, Standard often wins; below that, Autopilot.

### Cloud Run cost levers

- **Min-instances** — avoid cold-start cost but pay for idle instances
- **CPU always-allocated** — for background work; costs more but enables Pub/Sub processing
- **Concurrency** — set high concurrency (default 80) so you don't spin up many instances for parallel requests

### Shut-down schedules for non-prod

**Detection:** Dev/test/QA resources running 24/7

**Action:** Cloud Scheduler + Cloud Functions to stop/start VMs and Cloud SQL instances outside business hours. **Savings: ~65%.**

---

## Storage optimization

### Cloud Storage class tiering

| Class | Min retention | Storage cost reduction | Access cost |
|-------|--------------|------------------------|-------------|
| Standard | None | — | Lowest |
| Nearline | 30 days | ~50% off | Higher |
| Coldline | 90 days | ~80% off | Higher still |
| Archive | 365 days | ~95% off | Highest |

**Lifecycle Policies** auto-tier objects based on age, version, or storage class. Configure once; save continuously.

### Persistent Disks

| Type | Use |
|------|-----|
| pd-balanced | Most workloads (SSD perf, lower cost than pd-ssd) |
| pd-ssd | High-IOPS DBs |
| pd-standard | Truly cold; backup disks; very large + sequential |
| pd-extreme | Extreme IOPS (rare; specialized) |
| hyperdisk-balanced / extreme | Newer; for very high throughput; configurable IOPS / throughput |

**Common waste:** pd-ssd for VMs that don't need it. Switch to pd-balanced.

### Snapshot management

Snapshots are **incremental**. First snapshot is full size of used data; subsequent only deltas.

**Cleanup:** Snapshot schedule with retention policy (e.g., daily for 7 days, weekly for 4 weeks, monthly for 12). Delete one-off manual snapshots that piled up.

---

## Database optimization

### Cloud SQL tier choice

**Enterprise vs Enterprise Plus:**
- Plus adds data cache (faster reads), near-zero downtime maintenance, longer logs retention
- Plus costs more; worth it for hot reads + maintenance window constraints

**Right-size machine type:** Cloud SQL Recommender suggests right-sizing.

**Read replicas** for read scale-out — each replica is a billed instance.

**Serverless?** Cloud SQL doesn't have a serverless mode; for true serverless OLTP at small scale, Spanner has a low-cost option but it's different ergonomics.

### Spanner cost levers

**Pricing:** node-hours OR processing units (PUs). Storage separate. Backups separate.

**Right-size nodes/PUs:** Spanner metrics show CPU per node. If sustained < 50%, downsize.

**Multi-region** — true active-active, expensive. Use only when you need it.

**Granular backups:** Don't backup more often than needed; backups have a cost.

### BigQuery cost levers

**Biggest lever: query design.**
- `SELECT *` scans everything; lifecycle: ban it in code review
- Partition tables (by date) for scan reduction
- Cluster tables on filter columns
- Materialized views for repeated aggregations
- BI Engine for dashboard acceleration (faster + cheaper at scale)

**Pricing model:**
- **On-demand**: $5/TB scanned (typical, varies by region) — simple
- **Editions** (Standard/Enterprise/Enterprise Plus): commit to slot-hours; predictable cost
- **Switch from on-demand to Editions when** sustained > $5k/mo on-demand

**Cache:** BigQuery automatically caches query results for 24h — repeat queries are free.

**Storage:**
- Active storage: full price
- Long-term storage: 50% off after 90 days no modification
- Archive: cheaper still (preview tier)

---

## Networking optimization

### Egress

Bandwidth out of Google's network is the #1 hidden cost.

**Reduce egress:**
- **Cloud CDN** — caches at edge; ~$0.02/GB for cached content vs $0.12/GB for typical internet egress
- **Standard tier networking** — exits at nearest border (cheaper than Premium which uses Google's backbone end-to-end)
- **Compression** on responses
- **Avoid cross-region** when possible

### Premium vs Standard network tier

- **Premium** — default; uses Google's backbone to nearest user; better latency, more expensive
- **Standard** — exits at the nearest Google edge; user reaches over public internet to the GCP region; cheaper but variable performance

For latency-sensitive global apps: Premium. For cost-sensitive regional apps: Standard.

### NAT Gateway

Cloud NAT is cheaper than per-VM external IPs for outbound. Charged per-VM-hour + per-GB processed.

---

## Logging & monitoring optimization

### Cloud Logging

**Big cost lever.** Default behavior can balloon spend.

**Strategies:**
- **Filter at source** — exclusion filters to drop verbose debug logs before ingestion
- **Log retention per bucket** — default 30d; tier per log type (audit 1-2yr, app 30-90d)
- **Sink long-term logs to BigQuery** — storage in BQ is much cheaper than Logging long-term storage
- **Use log buckets to scope** retention separately per log type
- **Log routing to Pub/Sub** for real-time downstream (analytics, SIEM)

**Free tier:** 50 GB/mo per project. Above that: $0.50/GB ingested.

### Cloud Monitoring

Custom metrics cost: tiered (some free, then per-month per-metric).

**Optimize:**
- Don't emit metrics for unused dimensions (every label combination = a separate timeseries)
- Use SLOs sparingly (each SLO has small cost)

### Cloud Trace + Profiler

Generally low cost; default enabled is fine.

---

## Common per-workload cost recipes

### Cost recipe: Modest web app

- Cloud Run (default + min-instances 1): $25/mo light traffic
- Cloud SQL Enterprise Postgres 2vCore HA: ~$200/mo
- Cloud Storage Standard 100GB: $2/mo
- Cloud Logging (light): ~$20/mo
- Cloud Monitoring: free tier
- Egress (modest): $30/mo

**Total:** ~$280/mo

### Cost recipe: SaaS multi-tenant

- GKE Autopilot for app: ~$1500/mo (200 pods worth of resources)
- Spanner regional Standard 1 node: $720/mo
- Memorystore Standard M2: $150/mo
- Global LB + Cloud Armor Plus: $200/mo
- Cloud Logging 100 GB/day: $1500/mo (with filtering tuned)
- Cloud Monitoring + SLOs: $200/mo
- BigQuery Editions Enterprise (100 slots): $4000/mo

**Total:** ~$8300/mo (without volume discounts; CUDs and committed slots would reduce 25-40%)

### Cost recipe: Data pipeline

- Cloud Storage Standard (active) + Coldline (archive): cheap once tiered
- Dataflow (autoscaling): pay per vCPU-hour during pipeline runs
- BigQuery (scan-based on-demand if intermittent; slots if continuous)
- Pub/Sub: cheap per-message
- Composer (managed Airflow): ~$300/mo for small env

---

## Anti-patterns specific to cost

### "Premium because it's safer"

Premium tiers are about features (HA, multi-region, faster perf). Not safer generically. If you don't need the features, you're paying for nothing.

### "We'll scale up if we need to"

Pre-provisioning for hypothetical peak. Right-size for actual + autoscale for bursts.

### "It's only $50/month"

$50 × 100 forgotten resources = $5000/mo. Compound interest of waste.

### "We'll review costs quarterly"

Costs drift in days. Set budgets with alerts. Review monthly minimum; top 20 cost lines weekly during growth.

### "CUDs are scary"

1-year CUDs for stable baseline are nearly free money. Risk = overcommit; mitigate by starting with 50-70% coverage and growing.

### "BigQuery on-demand is fine"

Until it isn't. At $5k+/mo, switch to Editions slots. Often 30-50% cheaper at that scale.

### "Cloud Logging at default is fine"

Until you ingest 1TB/day in error logs. Filter at source; sink to BQ for long-term.

---

## Detection script outputs

`scripts/gcp_cost_estimator.py` takes a workload spec YAML and produces:

```
Service breakdown:
  GKE Autopilot (200 pods):           $1,500/mo
  Cloud SQL Enterprise+HA (4vCore):   $580/mo
  Spanner regional (1 node):          $720/mo
  Cloud Storage 1TB Standard:         $20/mo
  Cloud Logging (filtered, 30GB/day): $450/mo
  Global LB + Cloud Armor:            $250/mo
  Cloud CDN:                          $100/mo (cached traffic at lower rate)
  Egress (after CDN):                 $200/mo
  -----
  TOTAL:                              $3,820/mo

Optimization opportunities:
  [HIGH] Cloud SQL: 3-yr CUD eligible — save ~$200/mo
  [MED]  Spanner: enterprise tier needed? Standard may suffice — save ~$250/mo
  [LOW]  Storage: lifecycle Nearline after 30 days — save ~$10/mo

  Total potential savings: ~$460/mo (~12%)
```

---

## Cheat sheet

| Question | Answer |
|----------|--------|
| Where's most of my spend? | Billing → Reports → Cost by SKU or service |
| What's growing fastest? | Billing → Trends + filter by service |
| What's idle/orphaned? | Cloud Asset Inventory + Recommender |
| What can I commit to? | Recommender → CUD recommendations |
| Should I switch BigQuery to Editions? | If sustained > $5k/mo on-demand: yes |
| When to rearchitect for cost? | When right-sizing + CUD potential exhausted |
