# Review Write-up Format, 35-Item Checklist & Comment Labels

Read this when writing up the review: the write-up structure with worked must-fix/should-fix/suggestion examples, the complete 35-item review checklist, and the comment-label taxonomy.

## Review Write-up Format

Structure every review using this format:

```markdown
## PR Review: [PR Title] (#NUMBER)

**Blast Radius:** HIGH — changes `lib/auth` used by 5 services
**Security:** 1 finding (medium severity)
**Tests:** Coverage delta +2% (3 new tests for 5 new functions)
**Breaking Changes:** None detected

---

### MUST FIX (Blocking)

**1. SQL Injection risk in `src/db/users.ts:42`**
Raw string interpolation in WHERE clause.
```diff
- const user = await db.query(`SELECT * FROM users WHERE id = '${userId}'`)
+ const user = await db.query('SELECT * FROM users WHERE id = $1', [userId])
```

**2. Missing auth check on `POST /api/admin/reset`**
No role verification before destructive operation.
Add `requireRole('admin')` middleware.

---

### SHOULD FIX (Non-blocking)

**3. N+1 pattern in `src/services/reports.ts:88`**
`findUser()` called inside `results.map()` — batch with `findManyUsers(ids)`.

**4. New env var `FEATURE_FLAG_X` not in `.env.example`**
Add to `.env.example` with description so other developers know about it.

---

### SUGGESTIONS

**5. Consider pagination for `GET /api/projects`**
Currently returns all projects without limit. Add `?limit=20&offset=0`.

---

### LOOKS GOOD
- Auth flow for new OAuth provider is thorough
- DB migration has proper rollback (`down()` method)
- Error handling is consistent with rest of codebase
- Test names clearly describe what they verify
```

## Complete Review Checklist (35 Items)

```markdown
### Scope and Context
- [ ] PR title accurately describes the change
- [ ] PR description explains WHY, not just WHAT
- [ ] Linked ticket exists and matches scope
- [ ] No unrelated changes (scope creep)
- [ ] Breaking changes documented in PR body

### Blast Radius
- [ ] All files importing changed modules identified
- [ ] Cross-service dependencies checked
- [ ] Shared types/interfaces reviewed for breakage
- [ ] New env vars documented in .env.example
- [ ] DB migrations are reversible (have rollback)

### Security
- [ ] No hardcoded secrets or API keys
- [ ] SQL queries use parameterized inputs
- [ ] User inputs validated and sanitized
- [ ] Auth/authorization on all new endpoints
- [ ] No XSS vectors (innerHTML, dangerouslySetInnerHTML)
- [ ] New dependencies checked for known CVEs
- [ ] No sensitive data in logs (PII, tokens, passwords)
- [ ] File uploads validated (type, size, content)
- [ ] CORS configured correctly for new endpoints

### Testing
- [ ] New public functions have unit tests
- [ ] Edge cases covered (empty, null, max values)
- [ ] Error paths tested (not just happy path)
- [ ] Integration tests for API endpoint changes
- [ ] No tests deleted without clear justification
- [ ] Test names describe what they verify

### Breaking Changes
- [ ] No API endpoints removed without deprecation
- [ ] No required fields added to existing responses
- [ ] No DB columns removed without migration plan
- [ ] No env vars removed that may be in production
- [ ] Backward-compatible for external consumers

### Performance
- [ ] No N+1 query patterns introduced
- [ ] DB indexes added for new query patterns
- [ ] No unbounded loops on large datasets
- [ ] No heavy new dependencies without justification
- [ ] Async operations correctly awaited
- [ ] Caching considered for expensive operations

### Code Quality
- [ ] No dead code or unused imports
- [ ] Error handling present (no empty catch blocks)
- [ ] Consistent with existing patterns
- [ ] Complex logic has explanatory comments
```

## Comment Labels

Use consistent labels so authors can quickly prioritize:

| Label | Meaning | Action Required |
|-------|---------|-----------------|
| `must:` | Blocking issue | Must fix before merge |
| `should:` | Important improvement | Should fix, but not blocking |
| `nit:` | Style/preference | Take it or leave it |
| `question:` | Need clarification | Respond before merge |
| `suggestion:` | Alternative approach | Consider, no action needed |
| `praise:` | Good pattern | No action needed |
