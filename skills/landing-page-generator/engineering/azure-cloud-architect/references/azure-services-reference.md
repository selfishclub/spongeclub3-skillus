# Azure Services Reference

Per-service depth on the Azure services most commonly used in cloud architectures: pricing tiers, SLAs, limits, when to pick each, when to upgrade, and operational defaults.

This is a working reference, not exhaustive. Always cross-check current Azure docs for limits and pricing — Azure changes quickly.

---

## Compute services

### Azure Kubernetes Service (AKS)

**When to use:** Container workloads requiring full Kubernetes API; multi-service platform engineering; need for CRDs / Operators / custom schedulers.

**When NOT to use:** Single web app (App Service is cheaper and simpler). Batch jobs (Container Apps Jobs / Batch).

**Pricing model:**
- Control plane: free (Free tier) or $0.10/hr (Standard with uptime SLA) or $0.60/hr (Premium with extra support)
- Worker nodes: standard VM pricing (VMSS-managed)
- Add-ons: monitoring (Container Insights via Log Analytics), Azure Policy, Azure Monitor agents

**Operational defaults you should set:**
- **Enable Managed Identity** for kubelet (system-assigned) and for workloads (workload identity)
- **Enable Azure RBAC + Entra ID integration** (don't use local accounts)
- **Enable Network Policies** (Calico or Azure NPM)
- **Use Container Insights** for cluster + node + pod metrics
- **Enable Defender for Containers** (security posture management)
- **Use private cluster** unless public API endpoint is justified
- **Set up cluster autoscaler** with reasonable bounds
- **Set up Pod Disruption Budgets** on critical workloads

**Limits to know:**
- Max nodes per cluster: 1000 (most regions)
- Max pods per node: 250 (default), can go to 500 (advanced networking)
- Max node pools: 100
- AKS doesn't manage etcd backups; consider Velero for cluster state backup

### Azure App Service

**When to use:** Standard web apps (Node, Python, .NET, Java, PHP, Ruby) where you don't want to manage containers/orchestration.

**When NOT to use:** Need GPU; need cron-style scheduled jobs (use Logic Apps or Functions); need fine-grained control over OS / sidecar (use AKS).

**Tiers (Linux):**
- **Free / Shared** — dev/test only; no SLA; shared CPU
- **Basic (B1/B2/B3)** — small prod workloads; manual scale; 99.95% SLA per instance
- **Standard (S1/S2/S3)** — autoscale, deployment slots, 99.95% SLA
- **Premium v3 (P1v3/P2v3/P3v3)** — VNet integration, faster scale, dedicated cores, 99.95% SLA
- **Isolated v2** — App Service Environment v3; dedicated VNet, regulatory workloads

**Tip:** Premium v3 is now usually cheaper than Premium v2 for equivalent specs. Always check current pricing.

**Operational defaults:**
- **Use Premium v3 if you need VNet integration** (most production workloads do)
- **Enable deployment slots** (staging slot + swap) for zero-downtime deploys
- **Reference secrets from Key Vault** via App Settings: `@Microsoft.KeyVault(SecretUri=...)`
- **Enable Application Insights** for distributed tracing + metrics
- **Set custom domains + managed certificates**
- **Use Managed Identity** for outbound calls to Azure services

### Azure Container Apps

**When to use:** Microservices needing scale-to-zero, KEDA-based event scaling, container runtime without K8s overhead.

**When NOT to use:** Need full Kubernetes API (use AKS); single web app (App Service is simpler).

**Pricing model:**
- Per-vCPU-second + per-GiB-second of memory allocated, while requests are active
- Free monthly allowance: 180,000 vCPU-seconds + 360,000 GiB-seconds + 2M requests

**Operational defaults:**
- **Use revisions** for blue/green deployment
- **Use Managed Identity** for service-to-service auth
- **Use Dapr** if your services would benefit from pub/sub + state + secrets abstractions
- **Set CPU/memory limits** matching expected load (autoscale handles bursts)
- **Use private endpoints** for connections to PaaS

### Azure Functions

**When to use:** Event-driven workloads; HTTP APIs with sporadic traffic; lightweight processing; integration "glue."

**Plans:**
- **Consumption (Y1)** — pay per execution + memory-seconds; auto-scale; cold start latency; no VNet
- **Premium (EP1/EP2/EP3)** — always-warm; VNet integration; longer timeouts; per-instance pricing
- **Dedicated (App Service Plan)** — runs in your App Service Plan; predictable cost; reuse existing plan

**Operational defaults:**
- **Use Application Insights** (auto-enabled)
- **Use Premium plan for VNet** (Consumption can't reach private endpoints)
- **Use Functions v4 runtime** + supported language version
- **Set host timeout deliberately** (default 5 min Consumption; 30 min Premium)
- **Use durable functions** for orchestration patterns (don't write your own)

### Virtual Machine Scale Sets (VMSS)

**When to use:** Legacy stateful apps that need full VMs; specialized workloads (HPC, GPU); apps that can't be containerized.

**When NOT to use:** Anything stateless that fits a managed service.

**Operational defaults:**
- **Use availability zones** for HA (not single-zone)
- **Use Managed Identity**
- **Use Azure Update Manager** for OS patching
- **Tag all VMs** for cost allocation
- **Enable Defender for Servers** (Microsoft Defender Cloud)

---

## Data services

### Azure SQL Database

**When to use:** OLTP relational workload; standard SQL Server compatibility.

**Tiers / deployment models:**
- **Single Database** — most common; vCore or DTU model
- **Elastic Pool** — multiple DBs sharing resources; good for SaaS multi-tenant
- **Hyperscale** — DB > 4TB with fast restore; serverless variant available
- **Managed Instance** — SQL Server feature parity (cross-DB queries, agent, etc.)

**vCore model:**
- **General Purpose** — Standard SLA, remote storage; balanced
- **Business Critical** — local SSD, in-memory OLTP; high HA via AlwaysOn
- **Hyperscale** — separate compute / log / page servers; near-instant restore

**Operational defaults:**
- **Use Managed Identity** for app connection (no SQL auth)
- **Enable auditing → Log Analytics**
- **Enable Microsoft Defender for SQL**
- **Configure backups**: PITR retention 7-35 days; LTR up to 10 years
- **Configure geo-replication** for DR (Active geo-replication or auto-failover groups)
- **Enable Always Encrypted** for sensitive columns (column-level encryption)
- **Use Private Endpoint** (disable public access)

### Azure Cosmos DB

**When to use:** Global distribution; multi-region writes; flexible schema; need for multiple consistency models.

**APIs:**
- **NoSQL (Core)** — JSON documents; Azure-native; most features
- **MongoDB** — Mongo wire protocol compatibility
- **Cassandra** — CQL compatibility
- **Gremlin** — graph DB
- **Table** — Azure Table Storage compatibility
- **PostgreSQL (Citus)** — distributed PG; columnar; HTAP

**Consistency levels (NoSQL API):**
- **Strong** — linearizable, single-region only effectively
- **Bounded Staleness** — lag bounded by time/version
- **Session** — read-your-own-writes within a session (default; usually right)
- **Consistent Prefix** — reads see writes in order
- **Eventual** — cheapest; no ordering guarantees

**Pricing model:**
- **Manual throughput (RU/s)** — provision capacity; predictable cost
- **Autoscale** — sets a ceiling; pays for max(used, 10% of ceiling)
- **Serverless** — per-request; good for low/spiky traffic, max 1TB

**Operational defaults:**
- **Use Session consistency** unless you have specific reason for stronger
- **Use partition key thoughtfully** — hot partitions = throttling
- **Index policy**: opt out of indexing fields not queried (saves RU/cost)
- **Use private endpoint**
- **Enable continuous backup** (point-in-time restore)
- **Monitor RU consumption** per partition

### Azure Database for PostgreSQL Flexible Server

**When to use:** Need actual PostgreSQL (extensions, behavior). Most modern PG workloads.

**Tiers:**
- **Burstable** — small workloads; dev/test
- **General Purpose** — most workloads
- **Memory Optimized** — analytical / cache-heavy

**Operational defaults:**
- **Use private endpoint**
- **Enable HA** (zone-redundant if available in region)
- **Configure backups**: PITR retention 7-35 days
- **Use Managed Identity** for auth (instead of password)
- **Set up read replicas** for read scale-out
- **Enable extensions selectively** — `pg_cron`, `pg_stat_statements`, `pgvector`, etc.

### Azure Storage

**Account types:**
- **Standard general-purpose v2** — most workloads
- **Premium block blobs** — high-throughput blob (low-latency reads)
- **Premium file shares** — performance-tier file
- **Premium page blobs** — for VM disks

**Blob tiers:**
- **Hot** — frequent access; highest storage cost, lowest access cost
- **Cool** — < 30 days, infrequent access
- **Cold** — < 90 days, rare access
- **Archive** — long-term, retrieval in hours

**Operational defaults:**
- **Disable public blob access** at account level
- **Enable soft delete** for blobs + containers (7-365 day retention)
- **Enable versioning** (or use immutable storage / WORM for regulated)
- **Use Private Endpoint**
- **Use Managed Identity** for app access
- **Enable lifecycle management** to auto-tier old data
- **Enable Microsoft Defender for Storage**

### Azure Cache for Redis

**Tiers:**
- **Basic** — single node; no SLA
- **Standard** — 2 nodes (primary + replica); 99.9% SLA
- **Premium** — clustering, persistence, VNet, geo-replication; 99.95% SLA
- **Enterprise / Enterprise Flash** — Redis Enterprise features; multiple primary nodes; very large memory

**Operational defaults:**
- **Use Standard at minimum for production**
- **Premium if you need VNet integration**
- **Configure maxmemory-policy** appropriately for your access pattern
- **Set up alerts** on memory pressure, eviction count, replication lag
- **Use private endpoint**

---

## Networking services

### Virtual Network (VNet) + subnets

**Default address spaces** to avoid: 10.0.0.0/16 (very common); pick something distinct (e.g., 10.42.0.0/16) to enable peering with other environments without conflict.

**Subnets** to plan:
- App subnets (per workload)
- Database subnets (for delegation to managed PG/MySQL)
- AKS subnets (one per node pool if using kubenet; one per cluster if using Azure CNI)
- Private Endpoint subnet
- Gateway subnet (mandatory for VPN/ExpressRoute)
- Azure Firewall subnet (if used)
- Bastion subnet (if used)

### Application Gateway

**Tiers:**
- **Standard v2** — basic L7 LB
- **WAF v2** — adds OWASP Core Rule Set 3.x

**When to use:** Internal-facing or regional LB with WAF; URL-based routing; SSL termination; cookie affinity.

**When NOT to use:** Global (use Front Door); simple TCP load balancing (use Standard Load Balancer).

### Front Door

**Tiers:**
- **Standard** — basic
- **Premium** — adds private link to origin, managed rules, bot protection

**When to use:** Global L7 routing; static + dynamic content acceleration; WAF at edge; multi-region failover.

**Cache TTLs:** configure per route; default is what your origin says (Cache-Control); override if you need.

### Azure Firewall

**Tiers:**
- **Standard** — L3-L4 + FQDN allowlist
- **Premium** — TLS inspection, IDPS, URL filtering
- **Basic** — small workloads (< 250 Mbps)

**Force-tunneling pattern:** All spoke VNet egress UDR'd through the firewall in the hub. Inspect/log all outbound.

---

## Identity services

### Microsoft Entra ID (formerly Azure AD)

**Tiers:**
- **Free** — basic identity, sync from on-prem
- **P1** — Conditional Access, MFA, password write-back, Identity Protection (lite)
- **P2** — Identity Protection, PIM (Privileged Identity Management), access reviews

**P1 is the practical minimum for any organization with security requirements.**

### Key Vault

**Tiers:**
- **Standard** — software-protected keys; suitable for most secrets/certificates
- **Premium** — HSM-protected keys; required for some compliance (FIPS 140-2 Level 2)

**Operational defaults:**
- **Enable soft-delete** (mandatory)
- **Enable purge protection** (mandatory for prod)
- **Use Managed Identity** for app access; never embed keys
- **Use Private Endpoint** (disable public network access)
- **Use RBAC mode** (not access policies) for permission management
- **Rotate keys** periodically (Key Vault can auto-rotate certain keys)
- **Audit logs → Log Analytics**

---

## Monitoring & observability

### Azure Monitor + Log Analytics

**Workspaces:**
- One workspace per environment (prod / staging / dev), or per region for sovereignty
- **Pricing tiers**: Pay-as-you-go ($2.30/GB ingested typical) or Commitment tier ($/day)
- **Retention**: 30 days default (free); paid up to 730 days; archive tier beyond

**Data sources to send:**
- All Azure resource diagnostic logs (audit + resource logs)
- AKS Container Insights
- VM Insights (if using VMs)
- Application Insights (per app)

### Application Insights

**When to use:** Every web/API workload that you want distributed tracing + metrics for.

**Modes:**
- **Workspace-based** (recommended): connected to a Log Analytics workspace
- **Classic** (deprecated): standalone instance

**Sampling:** Adaptive (default) keeps cost in check; fixed-rate if you want predictable. Set sample rate to 100% in dev, lower in prod.

### Defender for Cloud

**When to use:** Always. Microsoft's CSPM + CWPP suite. Includes regulatory compliance dashboard mapping to ISO 27001 / SOC 2 / PCI-DSS / etc.

**Plans:**
- Free / Foundational CSPM
- Defender for Servers (P1/P2) — agent-based, vulnerability mgmt
- Defender for SQL — threat detection on DBs
- Defender for Containers — AKS security
- Defender for Storage — anomalous access detection
- Defender for App Service — runtime protection
- Defender for Key Vault — anomalous access

---

## Service summary table (typical defaults for production)

| Service | Tier (typical) | Why |
|---------|----------------|-----|
| AKS | Standard with uptime SLA | Need SLA for prod |
| App Service | Premium v3 | VNet integration + scale + slots |
| Container Apps | n/a (consumption-based) | No tier choice |
| Functions | Premium EP1 | For VNet + always-warm; Consumption only for sporadic |
| SQL Database | General Purpose, Gen5, vCore | Balanced; upgrade if you hit IOPS limits |
| Cosmos DB | Autoscale or serverless | Match traffic shape |
| PG Flexible Server | General Purpose with HA | HA is critical |
| Storage | Standard GPv2 | Premium only if you need it |
| Cache for Redis | Standard or Premium | Premium for VNet |
| Application Gateway | WAF v2 | WAF always on |
| Front Door | Premium | If you need global edge + WAF |
| Key Vault | Standard | Premium only for HSM mandate |
| Log Analytics | PAYG | Commitment tier above ~100GB/day |
| Entra ID | P1 | Minimum for Conditional Access |
| Defender for Cloud | Per service: enable | Cost grows with services protected |

---

## Common pricing gotchas

- **Inbound traffic is free; outbound (egress) is charged.** Plan accordingly (caching, CDN, region affinity).
- **Cross-region traffic is charged at outbound rate.** Replication, backup-to-other-region, cross-region API calls.
- **Cross-AZ traffic in same region is usually free.** (Within VNet.)
- **Read-replicas, geo-replication, etc.** double or more storage cost.
- **Premium SSDs cost much more than Standard SSDs.** Premium only if your IOPS need it.
- **Log Analytics ingestion** can dominate budget. Filter at source; archive cold logs.
- **Snapshots** are charged for what changes; sparse snapshots are cheap; full backups are not.
- **Disk size, not used capacity, is billed** for unmanaged disks. Right-size.
- **Idle resources still bill** — unused IPs, unused disks, stopped (but not deallocated) VMs.

---

## Region selection criteria

| Criteria | Lever |
|----------|-------|
| Latency to users | Pick a region closest to majority of users |
| Latency to other Azure services | Same region preferred; same paired region good DR |
| Compliance | EU workloads → EU regions; financial → specific regions sometimes mandated |
| Cost | Some regions consistently cheaper (e.g., West Europe < UK South often) |
| Service availability | Not all services in all regions; check before designing |
| Capacity | New regions sometimes constrained; check before large workloads |

**Paired regions** (Microsoft's term for Azure region pairs): used for some replication features. Most cross-region setups don't need pairs strictly, but it's a known-good DR choice.

---

## When to graduate

| You currently have | Consider upgrading to |
|--------------------|----------------------|
| App Service Basic | Premium v3 if you need VNet, scale, or slots |
| SQL DB DTU model | vCore model (more flexible) |
| Cosmos DB manual throughput | Autoscale if traffic varies |
| Single-region | Multi-region with Traffic Manager / Front Door |
| Public endpoints | Private Endpoint via Private Link |
| Shared keys for auth | Managed Identity |
| Spread tags / no governance | Azure Policy + Management Groups |
| Manual deployment | Bicep + GitHub Actions / Azure DevOps |
| Log Analytics PAYG with > 100GB/day | Commitment tier |
| AKS Free control plane | Standard (with uptime SLA) for prod |
