# Azure Well-Architected Framework — Assessment Reference

Per-pillar deep dive on the Azure Well-Architected Framework (WAF). For each of the five pillars: 10-question assessment checklist, common findings, severity scoring, and concrete remediation patterns.

Use with `scripts/azure_waf_scorer.py` to automate scoring a workload against this checklist.

---

## Pillar 1: Reliability

**Core question:** Will the workload stay up under expected and unexpected conditions?

### Assessment checklist

| # | Question | Severity if no |
|---|----------|----------------|
| R1 | Is the workload deployed across at least 2 availability zones? | Critical |
| R2 | Is there a documented RPO and RTO matching business requirements? | Critical |
| R3 | Are backups configured with tested restore procedures (not just configured, tested)? | Critical |
| R4 | Is there a documented multi-region DR plan with failover/failback procedures? | Warning (Critical for tier-1) |
| R5 | Are health probes configured for all stateless services? | Warning |
| R6 | Are auto-scaling rules in place for compute? | Warning |
| R7 | Are circuit breakers / retries with backoff implemented for dependency calls? | Warning |
| R8 | Are dependencies (DBs, caches, queues) configured for HA (multi-AZ or zone-redundant)? | Critical |
| R9 | Are PaaS services using zone-redundant tiers where available? | Warning |
| R10 | Has a chaos exercise been run against the workload in the past 6 months? | Info |

### Common findings

#### Finding: Single-AZ deployment

**Severity:** Critical
**Detection:** VMSS / AKS / App Service / SQL DB without zone redundancy enabled
**Fix:** Re-deploy with `zones: [1, 2, 3]` for VMSS/AKS; enable zone redundancy on SQL DB Premium/Business Critical; enable zone-redundant File Shares.

#### Finding: Backups configured but never tested

**Severity:** Critical
**Detection:** Backup vault exists, last restore test missing or > 90 days old
**Fix:** Schedule quarterly restore tests as part of operational cadence. Document restore time and discrepancies.

#### Finding: No documented RPO/RTO

**Severity:** Critical
**Detection:** No published RPO/RTO for the workload; team can't answer "how much data could we lose?" and "how fast can we recover?"
**Fix:** Define RPO/RTO with business stakeholders. Match technology choices (backup frequency, replication mode) to the target.

#### Finding: No multi-region plan for tier-1 workload

**Severity:** Critical (tier-1) / Warning (tier-2)
**Detection:** Single-region deployment for a customer-revenue or compliance-critical workload
**Fix:** Adopt active-passive (Traffic Manager + secondary region cold standby) or active-active (Front Door + read-replicas). Document failover runbook. Test annually.

#### Finding: No retry/circuit-breaker pattern

**Severity:** Warning
**Detection:** Dependency calls in code without retry policy or with naive infinite retry
**Fix:** Use Polly (.NET), tenacity (Python), retry libs with exponential backoff + jitter + max retries. Wire circuit breakers around flaky dependencies.

#### Finding: No autoscaling rules

**Severity:** Warning
**Detection:** Static instance count for variable-traffic workload
**Fix:** Configure autoscale rules (target CPU, memory, queue length, custom metric). Set sensible min/max. Avoid panic-scaling on noisy signals.

### Reliability patterns

| Pattern | When |
|---------|------|
| **Active-active multi-region** | High traffic, low RTO/RPO budget |
| **Active-passive multi-region** | Lower traffic; cheaper standby |
| **Zone-redundant single-region** | Adequate for many workloads; far cheaper than multi-region |
| **Pilot light** | Cold standby in second region with data replicated; spin up on disaster |
| **Backup + restore** | Last resort; longest RTO |

---

## Pillar 2: Security

**Core question:** Can the workload defend against threats, contain breaches, and recover from compromise?

### Assessment checklist

| # | Question | Severity if no |
|---|----------|----------------|
| S1 | Are all PaaS services accessed via Private Endpoint (not public endpoints)? | Critical |
| S2 | Are all secrets stored in Key Vault (not env vars / app settings)? | Critical |
| S3 | Are services using Managed Identity (not shared keys / connection strings)? | Critical |
| S4 | Is Entra ID with MFA enforced for all admin access? | Critical |
| S5 | Is Defender for Cloud enabled (relevant plans)? | Warning |
| S6 | Are diagnostic logs sent to Log Analytics for audit? | Critical |
| S7 | Are RBAC roles assigned at least-privileged scope? | Warning |
| S8 | Are network security groups (NSGs) configured with least-privilege rules? | Warning |
| S9 | Is encryption at rest enabled (default for most PaaS; explicit for VMs)? | Critical |
| S10 | Is TLS 1.2+ enforced; older protocols disabled? | Warning |

### Common findings

#### Finding: Public endpoints on production storage / database

**Severity:** Critical
**Detection:** Storage account / SQL DB / Cosmos DB with public network access enabled
**Fix:** Add Private Endpoint; disable public network access; if dev access needed, allow via specific IP allowlist with bastion.

#### Finding: Secrets in App Settings

**Severity:** Critical
**Detection:** Connection strings, API keys, passwords in App Service / Functions config
**Fix:** Move to Key Vault. Reference from app settings via `@Microsoft.KeyVault(SecretUri=https://...)` syntax. App must have MI with Key Vault role.

#### Finding: Shared keys for service-to-service auth

**Severity:** Critical
**Detection:** Storage account / Cosmos / SB connection strings in use; no MI configured
**Fix:** Enable Managed Identity on the calling service. Grant data-plane RBAC role on the target. Disable shared key access where possible.

#### Finding: No MFA on admin accounts

**Severity:** Critical
**Detection:** Entra ID without Conditional Access policy enforcing MFA on Global Admin / contributor roles
**Fix:** Conditional Access policy: enforce MFA for any admin role, any sensitive app, optionally all users.

#### Finding: Logs not centralized

**Severity:** Critical
**Detection:** Resources don't have diagnostic settings sending to Log Analytics
**Fix:** Enable diagnostic settings on every resource that supports it. Send Audit + Resource logs. Use Azure Policy `DeployIfNotExists` to enforce.

#### Finding: Wide RBAC scope

**Severity:** Warning
**Detection:** Contributor or Owner roles assigned at subscription or management group level for application identities
**Fix:** Re-scope to resource group or resource. Use built-in roles tighter than Contributor (e.g., Storage Blob Data Reader). Custom roles if needed.

#### Finding: NSG with 0.0.0.0/0 inbound

**Severity:** Critical (for management ports) / Warning (for app ports)
**Detection:** NSG rule with source = Any on RDP (3389), SSH (22), or Database port
**Fix:** Restrict source to specific IPs / Azure services. For management, use Bastion or just-in-time access via Defender for Servers.

### Security patterns

| Pattern | When |
|---------|------|
| **Zero Trust** | Never trust, always verify; identity-aware access; explicit auth at each hop |
| **Defense in depth** | Multiple layers: WAF + NSG + service-level auth + data encryption |
| **Just-in-time access** | Time-bound elevated permissions for admins (via PIM / JIT VM access) |
| **Workload Identity Federation** | OIDC federation; no secrets between identity providers |
| **Customer-managed keys (CMK)** | Encryption keys you manage in Key Vault; for compliance requirements |
| **Hub-and-spoke + Azure Firewall** | All egress through firewall; FQDN allowlists; IDPS in Premium |

---

## Pillar 3: Cost Optimization

**Core question:** Is the workload spending only what's needed for the value delivered?

### Assessment checklist

| # | Question | Severity if no |
|---|----------|----------------|
| C1 | Are resources right-sized (SKU matches actual load)? | Warning |
| C2 | Are Reserved Instances / Savings Plans purchased for predictable workloads? | Warning |
| C3 | Is autoscaling enabled for variable workloads? | Warning |
| C4 | Are spot/low-priority instances used for batch / fault-tolerant workloads? | Info |
| C5 | Is storage tiered (Hot/Cool/Cold/Archive) per access pattern? | Warning |
| C6 | Are dev/test environments shut down outside business hours? | Info |
| C7 | Have orphaned resources (unused disks, IPs, snapshots) been cleaned up? | Warning |
| C8 | Are Cosmos DB / SQL DB throughput tiers right-sized? | Warning |
| C9 | Is Log Analytics retention tuned (not default 730 days for everything)? | Warning |
| C10 | Are cost alerts / budgets configured per resource group / subscription? | Critical |

### Common findings

#### Finding: Over-provisioned VMs / App Service plans

**Severity:** Warning
**Detection:** Average CPU < 20% over 30 days
**Fix:** Right-size down to smaller SKU. Don't size for peak burst — autoscale handles that.

#### Finding: No Reserved Instances for predictable workloads

**Severity:** Warning
**Detection:** Workload has been running > 6 months at stable size; no RI / Savings Plan purchased
**Fix:** Purchase 1-year or 3-year RI / Savings Plan for the baseline. 1-year is usually 30-40% savings; 3-year up to 72%.

#### Finding: Premium tier everything

**Severity:** Warning
**Detection:** Premium App Service / Premium Cosmos / Premium SQL when Standard would suffice
**Fix:** Audit by service. Premium pays off when you need the specific premium features (VNet, in-memory OLTP, etc.); not as a "more is better" default.

#### Finding: Orphaned disks

**Severity:** Warning
**Detection:** Managed disks with no VM attached
**Fix:** Snapshot if needed for forensics; delete the disk. Bulk script via Azure Resource Graph.

#### Finding: No cost alerts

**Severity:** Critical
**Detection:** No budget configured on subscription
**Fix:** Set monthly budgets per subscription / resource group; alerts at 50%/80%/100%; email + action group.

#### Finding: Log Analytics retention 730 days for debug logs

**Severity:** Warning
**Detection:** All workspace tables at max retention
**Fix:** Tier per table. Operational metrics: 30-90 days. Audit logs: 1-2 years (per compliance). Application diagnostic logs: 30 days hot, archive beyond.

### Cost-optimization heuristics

| If you see | Try |
|-----------|-----|
| Cosmos DB > $10k/month | Switch to autoscale; tune partition key; opt out of indexing unused fields |
| Egress > 30% of bill | Add Front Door / CDN; use Private Link for cross-region; use peering for hub-spoke |
| AKS > $5k/month | Use spot nodes for stateless; right-size node SKUs; use Cluster Autoscaler aggressively |
| Storage > $2k/month | Move cold data to Cool/Cold/Archive tiers; enable lifecycle policies |
| SQL DB > $3k/month | Switch from DTU to vCore (more flexible); use Hyperscale for large DBs (cheaper than equivalent General Purpose at scale); use serverless tier for spiky workloads |
| Functions Premium > $1k/month | Audit instance count; can you go Consumption for some? |

---

## Pillar 4: Operational Excellence

**Core question:** Can the team deploy, observe, and recover changes safely?

### Assessment checklist

| # | Question | Severity if no |
|---|----------|----------------|
| O1 | Is all infrastructure defined as code (Bicep / ARM / Terraform)? | Warning |
| O2 | Are deployments automated via CI/CD (no manual portal changes for prod)? | Critical |
| O3 | Is there a staging environment with prod-like configuration? | Warning |
| O4 | Are application metrics monitored with alerting on SLO-relevant signals? | Warning |
| O5 | Are runbooks documented and accessible for common operational tasks? | Warning |
| O6 | Are deployments rolled out gradually (canary / blue-green / slots)? | Warning |
| O7 | Is on-call defined with documented escalation paths? | Warning |
| O8 | Are post-incident reviews held with blameless culture? | Info |
| O9 | Is Azure Policy used to enforce governance (tagging, allowed SKUs, allowed regions)? | Warning |
| O10 | Are deployment slots used for App Service / Functions zero-downtime swaps? | Info |

### Common findings

#### Finding: Click-ops in production

**Severity:** Critical
**Detection:** Activity log shows portal-based resource modifications by individual users in prod
**Fix:** IaC for everything. Lock down portal write access in prod (Reader only). All changes via PR + CI.

#### Finding: No staging environment

**Severity:** Warning
**Detection:** Single environment; dev = prod
**Fix:** Stand up staging with smaller-but-same-shape SKUs. Promote through dev → staging → prod via CI.

#### Finding: No SLO-based alerting

**Severity:** Warning
**Detection:** Alerts based on infra metrics (CPU, disk) but not on user-facing signals (error rate, latency p99)
**Fix:** Define SLOs (e.g., "99.5% of /search requests respond in < 500ms"). Alert on burn rate, not raw thresholds. Document SLI/SLO.

#### Finding: No deployment slots

**Severity:** Info
**Detection:** App Service deployments via direct deploy to production slot
**Fix:** Use staging slot; deploy there; warm up; swap with zero downtime. Easy rollback by re-swapping.

#### Finding: No Azure Policy governance

**Severity:** Warning
**Detection:** Untagged resources, resources in disallowed regions, public SKUs deployed despite policy
**Fix:** Built-in initiatives like "Azure Security Benchmark," "Tagging policy"; custom policies for org-specific rules. Audit mode first, then enforce.

### Operational patterns

| Pattern | When |
|---------|------|
| **GitOps** | Infra + app in Git; CI deploys on merge |
| **Slot swap** | App Service / Functions zero-downtime deploys |
| **Blue-green** | Switch traffic between full environments; supported by Front Door / Traffic Manager |
| **Canary** | Roll out to small % first; observe; expand |
| **Feature flags** | Decouple deploy from release; pair with `engineering/feature-flags-architect` |
| **SLO + error budget** | Define service objectives; spend budget on changes |

---

## Pillar 5: Performance Efficiency

**Core question:** Does the workload meet performance needs without over-provisioning?

### Assessment checklist

| # | Question | Severity if no |
|---|----------|----------------|
| P1 | Is performance tested under realistic load (not just unit tests)? | Warning |
| P2 | Are caches (Redis / CDN / Front Door) used appropriately? | Warning |
| P3 | Are database queries optimized (indexes, query plans reviewed)? | Warning |
| P4 | Is data partitioned to enable scale-out (Cosmos DB partition key; SQL sharding)? | Warning |
| P5 | Are async patterns used for I/O-bound work? | Info |
| P6 | Is autoscaling responsive to load changes (scale-up before users feel pain)? | Warning |
| P7 | Are static assets served via CDN (not direct from origin)? | Warning |
| P8 | Has the workload been profiled to identify bottlenecks? | Info |
| P9 | Are request/response sizes reasonable (no overfetching, oversized payloads)? | Info |
| P10 | Are SLOs defined and tracked (latency p95/p99, error rate, throughput)? | Warning |

### Common findings

#### Finding: No load testing

**Severity:** Warning
**Detection:** No load test artifacts; performance assumptions untested
**Fix:** Use Azure Load Testing service or k6/Locust. Test at expected peak + 50% headroom.

#### Finding: No caching

**Severity:** Warning
**Detection:** Every request hits the origin / DB; no Redis or CDN in path
**Fix:** Identify cacheable data (read-heavy, slow-changing). Add Redis for app-level cache. Add Front Door / CDN for HTTP assets.

#### Finding: Hot partition in Cosmos DB

**Severity:** Critical
**Detection:** Cosmos throttling (HTTP 429), partition key showing very uneven RU distribution
**Fix:** Re-design partition key (or composite). Sometimes requires data migration via change feed.

#### Finding: Autoscale too slow / aggressive

**Severity:** Warning
**Detection:** During load spikes, response time degrades for minutes before scale completes
**Fix:** Tune autoscale rules. Pre-scale before known peaks. Use Premium plans with faster scale.

#### Finding: No SLO definition

**Severity:** Warning
**Detection:** No documented latency / error-rate targets
**Fix:** Define SLOs with stakeholders. Set up dashboards. Use error budgets.

### Performance patterns

| Pattern | When |
|---------|------|
| **CQRS** | Separate read and write paths for very different scale profiles |
| **Event sourcing** | Append-only writes; derived read models |
| **Materialized views** | Pre-compute expensive joins / aggregations |
| **Eventual consistency** | Trade strong consistency for higher throughput |
| **Bulk operations** | Batch writes/reads to amortize per-request overhead |
| **Connection pooling** | Reuse DB / HTTP connections |
| **Async + non-blocking I/O** | Better resource utilization for I/O-bound workloads |
| **Compression** | gzip / brotli on responses; columnar formats for analytics |
| **Right-sizing for memory** | Many DB perf issues are memory bound; tune working set first |

---

## How the WAF scorer works

`scripts/azure_waf_scorer.py` takes a YAML workload spec and produces:

- **Per-pillar score** (0-100, weighted by severity of unanswered items)
- **Overall score** (average across pillars)
- **Findings list** sorted by severity
- **Remediation roadmap** ordered by impact

Example workload spec:

```yaml
name: orders-api
tier: 1
compute:
  type: app-service
  sku: P1v3
  zone_redundant: false
  autoscale: true
  slots: true
data:
  - service: sql-db
    tier: business-critical
    zone_redundant: true
    backup_pitr_days: 7
    backup_tested: false
network:
  vnet: true
  private_endpoints: true
identity:
  managed_identity: true
  rbac_scope: resource
observability:
  log_analytics: true
  app_insights: true
  alerts: true
security:
  defender_for_cloud: true
  mfa_enforced: true
operations:
  iac: true
  ci_cd: true
  staging_env: true
```

Findings example:
```
[CRITICAL] R1 Single AZ: compute.zone_redundant=false for tier-1 workload
[CRITICAL] R3 Backup untested: data[0].backup_tested=false
[WARNING] R4 No multi-region plan for tier-1
[OK]      S1-S10 all green
```
