# Tooling, Structure, Configuration & Workflows

Read this when choosing monorepo tools, laying out the repo, configuring Turborepo/pnpm, running impact analysis, setting up remote caching, wiring affected-only CI, publishing with Changesets, or migrating multi-repo to monorepo.

## Tool Selection Decision Matrix

| Requirement | Turborepo | Nx | pnpm Workspaces | Changesets |
|-------------|-----------|-----|-----------------|------------|
| Simple task runner | Best | Good | N/A | N/A |
| Remote caching | Built-in | Nx Cloud | N/A | N/A |
| Code generation | No | Best | N/A | N/A |
| Dependency management | N/A | N/A | Best | N/A |
| Package publishing | N/A | N/A | N/A | Best |
| Plugin ecosystem | Limited | Extensive | N/A | N/A |
| Config complexity | Minimal | Moderate | Minimal | Minimal |

**Recommended modern stack:** pnpm workspaces + Turborepo + Changesets

## Monorepo Structure

```
my-monorepo/
├── apps/
│   ├── web/                    # Next.js frontend
│   │   ├── package.json        # depends on @repo/ui, @repo/utils
│   │   └── ...
│   ├── api/                    # Express/Fastify backend
│   │   ├── package.json        # depends on @repo/db, @repo/utils
│   │   └── ...
│   └── mobile/                 # React Native app
│       ├── package.json
│       └── ...
├── packages/
│   ├── ui/                     # Shared React components
│   │   ├── package.json        # @repo/ui
│   │   └── ...
│   ├── utils/                  # Shared utilities
│   │   ├── package.json        # @repo/utils
│   │   └── ...
│   ├── db/                     # Database client + schema
│   │   ├── package.json        # @repo/db
│   │   └── ...
│   ├── types/                  # Shared TypeScript types
│   │   ├── package.json        # @repo/types (no runtime deps)
│   │   └── ...
│   └── config/                 # Shared configs (tsconfig, eslint)
│       ├── tsconfig.base.json
│       └── eslint.base.js
├── turbo.json                  # Turborepo pipeline config
├── pnpm-workspace.yaml         # Workspace package locations
├── package.json                # Root scripts, devDependencies
└── .changeset/                 # Changeset config
    └── config.json
```

## Turborepo Configuration

### turbo.json

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "globalEnv": ["NODE_ENV", "CI"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["src/**", "tsconfig.json", "package.json"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"],
      "env": ["NEXT_PUBLIC_*"]
    },
    "test": {
      "dependsOn": ["^build"],
      "inputs": ["src/**", "tests/**", "vitest.config.*"],
      "outputs": ["coverage/**"]
    },
    "lint": {
      "dependsOn": ["^build"],
      "inputs": ["src/**", ".eslintrc.*", "tsconfig.json"]
    },
    "typecheck": {
      "dependsOn": ["^build"],
      "inputs": ["src/**", "tsconfig.json"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### Key Turborepo Commands

```bash
# Run all tasks
turbo run build

# Run only affected packages (compared to main)
turbo run build test --filter='...[origin/main]'

# Run for a specific package and its dependencies
turbo run build --filter=@repo/web...

# Run for a specific package only (no deps)
turbo run test --filter=@repo/ui

# Dry run to see what would execute
turbo run build --dry=json

# View dependency graph
turbo run build --graph=graph.html

# Summarize cache usage
turbo run build --summarize
```

## pnpm Workspace Configuration

### pnpm-workspace.yaml

```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

### Cross-Package References

```json
// packages/ui/package.json
{
  "name": "@repo/ui",
  "version": "0.0.0",
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "dependencies": {
    "@repo/types": "workspace:*"
  }
}

// apps/web/package.json
{
  "name": "@repo/web",
  "dependencies": {
    "@repo/ui": "workspace:*",
    "@repo/utils": "workspace:*"
  }
}
```

### Workspace Commands

```bash
# Install all workspace dependencies
pnpm install

# Add a dependency to a specific package
pnpm add zod --filter @repo/api

# Add a workspace package as dependency
pnpm add @repo/utils --filter @repo/web --workspace

# Run a script in a specific package
pnpm --filter @repo/web dev

# Run a script in all packages that have it
pnpm -r run build

# List all packages
pnpm -r ls --depth -1
```

## Impact Analysis

### Find All Dependents of a Changed Package

```bash
# Using turbo to see what depends on @repo/ui
turbo run build --filter='...@repo/ui' --dry=json | \
  jq '.tasks[].package' -r | sort -u

# Manual: search for imports of a package
grep -r "from '@repo/ui'" apps/ packages/ --include="*.ts" --include="*.tsx" -l
```

### Dependency Graph Visualization

```bash
# Generate HTML visualization
turbo run build --graph=dependency-graph.html

# Generate DOT format for custom rendering
turbo run build --graph=deps.dot

# Quick Mermaid diagram from package.json files
echo "graph TD"
for pkg in packages/*/package.json apps/*/package.json; do
  name=$(jq -r '.name' "$pkg")
  jq -r '.dependencies // {} | keys[] | select(startswith("@repo/"))' "$pkg" | while read dep; do
    echo "  $name --> $dep"
  done
done
```

## Remote Caching

### Turborepo Remote Cache (Vercel)

```bash
# Login to Vercel (one-time)
turbo login

# Link repo to Vercel team
turbo link

# CI: set environment variables
# TURBO_TOKEN=<vercel-token>
# TURBO_TEAM=<team-slug>

# Verify remote cache works
turbo run build --summarize
# Look for "Remote cache: hit" entries
```

### Self-Hosted Remote Cache

```bash
# Using ducktape/turborepo-remote-cache
docker run -p 3000:3000 \
  -e STORAGE_PROVIDER=local \
  -e STORAGE_PATH=/cache \
  ducktape/turborepo-remote-cache

# Configure turbo to use it
# turbo.json:
# { "remoteCache": { "apiUrl": "http://cache-server:3000" } }
```

## CI/CD with Affected Packages Only

```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # needed for --filter comparisons

      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      # Only lint/test/build affected packages
      - run: turbo run lint test build --filter='...[origin/main]'
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ vars.TURBO_TEAM }}
```

## Publishing with Changesets

### Setup

```bash
# Install changesets
pnpm add -D -w @changesets/cli @changesets/changelog-github

# Initialize
pnpm changeset init
```

### .changeset/config.json

```json
{
  "$schema": "https://unpkg.com/@changesets/config@3.0.0/schema.json",
  "changelog": ["@changesets/changelog-github", { "repo": "org/repo" }],
  "commit": false,
  "fixed": [],
  "linked": [["@repo/ui", "@repo/utils"]],
  "access": "public",
  "baseBranch": "main",
  "updateInternalDependencies": "patch"
}
```

### Publishing Workflow

```bash
# 1. Developer adds a changeset for their changes
pnpm changeset
# Interactive: select packages, bump type (patch/minor/major), summary

# 2. Before release: consume changesets and bump versions
pnpm changeset version
# Updates package.json versions and CHANGELOG.md files

# 3. Publish to npm
pnpm changeset publish
# Replaces workspace:* with real versions and publishes
```

## Migration: Multi-Repo to Monorepo

```bash
# 1. Preserve git history using filter-repo
# In each source repo:
git filter-repo --to-subdirectory-filter packages/ui
git filter-repo --to-subdirectory-filter apps/api

# 2. Create monorepo and merge histories
mkdir monorepo && cd monorepo && git init
git remote add ui ../old-ui-repo
git fetch ui --no-tags
git merge ui/main --allow-unrelated-histories

git remote add api ../old-api-repo
git fetch api --no-tags
git merge api/main --allow-unrelated-histories

# 3. Set up workspace configuration
# Add pnpm-workspace.yaml, turbo.json, root package.json

# 4. Update internal imports
# Change "ui-package" imports to "@repo/ui"
# Change npm versions to "workspace:*"

# 5. Verify
pnpm install
turbo run build test
```
