# GCP Services Reference

Per-service depth on Google Cloud services most commonly used in cloud architectures: pricing tiers, SLAs, limits, when to pick each, when to upgrade, and operational defaults.

Working reference, not exhaustive. Always cross-check current GCP docs for limits and pricing.

---

## Compute services

### Google Kubernetes Engine (GKE)

**Modes:**
- **Autopilot** — Google manages nodes; per-pod billing; lower operational overhead
- **Standard** — You manage node pools; per-node billing; full flexibility

**When to pick Autopilot:**
- You don't need DaemonSets, privileged pods, GPU on most nodes, or specific node types
- Want minimum cluster operations
- Pay only for resources requested by Pods (no idle node cost)

**When to pick Standard:**
- Need full control over nodes (custom OS, GPUs, specific machine types)
- Need DaemonSets or privileged workloads
- Cost sensitivity for high-utilization workloads (Standard can be cheaper when nodes are dense)

**Pricing model:**
- **Autopilot**: per-Pod-CPU and per-Pod-memory billing; sustained-use discounts apply
- **Standard**: per-node VM cost + cluster management fee ($0.10/hour after first cluster) for Standard SLA
- **Premium tier (with uptime SLA)**: additional cost; only for clusters needing the SLA

**Operational defaults:**
- **Use Workload Identity** (KSA → GSA mapping) — eliminates SA keys in pods
- **Enable Binary Authorization** — only signed/attested images
- **Enable Shielded GKE Nodes** — Secure Boot + integrity monitoring
- **Use VPC-native cluster** (not legacy routes-based)
- **Use private cluster** — no public IPs on nodes
- **Use Anthos Service Mesh** if you need observability + traffic management
- **Use Cluster Autoscaler + HPA + VPA** for autoscaling
- **Enable Logging + Monitoring** (Cloud Operations Suite integration)

**Limits:**
- Standard max 15,000 nodes per cluster
- Autopilot max 1,000 nodes
- Max 110 Pods per node (default)

### Cloud Run

**When to use:** Container workloads; HTTP-driven or job-driven; want serverless container runtime with scale-to-zero.

**When NOT to use:** Long-running stateful processes; specialized hardware (use GKE); WebSocket-heavy apps with very long connections (Cloud Run supports up to 60 minutes for HTTP).

**Pricing model:**
- Per CPU-second + per memory-GiB-second while requests are active
- Per request fee
- Free tier: 2M requests/mo, 360k GB-s, 180k vCPU-s

**Operational defaults:**
- **Use a dedicated service account** per service
- **Use Cloud SQL Auth Proxy** OR private IP for DB access
- **Configure min-instances** if you need to avoid cold-start
- **Configure CPU always-allocated** for non-request work (e.g., listening to Pub/Sub)
- **Use VPC connector** OR direct VPC egress for VPC access
- **Set request timeout deliberately** (default 5 min, max 60 min)

### Cloud Functions (2nd gen)

**When to use:** Event-driven workloads; HTTP triggers; Pub/Sub, Cloud Storage, Firestore triggers; small focused functions.

**When NOT to use:** Anything Cloud Run handles better (Cloud Functions 2nd gen runs on Cloud Run anyway; choose Cloud Run if you want full control).

**Operational defaults:**
- **Use Eventarc** for cross-service triggers
- **Use Cloud Build** for deployments (built-in)
- **Configure VPC connector** for VPC access

### Compute Engine (GCE)

**When to use:** Stateful apps that need full VMs; specialized workloads (HPC, GPUs); legacy apps that can't be containerized; specific compliance requirements.

**Machine families:**
- **E2** — cost-optimized; auto-allocates resources
- **N2 / N2D** — general purpose Intel / AMD
- **C3 / C3D** — compute-optimized
- **M3** — memory-optimized
- **A2 / A3** — GPU (NVIDIA)
- **T2D / T2A** — Tau (cost-efficient, ARM)

**Operational defaults:**
- **Use Managed Instance Groups (MIGs)** for HA + autoscaling
- **Use OS Login** for SSH (instead of project-wide SSH keys)
- **Use Shielded VMs** (Secure Boot + vTPM + integrity monitoring)
- **Enable VM Manager** for patching
- **Use Confidential VMs** for sensitive workloads (AMD SEV / Intel TDX)

---

## Data services

### Cloud SQL

**Engines:** MySQL, PostgreSQL, SQL Server

**Editions:**
- **Enterprise** — standard tier; suitable for most workloads
- **Enterprise Plus** — additional features (data caching, near-zero downtime maintenance, longer retention)

**Operational defaults:**
- **Enable HA** (regional / multi-zone)
- **Enable automated backups** (PITR up to 35 days)
- **Use Cloud SQL Auth Proxy** or private IP (don't use public IPs in production)
- **Use IAM database authentication** (PostgreSQL/MySQL — no passwords)
- **Enable Query Insights**
- **Enable maintenance window** in low-traffic period

**Limits:**
- Max instance size depends on machine type (up to 624GB memory, 96 vCPUs)
- Max storage: 64TB (Enterprise) or 128TB (Enterprise Plus)

### Cloud Spanner

**When to use:** Strong consistency at horizontal scale; multi-region active-active; mission-critical OLTP needing 99.999%.

**When NOT to use:** Standard OLTP that fits Cloud SQL (Spanner costs more and adds complexity); analytics (use BigQuery).

**Editions:**
- **Standard** — regional; 99.99% SLA
- **Enterprise** — multi-region; 99.999% SLA
- **Enterprise Plus** — adds dual-region / fast failover features

**Pricing:** Node-hour or processing units (PU); storage; backups.

**Operational defaults:**
- **Choose multi-region** for true active-active
- **Use Spanner emulator** in local development
- **Pre-warm splits** before launch traffic
- **Use Backup + PITR**

### Firestore

**Modes:**
- **Native** — document DB; mobile/web client-direct; real-time updates
- **Datastore Mode** — legacy Datastore compatibility (cannot mix with Native in same project)

**Operational defaults:**
- **Multi-region location** for HA
- **Composite indexes** for complex queries
- **Security Rules** for client-direct access
- **TTL policies** to auto-expire old documents

### Bigtable

**When to use:** Wide-column at massive scale; sub-10ms reads; time-series; IoT; ad-tech.

**When NOT to use:** Small datasets (Cloud SQL is cheaper); transactional workloads (Spanner); document data (Firestore).

**Operational defaults:**
- **Use replication** for HA (multi-cluster instance)
- **Right-size cluster nodes** based on read/write QPS
- **Use SSD storage** (HDD only for cold data)
- **Design row keys carefully** — they're the only index

### BigQuery

**The serverless data warehouse. Always the answer to "where do we do analytics?"**

**Pricing models:**
- **On-demand** — $5/TB scanned (typical, varies by region)
- **BigQuery Editions** — Standard / Enterprise / Enterprise Plus; commit to slot capacity
- **Storage**: separate; cheap

**Operational defaults:**
- **Partition tables** by date/timestamp — massive scan reduction
- **Cluster tables** on filter columns
- **Use materialized views** for repeated aggregations
- **Use authorized views** for fine-grained access
- **Set up Editions slots** if you're running > $5k/mo on-demand
- **Use BI Engine** for BI dashboard acceleration
- **Avoid SELECT \*** — scans cost real money

### Cloud Storage

**Storage classes:**

| Class | Access cost | Storage cost | Min retention |
|-------|-------------|--------------|---------------|
| Standard | Lowest | Highest | None |
| Nearline | Higher | ~50% off | 30 days |
| Coldline | Higher still | ~80% off | 90 days |
| Archive | Very high (retrieval) | ~95% off | 365 days |

**Operational defaults:**
- **Block public access** at bucket level
- **Enable Object Versioning** for important buckets
- **Enable Object Lifecycle Management** for auto-tiering / auto-deletion
- **Use Customer-Managed Encryption Keys (CMEK)** for compliance workloads
- **Use Bucket-level IAM** (not legacy ACLs)
- **Use Signed URLs** for time-limited public access

### Memorystore

**Variants:** Redis, Memcached, Redis Cluster

**Tiers (Redis):**
- **Basic** — single node, no replication
- **Standard** — primary + replica; failover
- **Standard HA + Read replicas** — read scale-out

**Operational defaults:**
- **Standard tier minimum for production**
- **Use private IP** (default)
- **Set maxmemory-policy** appropriately
- **Configure persistence** if needed (RDB + AOF on Redis)

---

## Networking services

### Virtual Private Cloud (VPC)

GCP VPCs are **global** by default — subnets are regional, but routing is global. Different from AWS/Azure mental model.

**Subnet planning:**
- One subnet per region per workload type
- Plan IP ranges to avoid future overlap (especially for Shared VPC + Service Networking)
- Reserve secondary ranges for GKE pod and service CIDRs

**Default network:** Created in every project; **delete it** for production projects. Create your own VPC with explicit subnets.

### Load Balancers

| LB type | When |
|---------|------|
| **Global External Application LB (HTTP/S)** | Global anycast; supports Cloud Armor + CDN; serverless backends |
| **Regional External Application LB** | Single region; lower cost |
| **Internal Application LB** | Internal HTTP/S; supports serverless backends via Serverless NEG |
| **External Proxy Network LB (TCP/SSL)** | Global L4 proxy for TCP/SSL passthrough |
| **External Passthrough Network LB** | Regional L4; preserves client IP |
| **Internal Passthrough Network LB** | Internal L4 |

### Cloud Armor

WAF + DDoS protection at the edge, fronting global HTTP(S) LB.

**Tiers:**
- **Standard** — DDoS L3/L4 protection (free)
- **Plus / Enterprise** — Adaptive Protection, custom rules, WAF preconfigured rule sets (OWASP CRS)

### Private Service Connect (PSC)

**Why PSC:** Allows you to access GCP managed services and partner services via private IPs in your VPC, without VPC peering and without exposing services on public internet.

**Patterns:**
- **PSC for Google APIs** — `private.googleapis.com` or PSC endpoints for `*.googleapis.com`
- **PSC for managed services** — Cloud SQL, Memorystore, etc., reachable via private IP
- **PSC publish-consume** — partner publishes service, you consume via PSC endpoint

---

## Identity services

### Cloud IAM

**Role types:**
- **Predefined** (recommended) — e.g., `roles/storage.objectViewer`
- **Custom** — when predefined don't fit
- **Basic** (Owner, Editor, Viewer) — too broad; avoid in production

**Bind at smallest scope:** resource > project > folder > organization.

### Workload Identity Federation

The modern way to authenticate non-GCP workloads (AWS, Azure, OIDC providers, GitHub Actions, etc.) to GCP without service account keys.

**Setup:** Create a Workload Identity Pool with a provider (e.g., GitHub Actions OIDC). Workloads exchange their OIDC token for a GCP short-lived access token via STS.

**Use cases:**
- CI/CD running on GitHub Actions → no SA keys committed
- AWS Lambda calling GCP — federated, no key
- On-prem service calling GCP

### Secret Manager

**For secrets:**
- API keys, DB passwords, signing keys, OAuth client secrets

**Operational defaults:**
- **Enable Secret rotation** for supported types
- **Use CMEK** for compliance
- **Audit access via Cloud Audit Logs**
- **Use IAM at the secret level** (not just project level)

---

## Observability

### Cloud Logging

**Workspaces:** Implicitly per-project; aggregate to a centralized project via log sinks.

**Pricing:**
- First 50 GB/mo per project free
- $0.50/GB ingested after that
- Storage cost separate (varies by retention)

**Operational defaults:**
- **Use log-based metrics** for custom metrics from log events
- **Filter at source** with exclusion filters (don't ingest verbose debug logs)
- **Route to BigQuery** for long-term analytical retention (cheaper than Logging's long retention)
- **Set log retention per bucket** — default 30 days; up to 10 years

### Cloud Monitoring

**Workspaces:** Scope to multiple projects.

**Default metrics:** Most GCP services emit metrics automatically.

**Custom metrics:** Use OpenTelemetry SDK to send; or log-based metrics.

**Operational defaults:**
- **Set up uptime checks** for public endpoints
- **Configure alerting policies** on SLO-relevant signals
- **Use Cloud Monitoring SLOs** for service-level commitments

### Cloud Trace + Cloud Profiler

- **Cloud Trace** — distributed tracing across services
- **Cloud Profiler** — continuous CPU/memory profiling in production

Enable both by default for production services; cost is small relative to value.

### Security Command Center (SCC)

- **Standard tier** — basic findings, security health analytics
- **Premium tier** — Event Threat Detection, Container Threat Detection, virtual machine scanning, web security scanner, compliance dashboards (CIS, ISO 27001, PCI-DSS)

**Operational defaults:**
- **Enable SCC at org level**
- **Premium for production orgs**
- **Configure exports to Pub/Sub or BigQuery** for SIEM integration

---

## Service summary table (typical defaults for production)

| Service | Tier (typical) | Why |
|---------|----------------|-----|
| GKE | Autopilot | Lower ops; pay-per-pod |
| Cloud Run | Default + min-instances | Eliminate cold-start for prod |
| Cloud Functions | 2nd gen | 1st gen is legacy |
| Cloud SQL | Enterprise + HA | HA is critical for prod |
| Spanner | Multi-region Enterprise | Only when you need it |
| Firestore | Native + multi-region | Default for new |
| Cloud Storage | Standard + lifecycle | Tier old data via lifecycle |
| Memorystore Redis | Standard | HA |
| Global LB | HTTP(S) + Cloud Armor | Edge protection |
| Cloud Armor | Plus / Enterprise | WAF rules + adaptive |
| BigQuery | Editions slots above $5k/mo on-demand | Predictable cost |
| Cloud Logging | Default + sinks to BQ | Long retention cheaper in BQ |
| Cloud Monitoring | Default + uptime checks | Always on |
| SCC | Premium | For prod orgs |

---

## Common pricing gotchas

- **Inbound is free; outbound is charged.** Egress dominates many bills.
- **Inter-region (within GCP) is charged.** Replication, backups to other regions, cross-region API.
- **Inter-zone (same region) is small but non-zero.** Multi-zone HA does have a small cost.
- **BigQuery: scan cost dominates if you SELECT \*.** Partition + cluster + select only what you need.
- **Cloud Logging: ingestion + retention can balloon.** Filter at source; tier retention.
- **GKE Autopilot vs Standard:** Autopilot can be more expensive for high-utilization clusters; Standard cheaper for dense workloads.
- **Persistent disk snapshots are incremental;** first snapshot full size; subsequent only changes.
- **Static external IPs cost when attached AND when unattached.** Reclaim unused IPs.
- **Premium network tier vs Standard tier:** Premium uses Google's backbone (default; better latency, more expensive); Standard exits Google's network at nearest egress (cheaper, more variability).

---

## Region selection criteria

| Criteria | Lever |
|----------|-------|
| Latency to users | Pick a region closest to majority of users |
| Latency to other GCP services | Same region preferred |
| Compliance | EU workloads → EU regions; financial → specific |
| Cost | Some regions consistently cheaper (e.g., us-central1 often) |
| Service availability | Not all services in all regions; check before designing |
| Carbon | GCP publishes carbon-free energy % per region; some teams optimize for this |

---

## When to graduate

| You currently have | Consider upgrading to |
|--------------------|----------------------|
| Cloud Run no min-instances | Add min-instances for prod (cold-start mitigation) |
| Cloud SQL single zone | Multi-zone HA |
| Cloud SQL → growing past 64TB | Spanner |
| GKE Standard with low utilization | Autopilot (cheaper for sparse pods) |
| Public IPs on managed services | Private Service Connect |
| SA keys for CI/CD | Workload Identity Federation |
| Default VPC | Custom VPC with explicit subnets |
| BigQuery on-demand > $5k/mo | Editions slot reservations |
| Cloud Logging at default retention | Filter at source + BQ sink for long-term |
| No SCC | SCC Premium |
| Single project | Folder + multi-project + Shared VPC |
