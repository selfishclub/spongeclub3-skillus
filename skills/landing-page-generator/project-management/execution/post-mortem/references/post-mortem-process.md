# Post-Mortem Process

> Read this when running a post-mortem end to end: severity thresholds, the 10-section template, the Day 0 → Day 30 workflow, action-item follow-through, distribution/archive practice, and the artifact (assets) inventory.

## Severity Thresholds

| Severity | Customer impact | Post-mortem required? | Distribution |
|---|---|---|---|
| **Sev 0 / Sev 1** | Full outage, data loss, security incident | Mandatory; within 5 business days | All engineering + execs |
| **Sev 2** | Partial outage, major degradation, payments impact | Mandatory; within 7 business days | All engineering |
| **Sev 3** | Single-feature degradation, recoverable | Optional unless novel pattern | Owning team |
| **Sev 4** | Minor issue, manual workaround available | Skip unless near-miss | None |
| **Near miss** | Almost caused Sev 0/1/2 | Recommended | Owning team + SRE |

Severity is set at incident open and confirmed at incident close; it can be revised upward but rarely downward.

## Post-Mortem Template Sections

A standard post-mortem has 10 sections, in this order:

1. **Header** — title, date, severity, duration, status (draft / final), authors.
2. **Summary** — 3-5 sentences. What happened, who was affected, how it was resolved, what the durable fix is. A reader who reads only this section should still know the headline.
3. **Impact** — customers affected (count and segments), revenue impact, SLO error budget burned, internal teams blocked.
4. **Timeline** — minute-by-minute log of events from detection to resolution. Include the trigger, detection, escalation, mitigation, and resolution timestamps. Mark "moment of decision" rows.
5. **What went well** — actions, tooling, or decisions that reduced impact. This section is critical and is the one most often skipped. It anchors the document in learning, not just blame avoidance, and surfaces practices worth replicating.
6. **What went wrong** — the system conditions that allowed the incident to happen and to persist. Phrased as system properties, not human failures.
7. **Contributing factors** — the list of conditions that, in combination, produced the outcome. Distinguish from root cause (below).
8. **Root cause analysis** — 5 Whys or Causal Tree (see `references/5-whys-vs-causal-tree.md`). Document the method used.
9. **Action items** — durable changes. Each item has an owner, a due date, a tracking issue ID, and a category (prevent / detect / mitigate / respond / process).
10. **Lessons learned** — broader patterns the team takes away. These often inform engineering standards, runbooks, or hiring.

## Workflow

### Day 0 (incident close)

1. Incident commander declares the incident resolved and assigns an author.
2. Author opens the post-mortem document from `assets/post_mortem_template.md`.
3. Fill in Header, Summary (placeholder ok), Impact, and the Timeline scaffold from the incident chat transcript.
4. Schedule the post-mortem meeting within the SLA window (5 business days for Sev 1, 7 for Sev 2).

### Day 1-3 (drafting)

1. Author interviews everyone who took an action during the incident. Use the prompts in `assets/incident_timeline_worksheet.md`.
2. Refine the Timeline with every action, decision, and observation. Mark decision points.
3. Draft "What went well" using `assets/what_went_well_prompts.md`. Aim for 3-7 items minimum.
4. Draft "What went wrong" and "Contributing factors".
5. Run the chosen root-cause method (5 Whys or Causal Tree).

### Day 3-5 (review)

1. Hold the post-mortem meeting. 60-90 minutes. Agenda:
   - 5 min: blameless ground rules read aloud
   - 15 min: Timeline review
   - 15 min: What went well + what went wrong
   - 20 min: Root cause discussion
   - 20 min: Action items (owner + due date for each)
   - 5 min: Lessons learned
2. Apply the Allspaw test to the document.
3. Author finalizes and the incident commander signs off.

### Day 5-30 (follow-through)

1. Each action item is filed in `assets/action_item_tracker.md` and the team's tracker (Jira, Linear, GitHub Issues).
2. Action items are reviewed at sprint planning and at the weekly engineering review.
3. After 30 days, audit the action-item completion rate. Industry data shows ~50% of post-mortem action items are never completed; the team should track and target a higher rate.

## Action-Item Follow-Through

The single largest failure mode of post-mortems is that action items go unbuilt. Mitigations:

- **Each action item has a single named owner** (a person, not a team) and a due date no more than one sprint out for high-priority items.
- **Each action item is a real ticket** in the team's tracker, not a bullet in a doc. Link the ticket from the post-mortem.
- **Action-item review is on a recurring agenda** — weekly engineering review or monthly post-mortem audit. Completion rate is a tracked metric.
- **The owner has authority**, not just responsibility. If the action requires another team, escalate to a program manager or use `daci-framework/` to assign decision rights.
- **Acceptance criteria are testable.** "Improve monitoring" is not an action item. "Add an alert on queue depth > 5,000 with PagerDuty page to #payments-oncall" is.

## Post-Mortem Distribution & Archive

| Audience | Format | Channel |
|---|---|---|
| Owning team | Full document | Team wiki, Jira/Linear linked |
| All engineering | Full document | Engineering-wide channel, weekly digest |
| Executives (Sev 0/1) | Summary + Impact + Action items | Exec email or weekly review |
| Public (if customer-impacting) | Public-facing status-page postmortem | status.<company>.com |
| Future engineers | Searchable archive | Wiki tag `post-mortem`, indexed by service |

Post-mortems should be discoverable. A new engineer joining the team should be able to find every past incident on the services they own within 5 minutes. Tag every post-mortem with the affected services, the date, the severity, and the failure class.

## Tools / Artifacts

This skill is template-driven. No Python automation. The artifacts are:

| Artifact | Purpose |
|---|---|
| `assets/post_mortem_template.md` | Full Google SRE-style template, ready to copy and fill |
| `assets/incident_timeline_worksheet.md` | Interview prompts and timestamp scaffolding |
| `assets/action_item_tracker.md` | Spreadsheet-style tracker for action items across post-mortems |
| `assets/what_went_well_prompts.md` | 20+ prompts to draw out positive observations |
| `references/blameless-culture-guide.md` | Deep dive on blameless principles, with examples of blameful vs blameless phrasing |
| `references/5-whys-vs-causal-tree.md` | When to use each method, with worked examples |
