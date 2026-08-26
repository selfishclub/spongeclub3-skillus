# "What Went Well" Prompts

The "What Went Well" section is the most-often-skipped section of post-mortems and one of the highest-leverage. It:

- Surfaces practices, tooling, and decisions worth replicating across the team.
- Anchors the document in learning rather than blame avoidance.
- Builds psychological safety. A post-mortem that only catalogs failures becomes a punishment artifact even with the best intentions.
- Identifies what the team already does that the next incident should preserve.

Aim for a **minimum of 3 items**, ideally 5-7. If the section is genuinely empty, that itself is a finding — the team should investigate why nothing in the response went well.

## Prompts by phase

### Detection

- What signal first told us something was wrong? Was that signal designed to fire for this class of failure?
- How fast was detection compared to past incidents in this class?
- Did anyone notice through a non-paged channel (chat report, customer support, manual dashboard check)? That informal detection might be worth formalizing.
- Did a dashboard, an alert, or a log line make the cause obvious within seconds of looking?

### Communication

- Was the incident chat opened promptly? Was the right channel used?
- Did the team adopt clear roles (incident commander, scribe, communications) without confusion?
- Did external communication (status page, customer email, exec brief) go out at the right time and with the right tone?
- Was anyone notably good at translating between engineering detail and customer/exec language?

### Decision-making

- Was a critical decision made with limited information that, in hindsight, was the right call? That tells you something about the team's judgment process.
- Did the team avoid a tempting-but-wrong path (e.g. resisted "let's just restart everything" when the right move was to investigate first)?
- Was a reversible decision made quickly and an irreversible decision deliberately? That is decision hygiene worth naming.

### Tooling

- What tool, dashboard, or runbook step saved time?
- What recent investment in tooling paid off during this incident? (Especially if the investment was contested at the time.)
- What automation worked as designed?

### Mitigation

- What was the time-to-mitigation? Compare to past incidents.
- Did the rollback or feature-flag-disable work cleanly?
- Did failovers behave as designed?

### Containment

- Was customer impact smaller than it could have been? Why?
- Was the blast radius reduced by a recent architectural change (cell isolation, circuit breaker, rate limit)?

### Team behavior

- Did anyone bring outside expertise quickly (calling another team, an SRE on a non-rotational page)?
- Did anyone explicitly slow down to think when the team was in panic mode?
- Did a junior engineer ask a clarifying question that unlocked a path?
- Did the team avoid heroics — using documented process rather than improvisation under pressure?

### Recovery

- Was the customer-impact end clearly verified rather than assumed?
- Was the post-incident verification thorough?
- Did the team return to BAU work cleanly, or did the incident leave on-call exhausted? (Recovery wellbeing is part of post-incident health.)

## Anti-patterns when writing this section

- **Backhanded compliments.** "What went well: the team eventually figured it out." This is what-went-wrong dressed up. Remove.
- **Generic statements.** "Communication was good." Be specific: "The incident commander posted status updates every 10 minutes in #incident-payments, which kept exec stakeholders from interrupting the response work."
- **Listing the absence of bad things.** "Nobody panicked." Reframe to the positive presence: "The team paused for 90 seconds at minute 4 to confirm the leading hypothesis before acting."
- **Only naming tools, never people-system practices.** Tools matter, but so do practices. Both belong.

## Examples of good "what went well" entries

Drawn from anonymized post-mortems:

1. "The 80% pool-utilization warning alert (added after INC-2024-0089) fired at minute 2, giving on-call 6 minutes of headroom before the saturation alert at minute 8. The warning alert prevented a complete outage."
2. "The incident commander explicitly named a scribe at minute 4. The scribe's running log made the post-mortem timeline trivial to reconstruct and reduced post-mortem authoring time by an estimated 4 hours."
3. "Three engineers from different teams joined within 2 minutes of the page. The cross-team on-call rotation, despite being controversial when introduced, paid off — having a database engineer on the call from minute 3 enabled mitigation at minute 14 rather than minute 30+."
4. "Customer support's standard incident comm template (introduced in Q1) was published to the status page within 6 minutes of detection. Enterprise customers reported the proactive comm before they had noticed the outage."
5. "The runbook entry 'How to drain a node safely' was used directly, copy-pasted, and worked first try. The runbook had been reviewed 3 weeks prior."
6. "An on-call engineer pushed back on the suggested 'just restart Postgres' option at minute 11 and asked for 2 minutes to verify the hypothesis. The verification revealed the connection-leak source, which made the targeted mitigation possible. A blind restart would have masked the cause and likely caused a recurrence."
7. "The feature-flag rollback (`paymentApi.v2`) worked as designed at minute 17, ending customer impact within 30 seconds of the flag flip."

## When the section is truly empty

If after honest reflection the team cannot find 3 things that went well, that is a finding. Possibilities:

- The incident was the team's first of its kind. (Then "what went well" might be "the team learned a lot, and the documentation produced will help next time".)
- The team is exhausted and underinvested in tooling. (Then the post-mortem should surface this as a contributing factor and action item.)
- Psychological safety is too low for honest reflection. (Then escalate the cultural concern separately.)

Do not publish a post-mortem with an empty "What went well" section without explicitly noting why it is empty and what the team is doing about it.
