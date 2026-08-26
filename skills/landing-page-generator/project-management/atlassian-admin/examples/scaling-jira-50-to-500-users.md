# Example: Northwind SaaS — Scaling Jira from 50 to 500 Users with Permission Scheme Cleanup

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Northwind SaaS is a Series-B logistics platform that just closed its Series-C. Headcount is jumping from ~120 to a planned ~520 over the next 18 months, with the first 80 hires landing in the next quarter. Jira started life three years ago as a single project with permissions managed by adding individual users one at a time. Today there are 47 projects, 38 distinct permission schemes (most one-off), 9 workflow schemes, and 312 custom fields. Quarterly access reviews have not happened. Two former employees still have admin access in the audit log.

The new IT Director has been asked by the CISO to get Jira "audit-ready" before the company starts a SOC 2 Type II observation window in 90 days. The Atlassian admin skill is being applied to do a structural cleanup so that the next 400 users can be onboarded by group, not by hand.

## Inputs

- Current Jira Cloud Premium tenant, 47 projects, 38 permission schemes, 142 active users + 23 deactivated users still in groups
- SOC 2 Type II window starts 2026-08-15 (90 days out)
- Identity provider: Okta, already in use for Confluence SSO but NOT yet for Jira
- 4 product teams + 1 platform team + 1 data team + Sales/CS organizations using Jira
- Constraint: no project downtime; cutover must be transparent to existing users
- Constraint: org admins must drop from 7 to 3 by end of cleanup

## Applying the skill

1. **Inventory first.** Pulled an audit of permission schemes, group memberships, and admin grants using the Atlassian admin API. Did NOT touch anything in week one. The discipline of "inventory before cleanup" is what separates a clean migration from an outage.
2. **Apply RBAC patterns from the skill.** Mapped Northwind's 38 permission schemes onto the four standard archetypes (Public / Team / Restricted / Admin) defined in the skill workflow. 31 of the 38 schemes collapsed into the four standards.
3. **Design groups before touching users.** Created a group taxonomy organized by team, role, and product access tier — explicitly per the skill's "Use groups, not individual permissions" best practice.
4. **SSO and SCIM before onboarding.** Configured Okta SAML + SCIM provisioning so the next 80 hires onboard automatically, not through a ticket queue.
5. **Deprovisioning cleanup pass.** Ran the deprovisioning workflow against the 23 deactivated users still in groups. This closed the SOC 2 audit finding before the observation window opened.
6. **Locked down org admin grants.** Reduced from 7 org admins to 3, enforced MFA, and added an audit log alert for any new org admin grant.

## The artifact

```
================================================================
  Northwind SaaS — Jira Admin Cleanup & Scale-Up Plan
  Project window: 2026-05-22 to 2026-08-14 (12 weeks)
  Owner: IT Director
  Auditor handoff: 2026-08-15 (SOC 2 Type II observation start)
================================================================

CURRENT STATE INVENTORY
-----------------------
Tenant:               Jira Cloud Premium, US data residency
Projects:             47 (32 active, 15 dormant — no issue activity 180d+)
Permission schemes:   38 (4 standard + 34 one-off variants)
Workflow schemes:     9
Custom fields:        312 (only 187 used in last 90 days)
Issue types:          14 (4 default + 10 project-specific)
Users:                142 active + 23 deactivated still in groups
Org admins:           7 (target: 3)
SSO:                  None (Confluence has Okta, Jira does not)
SCIM:                 Not configured
Audit log retention:  90 days (target: 365 days for SOC 2)

PHASE 1 — INVENTORY & FREEZE (Weeks 1-2)
----------------------------------------
ACTIONS
  [x] Export all permission schemes and project-scheme mappings
  [x] Export all group memberships
  [x] Export org admin grants with grant dates and grantors
  [x] Identify all schemes used by exactly 1 project (candidates
      for consolidation): 22 of 38 schemes
  [x] Identify dormant projects (15) — flag for archival
  [x] Communicate freeze: no new permission schemes or one-off
      grants for 4 weeks
  [x] Open SOC 2 evidence folder in Confluence; start logging

EXIT CRITERIA
  - Inventory exported and reviewed by IT Director + CISO
  - Freeze acknowledged by all project leads

PHASE 2 — GROUP TAXONOMY DESIGN (Week 3)
----------------------------------------
Group naming convention: <scope>-<team>-<role>
  scope:  jira | confluence | atlassian
  team:   plat | data | prod-pay | prod-route | prod-track |
          prod-bill | sales | cs | finops | sec
  role:   admin | member | viewer

Examples:
  jira-plat-admin       Platform team Jira project admins
  jira-prod-pay-member  Payments team contributors
  jira-sales-viewer     Sales org read-only access
  atlassian-org-admin   Org-level admin (limit: 3 people)

Total groups after design: 38 (down from 47 ad-hoc groups)

PHASE 3 — PERMISSION SCHEME CONSOLIDATION (Weeks 4-6)
-----------------------------------------------------
Apply the four standard archetypes from the skill:

  Public Project       9 projects   (e.g. company-wide docs,
                                     onboarding tracker)
  Team Project         24 projects  (default for all product
                                     and platform teams)
  Restricted Project   12 projects  (security, legal, finance,
                                     people, audit)
  Admin Project        2 projects   (Atlassian admin internal,
                                     vendor-management)

CONSOLIDATION TABLE (excerpt)

  Old scheme                          -> New archetype       Projects
  ------------------------------------    ------------------ --------
  Payments-Eng-Scheme-2024-v3         -> Team Project        1
  Payments-Eng-Scheme-2024-v3-mod     -> Team Project        1
  Payments-Eng-Scheme-2024-final      -> Team Project        2
  Sec-Audit-Only                      -> Restricted Project  1
  Sec-Audit-Only-v2                   -> Restricted Project  1
  ... (28 more rows)

CUTOVER PROCEDURE PER PROJECT
  1. Snapshot current scheme + audit log entry
  2. Apply new archetype scheme in a low-traffic window
  3. Spot-check: project lead can still create + transition
  4. Spot-check: external collaborator (if any) still has
     intended access
  5. Decommission old scheme after 14-day soak

Rollback: revert scheme assignment from snapshot; total
rollback time < 5 minutes per project.

PHASE 4 — SSO + SCIM (Weeks 7-8)
--------------------------------
1. Configure Okta SAML app for Atlassian Cloud
2. Test SSO with an IT admin test account
3. Test SSO with one regular user in each team (8 testers)
4. Roll SSO to org in waves:
   Wave 1 (Day 1)  IT + Platform (10 users)
   Wave 2 (Day 3)  Engineering teams (62 users)
   Wave 3 (Day 5)  GTM + Ops (70 users)
5. After 7 days at 100% SSO, enforce SSO (disable password)
6. Configure SCIM:
   - Create -> auto-assign to jira-<team>-viewer baseline
   - Update -> sync group memberships from Okta
   - Deactivate -> remove from all groups, revoke product access
7. Document SSO failure runbook (break-glass admin account
   bypasses SSO for IT Director only, MFA enforced)

PHASE 5 — DEPROVISIONING SWEEP (Week 9)
---------------------------------------
Apply the skill's user deprovisioning workflow to all 23
already-deactivated-but-still-in-groups users.

Per user:
  1. Audit owned content
     - Owned projects:   reassign to current team EM
     - Owned filters:    transfer to team-shared owner
     - Owned dashboards: transfer to team-shared owner
     - Open issues:      reassign to current backlog owner
  2. Remove from all groups
  3. Revoke product access
  4. Delete account (per Northwind policy: 90 days after exit)
  5. Document in SOC 2 evidence folder

Outcome: 23 accounts cleaned. 4 of them had owned filters
that powered active dashboards — re-pointed without breakage.

PHASE 6 — ADMIN LOCKDOWN (Week 10)
----------------------------------
Reduce org admins from 7 to 3:
  KEEP    IT Director, CISO, Atlassian-admin lead (named)
  REMOVE  4 former-team admins (2 already left company)

Controls applied:
  - MFA enforced on all org admins (was: 5 of 7)
  - Audit log alert: any new org admin grant -> Slack +
    PagerDuty to IT Director
  - Quarterly admin access review on calendar
  - Org admin actions exported daily to SIEM
  - Audit log retention raised: 90 -> 365 days

PHASE 7 — DORMANT PROJECT ARCHIVAL (Week 11)
--------------------------------------------
15 dormant projects identified. Per project:
  1. Email project lead (or last assignee if lead is gone)
  2. 14-day notice before archive
  3. Export project to Confluence summary page
  4. Archive (not delete) — keeps audit history

Result: 32 active projects remain.

PHASE 8 — DOCUMENTATION + HANDOFF (Week 12)
-------------------------------------------
Confluence runbooks created:
  - Jira permission scheme archetypes (with screenshots)
  - Group taxonomy + naming convention
  - SSO + SCIM operational runbook
  - User provisioning and deprovisioning checklists
  - Quarterly access review SOP
  - Break-glass admin procedure

SOC 2 evidence folder finalized:
  - User access review log
  - Admin grant history (last 12 months)
  - Permission scheme cutover audit trail
  - Deprovisioning sweep results (23 accounts)
  - SSO enforcement date and exception log

POST-CLEANUP METRICS
--------------------
Permission schemes:   38  -> 6   (4 archetypes + 2 sensitive)
Groups:               47  -> 38  (intentional taxonomy)
Custom fields:        312 -> 187 (125 archived after audit)
Org admins:           7   -> 3
Audit log retention:  90d -> 365d
SSO coverage:         0%  -> 100% enforced
Deactivated-but-still-grouped users: 23 -> 0

ONBOARDING THE NEXT 80 HIRES
----------------------------
With Okta + SCIM in place, onboarding a new hire is now:
  1. Hiring manager adds new hire to the Okta team group
  2. Okta SCIM creates Jira user, adds to baseline
     jira-<team>-viewer group
  3. EM grants jira-<team>-member upgrade if applicable
  Time: ~5 minutes, zero tickets

Compared to the old process:
  1. Hiring manager files Jira ticket
  2. IT manually creates user
  3. IT manually adds user to 4-7 groups copy-pasted from
     previous similar user
  4. IT manually grants product access
  5. Hiring manager files follow-up ticket because access
     was wrong
  Time: ~2 hours over ~3 business days
```

## Why this works

- **Inventory before action.** Two weeks of read-only inventory caught the 23 deactivated-but-still-grouped users that would have been an automatic SOC 2 finding. Less-experienced admins start cleaning up before they finish counting.
- **Collapsed 38 schemes to 4 archetypes.** The skill workflow names the four standard permission archetypes for exactly this reason — most one-off schemes are slight variations that should converge.
- **Group taxonomy is the leverage.** Naming convention is `<scope>-<team>-<role>`. Once the taxonomy exists, SCIM does the work. Without it, you spend forever debugging Okta group mappings.
- **SSO rolled in waves.** A big-bang SSO cutover at 142 users is fine; at 500 it would be a P1 incident. Wave rollout matches the skill's change management guidance for major changes.
- **Org admin lockdown is a separate phase.** Treated as its own phase, not buried inside SSO. Reducing 7 -> 3 admins is the single biggest SOC 2 control improvement in the project.
- **Documentation is a phase, not an afterthought.** The Confluence runbook set is what makes the cleanup hold after the consultant leaves.

## What's next

- Hand off Jira project-specific configuration (workflow tuning, custom field consolidation, JQL training) to [`../jira-expert/`](../jira-expert/).
- Hand off Confluence space governance to [`../confluence-expert/`](../confluence-expert/) — the runbook pages need a space permission scheme too.
- Use [`../atlassian-templates/`](../atlassian-templates/) to roll out standardized project templates so new projects land in the right archetype by default.
- Schedule the next quarterly access review in 90 days and connect it to [`../senior-pm/`](../senior-pm/) for portfolio-level visibility.
- For the SOC 2 observation window itself, this cleanup is the input — the audit response itself is out of scope for the agile-coach and admin skills.
