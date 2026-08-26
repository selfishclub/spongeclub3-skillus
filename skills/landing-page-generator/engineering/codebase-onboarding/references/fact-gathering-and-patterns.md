# Codebase Fact-Gathering & Pattern Identification

Read this when you are examining a codebase before writing any onboarding docs — it holds the Phase 1 fact-gathering commands and the Phase 2 architecture-pattern classification.

## Codebase Analysis Process

### Phase 1: Gather Facts

Run these analysis commands to collect data before generating any documentation.

```bash
# 1. Package manifest and scripts
cat package.json 2>/dev/null | python3 -c "
import json, sys
pkg = json.load(sys.stdin)
print(f\"Name: {pkg.get('name')}\")
print(f\"Scripts: {list(pkg.get('scripts', {}).keys())}\")
print(f\"Deps: {len(pkg.get('dependencies', {}))}\")
print(f\"DevDeps: {len(pkg.get('devDependencies', {}))}\")
" || echo "No package.json found"

# 2. Directory structure (top 3 levels, excluding noise)
find . -maxdepth 3 \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  -not -path '*/.next/*' \
  -not -path '*/__pycache__/*' \
  -not -path '*/dist/*' \
  -not -path '*/.venv/*' | \
  sort | head -80

# 3. Largest source files (complexity indicators)
find src/ app/ lib/ -name "*.ts" -o -name "*.tsx" -o -name "*.py" -o -name "*.go" 2>/dev/null | \
  xargs wc -l 2>/dev/null | sort -rn | head -20

# 4. API routes
find . -name "route.ts" -path "*/api/*" 2>/dev/null | sort  # Next.js
grep -rn "router\.\(get\|post\|put\|delete\)" src/ --include="*.ts" 2>/dev/null | head -30  # Express

# 5. Database schema location
find . -name "schema.ts" -o -name "schema.prisma" -o -name "models.py" 2>/dev/null | head -10

# 6. Test infrastructure
find . -name "*.test.ts" -o -name "*.spec.ts" -o -name "test_*.py" 2>/dev/null | wc -l

# 7. Recent significant changes (last 90 days)
git log --oneline --since="90 days ago" | grep -iE "feat|refactor|breaking|migrate" | head -20

# 8. CI/CD configuration
ls .github/workflows/ 2>/dev/null || ls .gitlab-ci.yml 2>/dev/null || echo "No CI config found"

# 9. Environment variables referenced in code
grep -rh "process\.env\.\|os\.environ\.\|os\.getenv" src/ app/ lib/ --include="*.ts" --include="*.py" 2>/dev/null | \
  grep -oE "[A-Z_]{3,}" | sort -u | head -30
```

### Phase 2: Identify Architecture Patterns

Based on gathered facts, classify the project:

| Signal | Architecture Pattern |
|--------|---------------------|
| `app/` directory with `page.tsx` | Next.js App Router (file-based routing) |
| `src/routes/` with Express imports | Express REST API |
| FastAPI decorators | Python REST/async API |
| `docker-compose.yml` with multiple services | Microservices |
| Single `main.go` with handlers | Go monolith |
| `packages/` or `apps/` at root | Monorepo |
| Prisma/Drizzle schema file | ORM-managed database |
| `k8s/` or `terraform/` directories | Infrastructure as Code |

### Phase 3: Generate Documentation

Use the templates in [documentation-templates.md](documentation-templates.md) to produce the architecture overview, key file map, local setup guide, and debugging guide.
