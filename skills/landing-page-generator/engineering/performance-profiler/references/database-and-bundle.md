# Database Query Optimization and Bundle Analysis

Read this when optimizing slow SQL queries, detecting N+1 patterns, or reducing frontend bundle size.

## Database Query Optimization

### EXPLAIN ANALYZE Workflow

```sql
-- Step 1: Get the actual execution plan (not just estimated)
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT t.*, p.name as project_name
FROM tasks t
JOIN projects p ON p.id = t.project_id
WHERE p.workspace_id = 'ws_abc123'
  AND t.status = 'in_progress'
  AND t.deleted_at IS NULL
ORDER BY t.updated_at DESC
LIMIT 20;

-- What to look for in the output:
-- Seq Scan on tasks  → MISSING INDEX (should be Index Scan)
-- Rows Removed by Filter: 99000  → INDEX NOT SELECTIVE ENOUGH
-- Sort Method: external merge  → NOT ENOUGH work_mem
-- Nested Loop with inner Seq Scan  → MISSING INDEX ON JOIN COLUMN
-- Actual rows=1000 vs estimated rows=1  → STALE STATISTICS (run ANALYZE)
```

### N+1 Query Detection

```typescript
// PROBLEM: N+1 query pattern
async function getProjectsWithTasks(workspaceId: string) {
  const projects = await db.query.projects.findMany({
    where: eq(projects.workspaceId, workspaceId),
  });

  // This executes N additional queries (one per project)
  for (const project of projects) {
    project.tasks = await db.query.tasks.findMany({
      where: eq(tasks.projectId, project.id),
    });
  }
  return projects;
}
// Total queries: 1 + N (where N = number of projects)

// FIX: Single query with JOIN or relation loading
async function getProjectsWithTasks(workspaceId: string) {
  return db.query.projects.findMany({
    where: eq(projects.workspaceId, workspaceId),
    with: {
      tasks: true,  // Drizzle generates a single JOIN or subquery
    },
  });
}
// Total queries: 1-2 (depending on ORM strategy)
```

### N+1 Detection Script

```bash
# Log query count per request (add to middleware)
# Node.js with Drizzle:
let queryCount = 0;
const originalQuery = db.execute;
db.execute = (...args) => { queryCount++; return originalQuery.apply(db, args); };

// After request completes:
if (queryCount > 10) {
  console.warn(`N+1 ALERT: ${req.method} ${req.path} executed ${queryCount} queries`);
}
```

## Bundle Analysis

### Next.js Bundle Analyzer

```bash
# Install
pnpm add -D @next/bundle-analyzer

# next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});
module.exports = withBundleAnalyzer(nextConfig);

# Run analysis
ANALYZE=true pnpm build
# Opens browser with interactive treemap
```

### Quick Bundle Size Check

```bash
# Check what you're shipping
npx source-map-explorer .next/static/chunks/*.js

# Size of individual imports
npx import-cost  # VS Code extension for inline size

# Find heavy dependencies
npx depcheck --json | jq '.dependencies'
npx bundlephobia-cli <package-name>
```

### Common Bundle Wins

| Before | After | Savings |
|--------|-------|---------|
| `import _ from 'lodash'` | `import groupBy from 'lodash/groupBy'` | ~70KB |
| `import moment from 'moment'` | `import { format } from 'date-fns'` | ~60KB |
| `import { icons } from 'lucide-react'` | `import { Search } from 'lucide-react'` | ~50KB |
| Static import of heavy component | `dynamic(() => import('./HeavyChart'))` | Deferred |
| All routes in one chunk | Code splitting per route (automatic in Next.js) | Per-route |
