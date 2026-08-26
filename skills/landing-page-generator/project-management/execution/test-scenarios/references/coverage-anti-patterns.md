# Coverage Anti-Patterns + Fixes

## A1 — Only happy paths
**Symptom:** Test plan = "user signs up, user logs in, user does X."

**Fix:** For each happy path, generate 4-8 edge cases, 3-5 errors,
empty state. Most production bugs come from non-happy paths.

## A2 — No empty / first-use state
**Symptom:** Dashboard tested with 50 demo projects; empty state never tested.

**Fix:** Always test the first-use experience. It's the first impression.

## A3 — Errors tested in isolation
**Symptom:** "5xx returns error message" — but never tested what user does after.

**Fix:** Each error scenario must include:
- Message displayed
- Suggested action
- Recovery path (retry / cancel / report)
- No corrupt state

## A4 — Concurrent skipped for collab features
**Symptom:** Real-time editing tested only single-user.

**Fix:** Test 2-user scenarios as table stakes for any collaborative
feature. Race conditions ship otherwise.

## A5 — Accessibility tested last (or never)
**Symptom:** "We'll add a11y in v2."

**Fix:** Baseline a11y on every feature:
- Keyboard navigation
- Screen reader pass
- Color contrast
- Touch targets

Automated tools (axe-core) cover 30%; manual covers the rest.

## A6 — Security tested only at end
**Symptom:** "Pen test before launch."

**Fix:** Security scenarios per feature:
- Auth
- Permissions
- Injection
- Sensitive data handling

Tested incrementally; pen test confirms at end.

## A7 — Performance tested only with synthetic data
**Symptom:** Load test with 100 records; production has 10M.

**Fix:** Test with production-like data volumes (or close).

## A8 — Cross-platform: only Chrome
**Symptom:** Tested only in Chrome dev machine.

**Fix:** Per supported browser + OS + device tier matrix.

## A9 — Localization: only English tested
**Symptom:** English looks fine; German breaks UI; Arabic backwards.

**Fix:** Pseudo-localization in CI (long-string, RTL); manual spot-check on shipped locales.

## A10 — "QA will catch it"
**Symptom:** Engineer / PM doesn't generate scenarios; relies on QA.

**Fix:** Scenarios are designed before code, not after. QA implements
tests; PM defines what to test.

## A11 — Same scenarios per feature regardless of risk
**Symptom:** Login feature gets same 5 scenarios as a help-text update.

**Fix:** Risk-weight scenario count:
- Auth / payment / data-integrity: heavy scenarios
- UI text: light scenarios

## A12 — Scenarios written; never reviewed
**Symptom:** Scenario list created; sits in a doc; not used.

**Fix:** Scenarios reviewed at:
- Sprint planning (sizing)
- Code review (verify coverage)
- QA planning (test pass)
- Production incidents (gap analysis)

## Worked example — signup feature

### Weak coverage

- User signs up successfully
- Form shows error on invalid email

### Strong coverage

**Happy path (3):**
1. User signs up with email + password → account created
2. User signs up with Google SSO → account created
3. User signs up via invite link → joins existing org

**Edge cases (8):**
1. Empty email → "Email required"
2. Email = "a" (invalid format) → "Invalid email format"
3. Email 257+ chars → "Email too long"
4. Password 7 chars (below min 8) → "Password too short"
5. Password 501+ chars (above max) → "Password too long"
6. Password no uppercase / digit / special → "Password must include..."
7. Email with emoji → handled (accept) or rejected (consistent)
8. Email matches existing → "Already registered. Sign in?"

**Error handling (5):**
1. Submit offline → "Connection lost"; form preserves input
2. Server 500 → "Something went wrong" (not stack trace)
3. Rate limited (10+ attempts) → "Too many attempts"; cool-down
4. SSO failure → fallback to email; partial state cleaned
5. Verification email fails to send → user sees "Resend"

**Empty / first-use (2):**
1. After signup → land on onboarding (not blank dashboard)
2. After email verification → land in product (not stuck on verification page)

**Concurrent (2):**
1. Same email signs up twice in parallel → only one account created
2. User submits twice quickly → idempotent (no duplicate)

**Accessibility (4):**
1. Tab through form → focus visible; logical order
2. Screen reader → labels read correctly
3. Submit with keyboard (Enter) → works
4. Error messages → associated with field via aria-describedby

**Security (5):**
1. Password not in URL / logs
2. Password hashed before storage (verify in DB)
3. SQL injection in email → sanitized
4. XSS in email field → escaped on display
5. Rate limit prevents brute force

**Performance (1):**
1. Signup endpoint < 500ms P95 under 1000 concurrent

**Cross-platform (3):**
1. iOS Safari → autofill works
2. Android Chrome → password manager integration
3. Older browsers (Safari 14) → graceful degradation

**Total: 33 scenarios vs original 2.**

The original missed:
- All edge cases
- Most errors
- Empty state
- Concurrent
- A11y entirely
- Security entirely
- Cross-platform

## Coverage gap analysis

For an existing feature's scenario list:

| Category | Recommended | Actual | Gap |
|----------|-------------|--------|-----|
| Happy | 1-3 | | |
| Edge | 4-8 | | |
| Error | 4-6 | | |
| Empty | 1-2 | | |
| Concurrent | varies | | |
| A11y | 3-4 baseline | | |
| Security | 3+ | | |

Highlight rows with gaps. Score by importance.

## Coverage discipline checklist

For each feature before code:

- [ ] PRD / spec reviewed
- [ ] User goals identified
- [ ] Inputs + outputs enumerated
- [ ] Happy paths defined (1-3)
- [ ] Edge cases per input (5+)
- [ ] Error handling for each failure mode
- [ ] Empty / first-use state covered
- [ ] Concurrent considered (if collab)
- [ ] Accessibility baseline covered
- [ ] Security considered (per feature sensitivity)
- [ ] Performance considered (per feature sensitivity)
- [ ] Localization considered (if i18n)
- [ ] Cross-platform considered (per supported)
- [ ] Priorities assigned (P0/P1/P2)
- [ ] Coverage reviewed at sprint planning
