# Red Flags: Summarize Meeting

> Common ways this skill's output goes wrong -- concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan every meeting summary before posting / emailing / linking it in Jira / Confluence. Each red flag has bad and good quoted examples.

---

## Red Flag 1: Minutes Without Owners

**Symptom.** "Action items: follow up with vendor, refine the spec, schedule next session."
**Why it's bad.** An action without an owner has no owner. It defaults to the meeting organizer or it dies. Either way, the team is not aligned and the next meeting starts with re-litigation of the same items.
**Bad example:**
> "Action items:
> - Follow up with vendor on SDK breaking change.
> - Refine spec for integration.
> - Schedule next sync."
**Good example:**
> "Action items:
> 1. Follow up with vendor on SDK breaking change. **Owner**: <name>. **Due**: Tue Jun 4.
> 2. Refine spec for integration. **Owner**: <name>. **Due**: Fri Jun 7.
> 3. Schedule next sync. **Owner**: <name>. **Due**: end of day."
**How to catch it.** Action items with no owner column = re-draft before sending.

---

## Red Flag 2: Decisions Buried in Narrative

**Symptom.** "We had a long discussion about the vendor situation, and after weighing options the team felt that switching might be wise."
**Why it's bad.** Decisions are the highest-value output of any meeting. Burying them in prose means people scan the summary, miss the decision, and proceed as if it had not been made. Worse, the wording is ambiguous -- did the team decide to switch, or to consider switching?
**Bad example:**
> "Discussion: the team weighed pros and cons of switching vendors. There were concerns about timeline. Ultimately the leaning was towards switching, though some open questions remain."
**Good example:**
> "**Decision**: switch from Vendor A to Vendor B by July 15.
> **Owner**: <name>.
> **Rationale**: Vendor A's SDK breaking change adds 4 weeks; Vendor B has a confirmed integration path.
> **Open questions**: contractual termination clause with Vendor A (legal owns; due Tue)."
**How to catch it.** Every decision must appear in its own labeled block (Decision / Owner / Rationale / Open Questions). Prose summaries hide decisions; surface them.

---

## Red Flag 3: No Distinction Between Decisions, Discussions, and Action Items

**Symptom.** Summary is one bulleted list mixing decisions, talking points, and to-dos.
**Why it's bad.** Each type of artifact has different downstream consumers. Decisions need to be archived as part of the decision log. Action items need to be tracked in Jira / Linear. Discussion items are just context. Mixing them means nothing is tracked properly.
**Bad example:**
> "- Vendor A is having issues.
> - Switch to Vendor B.
> - <name> will contact Vendor B.
> - Cost concern raised.
> - PM thinks we should defer."
**Good example:**
> "**Decisions** (logged in `decision-log.md`):
> - DEC-117: switch from Vendor A to Vendor B by July 15.
>
> **Action items** (logged in Jira):
> - <name>: contact Vendor B by Tue. Tracked: PROJ-422.
>
> **Discussion notes** (for context, not actionable):
> - Vendor A's SDK breaking change adds 4 weeks.
> - Cost differential is ~5%."
**How to catch it.** Single mixed list = restructure into three sections.

---

## Red Flag 4: Verbatim Transcript Pasted as Summary

**Symptom.** The summary is a 4-page transcript of who said what.
**Why it's bad.** A transcript is raw data, not a summary. It buries the signal in noise. People will not read it. Action items get lost. The whole point of the summary -- to compress -- is defeated.
**Bad example:**
> "Sarah: 'I think we should switch.'
> Tom: 'I disagree, switching costs are too high.'
> Sarah: 'But the breaking change blocks us.'
> [3 more pages of dialog]"
**Good example:**
> "Topic: vendor switch.
> Positions: Sarah advocated switching (citing 4-week delay if we stay); Tom raised switching costs (~$80k, 1-month transition).
> Decision: see DEC-117 (switch by July 15)."
**How to catch it.** Summary > 1 page of dialog with named speakers = compress.

---

## Red Flag 5: No Date or Attendees

**Symptom.** Summary headline: "Vendor discussion." No date, no attendee list.
**Why it's bad.** Six weeks later, when someone references "the vendor decision", nobody can tell which meeting. Decisions cannot be traced. Attendees who were quoted cannot be checked. The summary is unciteable.
**Bad example:**
> "# Vendor discussion
> Decisions: switch to Vendor B.
> ..."
**Good example:**
> "# Vendor discussion -- 2026-05-21 14:00 UTC
> **Attendees**: <name (chair)>, <name>, <name>. **Apologies**: <name>.
> **Linked context**: PROJ-419 (vendor evaluation), DEC-117 (this decision).
> ..."
**How to catch it.** Top of summary must have date + attendees + linked context. No exceptions.

---

## Red Flag 6: Sensitive Information Not Redacted

**Symptom.** Summary shared widely contains personnel feedback, customer-specific commercial terms, or in-flight legal language.
**Why it's bad.** Meeting summaries are circulated broadly. Including sensitive content leaks confidential information, harms trust, and may breach contracts. Once the email is sent, you cannot recall it.
**Bad example:**
> "Notes mention: 'Customer X is willing to pay 30% above list; we should not surface this'."
**Good example:**
> "Two summaries from the same meeting:
> - **Public** (shared with the project channel): topics, decisions, action items, redacted of commercials and personnel matters.
> - **Confidential** (shared only with attendees): full notes including commercial terms.
> Generator has a `--sensitivity public|confidential` flag."
**How to catch it.** Distribution list includes anyone outside the meeting = run a redaction pass.

---

## Red Flag 7: Summary Does Not Link Back to Source Artifacts

**Symptom.** "Decided to update the PRD" -- but no link to the PRD, no version reference.
**Why it's bad.** Decisions reference artifacts that change over time. Without a link, the reader has to hunt; with a stale link, the reader sees the wrong version. Either way, the decision is unmoored from the context it was made in.
**Bad example:**
> "Decision: update the PRD to reflect the new scope."
**Good example:**
> "Decision: update the PRD to reflect the new scope.
> **Source PRD**: `confluence://PROJ/prd-bulk-edit` (version as of meeting: `v1.4`, May 18 2026).
> **Owner**: <name>. **Due**: Fri Jun 4. New version expected: `v2.0`."
**How to catch it.** Decision references an artifact without a link + version = re-edit.

---

## Red Flag 8: Action Items With No Due Date

**Symptom.** "Follow up with marketing on launch copy. (No due date.)"
**Why it's bad.** Without a due date, the action item is open-ended and immediately becomes the lowest-priority thing on the owner's plate. By the next meeting, it has not been done, and the team re-discusses the same item.
**Bad example:**
> "Action: <name> follows up with marketing on launch copy."
**Good example:**
> "Action: <name> follows up with marketing on launch copy. **Due**: Fri Jun 7. **Definition of done**: a draft of the launch headline + 3 supporting paras committed to `confluence://LAUNCH/copy`."
**How to catch it.** No due date = unbounded = will not happen.

---

## Red Flag 9: Summary Generated From Audio Without Human Review

**Symptom.** AI-generated meeting transcript posted directly as summary, without anyone correcting hallucinations or mis-attributions.
**Why it's bad.** Auto-generated summaries hallucinate names, mis-attribute decisions, and sometimes invent action items that were never discussed. Posting them unreviewed propagates the errors as if they were authoritative.
**Bad example:**
> "AI-generated summary auto-posted to Slack. Includes a 'decision' that was actually a hypothetical. Two action items attributed to wrong owners."
**Good example:**
> "AI-generated draft summary is the *starting point*. The meeting chair reviews within 24h, corrects mis-attributions, removes hypotheticals, and validates owner / due-date for each action. Final summary marked `reviewed by <name>`."
**How to catch it.** No 'reviewed by' line = treat as draft, not summary.

---

## Red Flag 10: No Next-Steps or Next-Meeting Trigger

**Symptom.** Summary ends with action items but no plan for follow-up.
**Why it's bad.** Meetings often spawn next meetings or check-in points. Without explicit next-step triggers, the work stalls between meetings, and the decision-to-action gap grows.
**Bad example:**
> "Action items: <list>. End of summary."
**Good example:**
> "**Next steps**:
> - Action items tracked in Jira; updated weekly in #proj-status.
> - Mid-point check-in: Wed Jun 12, 14:00 UTC (calendar invite sent).
> - Final review: end of June, at the next vendor steering committee."
**How to catch it.** No next meeting / check-in trigger = add one before sending.

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Minutes without owners | Every action item has Owner + Due Date |
| 2 | Decisions buried in narrative | Each decision in its own labeled block |
| 3 | Mixed lists | Decisions / Actions / Discussion separated |
| 4 | Verbatim transcript | Summary > 1 page of dialog = compress |
| 5 | No date / attendees | Top of summary has both |
| 6 | Sensitive info not redacted | `--sensitivity` flag used appropriately |
| 7 | No links back | Each artifact reference includes link + version |
| 8 | Actions without due dates | Every action has a date + definition of done |
| 9 | AI-generated unreviewed | 'Reviewed by' line present |
| 10 | No next-steps trigger | Explicit next meeting / check-in point |

## Related Reading

- `SKILL.md` -- structured meeting summary template
- `references/decision-log-format.md` -- how decisions get archived
- Sibling skill: `execution/daci-framework/` -- decision rights for high-stakes meetings
- Sibling skill: `execution/status-update-generator/` -- weekly status reuses meeting decisions
- Sibling skill: `senior-pm/` (stakeholder mapping) -- audience considerations for distribution
- Sibling skill: `sprint-retrospective/` -- retro outputs follow the same pattern
