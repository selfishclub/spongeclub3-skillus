# Core Rules & Patterns

Read this when authoring tests: the golden rules, locator priority, base config, Page Object Model, test generation from stories, and shared-auth setup.

## 10 Golden Rules

These rules are non-negotiable. Following them eliminates 90% of E2E test failures.

1. **`getByRole()` over CSS/XPath** — resilient to markup changes
2. **Never `page.waitForTimeout()`** — use web-first assertions instead
3. **`expect(locator)` auto-retries; `expect(await locator.textContent())` does NOT**
4. **Isolate every test** — no shared state between tests
5. **`baseURL` in config** — zero hardcoded URLs in tests
6. **Retries: 2 in CI, 0 locally** — retries mask flakiness in dev
7. **Traces: `'on-first-retry'`** — rich debugging without slowdown
8. **Fixtures over globals** — `test.extend()` for shared setup
9. **One behavior per test** — multiple related assertions are fine
10. **Mock external services only** — never mock your own app

## Locator Priority (Most to Least Preferred)

```
1. getByRole('button', { name: 'Submit' })     — semantic, accessible
2. getByLabel('Email address')                   — form fields with labels
3. getByText('Welcome back')                     — visible text content
4. getByPlaceholder('Enter your email')          — inputs with placeholder
5. getByTestId('submit-button')                  — when no semantic option exists
6. page.locator('.submit-btn')                   — CSS as last resort
7. page.locator('//button[@type="submit"]')      — XPath: avoid entirely
```

### Why This Order Matters

```typescript
// FRAGILE: breaks when CSS class changes
await page.locator('.btn-primary-lg').click();

// FRAGILE: breaks when DOM structure changes
await page.locator('div > form > button:nth-child(2)').click();

// RESILIENT: survives refactors, tests what users see
await page.getByRole('button', { name: 'Create account' }).click();
```

## Configuration

### playwright.config.ts

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,
  reporter: process.env.CI
    ? [['html'], ['github'], ['json', { outputFile: 'test-results.json' }]]
    : [['html']],

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    // Auth setup: runs once, shares state with all tests
    { name: 'setup', testMatch: /.*\.setup\.ts/ },

    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
      dependencies: ['setup'],
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
      dependencies: ['setup'],
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
      dependencies: ['setup'],
    },
  ],

  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 30000,
  },
});
```

## Page Object Pattern

```typescript
// pages/login.page.ts
import { type Page, type Locator, expect } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;
  readonly forgotPasswordLink: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email address');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign in' });
    this.errorMessage = page.getByRole('alert');
    this.forgotPasswordLink = page.getByRole('link', { name: 'Forgot password?' });
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message);
  }

  async expectRedirectToDashboard() {
    await expect(this.page).toHaveURL(/\/dashboard/);
  }
}
```

```typescript
// pages/dashboard.page.ts
import { type Page, type Locator, expect } from '@playwright/test';

export class DashboardPage {
  readonly page: Page;
  readonly heading: Locator;
  readonly projectList: Locator;
  readonly createProjectButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.heading = page.getByRole('heading', { name: 'Dashboard' });
    this.projectList = page.getByRole('list', { name: 'Projects' });
    this.createProjectButton = page.getByRole('button', { name: 'New project' });
  }

  async expectLoaded() {
    await expect(this.heading).toBeVisible();
  }

  async getProjectCount() {
    return this.projectList.getByRole('listitem').count();
  }

  async createProject(name: string) {
    await this.createProjectButton.click();
    await this.page.getByLabel('Project name').fill(name);
    await this.page.getByRole('button', { name: 'Create' }).click();
  }
}
```

## Test Generation from User Stories

Given a user story, generate tests following this pattern:

```typescript
// tests/e2e/auth/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../../pages/login.page';
import { DashboardPage } from '../../pages/dashboard.page';

test.describe('User Login', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('successful login redirects to dashboard', async ({ page }) => {
    await loginPage.login('user@example.com', 'password123');
    const dashboard = new DashboardPage(page);
    await dashboard.expectLoaded();
  });

  test('shows error for invalid credentials', async () => {
    await loginPage.login('user@example.com', 'wrongpassword');
    await loginPage.expectError('Invalid email or password');
  });

  test('shows validation error for empty email', async () => {
    await loginPage.login('', 'password123');
    await loginPage.expectError('Email is required');
  });

  test('shows validation error for invalid email format', async () => {
    await loginPage.login('not-an-email', 'password123');
    await loginPage.expectError('Enter a valid email');
  });

  test('forgot password link navigates to reset page', async ({ page }) => {
    await loginPage.forgotPasswordLink.click();
    await expect(page).toHaveURL(/\/forgot-password/);
  });
});
```

## Authentication Setup (Shared State)

```typescript
// tests/e2e/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate as test user', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email address').fill('test@example.com');
  await page.getByLabel('Password').fill('password123');
  await page.getByRole('button', { name: 'Sign in' }).click();

  // Wait for redirect to confirm login succeeded
  await expect(page).toHaveURL(/\/dashboard/);

  // Save authentication state for reuse
  await page.context().storageState({ path: authFile });
});
```
