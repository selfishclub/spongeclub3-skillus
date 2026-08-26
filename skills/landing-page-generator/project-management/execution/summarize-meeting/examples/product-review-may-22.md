# Example: Structured Summary of a Product Review Meeting

> Real-world scenario showing how to apply this skill end-to-end.

## Context

Acme Analytics (B2B analytics SaaS, Series B, 80 people) runs a biweekly Product Review. Eight people attend: VP Product, VP Engineering, three PMs, two engineering leads, and the Head of Design. The meeting is 75 minutes and the agenda is usually too full. The PM hosting (Priya) writes a structured summary after every session.

This session covered the Search Platform mid-quarter check-in, a tense decision about a deprecated API, a hiring update, and a stuck cross-team dependency. Four decisions and twelve action items came out. Without a structured summary, half of them would be lost in Slack by Tuesday.

## Inputs

- Attendees: 8 (VP Product, VP Eng, 3 PMs, 2 eng leads, Head of Design)
- Date: 2026-05-22, 14:00-15:15 PT
- Agenda items: 5
- Decisions captured: 4
- Action items: 12
- Format target: Notion page + Slack thread summary

## Applying the skill

1. **Capture the meeting's purpose** in one line at the top: "Mid-quarter check on Search Platform, decide on legacy API sunset date, surface cross-team blockers."
2. **List attendees + apologies** explicitly. Future readers need to know who was in the room.
3. **Summarize each agenda item** in <=4 sentences. The summary is *what was said and concluded*, not a transcript.
4. **Decisions go in a numbered table** with owner + DACI role + reversibility note.
5. **Action items go in a separate numbered table** with owner + due date + linked ticket.
6. **Add a "What we did not decide"** section. The unresolved items are often more important than the resolved ones.

## The artifact

---

# Product Review -- 2026-05-22

**Purpose:** Mid-quarter check on Search Platform, decide on legacy API sunset date, surface cross-team blockers, hiring update.

**Date / time:** 2026-05-22, 14:00-15:15 PT (75 min)
**Facilitator:** Priya Iyer (PM, Search Platform)
**Note-taker:** Priya Iyer
**Next session:** 2026-06-05, 14:00 PT

### Attendees (8)

| Role | Person |
|------|--------|
| VP Product | Mira Chen |
| VP Engineering | Devraj Sundaram |
| PM, Search Platform | Priya Iyer |
| PM, Workspace | Tomas Veliz |
| PM, Onboarding | Hari Patel |
| Eng Lead, Search | Sarah Khoury |
| Eng Lead, Workspace | Marcus Vella |
| Head of Design | Ines Petrov |

**Apologies:** none

### Agenda

1. Search Platform mid-quarter check (15 min)
2. Legacy `/v1/search` API sunset decision (15 min)
3. Cross-team blocker: Search analytics dashboard from Data team (10 min)
4. Hiring update (10 min)
5. Open mic + parking lot (15 min)
6. Decisions, actions, recap (10 min)

### Summaries by agenda item

**1. Search Platform mid-quarter check.** Priya reported Yellow status, mostly on track. Latency win (480ms -> 210ms p95) celebrated. Two new risks raised: BigQuery cost spike post-rebuild ($12K/month overrun) and upstream telemetry data quality (3% null user_id). Mira asked whether the activation OKR is still on track if synonym expansion holds at 14% CTR uplift; Priya said yes if rollout is gated on narrow-query precision. Devraj asked if backend hire (starts Jun 8) is in time for Q3 Snowflake commitment; Priya said yes with pair-programming ramp plan.

**2. Legacy `/v1/search` API sunset decision.** Tomas presented the proposal: deprecate `/v1/search` on 2026-09-01, full sunset 2027-01-01. Three customer accounts still on v1 (one strategic: Skyway). Devraj pushed back -- proposed Skyway gets a 60-day extension. Group decided: deprecate 2026-09-01 as planned, sunset 2027-01-01, Skyway gets a contracted carve-out through 2027-04-01 with a written exception. Mira to brief Skyway CSM.

**3. Cross-team blocker: Search analytics dashboard.** Priya flagged that the data team has the dashboard request as #4 in their queue, blocking CSM team. Devraj said he will talk to Head of Data on Tuesday May 26. Decision deferred until that conversation. Hari noted the same Data-team contention affects Onboarding -- raised to "watch list."

**4. Hiring update.** Devraj reported two open reqs: senior backend (offer accepted, starts Jun 8) and senior data engineer (final round next week, two candidates). Ines flagged that Design is also hiring (one open req for product designer, Ines plans to extend offer this week). Mira asked about contractor budget for Q3 cover; Devraj confirmed $40K available.

**5. Open mic.** Two items raised: (a) Tomas proposed a Working Backwards PR/FAQ exercise for the multi-tenant feature -- group agreed in principle; Tomas to schedule. (b) Ines flagged usability research is two weeks behind because user-research vendor delivery slipped -- moved to parking lot for Devraj + Ines offline.

### Decisions (4)

| # | Decision | Owner | DACI role | Reversible? |
|---|----------|-------|-----------|-------------|
| D1 | Sunset `/v1/search` API on 2027-01-01 with deprecation 2026-09-01 | Tomas Veliz | Driver | Hard to reverse (customer migration started) |
| D2 | Grant Skyway Logistics a contracted carve-out through 2027-04-01 | Mira Chen | Approver | Yes (renewable annually) |
| D3 | Search Platform stays Yellow; no escalation; revisit at next review | Priya Iyer | Driver | Easily reversible |
| D4 | Schedule PR/FAQ Working Backwards session for multi-tenant feature | Tomas Veliz | Driver | Easily reversible |

### Action items (12)

| # | Action | Owner | Due | Linked ticket |
|---|--------|-------|-----|---------------|
| A1 | Send written exception memo for Skyway carve-out (CC: Legal, CS) | Mira Chen | 2026-05-26 | -- |
| A2 | Brief Skyway CSM on carve-out terms | Mira Chen | 2026-05-26 | -- |
| A3 | Publish `/v1/search` deprecation notice in docs and customer email | Tomas Veliz | 2026-06-01 | DOC-412 |
| A4 | Talk to Head of Data about dashboard priority | Devraj Sundaram | 2026-05-26 | -- |
| A5 | Update mid-quarter status note with risks in the risk register | Priya Iyer | 2026-05-23 | RISK-018, RISK-019 |
| A6 | BigQuery cost optimization spike + materialized view design | Sarah Khoury | 2026-05-27 | PR-4615 |
| A7 | Upstream telemetry data quality root-cause coordination | Priya Iyer | 2026-05-29 | TEL-008 |
| A8 | Pair-programming ramp plan for new backend hire | Sarah Khoury | 2026-06-08 | HIRE-022 |
| A9 | Schedule PR/FAQ session for multi-tenant feature | Tomas Veliz | 2026-06-05 | -- |
| A10 | Extend product designer offer | Ines Petrov | 2026-05-23 | HIRE-024 |
| A11 | Discuss user-research vendor slip offline | Ines + Devraj | 2026-05-26 | -- |
| A12 | Synonym expansion rollout gate: confirm narrow-query precision >=95% | Priya Iyer | 2026-05-29 | PR-4533 |

### What we did *not* decide

- Whether Search analytics dashboard moves to #2 in Data team's queue (waiting on A4)
- Whether to backfill Snowflake connector capacity with a contractor (pending hire ramp)
- Multi-tenant feature scope -- to be addressed in the PR/FAQ session (A9)

### Parking lot

- User-research vendor slip (taken offline by Ines + Devraj)
- Q3 OKR draft -- need a half-day session before June 12

### Recap (sent to #pm-leadership Slack)

> **PR -- 2026-05-22 -- recap**
> 4 decisions: v1 search sunset 2027-01-01 with Skyway carve-out; Search stays Yellow; PR/FAQ for multi-tenant.
> 12 actions, all logged in [Notion link].
> Open: Data team dashboard priority (Devraj + Head of Data this week).
> Next session: Jun 5, 14:00 PT.

## Why this works

- The summary states the meeting's purpose in one line. Anyone scanning later knows whether this is the meeting they care about.
- Decisions are in a table, numbered, with DACI roles. Future readers can re-litigate by referring to "D2" rather than "the Skyway thing in the May meeting."
- Action items each have an owner *and* a due date *and* (when applicable) a linked ticket. Action items without all three usually do not happen.
- "What we did not decide" is a named section. Surfacing the unresolved set is often the most useful artifact of the meeting.
- The Slack recap is a 5-line summary of the summary. The full doc is for those who need it; the recap is for everyone else.

## What's next

- Confirm decisions are reflected in `../release-notes/` (for D1) and `../daci-framework/` (for D2).
- Update the cross-team dependency tracker via `../dependency-map/` after A4 conversation.
- Mid-quarter status update reflects new risks via `../status-update-generator/`.
- PR/FAQ for multi-tenant feature uses `../prfaq/` skill.
- Re-confirm action item ownership at the next Product Review on 2026-06-05.
