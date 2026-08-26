# SOC 2 Evidence Collection Sprint Plan

Week-by-week plans for 4 / 8 / 12-week audit-prep sprints. Each plan includes daily-level milestones, owner assignments, and decision gates.

---

## 4-week sprint (Type I, mostly ready)

For organizations with strong existing controls; this sprint is mostly evidence collection + walkthroughs.

### Week 1: Inventory + scoping

**Day 1**:
- Assign audit owner (single point of accountability)
- Confirm Trust Services Criteria scope (always Security; plus chosen others)
- Auditor kickoff call scheduled
- Pull existing evidence into shared workspace

**Day 2-3**:
- Run `scripts/soc2_readiness_score.py` against current state
- Run `scripts/evidence_gap_finder.py`
- Per-criterion gap list created

**Day 4**:
- Gap-closure priorities set
- Per-criterion owners assigned
- Auditor kickoff call held; confirm requested evidence list

**Day 5**:
- Daily standup cadence started
- Weekly checkpoint scheduled (audit owner + leadership)

### Week 2: Gap closure

**Day 1-3**:
- Policy updates per gap list (information security policy, change management, incident response, etc.)
- Policy approvals (CRO / CTO / CFO / GC per content)

**Day 4-5**:
- Technical fixes (MFA universal, logging coverage, encryption verification)
- Process gaps (vendor reviews, access reviews, training completion)

### Week 3: Evidence finalization

**Day 1-3**:
- Evidence packets compiled per criterion
- Walkthrough scripts prepared per control owner
- Auditor Q&A document (anticipated questions)

**Day 4**:
- Pre-audit checkpoint with auditor (informal review of evidence)
- Auditor flags any major missing items

**Day 5**:
- Final gap closures from checkpoint
- All walkthroughs scheduled

### Week 4: Audit week

**Day 1**:
- Auditor onsite kickoff
- Initial walkthroughs (high-level)

**Day 2-3**:
- Per-control walkthroughs with owners
- Sample testing (auditor requests evidence)

**Day 4**:
- Findings preliminary discussion
- Management response drafting begins

**Day 5**:
- Closing meeting
- Findings + management response finalized
- Audit report timeline confirmed

---

## 8-week sprint (Type I with gaps)

For organizations with gaps requiring time to remediate.

### Weeks 1-2: Inventory + scoping + gap identification

(Same as 4-week W1, expanded to 2 weeks for deeper gap-finding)

- Detailed gap analysis per TSC
- Per-gap remediation plan with owner + due date
- Risk-rank gaps (severity × likelihood of audit finding)
- Auditor kickoff includes gap acknowledgment + remediation timeline

### Weeks 3-5: Gap closure (parallel tracks)

**Track A: Policy / process**
- Policy gaps → drafted, reviewed, approved
- Process gaps → procedures documented, training conducted
- Vendor due diligence backlog cleared

**Track B: Technical controls**
- Logging coverage extended
- MFA / SSO universal
- Encryption verified
- Backup / restore tested

**Track C: Evidence backfill**
- Past-period evidence collected (access reviews, change records, incident reports)
- If gaps in past period exist, document remediations + start fresh evidence trail

### Weeks 6-7: Evidence finalization + walkthroughs

- Same as 4-week W3
- Plus: pre-audit checkpoint with auditor 2 weeks early
- Address auditor flagged items

### Week 8: Audit week

- Same as 4-week W4

---

## 12-week sprint (Type II observation prep)

Type II requires controls operating over observation period (typically 3-12 months; minimum 6 months for first Type II). This sprint prepares the period leading up to and including initial observation.

### Weeks 1-2: Inventory + scoping + gap identification

(Same as 8-week W1-2)

### Weeks 3-4: Gap closure

- Same as 8-week W3-5, condensed
- Goal: all controls in operational state before observation period begins

### Weeks 5-12: Observation period (controls operating)

**Continuous activities:**
- Evidence accumulates automatically (logs, change tickets, incident records, access reviews)
- Monthly internal audit checkpoints
- Issue / remediation tracking

**Monthly checkpoints:**
- Run `scripts/evidence_gap_finder.py` to verify evidence accumulating
- Spot-check control operations
- Address drift (controls degrading over time)

### After observation period: audit week

- Auditor reviews evidence accumulated over observation period
- Walkthroughs of each control
- Sample testing across the observation period (not just current state)

---

## Sprint roles

### Audit owner (full-time during sprint)

- Single point of accountability
- Tracks all evidence collection
- Coordinates with auditor
- Reports weekly to leadership

### Control owners (per criterion)

- One per TSC area
- Responsible for evidence for their controls
- Available for walkthroughs

### Leadership sponsor

- CRO / CISO / CTO depending on org structure
- Removes blockers
- Approves policy updates
- Available for auditor escalations

### Technical lead

- Provides infrastructure evidence (logs, configurations, etc.)
- Implements technical control gaps
- Often the security engineer or DevSecOps lead

---

## Daily standup template

```
Date: YYYY-MM-DD
Audit week countdown: <N days>

Yesterday's progress:
- <item> [completed / in progress / blocked]

Today's plan:
- <item> — owner: <name>

Blockers:
- <blocker> — escalation needed: <yes/no>

Evidence status:
- Criteria fully evidenced: <count>
- Criteria with gaps: <count>
- Total evidence items collected: <count>
```

---

## Pre-audit checkpoint with auditor

Held 1-2 weeks before audit week. Informal. Goal: surface major gaps before audit day.

**Agenda (60-90 min)**:
1. Confirm scope + criteria
2. Walk through high-level control inventory
3. Auditor reviews sample evidence per criterion
4. Identify major gaps + remediation plan
5. Confirm walkthrough schedule for audit week
6. Q&A

After the checkpoint:
- Address all flagged items
- Send updated evidence to auditor
- Confirm readiness for audit week

---

## Common sprint failure modes

| Failure | Cause | Recovery |
|---------|-------|----------|
| Sprint slips past audit date | Underestimated gap closure time | Reschedule audit; transparency with auditor |
| Evidence collected; not organized | No standard evidence template | Reorganize per audit owner's template |
| Walkthroughs fail | Control owners not prepared | Run mock walkthroughs Week 3 |
| Auditor finds gap at audit | Pre-audit checkpoint skipped | Hold checkpoint; address |
| Control was fine until audit week | Drift between assessment + audit | Daily verification of critical controls |
| Sub-service org evidence missing | Vendor unresponsive | Escalate early; have alternatives |

---

## Sprint metrics

Track weekly:
- % of criteria fully evidenced
- % of gaps closed
- Number of open findings (target: 0 by audit week)
- Auditor responsiveness (delays kill sprint timing)

---

## Post-audit cleanup

After audit completes:
- Findings register: each finding tracked to remediation
- Management response: documented per finding
- Evidence archive: complete audit packet stored for 7 years
- Continuous evidence collection: automated where possible (especially for Type II)
- Schedule next year's audit + start observation period planning

---

## Cheat sheet

| Question | Answer |
|----------|--------|
| When should I start? | 4-12 weeks before audit, depending on readiness |
| What's the first action? | Assign single audit owner |
| Type I or Type II first? | Type I unless you've operated controls 6+ months |
| Audit owner needs how much time? | Half-time during sprint; full-time during audit week |
| What if we slip? | Reschedule the audit; transparency with auditor; better than failing |
| What if auditor finds new gap day-of-audit? | Document remediation plan; included in management response |
| Mock walkthrough timing? | Week 3 of sprint at latest |
| Pre-audit checkpoint timing? | 1-2 weeks before audit |
