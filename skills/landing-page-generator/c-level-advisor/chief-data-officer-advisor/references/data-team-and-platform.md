# Data Team & Platform Reference

How to organize the data function, the roles you need, and the platform
patterns that work in 2026.

## 1. The data org — three core groups

### A) Data Platform
Owns infrastructure, tooling, and shared services. Roles:
- Platform engineering (ingestion, transformation orchestration, storage, observability)
- DataOps / SRE-for-data (reliability, on-call, cost)
- Catalog and lineage tooling owner
- Quality tooling owner

### B) Data Engineering (domain or central)
Owns pipelines and dataset production. Roles:
- Senior / Staff data engineer (ingestion, transformation, modeling)
- Analytics engineer (dbt-style transformation; semantic layer)
- ML data engineer (feature engineering, feature store)

### C) Analytics + Insights
Owns "insight production" for the business. Roles:
- Analytics lead per domain
- Senior analyst / decision-science partner
- BI engineer (self-serve enablement)
- Data scientist (when ML is in scope; otherwise embedded in product/AI org)

### D) Governance (separate group; sometimes inside the platform group)
Owns policy and stewardship. Roles:
- Head of data governance
- Data steward leads
- Privacy partner (dotted line into DPO / legal)

## 2. Hiring sequence by org size

### Stage 1 — < 100 engineers
- **1–2 generalist data engineers** (ingestion + transformation + ad-hoc analytics)
- **1 analyst** (often shared with finance / ops)
- **Catalog and quality are manual / lightweight**

### Stage 2 — 100–500 engineers
Add:
- **Platform engineer #1** for ingestion + observability
- **Analytics engineer** for dbt models, semantic layer
- **Lead analyst per domain** (often 3–5 by Series B)
- **Part-time data governance lead** (often inside privacy / GRC)

### Stage 3 — 500–2000 engineers
Add:
- **Head of data platform** + 3–5 platform engineers
- **Data governance lead** (full-time) + 1–2 stewards
- **Analytics engineering leads** (1 per domain)
- **Analytics leads** embedded in BU
- **First data product manager**

### Stage 4 — 2000+ engineers
Add:
- **CDO** (if not already in place)
- **Domain data engineering teams** (data mesh-style ownership where appropriate)
- **Dedicated MDM lead**
- **Data product manager(s)** for internal + external products
- **Red-team-equivalent for governance** (assurance, internal audit)

## 3. Role definitions

### Chief Data Officer
- Owns data strategy, portfolio, and risk
- Peer to CTO / CISO / CAIO (sometimes reports to CEO, COO, or CFO)
- Decision rights: budget, platform direction, governance policy
- Board-facing for data narrative

### Head of Data Platform
- Owns the platform, observability, cost, vendor management
- Sets standards every domain consumes
- Reports to CDO or CTO

### Head of Data Governance
- Owns governance program, council secretariat, policy, audit
- Liaises with GC, privacy, security
- Reports to CDO

### Data Steward (domain)
- Owns quality + classification + lineage hygiene for a domain
- Part-time role; reports to business leader; dotted-line to governance

### Analytics Engineer
- Transforms raw data into modeled, tested datasets
- Owns the semantic layer for their domain
- Modern dbt practitioner profile

### Data Engineer
- Ingestion, transformation infra, complex pipelines
- Pairs with analytics engineers and platform team

### Data Scientist / ML Engineer
- Modeling, feature engineering, model deployment
- May live in product, AI org, or central depending on stage

### Data Product Manager
- Owns the roadmap, SLAs, adoption of a data product
- Especially needed when data products go external

## 4. Org pattern recommendations by stage

| Stage | Pattern | Reporting line |
|-------|---------|----------------|
| < 200 engineers | Central data team | CTO or COO |
| 200–500 | Hub-and-spoke; central platform + embedded analysts | CDO or CTO |
| 500–2000 | Hub-and-spoke at scale; domain ownership for analytics + dbt | CDO (CEO or CFO) |
| 2000+ | Hub-and-spoke or mesh; central platform-as-product | CDO at exec table |

Most orgs that try data mesh too early end up with mush. Earn the right
to mesh by first running hub-and-spoke well.

## 5. Compensation realities (2026, US-tier markets)

| Role | Base | Total comp (approx.) |
|------|------|----------------------|
| Sr data engineer | $180k–$240k | $300k–$450k |
| Staff data engineer | $230k–$320k | $450k–$700k |
| Analytics engineer | $160k–$220k | $250k–$400k |
| Head of data platform | $250k–$340k | $500k–$900k |
| Data governance lead | $180k–$260k | $300k–$450k |
| CDO | $350k+ | $700k–$1.6M (equity-heavy) |

European markets generally run 50–70% of US numbers.

## 6. Data platform — the canonical stack (2026)

A pragmatic, opinionated baseline:

| Layer | Default pick | Alternatives |
|-------|--------------|--------------|
| Object storage | S3 / GCS / ADLS | — (de facto cloud) |
| Open table format | Iceberg | Delta, Hudi |
| Warehouse | Snowflake / BigQuery / Redshift / Databricks SQL | Synapse |
| Ingestion | Fivetran / Airbyte | Custom for proprietary sources |
| CDC | Debezium | Vendor CDC |
| Orchestration | Airflow / Dagster / Prefect | Argo Workflows for k8s-native |
| Transformation | dbt | SQLMesh, native SQL |
| Reverse ETL | Hightouch / Census | Custom |
| BI | Looker / Tableau / Mode / Hex | Metabase, Superset |
| Catalog + lineage | DataHub / OpenMetadata / Atlan / Collibra | Unity Catalog inside lakehouse |
| Quality | Great Expectations / Soda / dbt tests | Custom |
| Observability | Monte Carlo / Bigeye / OSS combos | — |
| Semantic layer | dbt Semantic Layer / Cube | Native in warehouse |
| Feature store | Feast / Tecton | Vendor-native |
| Streaming | Kafka / Kinesis / PubSub | Pulsar |
| Stream processing | Flink / Spark Streaming | ksqlDB |

Don't pick all 14 layers from different vendors. Sane consolidations:

- **Snowflake-anchored:** Snowflake + Fivetran + dbt + Looker + OpenMetadata + Monte Carlo + Feast
- **Databricks-anchored:** Databricks (storage + compute + Unity Catalog) + dbt + Hex + Monte Carlo + Tecton
- **BigQuery-anchored:** BigQuery + Airbyte + dbt + Looker + DataHub + Soda + Vertex
- **OSS-leaning:** S3 + Iceberg + Trino/Spark + Airflow + dbt + Superset + DataHub + Great Expectations

## 7. Cost levers (where most data spend leaks)

- **Warehouse compute on long-running queries** — query optimization + workload management
- **Pipeline cost from over-frequent runs** — match schedule to consumer need
- **Ingestion cost for huge slowly-changing sources** — CDC + incremental
- **Storage of tables nobody uses** — TTL + lifecycle policy
- **Tool sprawl** — three BI tools, two catalogs, two quality tools — consolidate
- **Vendor over-commitment** — annual commits with no usage tracking

Track cost per data product, not just total spend. Cost-attribution
discipline changes behavior more than dashboards.

## 8. Data platform SLOs

A platform team is a SaaS team — instrument it accordingly:

- **Pipeline reliability:** % of expected runs that succeed (target 99%+)
- **Pipeline latency:** P95 lag from source event to consumer (per pipeline)
- **Query latency:** P95 query time on certified datasets
- **Catalog freshness:** median age of last reviewed metadata
- **Cost per insight:** $ per modeled dataset, per dashboard, per data product

## 9. Data product mindset

Treat datasets and dashboards as products, not artifacts.

A "data product" has:
- An owner accountable for outcomes (not just for the code)
- A defined consumer (named team or persona)
- An SLA (freshness, quality, schema stability)
- A roadmap (additions, deprecations, changes communicated)
- Telemetry (usage, satisfaction, business impact)

If those five aren't true, you have a dataset, not a product. Mixing the two
is fine; pretending otherwise is the problem.

## 10. The replatforming question

You consider a replatform when:
- Cost growth is outpacing usage growth materially
- Onboarding a new use case takes >2x the time it should
- Critical capabilities (governance, openness, AI) are blocked by the platform
- Vendor risk has become existential (price hikes, deprecations, lock-in)

You don't replatform when:
- The platform is annoying but functional
- A vocal advocate has a new favorite tool
- You haven't proven the use case the new platform unlocks

Use `data_platform_evaluator.py` to make the decision defensible — and
expect any replatform to take 12–24 months in a serious org.

## 11. Outsourcing — what works, what doesn't

Works:
- **Annotation and labeling** with your QA layer
- **Implementation partners** for one-time migrations
- **Audit and assurance**
- **Vendor management** for utility tools

Doesn't work:
- **Data strategy** (too company-specific)
- **Governance program ownership**
- **Critical-pipeline ownership**
- **Eval design** for differentiating analytics

## 12. AI / data interface

The CDO and CAIO share the data plane. Common splits:

- CDO owns: warehouse, lake, catalog, governance, quality, BI platform
- CAIO owns: model registry, eval harness, foundation-model gateway, AI policy
- Shared: feature store, retrieval pipelines, AI eval datasets, data classification for AI use

The interface is brittle without:
- Shared classification + access standards
- Shared incident response process
- Joint forum (the CAIO sits on the data council; CDO sits on the AI council)
- Joint budget for ML data infrastructure (feature store, eval datasets)

## 13. Common pitfalls

- **Org chart that hides ownership.** Two people own everything = no one owns anything.
- **Platform team that doesn't measure adoption.** Tools without users.
- **Analytics team without engineering rigor.** Untested dashboards become the source of truth.
- **Governance team without operational integration.** Pure policy office.
- **A single staff engineer who knows the whole stack.** Bus risk.
- **Replatform as a make-work project.** Always anchor to a use case.
