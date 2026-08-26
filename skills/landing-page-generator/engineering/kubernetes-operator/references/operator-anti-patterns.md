# Operator Anti-patterns

Catalog of common operator design and implementation mistakes, each with: symptoms (how to spot it), root cause, real-world consequences, and concrete fixes. Use during operator design review, code review, and pre-production audit.

---

## How to use this catalog

Pair with `scripts/reconciliation_audit.py` for automated detection of the static-analyzable ones. The behavioral / design ones require human review.

Severity legend:
- **P0** — operator may corrupt data, lose state, or cause cascading failures
- **P1** — operator works but creates operational pain (leaks, surprises, debug nightmares)
- **P2** — design smell; not actively harmful but limits evolution

---

## Anti-pattern 1: Status writes spec fields

**Severity:** P0

**Symptom:** The CRD defines `spec.replicas`, and the controller writes back to `spec.replicas` based on observed pod count.

**Root cause:** Engineer confused "what user asked for" with "what is currently true."

**Consequences:**
- Reconcile loops forever (controller writes spec, K8s sees spec change, controller reconciles, writes again)
- User's desired state is overwritten by observation
- HPA / scaler can't function
- Spec history (`kubectl get ... -o yaml -w`) shows nonsense

**Fix:** Move observed values to status. Controller writes spec **never** (except possibly to add a finalizer or owner-injected metadata — and even those changes typically don't trigger reconcile because they don't change `generation`).

---

## Anti-pattern 2: No finalizer + external resources

**Severity:** P0

**Symptom:** Controller creates resources outside K8s (cloud database, DNS record, S3 bucket, IAM role) but has no finalizer on the CR.

**Root cause:** Engineer thought K8s garbage collection handles it. K8s GC only handles K8s objects.

**Consequences:**
- User deletes the CR; cloud resources leak
- Cost grows; security surface grows
- After enough leaks, accountability problem ("who created this database in our account?")

**Fix:** Add a finalizer. On CR delete (`metadata.deletionTimestamp != nil`), the controller deletes external resources, then removes the finalizer. Only then does K8s GC complete the delete.

See [controller-runtime-patterns.md](controller-runtime-patterns.md) for the finalizer pattern.

---

## Anti-pattern 3: Finalizer that can never complete

**Severity:** P0

**Symptom:** Finalizer logic depends on a service that may be down or a state that may not be reachable. User tries to delete CR; it hangs forever.

**Root cause:** No max-retry / max-age on finalizer logic.

**Consequences:**
- User can't delete the CR
- Manual recovery (`kubectl patch ... finalizers: []`) leaves leaked external resources
- Operators on call get woken up at 3am to manually edit finalizers

**Fix:** Add a max-retry / max-age (e.g., 30 minutes). After timeout, log a loud warning, write a status condition `CleanupFailed: true`, remove the finalizer anyway. Note for the user: "external cleanup may be incomplete; investigate."

---

## Anti-pattern 4: No leader election with multiple replicas

**Severity:** P0

**Symptom:** Operator deployment has `replicas: 3`, but no `--enable-leader-election` flag (or `LeaderElection: false` in manager options).

**Root cause:** Engineer ran HA replicas for availability but didn't configure leader election to serialize reconciliation.

**Consequences:**
- All replicas reconcile every event simultaneously
- Conflict on status updates (one wins, others retry)
- Status flapping (each replica sees slightly different observed state)
- External resources created multiple times
- Quotas hit faster than expected

**Fix:** Enable leader election:

```go
mgr, _ := ctrl.NewManager(cfg, ctrl.Options{
    LeaderElection:          true,
    LeaderElectionID:        "myop.example.com",
    LeaderElectionNamespace: "myop-system",
})
```

---

## Anti-pattern 5: Tight loop on error

**Severity:** P0

**Symptom:** Reconcile returns `err` for every reconcile when the underlying issue is permanent (bad spec, missing dependency). Controller-runtime backoff caps eventually, but at peak rate the operator burns CPU and floods logs.

**Root cause:** Permanent errors treated the same as transient.

**Consequences:**
- CPU pegged
- Logs unreadable (millions of identical errors)
- API server load (each retry is a fetch + status update)

**Fix:** Distinguish transient vs permanent. For permanent: write status condition, **don't** return error (return `ctrl.Result{}, nil`). User edits spec → new generation → reconcile triggered with corrected input.

```go
if isPermanent(err) {
    // record on status; do not requeue
    db.Status.Phase = "BadSpec"
    meta.SetStatusCondition(&db.Status.Conditions, metav1.Condition{
        Type: "Available", Status: "False", Reason: "InvalidSpec", Message: err.Error(),
    })
    return ctrl.Result{}, r.Status().Update(ctx, db)
}
return ctrl.Result{}, err  // transient: requeue with backoff
```

---

## Anti-pattern 6: Reconcile creates resources without OwnerReference

**Severity:** P1

**Symptom:** Controller creates a Deployment / StatefulSet / Service for a CR, but doesn't set OwnerReference.

**Root cause:** Engineer used `r.Create(ctx, sts)` directly without `controllerutil.SetControllerReference(...)`.

**Consequences:**
- When CR is deleted, children survive (orphaned)
- Garbage collection can't trace ownership
- Cleanup requires manual intervention or post-hoc scripts

**Fix:**
```go
if err := controllerutil.SetControllerReference(parent, child, r.Scheme); err != nil {
    return fmt.Errorf("set owner ref: %w", err)
}
// then create/apply child
```

---

## Anti-pattern 7: Spec array field that's appended-to instead of set

**Severity:** P1

**Symptom:** CR has `spec.replicas: []ReplicaSpec`; controller logic does `db.Spec.Replicas = append(db.Spec.Replicas, ...)`.

**Root cause:** Misunderstood reconcile as "diff and patch" instead of "compute desired and set."

**Consequences:**
- Each reconcile appends; array grows unbounded
- Eventually exceeds etcd object size limit (~1.5MB)
- Updates fail; users can't modify CR

**Fix:** Compute the desired full array on every reconcile and set it. Never append to a spec field.

```go
desired := computeReplicasFromSpec(db.Spec.Template)
db.Spec.Replicas = desired  // set, don't append
```

(Note: writing to spec from the controller is itself an anti-pattern unless absolutely required. Usually this pattern means the data should be in status.)

---

## Anti-pattern 8: Cross-CR coupling without watches

**Severity:** P1

**Symptom:** Controller A reads from CR B (e.g., Database references a CredentialsSecret managed by another operator). But A doesn't watch B. When B changes, A doesn't re-reconcile until something else triggers it.

**Root cause:** Engineer didn't wire `Watches(...)` for the cross-CR dependency.

**Consequences:**
- Stale references; user updates B and expects A to react; nothing happens
- Manual `kubectl annotate database/foo trigger=$RANDOM` to force reconcile
- Confusing debug experience

**Fix:**

```go
return ctrl.NewControllerManagedBy(mgr).
    For(&v1.Database{}).
    Watches(
        &corev1.Secret{},
        handler.EnqueueRequestsFromMapFunc(r.findDatabasesForSecret),
    ).
    Complete(r)
```

With an indexer for fast lookup.

---

## Anti-pattern 9: Wide RBAC

**Severity:** P1 (production); P0 (security audit)

**Symptom:** Operator has `cluster-admin` ClusterRoleBinding, or RBAC with `verbs: ["*"]` on `resources: ["*"]`, or namespace-scoped operator with cluster-wide permissions.

**Root cause:** Convenience during early development; never tightened.

**Consequences:**
- Compromised operator = compromised cluster
- Audit findings; can't pass security review
- Blast radius of any controller bug is everything

**Fix:** Enumerate exactly the verbs and resources needed. Use namespace-scoped Role + RoleBinding when the operator only manages its own namespace. Cluster-scoped only when truly needed.

`scripts/reconciliation_audit.py` flags wide RBAC patterns.

---

## Anti-pattern 10: No status conditions

**Severity:** P1

**Symptom:** CRD has `status.phase: string` and nothing else.

**Root cause:** Status was an afterthought; phase string seemed sufficient.

**Consequences:**
- User has no way to tell why a CR is failing
- Tools that integrate with operators (dashboards, alerts) can't reason about partial degradation
- Debugging requires logs (not always accessible)

**Fix:** Use the K8s convention `conditions` array. At minimum: `Available`, `Progressing`, `Degraded`. Each with status (True/False/Unknown), reason, message, lastTransitionTime.

```go
meta.SetStatusCondition(&db.Status.Conditions, metav1.Condition{
    Type:               "Available",
    Status:             metav1.ConditionFalse,
    Reason:             "WaitingForStorage",
    Message:            "PVC pending; storage class not ready",
    ObservedGeneration: db.Generation,
})
```

---

## Anti-pattern 11: Missing observedGeneration

**Severity:** P1

**Symptom:** Status doesn't track `observedGeneration`. User edits spec; can't tell whether the operator has noticed.

**Root cause:** Forgotten; not in original status design.

**Consequences:**
- Users can't tell "did my change take effect, or is the operator slow?"
- Tooling that waits for changes can't tell when they've been applied
- Status of a stale generation is misleading

**Fix:**

```go
db.Status.ObservedGeneration = db.Generation
```

Set this at the end of every reconcile. Now users can `kubectl wait --for=jsonpath='{.status.observedGeneration}'=5 database/foo`.

---

## Anti-pattern 12: Operator that requires `kubectl edit` for normal operations

**Severity:** P1

**Symptom:** Routine operations (rotation, recovery, scaling beyond limits) require users to manually edit annotations, labels, or fields not exposed in the spec.

**Root cause:** Operator design didn't capture the full operational lifecycle.

**Consequences:**
- Users develop wiki of edits required
- GitOps workflows break (edits aren't in version control)
- Eventually defeats the declarative API

**Fix:** Every routine operation gets a spec field. If users need to manually intervene, that's a missing feature.

---

## Anti-pattern 13: Operator that mutates Pods directly

**Severity:** P1

**Symptom:** Controller does `r.Patch(ctx, &pod, ...)` to modify a Pod owned by a StatefulSet/Deployment.

**Root cause:** Operator wanted to set a Pod-level annotation, env var, or change without going through the Deployment.

**Consequences:**
- StatefulSet/Deployment reconciler reverts the change
- Race condition: operator writes; deployment-controller overwrites; loop
- Surprising behavior; Pod doesn't match its parent's template

**Fix:** Modify the parent (Deployment / StatefulSet / DaemonSet) template. Let the K8s built-in controllers replicate to Pods.

---

## Anti-pattern 14: Reconcile reads its own previous writes

**Severity:** P1

**Symptom:** Controller writes to status, then immediately re-fetches the CR and reads status. Sees stale (pre-write) value.

**Root cause:** Eventual consistency between API server cache and writes. Reads via the controller-runtime cache aren't immediately consistent with writes.

**Consequences:**
- Decisions based on stale state; incorrect behavior on next reconcile
- Reconciles may flip-flop

**Fix:** Compute and store the final state in local variables; don't rely on re-reading. Or read with `r.APIReader.Get(...)` (uncached) — slower but consistent.

---

## Anti-pattern 15: Operator-version baked into CRD

**Severity:** P2

**Symptom:** CRD includes operator-implementation details in user-facing fields (e.g., `spec.helmChartVersion: 1.2.3`).

**Root cause:** Implementation leaked into the API.

**Consequences:**
- Can't change implementation without breaking API
- Users have to know about your internals

**Fix:** Spec describes user intent in user terms. Operator chooses the implementation. If users need to influence the implementation, name the field after the user-facing concept (e.g., `spec.optimization: "throughput"`), not the implementation detail.

---

## Anti-pattern 16: Idempotency violated by side effects

**Severity:** P1

**Symptom:** Reconcile sends an email / creates a billing event / increments a metric on every run, not just on state transitions.

**Root cause:** Engineer thought reconcile runs once per "change"; it actually runs many times.

**Consequences:**
- Duplicate emails; duplicate billing
- Metrics inflated
- User-visible weirdness

**Fix:** Track state of side effects in status (or annotations). Only fire side effect on transition. Pattern:

```go
if !meta.IsStatusConditionTrue(db.Status.Conditions, "WelcomeEmailSent") {
    if err := sendWelcomeEmail(db); err != nil { ... }
    meta.SetStatusCondition(&db.Status.Conditions, metav1.Condition{
        Type: "WelcomeEmailSent", Status: "True", Reason: "Sent",
    })
    r.Status().Update(ctx, db)
}
```

---

## Anti-pattern 17: Operator with one giant reconcile function

**Severity:** P2

**Symptom:** `Reconcile()` is 600 lines, switches on every phase, every condition, mixed concerns.

**Root cause:** Grew organically; never refactored.

**Consequences:**
- Hard to test (every test exercises everything)
- Hard to change (every change risks unrelated behavior)
- Hard to read

**Fix:** Decompose. Strategies:

- Sub-controllers per concern (one for StatefulSet, one for backups, one for network policies)
- Phase handler functions per phase: `func (r *R) handleBootstrap(...)`, `handleRunning(...)`, etc.
- Extract pure-function builders for desired-state objects
- Keep `Reconcile` itself as a dispatcher: fetch → handle delete → call sub-reconcilers → update status

---

## Anti-pattern 18: Operator that requires being deployed in a specific namespace

**Severity:** P2

**Symptom:** Operator code does `r.Get(ctx, client.ObjectKey{Namespace: "my-operator-system", Name: "config"}, &cm)` — hardcoded.

**Root cause:** Convenience.

**Consequences:**
- Operator can't be installed elsewhere
- Multi-tenant clusters that want one operator per tenant can't
- Test isolation harder

**Fix:** Read own namespace from environment or service-account token. Don't hardcode.

---

## Anti-pattern 19: CRD with `x-kubernetes-preserve-unknown-fields: true`

**Severity:** P2 (P1 in some contexts)

**Symptom:** CRD schema has `x-kubernetes-preserve-unknown-fields: true` at the top of spec.

**Root cause:** Engineer wanted to "accept any structure" or was migrating an old CRD.

**Consequences:**
- API server doesn't validate the spec structure
- Typos in spec are silently accepted ("replcas: 3" — typo, ignored)
- Auto-generated clients can't infer types

**Fix:** Define the full structural schema. If you genuinely need polymorphic data, model it explicitly (oneOf with discriminator, or a small set of typed alternatives).

---

## Anti-pattern 20: Operator that pegs the K8s API server

**Severity:** P1

**Symptom:** Operator polls (instead of watches), or lists all resources without selectors, or reconciles too aggressively without caching.

**Root cause:** Educational gap — controller-runtime's defaults are usually right but can be misused.

**Consequences:**
- API server CPU pegged
- etcd request rate high
- Other controllers slowed
- In extreme cases, control plane outage

**Fix:**
- Use watches (`For(...)`, `Owns(...)`, `Watches(...)`) — controller-runtime sets this up by default. Don't write your own polling loop.
- Use label selectors and field selectors on lists.
- Use indexers for fast lookups.
- Cache by default; only use `APIReader` (uncached) when consistency demands it.

---

## Anti-pattern 21: Operator that depends on its own webhook for normal operation

**Severity:** P1

**Symptom:** Operator's mutation/validation webhook is part of the create flow; if the webhook is down, no resources can be created — including the operator's own pods after upgrade.

**Root cause:** Webhook treated as nice-to-have, deployed in same Deployment as the operator, with no failure-mode planning.

**Consequences:**
- Upgrade order: webhook down → operator up → operator can't reconcile its own pods → cluster stuck
- Cluster-wide impact if the webhook is on a common resource type
- Recovery requires manually editing `MutatingWebhookConfiguration` to skip the webhook

**Fix:**
- Set `failurePolicy: Ignore` for non-critical webhooks (admit even if webhook is down)
- For critical webhooks, ensure HA + zero-downtime upgrade
- Exclude `kube-system` (and your own operator's namespace) from webhook scope
- Have a documented recovery procedure for "operator stuck, webhook is the cause"

---

## Anti-pattern 22: Operator that doesn't honor `imagePullPolicy`

**Severity:** P2

**Symptom:** Operator hardcodes container images (versions, registries) instead of accepting them via spec or values.

**Root cause:** Convenience.

**Consequences:**
- Air-gapped / private-registry users can't run the operator
- Image upgrades require operator upgrade
- Mismatch between operator and operated component when versions don't line up

**Fix:** Accept image versions in spec (e.g., `spec.version: "14.10"` mapped to `postgres:14.10`). Accept registry overrides via operator-level config. Document the mapping.

---

## Anti-pattern 23: Operator with no upgrade story

**Severity:** P1

**Symptom:** Upgrading the operator requires `kubectl apply` of new manifests and... that's it. No migration path for existing CRs to a new schema. No rollback plan.

**Root cause:** Engineer focused on the initial deployment.

**Consequences:**
- v0.2 operator can't read v0.1 CRs (schema mismatch)
- Users stuck on old operator
- Rollback is impossible (CRD schema can't be downgraded once changed)

**Fix:**
- Versioned CRDs with conversion webhooks
- Documented upgrade and rollback procedures
- Smoke tests of upgrades in CI
- Storage version migrator for major schema changes

---

## Anti-pattern 24: Status fields with PII or secrets

**Severity:** P0

**Symptom:** Operator writes the database password / API key / customer name into `status.password` for convenience.

**Root cause:** Status was treated as a scratchpad.

**Consequences:**
- Anyone with `get` permission on the CR sees the secret
- `kubectl get -o yaml | git commit` exposes it
- Audit logs leak it

**Fix:** Never put secrets or PII in status. References to Secrets, yes. The Secret values themselves, never.

---

## Detection summary (for audit)

| Anti-pattern | Static-detectable? | How |
|--------------|--------------------|-----|
| Status writes spec | Partial | Grep for `r.Update(... db)` after status field writes |
| No finalizer | Yes | Search controller code; if creates external resources but no finalizer, flag |
| Finalizer can never complete | No | Behavioral; design review only |
| No leader election with replicas > 1 | Yes | Read Deployment manifest + manager options |
| Tight loop on error | Partial | Look for unconditional `return ctrl.Result{}, err` without error classification |
| No OwnerReference | Yes | Grep for `r.Create` / `r.Apply` without preceding `SetControllerReference` |
| Spec array appended | Partial | AST analysis; look for `append(... .Spec.Something, ...)` |
| Cross-CR coupling without watch | Yes | Read `SetupWithManager` for missing `Watches` |
| Wide RBAC | Yes | Read kubebuilder markers / generated YAML |
| No status conditions | Yes | Read CRD schema |
| Missing observedGeneration | Yes | Grep for `ObservedGeneration` in status update paths |
| Mutates Pods directly | Yes | Grep for `r.Patch(... pod` |
| Reconcile is too long | Yes | Function line-count threshold |
| Hardcoded namespace | Yes | Grep for hardcoded namespace strings in `Get/List` calls |
| Preserve-unknown-fields | Yes | Read CRD schema |
| Operator depends on own webhook | Partial | Read MutatingWebhookConfiguration scope |
| Hardcoded images | Yes | Grep for image strings without spec/config indirection |
| Secrets in status | No | Behavioral; review status update sites |

`scripts/reconciliation_audit.py` automates the static-detectable ones.

---

## Quick triage by symptom

| Symptom | Likely anti-pattern |
|---------|---------------------|
| Reconcile loops forever | #1 (status writes spec) or #15 (op-version baked in) |
| User can't delete CR | #3 (finalizer can never complete) |
| Multiple resources created | #4 (no leader election) or #16 (idempotency violated) |
| Cloud resources leak | #2 (no finalizer) |
| CR doesn't react to changes | #8 (no cross-CR watch) |
| Reconcile floods logs with errors | #5 (tight loop on error) |
| Stale state in status | #14 (cache eventual consistency) |
| Operator can't be moved namespaces | #18 (hardcoded namespace) |
| Sec audit blocked | #9 (wide RBAC) or #24 (secrets in status) |
| Upgrade broke everything | #23 (no upgrade story) or #21 (webhook dep) |

---

## Quick anti-pattern checklist (skill-body summary)

- **Status fields in spec.** User writes "phase: Running", operator never overrides — chaos. Status is operator-only.
- **No finalizer + external resources.** User deletes CR, cloud resources leak.
- **No leader election + multiple replicas.** Two controllers race; status flaps.
- **Tight loop on error.** Reconcile returns error, K8s requeues immediately, infinite spin. Always backoff.
- **Reconcile creates resources directly with name = CR name (no ownerRef).** Garbage collection won't clean up; orphaned resources accumulate.
- **Spec field is array; controller appends instead of setting.** Each reconcile grows the array; eventually hits etcd object size limit.
- **Cross-CR coupling without watchers.** Controller for A reads B; if B changes, A doesn't reconcile until something else triggers it.
- **Wide RBAC.** `cluster-admin` for convenience; massive blast radius.
- **No status conditions.** User has no way to tell why a CR is failing.
- **Operator that requires `kubectl edit` for normal operations.** Defeats the declarative API.
- **No observed generation.** User can't tell if their spec change has been processed.
- **Operator that mutates Pods directly.** Bypasses StatefulSet/Deployment semantics; gets very confusing very fast.
