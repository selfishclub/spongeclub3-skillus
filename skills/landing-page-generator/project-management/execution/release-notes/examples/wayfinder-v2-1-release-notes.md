# Example: Release Notes for Wayfinder v2.1

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Wayfinder is a travel-tech company (Series B, 120 people) building a B2B booking-management API for tour operators. v2.1 is a quarterly release that bundles 15 categories of changes: 5 features, 4 enhancements, 3 bug fixes, 2 deprecations, and 1 breaking change with a migration path. The release ships May 22, 2026.

The PM (Liana) needs two artifacts: a *customer-facing* release notes page that highlights value and provides migration guidance, and an *internal* engineering changelog with all ticket IDs and links. The customer page goes to the docs site and gets summarized in the monthly customer newsletter. The internal page goes to Notion and is the source of truth for Support and Customer Success.

## Inputs

- 15 categories of changes, all with linked Jira tickets (WF-* IDs)
- Two audiences: customers (tour operator engineering teams) and internal staff (Support, CS, Sales Engineering)
- One breaking change (legacy bookings endpoint deprecation) with a 90-day migration window
- v2.0 release notes as the formatting template
- Release date: 2026-05-22

## Applying the skill

1. **Sort changes by audience-value, not type.** Features that move the needle for customers go first. Bug fixes go below. Deprecations and breaking changes go in their own sections with explicit migration steps.
2. **Write the customer-facing page** in active voice, name the user benefit first, follow with the technical detail.
3. **Write the internal changelog** with every ticket ID, so Support can grep when a customer reports an issue.
4. **Promote the breaking change** to its own callout at the top, including the deadline date and the migration command.
5. **Cross-link** both documents so the internal team can hand a customer the right URL on the first try.

## The artifact

---

### Customer-facing release notes (docs.wayfinder.com/releases/v2.1)

# Wayfinder API v2.1

**Released:** 2026-05-22
**Audience:** Tour operator engineering teams using Wayfinder's booking API

---

> **Breaking change ahead.** The `/v1/bookings` endpoint is deprecated and will stop accepting requests on 2026-08-20. New `/v2/bookings` endpoint available now. See "Migration: bookings endpoint" below.

---

## What's new

### Multi-leg itinerary support
Tour operators can now create itineraries with multiple legs (flight + transfer + activity) in a single API call. Previously this required three sequential calls and manual orchestration. The new `POST /v2/itineraries` endpoint accepts up to 12 legs per itinerary and returns a single confirmation reference.

- Reduces booking-creation latency from ~3.4s to ~900ms in our internal benchmarks.
- One reference number per itinerary -- supports our customers' single-record finance reporting.

### Real-time availability webhooks
Subscribe once and receive push notifications whenever inventory changes for a supplier you track. Webhook payload includes supplier ID, room/seat type, and the new availability count. Replaces the previous polling pattern that was rate-limited at 60 req/min.

### Self-serve API key rotation
You can now rotate API keys without contacting support. Generate a new key, run with both old and new keys for up to 14 days (the overlap window), then revoke the old key from the dashboard.

### Sandbox seeded data
The sandbox environment now ships with 200 realistic suppliers, 50 itineraries, and 30 mock customers. Faster onboarding -- no more "what data do I test against?"

### GraphQL alpha (opt-in)
Behind a feature flag for design-partner customers: a read-only GraphQL endpoint at `/v2/graphql`. Schema introspection enabled. Contact your account manager for access.

## Enhancements

- **Search latency.** `/v2/search` p95 dropped from 1.4s to 480ms after a query-plan rewrite.
- **Webhook retries.** Failed webhook deliveries now retry with exponential backoff over 24 hours. Previously: 3 retries over 30 minutes.
- **Better error messages.** Validation errors now include the offending field path and an example of a valid value. Saves debug time for new integrations.
- **Higher rate limits for paid plans.** Pro plan rate limit raised from 1,000 to 2,500 req/min. Enterprise unchanged at 10,000 req/min.

## Bug fixes

- Fixed: bookings created near midnight UTC could be tagged with the wrong reporting day. (WF-3041)
- Fixed: webhook signature was incorrect for payloads containing emoji characters. (WF-3104)
- Fixed: cancellation confirmation email failed to send if the booking had no associated customer email -- now correctly skipped without erroring. (WF-3201)

## Deprecations

| Item | Status | Sunset date | Replacement |
|------|--------|------------|-------------|
| `/v1/bookings` endpoint | Deprecated | 2026-08-20 | `/v2/bookings` |
| `bookingRef` field on webhook payload | Deprecated | 2026-08-20 | `itineraryRef` (covers multi-leg) |

## Migration: bookings endpoint

The legacy `/v1/bookings` endpoint will return HTTP 410 Gone after 2026-08-20.

**What you need to do:**

1. Replace calls to `POST /v1/bookings` with `POST /v2/bookings`.
2. Update your response parsers -- the response now includes `itineraryRef` (top-level) and an array of `legs[]` even for single-leg bookings (length = 1).
3. Update your webhook handlers to read `itineraryRef` instead of `bookingRef`.

**Migration command** (for our official SDKs):

```bash
npm install @wayfinder/sdk@^2.1.0
# or
pip install --upgrade wayfinder-sdk>=2.1.0
```

The SDK ships a one-call migration helper:

```javascript
import { migrateV1ToV2 } from '@wayfinder/sdk';
const migrationReport = await migrateV1ToV2({ dryRun: true });
console.log(migrationReport); // shows every v1 call your codebase will need to update
```

Need help? Email integrations@wayfinder.com or post in the #api-support Slack channel.

---

### Internal changelog (Notion: Engineering / Releases / v2.1)

# Wayfinder v2.1 -- Internal Release Changelog

**Released:** 2026-05-22
**Release manager:** Liana Petrov
**Engineering lead:** Marcus Vella
**Customer-facing notes:** [docs.wayfinder.com/releases/v2.1]

## Tickets shipped (full list)

### Features (5)

| Ticket | Title | Author | PR |
|--------|-------|--------|-----|
| WF-2810 | Multi-leg itinerary endpoint (`POST /v2/itineraries`) | tomas.k | #4521 |
| WF-2811 | Itinerary DB schema + migration | tomas.k | #4525 |
| WF-2902 | Real-time availability webhooks | priyanka.s | #4533 |
| WF-2945 | Self-serve API key rotation flow | jin.l | #4540 |
| WF-2980 | Sandbox seeded data v1 | ramon.c | #4555 |
| WF-3010 | GraphQL alpha read-only endpoint (feature-flagged) | tomas.k | #4561 |

### Enhancements (4)

| Ticket | Title | Author | PR |
|--------|-------|--------|-----|
| WF-3022 | Search latency: query-plan rewrite | priyanka.s | #4568 |
| WF-3038 | Webhook retries: exponential backoff | jin.l | #4572 |
| WF-3045 | Validation error message format | ramon.c | #4576 |
| WF-3050 | Rate limit raise: Pro 1K -> 2.5K req/min | marcus.v | #4580 |

### Bug fixes (3)

| Ticket | Title | Author | PR | Customer impact |
|--------|-------|--------|-----|-----------------|
| WF-3041 | Midnight-UTC reporting day off-by-one | priyanka.s | #4582 | 3 reports/month |
| WF-3104 | Webhook signature wrong for emoji payloads | jin.l | #4585 | 2 customers blocked |
| WF-3201 | Cancellation email crash on null customer email | ramon.c | #4590 | ~15 events/week |

### Deprecations (2)

| Ticket | Item | Sunset | Notes |
|--------|------|--------|-------|
| WF-3060 | `/v1/bookings` deprecation banner | 2026-08-20 | 90-day window |
| WF-3061 | `bookingRef` field deprecation in webhooks | 2026-08-20 | Replaced by `itineraryRef` |

### Breaking change (1)

| Ticket | Title | Mitigation |
|--------|-------|-----------|
| WF-2810 + WF-3060 | New itinerary contract + v1 deprecation | SDK migrator + 90-day window + targeted customer emails |

## Customer comms timeline

| Date | Channel | Owner |
|------|---------|-------|
| 2026-05-22 | Release notes page goes live | Liana |
| 2026-05-22 | Email to all API customers | Mira (Marketing) |
| 2026-05-29 | Migration webinar #1 | Marcus + DevRel |
| 2026-06-19 | Migration webinar #2 | DevRel |
| 2026-07-22 | Per-customer migration status email | CSM team |
| 2026-08-13 | Final reminder (7 days out) | CSM team |
| 2026-08-20 | v1 endpoint returns 410 Gone | Eng on-call |

## Support runbook update

- Re-trained Support on the new `/v2/bookings` response shape. (Done 2026-05-19)
- Updated the FAQ macros for the most common v1-to-v2 questions. (Done 2026-05-21)
- Tracking dashboard for v1 call volume by customer: linked in the on-call doc.

## Risk register entries

| Risk | Status | Owner |
|------|--------|-------|
| Customer misses deadline, gets 410 unexpectedly | Mitigated by 7-touch email cadence | CSM team |
| GraphQL alpha leaks beyond design partners | Feature-flag, rolled by Marcus weekly | Marcus |

## Why this works

- Two artifacts, two audiences. Customer page leads with value; internal page leads with ticket IDs.
- Breaking change is promoted to a callout at the very top. Nobody reads release notes top-to-bottom, but everyone reads the box that says "Breaking change ahead."
- Migration includes an actual SDK command and a `dryRun` helper -- the docs do the work for the customer.
- Internal changelog includes ticket IDs and PR numbers for every change. Support can grep for a ticket and answer a question in 30 seconds.
- Customer comms timeline is committed, not aspirational. Each touch has a date, channel, and owner.

## What's next

- Track v1 call volume daily until 2026-08-20; use `../status-update-generator/` to keep leadership informed.
- Update the deprecation tracker in `../eol-communication/` with the August 20 sunset.
- Use `../launch-playbook/` for the next major release (v3.0) to plan a broader internal/external launch.
- Roll the GraphQL alpha into a beta program via `../beta-program/` when ready.
