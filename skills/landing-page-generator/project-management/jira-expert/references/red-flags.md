# Red Flags: Jira Expert

> Common ways this skill's output goes wrong -- concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan every Jira configuration change, JQL query, automation rule, or dashboard before publishing to a team. Each red flag has bad and good quoted examples.

---

## Red Flag 1: Workflow Proliferation

**Symptom.** Each project has its own custom workflow with 12+ states; the org has 47 distinct workflows across 30 projects.
**Why it's bad.** Workflow proliferation makes cross-project reporting impossible (no shared statuses), trains every new joiner from scratch, and means automation rules cannot be reused. The Jira admin spends most of their week mapping workflow A's "In Review" to workflow B's "Code Review In Progress".
**Bad example:**
> "Project A workflow: Open -> In Triage -> Ready -> In Progress -> In Code Review -> In QA -> Ready for UAT -> In UAT -> Done -> Closed -> Archived.
> Project B workflow: To Do -> Doing -> Reviewing -> Validated -> Released.
> (Cross-project velocity report breaks.)"
**Good example:**
> "Org-wide shared workflow: Open -> In Progress -> In Review -> Done. Custom states *only* in projects with a defended exception (e.g., regulated team needs an explicit 'Awaiting QA Signoff' state). Exceptions logged in the Jira-admin charter."
**How to catch it.** Count distinct active workflows. > 5 across the org = proliferation; consolidate.

---

## Red Flag 2: JQL Spaghetti

**Symptom.** Filters and dashboards use 200-character JQL queries with nested AND / OR / NOT chains nobody can read.
**Why it's bad.** Spaghetti JQL is unmaintainable. The original author leaves; the query becomes load-bearing infrastructure nobody dares touch. Subtle bugs (an OR scoping wrong, a missing parenthesis) silently exclude tickets.
**Bad example:**
> "project in (PROJ, OPS, INFRA) AND ((status not in (Done, Closed) AND assignee in membersOf('eng-team')) OR (labels in (urgent, blocker) AND status != Done)) AND created >= -90d AND (component != 'legacy' OR resolution = Unresolved)"
**Good example:**
> "Saved filter `Eng Active Work` (definition stored in `jira-filters.md` with comments):
> ```
> project in (PROJ, OPS, INFRA)
> AND status != Done
> AND (assignee in membersOf('eng-team') OR labels in (urgent, blocker))
> AND created >= -90d
> ```
> Then a dashboard widget references the named filter, not raw JQL."
**How to catch it.** Any inline JQL > 120 chars or > 2 levels of parens = refactor into named saved filters with comments.

---

## Red Flag 3: Dashboards Nobody Opens

**Symptom.** The team has 14 Jira dashboards, all created during onboarding, used by 0 people in the last 30 days.
**Why it's bad.** Dashboards are infrastructure. Unused ones drift, embed stale assumptions, and mislead new joiners who *do* find them. The right number of dashboards is the number people actually use.
**Bad example:**
> "Dashboards in the team's space: Sprint Health, Quarterly Velocity, Bug Bash 2024, Q1 Retrospective Data, Hiring Pipeline, Old Atlas Project, ..."
**Good example:**
> "Quarterly Jira-hygiene review: open dashboard audit log; any dashboard with 0 views in 30 days is archived. Standing dashboards: 3 (Sprint Health, Quarter-View, Incident Tracker). New dashboards require an owner + a use case stated in the description."
**How to catch it.** Run `Dashboard activity report` (Jira admin); any dashboard with 0 views in 30 days = archive.

---

## Red Flag 4: Custom Fields Sprawl

**Symptom.** The Jira instance has 340 custom fields, half referencing departed team configurations.
**Why it's bad.** Custom-field sprawl slows Jira queries, clutters issue-creation forms, and increases the chance of inconsistent data ('Story Points' vs 'Story Pts' vs 'Estimate' all in use). It also exhausts Jira's custom-field index limits.
**Bad example:**
> "Issue creation form has 47 fields, half pre-filled with default values nobody understands, 6 abandoned fields from a 2022 process. Search performance degraded by ~30%."
**Good example:**
> "Custom fields: 28, each with a documented owner and a use case. Quarterly audit removes orphaned fields. Issue creation forms use field configuration schemes to hide non-essential fields per issue type (Bug: 6 fields; Story: 8 fields; Spike: 5 fields)."
**How to catch it.** Custom field count > 80 = audit. Any field with 0 issues touched in 90 days = candidate for removal.

---

## Red Flag 5: Automation Rules That Conflict

**Symptom.** Two automation rules fire on the same transition: one moves the ticket to "Done", the other transitions it back to "In Review". Tickets oscillate.
**Why it's bad.** Conflicting rules produce non-deterministic Jira behavior. Engineers cannot trust the board state. Worse, the bug is hard to diagnose because each rule looks correct in isolation.
**Bad example:**
> "Rule 1: 'On commit message [DONE-XYZ], transition to Done.'
> Rule 2: 'On status change to Done without a QA sign-off, transition back to In Review.'
> (Tickets bounce.)"
**Good example:**
> "Automation rules are catalogued in `jira-automation.md` with each rule's trigger, condition, action, and known interactions. Quarterly review tests all rules together in a staging Jira project before promoting to production."
**How to catch it.** Any ticket that has changed status > 4 times in a day = inspect for rule conflict.

---

## Red Flag 6: Story Points as a Performance Metric

**Symptom.** Manager pulls "story points completed per engineer per sprint" and uses it in performance reviews.
**Why it's bad.** Story points are a *team* relative-sizing tool, not an individual productivity metric. Treating them as performance data trains engineers to inflate estimates, decline complex work, and avoid pair programming. Velocity collapses as a planning signal.
**Bad example:**
> "Performance review: 'Sarah completed 38 SP last sprint; Tom completed 18. Tom needs a PIP.' (Ignoring that Tom's work included on-call + a complex migration.)"
**Good example:**
> "Story points are used only at the team-level (sprint capacity + velocity forecasting). Performance is reviewed via the career-ladder rubric (`pm-career-ladder` skill), not Jira numbers. Engineering managers have explicit org-wide guidance: 'no individual story-point reports'."
**How to catch it.** Any Jira filter / dashboard grouping story points by assignee = remove. See `scrum-master/references/red-flags.md` Red Flag 1.

---

## Red Flag 7: Sprints That Never End

**Symptom.** "Sprint 47" has been "active" for 8 weeks because tickets keep getting carried over.
**Why it's bad.** A sprint is a time-boxed iteration. Letting it run past its end-date corrupts velocity, makes retrospectives meaningless, and erodes the "complete what you commit" discipline. Worse, it hides scope creep -- the sprint just expands.
**Bad example:**
> "Sprint 47: started March 1, originally 2 weeks. Today is May 20. 22 tickets still open. Sprint 48 cannot start because 47 has not closed."
**Good example:**
> "Sprint discipline: sprints close on their scheduled end-date, regardless of completion. Incomplete tickets are explicitly moved (either back to the backlog with a retrospective lesson, or into the next sprint with a documented reason). Closing a sprint is the scrum master's responsibility on the scheduled day."
**How to catch it.** Sprint open longer than 1.5x its planned duration = close it; write a retro lesson.

---

## Red Flag 8: Epic / Story / Subtask Hierarchy Inversion

**Symptom.** Stories with 12 subtasks; subtasks larger than the parent story; epics containing one story.
**Why it's bad.** The hierarchy exists to keep work coherent. Inversions signal under-thought structure -- subtasks-as-stories is a misuse of the type (subtasks are within-sprint slices). Reports break: epic-level burndown shows tiny epics; subtask totals dwarf parent stories.
**Bad example:**
> "Epic 'Bulk Edit' contains 1 story 'Implement Bulk Edit', which contains 22 subtasks ranging from UI to backend to DB migration."
**Good example:**
> "Epic 'Bulk Edit' contains 6 stories (one per vertical slice from `story-splitting`). Each story has 2-5 subtasks for within-sprint coordination only (e.g. 'write tests', 'cut release'). Stories are the unit of value; subtasks are the unit of within-sprint work."
**How to catch it.** Any story with > 6 subtasks, or any subtask > 5 SP = restructure.

---

## Red Flag 9: Inconsistent Issue Types Across Projects

**Symptom.** Project A uses 'Bug, Story, Task, Epic'. Project B uses 'Defect, Feature, Improvement, Initiative'.
**Why it's bad.** Inconsistent types break org-wide reporting and make every cross-project ritual (release notes, security audit, executive reporting) require manual translation. It is also confusing to people who work across projects.
**Bad example:**
> "Org-wide bug report: cannot be generated because 'Bug' and 'Defect' are distinct issue types in different projects."
**Good example:**
> "Issue-type scheme is org-standardized: Story, Task, Bug, Epic, Spike, Subtask. New projects inherit the scheme. Exceptions for regulated teams approved via the Jira-admin charter."
**How to catch it.** Cross-project issue-type count > 8 distinct = consolidate.

---

## Red Flag 10: Permissions Configured Per-Project By Hand

**Symptom.** Each project has a hand-edited permission scheme; the QA team has read access in 11 of 14 projects and nobody knows why the 3 are different.
**Why it's bad.** Per-project hand-editing is unscalable, error-prone, and creates security risk (forgotten access). Reconciling who-has-what-where takes hours per incident.
**Bad example:**
> "47 distinct permission schemes across 30 projects. Half were copies of another scheme with one tweak."
**Good example:**
> "3 org-wide permission schemes: 'Open' (read-all, write-team), 'Restricted' (read-team, write-team), 'Confidential' (read-named-roles). Projects pick one. Role memberships drive access. Documented in `jira-permissions.md`."
**How to catch it.** Permission schemes > 5 = consolidate.

---

## Red Flag 11: JQL in Documentation Without an As-of Date

**Symptom.** "To see open bugs: `project = PROJ AND issuetype = Bug AND status != Done`." Documentation written 2 years ago.
**Why it's bad.** JQL semantics shift as projects evolve (issue types renamed, statuses added). Old JQL silently returns wrong results. The reader trusts the documentation; the documentation is wrong.
**Bad example:**
> "[Old runbook]: 'Open bugs: `project = PROJ AND issuetype = Bug AND status != Done`. (No date, no verification.)'"
**Good example:**
> "[Runbook, 2026-05-21]: 'Open bugs: saved filter `OPEN-BUGS-PROJ` (definition link). Verified against current schema; renewed on the quarterly runbook review.' (Filter ownership: <name>; expires if not renewed.)"
**How to catch it.** Any JQL in a runbook with no date / no saved-filter wrapper = re-validate.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Workflow proliferation | > 5 distinct workflows = consolidate |
| 2 | JQL spaghetti | Inline JQL > 120 chars = saved filter |
| 3 | Dashboards nobody opens | 0 views in 30 days = archive |
| 4 | Custom field sprawl | > 80 custom fields = audit |
| 5 | Automation rules conflict | Tickets oscillating between states |
| 6 | SP as performance metric | No SP-by-assignee filters |
| 7 | Sprints that never end | Open > 1.5x planned duration = close |
| 8 | Hierarchy inversion | Story with > 6 subtasks = restructure |
| 9 | Inconsistent issue types | > 8 cross-project types = consolidate |
| 10 | Per-project permissions | Permission schemes > 5 = consolidate |
| 11 | JQL in docs without date | All runbook JQL via saved filters |

## Related Reading

- `SKILL.md` -- Jira administration patterns
- `references/jql-patterns.md` -- canonical JQL recipes
- `references/automation-recipes.md` -- standard automation rules
- Sibling skill: `linear-expert/` -- Linear's equivalent patterns
- Sibling skill: `atlassian-admin/` -- broader Atlassian-suite admin
- Sibling skill: `scrum-master/` -- the data Jira-expert serves
- Sibling skill: `confluence-expert/` -- the documentation paired with Jira
