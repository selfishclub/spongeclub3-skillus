# Red Flags: Confluence Expert

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them. Pair with the SKILL.md and Troubleshooting table.

## How to use this document

When you have just produced a Confluence space design, IA proposal, page template, or governance policy, scan the red flags below. Each red flag shows a *bad* and *good* version of the same artifact.

---

## Red Flag 1: Information-Architecture Chaos (Flat Spaces with 800+ Pages)

**Symptom.** A single space has 800 top-level pages and no hierarchy. Search returns 40 results for any common term. Nobody knows where to put new content.

**Why it's bad.** Confluence is a hierarchical wiki by design. A flat space defeats the navigation tree, breaks page-tree macros, and turns every search into a needle-in-haystack exercise. Users start writing in personal spaces because the main space is unusable.

**Bad example:**
> Engineering space: 1,200 pages, 947 at root level. Mixed: meeting notes, RFCs, runbooks, onboarding, OKRs, retros.

**Good example:**
> Engineering space, 5-section IA: (1) /Strategy (OKRs, roadmap), (2) /Practices (runbooks, on-call), (3) /Projects (one branch per project), (4) /People (onboarding, growth), (5) /Archive. Each section has an owner, a page-tree macro on the landing page, and a retention policy."

**How to catch it.** Open the space tree. If the root has more than ~15 pages, you have IA chaos.

---

## Red Flag 2: Orphan Pages (No Inbound Links, No Parent)

**Symptom.** 30% of pages in a space have zero inbound links and are not children of any indexed page. They exist but are not findable except by URL.

**Why it's bad.** Orphan pages cannot be discovered, so their content is invisible. Worse, they often contain critical info (a forgotten policy, a half-finished design doc) that someone reinvented later because they could not find the original.

**Bad example:**
> Space audit: 2,400 pages total. 720 (30%) orphan — no inbound links, no parent. Half are "draft" pages from 2-3 years ago.

**Good example:**
> Quarterly orphan-page audit run via REST API. Orphans either (a) re-parented and linked, (b) archived to /Archive with date label, or (c) deleted with stakeholder confirmation. Current orphan rate <5%."

**How to catch it.** Use the Confluence REST API or a community macro to list orphans. Anything above 10% is unhealthy.

---

## Red Flag 3: Documentation Treated as Storage, Not Communication

**Symptom.** Pages exist but are wall-of-text dumps with no structure, no summary, no audience identification. Readers cannot find the answer in 30 seconds.

**Why it's bad.** Confluence content competes with Slack threads and human memory. A page that takes 10 minutes to skim loses to a 1-minute Slack search. Pages must be skimmable: TL;DR, headings, structured tables.

**Bad example:**
> Page "Deployment Process": 2,400 words, single block of text, no headings, no TL;DR. Last updated 2023.

**Good example:**
> Page "Deployment Process": 1-paragraph TL;DR, audience banner ("for: on-call engineers"), table of common scenarios, expandable sections for edge cases. Last reviewed banner: 2026-04. Owner named."

**How to catch it.** Open any page. Can a reader find the key info in 30 seconds? If not, the page is storage, not communication.

---

## Red Flag 4: No Page Ownership or Review Cadence

**Symptom.** Pages have no owner field, no "last reviewed" date, no review cadence. Stale info accumulates indefinitely.

**Why it's bad.** Documentation rots. Without a named owner and review cadence, pages drift from reality and become liabilities — readers act on stale info and cause incidents. The runbook that says "page Jane on-call" when Jane left two years ago is a real outage waiting to happen.

**Bad example:**
> Runbook page last edited 2022. No owner. References old infrastructure (no longer in production).

**Good example:**
> Every page in /Practices has page properties: `owner`, `last-reviewed`, `review-cadence` (quarterly/annual). Page-properties report on space landing page surfaces stale pages. Pages overdue for review get a banner."

**How to catch it.** Does every page in your operational spaces have owner + review date? If not, content rot is invisible.

---

## Red Flag 5: Permissions Tangled at the Page Level

**Symptom.** Space has space-level permissions, but 100+ pages have individual page-level restrictions on top. New users cannot see what they should; some users see things they shouldn't.

**Why it's bad.** Page-level permissions are a maintenance nightmare. They are not visible in space-permission audits, so access drift is silent. New employees inherit a permission patchwork that no one can fully explain.

**Bad example:**
> "We restrict sensitive pages individually. Currently 187 page-level restrictions across the space."

**Good example:**
> "Sensitive content lives in a separate Restricted space with appropriate space-level permissions. Main space uses inheritance only. Page-level restrictions reserved for genuinely exceptional cases (<5 across the org), all logged."

**How to catch it.** Count page-level permission overrides. Above 20 in a space is excessive complexity.

---

## Red Flag 6: Jira-Confluence Drift (Macros Pointing to Dead Projects)

**Symptom.** Pages embed Jira-issues macros, status reports, and Jira filters. Many filter results render empty because projects were renamed or archived.

**Why it's bad.** Broken macros render as blank panels. Readers cannot tell if there is no work or if the macro is broken. Status pages stop being trustworthy.

**Bad example:**
> Quarterly status page: 6 embedded Jira filter macros. 3 return zero results because referenced projects archived. Page still says "Q1 Status: On Track."

**Good example:**
> Status page macros parameterized via page properties (jira-project-key). Annual macro-health audit via REST API. Empty results trigger a warning banner ('configure page property: jira-project-key')."

**How to catch it.** Open status/dashboard pages. Are macros displaying real content or silently empty? Silent empties are bugs.

---

## Red Flag 7: Confluence as a Single Source of Truth without Defining "Truth"

**Symptom.** "Confluence is our source of truth" — but the same topic has 4 pages with conflicting info and no canonical pointer.

**Why it's bad.** Single source of truth (SSoT) is a discipline, not a slogan. If a topic has multiple pages, you do not have SSoT — you have redundancy and ambiguity. Readers find different pages and get different answers.

**Bad example:**
> Search "deployment process" returns 5 pages, all from different teams, all slightly contradicting. Each team thinks theirs is "the" page.

**Good example:**
> One canonical page per topic, with `canonical: true` page property. Other pages on the topic include a "Canonical reference: [link]" callout at the top, and exist only to extend, not duplicate. Cross-team review for new canonical pages."

**How to catch it.** For your top 10 most-searched topics, is there exactly one canonical page? If multiple, SSoT is fiction.

---

## Red Flag 8: Meeting Notes as Permanent Pages

**Symptom.** /Meeting Notes branch has 2,000+ pages. Search returns meeting notes for any product term, drowning out canonical content.

**Why it's bad.** Meeting notes are ephemeral. They should live in a dedicated subspace with retention policies, not pollute the main searchable corpus. The result of search becoming meeting-notes-noise is that nobody trusts search.

**Bad example:**
> /Engineering/Meeting Notes: 2,400 pages going back 4 years. Searching "rate limiter" returns 18 meeting notes mentioning it in passing.

**Good example:**
> /Engineering/Meeting Notes: separate space (excluded from default site search). Retention policy: archive after 90 days. Decisions extracted into canonical decision-log pages on the main space. Meeting notes link out to those decisions."

**How to catch it.** Search a common term. If meeting notes outnumber canonical content in results, your search is polluted.

---

## Red Flag 9: Templates Exist but Are Not Discoverable

**Symptom.** Space has 12 well-designed templates. New page creators click "Blank Page" because they do not know templates exist.

**Why it's bad.** Templates only help if they are used. A library nobody finds produces no quality lift. The template space needs landing pages, prompts at page-create time, and onboarding inclusion.

**Bad example:**
> Templates space exists. Adoption: 8% of new pages use a template.

**Good example:**
> Templates surfaced in the "Create Page" dialog by default. Template catalog page indexed by use case. Featured in onboarding. Adoption: 71% of new pages use a template. Quarterly review of template fit."

**How to catch it.** What percent of new pages in the last 30 days came from a template? Below 50% means templates are invisible.

---

## Red Flag 10: Mixing Personal Notes into Team Spaces

**Symptom.** Individuals create personal scratch pages in team spaces. Half-finished thoughts, draft questions, personal lists — all visible to the team and indexed in search.

**Why it's bad.** Personal notes in team spaces pollute the corpus. They lower the signal-to-noise of search and confuse readers ("is this a real plan or someone's brainstorm?"). Confluence has personal spaces for this; the team space should be clean.

**Bad example:**
> Engineering space contains pages like "Sarah's notes from her Monday review" and "Random ideas for retros."

**Good example:**
> Personal scratchwork lives in each user's personal Confluence space. Team space contains only canonical, owned content. Onboarding includes 'use your personal space for notes' guidance."

**How to catch it.** Sample 50 recent pages in a team space. Any that are explicitly personal-titled? If yes, the discipline is missing.

---

## Red Flag 11: No Archival Lifecycle

**Symptom.** Pages from 2018 still live in the active hierarchy alongside current pages. Nothing is archived; everything stays "live forever."

**Why it's bad.** Without archival, the space accumulates indefinitely. Search performance degrades; orphan rates climb; readers see stale content alongside current content. Confluence's `archive` feature exists for this reason but goes unused.

**Bad example:**
> Roadmap space: contains roadmap pages from 2018-2026, all in /Roadmaps, all in search results. Newest mixed with oldest.

**Good example:**
> Annual archival pass each January: anything older than 18 months and superseded gets `archive` flag. Archived pages remain searchable when filter applied but not in default search. Retention policy documented per space."

**How to catch it.** How many pages older than 24 months are in active hierarchy? If many, the lifecycle is broken.

---

## Red Flag 12: Page Titles That Do Not Describe Content

**Symptom.** Page titles like "Draft", "Working Doc", "Notes", "Untitled (1)". Search returns useless title matches.

**Why it's bad.** Search relevance depends on titles. Vague titles destroy findability. Confluence does not auto-rename when content evolves, so the placeholder title persists.

**Bad example:**
> Pages titled: "Draft", "Working", "Notes", "Brainstorm v3", "Untitled".

**Good example:**
> Style guide: page titles are noun phrases describing content. "Q3 Activation Strategy" not "Working". Onboarding includes title-style review. Bad titles flagged in monthly content audit."

**How to catch it.** Search "draft", "working", "notes", "untitled" in your space. Each hit is a title to rename.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | IA Chaos | Space root has ~15 or fewer pages? |
| 2 | Orphan Pages | Orphan rate under 10%? |
| 3 | Storage Not Communication | Key info findable in 30 seconds? |
| 4 | No Owner / Review Cadence | Operational pages have owner + review date? |
| 5 | Tangled Page Permissions | Page-level overrides under 20 per space? |
| 6 | Broken Jira Macros | Macros show content or clear "configure me" prompt? |
| 7 | Multiple "Sources of Truth" | One canonical page per top-10 topic? |
| 8 | Meeting Notes Polluting Search | Meeting notes in separate subspace, retention 90d? |
| 9 | Templates Not Discoverable | Template-based page creation above 50%? |
| 10 | Personal Notes in Team Space | Recent pages all canonical, none personal? |
| 11 | No Archival Lifecycle | Annual archive pass; old content not in active hierarchy? |
| 12 | Vague Page Titles | Search "draft/working/untitled" returns zero hits? |

## Related Reading

- SKILL.md Troubleshooting section (for symptom -> root cause -> resolution)
- references/space-architecture.md (for IA patterns, if present)
- atlassian-admin/references/red-flags.md (for org-wide governance)
- atlassian-templates/references/red-flags.md (for template library health)
