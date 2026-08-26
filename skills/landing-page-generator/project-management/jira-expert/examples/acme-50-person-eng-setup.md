# Example: Jira Setup for a 50-Person Engineering Org

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Acme Analytics (B2B analytics SaaS, Series B, 80 people) just consolidated three Jira instances (one per acquired team) into a single cloud instance. The engineering org is now 50 people in five squads: Search Platform, Workspace, Onboarding, Data Platform, and Reliability. The PMO (Priya) is setting up the new instance from scratch.

The previous setups failed for predictable reasons: every squad invented its own workflow, JQL queries did not work across boards, custom fields proliferated to 187 (most unused), and automation rules were untracked and conflicted. The new setup must be opinionated, documented, and minimal.

## Inputs

- 50 engineers, 5 squads, 5 squad leads, 1 VP Engineering
- One Jira Cloud instance, Premium plan
- Connected: GitHub, Slack, PagerDuty, Confluence
- Constraint: 12 custom fields maximum; one company-wide workflow with squad-specific extensions only by exception
- Naming convention: `<SQUAD>-<NNNN>` (e.g., `SEARCH-1042`)

## Applying the skill

1. **Define the projects and naming convention** before anything else.
2. **Design one canonical workflow** and a small set of issue types.
3. **Limit custom fields** to a documented list -- everything else is rejected.
4. **Write the JQL query library** that the org will use day-to-day.
5. **Define automation rules** as code (YAML-ish) in Confluence, not just in the Jira UI.
6. **Build the standard dashboards** every squad/lead/VP uses.

## The artifact

### Project structure

| Key | Project name | Type | Lead |
|-----|--------------|------|------|
| SEARCH | Search Platform | Software (Scrum) | Sarah Khoury |
| WS | Workspace | Software (Scrum) | Marcus Vella |
| ONB | Onboarding | Software (Kanban) | Jin Lee |
| DATA | Data Platform | Software (Scrum) | Tomas Veliz |
| REL | Reliability | Software (Kanban) | Ramon Cortes |
| PMO | PMO Cross-Project | Service Management | Priya |
| ARCH | Architecture Decisions | Business | Devraj (VP Eng) |

### Issue types (canonical)

- Epic (planning level, has Fix Version)
- Story (user-facing change)
- Task (technical work, no user-visible change)
- Bug (defect in shipped behavior)
- Spike (time-boxed investigation; outputs are docs, not code)
- Incident (created automatically from PagerDuty; closed via post-mortem doc)

### Canonical workflow (one-size-fits-most)

```
Backlog -> Ready -> In Progress -> In Review -> Verified -> Done
                                                          \-> Won't Do (terminal)
```

Transitions:
- Backlog -> Ready: requires Definition of Ready checklist passing (linked to a Confluence page)
- In Progress -> In Review: requires linked PR
- In Review -> Verified: requires PR merged + linked deployment record
- Verified -> Done: requires acceptance criteria checked off

**Exceptions** (granted, documented, dated):
- REL adds `In Progress -> Paged` transition (for active incident states)
- DATA adds `Verified -> Data QA` step (one-day async data validation)

### Custom field allowlist (12 max)

| # | Field name | Type | Purpose |
|---|-----------|------|---------|
| 1 | Squad | Single-select | Search/Workspace/Onboarding/Data/Reliability |
| 2 | Story Points | Number | Standard agile points |
| 3 | RICE Score | Calculated number | `(Reach * Impact * Confidence) / Effort` |
| 4 | Fix Version | Multi-select | Release version |
| 5 | Customer Impact | Single-select | None / Low / Medium / High / SEV |
| 6 | Definition of Ready | Checkbox | DoR checklist (5 items) |
| 7 | Acceptance Criteria | Wiki text | WWAS-style criteria |
| 8 | Linked PR | URL | GitHub PR (auto-populated) |
| 9 | Deploy Record | URL | Deployment ID (auto-populated) |
| 10 | Risk Score | Single-select | L/M/H |
| 11 | OKR Link | URL | Link to OKR (Quarterly) |
| 12 | Post-Mortem Doc | URL | Confluence link (Incident issue type only) |

### JQL query library

#### My day

```jql
assignee = currentUser()
AND statusCategory != Done
AND sprint in openSprints()
ORDER BY priority DESC, updated DESC
```

#### Squad standup query (run by all squad leads)

```jql
project = "SEARCH"
AND sprint in openSprints()
AND status in (
  "Backlog", "Ready", "In Progress", "In Review", "Verified"
)
ORDER BY status, "Story Points" DESC
```

#### Bugs aging > 30 days

```jql
type = Bug
AND statusCategory != Done
AND created < -30d
ORDER BY priority DESC, created ASC
```

#### High customer impact items in flight (VP Eng dashboard)

```jql
"Customer Impact" in (High, SEV)
AND statusCategory != Done
ORDER BY priority DESC, updated DESC
```

#### RICE top-20 (planning query)

```jql
project in (SEARCH, WS, ONB, DATA, REL)
AND statusCategory = "To Do"
AND "RICE Score" > 0
ORDER BY "RICE Score" DESC
```

(Use limit 20 in the dashboard gadget.)

#### Sprint cleanup (find orphan tickets at sprint end)

```jql
sprint = closedSprintsBefore(2)
AND statusCategory != Done
ORDER BY assignee, updated DESC
```

#### Items missing acceptance criteria (DoR enforcement)

```jql
type in (Story, Task)
AND status = Ready
AND "Acceptance Criteria" is EMPTY
```

#### Open incidents in last 30 days

```jql
type = Incident
AND created > -30d
ORDER BY priority DESC, created DESC
```

#### Items linked to a specific OKR

```jql
"OKR Link" ~ "OKR-Q4-2026-O1-KR1"
AND statusCategory != Done
```

### Automation rules (the 7 we run)

#### Rule 1: PR-merged -> Verified

```yaml
trigger: github_pr_merged
condition: branch_name matches "^[A-Z]+-\d+-.*"
action:
  - extract issue_key from branch_name
  - transition issue from "In Review" to "Verified"
  - add_comment "Merged via {{pr.url}}"
  - set field "Linked PR" = pr.url
```

#### Rule 2: PR-opened -> In Review

```yaml
trigger: github_pr_opened
action:
  - transition issue from "In Progress" to "In Review"
  - link pr.url to issue
```

#### Rule 3: PagerDuty incident -> Incident issue

```yaml
trigger: pagerduty_incident_created
action:
  - create_issue:
      project: REL
      type: Incident
      summary: pagerduty.summary
      priority: pagerduty.priority
  - set field "Customer Impact" = mapped_from_pagerduty_severity
  - notify Slack channel #eng-incidents
```

#### Rule 4: Bug aged > 60 days -> escalate

```yaml
trigger: schedule_daily
jql: "type = Bug AND statusCategory != Done AND created < -60d"
action:
  - add_label "aging-bug"
  - notify squad_lead via Slack DM
  - add to weekly squad-health digest
```

#### Rule 5: Acceptance Criteria empty -> auto-comment in standup

```yaml
trigger: status_transition_to "Ready"
condition: field "Acceptance Criteria" is empty
action:
  - revert to "Backlog"
  - add_comment: "Auto-reverted: Definition of Ready not met -- Acceptance Criteria empty."
  - notify assignee + reporter
```

#### Rule 6: Customer-Impact High -> notify VP Eng

```yaml
trigger: field_changed "Customer Impact"
condition: new value in (High, SEV)
action:
  - send_email vp_eng@acme.com
  - tag in Slack #cs-escalations
```

#### Rule 7: Sprint end -> archive orphans

```yaml
trigger: sprint_completed
jql: "sprint = ${sprint.id} AND statusCategory != Done"
action:
  - add_comment "Auto-archived from Sprint {{sprint.name}}; revisit in next planning."
  - remove from sprint (return to backlog)
```

### Standard dashboards

#### Dashboard: Squad Health (each squad lead)

Gadgets:
1. Sprint Burndown
2. JQL: My-squad in-progress (linked to "Squad standup query")
3. JQL: My-squad bugs aging > 30 days
4. JQL: Items missing Acceptance Criteria
5. Velocity chart (last 6 sprints)
6. Customer-impact High/SEV in my squad

#### Dashboard: VP Engineering

Gadgets:
1. Cross-squad in-progress count by squad
2. Open incidents last 30 days
3. High-customer-impact tickets in flight
4. RICE top-20 across all squads
5. Aging bugs > 60 days (escalated)
6. Sprint goal commitment vs delivered (each squad)

#### Dashboard: PMO weekly status pull

Gadgets:
1. JQL for current sprint per squad
2. Filtered list: changes shipped in last 7 days, grouped by squad
3. Items linked to current quarter OKRs
4. DACI decisions due this week (PMO project)

### Permission scheme (simple)

| Role | Can do |
|------|--------|
| Engineer | Create/edit own issues; transition through workflow; view all |
| Squad Lead | All of Engineer + edit anyone's issue in own project + manage sprints |
| PM | All of Squad Lead across PM-owned projects |
| Admin | Schema and workflow changes; one person per squad designated |

### Documentation handoff

A single Confluence page titled "Jira Conventions at Acme" lists:
- Issue type definitions + when to use each
- The canonical workflow with allowed transitions
- The 12 custom fields and why they exist
- JQL queries (above)
- All 7 automation rules (above) with their owners
- The exception process: who approves a custom field, new workflow, etc.

Every new engineer reviews this on day one.

## Why this works

- One canonical workflow + a small, deliberate exception process. Squads cannot invent workflows in private.
- Custom fields capped at 12. New requests must displace an existing field or be rejected.
- JQL queries are a *library*, not folklore. Same query works everywhere because the schema is consistent.
- Automation rules are documented as code in Confluence with named owners. Rules that drift get caught at quarterly review.
- Dashboards are role-targeted (squad lead, VP Eng, PMO). No "everyone dashboard."
- Permission scheme is simple. Most engineers do not need fine-grained access; they need to ship.

## What's next

- Lift dashboards into Confluence reports via `../confluence-expert/`.
- Use `../sprint-retrospective/` to track which automation rules are working.
- For cross-team coordination, the PMO project uses `../execution/dependency-map/`.
- New PM onboarding: read this page, build their first dashboard. Covered by `../career/pm-onboarding/`.
- Reconsider field allowlist quarterly; remove fields with low engagement.
