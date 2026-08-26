# Compute & Data Store Decision Trees

Read this when choosing the right GCP compute path (GKE / Cloud Run / Functions / Jobs / Compute Engine / Vertex AI) or the right data store (Cloud SQL / Spanner / Firestore / Bigtable / BigQuery / Memorystore / Cloud Storage).

## Compute decision tree

GCP gives you many compute paths; picking the wrong one wastes money and operational burden.

```
Stateless HTTP service?
├── Need full control over OS / sidecar / custom runtime?
│   └── → GKE (Autopilot for managed; Standard for full control)
├── Container-packaged service, want zero infra?
│   ├── Auto-scale to zero acceptable? Per-request billing?
│   │   └── → Cloud Run (Service)
│   └── Long-running container (always-warm)?
│       └── → Cloud Run with min-instances OR GKE Autopilot
├── Function-style, event-driven?
│   └── → Cloud Functions (2nd gen, runs on Cloud Run under the hood)
├── Batch / job processing?
│   ├── Containers, finite duration?
│   │   └── → Cloud Run Jobs
│   ├── Large-scale batch (HPC)?
│   │   └── → Batch (compute engine pool) OR Dataflow (for data)
└── Long-running stateful processes / legacy?
    └── → Compute Engine VMs (MIGs for groups)

Stateful service (DBs you self-manage)?
├── → Generally prefer managed: Cloud SQL, Spanner, Firestore, BigQuery
└── Or VM + your own DB (rarely the right call)

ML inference?
├── Realtime, GPU?
│   └── → GKE (GPU node pools) OR Vertex AI online endpoints
└── Batch?
    └── → Vertex AI batch prediction OR Dataflow pipelines

Static frontend?
└── → Firebase Hosting OR Cloud Storage + Cloud CDN

API gateway?
├── In-VPC, internal-only?
│   └── → Internal HTTP(S) Load Balancer
├── Global edge, custom routing, WAF?
│   └── → External HTTP(S) Load Balancer + Cloud Armor
├── API management (rate limit, dev portal, monetization)?
│   └── → Apigee
```

See [gcp-services-reference.md](gcp-services-reference.md) for service-by-service depth: tiers, SLAs, limits, when to upgrade.

## Data store decision tree

```
Relational?
├── Standard OLTP, regional or multi-zone?
│   └── → Cloud SQL (MySQL / PostgreSQL / SQL Server)
├── Global, strong consistency, horizontal scale?
│   └── → Cloud Spanner (regional or multi-region)
├── Multi-region with high concurrency, fault-tolerant?
│   └── → Cloud Spanner (true multi-region active-active)

Document / NoSQL?
├── Mobile/web client-direct, real-time updates?
│   └── → Firestore (Native mode)
├── Schemaless, low-latency, regional or multi-region?
│   └── → Firestore OR Datastore (legacy Datastore Mode of Firestore)
├── Wide-column at massive scale, < 10ms reads?
│   └── → Bigtable

Key-value cache?
└── → Memorystore (Redis or Memcached)

Object storage?
└── → Cloud Storage (pick Standard / Nearline / Coldline / Archive)

Time-series / metrics?
├── Operational (Stackdriver-style)?
│   └── → Cloud Monitoring (built-in metric store)
├── Application time series?
│   └── → Bigtable OR BigQuery (depending on cardinality/query pattern)

Search?
├── Full-text on app data?
│   └── → Vertex AI Search OR self-managed Elasticsearch on GKE
└── Vector search for ML?
    └── → Vertex AI Vector Search OR pgvector on Cloud SQL OR Bigtable with vectors

Data warehouse?
└── → BigQuery (the answer to "should we use a warehouse?" on GCP)

Analytical OLAP?
└── → BigQuery (serverless) OR BigQuery + BigQuery BI Engine

Stream processing?
└── → Dataflow (Apache Beam) OR Pub/Sub + Dataflow
```
