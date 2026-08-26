# Networking & Identity Patterns

Read this when designing VPC topology, choosing a load balancer, picking a connectivity pattern, or setting up IAM / Service Accounts / Workload Identity Federation correctly.

## Networking patterns

### Three core building blocks

| Component | What it does | When |
|-----------|--------------|------|
| **VPC** | L3 isolation; private IP space; global by default in GCP | Every non-trivial GCP deployment |
| **Private Service Connect (PSC)** | Brings managed services into your VPC privately | Default for production access to managed services |
| **Cloud Interconnect / VPN** | On-prem connectivity (Interconnect is dedicated; VPN is over internet) | Hybrid setups |

### Load balancers

| LB | When |
|----|------|
| **Global External HTTP(S) Load Balancer** | Global anycast; Cloud Armor; CDN; serverless backends |
| **Regional External HTTP(S) LB** | Regional only; cheaper for non-global workloads |
| **Internal HTTP(S) LB** | Internal services; supports serverless backends |
| **TCP/UDP Network LB** | L4 load balancing; lower cost; for non-HTTP workloads |
| **Internal TCP/UDP LB** | Internal L4 |

### Common networking patterns

| Pattern | What | When |
|---------|------|------|
| **Shared VPC** | Central host project owns VPC; service projects attach their resources | Enterprise / multi-team |
| **VPC peering** | Connect two VPCs (transitive routing not supported) | Multi-project organizations |
| **Private Service Connect** | Consumer endpoint in your VPC → producer service | Default for managed services |
| **Cloud Armor + global LB** | DDoS protection + WAF rules at the edge | Public-facing apps |
| **Hub-and-spoke via Network Connectivity Center** | Centralized routing for multi-VPC orgs | Large orgs |

## Identity patterns

### IAM, Service Accounts, Workload Identity Federation

| Concept | Use |
|---------|-----|
| **Cloud IAM** | Role-based access control for users, groups, service accounts |
| **Service Account (SA)** | Identity for an app or workload |
| **Service Account Key** | Static credential for SA — avoid in modern setups |
| **Workload Identity Federation** | Federated identity; on-prem / other-cloud workloads get GCP access without keys |
| **Workload Identity (GKE)** | K8s service accounts mapped to GCP SAs; no key mounting in pods |
| **Application Default Credentials (ADC)** | Standard library for auth; uses ambient credentials |

### Choosing identity

```
Workload running on GCP that calls other GCP services?
├── On GKE → GKE Workload Identity (KSA → GSA)
├── On Cloud Run / Functions → service identity (built-in)
├── On Compute Engine → instance service account
└── In a CI/CD pipeline outside GCP → Workload Identity Federation (no keys)

Workload outside GCP needing GCP access?
├── From AWS / Azure / OIDC provider → Workload Identity Federation
└── Last resort → Service Account key (rotate frequently)

User-facing auth?
└── Identity Platform (GCP's auth-as-a-service; or Firebase Auth for client-direct)
```

### Least-privilege IAM

GCP supports three forms:
- **Predefined roles** (e.g., `roles/storage.objectViewer`) — preferred
- **Custom roles** at organization or project — when predefined doesn't fit
- **Basic roles** (`owner`, `editor`, `viewer`) — too broad; avoid in production

Bind roles at the most specific scope:
- Resource → preferred
- Project → standard for project-scoped apps
- Folder → for organizational sub-tree
- Organization → only org-wide admins
