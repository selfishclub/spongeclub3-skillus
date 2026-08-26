# Diagnosis, Migration, CI & Quality

Read this when diagnosing flaky tests, migrating from Cypress, wiring CI, adding visual regression or accessibility checks, or auditing a suite against the quality bar.

## Flaky Test Diagnosis

### Common Causes and Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `waitForTimeout(2000)` in test | Timing-dependent | Replace with `await expect(locator).toBeVisible()` |
| Test passes locally, fails in CI | Race condition | Add web-first assertion before interaction |
| Element not found after navigation | Page not loaded | `await page.waitForURL('/expected-path')` |
| Stale element reference | DOM re-rendered | Use Playwright locators (auto-retry) |
| Different data between runs | Shared test state | Isolate with `test.beforeEach` setup |
| Flaky on slow CI runners | Insufficient timeout | Increase `expect` timeout, not `waitForTimeout` |

### Diagnosis Commands

```bash
# Run with trace on every test (not just retries)
npx playwright test --trace on

# Run a specific flaky test 10 times
for i in $(seq 1 10); do npx playwright test tests/e2e/checkout.spec.ts; done

# Show test timeline
npx playwright test --trace on
npx playwright show-trace test-results/*/trace.zip

# Run in headed mode for visual debugging
npx playwright test --headed --retries 0

# Debug a specific test interactively
npx playwright test --debug tests/e2e/checkout.spec.ts
```

## Cypress to Playwright Migration

| Cypress | Playwright |
|---------|-----------|
| `cy.visit('/path')` | `await page.goto('/path')` |
| `cy.get('.selector')` | `page.locator('.selector')` |
| `cy.contains('text')` | `page.getByText('text')` |
| `cy.get('[data-testid="x"]')` | `page.getByTestId('x')` |
| `cy.intercept('GET', '/api/*')` | `await page.route('/api/*', ...)` |
| `cy.wait('@alias')` | `await page.waitForResponse('/api/*')` |
| `cy.should('be.visible')` | `await expect(locator).toBeVisible()` |
| `cy.should('have.text', 'x')` | `await expect(locator).toHaveText('x')` |
| `cy.fixture('data.json')` | `JSON.parse(fs.readFileSync(...))` |
| `beforeEach(() => { cy.login() })` | Auth setup project + storageState |

## CI Integration

### GitHub Actions

```yaml
name: E2E Tests
on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm exec playwright install --with-deps chromium

      - run: pnpm build  # build the app first
      - run: pnpm exec playwright test
        env:
          BASE_URL: http://localhost:3000

      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7
```

## Visual Regression Testing

```typescript
// tests/e2e/visual/dashboard.spec.ts
import { test, expect } from '@playwright/test';

test('dashboard matches visual snapshot', async ({ page }) => {
  await page.goto('/dashboard');
  await page.waitForLoadState('networkidle');

  // Full page screenshot comparison
  await expect(page).toHaveScreenshot('dashboard.png', {
    maxDiffPixels: 50,  // allow small rendering differences
  });
});

test('project card component snapshot', async ({ page }) => {
  await page.goto('/dashboard');
  const card = page.getByTestId('project-card').first();

  await expect(card).toHaveScreenshot('project-card.png', {
    maxDiffPixelRatio: 0.01,
  });
});
```

```bash
# Generate/update baseline screenshots
npx playwright test --update-snapshots

# Run visual comparison
npx playwright test tests/e2e/visual/
```

## Accessibility Testing

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('login page has no accessibility violations', async ({ page }) => {
  await page.goto('/login');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();

  expect(results.violations).toEqual([]);
});

test('dashboard meets WCAG AA standards', async ({ page }) => {
  await page.goto('/dashboard');

  const results = await new AxeBuilder({ page })
    .exclude('.third-party-widget')  // exclude elements you don't control
    .analyze();

  // Log violations for debugging
  for (const violation of results.violations) {
    console.log(`${violation.impact}: ${violation.description}`);
    for (const node of violation.nodes) {
      console.log(`  - ${node.html}`);
    }
  }

  expect(results.violations.filter(v => v.impact === 'critical')).toEqual([]);
});
```

## Common Pitfalls

- **`page.waitForTimeout(N)`** — the single most common cause of flaky tests; use web-first assertions
- **CSS selectors as primary strategy** — breaks on every refactor; use role/label/text locators
- **Shared state between tests** — one test's data pollutes another; isolate with proper setup/teardown
- **No trace configuration** — debugging CI failures without traces wastes hours; enable `on-first-retry`
- **Testing third-party services** — mock external APIs; only test your own application
- **Running all browsers in development** — test Chromium locally, full matrix in CI only
- **No page objects** — duplicate locators across tests create maintenance nightmares

## Best Practices

1. **Page Object per page/component** — centralize locators, expose user-intent methods
2. **Web-first assertions everywhere** — `expect(locator).toBeVisible()` auto-retries, `waitForTimeout` does not
3. **Auth as a setup project** — authenticate once, reuse `storageState` across all tests
4. **One behavior per test** — keeps failures isolated and test names meaningful
5. **Run in CI with `--retries 2`** — but investigate any test that needs retries locally
6. **Trace + screenshot on failure** — upload as CI artifacts for post-mortem debugging
7. **Visual regression for critical UI** — catch unintended visual changes automatically
8. **Accessibility tests in the suite** — WCAG compliance as a regression gate, not an afterthought

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `locator.click()` times out | Element hidden behind overlay/modal or not yet rendered | Add `await expect(locator).toBeVisible()` before clicking; check for z-index overlays blocking the target |
| Visual snapshots fail on every CI run | Different OS font rendering between local and CI | Generate baseline screenshots inside CI (Linux), not locally (macOS); use `maxDiffPixelRatio: 0.02` for tolerance |
| Auth setup project runs but tests get 401 | `storageState` path mismatch or expired token | Verify `storageState` path in `playwright.config.ts` matches the setup script; confirm tokens don't expire mid-suite |
| `page.route()` intercept never triggers | Route pattern doesn't match the actual request URL or glob syntax error | Log requests with `page.on('request', r => console.log(r.url()))` to verify the exact URL; use `**` glob for subpaths |
| Tests pass individually but fail when run together | Shared mutable state or port collision between parallel workers | Ensure test isolation via `test.beforeEach` setup; use unique test data per worker with `test.info().parallelIndex` |
| `toHaveScreenshot()` throws "missing baseline" | Snapshot file not committed to version control | Run `npx playwright test --update-snapshots` and commit the generated files under the `__screenshots__` directory |
| Accessibility audit returns false positives | Axe scanning third-party embedded widgets or iframes | Use `.exclude('.third-party-widget')` or `.include('#app-root')` to scope the audit to your own markup |

## Success Criteria

- **Flaky test rate below 2%** — measured over a rolling 7-day window across all CI runs; any test exceeding 5% flake rate is quarantined and fixed within 48 hours
- **E2E suite completes within 10 minutes** — full cross-browser matrix (Chromium, Firefox, mobile) on CI with 4 parallel workers; alert if wall-clock time exceeds threshold
- **100% of critical user journeys covered** — login, checkout, onboarding, and core CRUD workflows each have dedicated spec files with happy-path and primary error-path tests
- **Zero `waitForTimeout()` calls in the codebase** — enforced via ESLint rule or grep-based CI check; all waits use web-first assertions
- **Page Object coverage for every tested page** — no raw locators in spec files; all element access goes through page object classes with user-intent method names
- **WCAG AA compliance gate passing** — accessibility tests run on every PR; zero critical or serious violations allowed to merge
- **Visual regression baselines reviewed on every UI PR** — screenshot diffs attached to PR as artifacts; baseline updates require explicit reviewer approval
