# Azure Decision Trees: Compute, Data, Networking, Identity

Read this when selecting Azure services for a workload — compute, data store, networking topology, or identity. For per-service depth (tiers, SLAs, limits) see `azure-services-reference.md`.

## Compute decision tree

Azure offers many compute options; picking the wrong one wastes money and adds operational burden.

```
Stateless HTTP service?
├── Need full control over OS / sidecar / custom runtime?
│   └── → AKS (Kubernetes; serious operational investment)
├── Standard web app (Node / Python / .NET / Java)?
│   ├── < 5 services, low traffic, want zero infra?
│   │   └── → App Service (Linux/Windows; managed PaaS)
│   ├── Need autoscale to zero + container runtime?
│   │   └── → Container Apps (KEDA-based; sweet spot for microservices)
│   └── Need true serverless / event-driven?
│       └── → Functions (Premium for VNet/always-warm; Consumption for cheap+bursty)
├── Batch / job processing?
│   └── → Container Apps Jobs OR Batch (HPC-scale)
└── Long-running stateful processes / legacy?
    └── → VMs / VMSS

Stateful service (DBs you self-manage)?
├── → Generally prefer managed: SQL DB, Cosmos, PG Flexible
├── Or VM + your own DB (rarely the right call)

ML inference?
├── Realtime, GPU?
│   └── → AKS (GPU node pools) OR Azure ML managed endpoints
└── Batch?
    └── → Azure ML pipelines OR Container Apps Jobs

Static frontend?
└── → Static Web Apps (auto SSL, GitHub/Bitbucket deploy)

API gateway?
├── In-VNet, internal-only?
│   └── → Application Gateway
├── Global edge, custom routing, WAF?
│   └── → Front Door
├── API management (rate limit, dev portal, monetization)?
│   └── → API Management
```

See `azure-services-reference.md` for service-by-service depth: pricing tiers, SLAs, limits, when to upgrade.

## Data store decision tree

```
Relational?
├── Standard OLTP, low-to-medium scale?
│   └── → Azure SQL Database (Single DB; serverless tier for spiky)
├── Want PostgreSQL specifically?
│   └── → Azure Database for PostgreSQL Flexible Server
├── Want MySQL specifically?
│   └── → Azure Database for MySQL Flexible Server
├── Multi-region with high concurrency, global reads?
│   └── → Cosmos DB (PostgreSQL or NoSQL API)

Document / NoSQL?
├── Global distribution, multiple consistency models, multi-region writes?
│   └── → Cosmos DB
├── Single-region key-value at scale?
│   └── → Azure Table Storage (cheap) OR Cosmos DB (Table API)

Key-value cache?
└── → Azure Cache for Redis (Standard for HA, Premium for VNet/persistence)

Blob / object storage?
└── → Storage Account (Blob); pick Hot / Cool / Cold / Archive tier per access pattern

Time-series / metrics?
├── Operational (low cost, queryable)?
│   └── → Azure Monitor Logs (Log Analytics workspace)
├── Application time series?
│   └── → Azure Data Explorer (Kusto) — purpose-built

Search?
└── → Azure AI Search (formerly Cognitive Search) — managed Lucene-based

Vector / embeddings?
├── Same workload as existing Cosmos / SQL DB?
│   └── → Cosmos DB (vector search support) OR Azure SQL DB (vector type)
└── Dedicated vector search?
    └── → Azure AI Search (vector indexes)

Data warehouse?
├── < 10TB, occasional queries?
│   └── → Azure SQL Database (DTU/vCore high tier) OR Synapse Serverless
└── > 10TB, analytical workloads?
    └── → Azure Synapse Analytics (Dedicated Pool) OR Microsoft Fabric
```

## Networking patterns

### Three core building blocks

| Component | What it does | When |
|-----------|--------------|------|
| **Virtual Network (VNet)** | L3 isolation; private IP space; subnets | Every non-trivial Azure deployment |
| **Private Endpoint** | Brings Azure PaaS services into your VNet via private IP | Default for production access to PaaS (Storage, SQL, etc.) |
| **Service Endpoint** | Lower-cost predecessor to Private Endpoint; restricts access to your VNet | Cost-sensitive, lower-security workloads only |

### Gateway services

| Service | Use when |
|---------|----------|
| **Application Gateway (v2)** | L7 LB inside VNet; WAF; OWASP rules; private + public modes; not global |
| **Front Door** | Global L7; multi-region routing; WAF at edge; CDN; URL-based routing |
| **Azure Firewall** | L3-L4-L7 stateful; egress filtering with FQDN allowlists |
| **NAT Gateway** | Predictable outbound IP for VNet egress; replaces SNAT exhaustion concerns |
| **VPN Gateway / ExpressRoute** | On-prem connectivity (S2S VPN cheaper; ER private + faster) |

### Common networking patterns

| Pattern | What | When |
|---------|------|------|
| **Hub-and-spoke** | Central hub VNet with shared services (firewall, ER, AD DS), peered with workload-specific spoke VNets | Multi-team / multi-workload orgs |
| **VWAN** | Microsoft-managed hub network simplifying multi-region + on-prem | When hub-spoke complexity gets painful |
| **Private Link for everything** | Every PaaS access via Private Endpoint; no public endpoints | Default for production / regulated workloads |
| **Azure Front Door + AppGw** | Global edge (AFD) → regional WAF/L7 (AGW) → backend | High-traffic global apps |

## Identity patterns

### Entra ID, Managed Identity, RBAC

| Concept | Use |
|---------|-----|
| **Microsoft Entra ID** (formerly Azure AD) | Identity provider for users, groups, apps |
| **Service Principal** | Identity for an app; has a secret or cert |
| **Managed Identity** | Service Principal whose lifecycle is tied to an Azure resource; no secrets |
| **System-assigned Managed Identity** | One per resource; deleted when resource is deleted |
| **User-assigned Managed Identity** | Independent lifecycle; can attach to multiple resources |
| **Workload Identity (AKS)** | Federated identity for K8s pods; no secret mounting |

### Choosing identity

```
Service running in Azure that calls other Azure services?
├── Single Azure resource → System-assigned MI
├── Multiple resources sharing identity (e.g., a pool of VMSS instances) → User-assigned MI
├── K8s pod → AKS Workload Identity
└── External app (CI/CD, on-prem) → Service Principal with cert (NOT secret)

Service calling external API (non-Azure)?
└── Service Principal OR app secret in Key Vault, accessed via MI

User-facing auth?
└── Entra ID with OIDC; B2C if customer-facing identity
```

### RBAC scopes (least privilege)

Assign RBAC at the smallest necessary scope:

| Scope | When |
|-------|------|
| Resource | Most specific; preferred default |
| Resource group | When the role applies to a logical group |
| Subscription | Only for subscription-wide admins |
| Management group | Cross-subscription enterprise governance |

Use built-in roles when they exist (Reader, Contributor, Storage Blob Data Reader, etc.). Custom roles only when truly needed.
