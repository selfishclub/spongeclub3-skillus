# Red Flags: Post-Mortem

> Common ways this skill's output goes wrong — concrete examples, why they're bad, and how to fix them.

## How to use this document

Scan the draft post-mortem and the action-item tracker before publishing or signing off. Each red flag shows the *bad* version next to the *good* version, anchored to Google SRE practice, John Allspaw's blameless tradition, Charles Perrow's Normal Accident Theory, and Sidney Dekker's *Field Guide to Understanding Human Error*.

---

## Red Flag 1: Blame language

**Symptom.** Narrative says "Sarah should have caught this" or "the team failed to deploy properly" or "if only the engineer had…".

**Why it's bad.** Blame language breaks the central premise of blameless review. Once people read their name attached to "should have", psychological safety collapses for the next incident. Engineers sanitize their narrative; the document loses learning value. Worse, it makes the discipline counterproductive.

**Bad example:**
> "At 14:08, Sarah should have noticed the queue depth alert and acted. She missed it because she was focused on her ticket. The on-call engineer failed to follow runbook step 3."

**Good example:**
> "At 14:08, queue depth had crossed the alert threshold but the dashboard did not surface this prominently — the on-call engineer was triaging a separate incident on the same dashboard. The runbook's step 3 references a tool that has been renamed; the engineer searched for the old name and did not find it."

**How to catch it.** Search the document for: "should have", "could have", "failed to", "if only", "did not". Replace each with a system property the team can change.

---

## Red Flag 2: Action items without owners

**Symptom.** Action items section lists 8 bullets: "Improve monitoring", "Update runbook", "Add tests". No names, no dates, no tracker tickets.

**Why it's bad.** Action items without owners do not get built. Industry data shows ~50% of post-mortem action items are never completed; the absence of owners is the most common reason. The post-mortem becomes a learning artifact with no follow-through.

**Bad example:**
> "Action items:
> • Improve monitoring on the queue
> • Update the runbook
> • Add integration tests for the error path"

**Good example:**
> "Action items:
> | # | Item | Owner | Due | Ticket | Category |
> | 1 | Add PagerDuty alert on queue depth > 5,000 with page to #payments-oncall | Tomas R | 2026-06-05 | ENG-2041 | Detect |
> | 2 | Update runbook step 3 to reference new tool name; add quick-link | Priya N | 2026-05-29 | DOC-104 | Respond |
> | 3 | Add integration test exercising connection-pool exhaustion path | Sarah K | 2026-06-12 | ENG-2042 | Prevent |"

**How to catch it.** Read each action item. Does it have: (1) one named owner, (2) a date, (3) a tracker ticket ID? Missing any = will not happen.

---

## Red Flag 3: Single "root cause" stops the analysis

**Symptom.** Post-mortem declares one root cause ("the connection pool was exhausted") and proposes one fix. No discussion of contributing factors.

**Why it's bad.** Charles Perrow's Normal Accident Theory: in tightly-coupled complex systems, there is rarely a single cause. The incident emerged from contributing factors aligning. A single-root analysis misses the other contributing factors; those factors will produce the next incident.

**Bad example:**
> "Root cause: connection pool was exhausted by a leaky batch job. Fix: add connection cleanup to the batch job. (Section ends.)"

**Good example:**
> "Contributing factors:
> 1. Connection pool exhausted (mechanical cause).
> 2. Pool size set conservatively for cost reasons; capacity planning predates current traffic shape.
> 3. Alert fired late — threshold at 95% with no 80% warn.
> 4. PagerDuty escalation path stale — primary owner rotated 6 weeks ago.
> 5. Runbook missing pool-restart command; on-call had not shadowed a database incident.
> Action items address each factor (see action item table). Allspaw's framing: 'the set of contributing factors that aligned' is the answer to 'what caused this'."

**How to catch it.** Does the analysis section name multiple contributing factors? Single-cause analysis is incomplete.

---

## Red Flag 4: Second-mortem (same incident class recurs)

**Symptom.** This is the third connection-pool-exhaustion incident in 8 months. Each had a post-mortem. Each named a different root cause.

**Why it's bad.** Recurring incidents in the same class mean previous post-mortems treated symptoms, not contributing factors — or action items from previous post-mortems were never completed. The team is paying the incident cost repeatedly without compounding learning.

**Bad example:**
> "Sept 2025: connection-pool incident. PM: 'fix the leak.' Done.
> Jan 2026: connection-pool incident. PM: 'fix the new leak.' Done.
> May 2026: connection-pool incident. PM: 'fix that other leak.' Done.
> (No structural learning across the three.)"

**Good example:**
> "This is the third connection-pool incident in 8 months. Pre-meeting audit: of 12 action items from prior 2 post-mortems, 6 are unfilled. The recurrence is a both-and: action items not built, and structural factor (pool sizing + alerting + runbook) not addressed across instances. New analysis treats this as a pattern, not a single incident. Action items: (1) finish the 6 outstanding items from prior post-mortems; (2) structural: convert from fixed-size pool to dynamic with auto-scaling; (3) process: monthly review of connection-pool metrics."

**How to catch it.** Search the team's post-mortem archive for the failure class. > 2 occurrences in 12 months = the prior post-mortems missed the structural issue.

---

## Red Flag 5: "What went well" section empty

**Symptom.** Post-mortem has Timeline, What Went Wrong, Root Cause, and Action Items. "What went well" is missing or has one bullet.

**Why it's bad.** What-went-well is the section most often skipped under time pressure. It anchors the post-mortem in learning, not blame. It also surfaces practices worth replicating — incident-response actions that reduced impact. Skipping it means losing half the learning.

**Bad example:**
> "What went well:
> (empty)
> What went wrong:
> (8 detailed bullets)"

**Good example:**
> "What went well (using `assets/what_went_well_prompts.md`):
> 1. Detection: monitoring caught the error spike within 4 minutes of onset.
> 2. Incident commander designation: clear within 6 minutes; war room opened in Slack.
> 3. Customer comms: status page updated within 15 minutes; CS team had macros within 20 minutes.
> 4. Mitigation: kill-switch flipped within 12 minutes of decision; effective.
> 5. Engineering collaboration: 3 teams contributed without coordination friction.
> 6. Documentation: timeline captured live in Slack, easy to reconstruct.
> 7. Tone: blameless ground rules from the start of the meeting; nobody got defensive.
> (These practices are now standards in the incident-response runbook.)"

**How to catch it.** Count items in What Went Well. < 3 = the section was rushed; use the prompts file to expand.

---

## Red Flag 6: Counterfactuals in the root-cause analysis

**Symptom.** Analysis says "If only the engineer had checked the dashboard at 14:05, this would have been caught earlier."

**Why it's bad.** Counterfactuals are wishes, not causes. They cannot be acted on (you cannot retroactively change what someone did). They also signal hindsight bias: what is obvious now was not obvious then. Dekker's framing: replace counterfactuals with system properties.

**Bad example:**
> "If the engineer had escalated immediately, we would have caught this. If only the rollout had been slower, the bug would have surfaced in canary."

**Good example:**
> "At 14:05, the dashboard did not show queue depth above the fold; the engineer was working on an unrelated incident on the same dashboard and did not see the queue widget. (Action item 1: surface queue depth above the fold on the on-call dashboard.) The canary stage was 5%; this bug requires concurrent batch jobs to manifest, which only triggers at higher traffic. (Action item 2: extend canary duration to 24h to cover the next batch-job interval.)"

**How to catch it.** Search for: "if only", "if X had", "would have", "should have", "could have been". Each is a counterfactual.

---

## Red Flag 7: Named individuals in the narrative

**Symptom.** Narrative uses "Sarah", "Tomas", "Priya" throughout. Engineers feel exposed; one quietly asks to leave the team.

**Why it's bad.** Names in the narrative undermine blameless culture. Even when phrased neutrally, naming an individual associates them with the incident in the searchable archive. Future managers will find it. Engineers learn to hide details to avoid future naming.

**Bad example:**
> "Timeline: 14:03 Sarah deploys the batch-job refactor. 14:07 Tomas notices the error rate. 14:10 Priya checks the runbook."

**Good example:**
> "Timeline: 14:03 the batch-job refactor deploys (PR #2042). 14:07 the on-call engineer notices the error rate via PagerDuty. 14:10 the second on-call engineer checks the runbook. (Names appear only in the Contacts table at the top and the Action Item owner column at the bottom.)"

**How to catch it.** Search the narrative for any first name. If present and the post-mortem is blameless, refactor to roles.

---

## Red Flag 8: Severity downgraded after the fact

**Symptom.** Incident was declared Sev 1 during response. Three days later, post-mortem reads "Sev 3, contained, minor customer impact".

**Why it's bad.** Severity revision downward after-the-fact looks like minimizing. It also bypasses the post-mortem SLA (Sev 1 = 5 business days; Sev 3 = optional). Engineers learn to lobby for downgrades; the discipline of consistent severity erodes.

**Bad example:**
> "Initial declaration: Sev 1. Post-mortem heading: Sev 3. Reason in line 4: 'turned out to be less impactful than we thought.'"

**Good example:**
> "Severity: Sev 1 (confirmed at incident close).
> Initial declaration: Sev 1.
> Final classification: Sev 1.
> Customer impact: 22 minutes of 500 errors on the /search endpoint; 12,400 affected sessions; 6 paid-customer escalations.
> SLA: post-mortem published within 5 business days of incident close — met (4 days)."

**How to catch it.** Compare incident-open severity to post-mortem severity. Downward revisions need explicit explanation (and rarely happen — usually upward).

---

## Red Flag 9: Generic "improve X" action items

**Symptom.** Action item: "Improve monitoring". Owner: TBD. Due: TBD.

**Why it's bad.** Unspecific action items are unimplementable. "Improve monitoring" cannot be marked done; "add an alert on queue depth > 5,000 with PagerDuty page to #payments-oncall" can. Vague items inflate the action-item count without producing improvement.

**Bad example:**
> "Action items:
> • Improve monitoring
> • Update runbook
> • Better tests
> • Train the team"

**Good example:**
> "Action items (testable acceptance criteria):
> 1. Add Datadog alert: queue_depth > 5000 sustained 5 min, paging #payments-oncall. Test: simulate threshold in staging; alert fires. Owner: Tomas R. Due: Jun 5. Ticket ENG-2041.
> 2. Replace 'restart_pool' command in runbook section 7 with 'kubectl rollout restart deployment payments-svc'. Verify by walking the runbook in a non-prod incident drill. Owner: Priya N. Due: May 29. Ticket DOC-104.
> 3. Add integration test exercising connection-pool exhaustion. Test scope: 200 concurrent batch jobs against a 50-connection pool; expect graceful degradation, not crash. Owner: Sarah K. Due: Jun 12. Ticket ENG-2042."

**How to catch it.** For each action item, ask: "what is the testable acceptance criterion?" If absent, the item is not implementable.

---

## Red Flag 10: Post-mortem becomes a sweeping retrospective

**Symptom.** Document started about a 22-minute incident. Now it covers 6 unrelated org issues, 3 hiring concerns, and a 2-page essay on engineering culture.

**Why it's bad.** Sweeping post-mortems lose focus and never publish. The specific learning from the specific incident gets diluted. Adjacent topics deserve their own retrospectives; mixing them produces document paralysis.

**Bad example:**
> "Post-mortem draft (week 3 of writing): 18 pages. Covers: the 22-minute incident, broader on-call burden, hiring backlog in SRE, the new team's onboarding gaps, last quarter's reorg, and a section titled 'culture observations'."

**Good example:**
> "Post-mortem strictly scoped to this incident. 4 pages. Adjacent themes the author noticed during interviews:
> • On-call burden — surface in next sprint retro
> • SRE hiring backlog — escalate to Eng Director separately
> • Onboarding gaps — propose a topic for the team's monthly engineering review
> Each spun off as its own work item; not in this post-mortem."

**How to catch it.** Post-mortem length. > 8 pages for a routine incident = scope creep. Compress or split.

---

## Red Flag 11: Allspaw test failure

**Symptom.** Author writes the post-mortem; doesn't ask whether the engineers in it would feel fairly represented. Three engineers separately complain in 1:1s after publication.

**Why it's bad.** Allspaw test failure is silent in the document but loud in the team. Engineers stop participating fully in future post-mortems. Future authors get sanitized narratives. The discipline degrades over months without any single visible breakdown.

**Bad example:**
> "PM publishes the post-mortem at 17:00 Friday. Sunday: two engineers DM the manager: 'I don't think the timeline represents what actually happened. It makes it look like I was the cause.'"

**Good example:**
> "Pre-publish step: Allspaw test. Author sends draft to each engineer named in the Contacts table or referenced in the timeline (by role). Question: 'does this fairly represent your experience? If not, what should change?' Wait for response or explicit OK before publishing. Of last 8 post-mortems: 3 went through revision after Allspaw test surfaced an issue. The test is a normal pre-publish gate."

**How to catch it.** Has the Allspaw test been run? If no, run it before publishing.

---

## Red Flag 12: Action-item completion not audited

**Symptom.** Post-mortem published with 9 action items. 6 months later, audit reveals: 4 completed, 3 in-progress, 2 unfilled (never tracker ticketed). Same class of incident recurs.

**Why it's bad.** Unaudited action items become "we wrote it down" theater. The team feels productive after the post-mortem and then doesn't follow through. Industry baseline of 50% completion is the result of no audit; teams with audit hit 80-90%.

**Bad example:**
> "9 action items filed. Nobody tracks completion. 6 months later, no one knows the status of most."

**Good example:**
> "Action-item audit cadence (in `assets/action_item_tracker.md`):
> Weekly: each action item owner reports status at engineering review.
> Monthly: cross-incident audit — completion rate target >= 80% at 30 days.
> Quarterly: full audit of last quarter's post-mortems; completion rate is a tracked engineering metric.
> 90-day target: >= 90% completion.
> Any item slipping past due date is escalated to the EM, who decides: accelerate, defer with rationale, or accept and document the residual risk."

**How to catch it.** Open any post-mortem from > 60 days ago. Pull the action items. What % are complete?

---

## Red Flag Quick Reference

| # | Anti-pattern | One-line check |
|---|---|---|
| 1 | Blame language | Search for: should have, could have, failed to, if only |
| 2 | Action items without owners | Each item: owner + date + ticket ID? |
| 3 | Single root cause | Are multiple contributing factors named? |
| 4 | Second-mortem | Has this class of incident recurred in the archive? |
| 5 | What-went-well empty | Count items: < 3 = rushed |
| 6 | Counterfactuals | Search for: if only, would have, should have |
| 7 | Named individuals in narrative | Search for any first name |
| 8 | Severity downgraded after the fact | Compare incident-open vs post-mortem severity |
| 9 | Generic "improve X" action items | What is the testable acceptance criterion? |
| 10 | Post-mortem as sweeping retrospective | Document length > 8 pages? |
| 11 | Allspaw test failure | Has the draft been Allspaw-tested? |
| 12 | Action-item completion not audited | What % of items from > 60 days ago are complete? |

## Related Reading

- SKILL.md Troubleshooting
- references/blameless-culture-guide.md
- references/5-whys-vs-causal-tree.md
- Google SRE Book, "Postmortem Culture: Learning from Failure"
- John Allspaw, "Blameless PostMortems and a Just Culture" (2012)
- Richard Cook, "How Complex Systems Fail" (1998)
- Charles Perrow, *Normal Accidents* (1984)
- Sidney Dekker, *The Field Guide to Understanding Human Error* (3rd ed., 2014)
- Sidney Dekker, *Just Culture* (3rd ed., 2017)
- `discovery/pre-mortem/` (pre-mortem before incidents; post-mortem after)
- `daci-framework/` (action item owner assignment)

---

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---|---|---|
| Post-mortem feels blameful despite no names | Counterfactuals ("if only", "should have") embedded in narrative | Search the document for "should", "could have", "if only"; rewrite each as a system property the team can change |
| Action items never get completed | No single owner, no tracker ticket, or no recurring review | Each item must have one named owner and a real Jira/Linear ticket; review completion in weekly engineering ops |
| Same incident class recurs | First post-mortem identified a symptom, not contributing factors; or contributing-factor action items were dropped | Re-run with Causal Tree instead of 5 Whys; audit what action items from the prior post-mortem were filed but not completed |
| Team avoids difficult observations | Psychological safety low; managers in the room creating power dynamics | Run an anonymous pre-meeting survey; consider a facilitator outside the team; separate post-mortems from performance reviews explicitly |
| Post-mortem takes more than 2 weeks to publish | Author has competing priorities or scope crept into a sweeping retrospective | Set a hard "first draft within 3 business days" rule; cut anything not directly tied to this incident; spin off broader themes into a separate retrospective |
| Executives push for a single root cause | Cultural expectation of accountability framed as blame | Educate using Normal Accident Theory framing; provide the contributing-factor list as the answer to "what caused this"; offer one-line summary that lists top 3 contributing factors |
| "What went well" section is empty | Author skipped the section under time pressure, or team culture undervalues positive observations | Use `assets/what_went_well_prompts.md`; require minimum 3 items before publishing; surface positives in distribution channels |

## Success Criteria

- Every Sev 0 / Sev 1 / Sev 2 incident has a post-mortem published within the SLA window (5 / 5 / 7 business days)
- 100% of post-mortems pass the Allspaw test ("would I send this to the engineer who pushed the button?")
- Each post-mortem has at least one item in "What went well" (minimum 3 preferred)
- Every action item has a named owner, a tracker ticket, and a due date
- Post-mortem action-item 30-day completion rate >= 70%; 90-day completion rate >= 90%
- Recurring incident classes (same failure mode within 90 days) decrease quarter over quarter
- New engineers can find post-mortems for their service within 5 minutes of starting
- Post-mortems are explicitly disconnected from performance review processes; no engineer has ever been disciplined as a direct result of a post-mortem narrative
