# Azure Cost Optimization

Reference catalog of cost levers for Azure workloads: per-service optimization patterns, detection heuristics, and a prioritization rubric. Pairs with `scripts/azure_cost_estimator.py` for quantification.

---

## Cost optimization framework

Three stages: **detect** (find waste), **prioritize** (biggest ROI first), **act** (implement).

### Detect — common waste signals

| Signal | Where to look | Likely waste |
|--------|---------------|--------------|
| Resources tagged `env: dev` running 24×7 | Cost Management / tags | Schedule shutdown outside business hours: 65-70% savings |
| Resources with no tags | Resource Graph | Untracked, likely orphaned |
| Snapshots > 90 days old | Resource Graph | Likely forgotten; verify, delete |
| Unattached managed disks | Resource Graph | Orphaned; delete |
| Standby (allocated, deallocated) VMs | Resource Graph | Bill stops only when deallocated, not "stopped" |
| Public IPs not attached | Resource Graph | Bill for IP regardless of attachment |
| Load Balancers with 0 rules | Resource Graph | Forgotten infra |
| Cosmos DB collections at autoscale ceiling | Cosmos metrics | Right-size ceiling down |
| App Service plans at < 30% CPU 30 days | App Service plan metrics | Right-size SKU |
| SQL DB at 5% DTU for a month | SQL DB metrics | Switch tier or serverless |
| Storage in Hot tier, last accessed > 30 days | Lifecycle Management report | Move to Cool/Cold |
| Log Analytics workspace > 100GB/day | Workspace usage report | Filter at source; tier per table |
| Backup retention 730 days for all data | Backup vault config | Tier per workload |

### Prioritize

Use the **80/20 rule** — usually 20% of resources account for 80% of cost. Identify the top 20 cost lines from Cost Management. Optimize those first.

Per-resource ROI = `monthly_savings × (1 - effort_score)`

| Effort | Score | Examples |
|--------|-------|----------|
| Trivial | 0.1 | Delete orphaned disk, set lifecycle policy |
| Low | 0.3 | Buy Reserved Instance, downsize SKU |
| Medium | 0.5 | Add autoscaling, migrate to serverless |
| High | 0.8 | Re-architect for caching, switch regions |
| Massive | 0.95 | Full cloud migration, re-platform |

Pick the highest-ROI items first; do them.

### Act — the optimization patterns

---

## Compute optimization

### Right-sizing VMs

**Detection:** Average CPU < 25% over 30 days; or memory < 50%.

**Action:**
- Use Azure Advisor recommendations (built-in right-size suggestions)
- Step down one SKU at a time; verify performance
- Don't downsize for headroom of peak — that's what autoscale is for

**Savings:** Typically 30-50% per right-sized VM.

### Reserved Instances / Savings Plans

**When to buy:**
- Workload has been running > 6 months at predictable size
- You can commit to 1 or 3 years
- Specific VM SKU + region (RI) OR any compute (Savings Plan)

**RIs vs Savings Plans:**
- **RI** — locks specific VM SKU + region; up to 72% (3yr) savings
- **Savings Plan** — flexible across SKUs and regions; up to 65% (3yr); easier to evolve

**Don't buy RIs for:**
- Unstable workloads (might not need them in 1 year)
- Workloads you might modernize (RIs don't apply to serverless / Functions Consumption)

### Spot / Low-Priority VMs

**When:**
- Batch jobs that can checkpoint and restart
- CI runners
- Dev/test fleets
- Stateless web frontends (paired with on-demand baseline)

**Savings:** Up to 90% off list price.

**Constraints:** Can be evicted with 30-second warning; not for stateful workloads.

### Autoscaling

**Without autoscale:** Provisioned for peak; pay for idle most of the time.
**With autoscale:** Match capacity to load; 20-40% savings typical.

**Configure on:**
- VMSS (scale-out / scale-in rules)
- AKS (Cluster Autoscaler + KEDA / HPA)
- App Service Premium (auto-scale settings)
- Functions Premium (pre-warmed instances + max burst)
- Cosmos DB autoscale throughput
- SQL DB serverless tier

**Avoid:** Scale rules so aggressive they thrash (scale-out → cost spike → scale-in → cold-cache → latency → scale-out again).

### Shut-down schedules for non-prod

**Detection:** Dev/test/QA resources running 24×7.

**Action:** Azure Automation runbooks, DevTest Labs auto-shutdown, or built-in VM auto-shutdown for VMs. Default: shut down 7pm–7am weekdays + all weekend.

**Savings:** ~65% if used in business hours only.

---

## Storage optimization

### Storage tiering

**Tiers** (Blob storage):

| Tier | Access cost | Storage cost | Min retention |
|------|-------------|--------------|---------------|
| Hot | Lowest | Highest | None |
| Cool | Higher | ~50% of Hot | 30 days |
| Cold | Higher | ~80% off Hot | 90 days |
| Archive | Very high (hours) | ~95% off Hot | 180 days |

**Heuristic:**
- Hot — accessed in last 30 days
- Cool — accessed in last 30-90 days
- Cold — accessed in last 90-180 days
- Archive — long-term retention (compliance, legal)

**Lifecycle Management** policies automate this. Set once; saves continuously.

### Disk tier

**Managed Disks:**

| Tier | When |
|------|------|
| Standard HDD | Truly cold; OS disks for dev VMs |
| Standard SSD | Most production OS disks; light data disks |
| Premium SSD | Production databases, high-IOPS workloads |
| Premium SSD v2 | Like Premium but cheaper for moderate IOPS (configurable) |
| Ultra Disk | Extreme IOPS / throughput (rare; SAP, large Oracle) |

**Common mistake:** Premium SSD for every disk; Standard SSD is enough for most non-DB workloads.

### Reserved Capacity for Storage

For predictable storage volume (multi-TB), 1-yr or 3-yr reservations save 25-38%.

---

## Database optimization

### SQL DB tier choice

**General Purpose** vs **Business Critical**:
- BC has local SSD (lower latency), in-memory OLTP, 99.995% SLA
- BC costs ~2.5× GP for same vCore
- BC only when you need its specific features

**Hyperscale**:
- For large DBs (> 4TB)
- Pay for compute + actually-used storage
- Often cheaper than equivalent GP at scale

**Serverless (Single DB only)**:
- Compute scales to zero after idle period
- Pay for memory + compute-second
- Right for spiky/idle workloads (dev, low-traffic prod)

### DTU vs vCore

DTU is older, bundled model. vCore is newer, more flexible, supports Hybrid Benefit (reuse on-prem SQL licenses for 30-55% discount).

**Migrate from DTU to vCore** for flexibility.

### Cosmos DB optimization

**Throughput model:**

| Model | When |
|-------|------|
| Manual provisioned RU/s | Stable predictable load |
| Autoscale (10%-100% of max) | Variable; pays for max(consumed, 10% of ceiling) |
| Serverless (max 1TB, max 5000 RU/s) | Low / spiky |

**Cost levers:**
- **Tune partition key** to avoid hot partitions (throttling + paying for unused capacity)
- **Opt out of indexing** for fields not queried (reduces RU + storage)
- **Use point reads** (1 RU) over queries (many RUs)
- **Set TTL** to auto-expire old data (lowers storage)
- **Use change feed** for downstream pipelines (cheap; included)

### PostgreSQL / MySQL Flexible Server

- **Burstable tier** for low-traffic apps
- **Right-size storage** — storage cost dominates for small DBs
- **Read replicas** for read scale-out (each replica is a separate billed instance)
- **Reserve capacity** for predictable workloads

---

## Networking optimization

### Egress

Bandwidth out of Azure is the #1 hidden cost driver.

**Reduce egress:**
- **CDN** (Azure CDN, Front Door) — caches at edge
- **Inter-region replication via paired regions** is sometimes discounted
- **Private peering** for on-prem traffic (ExpressRoute) — cheaper than public internet bandwidth
- **Compression** on responses (gzip / brotli)
- **API design** that doesn't overfetch

### NAT Gateway vs Public IP

NAT Gateway is cheaper than Public IPs for outbound from VNet at scale. Replaces unpredictable SNAT port exhaustion with deterministic gateway capacity.

### Front Door vs Application Gateway

- **Front Door** — global edge, includes CDN, caching, WAF
- **App Gateway** — regional, no caching, WAF inside VNet

If you need both edge caching AND regional WAF, use Front Door → App Gateway → backend.

---

## Observability cost optimization

### Log Analytics workspaces

**Big cost lever.** Default settings can balloon spend quickly.

**Per-table commitment tier (Basic Logs):**
- Some tables (e.g., container stdout) can be moved to "Basic Logs" pricing — 25× cheaper to ingest, but limited querying
- Useful for high-volume, low-query data

**Retention tiering:**
- Default 30 days free; paid up to 730 days
- **Tier by table:**
  - Audit / signin logs — 1-2 years (compliance)
  - App logs — 30-90 days
  - Container stdout — 7-30 days
  - Custom metrics — 1 year (often needed for capacity planning)
- **Archive tier** beyond hot retention is cheaper for cold data

**Commitment tiers:**
- Pay-As-You-Go: $2.30/GB
- 100 GB/day: $1.96/GB (15% off)
- 200 GB/day: $1.84/GB (20% off)
- 500 GB/day: $1.61/GB (30% off)
- 1000+ GB/day: bigger discounts

Buy commitment tier as soon as you're above the next threshold.

### Application Insights

**Sampling:**
- Adaptive (default) — auto-adjusts; usually fine
- Fixed rate — for predictable cost; tune per environment (100% in dev, 5-20% in prod)

**Data caps:** Set daily cap to prevent runaway costs from accidental log explosion.

---

## Common per-workload cost recipes

### Cost recipe: Modest web app

- App Service Premium v3 P1v3 (reserved 1-yr): $130/mo (instead of $186 PAYG)
- Azure SQL DB GP Gen5 4 vCore reserved 1-yr: $580/mo (instead of $830 PAYG)
- Storage Account Standard GPv2 Hot (1TB): $20/mo
- Application Insights: included with App Service plan + small data ingestion
- Log Analytics PAYG: ~$30/mo (light usage)

**Total:** ~$760/mo. Without reservations: ~$1066/mo. Savings: ~30%.

### Cost recipe: SaaS multi-tenant

- AKS Standard with 5× D4s_v5 worker nodes (3yr RI): savings 60% off list
- Cosmos DB autoscale max 10,000 RU/s: charged for max(used, 1000 RU/s)
- Azure Cache for Redis Standard C1: $80/mo
- Front Door Premium: $330/mo
- Log Analytics 100 GB/day commitment: $5,880/mo (vs PAYG $6,900)

### Cost recipe: Batch / data pipeline

- Container Apps Jobs (consumption): pays per execution
- Spot VMs in VMSS for compute-heavy stages: 80% off
- Storage with lifecycle to Archive: 95% off after 90 days
- Synapse Serverless: pay per TB scanned (cheap for query-on-demand)

---

## Anti-patterns specific to cost

### "Premium because it's safer"

Premium tiers are about features (VNet, in-memory, faster scale). They're not "safer" generically. If you don't need the features, you're paying for nothing.

### "We'll scale up if we need to"

Pre-provisioning for hypothetical peak you don't yet have. Right-size for actual load + autoscale for bursts.

### "It's only $50/month, who cares"

$50 × 100 forgotten resources = $5000/month. Compound interest of waste. Tag everything; cost-allocate; review regularly.

### "We'll review costs quarterly"

Costs drift in days, not quarters. Set budgets with alerts. Review monthly at minimum. Top 20 cost lines weekly during growth.

### "Reserved Instances are scary"

1-year RIs for clearly-stable workloads are nearly free money. The risk is overcommitting; mitigate by starting with conservative coverage (50-70%) and scaling commitment as you learn.

### "We need real-time logs for everything"

Real-time hot logs are expensive. Most teams can do: real-time alerts on a small set of critical metrics; everything else in cheaper tiers (archive, basic logs).

---

## Detection script outputs

`scripts/azure_cost_estimator.py` takes a workload spec YAML and produces:

```
Service breakdown:
  AKS (Standard SLA + 3× D4s_v5):     $1,240/mo
  Azure SQL DB (BC Gen5 4vCore):       $1,830/mo
  Cosmos DB (autoscale 5000 RU/s):     $290/mo
  Storage (1TB Hot):                   $20/mo
  Log Analytics (50 GB/day):           $3,450/mo
  Front Door Premium:                  $330/mo
  Other (NAT GW, Public IP, etc.):     $200/mo
  -----
  TOTAL:                               $7,360/mo

Optimization opportunities:
  [HIGH] Log Analytics: 50 GB/day eligible for commitment tier — save ~$520/mo
  [MED]  AKS nodes: 3yr RI eligible — save ~$745/mo
  [LOW]  Cosmos: opt out of unused field indexing — save ~$50/mo

  Total potential savings: $1,315/mo (~18%)
```

---

## Cheat sheet

| Question | Answer |
|----------|--------|
| Where's most of my spend? | Cost Management → "Cost by service" filter |
| What's growing fastest? | Cost Management → "Cost trends" + filters |
| What's idle/orphaned? | Azure Advisor + Resource Graph queries |
| What can I reserve? | Azure Advisor → Reservation recommendations |
| Should I buy a commitment? | If consistent monthly spend > 6 months: yes |
| When to rearchitect for cost? | When right-sizing/reservation potential is exhausted |
