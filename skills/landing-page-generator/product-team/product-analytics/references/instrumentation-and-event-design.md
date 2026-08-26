# Instrumentation & Event Design Reference

Practical reference for designing and maintaining a product event taxonomy.

## 1. Why instrumentation matters

Bad instrumentation produces:
- Wrong numbers (the worst case)
- Missing numbers
- Numbers that take a week to compute
- Privacy and compliance exposure
- Re-instrumentation cycles that consume engineering time

Good instrumentation makes product analytics possible. The taxonomy is
the foundation — get this wrong and everything downstream is shaky.

## 2. Event categories — a workable taxonomy

A useful product event taxonomy groups events into 4 categories:

### A) Lifecycle events
Major user-state transitions.
- `user_signed_up`
- `user_activated`
- `user_invited`
- `user_subscribed`
- `user_churned`

### B) Core action events
Actions central to the value proposition.
- `message_sent`
- `file_created`
- `payment_completed`
- `playlist_played`
- `transaction_succeeded`

### C) Navigation / engagement events
Where users go and how often (less analytics value but useful for funnels).
- `page_viewed`
- `feature_opened`
- `tab_clicked` (use sparingly)

### D) System / context events
Captured for product health, not value.
- `error_occurred`
- `session_started`
- `latency_observed`

Avoid:
- Per-button-click events (volume explosion)
- Generic `event_fired` with all info in properties
- One mega-event with 50 properties

## 3. Event naming conventions

Pick one and enforce. Common choices:

### Object + Action (recommended)
`message_sent`, `file_created`, `payment_failed`

### Action + Object
`sent_message`, `created_file`, `failed_payment`

### Hierarchical
`payments.checkout.completed`, `editor.file.saved`

### What to avoid
- Mixed casing: `Message_Sent`, `messageSent`, `message_sent`
- Tenses: `message_sent` vs `sending_message` vs `send_message`
- Spaces or special chars
- Past tense vs imperative mood inconsistency
- Generic names like `click`, `view`, `event`

Document the convention; lint event names in CI.

## 4. Event properties — what to include

Each event should carry standard context properties:

### User properties
- `user_id` (immutable, internal)
- `user_segment` (free, paid, trial)
- `user_plan_tier`
- `user_creation_date` (or `user_age_days`)

### Account / company properties (B2B)
- `account_id`
- `account_segment`
- `account_plan_tier`
- `account_creation_date`

### Context properties
- `platform` (web / iOS / Android)
- `app_version`
- `experiment_assignments` (running A/B tests)
- `referrer` (acquisition source)
- `device_type`

### Event-specific properties
Only what's needed for analysis (e.g., for `message_sent`:
`channel_type`, `message_length`, `attachment_count`).

## 5. PII and privacy

Categorize each property:

| Tier | Examples | Treatment |
|------|----------|-----------|
| **Public** | Page URL, action type | OK in events |
| **Internal** | User ID, account ID | OK in events; not exported in BI |
| **Sensitive PII** | Email, name, phone | Hash or omit |
| **Restricted PII** | SSN, payment details | Never in analytics events |

Common errors:
- Email captured as `user_email` and stored in event warehouse
- Free-text fields (`search_query`, `message_content`) containing PII
- IP address stored without retention policy
- Geo at city granularity for one user (re-identification risk)

Run instrumentation reviews quarterly with privacy / DPO.

## 6. Server-side vs client-side

| Where | When | Risk |
|-------|------|------|
| Client-side | UI interactions, in-product behavior | Ad blockers, tracking blockers, network unreliability |
| Server-side | Transactions, state changes, critical metrics | Slower to add new events |
| Both | Critical user actions (e.g., signups) | Reconciliation complexity |

Practical pattern:
- All revenue / state-change events: server-side
- All UX engagement events: client-side
- Hybrid for high-importance UX events: both, with reconciliation in BI

## 7. Event schema discipline

### Schema definition
- Maintain a `events.yaml` or equivalent in the repo
- Schema includes: event name, description, owner, properties (with types), examples, version
- Linter validates events at write time and at ingestion time
- Schema in repo = code-reviewable; schema in vendor UI = no review

### Versioning
- New required property = new event version
- Renaming property = deprecate old, add new, dual-fire during transition
- Removed event = mark deprecated; track usage during sunset

### Common tooling
- Segment Protocols
- Amplitude Govern
- mParticle Data Master
- OpenLineage for ingestion-level
- Custom in-house validators

## 8. The instrumentation review

Before any feature with analytics requirements ships, run an
**instrumentation review** with:

- Engineer implementing the feature
- PM or analytics partner
- Privacy partner (if PII implications)

Cover:
- Events to be fired (with full property list)
- Source of truth (client / server)
- Naming consistency with existing events
- PII implications
- Performance impact
- Documentation update

10-minute meeting most of the time; saves weeks of cleanup later.

## 9. Common instrumentation pitfalls

- **Mass-event creation by every dev.** Naming inconsistency from week 1.
- **Tracking everything "just in case."** Volume cost + slow queries; nothing actionable.
- **No documentation.** Future analysts can't tell `message_sent` from `message_send`.
- **PII leaking into events.** Privacy nightmare; cleanup costs weeks.
- **Critical events on client only.** Ad blockers + flakiness = unreliable numbers.
- **No schema validation.** Bad events ingest; analysts find broken numbers.
- **Renaming without dual-fire.** Cohort comparisons break across the rename.
- **Free-text properties.** PII risk + impossible to aggregate.
- **No event ownership.** Orphan events accumulate.

## 10. Migration: cleaning up bad instrumentation

If you inherit a chaotic taxonomy:

### Phase 1: inventory and stabilize
- Pull all events with usage volume
- Categorize: actively-used, low-usage, orphan
- Stop the bleeding: require schema review for all new events

### Phase 2: rename and consolidate
- Identify duplicate / near-duplicate events
- Dual-fire renamed events for 1 quarter
- Update dashboards / queries to use new names

### Phase 3: deprecate
- Sunset old events with usage tracking
- Remove from code when usage = 0

### Phase 4: govern
- Schema in repo
- Linter in CI
- Quarterly review with PM + analytics + privacy

## 11. Standard event reference (B2B SaaS)

A starter catalog for a B2B SaaS product:

```yaml
# Lifecycle
- user_signed_up
- user_activated
- user_invited_collaborator
- subscription_started
- subscription_upgraded
- subscription_canceled

# Account
- account_created
- account_plan_changed
- account_admin_added
- account_seat_added

# Core actions (product-specific; replace with yours)
- project_created
- project_deleted
- file_created
- file_shared
- collaborator_added

# Engagement
- session_started
- feature_opened
- dashboard_viewed

# Notifications
- email_sent
- email_opened
- in_app_notification_shown
- in_app_notification_clicked

# Errors / system
- error_occurred
- api_rate_limit_hit
```

## 12. Common pitfalls

- **No event ownership.** Events without owners rot.
- **Vendor-specific event format.** Lock-in; migration pain.
- **Granular click tracking everywhere.** Volume cost; few insights.
- **Event names that document the implementation, not the behavior.** Hard to refactor.
- **Inconsistent units in properties.** "Duration" in seconds vs milliseconds.
- **No reconciliation between client and server.** Numbers don't match; trust dies.
