# Example: Acme Analytics — Building the Product Team Confluence Space

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Acme Analytics (Series-B B2B data platform, ~220 employees) has Confluence but uses it badly. Each of the 6 product teams (Ingestion, Modeling, Activation, Reporting, Identity, Billing) has its own ad-hoc space; cross-team artifacts (vision, OKRs, roadmaps) live in three different places; new PMs spend their first week asking "where is X?" The VP Product has asked the new Product Operations lead to design a unified Product space — clean information architecture, sane permissions, and templates so the next 12 months of artifacts land in the right place.

The confluence-expert skill is being applied to design the space architecture, permission scheme, and template set before any content migration begins. No "let's just clean up later" — the space is being designed correctly the first time.

## Inputs

- Existing: 11 fragmented Confluence spaces with overlapping content
- Required users: 11 PMs, 6 EMs, 4 designers, 1 VP, 1 Product Ops lead, ~80 view-only stakeholders
- Constraint: no content loss; everything migrates or links from old spaces
- Constraint: 4-week timeline, must be live for the Q3 planning offsite
- Permission requirement: some pages (e.g. compensation philosophy, hiring) are PM-org private; some (e.g. roadmap, vision) are company-wide; some (e.g. customer interview transcripts) are restricted
- Atlassian Cloud Premium tenant; Okta SSO + SCIM in place

## Applying the skill

1. **Designed information architecture before creating the space.** Drafted the page tree on paper first. Max 3 levels deep per the skill's best practice. Every leaf node has a templated structure.
2. **Defined permissions by zone, not page.** Three permission archetypes (Public, Product-team, Restricted) mapped to three branches of the tree. No one-off page permissions.
3. **Picked a homepage that reduces "where is X" questions.** Homepage is a navigation page, not a welcome message.
4. **Macro choices intentional.** Used Page Tree, Jira Issue, Roadmap Planner, Decision Log, and Children Display. Did NOT enable every available macro.
5. **Templates tied to the atlassian-templates rollout.** The Confluence templates here are the same v1.0 set being rolled out in parallel.
6. **Migration plan with explicit "leave, link, or move" decisions per page.**

## The artifact

```
================================================================
  ACME ANALYTICS — PRODUCT TEAM CONFLUENCE SPACE
  Space key:   PROD
  Space type:  Team
  Owner:       Product Operations Lead
  Effective:   2026-05-22
================================================================

PART 1 — SPACE OVERVIEW

Name:               Product
Key:                PROD
URL:                /wiki/spaces/PROD
Description:        Central home for the Acme Analytics product
                    organization. Strategy, roadmaps, PRDs,
                    discovery, OKRs, and ops.
Theme:              Standard with Acme brand colors
Homepage:           "Product at Acme — Start Here"

PART 2 — INFORMATION ARCHITECTURE (3 LEVELS MAX)

PROD/  Home page — navigation only
├── 01. Start Here
│   ├── New PM onboarding (links to pm-onboarding skill)
│   ├── How we work — operating principles
│   ├── Glossary of product terms
│   └── "I'm looking for..." search hints
│
├── 02. Strategy
│   ├── Product vision (one page, owned by VP)
│   ├── North-star metric tree
│   ├── Annual themes
│   └── Strategic decisions log (DACI)
│
├── 03. Roadmap
│   ├── Current quarter roadmap (live, all teams)
│   ├── Next quarter draft
│   ├── Backlog of bets (>2 quarters out)
│   └── Roadmap archive (past quarters)
│
├── 04. OKRs
│   ├── Company OKRs (Q3 2026)
│   ├── Product OKRs (Q3 2026)
│   ├── Team OKRs (links to each team page)
│   └── OKR archive
│
├── 05. PRDs
│   ├── Active PRDs (filtered by status)
│   ├── Approved & shipping
│   ├── Shipped & retrospected
│   ├── Killed & learned-from
│   └── PRD template v1.0 (canonical link)
│
├── 06. Discovery
│   ├── Customer interview library (restricted)
│   ├── Opportunity solution trees
│   ├── Experiments register
│   └── Discovery cadence + ground rules
│
├── 07. Launches
│   ├── Upcoming launches calendar (next 90 days)
│   ├── Launch playbook (canonical link)
│   ├── Recent launches (linked to post-mortems)
│   └── PR/FAQ archive
│
├── 08. Teams
│   ├── Ingestion (links to team Confluence sub-tree)
│   ├── Modeling
│   ├── Activation
│   ├── Reporting
│   ├── Identity
│   └── Billing
│
├── 09. Operations
│   ├── Weekly status updates (auto-aggregated)
│   ├── Monthly business reviews
│   ├── Quarterly planning records
│   ├── Decision log (DACI archive)
│   └── Working agreements
│
└── 10. People (RESTRICTED — PM org only)
    ├── PM career ladder
    ├── Hiring loop + interview rubrics
    ├── 1:1 templates
    └── Calibration history

NOTES ON THE TREE
  - 10 top-level branches, each numbered for stable URLs.
  - Every leaf page exists from day 1, even if empty.
  - "Start Here" is branch 01 deliberately so it sorts first.
  - The Teams branch (08) is the only one that goes 4 levels
    deep (PROD > Teams > Activation > Activation Discovery >
    interview transcript). The 3-level rule applies to navi-
    gation pages, not detail pages.


PART 3 — PERMISSION ARCHITECTURE

Three archetypes mapped to branches:

  Archetype       Who can view       Who can edit
  -----------     ----------------   ----------------
  PUBLIC          All Acme staff     Product team
  PRODUCT-TEAM    PM org + EMs       Product team
  RESTRICTED      Named list only    Named list only

Branch-to-archetype mapping:

  01 Start Here       PUBLIC
  02 Strategy         PUBLIC
  03 Roadmap          PUBLIC
  04 OKRs             PUBLIC
  05 PRDs             PRODUCT-TEAM (some PRDs are pre-launch
                      sensitive; default to internal until
                      the PM elevates to public)
  06 Discovery        RESTRICTED (customer interview library)
                      PRODUCT-TEAM (everything else)
  07 Launches         PUBLIC
  08 Teams            PRODUCT-TEAM by default; teams may
                      elevate to PUBLIC per page
  09 Operations       PRODUCT-TEAM
  10 People           RESTRICTED — VP Product + Product Ops
                      + active PM managers only

Permission groups (created via atlassian-admin):
  confluence-prod-admin       Space admins (3 people)
  confluence-prod-edit        Product team editors (~22 people)
  confluence-prod-view        PM org viewers (~28 people)
  confluence-prod-restricted  Restricted access (10-15 people,
                              varies by sub-folder)

Anti-pattern explicitly avoided:
  No per-page permission overrides except inside branch 06
  (Customer Interview Library) and branch 10 (People).
  Everything else inherits from branch-level permissions.
  This is what makes the space maintainable.


PART 4 — HOMEPAGE DESIGN

The homepage answers ONE question: "where is X?"

Layout (left to right, top to bottom):

  +--------------------------------------------------+
  | Banner: Product at Acme - Start Here             |
  +--------------------------------------------------+
  | I'm looking for...                               |
  |   - The current quarter's roadmap     -> link    |
  |   - The product vision                -> link    |
  |   - A specific PRD                    -> search  |
  |   - My team's OKRs                    -> link    |
  |   - Upcoming launches                 -> link    |
  |   - Customer interview I remember     -> search  |
  |   - Decision history                  -> link    |
  +--------------------------------------------------+
  | This week                                        |
  |   {Macro: Latest weekly status update}           |
  |   {Macro: Children of "Launches > Upcoming"}     |
  +--------------------------------------------------+
  | I'm new here                                     |
  |   -> New PM onboarding                           |
  |   -> Glossary                                    |
  |   -> Who's who in product                        |
  +--------------------------------------------------+
  | Page tree (auto-generated, depth 2)              |
  +--------------------------------------------------+

What the homepage does NOT contain:
  - A welcome paragraph from leadership (lives in branch 02)
  - News announcements (lives in branch 09)
  - Random links the VP wants pinned today
    (those move to "Start Here" or are not pinned at all)


PART 5 — TEMPLATE LIBRARY

Templates installed in PROD space (synced from
atlassian-templates rollout v1.0):

  PRD v1.0
  Epic discovery brief
  Customer interview note
  Customer interview synthesis
  Experiment design + readout
  Pre-mortem
  Launch checklist
  Post-mortem (incident)
  Post-launch retro (non-incident)
  Decision log entry (DACI)
  Weekly status update
  Monthly business review
  Quarterly OKR draft
  Quarterly OKR review

Each template:
  - Has a version number in its title
  - Has a 1-paragraph "when to use this" header
  - Links to the canonical reference in the PROD/05 PRDs
    sub-tree or in the relevant skill folder


PART 6 — MACRO PALETTE

The space enables a deliberately small set of macros. Anything
else requires Confluence admin approval.

  Page Tree              navigation pages
  Children Display       branch landing pages
  Jira Issue             single issue embed
  Jira Filter            issue list embed
  Roadmap Planner        roadmap pages
  Status                 PRD status flags
  Info / Note / Warning  PRD callouts
  Table of Contents      long pages (>3 sections)
  Excerpt / Excerpt Include  re-using definitions across pages
  Decision               decision log entries

Macros NOT enabled by default (require approval):
  Multi-Source Iframes, Drawio, third-party diagram embeds,
  poll macros, gallery macros. These bloat pages and slow
  page load.


PART 7 — MIGRATION PLAN (4 WEEKS)

Existing content sources (11 fragmented spaces):
  PROD-OLD, ACT, ING, MOD, REP, ID, BILL, PRODOPS, ROAD,
  DISCOVERY, LEADERSHIP-PRODUCT

Per-page disposition (one of three actions):

  MOVE     Page moves into new PROD space with a redirect
           from old URL. Used for active strategy, current
           roadmap, current OKRs, in-flight PRDs.

  LINK     Page stays in original space; new PROD page links
           to it. Used for team-specific operational docs that
           live in team spaces.

  ARCHIVE  Page is superseded; archived to a read-only
           "Legacy" branch in the old space. Used for
           obsolete content.

Migration backlog (estimated):
  ~340 pages total across old spaces
  ~110 MOVE
  ~ 80 LINK
  ~150 ARCHIVE

Week 1   Build PROD skeleton, install templates, set permissions
Week 2   Migrate strategy, roadmap, OKRs (MOVE: ~40 pages)
Week 3   Migrate active PRDs and discovery (MOVE: ~50 pages)
         Set up LINKs to team spaces (~80 pages)
Week 4   Archive obsolete content; announce; old spaces become
         read-only

Zero data loss requirement: every old URL must either resolve
to a new page or to an archived snapshot. The Confluence admin
sets up redirects for the MOVE category.


PART 8 — GOVERNANCE

Space admins: 3 people (Product Ops Lead + 2 named PMs)
Review cadence:
  Quarterly  Page tree audit, broken-link sweep, orphan-page
             check
  Monthly    Homepage refresh; "this week" macros validated
  Weekly     Status update lands automatically (no manual step)

Naming convention:
  - Branch pages start with their number: "03 Roadmap"
  - PRD pages: "[Team] [Feature] PRD v[N]" e.g. "Activation
    trial flow PRD v2"
  - Meeting notes: "YYYY-MM-DD - Topic"
  - Decisions: "DEC-NNN - Title"

Orphan-page policy: any page outside the tree for >30 days
is flagged for re-parenting or archival.


PART 9 — SUCCESS METRICS (90-DAY)

  Metric                              Baseline   Target
  ---------------------------------   --------   --------
  Avg time-to-find for new PMs        15 min     <3 min
                                      (survey)
  % of PRDs created via template      ~35%       >90%
  Pages outside the page tree         estimated  <10
                                      ~60
  Search-no-result rate               (unknown)  <15%
  Stakeholder NPS for product docs    -4         >+10
```

## Why this works

- **Page tree first, content second.** The architecture is what makes the space last. Most "let's clean up Confluence" efforts start by moving pages around and end in another mess. Designing the IA first, with explicit slots for everything, is the leverage.
- **Permission by zone, not by page.** Per-page permissions are how a Confluence space rots over 12 months. Three archetypes mapped to three branches scales.
- **Homepage answers "where is X?"** Most Confluence homepages are leadership-welcome essays no one reads. This one is a navigation page with the literal question "I'm looking for..." up top.
- **Numbered branches.** "01 Start Here", "02 Strategy" — the leading numbers stabilize sort order and give pages stable URLs. PMs onboarding learn the tree quickly.
- **Macro palette is intentional and small.** Enabling every available macro is a Confluence anti-pattern (slow page load, format chaos). The 11-macro palette covers 95% of product use cases.
- **Migration with explicit MOVE / LINK / ARCHIVE.** Every old page gets a disposition. Nothing falls through the cracks. Old URLs redirect; nothing is lost.
- **Success metrics defined.** "Time-to-find for new PMs" is the right metric — it measures the user outcome, not the artifact count.

## What's next

- The template set referenced here is rolled out by [`../atlassian-templates/`](../atlassian-templates/) — the two skills run in parallel.
- Permission groups and SSO/SCIM provisioning come from [`../atlassian-admin/`](../atlassian-admin/).
- For Jira-Confluence linking (e.g. epic auto-population on PRDs), see [`../jira-expert/`](../jira-expert/).
- New PM onboarding inside the "Start Here" branch is anchored to [`../career/pm-onboarding/`](../career/pm-onboarding/).
- The decision log macro entries follow the format in [`../execution/daci-framework/`](../execution/daci-framework/).
- Weekly status updates auto-populating the homepage come from [`../execution/status-update-generator/`](../execution/status-update-generator/).
