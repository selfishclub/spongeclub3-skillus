# Example: Rewriting 10 Northwind Backlog Items in Why-What-Acceptance Format

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Northwind SaaS (Series C fintech, 200 people) is mid-Q4 and the Treasury Core squad's backlog is full of stories that read like specs. Engineers complain that they keep building features that "technically pass" but miss the user intent. Tomas (Treasury lead) and Ines (Head of Product) agreed: every backlog item from now on must follow Why-What-Acceptance (WWAS) before it enters refinement.

The PM (Ana) is rewriting 10 existing backlog items as a forcing function -- and as a teaching example for the rest of the PM team. The original items came from Jira and from a sales-driven escalation slack.

## Inputs

- 10 existing backlog items, all in "spec" format (no "why")
- Northwind's product: a multi-entity treasury platform for mid-market companies
- Target audience for items: 14 engineers + 3 designers
- Constraint: each rewrite must be <=200 words and pass an "outsider readability" test

## Applying the skill

For each item: capture **Why** (the user/business reason), **What** (the user-visible change), and **Acceptance** (the testable conditions that prove "done"). Cross-check that the Why is not a paraphrase of the What.

## The artifact

---

### 1. "Add bulk approve button" (original) -> WWAS

**Why.** Treasury operators at Skyway and Northwind's other top-15 accounts process 80-200 payments a day. Today each approval is a click + a confirm modal = ~7 seconds per payment. At scale that is 14-24 minutes of pure clicking per day per operator. Two operators quit citing "the click work" in their exit interview.

**What.** Operators can multi-select payments in the queue and approve them in a single action (with a single confirm-modal listing the count).

**Acceptance.**
- Multi-select with shift-click + Cmd/Ctrl-click + "Select all on page."
- Bulk approve action requires a single confirm modal listing the count and total amount.
- All-or-nothing: if any payment in the batch fails validation, the bulk action is rolled back atomically.
- Audit log records each underlying approval with the bulk-action correlation ID.
- Bulk approve disabled when more than 250 items selected (UI banner explains the limit).

---

### 2. "Add CSV export to dashboard" (original) -> WWAS

**Why.** Finance teams using Northwind reconcile against their ERP weekly. Today they screenshot the dashboard. Three of our top-25 accounts have asked for CSV export in the last 30 days; two of them said "or we cannot expand."

**What.** Any dashboard chart or table on the Northwind UI has a "Download CSV" action that exports the underlying data.

**Acceptance.**
- "Download CSV" button visible on every chart/table for users with the Finance role.
- CSV uses RFC 4180 quoting; opens correctly in Excel + Google Sheets + Numbers.
- Includes column headers in row 1 matching the dashboard column names.
- Respects the same date-range and filters as the current dashboard view.
- File name pattern: `<dashboard-name>_<YYYY-MM-DD>_<account-name>.csv`.
- Audit log entry per export with user, account, dashboard, and filters.

---

### 3. "Add weekly email digest" (original) -> WWAS

**Why.** Treasury managers (the buyers, not the daily users) want a passive way to stay informed without opening the app daily. Customer interviews of 12 treasury managers showed 11 of 12 do not log in more than once a week and only when alerted.

**What.** Treasury managers receive a weekly email summarizing flows, exceptions, and overdue items for their entities.

**Acceptance.**
- Default schedule: Monday 08:00 in user's local timezone; configurable in user preferences.
- Email contains: total flows last week, exceptions count + top-5, overdue approvals count + named items, and a deep link per item.
- Unsubscribe in one click; respected within 5 minutes.
- Branded with account workspace name; multi-entity managers get one email summarizing all their entities.
- Email send tracked in audit log; deliverability monitored in Postmark dashboard.

---

### 4. "Support OAuth login" (original) -> WWAS

**Why.** Three enterprise prospects (Skyway, Riverdale, Halverson) require SSO via their IdP as a contractual gate. Without it we cannot close any of the three; total ARR opportunity is $720K.

**What.** Users can sign in to Northwind via their company's SAML or OAuth IdP. Account admins configure the IdP connection from the workspace settings.

**Acceptance.**
- SAML 2.0 + OIDC supported via WorkOS.
- Account admin can configure IdP from `Workspace settings -> SSO`.
- Once SSO is enforced, password login is disabled for that workspace's users (admin retains break-glass).
- JIT provisioning: user logging in via IdP is created in Northwind with role mapped from IdP attribute (configurable).
- Audit log: SSO config change, JIT provisioning event, login events tagged "SSO."

---

### 5. "Add audit log search" (original) -> WWAS

**Why.** Northwind's SOC 2 Type II audit (in progress, evidence by 2026-12-15) requires demonstrable audit-log search. Auditors will ask for "who approved payment X on day Y?" and we need to answer in under 60 seconds.

**What.** Account admins can search the audit log by user, action type, resource ID, and date range.

**Acceptance.**
- Search fields: user (email or ID), action type (multi-select), resource ID (free text), date range.
- Returns results in <=2 seconds for any 30-day window with up to 100K events.
- Results paginated, 50 per page, CSV export of the current result set.
- Permission: Admin role only. Other roles see "Forbidden" with a clear message.
- Audit log entry recorded when an admin searches the audit log (yes, this is intentional).

---

### 6. "Multi-currency support" (original) -> WWAS

**Why.** Skyway has entities in three countries and bills in USD, EUR, and GBP. Today they have to keep three separate Northwind workspaces. We are blocking Skyway's expansion to enterprise tier ($240K ARR uplift).

**What.** A single entity in Northwind can hold balances and transact in multiple currencies. Display currency is per-user. Reporting offers consolidated view in account base currency.

**Acceptance.**
- Entity-level setting: enabled currencies (subset of supported list).
- Display currency persisted per-user; UI toggle in top bar.
- All transactions store native currency + amount + FX rate (rate from xe.com, snapped at transaction time).
- Consolidated reporting uses the account base currency with all FX conversions shown alongside.
- Audit log records currency conversions and FX rate snapshots.
- Supported currencies in v1: USD, EUR, GBP, CAD, AUD, JPY, CHF (others deferred).

---

### 7. "Add approval workflow" (original) -> WWAS

**Why.** Today every payment requires one approval, regardless of amount. Two of our largest customers ($120K, $180K ACV) have separation-of-duties controls that require *different* approvers above thresholds. Loss of these accounts is a real risk if we cannot offer this in Q4.

**What.** Account admins can define approval policies: thresholds with required approver roles per threshold.

**Acceptance.**
- Policy editor: rule format = "amount >= X requires approver from role Y; amount >= Z requires two approvers from role Y."
- Up to 3 thresholds per policy.
- Self-approval blocked: initiator cannot be approver.
- Out-of-policy payments cannot leave "Pending Approval" state.
- Policy changes audit-logged with before/after.
- Default policy out of box: "any amount requires 1 Treasurer approval."

---

### 8. "Improve search relevance" (original) -> WWAS

**Why.** Operators complain that searching for "ACH return reason R01" surfaces irrelevant results. Operator team logged 48 "could not find what I was looking for" incidents in Q3. Operator productivity is impacted; one mentioned the issue in a customer call.

**What.** Search returns higher-relevance results for known operator query patterns (transaction IDs, return reason codes, entity names).

**Acceptance.**
- "Search for transaction ID" returns the exact transaction as the top hit when ID matches.
- "Search for return reason code" (e.g., "R01") returns transactions tagged with that code.
- "Search for entity name" returns the entity page as the top hit.
- p95 search latency <=500ms.
- Operator team validates by closing 40 of the 48 Q3 incidents as "this query now returns the right result."

---

### 9. "Implement webhook signing" (original) -> WWAS

**Why.** Customer security teams need to verify that webhooks originated from Northwind, not from a spoofer. This is on the SOC 2 audit punch list and is a frequent question in security reviews -- five blockers logged this quarter.

**What.** All Northwind-emitted webhooks include an HMAC-SHA256 signature header that customers can verify with a shared secret.

**Acceptance.**
- `X-Northwind-Signature` header on every outbound webhook: `t=<unix-ts>,v1=<hex-hmac>`.
- Shared secret rotatable from `Workspace settings -> Webhooks`; rotation supports overlap window (both old + new accepted for 14 days).
- Docs page with sample verification code in Node.js, Python, and Go.
- Existing webhooks continue to work; signing is additive.

---

### 10. "Add 2FA" (original) -> WWAS

**Why.** Two prospect security reviews flagged "no 2FA" as a finding (Skyway pilot, Halverson RFP). Treasury operators handle high-value movements; lack of 2FA is a credible risk and a procurement blocker.

**What.** Users can enable TOTP-based 2FA on their account; workspace admins can require 2FA org-wide.

**Acceptance.**
- TOTP setup with QR code + manual key option.
- 10 single-use recovery codes generated at setup.
- Workspace admin can set "2FA required" policy; non-compliant users prompted to enroll within 7 days.
- "Remember this device" option for 30 days.
- Audit log: 2FA enrolled, 2FA disabled, recovery code used.
- v1 supports TOTP only (SMS deferred; security team flagged SMS as low-trust).

---

### Side-by-side: an item before/after WWAS

**Before:**
> "Add bulk approve button. Treasury operators need to approve payments faster."

**After (see item 1):** 180 words with 5 testable acceptance criteria and a clear user-impact "why."

The original could be implemented half a dozen wrong ways. The WWAS version cannot.

## Why this works

- Each Why is grounded in a real artifact -- a customer name, a number, an exit interview, a contractual gate. Whys that say "users need this" are not Whys; they are Whats in disguise.
- Each Acceptance set is *testable*. "Easy to use" is not an acceptance criterion; "p95 search latency <=500ms" is.
- Negative space is included where it matters: item 6 says "USD, EUR, GBP, CAD, AUD, JPY, CHF -- others deferred." item 10 says "v1 supports TOTP only." This protects scope from later "but it should also..." conversations.
- WWAS items are short enough to read in 60 seconds and clear enough that an engineer can start work without further clarification.
- Items reference each other where they belong together (e.g., item 5 audit log search supports item 4's SSO audit events).

## What's next

- Score the rewritten items via `../prioritization-frameworks/` (RICE).
- Apply `../story-splitting/` to items that came out larger than one sprint (items 6, 7).
- Verify Definition of Ready via `../backlog-refinement/`.
- Push the WWAS pattern into the Notion backlog template via `../../notion-pm/`.
- Use `../create-prd/` for items that warrant a full PRD (items 4, 6, 7).
