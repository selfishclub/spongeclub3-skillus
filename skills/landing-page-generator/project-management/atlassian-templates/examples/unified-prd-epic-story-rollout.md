# Example: Acme Analytics — Rolling Out a Unified PRD/Epic/Story Template Set Across 6 Teams

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Acme Analytics is a Series-B data platform (220 employees). Six product teams (Ingestion, Modeling, Activation, Reporting, Identity, Billing) each evolved their own PRD format, Jira epic structure, and story conventions over the last two years. The result: cross-team dependency reviews require translation, PM onboarding takes weeks, and roadmap rollups break because epics from different teams do not have comparable fields.

The new VP Product wants one PRD template, one epic template, and one story template adopted by all six teams within 60 days — without forcing anyone to migrate historical artifacts. The atlassian-templates skill is being applied to design, govern, and roll out the unified template set.

## Inputs

- 6 product teams, 11 PMs, 6 EMs, 4 designers
- Confluence: 6 different PRD page templates in active use, 3 inherited from contractors
- Jira: 6 different epic descriptions, 4 different story field configurations
- Constraint: no forced backfill of existing PRDs/epics; new artifacts only
- Constraint: each team has 30 minutes max in their team meeting for rollout training
- VP Product: "I want to be able to read any team's PRD without a Rosetta Stone."

## Applying the skill

1. **Discover before designing.** Interviewed all 11 PMs about what they actually use from their current templates. 70% of "essential" sections were the same across teams; only 30% were team-specific.
2. **Designed the common core + team extensions.** Built one master template with eight required sections, plus an extensions block where each team can add up to two team-specific sections. This avoids the "lowest common denominator" trap.
3. **Versioned everything.** Each template has a version number in its title (e.g. "Acme PRD v1.0"). Old templates are marked deprecated, not deleted.
4. **Linked epic <-> PRD <-> story.** The Jira epic template includes a "PRD link" field that is required. The story template includes a "Parent epic" field that is required. The Confluence PRD template includes a Jira-query macro that auto-lists child epics and their status.
5. **Rollout in waves.** Two teams in week 1 (PMs who volunteered), two in week 3, two in week 5. Adoption telemetry tracked weekly.
6. **Governance defined up front.** Quarterly template review committee. Anyone can propose a change. Changes ship as v1.1, v1.2 — old versions remain usable for 90 days.

## The artifact

```
================================================================
  ACME ANALYTICS — UNIFIED TEMPLATE SET v1.0
  Owner: VP Product
  Effective: 2026-05-22
  Next review: 2026-08-22
================================================================

PART 1 — CONFLUENCE PRD TEMPLATE v1.0
=====================================

[Template metadata]
Template name:   Acme PRD v1.0
Confluence space: Product (PROD)
Restricted to:   Anyone in confluence-prod-member group can create

[Page header (auto-populated)]
PRD Title:        {page-title}
Author:           @{current.user}
Status:           Draft | In Review | Approved | Shipped | Killed
Last updated:     {date:format=dd MMM yyyy}
Team:             [Ingestion | Modeling | Activation | Reporting
                   | Identity | Billing]
Epic link:        {jira:issue-key}   (required at "In Review")
Reviewers:        @reviewer1 @reviewer2

[Section 1 — Problem]
What problem are we solving? For whom? Why now?
(Required. 3-5 sentences. No solution language.)

[Section 2 — Target customer]
Who feels the pain most? Be specific — persona + segment + use case.
(Required.)

[Section 3 — Evidence]
What customer signal supports this problem?
  - Interview quotes (link Dovetail clips)
  - Support ticket volume / themes
  - Funnel or NSM data
  - Sales / CS escalations
(Required. At least 2 evidence types.)

[Section 4 — Goal & success metric]
What outcome will this PRD move?
  - North-star input metric: ___
  - Target: from ___ to ___ by ___
  - Counter-metric (what we watch to make sure we don't break it): ___
(Required.)

[Section 5 — Proposal]
What we are building (at the right altitude — not the spec).
Include:
  - High-level approach
  - Mermaid diagram or wireframe if helpful
  - Key user-visible behaviors
(Required.)

[Section 6 — Scope]
In scope (v1):
In scope (fast-follow):
Out of scope (explicit):
(Required.)

[Section 7 — Risks & open questions]
Top 5 risks (with mitigations).
Top 5 open questions (with owners and due dates).
(Required. Empty is not acceptable.)

[Section 8 — Rollout & launch]
- Feature flag plan
- Beta cohort and exit criteria
- GA criteria
- Comms plan link
(Required.)

[Team extensions block — up to 2 sections]
Each team may add up to two team-specific sections.
Recorded extensions:

  Ingestion       "Source compatibility matrix"
  Modeling        "Query plan diff"
  Activation      "Channel reach estimate"
  Reporting       "Embedding compatibility"
  Identity        "Auth path diagram"
  Billing         "Pricing impact analysis"

[Auto-generated footer]
{jira-query: parent-epic = {page.epic-link}}
  -> Lists all child stories with status, assignee, sprint

================================================================
PART 2 — JIRA EPIC TEMPLATE v1.0
================================

Issue type:       Epic
Required fields:
  Summary           free text
  PRD link          URL to Confluence PRD (validated)
  Team              dropdown (6 teams)
  Outcome metric    free text (1 line, must mention NSM input)
  Target quarter    Q1 | Q2 | Q3 | Q4 | Backlog
  Status            Discovery | Design | Build | Beta | GA | Done
  Risk level        Tiger | Paper Tiger | Elephant
                    (from pre-mortem classification)
Optional fields:
  Beta cohort
  Feature flag key

Default description (auto-populated):
  ## Outcome
  [What outcome moves when this ships]

  ## PRD
  [PRD link — auto-filled from PRD link field]

  ## Stories
  [Auto-populated by Jira from child stories]

  ## Status update (latest)
  [Most recent weekly status from status-update-generator]

================================================================
PART 3 — JIRA STORY TEMPLATE v1.0
================================

Issue type:       Story
Required fields:
  Summary           free text, MUST start with "As a..."
  Parent epic       Jira epic key (validated)
  Acceptance criteria   list, at least 2 items
  Story points      Fibonacci (1, 2, 3, 5, 8, 13)
  Team              auto-inherited from epic
  Component         dropdown per team
Optional fields:
  Feature flag key (auto-inherited from epic if set)

Default description (auto-populated):
  ## User story
  As a [persona],
  I want [capability],
  so that [outcome].

  ## Acceptance criteria
  - Given [context]
    When [action]
    Then [outcome]
  - Given ...

  ## Notes
  [Free text]

================================================================
PART 4 — ROLLOUT PLAN
================================

WAVE 1 — Weeks 1-2 (Volunteers)
  Teams:     Activation, Reporting
  Training:  30 min team meeting, PM + EM together
  Support:   Daily standup drop-in for first week
  Telemetry: Count new PRDs using v1.0, count new epics with
             PRD link filled, count new stories with parent epic

WAVE 2 — Weeks 3-4
  Teams:     Modeling, Identity
  Training:  Same format. Wave 1 PMs co-present.
  Telemetry: Same. Plus retrospective input from Wave 1 PMs.

WAVE 3 — Weeks 5-6
  Teams:     Ingestion, Billing
  Training:  Same format. Wave 1 + Wave 2 PMs co-present.
  Telemetry: Same. Adoption target: 80% of new artifacts on v1.0
             by end of week 8.

OLD TEMPLATES
  Marked DEPRECATED on day 1.
  Remain creatable for 90 days (gives in-flight PRDs time to land).
  After 90 days, old templates are hidden (not deleted).
  After 180 days, old templates are archived to a "Legacy
  Templates" Confluence page.

NO FORCED BACKFILL
  Existing PRDs and epics keep their original format.
  Cross-team rollup queries are written against the v1.0 fields.
  Old artifacts that are still active are migrated only if/when
  the PM voluntarily touches them.

================================================================
PART 5 — GOVERNANCE
================================

REVIEW COMMITTEE
  VP Product (chair)
  1 PM per team (rotates quarterly)
  1 EM representative
  1 Designer representative

CHANGE PROCESS
  Anyone may open a "Template change request" Jira ticket
  in the TPL (Templates) project.
  Committee reviews monthly.
  Approved changes ship as v1.1, v1.2, etc.
  v2.0 requires a re-rollout plan (only if breaking change).

VERSION POLICY
  Patch (v1.0 -> v1.0.1): typo, wording.
  Minor (v1.0 -> v1.1):   added optional field, new section.
  Major (v1.x -> v2.0):   removed/renamed required field, new
                          required section.

ADOPTION METRICS (reported monthly)
  - % new PRDs created on v1.0
  - % new epics with PRD link filled
  - % new stories with parent epic linked
  - Cross-team rollup query success rate
  - PM onboarding time (target: cut from 3 weeks to 1 week)

================================================================
PART 6 — TRAINING DECK SKELETON (30 MIN)
================================

  0-5 min   Why one template set: cross-team readability,
            faster onboarding, working rollups.
  5-15 min  Walk through the PRD v1.0 sections, focusing on
            what is required vs optional.
  15-22 min Jira epic + story templates demo.
  22-27 min Team extension block — pick your two extensions.
  27-30 min Q&A and where to file change requests.
```

## Why this works

- **Common core + team extensions.** This avoids the failure mode of every template rollout: either everything is forced to a single rigid format (teams revolt) or every team keeps its own (no consistency gained). 8 required sections + 2 optional team-specific sections is the right balance.
- **Versioning is visible.** Templates are named with version numbers. Anyone reading a PRD can tell which version it is. Less-experienced template owners ship v2 by overwriting v1 — that breaks every link and PRD that referenced "the PRD template."
- **PRD <-> epic <-> story linking is enforced.** The "PRD link" is required at "In Review" status. The "Parent epic" is required on stories. This is what makes rollups actually work — the structural connection is in the data model, not in PM discipline.
- **Wave rollout with peer trainers.** Wave 2 is trained by Wave 1 PMs. Wave 3 by Wave 1 + 2. This builds internal advocacy and surfaces real questions, not vendor questions.
- **No forced backfill.** The instinct to migrate everything is wrong. Migrate-on-touch is sufficient and avoids a multi-month freeze.
- **Governance up front.** Naming a review committee and a change process on day one prevents the template from rotting in month 6.

## What's next

- Hand off Jira global template deployment to [`../atlassian-admin/`](../atlassian-admin/) — they own the deployment to the Atlassian tenant.
- The PRD template content itself maps to [`../execution/create-prd/`](../execution/create-prd/) — that skill is the canonical reference for what each section should contain.
- For the team extension blocks that use specialized formats (e.g. AI feature PRDs), point teams at [`../execution/ai-feature-prd/`](../execution/ai-feature-prd/) and [`../execution/pricing-prd/`](../execution/pricing-prd/).
- Monthly adoption metrics piggyback on [`../execution/status-update-generator/`](../execution/status-update-generator/).
- After 90 days, schedule a retrospective using [`../sprint-retrospective/`](../sprint-retrospective/) to decide what goes into v1.1.
