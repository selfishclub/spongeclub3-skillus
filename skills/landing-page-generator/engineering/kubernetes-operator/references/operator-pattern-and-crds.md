# Operator Pattern and CRDs

Deep reference on the Kubernetes operator pattern, CRD schema design, versioning strategy, conversion webhooks, the status subresource, and how K8s API conventions apply to custom resources.

---

## The operator pattern, expanded

An operator is the codification of a human operator's runbook as a Kubernetes-native software component. Where SREs once wrote "to scale the database, do X, then Y, then Z," an operator does it automatically when the user changes `spec.replicas`.

The pattern was named at CoreOS (2016) but instantiates an older idea: **the controller pattern** — control loops watching desired state, driving observed state to match. Kubernetes is itself built from controllers (ReplicaSet, Deployment, StatefulSet, Service, Ingress, etc.).

An operator adds three things on top of vanilla controllers:

1. **Domain knowledge.** It encodes "how to operate this specific kind of thing."
2. **Custom Resource Definition (CRD).** It extends the Kubernetes API with new types.
3. **Reconciliation across complex state machines.** Often dealing with stateful, multi-step, error-prone lifecycles.

---

## Resource model: spec / status / metadata

Every Kubernetes resource — including custom ones — has three top-level fields:

| Field | Owner | Purpose |
|-------|-------|---------|
| `metadata` | Mostly user (name, labels, annotations); some K8s-managed (uid, resourceVersion, generation) | Identity, ownership, tracking |
| `spec` | User-controlled | Desired state |
| `status` | Operator-controlled | Observed state |

The discipline: **spec is the contract between user and operator; status is the operator's report.** Mixing them creates ambiguity (whose source of truth is it?), reconciliation loops (operator writes spec → spec change triggers reconcile → operator writes spec again), and confusion for users.

---

## CRD essentials

A CRD is itself a Kubernetes resource. You apply it like any YAML manifest; once it's applied, the API server exposes a new endpoint for the custom resource type.

### Minimal CRD

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: databases.example.com
spec:
  group: example.com
  names:
    kind: Database
    plural: databases
    singular: database
    shortNames: [db]
    categories: [all]
  scope: Namespaced
  versions:
    - name: v1alpha1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                version: { type: string }
                storage: { type: string }
                replicas: { type: integer, minimum: 1, maximum: 7 }
            status:
              type: object
              properties:
                phase: { type: string }
      subresources:
        status: {}
      additionalPrinterColumns:
        - name: Phase
          type: string
          jsonPath: .status.phase
        - name: Version
          type: string
          jsonPath: .spec.version
        - name: Age
          type: date
          jsonPath: .metadata.creationTimestamp
```

### Required vs nice-to-have

| Element | Required? | Why |
|---------|-----------|-----|
| `group` | Yes | Namespaces your API; pick a domain you own (`example.com`, not `kubernetes.io`) |
| `version[*]` | Yes | At least one served version |
| `names` (kind, plural, singular) | Yes | How the resource is identified |
| `scope` | Yes | Namespaced vs Cluster |
| `schema.openAPIV3Schema` | Yes (effective requirement) | Without schema, the API server can't validate |
| `subresources.status` | Highly recommended | Cleaner separation, fewer reconcile loops |
| `additionalPrinterColumns` | Recommended | `kubectl get` becomes useful |
| `categories` | Optional | Enables `kubectl get all,<category>` |
| `shortNames` | Optional | UX win for users |
| `validation rules (x-kubernetes-validations)` | When needed | Cross-field validation without webhook |
| `conversion webhook` | When > 1 served version | Translates between versions |

---

## Schema design

### Spec field design principles

1. **Each spec field maps to a real user decision.** If users don't have an opinion, default it; don't expose the field.
2. **Use enums for discrete choices.** `enum: ["small", "medium", "large"]` beats free-form string.
3. **Validate at the boundary.** required, enum, pattern, min/max, format — all enforced by API server before the operator ever sees the request.
4. **Avoid optional structures that change everything.** A nested `spec.advanced.legacyMode: true` that flips half the controller logic is a maintenance nightmare.
5. **Stable IDs.** Once a field exists in a served version, you can rename only with a conversion webhook.
6. **Descriptions matter.** They appear in `kubectl explain`, which is documentation users actually consult.

Example with full validation:

```yaml
spec:
  type: object
  required: [version, storage, replicas]
  properties:
    version:
      type: string
      pattern: "^[0-9]+\\.[0-9]+(\\.[0-9]+)?$"
      description: |
        PostgreSQL major.minor version, e.g., "14.10" or "15.5".
    storage:
      type: string
      pattern: "^[0-9]+[GMK]i$"
      description: |
        Persistent storage size in Kubernetes resource notation
        (e.g., "100Gi"). Cannot be reduced after creation.
    replicas:
      type: integer
      minimum: 1
      maximum: 7
      default: 3
      description: |
        Number of database replicas. 1 = single-node (no HA).
        Odd numbers recommended for quorum (3, 5, 7).
    backup:
      type: object
      properties:
        enabled:
          type: boolean
          default: true
        schedule:
          type: string
          pattern: "^(\\*|[0-9,/-]+)(\\s+(\\*|[0-9,/-]+)){4}$"
          default: "0 2 * * *"
          description: Cron expression in UTC.
        retention:
          type: integer
          minimum: 1
          maximum: 365
          default: 30
          description: Days to retain backups.
```

### Cross-field validation with CEL

Kubernetes 1.25+ supports `x-kubernetes-validations` using Common Expression Language:

```yaml
spec:
  type: object
  properties:
    replicas: { type: integer }
    backup:
      type: object
      properties:
        enabled: { type: boolean }
        schedule: { type: string }
  x-kubernetes-validations:
    - rule: "!self.backup.enabled || size(self.backup.schedule) > 0"
      message: "If backup.enabled is true, backup.schedule is required."
    - rule: "self.replicas == 1 || self.replicas % 2 == 1"
      message: "Replicas must be 1 or an odd number for quorum."
```

CEL rules run at API admission time — fast, no webhook required.

### Status field design

Status reports current state. Three patterns:

#### 1. Phase string

Simple state machine; user reads at a glance.

```yaml
status:
  type: object
  properties:
    phase:
      type: string
      enum: [Pending, Bootstrapping, Running, Updating, Failed, Terminating]
```

Drawback: a single field encodes everything; can't express "running but degraded."

#### 2. Conditions array (recommended for complex resources)

K8s convention since core types (PodConditions, NodeConditions). Multiple orthogonal state dimensions.

```yaml
status:
  type: object
  properties:
    conditions:
      type: array
      items:
        type: object
        required: [type, status, lastTransitionTime, reason]
        properties:
          type: { type: string }
          status: { type: string, enum: ["True", "False", "Unknown"] }
          lastTransitionTime: { type: string, format: date-time }
          reason: { type: string }
          message: { type: string }
```

Common condition types: `Available`, `Progressing`, `Degraded`, `BackupReady`, `MigrationComplete`.

#### 3. Mixed (phase + conditions + observed values)

Use phase as a top-level summary, conditions for detail, plus observed values:

```yaml
status:
  phase: Running               # quick summary
  observedGeneration: 5        # so user knows spec was seen
  conditions:                  # detailed health
    - type: Available
      status: "True"
  endpoints:                   # operator-discovered facts
    primary: "..."
    replicas: ["..."]
  observedVersion: "14.10"     # what's actually running
  lastBackup: "2026-05-27T02:00:00Z"
```

---

## Versioning

Kubernetes API versioning is taken seriously because users build CI/CD on top of your API.

### Version names

| Stage | Name | Stability promise |
|-------|------|-------------------|
| Alpha | `v1alpha1`, `v1alpha2`, ... | Can break in any release; disabled by default in some installations; intended for early adopters |
| Beta | `v1beta1`, `v1beta2`, ... | Reasonably stable; breaking changes possible with one release deprecation period; enabled by default |
| Stable | `v1`, `v2`, ... | Long-term API guarantee; no breaking changes within same major version |

Most operators graduate `v1alpha1` → `v1beta1` → `v1` over 1-2 years.

### Multiple served versions

Once you have v1 alongside v1alpha1, both must be served simultaneously for a transition period. Pick a single **storage version**; all other served versions are converted on the fly.

```yaml
versions:
  - name: v1alpha1
    served: true
    storage: false
    schema: { ... }
  - name: v1
    served: true
    storage: true       # ← only one can be storage:true at a time
    schema: { ... }
```

### Conversion webhook

When schemas differ between versions, you need a conversion webhook. The API server calls your webhook when a user requests one version but storage is another.

```yaml
spec:
  conversion:
    strategy: Webhook
    webhook:
      conversionReviewVersions: ["v1"]
      clientConfig:
        service:
          namespace: my-operator-system
          name: my-operator-conversion-webhook
          path: /convert
```

The webhook receives objects in one version and returns them in another. Test conversion both directions thoroughly (round-trip).

### Deprecation

To remove a version:

1. Mark it `deprecated: true` in the CRD (shows warnings to users on get/list).
2. Wait at least one release.
3. Set `served: false` (no new reads/writes).
4. Wait at least one release.
5. Remove from the CRD entirely.

Don't skip the warning period. Users build automation; their tooling will break without notice.

---

## The status subresource

The `status` subresource is **the single most important production setting** for a CRD. Always enable it.

```yaml
subresources:
  status: {}
```

What it does:

1. **Separates RBAC.** Users can update `spec` without `status` permission. The operator updates `status` via a different endpoint.
2. **Prevents reconcile loops.** Updates to `status` do not increment `metadata.generation`. Without the subresource, every status write would look like a spec change.
3. **Atomic semantics.** Status updates use optimistic concurrency on `resourceVersion`, separately from spec.

The endpoint is `/apis/example.com/v1/namespaces/default/databases/foo/status` — accessed via the K8s client `Status().Update(...)` method.

---

## Printer columns

Without printer columns, `kubectl get database` shows only NAME and AGE. With them, you get a useful summary:

```yaml
additionalPrinterColumns:
  - name: Phase
    type: string
    jsonPath: .status.phase
  - name: Version
    type: string
    jsonPath: .spec.version
  - name: Replicas
    type: integer
    jsonPath: .spec.replicas
  - name: Available
    type: string
    jsonPath: .status.conditions[?(@.type=='Available')].status
  - name: Age
    type: date
    jsonPath: .metadata.creationTimestamp
```

Output:
```
NAME          PHASE     VERSION   REPLICAS   AVAILABLE   AGE
prod-orders   Running   14.10     3          True        14d
staging-test  Pending   14.10     1          False       2m
```

Add a `priority: 1` column to hide it from `kubectl get` default but show it with `-o wide`.

---

## Categories and `kubectl get all,<category>`

By default, `kubectl get all` returns the K8s built-in `all` category (Pods, Services, Deployments, ReplicaSets, StatefulSets, ...). Your CR doesn't show up.

Add it:

```yaml
names:
  categories:
    - all              # appears in `kubectl get all`
    - databases        # custom category; `kubectl get databases`
```

Use sparingly — `kubectl get all` cluster-wide can be very slow if many CRDs join `all`.

---

## RBAC for CRDs

When you apply a CRD, the API server doesn't auto-grant any permissions to it. You explicitly write RBAC:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: database-admin
rules:
  - apiGroups: ["example.com"]
    resources: ["databases"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
  - apiGroups: ["example.com"]
    resources: ["databases/status"]
    verbs: ["get", "update", "patch"]
  - apiGroups: ["example.com"]
    resources: ["databases/finalizers"]
    verbs: ["update"]
```

Note the three sub-resources: the main resource, `/status`, and `/finalizers`. All three need explicit RBAC.

For the operator itself, give it just what it needs to operate the resource (and its children). For users, give the main resource (often `get/list/watch/create/update/patch/delete`) but NOT `/status` or `/finalizers` (those are operator-only).

---

## Common CRD pitfalls

### Pitfall: Preserve-unknown-fields

```yaml
schema:
  openAPIV3Schema:
    type: object
    x-kubernetes-preserve-unknown-fields: true
```

Allows any structure; defeats the purpose of validation. Use only when modeling truly polymorphic data. Default to structural schemas (no preserve-unknown).

### Pitfall: Storage version mismatch

If you change storage version casually, the API server can't read old objects until they're rewritten. Use the `kube-storage-version-migrator` to perform safe migrations.

### Pitfall: Missing `required` fields

If a field is conceptually required, mark it `required:` in the schema. Otherwise users create resources with empty fields and the operator must defensively handle missing values everywhere.

### Pitfall: Wide-open string fields

A `type: string` with no `enum`, no `pattern`, no `format`, no length limit is a user-error magnet. Add constraints.

### Pitfall: Defaults that mutate

If you set a default, the API server fills it in on create. Subsequent reads see the default. Users who didn't specify the field can't tell they got the default — it looks like they did. For settings users should make explicit choices about, don't default.

### Pitfall: Spec field that's actually status

"observedReplicas" in spec is wrong; it's a status. "desiredReplicas" in status is wrong; it's spec (or derivable from spec). Each field has exactly one owner.

---

## Status conventions (from K8s API conventions)

Follow these for consistency with the broader K8s ecosystem:

- `status.observedGeneration` — equal to `metadata.generation` of the spec the operator last reconciled. Users can compare to detect "spec changed, operator hasn't caught up yet."
- `status.conditions` — array of structured condition objects (type, status, lastTransitionTime, reason, message).
- `status.phase` — high-level summary string, if used.
- `status.replicas` / `status.readyReplicas` — for scale subresource compatibility.

---

## The scale subresource

If your resource has a `spec.replicas` field, enable the `scale` subresource:

```yaml
subresources:
  scale:
    specReplicasPath: .spec.replicas
    statusReplicasPath: .status.replicas
    labelSelectorPath: .status.selector
```

Now `kubectl scale database/prod-orders --replicas=5` works. HPA can target your resource. Other K8s tooling that expects `scale` works.

---

## Summary checklist for a production CRD

- [ ] Group is a domain you own (not `kubernetes.io`, not `k8s.io`)
- [ ] Names: kind / plural / singular all set; consider shortNames + categories
- [ ] Scope: chosen deliberately (Namespaced default; Cluster only when global)
- [ ] At least one version, with explicit `served` and `storage`
- [ ] Full structural OpenAPI schema (no preserve-unknown unless necessary)
- [ ] `required` fields marked
- [ ] Enums on discrete fields
- [ ] Pattern / format / min / max on values
- [ ] Descriptions on every field (visible in `kubectl explain`)
- [ ] `x-kubernetes-validations` (CEL) for cross-field rules
- [ ] Sensible defaults only where appropriate
- [ ] `subresources.status: {}` enabled
- [ ] `subresources.scale` enabled if user-controlled replicas
- [ ] `additionalPrinterColumns` (at minimum: phase + age)
- [ ] Status uses `conditions` array (or phase) consistently
- [ ] `status.observedGeneration` tracked
- [ ] RBAC explicitly granted (CR + /status + /finalizers)
- [ ] Conversion webhook designed if planning multiple served versions
- [ ] Documented deprecation policy

---

## Reading

- Kubernetes API Conventions (the source of truth for status/conditions/etc.)
- CRD validation reference (OpenAPI v3 + CEL extensions)
- Kubebuilder book (uses controller-runtime; good intro)
- Operator-SDK docs (if OLM-focused)

---

## CRD design — the foundation (skill-body overview)

A bad CRD = perpetual operator pain. Spend time here.

### Required design decisions

| Decision | Options | Default |
|----------|---------|---------|
| Scope | Namespaced / Cluster | Namespaced (unless cluster-wide makes no sense without it) |
| Versioning | v1alpha1 / v1beta1 / v1 | Start v1alpha1, graduate per Kubernetes API conventions |
| Conversion | None / Webhook / None-with-storage-version | Webhook once you have > 1 served version |
| Subresources | status / scale / both | Always enable `status`; `scale` if user-controlled replicas |
| Validation | OpenAPI schema / admission webhook / both | OpenAPI for shape; webhook for cross-field |
| Printer columns | Yes (recommended) | Always — kubectl get is much nicer |
| Categories | Optional | Add for grouping (e.g., `kubectl get all,databases`) |
| Short names | Optional | Add (e.g., `db` for `Database`) |

### Spec / Status separation

**Spec** = what the user wants (desired state)
**Status** = what the operator observes (actual state)

The user writes Spec. The operator writes Status. Never the other way round.

```yaml
apiVersion: example.com/v1
kind: Database
metadata:
  name: prod-orders
spec:                          # user-owned
  version: "14.10"
  storage: 100Gi
  replicas: 3
  backup:
    schedule: "0 2 * * *"
status:                        # operator-owned
  phase: Running
  observedGeneration: 5
  conditions:
    - type: Available
      status: "True"
      reason: AllReplicasReady
      lastTransitionTime: "2026-05-27T08:00:00Z"
  endpoints:
    primary: prod-orders-primary.default.svc.cluster.local
    replicas: ["prod-orders-replica-0.default.svc.cluster.local"]
  observedVersion: "14.10"
```

### CRD schema rules

- **Use OpenAPI v3 schema**, structural (no `x-kubernetes-preserve-unknown-fields` unless you really need it)
- **Validate at the API edge** — required fields, enum values, format, regex pattern, min/max
- **Use defaults sparingly** — every default is something users can't tell the operator "I don't care, you decide"
- **Add descriptions** — they show up in `kubectl explain`, which is how users learn your API
- **Use `x-kubernetes-validations`** (CEL, K8s 1.25+) for cross-field validation that doesn't need a webhook
- **Version your API thoughtfully** — v1alpha1 can break; v1 is forever
