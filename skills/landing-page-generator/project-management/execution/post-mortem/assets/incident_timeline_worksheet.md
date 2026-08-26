# Incident Timeline Worksheet

Use this worksheet to reconstruct a complete, blameless timeline of an incident. Fill it in by interviewing each person who took an action, then merge into the post-mortem timeline section.

## How to use

1. List every person who was active in the incident chat or who took an action.
2. Schedule a 20-minute conversation with each. Conduct in 1:1, not as a group.
3. Walk them through their experience using the prompts below.
4. Record their answers below (one section per person).
5. Merge into a single chronological table in the post-mortem.

Use neutral language. The goal is to learn what they knew, when, and what they did about it — not to evaluate whether their actions were correct.

---

## Interview prompts

### Detection and awareness

- When did you first become aware of the incident? Via what channel (alert, chat, customer report)?
- What was the signal you saw? What did you initially think it meant?
- What did you check first to verify the signal?
- What other signals were present that you noticed (or did not notice) at the time?

### Decisions

- What options did you consider?
- What made you choose the option you took?
- What information did you have at that moment that informed the decision?
- What information do you wish you had had?
- Was there anyone you consulted? Anyone you wish you could have reached but could not?

### Actions

- What did you actually do, step by step?
- How did you know whether each step worked?
- When did you communicate to the rest of the team / to customers? Via what channel?

### Reflection

- What surprised you during the incident?
- What part of the system worked exactly as you would expect?
- What part of the system did not behave as you would expect?
- What tooling, documentation, or process was helpful?
- What tooling, documentation, or process was missing or unhelpful?
- If a similar incident started right now, what would you do differently? (Note: this is for system learning, not personal critique.)

---

## Per-person interview record

### Interview 1: [role, not name]

**Date:** YYYY-MM-DD

| Time (UTC) | What they observed | What they did | What they knew |
|---|---|---|---|
| HH:MM | | | |
| HH:MM | | | |
| HH:MM | | | |

**Decisions and rationale:**

- ...

**System properties they encountered:**

- ...

**Tooling / documentation observations:**

- Helpful: ...
- Missing: ...

---

### Interview 2: [role, not name]

(repeat structure above)

---

## Merged timeline (paste into post-mortem section 3)

| Time (UTC) | Event | Source |
|---|---|---|
| HH:MM | (event description) | (which interview / which log) |

## Decision points

Mark with [DECISION] in the merged timeline. For each decision, the post-mortem narrative should answer:
- What were the options at the time?
- What information was available?
- Was the decision reversible? Was that a factor?

## Anchor events

Every timeline should have these anchor events identified:

| Anchor | Time | Source |
|---|---|---|
| Trigger (what changed in the system) | HH:MM | |
| First signal (when monitoring saw it) | HH:MM | |
| Detection (when a human knew) | HH:MM | |
| Escalation (when authority was engaged) | HH:MM | |
| First mitigation attempt | HH:MM | |
| Customer impact ended | HH:MM | |
| Full resolution | HH:MM | |
| Incident closed | HH:MM | |

**Detection latency:** First signal → Detection (target < 5 minutes for Sev 1).

**Time to mitigation:** Detection → Customer impact ended (target < 30 minutes for Sev 1).

**Time to resolution:** Detection → Full resolution.

These metrics feed the team's incident-response SLOs and may surface contributing-factor patterns over time.
