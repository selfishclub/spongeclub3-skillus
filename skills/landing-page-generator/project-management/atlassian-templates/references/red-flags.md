# Red Flags: Atlassian Templates

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them. Pair with the SKILL.md and Troubleshooting table.

## How to use this document

When you have just designed a Confluence page template, Jira issue template, or blueprint for org-wide use, scan the red flags below before publishing it. Each red flag shows a *bad* and *good* version of the same artifact.

---

## Red Flag 1: Template Sprawl (a Template per Use Case)

**Symptom.** The org has 60+ Confluence templates, including "PRD v1", "PRD v2", "PRD - mobile", "PRD - copy of PRD v2 for that one project", and so on.

**Why it's bad.** Template sprawl is the documentation equivalent of permission scheme bloat. Authors cannot find the right template; the wrong template gets used; outdated templates remain in circulation forever. The fix is a small set of canonical templates with parameterized sections, not a template per variation.

**Bad example:**
> "Templates in space: 64 templates including 7 PRD variants, 5 RFC variants, 4 release-notes formats, and 12 retrospective templates."

**Good example:**
> "8 canonical templates, each with parameterized sections. PRD template includes optional sections (mobile, enterprise, AI). Template owners listed. Quarterly review removes unused templates."

**How to catch it.** Count templates per space. More than 15 per top-level space is sprawl.

---

## Red Flag 2: Fields Nobody Fills In

**Symptom.** The template has 40 fields. In practice, 25 of them are left blank or filled in with "TBD" or "N/A".

**Why it's bad.** Required fields nobody fills in train users to ignore the template. Optional fields nobody fills in are dead weight that clutters the page. The signal-to-noise ratio drops; future authors copy the bad pattern.

**Bad example:**
> "Bug report template: 18 fields including 'Browser', 'OS', 'Carrier', 'Time of day', 'Mood when bug occurred'. 70% of fields blank in the last 200 reports."

**Good example:**
> "Bug report template: 6 required fields (summary, steps to reproduce, expected, actual, environment, version). Optional 'attachments' field. Quarterly review of fill-rate; fields under 40% fill-rate are deprecated."

**How to catch it.** Measure fill rate per field across the last 50 uses. Any field below 50% fill is a candidate for removal or making it optional.

---

## Red Flag 3: Template with No Owner

**Symptom.** The template was created by someone who left the company. No one knows what it is for or whether it should still be used.

**Why it's bad.** Unowned templates rot. Examples become stale, instructions reference removed features, and there is no one to update them when frameworks change. The library erodes one orphaned template at a time.

**Bad example:**
> "Confluence template 'Quarterly Planning Doc' last edited 2022. Author: ex-employee. 47 pages created from it in 2025."

**Good example:**
> "Every template has a named owner (single-threaded). Owner reviews quarterly: still in use? still accurate? Updated 2026-02. If owner unidentified for 60 days, template archived."

**How to catch it.** Audit template metadata. Any template without a current employee as owner is a red flag.

---

## Red Flag 4: Instructions Buried Inside the Template

**Symptom.** The template body has the instructions ("Replace this section with your goals", "Delete this if not applicable") and authors forget to remove them. Final published pages contain the scaffolding text.

**Why it's bad.** Instructional text in the template becomes published content, which is embarrassing and signals lack of care. Worse, readers cannot distinguish guidance from content.

**Bad example:**
> Published PRD says: "**Goals:** [Replace this with 3-5 SMART goals for the feature. See PM guide for SMART criteria.] We want to improve onboarding."

**Good example:**
> Template uses Confluence info-panel macro for instructions, set to "hide on view." Author guidance is in a separate page (`/templates/prd-author-guide`) linked from the template description. Final published page contains only content.

**How to catch it.** Spot-check the last 20 pages created from the template. If any contain template instruction text, the template is broken.

---

## Red Flag 5: Linked Issues / Smart Macros That Break Silently

**Symptom.** Template includes a Jira-issues macro tied to a hardcoded JQL filter, or a page-properties report referencing a label that no one uses. Pages render with empty results.

**Why it's bad.** Authors copy the template and get a blank macro. They do not know whether it is broken or whether there is just no data. The macro becomes invisible noise.

**Bad example:**
> "Status page template embeds Jira filter `project = OLDPROJ AND status = 'In Progress'`. Project OLDPROJ archived 8 months ago. All status pages show empty issue list."

**Good example:**
> "Status page template uses a parameter (page-property) for project key. Macro guides author with placeholder text 'Set page-property `jira-project` to your project key'. Quarterly broken-macro audit via Confluence REST API."

**How to catch it.** Render the template into a sample page. Every macro should display real content or a clear "configure me" prompt — never silently empty.

---

## Red Flag 6: Version Drift across Templates

**Symptom.** PRD template was updated in March, but the RFC, post-mortem, and quarterly-planning templates still reference the old PRD section names. Documents stop cross-linking cleanly.

**Why it's bad.** Templates are an ecosystem. A change in one ripples to others; if updates are not coordinated, the library decays. Authors learn that "the templates do not match each other" and lose trust.

**Bad example:**
> "PRD template renamed 'Success Metrics' to 'Outcomes'. Retro template still asks 'did we hit the PRD's Success Metrics?'. Authors confused; some answer the old, some the new."

**Good example:**
> "Templates ship with a `template-version` page property. Cross-references use the property, not hard-coded names. Quarterly cross-template audit confirms consistency. Major changes communicated via template-release notes."

**How to catch it.** Search the template library for shared terms. Any term that means different things in different templates is drift.

---

## Red Flag 7: Template That Replicates Tribal Knowledge Instead of Encoding It

**Symptom.** The template has empty sections ("Strategy", "Risks", "Resourcing") with no prompts, no examples, no rubrics. Authors who do not already know how to fill it out produce poor pages.

**Why it's bad.** A good template is a thinking tool. It encodes the framework the author should use. Empty section headers are just paperwork.

**Bad example:**
> Template section: "**Risks:** [Add risks here.]"

**Good example:**
> Template section: "**Risks:** Use the Pre-Mortem framework — Tigers (real risks with evidence), Paper Tigers (sound risky but unlikely), Elephants (large but acceptable). For each Tiger, name owner and mitigation. See `/templates/risks-author-guide`. Example below.\n\n[Example: 'Tiger: payment provider has 99.5% SLA; launch-day traffic spike likely. Owner: platform. Mitigation: pre-warm capacity, fall-back provider configured.']"

**How to catch it.** For each section, ask: would a new joiner know how to fill this out? If not, add a prompt and an example.

---

## Red Flag 8: Templates That Lock Authors into a Single Workflow

**Symptom.** PRD template assumes a Scrum delivery model with story points; Kanban teams cannot use it. Or the post-mortem template assumes a blameful "root cause" model.

**Why it's bad.** A template that hard-codes one methodology forces all teams onto that methodology, or forces them to deviate from the template (defeating standardization). Templates should encode *outputs*, not *methodologies*.

**Bad example:**
> PRD template includes "Story points for each user story (Fibonacci 1, 2, 3, 5, 8, 13)". Kanban team using cycle-time cannot complete the section.

**Good example:**
> PRD template asks for "estimated size and timeline" with examples for story points, t-shirt sizing, or cycle-time forecasts. Methodology-neutral, output-focused.

**How to catch it.** List the templates' assumptions. Any assumption about delivery model, estimation method, or team structure should be optional or parameterized.

---

## Red Flag 9: No Template Adoption Metrics

**Symptom.** The team has spent weeks designing a new template. After launch, no one measures whether it is being used or whether quality improved.

**Why it's bad.** Template design is product work. Templates that are not measured may not be used; templates that are used may not be helping. Without metrics, you cannot iterate.

**Bad example:**
> "We rolled out the new PRD template last quarter. Hope teams are using it."

**Good example:**
> "PRD template adoption: 78% of new PRDs (target 90% by Q3). Quality leading indicators: % with measurable success metric (62% -> 84%), % with named risks (40% -> 71%). Author feedback survey quarterly."

**How to catch it.** Every template launch should declare a target adoption rate and at least one quality indicator measurable from page content.

---

## Red Flag 10: Templates Coupled to Specific People or Tools that Change

**Symptom.** Template includes hardcoded references to a specific tool ("Paste your Mixpanel dashboard URL here"), specific person ("Submit for review to Jane Doe"), or specific Slack channel that has since been renamed.

**Why it's bad.** Templates outlive specific tools and individuals. Hardcoded references rot. Authors copy stale instructions and produce broken pages.

**Bad example:**
> "PRD template: 'Get review approval from Jane Doe in #product-reviews Slack channel.'"

**Good example:**
> "PRD template: 'Get review approval from the PM Director (see /org-chart). Post in the product-reviews channel.' Org-chart and channel referenced by directory entry, not name."

**How to catch it.** Search templates for proper nouns (people, tools, channels). Each is a future failure point.

---

## Red Flag 11: Required Fields That Should Be Optional

**Symptom.** Every PRD must fill out "Competitive Analysis" — even internal tools with no competitive landscape. Authors fabricate content or leave it as "N/A".

**Why it's bad.** Mandatory-everywhere fields train authors to fill in junk. The signal value of "Competitive Analysis" drops to zero when half the answers are "N/A".

**Bad example:**
> PRD template requires Competitive Analysis. Internal-tool PRD says: "Competitors: N/A, we are the only internal tool."

**Good example:**
> PRD template has Competitive Analysis as a conditional section: "Required for customer-facing features. Omit for internal tools." Template guidance explains when to include.

**How to catch it.** For each required section, ask: would 80%+ of users have meaningful content here? If not, make it conditional.

---

## Red Flag 12: Template Library with No Discovery Surface

**Symptom.** Templates exist in a Confluence space, but nobody knows they exist. New PMs ask in Slack "what's the PRD template?" and get pointed to a personal page.

**Why it's bad.** Templates only work if authors can find them. A library without discovery is just a backup. Adoption is bounded by surface area.

**Bad example:**
> "Templates are in the 'Templates' Confluence space." (Space has no landing page, no index, not pinned, not linked from team handbooks.)

**Good example:**
> "Template catalog page: indexed by use case (PRDs, RFCs, retros, status, incident, planning). Each template has a 1-line description, owner, last-updated date. Linked from team handbook, onboarding pages, and Jira issue-create panels."

**How to catch it.** Ask 3 people in different teams: "where do you find the [X] template?" If you get 3 different answers, the discovery surface is broken.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Template Sprawl | Fewer than ~15 templates per space? |
| 2 | Fields Nobody Fills In | Each field above 50% fill rate? |
| 3 | Template with No Owner | Every template owned by a current employee? |
| 4 | Instructions Buried Inline | Instructions hidden on view, not part of content? |
| 5 | Broken Smart Macros | Macros parameterized, never silently empty? |
| 6 | Version Drift | Cross-references use page properties, not names? |
| 7 | Empty Section Headers | Every section has prompt + example? |
| 8 | Single Methodology Locked In | Outputs parameterized, not methodology? |
| 9 | No Adoption Metrics | Target adoption + quality indicator measured? |
| 10 | Hardcoded People/Tools | No proper nouns; use directory entries? |
| 11 | Required Should Be Optional | 80%+ of authors have real content for required sections? |
| 12 | No Discovery Surface | 3 random people find the template the same way? |

## Related Reading

- SKILL.md Troubleshooting section (for symptom -> root cause -> resolution)
- references/template-library-governance.md (if present)
- atlassian-admin/references/red-flags.md (for org-wide governance patterns)
