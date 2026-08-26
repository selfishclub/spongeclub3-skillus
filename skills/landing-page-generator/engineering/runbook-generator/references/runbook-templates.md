# Stack Detection & Runbook Templates

Read this when scanning a repo to detect its stack, or when writing a deployment, incident response, or database maintenance runbook — copy the matching template and fill in stack-specific commands.

## Stack Detection

Scan the repository before writing any runbook:

```bash
# CI/CD Platform
[ -d ".github/workflows" ] && echo "GitHub Actions"
[ -f ".gitlab-ci.yml" ]    && echo "GitLab CI"
[ -f "Jenkinsfile" ]       && echo "Jenkins"

# Database
grep -rl "postgres\|postgresql" package.json pyproject.toml 2>/dev/null && echo "PostgreSQL"
grep -rl "mysql\|mariadb" package.json 2>/dev/null && echo "MySQL"
grep -rl "mongodb\|mongoose" package.json 2>/dev/null && echo "MongoDB"

# Hosting
[ -f "vercel.json" ]       && echo "Vercel"
[ -f "fly.toml" ]          && echo "Fly.io"
[ -f "railway.toml" ]      && echo "Railway"
[ -d "terraform" ]         && echo "Terraform (custom cloud)"
[ -d "k8s" ] || [ -d "kubernetes" ] && echo "Kubernetes"
[ -f "docker-compose.yml" ] && echo "Docker Compose"

# Framework
[ -f "next.config.mjs" ] || [ -f "next.config.ts" ] && echo "Next.js"
grep -q "fastapi" requirements.txt 2>/dev/null && echo "FastAPI"
[ -f "go.mod" ] && echo "Go"
```

## Deployment Runbook Template

```markdown
# Deployment Runbook — [App Name]

**Stack:** [Framework] + [Database] + [Hosting]
**Last verified:** YYYY-MM-DD
**Owner:** [Team Name]
**Estimated total time:** 15-25 minutes

---

## Staleness Check

| Config File | Last Modified | Affects Steps |
|-------------|--------------|---------------|
| vercel.json | `git log -1 --format=%ci -- vercel.json` | Deploy, Rollback |
| db/schema.ts | `git log -1 --format=%ci -- db/schema.ts` | Migration |
| .github/workflows/deploy.yml | `git log -1 --format=%ci -- .github/workflows/deploy.yml` | CI |

If any config was modified after "Last verified" date, review affected steps.

---

## Pre-Deployment Checklist
- [ ] All PRs merged to main
- [ ] CI passing on main branch
- [ ] Database migrations tested in staging
- [ ] Rollback plan confirmed
- [ ] On-call engineer notified

## Step 1: Verify CI Status (2 min)

```bash
# Check latest CI run
gh run list --branch main --limit 3

# Verify specific run
gh run view <run-id>
```

VERIFY: Latest run shows green checkmark. If red, do not proceed.

## Step 2: Apply Database Migrations (5 min)

```bash
# Staging first
DATABASE_URL=$STAGING_DB_URL pnpm db:migrate

# Verify migration applied
DATABASE_URL=$STAGING_DB_URL pnpm db:migrate status
```

VERIFY: Output shows "All migrations applied" with today's date.

```bash
# Production (only after staging verification)
DATABASE_URL=$PROD_DB_URL pnpm db:migrate
```

VERIFY: Same output as staging. If error, see Rollback section.

WARNING: For migrations on tables with >1M rows, schedule during low-traffic window and monitor lock wait times.

## Step 3: Deploy to Production (5 min)

```bash
# Option A: Git push triggers deployment
git push origin main

# Option B: Manual trigger
vercel --prod
# or: fly deploy
# or: kubectl apply -f k8s/deployment.yaml
```

VERIFY: Deployment dashboard shows new version in progress. Note the deployment URL/ID for rollback.

## Step 4: Smoke Test (5 min)

```bash
# Health check
curl -sf https://myapp.com/api/health | jq .

# Critical user path
curl -sf https://myapp.com/api/v1/me \
  -H "Authorization: Bearer $TEST_TOKEN" | jq '.id'

# Check error rate (wait 2 minutes for data)
# Dashboard: [link to monitoring dashboard]
```

VERIFY:
- Health returns `{"status": "ok", "db": "connected"}`
- User endpoint returns a valid user ID
- Error rate < 1% on monitoring dashboard

## Step 5: Monitor (10 min)

Watch these metrics for 10 minutes after deployment:
- Error rate: < 1% (dashboard: [link])
- P95 latency: < 200ms (dashboard: [link])
- Active DB connections: < 80% of max (query below)

```bash
psql $PROD_DB_URL -c "SELECT count(*) FROM pg_stat_activity;"
```

VERIFY: All metrics within normal range. If any spike, proceed to Rollback.

---

## Rollback

If smoke tests fail or metrics degrade:

```bash
# Instant rollback via Vercel
vercel rollback [previous-deployment-url]

# or Fly.io
fly releases --app myapp
fly deploy --image [previous-image]

# or Kubernetes
kubectl rollout undo deployment/myapp

# Database rollback (ONLY if migration was applied in this deploy)
DATABASE_URL=$PROD_DB_URL pnpm db:rollback
```

VERIFY: Previous version serving traffic. Run smoke tests again.

---

## Escalation

| Level | Who | When | Contact |
|-------|-----|------|---------|
| L1 | On-call engineer | First responder | PagerDuty rotation |
| L2 | Platform lead | DB issues, rollback failures | Slack: @platform-lead |
| L3 | VP Engineering | Production down > 30 min | Phone: [number] |
```

## Incident Response Runbook Template

```markdown
# Incident Response Runbook

**Severity:** P1 (down), P2 (degraded), P3 (minor)
**Estimated time:** P1: 30-60 min, P2: 1-4 hours, P3: next business day

---

## Phase 1: Triage (5 min)

### Confirm the Incident

```bash
# Is the app responding?
curl -sw "%{http_code}" https://myapp.com/api/health -o /dev/null

# Check for errors in recent logs
vercel logs --since=15m | grep -i "error\|exception\|5[0-9][0-9]"
# or: kubectl logs -l app=myapp --since=15m | grep -i error
```

VERIFY: 200 = app is up. 5xx or timeout = incident confirmed.

### Declare Severity

| Condition | Severity | Action |
|-----------|----------|--------|
| Site completely unreachable | P1 | Page L2/L3 immediately |
| Partial degradation or slow | P2 | Notify team channel |
| Single feature broken | P3 | Create ticket, fix in business hours |

### Communicate

```
# Post to incident channel (adjust for your tool)
Slack: #incidents
"INCIDENT: [severity] — [brief description]. Investigating. Updates every 15 min."
```

## Phase 2: Diagnose (10-15 min)

### Check Recent Changes

```bash
# Was something just deployed?
vercel ls --limit 5
# or: kubectl rollout history deployment/myapp

# Recent commits
git log --oneline -10
```

### Check Database

```bash
# Active queries (look for long-running or blocked queries)
psql $PROD_DB_URL -c "
SELECT pid, now() - query_start AS duration, state, query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC
LIMIT 20;"

# Connection pool saturation
psql $PROD_DB_URL -c "
SELECT count(*) AS active,
       (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') AS max
FROM pg_stat_activity;"
```

### Diagnostic Decision Tree

```
Recent deploy + new errors → ROLLBACK (see Deployment Runbook)
DB queries hanging        → Kill long queries, check connection pool
External API failing      → Check status pages, enable circuit breaker
Memory/CPU spike          → Check for infinite loops, scale up temporarily
```

## Phase 3: Mitigate (variable)

```bash
# Kill a runaway database query
psql $PROD_DB_URL -c "SELECT pg_terminate_backend(<pid>);"

# Rollback last deployment
vercel rollback [previous-url]

# Scale up (if capacity issue)
fly scale count 4 --app myapp
# or: kubectl scale deployment/myapp --replicas=4
```

## Phase 4: Resolve and Postmortem

Within 24 hours of resolution:

1. Write incident timeline (what happened, when, who noticed, what fixed it)
2. Identify root cause (5 Whys analysis)
3. Define action items with owners and due dates
4. Update this runbook if a step was missing or wrong
5. Add monitoring/alerting that would have caught this earlier
```

## Database Maintenance Runbook Template

```markdown
# Database Maintenance — PostgreSQL

**Schedule:** Weekly vacuum (automated), monthly manual review

## Backup

```bash
pg_dump $PROD_DB_URL \
  --format=custom \
  --compress=9 \
  --file="backup-$(date +%Y%m%d-%H%M%S).dump"
```

VERIFY: File exists and size > 0. Test monthly with:
```bash
pg_restore --dbname=$STAGING_DB_URL backup-*.dump
psql $STAGING_DB_URL -c "SELECT count(*) FROM users;"
```

## Vacuum and Reindex

```bash
# Check bloat
psql $PROD_DB_URL -c "
SELECT tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
       n_dead_tup,
       ROUND(n_dead_tup::numeric / NULLIF(n_live_tup, 0) * 100, 1) AS dead_pct
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 10;"

# Vacuum high-bloat tables (non-blocking)
psql $PROD_DB_URL -c "VACUUM ANALYZE tablename;"

# Reindex (CONCURRENTLY to avoid locks)
psql $PROD_DB_URL -c "REINDEX INDEX CONCURRENTLY index_name;"
```

VERIFY: dead_pct drops below 5% after vacuum.
```
