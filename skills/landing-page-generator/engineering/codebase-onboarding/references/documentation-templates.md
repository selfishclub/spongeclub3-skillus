# Onboarding Documentation Templates

Read this when generating the actual onboarding documents (Phase 3) — it holds the architecture overview, key file map, local setup, and debugging guide templates plus the audience-specific customization additions.

## Architecture Overview Template

```markdown
## Architecture

### System Diagram

[Use the ASCII diagram pattern below — it renders in any markdown viewer]

```
Browser / Mobile App
    │
    v
[API Gateway / Load Balancer]
    │
    ├──> [Web Server: Next.js / Express / FastAPI]
    │       ├── Authentication (JWT / OAuth)
    │       ├── Business Logic
    │       └── Background Jobs
    │
    ├──> [Primary Database: PostgreSQL]
    │       └── Migrations managed by [ORM]
    │
    ├──> [Cache: Redis]
    │       └── Sessions, rate limits, job queue
    │
    └──> [Object Storage: S3 / R2]
            └── File uploads, static assets

External Integrations:
    ├── [Stripe] — Payments
    ├── [SendGrid / Resend] — Transactional email
    └── [Sentry] — Error tracking
```

### Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | [framework] | [why chosen] |
| API | [framework] | [routing, middleware] |
| Database | [database + ORM] | [data storage, migrations] |
| Auth | [provider] | [authentication method] |
| Queue | [system] | [background processing] |
| Deployment | [platform] | [hosting, CI/CD] |
| Monitoring | [tool] | [errors, performance] |
```

## Key File Map Template

```markdown
## Key Files

Priority files — read these first to understand the system:

| Priority | Path | What It Does | When to Read |
|----------|------|-------------|-------------|
| 1 | `src/db/schema.ts` | Database schema — single source of truth for data model | First day |
| 2 | `src/lib/auth.ts` | Authentication configuration and session handling | First day |
| 3 | `app/api/` | All API route handlers | First week |
| 4 | `middleware.ts` | Request middleware (auth, logging, rate limiting) | First week |
| 5 | `.env.example` | All environment variables with descriptions | Setup day |

Dangerous files — coordinate before modifying:

| Path | Risk | Coordination Required |
|------|------|----------------------|
| `src/db/schema.ts` | Schema changes affect all services | PR review from DB owner |
| `middleware.ts` | Affects every request | Load test after changes |
| `lib/stripe.ts` | Payment processing | Finance team notification |
```

## Local Setup Guide Template

```markdown
## Local Setup (Target: under 10 minutes)

### Prerequisites

| Tool | Required Version | Install Command |
|------|-----------------|----------------|
| Node.js | 20+ | `nvm install 20` |
| pnpm | 9+ | `corepack enable && corepack prepare pnpm@latest` |
| Docker | 24+ | [docker.com/get-docker](https://docker.com/get-docker) |
| PostgreSQL | 16+ | Via Docker (see step 3) |

### Steps

**Step 1: Clone and install** (2 min)
```bash
git clone [repo-url]
cd [repo-name]
pnpm install
```

**Step 2: Configure environment** (1 min)
```bash
cp .env.example .env
# Edit .env — minimum required values:
#   DATABASE_URL=postgresql://dev:dev@localhost:5432/myapp
#   APP_SECRET=$(openssl rand -base64 32)
```

**Step 3: Start infrastructure** (1 min)
```bash
docker compose up -d
# Starts: PostgreSQL, Redis
# Verify: docker compose ps (all should show "running")
```

**Step 4: Set up database** (1 min)
```bash
pnpm db:migrate
pnpm db:seed    # Optional: loads test data
```

**Step 5: Start dev server** (30 sec)
```bash
pnpm dev
# App runs at http://localhost:3000
```

### Verify Everything Works

- [ ] http://localhost:3000 loads the app
- [ ] http://localhost:3000/api/health returns `{"status": "ok"}`
- [ ] `pnpm test` passes with no failures
- [ ] You can log in with the seeded test user (see .env.example for credentials)
```

## Debugging Guide Template

```markdown
## Debugging Guide

### Common Errors and Fixes

**`Error: connect ECONNREFUSED 127.0.0.1:5432`**
```
Cause: PostgreSQL is not running
Fix: docker compose up -d postgres
Verify: docker compose ps postgres (should show "running")
```

**`Error: relation "users" does not exist`**
```
Cause: Migrations have not been applied
Fix: pnpm db:migrate
Verify: pnpm db:migrate status (should show all applied)
```

**`TypeError: Cannot read property 'id' of null`**
```
Cause: Session is null — usually a missing or expired auth token
Fix: Check that the request includes a valid Authorization header
Debug: Add console.log(session) in the route handler to inspect
```

### Where to Find Logs

| Environment | Location | Command |
|-------------|----------|---------|
| Local dev | Terminal running `pnpm dev` | Scroll up in terminal |
| Local DB | Docker logs | `docker compose logs postgres` |
| Staging | [Platform dashboard] | [Link to staging logs] |
| Production | [Platform dashboard] | [Link to production logs] |

### Useful Diagnostic Commands

```bash
# Check database connectivity
psql $DATABASE_URL -c "SELECT 1"

# View active database connections
psql $DATABASE_URL -c "SELECT count(*), state FROM pg_stat_activity GROUP BY state"

# Check if a specific migration was applied
pnpm db:migrate status

# Clear local caches
redis-cli FLUSHDB

# Verify environment variables are loaded
node -e "console.log(process.env.DATABASE_URL ? 'Set' : 'MISSING')"
```
```

## Audience-Specific Customization

### Junior Developer Additions
- Explain acronyms on first use (ORM, RLS, JWT, etc.)
- Add "read this first" ordered reading list of 5 files
- Include screenshots for UI-related flows
- Link to external learning resources for key technologies
- Add a "glossary" section for domain-specific terms

### Senior Engineer Additions
- Link to Architecture Decision Records (ADRs)
- Include performance benchmark baselines
- Document known technical debt and planned improvements
- Provide security model overview with threat boundaries
- Share scaling limits and planned capacity changes

### Contractor Additions
- Define scope boundaries ("only modify files in src/features/your-feature/")
- Specify communication channels and response expectations
- Document access request process for required systems
- Include time logging requirements and reporting cadence
- List prohibited actions (direct push to main, schema changes, etc.)
