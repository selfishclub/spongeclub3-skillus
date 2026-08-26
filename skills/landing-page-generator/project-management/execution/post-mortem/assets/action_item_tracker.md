# Post-Mortem Action-Item Tracker

The single largest failure mode of post-mortems is that action items go unbuilt. This tracker is the system of record for action items across all post-mortems. Review weekly in the engineering operations meeting.

## Tracking principles

- Each action item has **one named owner** (a person, not a team).
- Each action item is filed as a **real ticket** in the team's tracker (Jira / Linear / GitHub Issues). The tracker ID below links back.
- Each action item has a **due date** (no more than one sprint out for P0, one month for P1, one quarter for P2).
- Each action item has **testable acceptance criteria** — "improve monitoring" is not an action item; "add a PagerDuty alert on `queue_depth > 5000` paging `#payments-oncall`" is.
- Status moves: **Open → In Progress → In Review → Done / Cancelled (with rationale)**.
- An item moves to **Cancelled** only with explicit rationale signed off by the owning team lead.

## Master tracker

| Post-mortem | Action # | Owner | Action | Tracker ID | Category | Due | Status | Closed (date) |
|---|---|---|---|---|---|---|---|---|
| INC-YYYY-NNNN | 1 | | | | prevent / detect / mitigate / respond / process | YYYY-MM-DD | Open | |
| INC-YYYY-NNNN | 2 | | | | | YYYY-MM-DD | Open | |
| INC-YYYY-NNNN | 3 | | | | | YYYY-MM-DD | Open | |

## Categories

| Category | Definition | Example |
|---|---|---|
| **Prevent** | Reduce probability of the trigger recurring | Fix the connection-leak bug |
| **Detect** | Reduce time to detection | Add alert on queue depth |
| **Mitigate** | Reduce time-to-mitigation once detected | Add kill-command to runbook |
| **Respond** | Improve incident-response process | Update PagerDuty rotation |
| **Process** | Change a team process or policy | Require error-path test coverage on PRs |

## Weekly review checklist

Run the following review in the weekly engineering ops meeting:

- [ ] List all action items due in the next 7 days. Confirm each has progress this week.
- [ ] List all overdue action items. For each: owner explains current state in one sentence, agrees a new due date, or escalates for cancellation.
- [ ] List all action items closed this week. Celebrate them.
- [ ] Audit any action items unchanged for 30 days. Escalate to the engineering lead.

## Quarterly completion-rate report

Tracked metrics:

| Metric | Target |
|---|---|
| 30-day completion rate (action items closed within 30 days of post-mortem publish) | ≥ 70% |
| 90-day completion rate | ≥ 90% |
| Cancellation rate (closed without delivery) | < 10% |
| Recurrence rate (same failure class within 90 days) | Trending down quarter over quarter |

| Quarter | 30-day | 90-day | Cancellation | Recurrence |
|---|---|---|---|---|
| YYYY Qn | % | % | % | count |

## Common failure modes (of the tracker itself)

| Symptom | Resolution |
|---|---|
| Action items pile up with no owner shipping | Reassign to the engineering lead; if unclear who owns, the owning team lead is the default |
| Owner left the team | Reassign within 7 days; do not let action items sit orphaned |
| Item still open after 90 days | Either reset scope to something achievable, or cancel with written rationale |
| Same action item appears in multiple post-mortems | The recurrence itself is a learning; bundle into a single P0 with executive visibility |
| Tracker out of date with Jira/Linear | Designate a single owner for tracker hygiene; sync weekly |

## References

- Google SRE Book, "Postmortem Culture: Learning from Failure" — https://sre.google/sre-book/postmortem-culture/
- See `references/blameless-culture-guide.md` for why action-item completion is the loudest signal of post-mortem-culture seriousness
