# Red Flags: Atlassian Admin

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them. Pair with the SKILL.md and Troubleshooting table.

## How to use this document

When you have just produced a permission scheme, workflow design, user-provisioning plan, or org-wide governance recommendation, scan the red flags below before shipping it. Each red flag names a specific failure mode and shows the *bad* version next to the *good* version.

---

## Red Flag 1: Permission Scheme Bloat

**Symptom.** The org has 40+ permission schemes — one per project, plus historical variations no one remembers creating.

**Why it's bad.** Permission scheme sprawl makes audits impossible, slows project setup to days, and produces accidental data exposure when an obscure scheme is reused as a template. Atlassian's own guidance is that most orgs need 3-5 schemes total: Default, Restricted, Confidential, Customer-Facing, External-Partner.

**Bad example:**
> "We have 47 permission schemes. New projects copy 'Eng-Default-v3-modified-2024' which inherits half-deprecated groups."

**Good example:**
> "5 canonical permission schemes (Default, Restricted, Confidential, Customer-Facing, Partner). New projects must pick one; deviations require admin approval and a documented reason. 47 -> 5 migration plan tracked in the governance project."

**How to catch it.** Count permission schemes. If the number is greater than 10 and the org has fewer than 100 projects, you have bloat.

---

## Red Flag 2: Workflow Proliferation (Workflow Per Project)

**Symptom.** Every project has its own custom workflow. No two are alike. New issue types require a new workflow.

**Why it's bad.** Custom workflows per project guarantee that automation rules, reports, and SLAs do not roll up across the org. Onboarding new teams takes weeks because each project's status names are different. The fix is workflow *families*: 3-5 canonical workflows that cover 95% of cases.

**Bad example:**
> "Each team designs its own workflow. The mobile team has 11 statuses including 'On the Bench' and 'Cooking', the platform team has 4."

**Good example:**
> "3 canonical workflow families: (a) Standard SDLC (To Do -> In Progress -> In Review -> Done), (b) Support (New -> Triaged -> Working -> Waiting -> Resolved), (c) Compliance (Draft -> Pending Review -> Approved -> Archived). Custom statuses require governance approval."

**How to catch it.** Count distinct workflow schemes. More than 8-10 across an org of 50+ projects is sprawl.

---

## Red Flag 3: Stale Group Memberships

**Symptom.** Groups contain users who left the company months ago, or service accounts no one can identify.

**Why it's bad.** Stale group memberships are the #1 audit finding in SOC 2 access reviews of Atlassian deployments. Beyond compliance, they create real risk: orphaned accounts and former employees may still have admin access to confidential spaces.

**Bad example:**
> "Group 'jira-administrators' has 23 members. 7 of them are no longer at the company. 3 are unidentified service accounts named 'svc-test-2019'."

**Good example:**
> "Quarterly access review (Q1 2026): admins-group reduced 23 -> 9. SCIM provisioning from Okta enforces deprovisioning within 24 hours of HR offboarding. Service accounts now owned by a named human; unowned accounts disabled."

**How to catch it.** Set a quarterly access-review cadence. Any group not reviewed in 90+ days is presumed stale.

---

## Red Flag 4: Admin Privileges as the Default

**Symptom.** A long list of users with org admin or site admin access "because they sometimes need to change things."

**Why it's bad.** Least-privilege is a foundational security principle. Every additional admin is a blast-radius multiplier. If 30 people are admins, the org effectively has no privilege boundary, and SOC 2/ISO 27001 auditors will flag it.

**Bad example:**
> "Org admins: 28 users (including 12 EMs, all PMs, plus all of platform team)."

**Good example:**
> "Org admins: 4 users (CTO, IT director, 2 platform-on-call rotation). Project admin role used for team-level changes. Privileged Access Management (PAM) workflow for time-boxed admin elevation."

**How to catch it.** If the number of org admins exceeds 5 (or 1% of total users, whichever is larger), audit and reduce.

---

## Red Flag 5: SSO Configured but Local Logins Still Enabled

**Symptom.** SAML SSO is enabled, but Atlassian-account password login is also enabled "as a backup."

**Why it's bad.** This defeats SSO. Users can bypass MFA, IP allowlists, and conditional-access policies enforced by the IdP simply by logging in with their Atlassian password. Compromised credentials become a single point of failure.

**Bad example:**
> "SSO is enabled. Users can also log in with Atlassian password (used as a fallback during the IdP outage in 2024)."

**Good example:**
> "SSO enforced for all human users. Break-glass account (1 named, audited, password vaulted in 1Password) for IdP outage. API tokens scoped per integration. Atlassian password login disabled."

**How to catch it.** Audit the authentication policies. If multiple methods are allowed without an explicit reason and audit log, fix it.

---

## Red Flag 6: Custom Fields as a Junk Drawer

**Symptom.** 200+ custom fields, many created ad-hoc, half of them named "ID" or "Status" or "Priority" with no context.

**Why it's bad.** Each custom field has a real performance cost (Jira indexes them globally). Beyond performance, field sprawl makes JQL queries unreliable: which "Status" did you mean? Reports break, dashboards lie, automation rules fire on wrong fields.

**Bad example:**
> "247 custom fields. 18 named some variant of 'Priority'. 31 with no owner. Field 'tshirt size' exists in 2 projects."

**Good example:**
> "Field governance: 40 canonical fields with clear owners and definitions. New field requests go through a request form (justification, owner, scope). Quarterly cleanup of zero-usage fields. JQL aliases maintained for legacy queries."

**How to catch it.** Run a custom-field usage report. Any field used in fewer than 3 issues across the org is a candidate for deprecation.

---

## Red Flag 7: 2FA "Recommended" but Not Enforced

**Symptom.** Security policy says "users should enable 2FA" but it is not required. Compliance dashboard shows 60% adoption.

**Why it's bad.** Voluntary 2FA is a coin flip on whether the user with admin privileges has it. Phishing attacks succeed on the 40% who did not opt in. SOC 2 CC6.1, ISO 27001 A.9, and most regulator guidance require enforced MFA for privileged access.

**Bad example:**
> "2FA recommended via email reminders. Adoption: 62%."

**Good example:**
> "2FA enforced via IdP for all human users. API integrations use service accounts with scoped tokens. Adoption: 100% (enforced, not requested). Privileged access requires hardware key (FIDO2)."

**How to catch it.** If 2FA adoption is less than 100% for any user with project-admin or higher, it is not enforced.

---

## Red Flag 8: No Audit Log Retention Strategy

**Symptom.** Audit logs are enabled in the product UI but never exported, never reviewed, and may roll off after 6 months.

**Why it's bad.** Audit logs are evidence for security incidents and compliance audits. If you cannot produce who-did-what-when going back 12 months, you fail SOC 2 CC7.2 and have no forensic trail when an incident occurs.

**Bad example:**
> "Audit logging enabled in Jira. We can see the last 30 days in the UI."

**Good example:**
> "Audit logs streamed to SIEM (Splunk) via REST API. 13-month retention. Monthly review for anomalies (admin grants, permission changes, mass deletes). Quarterly access-review report generated from audit data."

**How to catch it.** Ask: "show me who granted admin to X in February 2025." If you cannot, your audit posture is broken.

---

## Red Flag 9: Marketplace Apps Without Owner or Review

**Symptom.** 30+ marketplace apps installed. Half have not been used in a year. None have a designated owner. No review of vendor security posture.

**Why it's bad.** Marketplace apps are third-party code with access to Jira/Confluence data. Each is a supply-chain risk. Unused apps still consume licenses and may auto-update with new permissions. A breached app is a breached Atlassian instance.

**Bad example:**
> "37 marketplace apps installed across Jira and Confluence. App usage report has not been generated."

**Good example:**
> "Marketplace app policy: each app requires (1) named owner, (2) business justification, (3) vendor security review (SOC 2 minimum), (4) quarterly usage check. Currently 12 apps installed, all in-scope. Annual security review for SaaS vendors."

**How to catch it.** Pull the app inventory. Apps with no owner or 0 usage in 90 days are candidates for removal.

---

## Red Flag 10: Project Categories Misused as Permissions

**Symptom.** Sensitive projects (HR, legal, M&A) are protected only by project category labels, not by permission schemes or space restrictions.

**Why it's bad.** Project categories are a *navigation* feature, not a *security* feature. Anyone who can list projects can see the names. Sensitive metadata leaks (project titles, issue counts, assignees) even when content is restricted.

**Bad example:**
> "HR projects are in the 'HR' category, which is hidden from the main project list."

**Good example:**
> "HR projects use a Confidential permission scheme: browse-project restricted to HR group only. Project category is metadata, not a control. Space-level restrictions in Confluence mirror Jira permissions."

**How to catch it.** Test as a non-privileged user: can you see project names, issue counts, or assignees you should not? If yes, the protection is cosmetic.

---

## Red Flag 11: Bulk Changes without Dry-Run

**Symptom.** Admin proposes a bulk operation ("re-assign all issues from old project to new", "change all permission schemes for engineering") and executes directly in production.

**Why it's bad.** Bulk operations in Jira are largely irreversible. A misconfigured JQL filter can mass-modify thousands of issues, and Atlassian's undo support is limited. The fix is a documented dry-run discipline.

**Bad example:**
> "I am moving all issues from project ABC to project XYZ via bulk move. Click confirm."

**Good example:**
> "Dry-run: JQL match returns 1,247 issues. Sample 10 reviewed manually. Backup taken (project export). Change window scheduled. Communication sent to affected teams. Execute in chunks of 200 with verification after each chunk."

**How to catch it.** Every bulk operation must produce a written change record: JQL preview, sample verification, backup, rollback plan.

---

## Red Flag 12: Sandbox/Staging Environment Skipped for Config Changes

**Symptom.** Workflow, screen scheme, or notification scheme changes are made directly in production "because it's just a small change."

**Why it's bad.** Even small workflow changes can cascade: a renamed status breaks automation rules, dashboards, and external integrations. The Atlassian Cloud sandbox (or a DC staging instance) exists specifically to catch these before users notice.

**Bad example:**
> "I added a new status 'Waiting on Legal' to the workflow. Rolled out at 3pm Friday."

**Good example:**
> "Workflow change tested in sandbox. Impact analysis: 4 automation rules and 2 dashboards reference status names; 1 needed updating. Change window: Tuesday 10am, with 1-hour bake-in monitored. Rollback: restore previous workflow scheme from snapshot."

**How to catch it.** Any change to schemes (workflow, screen, notification, permission, custom field) goes to sandbox first. Production changes require a dated change record.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Permission Scheme Bloat | Do you have fewer than ~10 schemes? |
| 2 | Workflow Proliferation | Are most projects on a canonical workflow family? |
| 3 | Stale Group Memberships | Last access review within 90 days? |
| 4 | Admin Privilege Default | Org admin count under 5 (or 1%)? |
| 5 | SSO with Local Login Fallback | Local password login disabled? |
| 6 | Custom Field Junk Drawer | Custom field count under 50, all with owners? |
| 7 | 2FA Optional | 2FA enforced at 100% via IdP? |
| 8 | No Audit Log Retention | Can you query who-did-what 12 months ago? |
| 9 | Marketplace Apps Unowned | Every app has an owner, justification, security review? |
| 10 | Categories as Permissions | Tested project visibility as non-privileged user? |
| 11 | Bulk Changes without Dry-Run | Dry-run + sample verification + rollback documented? |
| 12 | Skipping Sandbox | Scheme changes tested in sandbox first? |

## Related Reading

- SKILL.md Troubleshooting section (for symptom -> root cause -> resolution)
- references/permission-model.md (for the canonical permission scheme design, if present)
- references/governance.md (for org-wide policy templates, if present)
