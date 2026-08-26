# Red Flags: Create PRD

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan a draft PRD before sending to stakeholders. Each red flag shows the *bad* version next to the *good* version, anchored to the 8-section structure (Summary / Contacts / Background / Objective / Market Segments / Value Prop / Solution / Release).

---

## Red Flag 1: Solution before problem

**Symptom.** The PRD opens with Section 7 (Solution) energy — feature lists, mockups, P0/P1/P2 — before the problem in Sections 3 (Background) and 5 (Market Segments) is established.

**Why it's bad.** A reader who lands on Solution first has no way to evaluate it. They cannot tell whether the features address the actual problem or whether the team has fallen in love with an implementation. Engineering builds the wrong thing.

**Bad example:**
> "Section 1 Summary: 'We will ship an AI-powered chatbot, a new dashboard, push notifications, and a Slack integration.' (Sections 3 and 5 left thin: 'Background: many customers complain about onboarding.' 'Segments: SMB and enterprise.')"

**Good example:**
> "Section 1: 'Time-constrained sales leaders lose 90 minutes per opportunity researching prospects before calls. We are reducing that to 10 minutes with auto-research.' Section 3: 'Until now this was solved by SDRs spending their day on research. New LLM capabilities make context-window-sized research feasible in seconds. Customer interviews (n=22) show this is the #2 reason quota is missed.' Section 5: 'B2B sales leaders at companies with 50-500 reps who run multiple weekly opportunity-review calls.' Section 7: 'The auto-research panel surfaces top 3 talking points from a 15-source aggregation.'"

**How to catch it.** Read Section 7 alone. Could a reader tell what problem it solves? If no, Sections 3 and 5 are too thin.

---

## Red Flag 2: Section 7 (Solution) bloat

**Symptom.** Section 7 is 8 pages long. P0 list has 24 items. Mockup references multiply.

**Why it's bad.** A PRD is not a spec. Bloated Solution sections crowd out the Why; reviewers skim; v1 scope becomes "all of it"; the release plan in Section 8 becomes incoherent because there is nothing left to cut.

**Bad example:**
> "Section 7 Solution: 8 pages, 24 P0 features, 18 P1 features, 12 P2 features, 6 nested UX subsections, references to 14 Figma files."

**Good example:**
> "Section 7 Solution: 1.5 pages. 'UX: 3 key screens (link to single Figma). Key Features: 4 P0 (numbered list, one sentence each), 2 P1, 1 P2 deferred. Tech: 2 architecture notes. Assumptions: 3 numbered with validation plan.' Section 8: 'v1 ships the 4 P0; everything else explicitly deferred to v1.1 or later.'"

**How to catch it.** Count pages in Section 7. > 3 pages on a feature-sized PRD is a flag.

---

## Red Flag 3: Market segments by demographics

**Symptom.** Section 5 says "Millennials aged 25-35 in urban areas" or "Mid-market companies in tech".

**Why it's bad.** Demographic segments are not actionable. Two 30-year-olds in San Francisco can have completely different jobs-to-be-done. Designing for demographics produces feature ambiguity. JTBD-based segments produce specific design choices.

**Bad example:**
> "Section 5 Market Segments: Segment 1: Millennials aged 25-35 in urban areas. Segment 2: Mid-market companies in tech."

**Good example:**
> "Section 5 Market Segments: Segment 1: 'Sales leaders who run 5+ pipeline-review calls per week and prepare for them between meetings, because their team's win rate depends on the quality of pre-meeting talking points.' Segment 2: 'New sales reps in their first 90 days who do not yet know the buyer journey deeply, because they need a research scaffolding to compensate for missing domain knowledge.'"

**How to catch it.** Read Section 5. If a segment includes age, geography, or industry without a "because" clause naming the job, rewrite.

---

## Red Flag 4: Section 4 KRs without baselines

**Symptom.** Key Results read "Increase activation by 30%" — no current value, no target value, no date.

**Why it's bad.** Without a baseline, "30%" is meaningless. The team will measure 30% of *something* and call it done. With no target value and date, success is a moving target.

**Bad example:**
> "KR1: Increase activation significantly.
> KR2: Drive enterprise growth.
> KR3: Improve customer satisfaction."

**Good example:**
> "KR1: D7 activation rate from 32% (Apr 2026 baseline) to 52% by Q3 end.
> KR2: Enterprise MRR from $1.2M to $2.4M by Q3 end.
> KR3 (counter): NPS stays above 42 (current 45)."

**How to catch it.** Each KR should follow the pattern "[metric] from [baseline] to [target] by [date]". Anything else is incomplete.

---

## Red Flag 5: Assumptions listed without validation plans

**Symptom.** Section 7 has an Assumptions sub-list with 4 bullets. None has an owner or a validation method.

**Why it's bad.** Listing assumptions without validating them is theater. The team writes them down and then ignores them. Production reveals that the load-bearing assumption was wrong; the project is 80% built; everyone is surprised.

**Bad example:**
> "Assumptions:
> 1. Users will accept research summaries from LLM
> 2. CRM API supports the data we need
> 3. Sales managers have time to review research before calls"

**Good example:**
> "Assumptions (each with owner + validation plan):
> 1. 'Users will accept LLM-summarized research' — owner: PM. Test: 5-user concept test by 2026-05-30. See `discovery/identify-assumptions/`.
> 2. 'CRM API supports the fields we need' — owner: Eng Lead. Test: API smoke test by 2026-05-25.
> 3. 'Sales managers have 5 min before calls to review' — owner: PM. Test: time-diary study (n=10) by 2026-06-05."

**How to catch it.** For each assumption, ask "who is testing this, by when, how?" Missing answer = unvalidated assumption.

---

## Red Flag 6: PRD reads like marketing copy

**Symptom.** Words like "seamless", "revolutionary", "transformative", "world-class" appear in Sections 1, 3, or 6.

**Why it's bad.** Marketing language hides specificity. A reviewer reading "seamless onboarding" cannot evaluate whether the team has thought through edge cases. A reviewer reading "reduces onboarding from 12 steps to 4 steps" can.

**Bad example:**
> "Section 1 Summary: 'A revolutionary, AI-powered, seamless onboarding experience that transforms how new users discover our world-class product.'"

**Good example:**
> "Section 1 Summary: 'New users currently complete 12 onboarding steps in a median of 9 minutes; 41% bail before step 7. We are cutting the flow to 4 steps targeting < 3 minutes median, by deferring 8 setup decisions to in-app contextual prompts after first value.'"

**How to catch it.** Search the PRD for: seamless, revolutionary, transformative, world-class, cutting-edge, next-generation. Replace each with specific facts.

---

## Red Flag 7: Section 8 (Release) without explicit deferral list

**Symptom.** Section 8 says "v1 ships in Q3" but does not list what is *not* in v1.

**Why it's bad.** Scope creep is the default outcome. Without an explicit deferral list, every stakeholder assumes their favorite feature is in v1. The team commits to a too-large scope; ship slips; trust erodes.

**Bad example:**
> "Section 8 Release: 'v1 targets Q3 launch. Future versions will add additional capabilities.'"

**Good example:**
> "Section 8 Release: 'v1 (Now, ships Aug 2026): 4 P0 features [list]. Explicitly deferred to v1.1 (Next, Q4 2026): mobile push, Slack integration, custom dashboards [list with rationale]. Explicitly deferred to v2 (Later, Q1 2027 or later): white-label, API marketplace [list]. Success criteria: D7 activation hits 52% (KR1) on a 30-day rolling cohort.'"

**How to catch it.** Search Section 8 for "deferred" or "explicitly not". If missing, scope is undefined.

---

## Red Flag 8: Contacts section padded

**Symptom.** Section 2 lists 14 names — exec sponsor, 3 PMs, 2 designers, 4 engineers, 2 marketing, legal, finance, "miscellaneous stakeholders".

**Why it's bad.** A 14-person contact table dilutes accountability. Nobody is sure who decides. The PRD becomes consensus-by-committee. Decisions drag.

**Bad example:**
> "Section 2: PM, Sr PM, Group PM, Eng Manager, Eng Lead, Sr Eng (2), Designer, Sr Designer, PMM, Marketing Manager, Legal Counsel, Finance Partner, Exec Sponsor."

**Good example:**
> "Section 2 (5 people): PM (Sarah K) — final decision on scope. Eng Lead (Tomas R) — technical feasibility. Design Lead (Amy L) — UX direction. PMM (Jorge M) — positioning + GTM. Exec Sponsor (VP Product, David T) — business approval. Other reviewers are listed in the project Slack but do not appear here."

**How to catch it.** Count names in Section 2. > 6 is a flag.

---

## Red Flag 9: Stale PRD treated as authoritative

**Symptom.** PRD was written Feb 2026. Engineering started building in March. It's now May. The PRD has not been updated; assumptions in Section 7 have all been validated/invalidated, but the doc still reads as if they're open.

**Why it's bad.** A PRD is a communication tool, not a contract. Stale PRDs misinform new joiners and stakeholders. They become reference artifacts that nobody trusts but everybody cites.

**Bad example:**
> "PRD last updated Feb 14. (Reality: 60% of assumptions have been validated; the architecture pivoted from monolith to event-driven; v1 scope changed.) PRD remains the doc people reference."

**Good example:**
> "PRD has a 'Changelog' at the top: 'v1.4 (May 18): assumption 1 validated via concept test; assumption 2 invalidated, scope reduced. v1.3 (Apr 5): architecture pivot — see ADR-014. v1.2 (Mar 12): KR3 target adjusted from NPS 50 to NPS 45 after baseline correction.' Each milestone review updates the doc."

**How to catch it.** Check the last-modified date. If the PRD has not been touched in > 30 days and the project is mid-build, it is stale.

---

## Red Flag 10: Value Proposition reads like internal wishlist

**Symptom.** Section 6 lists "gains" like "users will love the new interface" or "more revenue".

**Why it's bad.** Vague gains do not test against customer reality. Real value propositions name a specific job, a measurable gain, and a specific pain relieved. Without specificity, the team has no way to know if v1 delivered the value prop.

**Bad example:**
> "Section 6 Value Proposition: 'Jobs addressed: better workflow. Gains: time saved. Pains relieved: frustration. Competitive advantage: better UX.'"

**Good example:**
> "Section 6 Value Proposition for Segment 1 (sales leaders):
> Jobs: prepare for pipeline review in <10 min; coach SDR talking points using the same research.
> Gains: 80 minutes/week saved per leader; shared research artifact for the team.
> Pains relieved: skipping prep when calendar is back-to-back; reps showing up unprepared.
> Competitive advantage: integrated into existing CRM with no second tool to open; alternatives (manual + Gong + Notion) require 3 tabs."

**How to catch it.** Could the team measure each gain in 90 days? If no, the value prop is too vague.

---

## Red Flag 11: Background dodges "why now"

**Symptom.** Section 3 lists context ("customers complain about X") but never says what changed to make this feature feasible or urgent *now*.

**Why it's bad.** "Why now" is the question every exec sponsor asks. Without it, the PRD looks opportunistic — a feature the team wanted to build, dressed in a customer story. Sponsors withhold funding because they cannot tell strategic urgency from desk-driven enthusiasm.

**Bad example:**
> "Section 3 Background: 'For years, customers have asked for better search. The current search is slow and limited. We should improve it.'"

**Good example:**
> "Section 3 Background: (Context) Search is the #2 in-app event by volume; current p95 latency is 4.2s. (Why now) Three things changed in 2026: (1) Elasticsearch 9 reduces our latency floor to 800ms at our scale. (2) Two competitor releases have raised buyer expectations — our last 3 lost deals cited search. (3) Internal data pull (Apr 2026) shows search-abandon correlates 0.61 with churn. (What recently became possible) The new ES cluster lands in May; engineering capacity opens after the migration."

**How to catch it.** Read Section 3. Find the phrase "Why now". If absent, the urgency is unstated.

---

## Red Flag 12: "10-second executive test" fails

**Symptom.** Sponsor reads Section 1 (Summary) and cannot answer: "What is this? Who is it for? Why now?"

**Why it's bad.** Section 1 is the entire PRD compressed. If a busy exec cannot leave that section knowing the answer, the rest of the document will not save them. Funding decisions are made on Section 1.

**Bad example:**
> "Section 1 Summary: 'This PRD describes our plans for the upcoming quarter, focused on improvements to our product. We will be building several features across multiple workstreams, with the goal of increasing customer satisfaction and growth.'"

**Good example:**
> "Section 1 Summary: 'Auto-research panel for B2B sales leaders. Cuts pre-call research from 90 to 10 minutes per opportunity. Targeting sales leaders at 50-500-rep companies; ships Aug 2026. Built now because LLM context-window pricing dropped 4x in Q1 and our top-3 lost deals all named research time as a coaching gap.'"

**How to catch it.** Time a stakeholder reading Section 1. Ask them the three questions. If they hesitate, rewrite.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Solution before problem | Could a reader of Section 7 alone tell what problem it solves? |
| 2 | Section 7 bloat | Is Section 7 > 3 pages? |
| 3 | Segments by demographics | Does each segment include a "because [job]" clause? |
| 4 | KRs without baselines | Does each KR follow "[metric] from X to Y by date"? |
| 5 | Assumptions without validation plans | For each assumption: who, by when, how? |
| 6 | Marketing-copy adjectives | Search for: seamless, revolutionary, world-class. |
| 7 | Section 8 without deferral list | Does it list what is explicitly NOT in v1? |
| 8 | Padded Contacts section | > 6 names? |
| 9 | Stale PRD | Last updated > 30 days ago and project mid-build? |
| 10 | Value Prop reads as wishlist | Can each gain be measured in 90 days? |
| 11 | Background dodges "why now" | Does Section 3 explicitly say "why now"? |
| 12 | 10-second executive test fails | Can a reader answer What / Who / Why now from Section 1? |

## Related Reading

- SKILL.md Troubleshooting
- references/prd-writing-guide.md
- `prfaq/` (Working Backwards PR as a pre-PRD discipline)
- `discovery/identify-assumptions/` (for the validation plans in Section 7)
- `brainstorm-okrs/` (KRs in Section 4)
- `outcome-roadmap/` (Section 8 Now/Next/Later horizons)
