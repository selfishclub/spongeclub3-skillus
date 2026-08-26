# Google Cloud Architecture Framework — Assessment Reference

Per-pillar deep dive on the Google Cloud Architecture Framework (CAF). For each of the five pillars: 10-question assessment checklist, common findings, severity scoring, and remediation patterns.

Use with `scripts/gcp_caf_scorer.py` to score a workload.

---

## Pillar 1: Operational Excellence

**Core question:** Can the team operate, deploy, observe, and recover safely?

### Assessment checklist

| # | Question | Severity if no |
|---|----------|----------------|
| O1 | Is all infrastructure defined as code (Terraform / Config Connector / Deployment Manager)? | Warning |
| O2 | Are deployments automated via CI/CD (no manual console changes for prod)? | Critical |
| O3 | Is there a staging environment with prod-like configuration? | Warning |
| O4 | Are application metrics monitored with SLO-based alerting? | Warning |
| O5 | Are runbooks documented and accessible? | Warning |
| O6 | Are gradual deployments used (canary / blue-green / traffic-splitting)? | Warning |
| O7 | Is on-call defined with documented escalation paths? | Warning |
| O8 | Are post-incident reviews held with blameless culture? | Info |
| O9 | Is Organization Policy used to enforce governance (allowed services, allowed regions)? | Warning |
| O10 | Are Cloud Run / GKE deployments using traffic splitting for zero-downtime? | Info |

### Common findings

#### Finding: Click-ops in production

**Severity:** Critical
**Detection:** Activity log shows console-based resource modifications by individuals in prod
**Fix:** Terraform / Config Connector. Lock console write access in prod. All changes via PR + CI.

#### Finding: No staging environment

**Severity:** Warning
**Detection:** Single environment; dev = prod
**Fix:** Stand up staging with smaller-but-same-shape resources. Promote dev → staging → prod via CI.

#### Finding: No SLO-based alerting

**Severity:** Warning
**Detection:** Alerts on raw infra (CPU, disk) not user-facing signals
**Fix:** Define SLOs (error rate, latency p95/p99). Use Cloud Monitoring SLO objects. Alert on burn rate.

#### Finding: Cloud Run / GKE deploys without traffic splitting

**Severity:** Info
**Detection:** Deploys go to 100% immediately
**Fix:** Cloud Run revisions with `--no-traffic` first; split traffic gradually. GKE: rolling updates with PDBs + canary deployments.

#### Finding: No Organization Policy

**Severity:** Warning
**Detection:** Anyone in org can create resources in any region, use any service
**Fix:** Set Org Policy constraints — allowed regions, allowed services, disallow public IPs, disallow external IPs on GCE, require shielded VMs.

---

## Pillar 2: Security, Privacy, and Compliance

**Core question:** Can the workload defend against threats, contain breaches, and meet regulatory needs?

### Assessment checklist

| # | Question | Severity if no |
|---|----------|----------------|
| S1 | Is Private Service Connect (or VPC private IP) used for managed service access? | Critical |
| S2 | Are secrets stored in Secret Manager (not env vars / config files)? | Critical |
| S3 | Are workloads using Workload Identity / Workload Identity Federation (not SA keys)? | Critical |
| S4 | Is MFA enforced for admin Google Accounts? | Critical |
| S5 | Is Security Command Center enabled (Premium for prod)? | Warning |
| S6 | Are audit logs enabled and exported to BigQuery / Pub/Sub? | Critical |
| S7 | Are IAM roles least-privileged (predefined > custom > basic)? | Warning |
| S8 | Are firewall rules least-privilege (no 0.0.0.0/0 to management ports)? | Warning |
| S9 | Is encryption at rest enabled (default for most; CMEK for compliance)? | Critical |
| S10 | Is TLS 1.2+ enforced for all public endpoints? | Warning |

### Common findings

#### Finding: Public IPs on Cloud SQL / Memorystore

**Severity:** Critical
**Detection:** Managed services accessible via public internet
**Fix:** Use private IP via Service Networking + private services access. Disable public IP. Use Cloud SQL Auth Proxy for local dev.

#### Finding: Service Account keys in source control

**Severity:** Critical
**Detection:** `*-credentials.json` files in repo, GitHub secret scanning alerts
**Fix:** Workload Identity Federation. Revoke leaked keys immediately. Org Policy `iam.disableServiceAccountKeyCreation`.

#### Finding: GCS bucket allUsers read

**Severity:** Critical
**Detection:** Bucket IAM grants `allUsers` or `allAuthenticatedUsers` read
**Fix:** Remove the grant. Use signed URLs for time-limited public access. Enable Org Policy `storage.publicAccessPrevention`.

#### Finding: No SCC

**Severity:** Warning (Critical for regulated workloads)
**Detection:** Security Command Center not enabled
**Fix:** Enable SCC Premium for org. Configure event exports. Use compliance dashboard for ISO 27001 / SOC 2 / PCI-DSS evidence.

#### Finding: Wide IAM bindings

**Severity:** Warning
**Detection:** Basic roles (`roles/owner`, `roles/editor`) assigned at project/org level
**Fix:** Replace with predefined roles (or custom roles) at the smallest scope. Use IAM Recommender for least-privilege guidance.

#### Finding: Default firewall rules allow internal traffic

**Severity:** Info (depends on threat model)
**Detection:** `default-allow-internal` rule active
**Fix:** Replace with explicit segment-by-segment firewall rules using tags or service accounts.

---

## Pillar 3: Reliability

**Core question:** Will the workload stay up under expected and unexpected conditions?

### Assessment checklist

| # | Question | Severity if no |
|---|----------|----------------|
| R1 | Is the workload deployed across multiple zones (regional resources)? | Critical |
| R2 | Is there documented RPO/RTO matching business requirements? | Critical |
| R3 | Are backups configured AND restore tested? | Critical |
| R4 | Is there a multi-region DR plan for tier-1 workloads? | Critical (tier-1) |
| R5 | Are health probes configured for all stateless services? | Warning |
| R6 | Is autoscaling enabled? | Warning |
| R7 | Are retry/circuit-breaker patterns used for dependency calls? | Warning |
| R8 | Are data services configured for HA? | Critical |
| R9 | Are managed services using regional tiers (not zonal)? | Warning |
| R10 | Has a chaos exercise been run in the past 6 months? | Info |

### Common findings

#### Finding: Single-zone GCE / Cloud SQL

**Severity:** Critical
**Detection:** VMs in single zone; Cloud SQL configured without HA
**Fix:** GCE → Regional MIG (multi-zone); Cloud SQL → Enable HA (synchronous replica in another zone).

#### Finding: Backups configured but never tested

**Severity:** Critical
**Detection:** Last restore drill > 90 days or never
**Fix:** Schedule quarterly restore tests. Document time to restore.

#### Finding: No multi-region plan for tier-1

**Severity:** Critical (tier-1)
**Detection:** Single-region setup for a customer-revenue or compliance-critical service
**Fix:** Plan failover/failback. Use Spanner multi-region for DB, or Cloud SQL cross-region replicas. Use global LB with multi-region backends.

#### Finding: No retry/backoff in code

**Severity:** Warning
**Detection:** Dependency calls without retry policy or with naive infinite retry
**Fix:** Use a retry library (tenacity, etc.) with exponential backoff + jitter + max retries. Wire circuit breakers for flaky downstream services.

---

## Pillar 4: Cost Optimization

**Core question:** Is the workload spending only what's needed for the value delivered?

### Assessment checklist

| # | Question | Severity if no |
|---|----------|----------------|
| C1 | Are resources right-sized to actual load? | Warning |
| C2 | Are Committed Use Discounts (CUDs) purchased for predictable workloads? | Warning |
| C3 | Is autoscaling enabled? | Warning |
| C4 | Are preemptible / Spot VMs used for fault-tolerant workloads? | Info |
| C5 | Is storage class tiering (Standard/Nearline/Coldline/Archive) used? | Warning |
| C6 | Are dev/test resources shut down outside business hours? | Info |
| C7 | Have orphaned resources been cleaned up (idle disks, IPs, snapshots)? | Warning |
| C8 | Are BigQuery slot reservations used for high-volume workloads? | Warning |
| C9 | Is Cloud Logging retention tuned per log type? | Warning |
| C10 | Are billing budgets and alerts configured? | Critical |

### Common findings

#### Finding: Over-provisioned VMs

**Severity:** Warning
**Detection:** Average CPU < 25% over 30 days (Recommender shows right-size suggestions)
**Fix:** Step down machine type. Don't size for peak; autoscale handles bursts.

#### Finding: No CUDs

**Severity:** Warning
**Detection:** Workload has stable baseline > 6 months; no CUDs purchased
**Fix:** Buy 1-yr or 3-yr CUDs for baseline. Resource-based CUDs (specific machine type + region) or spend-based CUDs (more flexible).

#### Finding: BigQuery on-demand for high-volume

**Severity:** Warning
**Detection:** BigQuery on-demand bill > $5k/mo
**Fix:** BigQuery Editions slots reservation. Often 30-50% cheaper at sustained scale.

#### Finding: No budgets

**Severity:** Critical
**Detection:** No billing budgets configured
**Fix:** Set monthly budgets per project / billing account. Configure email + Pub/Sub notifications at 50%/80%/100%/120%.

#### Finding: Cloud Logging at default retention for everything

**Severity:** Warning
**Detection:** All logs at default retention; Logging cost is high
**Fix:** Use log sinks: keep operational logs short retention in Logging; archive long-term audit logs to BigQuery (much cheaper for storage + queryable).

---

## Pillar 5: Performance Optimization

**Core question:** Does the workload meet performance needs without over-provisioning?

### Assessment checklist

| # | Question | Severity if no |
|---|----------|----------------|
| P1 | Is performance tested under realistic load? | Warning |
| P2 | Are caches (Memorystore / Cloud CDN) used appropriately? | Warning |
| P3 | Are database queries optimized (indexes, query plans, partitioning)? | Warning |
| P4 | Is data partitioned/sharded for scale-out? | Warning |
| P5 | Are async patterns used for I/O-bound work? | Info |
| P6 | Is autoscaling responsive to load changes? | Warning |
| P7 | Are static assets served via Cloud CDN? | Warning |
| P8 | Has Cloud Profiler been used to identify bottlenecks? | Info |
| P9 | Are request/response sizes reasonable (no overfetching)? | Info |
| P10 | Are SLOs defined and tracked (latency p95/p99, error rate)? | Warning |

### Common findings

#### Finding: No load testing

**Severity:** Warning
**Detection:** No load test artifacts; performance assumptions untested
**Fix:** Use Cloud Build + k6 / Locust. Test at expected peak + 50%.

#### Finding: BigQuery scan inefficiency

**Severity:** Warning
**Detection:** Average bytes scanned per query is large; `SELECT *` in code
**Fix:** Partition tables; cluster on filter columns; explicit column lists. Use BigQuery scheduled queries to pre-aggregate.

#### Finding: No CDN for static assets

**Severity:** Warning
**Detection:** Static images / JS / CSS served from origin
**Fix:** Cloud CDN attached to HTTP(S) LB. Or Cloud Storage with CDN + signed URLs for private assets.

#### Finding: Hot partition / hot row in Bigtable / Spanner

**Severity:** Critical
**Detection:** Spanner/Bigtable metrics show CPU at 100% while bandwidth is fine
**Fix:** Re-design key prefix to distribute load. For Bigtable, salting; for Spanner, careful primary key design.

---

## How the CAF scorer works

`scripts/gcp_caf_scorer.py` takes a YAML workload spec and produces:

- **Per-pillar score** (0-100, weighted by check severity)
- **Overall average score**
- **Failed checks list** sorted by severity
- **Remediation roadmap** in priority order

Example workload spec:

```yaml
name: orders-api
tier: 1
compute:
  type: cloud-run
  min_instances: 2
  multi_region: false
  autoscale: true
data:
  - service: cloud-sql
    tier: enterprise
    ha: true
    backup_pitr_days: 7
    backup_tested: false
  - service: bigquery
    pricing_model: on-demand
    monthly_scan_tb: 50
network:
  vpc: true
  private_service_connect: true
identity:
  workload_identity: true
  service_account_keys: false
observability:
  cloud_logging: true
  cloud_monitoring: true
  slo_alerts: true
security:
  scc_premium: true
  mfa_enforced: true
  secret_manager: true
operations:
  iac: true
  ci_cd: true
  org_policies: true
```
