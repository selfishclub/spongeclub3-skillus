# Review Workflow & Command Catalog

Read this when performing a hands-on review: the 6-step workflow with the exact `gh`/`grep` commands for gathering context, blast-radius analysis, security scanning, breaking-change detection, test-coverage delta, and performance impact.

## Step 1: Gather Context

```bash
PR=123

# PR metadata
gh pr view $PR --json title,body,labels,milestone,assignees | jq .

# Files changed
gh pr diff $PR --name-only

# Full diff for analysis
gh pr diff $PR > /tmp/pr-$PR.diff

# CI status
gh pr checks $PR
```

## Step 2: Blast Radius Analysis

For each changed file, determine its impact scope:

```bash
DIFF_FILES=$(gh pr diff $PR --name-only)

# Find all files that import changed modules
for file in $DIFF_FILES; do
  module=$(basename "$file" .ts | sed 's/\..*$//')
  echo "=== Dependents of $file ==="
  grep -rl "from.*$module\|import.*$module\|require.*$module" src/ --include="*.ts" --include="*.tsx" -l 2>/dev/null
done

# Check if changes span multiple services (monorepo)
echo "$DIFF_FILES" | cut -d/ -f1-2 | sort -u

# Identify shared contracts
echo "$DIFF_FILES" | grep -E "types/|interfaces/|schemas/|models/|shared/"
```

**Blast Radius Severity:**

| Severity | Criteria | Examples |
|----------|----------|---------|
| CRITICAL | Shared library used by 5+ consumers | `packages/utils/`, auth middleware, DB schema |
| HIGH | Cross-service impact, shared config | API contracts, env vars, shared types |
| MEDIUM | Single service internal change | Service handler, utility function |
| LOW | Isolated change, no dependents | UI component, test file, documentation |

## Step 3: Security Scan

```bash
DIFF=/tmp/pr-$PR.diff

# SQL injection — raw string interpolation in queries
grep -n "query\|execute\|raw(" $DIFF | grep -E '\$\{|f"|%s|format\(' | grep "^+"

# Hardcoded secrets
grep -nE "(password|secret|api_key|token|private_key)\s*=\s*['\"][^'\"]{8,}" $DIFF | grep "^+"

# AWS keys
grep -nE "AKIA[0-9A-Z]{16}" $DIFF

# XSS vectors
grep -n "dangerouslySetInnerHTML\|innerHTML\s*=" $DIFF | grep "^+"

# Auth bypass indicators
grep -n "bypass\|skip.*auth\|noauth\|TODO.*auth" $DIFF | grep "^+"

# Insecure crypto
grep -nE "md5\(|sha1\(|createHash\(['\"]md5|createHash\(['\"]sha1" $DIFF | grep "^+"

# eval/exec
grep -nE "\beval\(|\bexec\(|\bsubprocess\.call\(" $DIFF | grep "^+"

# Path traversal
grep -nE "path\.join\(.*req\.|readFile\(.*req\." $DIFF | grep "^+"

# Prototype pollution
grep -n "__proto__\|constructor\[" $DIFF | grep "^+"

# Sensitive data in logs
grep -nE "console\.(log|info|warn|error).*password\|console\.(log|info|warn|error).*token\|console\.(log|info|warn|error).*secret" $DIFF | grep "^+"
```

## Step 4: Breaking Change Detection

```bash
# API endpoint removals
grep "^-" $DIFF | grep -E "router\.(get|post|put|delete|patch)\(|@app\.(get|post|put|delete)"

# TypeScript interface/type removals
grep "^-" $DIFF | grep -E "^-\s*(export\s+)?(interface|type) "

# Required field additions to existing types
grep "^+" $DIFF | grep -E ":\s*(string|number|boolean)\s*$" | grep -v "?" # non-optional additions

# Database migrations: destructive operations
grep -E "DROP TABLE|DROP COLUMN|ALTER.*NOT NULL|TRUNCATE" $DIFF

# Index removals
grep -E "DROP INDEX|remove_index" $DIFF

# Removed env vars
grep "^-" $DIFF | grep -oE "process\.env\.[A-Z_]+" | sort -u

# New env vars (may not be set in production)
grep "^+" $DIFF | grep -oE "process\.env\.[A-Z_]+" | sort -u
```

## Step 5: Test Coverage Delta

```bash
# Count source vs test changes
SRC_FILES=$(gh pr diff $PR --name-only | grep -vE "\.test\.|\.spec\.|__tests__|\.stories\.")
TEST_FILES=$(gh pr diff $PR --name-only | grep -E "\.test\.|\.spec\.|__tests__")

echo "Source files changed: $(echo "$SRC_FILES" | grep -c .)"
echo "Test files changed:   $(echo "$TEST_FILES" | grep -c .)"

# New lines of logic vs test
LOGIC_LINES=$(grep "^+" $DIFF | grep -v "^+++" | grep -v "\.test\.\|\.spec\." | wc -l)
TEST_LINES=$(grep "^+" $DIFF | grep -v "^+++" | grep "\.test\.\|\.spec\." | wc -l)
echo "New logic lines: $LOGIC_LINES"
echo "New test lines:  $TEST_LINES"
```

**Coverage Rules:**
- New public function without tests: flag as must-fix
- Deleted tests without deleted code: flag as must-fix
- Coverage drop >5%: block merge
- Auth/payments paths: require near-100% coverage

## Step 6: Performance Impact

```bash
# N+1 patterns: DB calls that might be inside loops
grep -n "\.find\|\.findOne\|\.query\|db\." $DIFF | grep "^+" | head -20

# Heavy new dependencies
grep "^+" $DIFF | grep -E '"[a-z@].*":\s*"[0-9^~]' | head -10

# Unbounded loops
grep -n "while (true\|while(true" $DIFF | grep "^+"

# Missing await (accidentally sequential)
grep -n "await.*await" $DIFF | grep "^+"

# Large allocations
grep -n "new Array([0-9]\{4,\}\|Buffer\.alloc" $DIFF | grep "^+"
```
