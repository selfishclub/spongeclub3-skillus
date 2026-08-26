# Controller-Runtime Patterns

Reference for building production controllers with Go's `controller-runtime` library — the foundation of Kubebuilder, operator-SDK, and most modern Kubernetes operators. Covers reconciliation patterns, error handling, finalizers, leader election, RBAC scoping, indexers, predicates, and the test patterns that catch real bugs before production.

---

## The reconciliation contract

Every controller implements:

```go
type Reconciler interface {
    Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error)
}
```

The contract:

| Input | Meaning |
|-------|---------|
| `req.NamespacedName` | The CR that changed |
| `ctx` | Cancellation + deadline + logger |

| Return | Meaning |
|--------|---------|
| `ctrl.Result{}, nil` | Done; no requeue |
| `ctrl.Result{Requeue: true}, nil` | Requeue immediately (use sparingly) |
| `ctrl.Result{RequeueAfter: 30 * time.Second}, nil` | Requeue after delay |
| `ctrl.Result{}, err` | Error; controller-runtime requeues with exponential backoff |

**Never** return both an error and Requeue:true — the error implies requeue with backoff already.

---

## Skeleton reconciler

```go
func (r *DatabaseReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := logf.FromContext(ctx)

    // 1. Fetch the CR
    var db v1.Database
    if err := r.Get(ctx, req.NamespacedName, &db); err != nil {
        // NotFound: object was deleted; nothing to reconcile
        if apierrors.IsNotFound(err) {
            return ctrl.Result{}, nil
        }
        return ctrl.Result{}, fmt.Errorf("fetch database: %w", err)
    }

    // 2. Handle deletion via finalizer
    if !db.DeletionTimestamp.IsZero() {
        return r.handleDelete(ctx, &db)
    }
    if !controllerutil.ContainsFinalizer(&db, dbFinalizer) {
        controllerutil.AddFinalizer(&db, dbFinalizer)
        if err := r.Update(ctx, &db); err != nil {
            return ctrl.Result{}, fmt.Errorf("add finalizer: %w", err)
        }
        return ctrl.Result{Requeue: true}, nil  // requeue with finalizer added
    }

    // 3. Reconcile children
    if err := r.reconcileStatefulSet(ctx, &db); err != nil {
        return r.failStatus(ctx, &db, "StatefulSetFailed", err)
    }
    if err := r.reconcileService(ctx, &db); err != nil {
        return r.failStatus(ctx, &db, "ServiceFailed", err)
    }
    if err := r.reconcileBackupCronJob(ctx, &db); err != nil {
        return r.failStatus(ctx, &db, "BackupFailed", err)
    }

    // 4. Update status
    return r.updateStatus(ctx, &db)
}
```

### Why each step matters

- **Step 1:** NotFound is the most common "error" (object deleted between watch event and reconcile). Don't propagate it.
- **Step 2:** Finalizer must be added before the CR can be deleted; check it first.
- **Step 3:** Each child resource ownership is its own concern; handle independently.
- **Step 4:** Always update status — failure or success.

---

## Idempotent resource creation pattern

Always use `CreateOrUpdate` or `Apply` semantics, never raw `Create`:

```go
// BAD: not idempotent
sts := buildStatefulSet(db)
if err := r.Create(ctx, sts); err != nil {
    return err  // fails on second reconcile because resource exists
}

// GOOD: idempotent
desired := buildStatefulSet(db)
op, err := controllerutil.CreateOrUpdate(ctx, r.Client, desired, func() error {
    // mutate `desired` here based on db.Spec
    desired.Spec.Replicas = ptr.To(db.Spec.Replicas)
    desired.Spec.Template.Spec.Containers[0].Image = imageFor(db)
    return nil
})
if err != nil {
    return fmt.Errorf("apply statefulset: %w", err)
}
log.V(1).Info("statefulset", "op", op)  // op = "created" / "updated" / "unchanged"
```

### Apply pattern (preferred for K8s 1.22+)

Server-Side Apply uses field-managers; multiple controllers can co-own different fields of the same object without fighting:

```go
sts := &appsv1.StatefulSet{
    ObjectMeta: metav1.ObjectMeta{
        Name:      db.Name,
        Namespace: db.Namespace,
    },
    Spec: buildStsSpec(db),
}
sts.Kind = "StatefulSet"
sts.APIVersion = "apps/v1"
if err := r.Patch(ctx, sts, client.Apply, client.FieldOwner("db-operator")); err != nil {
    return fmt.Errorf("apply statefulset: %w", err)
}
```

---

## Owner references for garbage collection

Every child resource should have an OwnerReference back to the parent CR. When the CR is deleted, K8s GC deletes the children automatically.

```go
desired := buildStatefulSet(db)
if err := controllerutil.SetControllerReference(db, desired, r.Scheme); err != nil {
    return fmt.Errorf("set owner ref: %w", err)
}
// then create/apply desired
```

`SetControllerReference` adds `controller: true` and `blockOwnerDeletion: true`, which is what you want for K8s-native lifecycle.

Anti-pattern: creating child resources without OwnerReference → orphaned children survive CR deletion.

---

## Status update patterns

### Update status as a separate call

```go
db.Status.Phase = "Running"
db.Status.ObservedGeneration = db.Generation
meta.SetStatusCondition(&db.Status.Conditions, metav1.Condition{
    Type:               "Available",
    Status:             metav1.ConditionTrue,
    Reason:             "AllReplicasReady",
    Message:            "All 3 replicas ready",
    ObservedGeneration: db.Generation,
})

if err := r.Status().Update(ctx, db); err != nil {
    return ctrl.Result{}, fmt.Errorf("update status: %w", err)
}
return ctrl.Result{}, nil
```

`r.Status().Update(...)` hits the `/status` subresource specifically. It doesn't bump `metadata.generation`, so it doesn't trigger reconcile.

### Patch status instead of update (less write contention)

```go
patch := client.MergeFrom(db.DeepCopy())
db.Status.Phase = "Running"
db.Status.ObservedGeneration = db.Generation
if err := r.Status().Patch(ctx, db, patch); err != nil {
    return ctrl.Result{}, fmt.Errorf("patch status: %w", err)
}
```

### Failure path

```go
func (r *DatabaseReconciler) failStatus(ctx context.Context, db *v1.Database, reason string, err error) (ctrl.Result, error) {
    db.Status.Phase = "Failed"
    meta.SetStatusCondition(&db.Status.Conditions, metav1.Condition{
        Type:               "Available",
        Status:             metav1.ConditionFalse,
        Reason:             reason,
        Message:            err.Error(),
        ObservedGeneration: db.Generation,
    })
    if updateErr := r.Status().Update(ctx, db); updateErr != nil {
        // Log but return the original error
        logf.FromContext(ctx).Error(updateErr, "failed to update status during error path")
    }
    return ctrl.Result{}, err  // controller-runtime requeues with backoff
}
```

---

## Finalizers

### Add on first reconcile

```go
if !controllerutil.ContainsFinalizer(db, dbFinalizer) {
    controllerutil.AddFinalizer(db, dbFinalizer)
    if err := r.Update(ctx, db); err != nil {
        return ctrl.Result{}, err
    }
    return ctrl.Result{Requeue: true}, nil
}
```

The Requeue forces a fresh fetch with the finalizer applied.

### Handle deletion

```go
func (r *DatabaseReconciler) handleDelete(ctx context.Context, db *v1.Database) (ctrl.Result, error) {
    log := logf.FromContext(ctx)
    if !controllerutil.ContainsFinalizer(db, dbFinalizer) {
        return ctrl.Result{}, nil  // already cleaned up
    }

    // 1. Cleanup external resources
    if err := r.cleanupCloudResources(ctx, db); err != nil {
        // Don't remove the finalizer — leave it for retry
        log.Error(err, "cleanup cloud resources")
        return ctrl.Result{RequeueAfter: 30 * time.Second}, nil
    }

    // 2. Remove the finalizer
    controllerutil.RemoveFinalizer(db, dbFinalizer)
    if err := r.Update(ctx, db); err != nil {
        return ctrl.Result{}, err
    }

    // 3. K8s will now garbage-collect the CR
    return ctrl.Result{}, nil
}
```

### Anti-pattern: finalizer that can never complete

If `cleanupCloudResources` depends on a service that's down, the finalizer hangs. User can't delete the CR. To recover, manually edit out the finalizer (`kubectl patch database/foo -p '{"metadata":{"finalizers":[]}}' --type=merge`).

Mitigation: add a max-retry / max-age. After N attempts, log loudly and remove the finalizer anyway (best-effort cleanup), with a status condition warning that external cleanup may have failed.

---

## Leader election

For HA, run the operator with multiple replicas. Without leader election, every replica reconciles every event → race conditions, status flapping, surprise.

```go
mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    LeaderElection:          true,
    LeaderElectionID:        "db-operator.example.com",
    LeaderElectionNamespace: "db-operator-system",
    // LeaderElectionReleaseOnCancel: true,  // release lease on graceful shutdown
})
```

Under the hood, controller-runtime uses a coordination.k8s.io/v1 Lease object. Only the holder reconciles; others sit idle (but ready to take over if the holder dies).

Trade-off: lease renewal latency adds 15-30 seconds to failover. For most operators that's fine; for highly latency-sensitive ones, consider active-active with careful conflict handling.

---

## Watches and triggers

By default, `For(&v1.Database{})` watches Database resources.

Add watches for owned resources so a change to a child triggers re-reconcile of the parent:

```go
return ctrl.NewControllerManagedBy(mgr).
    For(&v1.Database{}).
    Owns(&appsv1.StatefulSet{}).
    Owns(&corev1.Service{}).
    Owns(&batchv1.CronJob{}).
    Complete(r)
```

`Owns` translates child events back to parent (via OwnerReference). Child gets edited → parent reconciles.

For cross-CR dependencies (e.g., Database references a Secret managed by another operator), use `Watches`:

```go
return ctrl.NewControllerManagedBy(mgr).
    For(&v1.Database{}).
    Watches(
        &corev1.Secret{},
        handler.EnqueueRequestsFromMapFunc(r.findDatabasesForSecret),
    ).
    Complete(r)
```

`findDatabasesForSecret` queries which Databases reference this Secret and returns their NamespacedNames.

### Predicates (filter events)

Without predicates, every change to a watched resource triggers reconcile. Useful but noisy.

```go
return ctrl.NewControllerManagedBy(mgr).
    For(&v1.Database{}, builder.WithPredicates(predicate.GenerationChangedPredicate{})).
    Owns(&appsv1.StatefulSet{}).
    Complete(r)
```

`GenerationChangedPredicate{}` triggers reconcile only when `spec` changes (not on status updates from the controller itself). Prevents self-triggered loops.

Other useful predicates:
- `predicate.LabelChangedPredicate{}`
- `predicate.AnnotationChangedPredicate{}`
- `predicate.ResourceVersionChangedPredicate{}`
- Custom: implement `predicate.Funcs{}` with CreateFunc, UpdateFunc, DeleteFunc, GenericFunc.

---

## Indexers

For fast lookups (e.g., "all Databases that reference secret X"), pre-build an index:

```go
mgr.GetFieldIndexer().IndexField(
    ctx,
    &v1.Database{},
    "spec.credentialsSecretRef.name",
    func(obj client.Object) []string {
        db := obj.(*v1.Database)
        if db.Spec.CredentialsSecretRef.Name == "" {
            return nil
        }
        return []string{db.Spec.CredentialsSecretRef.Name}
    },
)
```

Then query:

```go
var dbs v1.DatabaseList
if err := r.List(ctx, &dbs, client.InNamespace(secret.Namespace),
    client.MatchingFields{"spec.credentialsSecretRef.name": secret.Name}); err != nil {
    return nil
}
```

Without an index, K8s API server would list all Databases and the operator would filter in-memory — fine for small clusters, painful at scale.

---

## Error handling

### Transient vs permanent

```go
if err := r.reconcileSomething(ctx, db); err != nil {
    if isTransient(err) {  // network, API throttling, etc.
        return ctrl.Result{RequeueAfter: 30 * time.Second}, nil
    }
    if isPermanent(err) {  // bad spec, missing required upstream
        // record on status, don't requeue
        return r.failStatus(ctx, db, "PermanentError", err)
    }
    return ctrl.Result{}, err  // default: requeue with backoff
}
```

### Conflict on update

```go
if err := r.Update(ctx, db); err != nil {
    if apierrors.IsConflict(err) {
        // Object was modified since we fetched. Requeue to retry with fresh state.
        return ctrl.Result{Requeue: true}, nil
    }
    return ctrl.Result{}, err
}
```

Conflicts are normal under concurrent updates. Re-fetch and retry.

---

## RBAC generation

Kubebuilder uses kubebuilder marker comments to generate RBAC:

```go
//+kubebuilder:rbac:groups=example.com,resources=databases,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=example.com,resources=databases/status,verbs=get;update;patch
//+kubebuilder:rbac:groups=example.com,resources=databases/finalizers,verbs=update
//+kubebuilder:rbac:groups=apps,resources=statefulsets,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=core,resources=services,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=core,resources=secrets,verbs=get;list;watch
```

Run `make manifests` to regenerate the RBAC YAMLs.

### Tightening RBAC

Default generated RBAC is permissive. Tighten:

- Remove verbs not actually used (does this controller really `delete` Secrets? Probably not.)
- Restrict by `resourceNames` if you only need specific objects
- Prefer namespace-scoped Role over cluster-scoped ClusterRole when possible
- For cross-namespace operations, use a ClusterRole with explicit list of namespaces if needed (via RoleBinding per namespace)

---

## Testing patterns

### Unit tests (function-level)

Test the pure functions (builders, validators) without K8s:

```go
func TestBuildStatefulSet(t *testing.T) {
    db := &v1.Database{
        Spec: v1.DatabaseSpec{Version: "14.10", Replicas: 3, Storage: "100Gi"},
    }
    sts := buildStatefulSet(db)
    assert.Equal(t, int32(3), *sts.Spec.Replicas)
    assert.Equal(t, "postgres:14.10", sts.Spec.Template.Spec.Containers[0].Image)
}
```

### Integration tests with envtest

Envtest spins up a real etcd + kube-apiserver in your test (not a full kubelet). You can `Create` / `Update` / `Get` against a real K8s API.

```go
func TestReconcile_HappyPath(t *testing.T) {
    ctx := context.Background()
    db := &v1.Database{
        ObjectMeta: metav1.ObjectMeta{Name: "test-db", Namespace: "default"},
        Spec:       v1.DatabaseSpec{Version: "14.10", Replicas: 1, Storage: "10Gi"},
    }
    require.NoError(t, k8sClient.Create(ctx, db))

    // Trigger reconcile
    _, err := reconciler.Reconcile(ctx, ctrl.Request{
        NamespacedName: types.NamespacedName{Name: "test-db", Namespace: "default"},
    })
    require.NoError(t, err)

    // Verify StatefulSet exists
    var sts appsv1.StatefulSet
    require.NoError(t, k8sClient.Get(ctx, types.NamespacedName{Name: "test-db", Namespace: "default"}, &sts))
    assert.Equal(t, int32(1), *sts.Spec.Replicas)
}
```

Envtest is the workhorse of operator testing. Aim for >70% of test value to come from envtest, not from unit tests of pure functions.

### E2E tests

Run against a real cluster (kind / k3d / actual GKE/EKS/AKS). Slower; reserve for the critical user journeys.

---

## Performance patterns

### Cache pressure

Controller-runtime caches all watched resources. Watching all Pods cluster-wide → big memory hit.

Mitigations:
- Use label selectors to narrow what's cached
- Scope watches to namespaces
- Don't watch resources you don't need

### Concurrent reconciles

```go
return ctrl.NewControllerManagedBy(mgr).
    For(&v1.Database{}).
    WithOptions(controller.Options{MaxConcurrentReconciles: 5}).
    Complete(r)
```

Default is 1. Increase if reconciles are long but not contended. Don't increase if reconciles do many writes (they'll fight on resourceVersion).

### Rate limiting

Default exponential backoff is `5ms * 2^retry` capped at 1000s. Usually fine. Override if you need different behavior:

```go
WithOptions(controller.Options{
    RateLimiter: workqueue.NewItemExponentialFailureRateLimiter(time.Second, 5*time.Minute),
})
```

---

## Common reconciliation patterns by use case

### Pattern: Phase machine

```go
switch db.Status.Phase {
case "":
    return r.bootstrap(ctx, db)
case "Bootstrapping":
    return r.checkBootstrap(ctx, db)
case "Running":
    return r.reconcileRunning(ctx, db)
case "Updating":
    return r.checkUpdate(ctx, db)
case "Failed":
    return r.attemptRecovery(ctx, db)
}
```

Use when the lifecycle has explicit linear stages. Keep transitions explicit.

### Pattern: Always-converge (no phases)

```go
desired := computeDesiredState(db.Spec)
if err := r.reconcileAllChildren(ctx, db, desired); err != nil { ... }
r.updateStatus(ctx, db, observeActual(ctx))
```

Use when each reconcile can re-derive everything from spec. Simpler than phase machines; less to go wrong.

### Pattern: Sub-controllers per concern

One controller for the StatefulSet, another for backups, another for network policies. Each watches the parent CR, each updates a distinct status condition.

Use when concerns are truly independent and the parent's status is multi-dimensional.

---

## Observability hooks

Controller-runtime exposes Prometheus metrics out of the box on `:8080/metrics`:

- `controller_runtime_reconcile_total{controller, result}`
- `controller_runtime_reconcile_errors_total{controller}`
- `controller_runtime_reconcile_time_seconds{controller}` (histogram)
- `controller_runtime_max_concurrent_reconciles{controller}`
- `controller_runtime_active_workers{controller}`
- `workqueue_depth{name}`
- `workqueue_adds_total{name}`
- `workqueue_queue_duration_seconds{name}`
- `workqueue_unfinished_work_seconds{name}`

Add your own:

```go
var dbReconcileLatency = prometheus.NewHistogramVec(prometheus.HistogramOpts{
    Name: "db_operator_reconcile_duration_seconds",
    Buckets: prometheus.ExponentialBuckets(0.001, 2, 15),
}, []string{"phase"})

func init() { ctrlmetrics.Registry.MustRegister(dbReconcileLatency) }
```

For logging, use structured fields:

```go
log := logf.FromContext(ctx).WithValues(
    "database", db.Name,
    "namespace", db.Namespace,
    "phase", db.Status.Phase,
    "generation", db.Generation,
)
log.Info("reconcile start")
```

---

## Summary

- Reconcile is **idempotent, level-triggered, converging**. Re-deriving state on every call is the norm.
- **Finalizers** for external cleanup. **Leader election** for HA. **Indexers** for fast lookups. **Predicates** to reduce noise.
- **Server-Side Apply** is the modern pattern for owning child resources without fighting other controllers.
- **Status updates** via `r.Status().Update(...)` — separate subresource, doesn't trigger reconcile loops.
- **RBAC** via kubebuilder markers; tighten the generated defaults.
- **Test with envtest** for the bulk of test coverage; envtest is real enough to catch real bugs.
- **Observability** is non-negotiable; controller-runtime gives you free metrics, you add the logs.

---

## The reconciliation loop (skill-body overview)

The control loop is the heart of an operator. It runs whenever a watched resource changes (or periodically).

```
loop {
  obj = fetch(CR_key)
  if (obj is being deleted) {
    handle_finalizer(obj)
    return
  }
  desired = compute_desired_state(obj.spec)
  actual = observe_actual_state(cluster)
  if (desired != actual) {
    apply_diff(desired, actual)
  }
  update_status(obj, actual)
  if (transient_error) requeue_after(backoff)
}
```

### Five rules of reconciliation

1. **Idempotent.** Running reconcile twice with the same inputs produces the same effect. No "create or fail" — always "ensure exists."
2. **Level-triggered, not edge-triggered.** Reconcile from current state, not from the diff of what changed. Don't say "user changed X, so increment Y" — say "Y should equal f(X), check and set if needed."
3. **Converge.** Each reconcile gets closer to desired state, or stays there. Doesn't oscillate.
4. **Fail safe.** If something errors, requeue with exponential backoff. Don't crash; don't loop tight.
5. **Observed generation tracking.** Status.observedGeneration tells users "yes, I saw your latest spec change."

### Common reconciliation patterns

| Pattern | When |
|---------|------|
| **Direct apply** | Stateless dependent resources (Deployments, Services, ConfigMaps owned by this CR) |
| **Phase machine** | Multi-step lifecycle with explicit phases (Pending → Bootstrapping → Running → Updating → Terminating) |
| **Sub-controllers** | One controller per logical concern (e.g., one for the StatefulSet, one for backups, one for network policies) |
| **Owner references** | All child resources have OwnerReference back to the CR → garbage collection is automatic on delete |

---

## Operational concerns (skill-body overview)

### Finalizers

Without finalizers, when a CR is deleted, the controller doesn't get to clean up external resources (database in cloud, DNS record, S3 bucket).

Pattern:
1. On CR create, add finalizer string to `metadata.finalizers`
2. On CR delete (when `metadata.deletionTimestamp` is set), do cleanup
3. After successful cleanup, remove the finalizer
4. K8s sees no finalizers, completes the delete

Anti-pattern: finalizer that can't complete (cleanup waits on something unavailable). User can't delete the CR; must manually edit out the finalizer (`kubectl patch`). Always have a max-retry / timeout for cleanup.

### Leader election

With > 1 controller replica (for HA), only one should reconcile at a time. Use lease-based leader election (built into controller-runtime).

```go
mgr, err := ctrl.NewManager(cfg, ctrl.Options{
    LeaderElection:          true,
    LeaderElectionID:        "myop.example.com",
    LeaderElectionNamespace: "myop-system",
})
```

Without leader election, two controllers fight, status flaps, you've created your own chaos.

### RBAC scoping

Default RBAC generated by Kubebuilder is wide ("get/list/watch/create/update/delete/patch on everything in my group + my CRD"). Tighten it:

- **Get/list/watch** on resources the controller observes
- **Create/update/patch** only on resources the controller manages
- **Delete** only on resources it owns
- **No `*` verbs** unless absolutely necessary
- **Cluster-scoped vs namespace-scoped** carefully — many operators don't need cluster scope

A controller with `cluster-admin` RBAC is a privilege-escalation vector.

### Status subresource

Always enable status as a subresource:

```yaml
versions:
- name: v1
  served: true
  storage: true
  subresources:
    status: {}
```

Why:
- `kubectl get -o yaml` shows status without ambiguity
- Updates to status don't change spec's `resourceVersion` (no infinite reconcile loop)
- RBAC can grant status-only updates separately

### Observability

Operators are silent until they aren't. Wire metrics:

- `reconcile_total{controller="db"}` — count of reconciliations
- `reconcile_errors_total{controller="db"}` — errored reconciliations
- `reconcile_duration_seconds{controller="db"}` — histogram
- `workqueue_depth{controller="db"}` — backlog
- `workqueue_unfinished_work_seconds{controller="db"}` — pending work age
- `controller_runtime_active_workers{controller="db"}` — concurrency

Controller-runtime exposes these via the `/metrics` endpoint. Scrape with Prometheus.

Logging:
- Structured (logr / zap)
- Include `namespace/name` of the reconciled CR
- Include `reconcileID` (UUID per reconciliation, threading through sub-calls)
- WARN/ERROR on requeue with reason
- INFO on phase transitions
