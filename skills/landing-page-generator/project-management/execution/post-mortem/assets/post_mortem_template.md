# Post-Mortem: [Short Incident Title]

| Field | Value |
|---|---|
| **Incident ID** | INC-YYYY-NNNN |
| **Date of incident** | YYYY-MM-DD |
| **Date of post-mortem** | YYYY-MM-DD |
| **Severity** | Sev 0 / Sev 1 / Sev 2 / Sev 3 / Near Miss |
| **Duration** | HH:MM (from detection to mitigation) |
| **Status** | Draft / In Review / Final |
| **Author** | (role + name) |
| **Reviewers** | (incident commander, owning team lead, on-call) |
| **Services affected** | (list, e.g. payments-api, billing-worker) |
| **Failure class tags** | (e.g. capacity, deploy-regression, dependency-failure) |

---

## 1. Summary

> 3-5 sentences. What happened? Who was affected? How was it resolved? What is the durable fix? A reader who reads only this section should know the headline.

[Write summary here]

---

## 2. Impact

| Dimension | Detail |
|---|---|
| **Customers affected** | (count, segments) |
| **Revenue impact** | (estimated $) |
| **SLO error budget burned** | (% of monthly budget) |
| **Internal teams blocked** | (list) |
| **Public communication** | (status page / customer email / silent?) |
| **Compliance / regulatory** | (any reportable breach?) |

---

## 3. Timeline

All times in UTC. Mark decision points with **[DECISION]**.

| Time (UTC) | Event |
|---|---|
| HH:MM | (trigger event — what changed in the system) |
| HH:MM | (first signal — what the monitoring saw) |
| HH:MM | (detection — when a human knew) |
| HH:MM | (escalation) |
| HH:MM | **[DECISION]** (e.g. "decided to roll back rather than roll forward") |
| HH:MM | (mitigation applied) |
| HH:MM | (customer impact ended) |
| HH:MM | (full resolution) |
| HH:MM | (incident closed) |

**Total customer-impact duration:** HH:MM

---

## 4. What Went Well

> Minimum 3 items. Use `assets/what_went_well_prompts.md` if stuck.

- ...
- ...
- ...

---

## 5. What Went Wrong

> Phrased as system properties, not human failures. Search this section for "should", "could have", "if only" before publishing.

- ...
- ...
- ...

---

## 6. Contributing Factors

> Conditions that, in combination, produced the outcome. Distinguished from a single "root cause".

| # | Contributing factor | Category (prevent / detect / mitigate / respond / process) |
|---|---|---|
| 1 | ... | ... |
| 2 | ... | ... |
| 3 | ... | ... |

---

## 7. Root Cause Analysis

**Method used:** 5 Whys / Causal Tree / Hybrid

### Analysis

> If 5 Whys, write the chain. If Causal Tree, paste the tree. See `references/5-whys-vs-causal-tree.md` for guidance.

```
[Tree or chain here]
```

### Statement of cause

> Avoid declaring a single root cause. Phrase as the set of contributing factors that aligned.

The incident was caused by the alignment of:
1. ...
2. ...
3. ...

---

## 8. Action Items

| # | Action | Owner | Due | Tracker ID | Category | Status |
|---|---|---|---|---|---|---|
| 1 | (specific, testable change) | (one person) | YYYY-MM-DD | (e.g. ENG-1234) | prevent / detect / mitigate / respond / process | Open |
| 2 | ... | ... | ... | ... | ... | Open |
| 3 | ... | ... | ... | ... | ... | Open |

**Action-item review cadence:** weekly engineering ops review.

**Completion target:** 70% by 30 days post-publication, 90% by 90 days.

---

## 9. Lessons Learned

> Broader patterns that go beyond this specific incident. These often feed engineering standards, runbooks, or hiring.

- ...
- ...

---

## 10. Appendix

### Linked materials

- Incident chat transcript: [link]
- Monitoring dashboards: [links]
- Related post-mortems: [links to prior incidents in this class]
- Relevant runbooks: [links]
- PR / deploy that triggered the incident: [link]

### Allspaw test

> "Would I send this document to the engineer who took the action that triggered the incident, and would they recognize their experience as fairly represented?"

- [ ] Yes — proceed to publish.
- [ ] No — return to draft and rewrite.

### Sign-off

| Role | Name | Signed |
|---|---|---|
| Author | | YYYY-MM-DD |
| Incident commander | | YYYY-MM-DD |
| Owning team lead | | YYYY-MM-DD |

---

## Distribution

- [ ] Posted to team wiki / Confluence / Notion
- [ ] Linked from incident tracker
- [ ] Shared in #engineering channel
- [ ] Summary shared with executives (Sev 0/1 only)
- [ ] Public-facing version on status page (if customer-impacting)
- [ ] Tagged with services and failure class for searchability
