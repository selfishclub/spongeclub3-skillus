# Example: Shared Dashboards PRD (Acme Analytics)

> Real-world scenario showing the standard 8-section PRD applied end-to-end.

## Context

Acme Analytics is a Series-C B2B analytics SaaS. Customer Success has heard repeatedly that customers want to share read-only dashboards with their own clients during QBRs. Today they screenshot or PDF-export and lose interactivity. Sales has named "shared dashboards" in 4 deal-review calls in the last 6 weeks.

The PM (Devi Rao) has cleared discovery: brainstormed ideas, identified assumptions, run a concierge experiment with 10 customers (8 of 10 generated >=3 share links in 4 weeks), and a pre-mortem. The next artifact is the PRD that funds the build.

## Inputs

- 11 customer interviews + 4 sales-call notes
- Concierge MVP results: 8/10 generated >= 3 share links in 4 weeks (KR exceeded)
- Engineering capacity: 1 squad, ~6 weeks
- Working Backwards PR drafted in `prfaq/`
- Pre-mortem risks: data-leak via stale link, EU residency, performance under load

## Applying the skill

1. **Ran the Problem Framing Canvas** with two CSMs to ground Section 3 (Background) and Section 5 (Market Segments) in the user's situation, not features.
2. **Used the Working Backwards PR** drafted in `prfaq/` as the source narrative for Section 6 (Value Proposition).
3. **Filled the 8 sections** from `assets/prd-template.md`.
4. **Hard-named who decides what** in Section 2 (Contacts), wired into a DACI matrix in `daci-framework/`.
5. **Set the Section 8 release stages** to feed `feature-flag-strategy/` and `beta-program/`.

Key decision quoted: *"Section 7 names what is OUT of v1 by name -- PDF export, white-label branding, custom domain. The single biggest PRD failure is silent scope expansion."*

## The artifact

````markdown
# PRD: Shared Dashboards v1

**Status:** Approved for build
**Author:** Devi Rao (PM Growth)
**Reviewers:** N. Okafor (EM), E. Lindqvist (Design Lead), J. Liu (PMM), M. Hughes (Legal), T. Park (Head of CS)
**Sponsor:** C. Bell (VP Product)
**Date:** 2026-05-22
**Target GA:** 2026-07-14 (Acme user conference)

## 1. Summary

A new capability that lets Acme Analytics customers share read-only dashboards with stakeholders outside their workspace via a secure, expiring link. Aimed at mid-market customers running QBRs with their own clients; replaces the current screenshot / PDF workflow with live, refreshable views.

## 2. Contacts

| Role | Name |
|---|---|
| PM (Driver) | Devi Rao |
| Engineering Manager | N. Okafor |
| Design Lead | E. Lindqvist |
| Product Marketing | J. Liu |
| Customer Success | T. Park |
| Legal & Privacy | M. Hughes |
| Security | R. Diaz |
| Exec Sponsor | C. Bell |

## 3. Background

Acme has 3,400 paying workspaces. Of those, 1,180 are mid-market customers whose primary use of Acme is internal reporting. In interviews and CSM logs, mid-market customers describe a recurring problem: when they want to show analytics to their own clients (during QBRs, board reviews, vendor-management meetings), they either screenshot the dashboard (losing interactivity), export a PDF (losing freshness), or grant a guest seat (violating their procurement policy or running up Acme seat cost).

Today's workaround costs:

- Sales: 4 mid-market deals stalled in Q1 over "no native share" feedback (Source: HubSpot deal-loss tags)
- CSM: estimated 6 hours/week per CSM rebuilding screenshot decks ahead of customer calls
- Customer: ~45 min per QBR re-keying data into client-facing slide decks

Competitor signal: Tableau Cloud and Looker Studio both ship share-link features; Mode shipped one in Q1 2026. The capability has become table stakes for mid-market analytics.

### Problem Framing Canvas (condensed)

**I am** a head of analytics at a 200-1000 employee company using Acme for internal reporting.
**Trying to** show our quarterly performance to our own clients with live, accurate data.
**But** I cannot give them an Acme seat (procurement won't approve, cost adds up) and screenshots go stale within hours.
**Because** Acme has no native external-share capability.
**Which makes me feel** stuck improvising decks the night before every QBR.

## 4. Objective

**Business benefit:** unblock mid-market deals where "shareable dashboards" is a deal-loss reason; increase Pro-tier expansion attributable to this surface area.

**Customer benefit:** share read-only, interactive, refreshable dashboards with external stakeholders in under 30 seconds, with control over expiry, access, and revocation.

**Key Results (Q3 2026):**

- KR1: 60% of Pro-tier workspaces generate >= 1 share link within 30 days of GA
- KR2: 35% of Pro-tier expansions in Q3 attributed to Shared Dashboards (CSM-tagged)
- KR3: Recipient NPS >= 30 (counter-metric)
- KR4: No P0 security incident in first 90 days

## 5. Market Segments

Jobs-to-be-done, not demographics.

| Segment | JTBD | In/Out v1 |
|---|---|---|
| Mid-market head of analytics | "Share live dashboards with my external clients during QBRs" | IN -- primary |
| Mid-market CSM | "Send a board-meeting view to my exec sponsor between meetings" | IN -- secondary |
| Enterprise admin | "Comply with our data-sharing controls when allowing external view" | Partial -- enterprise security features deferred to v1.1 |
| Free-tier user | n/a | OUT v1 (feature is Pro-tier and above) |
| End-recipient (external stakeholder) | "See the live dashboard without making an account" | IN (as the consumer surface) |

## 6. Value Proposition

**Gains:**
- Live, interactive view replaces screenshots and PDFs
- 30-second link creation, no admin overhead
- Audit log of every share + view (compliance gain)
- Recipient does not need an Acme account or seat

**Pains removed:**
- "I am rebuilding slide decks every QBR" -- gone
- "I cannot prove my client viewed the data" -- audit log resolves
- "My screenshot is wrong by next morning" -- live data resolves

**AI-free value:** this is a deterministic feature -- no model, no eval set. Standard PRD applies.

**Quote from the working-backwards PR (full PR in `prfaq/`):**
> "Before Shared Dashboards we spent half a day per QBR rebuilding slides. Now we send a link and the client sees the numbers as they update. It changed how we run reviews." -- Maya Chen, Head of Analytics at Northwind SaaS

## 7. Solution

### UX overview

1. From any dashboard, a "Share" button opens a share dialog.
2. The dialog has three controls: expiry date (default 30 days), password (optional), watermark (toggle).
3. On confirm, a share URL is generated and copied to clipboard.
4. The owner sees the share in a "Shared dashboards" list with view-count, last-viewed-by, and a Revoke button.
5. The recipient opens the link, optionally enters the password, and sees a read-only Acme view branded with the owner's workspace name.

### P0 features (v1)

- Create a share link from any dashboard
- Set expiry (30, 60, 90 days) and password (optional)
- View as a read-only dashboard outside auth, with workspace branding
- Revoke a share link
- Audit log of share events: created, viewed, revoked, password-fail
- Per-workspace limit: 50 active share links (raises ceiling per tier)

### P1 (deferred to v1.1)

- PDF export from a shared link
- White-label branding (remove Acme logo on link)
- Custom domain for shared links
- Live cursor presence
- Stakeholder NPS micro-survey embedded in link

### P2 / out of scope

- Editing rights on shared dashboards (would change the security model)
- Embedded share in third-party apps (use the existing iframe embed, not this feature)
- Sharing of dashboards containing PII or sensitive customer-data fields (system blocks; user gets explicit warning)
- Real-time chat on a shared view

### Assumptions to validate

- Workspaces will tolerate the 50-link limit -- ASSUMED FALSE for top 5% of customers (audit log confirms)
- The 30-day expiry default is right -- pilot showed customers extend; revisit in v1.1
- Recipients will tolerate a password prompt -- ASSUMED true; 88% of beta recipients accepted

## 8. Release

### Stages

| Stage | Audience | Gate | Date |
|---|---|---|---|
| Alpha (internal) | All Acme employees | Zero P0 in 2 weeks | 2026-04-15 to 2026-05-13 |
| Closed beta | 25 customers (see `beta-program/`) | Gates in beta plan | 2026-05-26 to 2026-07-07 |
| Canary | 10% of Pro workspaces by random flag | Adoption 40% in canary cohort; no Sev1 | 2026-07-08 to 2026-07-12 |
| GA | All Pro and Enterprise workspaces | Full launch checklist green | 2026-07-14 |
| v1.1 | -- | After GA + 30 days, scope from beta exit memo | 2026-08-14 |

### Feature flag

- Flag: `shared_dashboards_v1` (LaunchDarkly)
- Scope: workspace-level
- Kill-switch: yes; tested 2026-05-19

### Success criteria

See Section 4 (KRs) plus the post-launch metrics tracked in `status-update-generator/`.

### Risks (from pre-mortem)

| Risk | Severity | Mitigation |
|---|---|---|
| Stale share link leaks current data after a customer is offboarded | Tiger | Revoke-on-account-delete background job; revoke-all admin action |
| EU residency violation if a non-EU recipient views EU customer data | Tiger | Region-aware share-link domain (`share.eu.acme.com` for EU tenants) |
| Performance under load (recipient view) | Paper tiger | Read replica + CDN cache; not a real risk per perf test |
| Stakeholder NPS measurement instrument is flaky | Paper tiger | Defer to v1.1 |
| Sensitive-field exposure | Tiger | Field-level deny list per workspace; warning at share creation |

### Communications

- Internal launch: 2026-07-10 all-hands
- Sales enablement: 2026-07-08 by PMM
- Customer email + in-app: GA day
- Conference keynote: 2026-07-14
- Status page entry: GA day
- Changelog entry: GA day

### Rollback plan

- Flag off (instant)
- Existing links continue to work for 24h to avoid recipient confusion
- 24h after flag-off, links 404 with a "this share is temporarily unavailable" message
- Restore data via the audit log if needed (no destructive operations in v1)

### Dependencies

| Dependency | Owner | Needed by |
|---|---|---|
| Auth-less view route in front-end | Frontend team | 2026-06-15 |
| Share-link CDN setup | DevOps | 2026-06-22 |
| EU regional share domain | DevOps | 2026-06-22 |
| HubSpot CSM attribution tagging workflow | Head of CS | 2026-07-01 |
| Legal sign-off on ToS update for external recipients | Legal | 2026-07-01 |
````

## Why this works

- Section 7 names what is OUT of v1 explicitly (PDF export, white-label, custom domain). Silent scope expansion is the #1 PRD killer.
- Section 5 uses jobs-to-be-done rather than demographics, so the segment list maps to discovery interview notes.
- Section 8 includes a rollback plan with a 24-hour grace period -- a small detail that protects recipient trust.
- KRs in Section 4 include a counter-metric (recipient NPS), so the team cannot game adoption at the expense of recipient experience.
- Risks in Section 8 are tagged from the pre-mortem categories (Tiger / Paper Tiger) for continuity with discovery artifacts.

## What's next

- Pair with [../prfaq/](../prfaq/) -- the PR/FAQ stays as the customer-facing narrative; this PRD is the build artifact.
- Hand off to [../backlog-refinement/](../backlog-refinement/) to break Section 7 features into INVEST-compliant stories.
- Coordinate launch via [../launch-playbook/](../launch-playbook/) and the closed beta via [../beta-program/](../beta-program/).
- Use [../daci-framework/](../daci-framework/) to assign decision rights on scope changes during build.
- Wire deployment via [../feature-flag-strategy/](../feature-flag-strategy/).
