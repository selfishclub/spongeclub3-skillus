# Example: Blameless Post-Mortem for a 47-Minute Payment Outage at Northwind SaaS

> Real-world scenario showing how to apply Google SRE blameless post-mortem practice end-to-end.

## Context

Northwind SaaS is a Series-B B2B subscription product (~$15M ARR). On 2026-05-18 at 14:23 ET, the payments service returned 500 errors for new subscription signups and invoice charges. The outage lasted 47 minutes (14:23 to 15:10 ET). Approximately 184 paying customers were affected: 12 trials failed to convert to paid, 41 invoice charges failed, 4 enterprise renewals stalled.

The incident commander was the on-call SRE. The PM (Asha Ravi, Head of Product) is facilitating the post-mortem 4 business days later, per the Sev1 mandate. Engineering, Eng leadership, SRE, and the CFO will attend the review meeting.

Asha must produce a blameless post-mortem document, identify durable action items, and deliver lessons to the org without naming individuals in any narrative.

## Inputs

- PagerDuty + Datadog incident timeline (auto-exported)
- Slack `#incident-payments-2026-05-18` channel transcript (87 messages)
- Stripe webhook + retry logs
- Customer support ticket volume during incident: 23 tickets, 8 escalations
- Internal estimate of revenue impact: ~$31k of failed charges (most retried successfully overnight)

## Applying the skill

1. **Pulled raw evidence** from PagerDuty, Datadog, Slack -- before writing anything, to anchor in mechanism rather than narrative.
2. **Set up the timeline** in chronological order; tagged "moment of decision" rows.
3. **Wrote sections 1-4** (header, summary, impact, timeline) with role labels only -- no names in narrative.
4. **Ran a 5 Whys** on the immediate cause, then expanded into a causal tree because the failure had multiple parallel contributors.
5. **Wrote sections 5 (went well), 6 (went wrong), 7 (contributing factors)** -- and made section 5 longer than section 6, on purpose. This is the section most teams skip.
6. **Drafted action items** with owners + due dates + categories (prevent / detect / mitigate / respond / process).
7. **Ran the Allspaw test** on the draft: would the engineer who pushed the button feel this represents their experience fairly? Revised once after the on-call SRE flagged a sentence as implying counterfactual blame.

Key decision quoted: *"The action item is 'add canary stage for payments service deploys', not 'be more careful with deploys'. Process changes the outcome; individual care does not."*

## The artifact

````markdown
# Post-Mortem: Payments Service Outage 2026-05-18

**Severity:** Sev1
**Duration:** 47 min (14:23 - 15:10 ET)
**Status:** FINAL
**Authors:** Asha Ravi (PM, facilitator), N. Park (SRE on-call), L. Chen (Eng on-call), M. Patel (Eng Lead)
**Date of write-up:** 2026-05-22

## 1. Summary

On 2026-05-18 at 14:23 ET, the payments service began returning 500 errors on new subscription signups and invoice charges. The proximate cause was a deploy of the billing-service worker that introduced a regression in the database-connection lifecycle; the worker leaked connections under load, exhausting the pool within 11 minutes. Detection took 4 minutes; escalation was prompt; mitigation took 32 minutes -- mostly because the runbook lacked a pool-restart command and the on-call had not shadowed a payments incident. The durable fix is a canary deploy stage for the payments service plus connection-pool health alerts at 80% utilization.

## 2. Impact

- Duration: 47 minutes
- Affected customers: ~184
- Failed transactions during the window:
  - Trial-to-paid conversions: 12 (all retried successfully within 24h; 11/12 converted)
  - Invoice charges: 41 (all retried successfully overnight; 40/41 cleared)
  - Enterprise renewal API calls: 4 (3 cleared automatically; 1 required manual support)
- Estimated revenue at risk: ~$31k; actual lost revenue: ~$1.4k (the 1 unconverted trial)
- Support tickets opened during window: 23 (8 escalated to engineering)
- SLO error budget consumed: 38% of the monthly budget in a single event
- Brand impact: 2 customer Slack messages and 1 Twitter/X mention; no press coverage

## 3. Timeline

Times in ET. Roles, not names.

| Time | Event | Source |
|---|---|---|
| 14:18 | Billing-service deploy v3.14.2 begins (single canary not present in this service; deploy is all-at-once) | CI logs |
| 14:21 | Deploy completes; service running new version | CI logs |
| 14:23 | First 500 errors on `/charge` endpoint | Datadog |
| 14:24 | DB connection pool reaches 95% utilization | Datadog |
| 14:25 | DB connection pool reaches 100% | Datadog |
| 14:27 | **First page** -- PagerDuty alert on 500-rate > 1% | PagerDuty |
| 14:28 | On-call SRE acknowledges; opens `#incident-payments-2026-05-18` | Slack |
| 14:32 | **Moment of decision**: SRE considers rollback vs investigate; chooses to investigate first (rollback estimate 3 min, investigation could be faster) | Slack |
| 14:35 | SRE identifies connection-pool exhaustion in dashboard | Datadog |
| 14:36 | Eng on-call paged | PagerDuty |
| 14:38 | Eng on-call online; pair with SRE | Slack |
| 14:41 | Hypothesis: connection leak in new deploy | Slack |
| 14:43 | **Moment of decision**: rollback decided | Slack |
| 14:48 | Rollback triggered | CI |
| 14:52 | Rollback completes | CI |
| 14:54 | Connection pool still at 100%; rollback alone insufficient | Datadog |
| 14:56 | **Moment of decision**: pool restart needed | Slack |
| 14:59 | Runbook consulted; no pool-restart command found | Slack |
| 15:03 | Eng Lead joins; provides pool-restart command from memory | Slack |
| 15:05 | Pool restart issued | CLI |
| 15:08 | Error rate begins dropping | Datadog |
| 15:10 | Error rate back to baseline; incident declared resolved | PagerDuty |
| 15:25 | Customer comms email sent | PMM |
| 15:40 | Status page updated to "resolved" | DevOps |

## 4. What went well

This section is intentionally first. The team did several things that limited the blast radius and should be replicated.

1. **Detection in 4 minutes.** The 500-rate alert fired quickly and at the right threshold. The alert wording (-`500-rate > 1% sustained 60s`) was specific enough that the on-call did not have to debug whether the alert was real.
2. **Clear incident channel from minute 5.** A dedicated Slack channel was opened within 1 minute of paging. All decisions were captured in writing in real time, which made this post-mortem possible.
3. **Eng on-call paired within 2 minutes of being paged.** The pairing reduced the time-to-hypothesis from what a single responder would have taken.
4. **Rollback was decided in 20 minutes from first page.** Some incidents linger an hour before rollback is even considered. The on-call escalated to "let's roll back" early.
5. **Customer comms went out 15 minutes after resolution, with a clear apology and a refund offer where applicable.** The Support and PMM teams executed cleanly on the comms runbook.
6. **Stripe's automatic retry caught 96% of failed charges.** Our integration is configured to allow downstream retry, which converted a $31k revenue-impact scenario into a $1.4k actual loss.

## 5. What went wrong

System conditions that produced the outcome. No names. Phrased as system properties.

1. **The payments service does not have a canary deploy stage.** The deploy went to 100% of traffic at once; there was no opportunity to detect the regression in a small slice before broad impact.
2. **The connection-pool utilization alert did not fire until 95%, by which point the pool was 24 seconds from exhaustion.** No earlier warn alert existed (e.g., at 80%).
3. **The runbook lacked a pool-restart command.** When rollback alone proved insufficient, the team improvised. The pool-restart command lives in tribal memory rather than the runbook.
4. **The test suite did not exercise the connection-pool exhaustion path.** A refactor in March moved an `await db.close()` call into a code path that the test suite did not cover.
5. **The deploy that introduced the regression passed CI** despite the unit test coverage gap.
6. **The on-call SRE had not shadowed a payments-service incident.** This is the first major payments incident in 7 months; the rotation has churned since then.

## 6. Contributing factors

A breakdown of what combined to produce the outcome.

```
Outcome: Payments service returned 500s for 47 minutes
├── Connection pool exhausted
│   ├── Code defect: connection leak in error path (introduced in deploy v3.14.2)
│   │   ├── Refactor in March 2026 moved db.close() into a branch that did not always execute
│   │   └── Test suite did not cover the affected branch
│   └── Pool size sized for normal load, not headroom for leak under load
├── Detection slower than ideal
│   └── No warn-level alert at 80% pool utilization (only critical at 95%)
├── Mitigation took 32 minutes
│   ├── Runbook missing pool-restart command
│   ├── On-call had not shadowed a payments incident
│   └── Deploy lacked canary stage (could not partial-rollback)
└── Customer impact exposure was high
    └── No graceful-degradation mode for /charge (fails closed, no retry queue)
```

## 7. Root cause analysis (5 Whys, expanded)

Method used: 5 Whys, with a causal tree as the secondary analysis (above). Documented both.

```
1. Why did /charge return 500s for 47 minutes?
   -> Because the database connection pool was exhausted.

2. Why was the pool exhausted?
   -> Because a deploy introduced code that leaks connections on the
      error path.

3. Why did the deploy not catch this?
   -> Because the test suite does not exercise the error path that
      leaks, and the deploy went straight to 100% traffic.

4. Why did the test suite not exercise that path?
   -> Because the connection lifecycle is managed via a context
      manager that was bypassed by an early return introduced in the
      March refactor.

5. Why did the early return land without catching this?
   -> Because there is no canary deploy stage for the payments
      service, and connection-pool-utilization metrics are not part
      of the deploy health check.
```

The 5 Whys converge on two systemic conditions:

1. No canary stage for the payments service.
2. No pool-utilization signal in the deploy health check.

The causal tree adds:

3. Detection alerting threshold is too late (95% only).
4. Runbook missing pool-restart command.
5. On-call training gap (first payments incident in 7 months).

## 8. Action items

| # | Action | Category | Owner | Due | Tracking |
|---|---|---|---|---|---|
| AI-1 | Add canary deploy stage for payments service (5% -> 25% -> 100%) | Prevent | Eng Lead | 2026-06-12 | PAY-441 |
| AI-2 | Add deploy health check that includes connection-pool utilization | Prevent | SRE | 2026-06-12 | PAY-442 |
| AI-3 | Add unit + integration tests for the connection-leak code path | Prevent | Eng on-call | 2026-06-05 | PAY-443 |
| AI-4 | Add 80% pool-utilization warn alert + 95% critical alert | Detect | SRE | 2026-05-29 | PAY-444 |
| AI-5 | Add pool-restart command + rollback playbook to the runbook | Mitigate | SRE | 2026-05-29 | PAY-445 |
| AI-6 | Conduct payments-incident shadow exercise for all on-call engineers | Process | Eng Lead | 2026-06-26 | PAY-446 |
| AI-7 | Add graceful-degradation queue for /charge endpoint (fail-soft retry queue) | Mitigate | Eng on-call | 2026-07-15 | PAY-447 |
| AI-8 | Quarterly payments-service game-day exercise | Process | SRE Lead | 2026-08-01 | PAY-448 |
| AI-9 | Quarterly review of deploy patterns across all critical services to identify other "no canary" exposures | Process | Eng Lead | 2026-07-01 | PAY-449 |

## 9. Lessons learned

For broader engineering and product organization:

1. **Critical-service deploys need canary stages by default.** This is the second incident in 18 months where a missing canary stage turned a small defect into a large incident. Engineering standards now require canary for any service marked "critical" (defined as: payments, auth, share-link service, customer-facing API).
2. **"It works in tests" is not "it works under load."** The connection-leak path passed CI; production traffic was the first thing that exercised it. Critical paths need integration tests that simulate load and failure.
3. **Runbook gaps are a recurring source of mitigation delay.** Every post-mortem in 2026 has identified at least one runbook gap. The pattern suggests we need a runbook ownership and review cadence, not just incident-driven patches.
4. **On-call rotation freshness matters.** A first-incident-in-7-months responder is at a disadvantage versus regular practice. Game-day exercises mitigate this.
5. **"What went well" is at least as informative as "what went wrong".** Detection-in-4-minutes and rollback-in-20-minutes are practices worth replicating in other services.

## 10. Sign-off

- Eng Lead: M. Patel -- approved
- SRE Lead: N. Park -- approved
- PM Facilitator: A. Ravi -- approved
- VP Engineering: K. Vance -- approved
- CFO: J. Tran -- approved (financial impact noted)

Post-mortem distributed to: all engineering, exec team, board (summary only).

## Appendix: the Allspaw test pass

Asked the on-call SRE (after first draft): "Does this document represent your experience fairly?" Response: "Yes, except line in section 6 originally read 'on-call should have called for help sooner' -- changed to 'on-call had not shadowed a payments incident' to make the system condition explicit."

Final draft asks the system-level question, not the human-level question. Test passed.
````

## Why this works

- Section 5 (what went well) is detailed and comes before section 6 (what went wrong) -- anchoring the document in learning, not blame avoidance.
- Names appear only in the authors line; the narrative uses role labels ("on-call SRE", "Eng Lead") to avoid the personalization that triggers defensiveness.
- The 5 Whys converges on two systemic conditions (no canary, no pool-utilization signal), and the causal tree adds three more in parallel -- avoiding the "single root cause" trap.
- Every action item has an owner, a due date, a tracking ID, and a category (prevent / detect / mitigate / respond / process) -- so the post-mortem becomes execution.
- The Allspaw test was actually applied (and noted in the appendix) -- the document earned its blameless framing rather than asserting it.

## What's next

- Pair with [../../discovery/pre-mortem/](../../discovery/pre-mortem/) -- the conditions identified here become risks in the next high-stakes deploy.
- Use [../launch-playbook/](../launch-playbook/) for the next payments deploy; the canary stage and runbook updates become launch-readiness gates.
- Use [../status-update-generator/](../status-update-generator/) to surface action-item progress weekly until all are closed.
- Use [../dependency-map/](../dependency-map/) for AI-7 (graceful-degradation queue) if it touches multiple services.
- Track recurring runbook-gap pattern in next quarter's review with [../../scrum-master/](../../scrum-master/).
