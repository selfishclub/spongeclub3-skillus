# CAF, Cost Optimization, Workflows & Anti-Patterns

Read this when running a Cloud Architecture Framework assessment, optimizing GCP cost, executing an end-to-end design/review/migration workflow, or checking for GCP-specific anti-patterns.

## Google Cloud Architecture Framework (CAF)

GCP's framework has five pillars (same naming families as Azure/AWS but with Google flavor).

| Pillar | Core question |
|--------|---------------|
| **Operational Excellence** | Can the team operate, deploy, observe, and recover safely? |
| **Security, Privacy, and Compliance** | Can the workload defend, contain, recover, and meet regulatory needs? |
| **Reliability** | Will the workload remain available under expected and unexpected conditions? |
| **Cost Optimization** | Is the workload spending only what's needed for the value delivered? |
| **Performance Optimization** | Does it meet performance needs without over-provisioning? |

Use `scripts/gcp_caf_scorer.py --workload-config workload.yaml` to score against each pillar.

See [gcp-well-architected.md](gcp-well-architected.md) for the per-pillar deep dive: 10-question checklist per pillar, common findings, remediation patterns.

## Cost optimization

### Cost levers from biggest to smallest

| Lever | Typical savings | Effort |
|-------|----------------|--------|
| **Right-sizing** | 30-50% | Low |
| **Committed Use Discounts (CUDs) / Sustained Use Discounts (SUDs)** | 20-70% | Low (commitment) |
| **Autoscaling** | 20-40% | Medium |
| **Preemptible / Spot VMs** | up to 91% | Medium |
| **Storage class tiering** | 30-95% on storage | Low |
| **Egress reduction** (Cloud CDN; private peering) | Variable, large | Medium-High |
| **Decommission unused** | Variable | Low |
| **BigQuery slot reservations** | 30-50% on analytics | Medium |
| **Region choice** | 10-25% | High (move) |

### Cost anti-patterns

- **Premium service tiers by default.** Enterprise Spanner / large BigQuery on-demand / GKE Standard when Autopilot suffices.
- **No autoscaling.** Always provisioned at peak. Easy 30-40% savings.
- **Egress through public internet.** Multi-region without peering or Cloud CDN.
- **Logs / metrics retention at default 30+ days for all data.** Tiering needed.
- **BigQuery on-demand pricing for stable, high-query workloads.** Reserved slots beat on-demand at scale.
- **Preemptible VMs not used for batch / fault-tolerant workloads.** Up to 91% savings missed.
- **Public IPs forgotten.** Each costs a few dollars/mo; multiply by hundreds of orphans.

See [gcp-cost-optimization.md](gcp-cost-optimization.md) for the full lever catalog and detection patterns.

## End-to-end workflows

### Workflow: Design a new workload

1. **Understand requirements** — traffic, data scale, latency, region requirements, compliance.
2. **Pick compute** using the decision tree.
3. **Pick data stores** using the decision tree.
4. **Design networking** — VPC topology, PSC, LB pattern.
5. **Design identity** — Service Accounts, Workload Identity, IAM scopes.
6. **Plan observability** — Cloud Logging, Cloud Monitoring, Cloud Trace, Cloud Profiler.
7. **Estimate cost** with `scripts/gcp_cost_estimator.py`.
8. **Validate against CAF** with `scripts/gcp_caf_scorer.py`.
9. **Document** the architecture; share for review.

### Workflow: Review an existing GCP architecture

1. **Gather artifacts** — Terraform code, network diagrams, service inventory.
2. **Run the validator** — `scripts/gcp_architecture_validator.py --terraform ./infra/*.tf` flags structural issues.
3. **Run CAF scorer** with the workload's actual config.
4. **Identify high-cost components** with the cost estimator.
5. **Produce findings** by pillar with severity and recommendation.

### Workflow: Migrate from AWS / Azure to GCP

1. **Map services** — most have equivalents (SQS → Pub/Sub; SNS → Pub/Sub topics; Lambda → Cloud Functions / Cloud Run; DynamoDB → Bigtable or Firestore; S3 → Cloud Storage; RDS → Cloud SQL or Spanner).
2. **Re-evaluate the architecture** in GCP-native terms (BigQuery is often the right answer for analytics in ways no other cloud quite matches).
3. **Network parity** — VPC equivalent (global VPC is unique to GCP); IAM equivalent; private connectivity (PSC).
4. **Data migration** — Database Migration Service for many SQL scenarios; Storage Transfer Service for object data; Datastream for CDC.
5. **Cost re-estimate** — GCP pricing differs per-service; don't assume parity.

## Anti-patterns (GCP-specific)

- **Service Account keys committed to source control.** Use Workload Identity Federation everywhere possible.
- **Single-zone production** — use multi-zone or regional resources by default.
- **No org policies** — set up Org Policy constraints (e.g., disallowed services, allowed regions, no public IPs).
- **Compute Engine VMs with public IPs by default.** Use NAT Gateway + private IPs.
- **GCS bucket allUsers read** — almost never wanted; use IAM + signed URLs.
- **Default network in use** — delete the default VPC; create your own with explicit subnets.
- **BigQuery on-demand for known high-volume workloads.** Buy slot reservations.
- **Cloud SQL without HA** — single-zone DB is one zone outage from disaster.
- **Service account = same email as default Compute SA used everywhere.** Create distinct SAs per workload.
- **Firestore Native + Datastore mixed** — same project can't have both modes simultaneously; design once.
- **GKE Standard when Autopilot would work.** Autopilot eliminates node management; cheaper to operate.

## Tooling outputs

| Script | Input | Output |
|--------|-------|--------|
| `scripts/gcp_architecture_validator.py` | Terraform file or YAML workload spec | Structural issues, anti-pattern findings, missing best-practice settings |
| `scripts/gcp_cost_estimator.py` | YAML workload spec (services + tiers + scale) | Per-service monthly cost estimate, total, optimization opportunities |
| `scripts/gcp_caf_scorer.py` | YAML workload spec | Score per CAF pillar, gap analysis, recommendations |

All scripts: stdlib only, argparse CLI, JSON or markdown output.
