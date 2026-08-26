# Stakeholder Mapping — Anti-Patterns + Fixes

## A1 — No map; trust the org chart
**Symptom:** "We just engage who we're supposed to."

**Fix:** Org chart shows hierarchy. Stakeholder map shows actual power +
interest. Cross-functional initiatives need explicit stakeholder mapping.

## A2 — Map exists; engagement plan doesn't
**Symptom:** Map drawn at kickoff; nobody refers to it again.

**Fix:** Map + engagement plan per quadrant + named cadence. Maintain.

## A3 — Ignoring blockers
**Symptom:** "Just don't tell them" or "They'll come around."

**Fix:** Blockers don't go away. Explicit conversion plan:
- Discover real objection
- Find evidence
- Find messenger
- Time the move

## A4 — Sleeping authority surprise
**Symptom:** HP/LI stakeholder absent during planning; emerges to veto at announcement.

**Fix:** Pre-brief HP/LI before any moment they could derail. Monthly
cadence; 5-min ask. Make engagement low-friction.

## A5 — Power = hierarchy
**Symptom:** Only org-chart hierarchy considered. Compliance, legal, security treated as advisory.

**Fix:** Veto power = power. CISO who blocks contract = HP regardless of org chart.

## A6 — Solo map
**Symptom:** PM builds stakeholder map alone.

**Fix:** Map with someone politically savvy (chief of staff, longtime
engineer, head of CS). Solo maps miss power dynamics.

## A7 — Static map
**Symptom:** Map from kickoff used 6 months later.

**Fix:** Refresh per quarter or major phase. Re-org, exec hire, pivot =
immediate refresh.

## A8 — Treating advocates as automatic supporters
**Symptom:** Champions assumed; never engaged.

**Fix:** Champions still need:
- Information to share
- Talking points
- Ammunition for their advocacy

Without these, champions go silent.

## A9 — Conflating power and influence
**Symptom:** CEO listed as highest power; no engagement plan because "we don't bother CEO".

**Fix:** If CEO has high power AND interest in initiative, engagement
plan needed. Failing to engage CEO when they care = surprise veto.

## A10 — Map without DACI
**Symptom:** Stakeholders listed; decision rights unclear.

**Fix:** Per major decision: who Decides? who Advises? who is Informed?
Map + DACI = complete.

## Worked example — enterprise deal stakeholder map

### Deal context
- Acme is selling $500K SaaS deal to Customer-X
- Customer-X has 12-person buying committee
- 6-month sales cycle expected

### Stakeholder map

| Stakeholder | Role | Power | Interest | Support | Engagement |
|-------------|------|-------|----------|---------|-------------|
| Mary, VP IT | Economic buyer | 5 | 5 | Champion | Weekly 1:1, exec sponsor pairing |
| John, CIO | Final approver | 5 | 3 | Neutral | Monthly brief, pre-brief major moments |
| Lisa, CISO | Veto power (security) | 4 | 4 | Skeptic | Address security concerns explicitly; deliver SOC 2 + pen test reports |
| Mike, IT Director | Technical buyer | 4 | 5 | Champion | Weekly tech review; co-design integration |
| Tom, IT Manager | User community lead | 2 | 5 | Supporter | Provide demo access; collect testimonials |
| Sarah, Procurement | Process owner | 4 | 2 | Neutral | Engage at right phase; have legal-friendly contracts ready |
| Janet, GC | Veto power (legal) | 4 | 2 | Neutral | Standard MSA + DPA; respond to redlines fast |
| Bob, Network Lead | Technical implementer | 2 | 3 | Neutral | Include in technical scoping calls |
| Carol, Helpdesk Lead | User impact | 2 | 4 | Skeptic | Address support model concerns; pilot with willing team |
| Dave, Finance | Budget approver | 3 | 3 | Neutral | ROI model; phased payment terms |
| Eve, Compliance | Veto power | 3 | 3 | Neutral | Compliance docs ready; map to their framework |
| Frank, Operations Lead | Adjacent impact | 1 | 1 | Neutral | Monitor; quarterly inclusion |

### Critical insights from map

1. **Mary is the champion + economic buyer** — invest heavily; don't lose her
2. **Lisa (CISO) is the riskiest skeptic** — her objection could kill deal; address early
3. **John (CIO) is HP/LI** — pre-brief before any major moment to prevent surprise veto
4. **3 veto holders** (Lisa, Janet, Eve) — all need explicit conversion
5. **Carol (skeptic, but LP)** — could rally helpdesk team against; address pilot offer

### Engagement plan

| Stakeholder | Frequency | Owner | Format | Goal |
|-------------|-----------|-------|--------|------|
| Mary | Weekly | AE | 1:1 + sponsor pairing | Maintain Champion |
| John | Monthly | AE + CRO | Pre-brief | Maintain Satisfied; prevent veto |
| Lisa | Bi-weekly | SE + Security partner | Tech + risk review | Convert Skeptic → Neutral+ |
| Mike | Weekly | SE | Tech review | Maintain Champion |
| Lisa, Janet, Eve | Joint kickoff | AE + Legal | Compliance review | Convert all 3 vetoes |

### Blocker conversion plan: Lisa (CISO)

- **Stated objection:** "We need SOC 2 Type 2 + pen test + DPA + data residency"
- **Actual concern (probed):** Bad experience with prior vendor's breach
- **Evidence to address:**
  - SOC 2 Type 2 report (provide)
  - Recent pen test summary (provide)
  - Incident response runbook (provide)
  - 3 reference customers who completed her security review
- **Messenger:** Acme CISO calls Lisa direct (peer-to-peer)
- **Timing:** Before any pricing discussion; security clears the path

Initiative likely to succeed = explicit map + engagement + blocker plan
+ regular refresh.

## Checklist

Before declaring a stakeholder map workable:

- [ ] All stakeholders listed (20+ for major initiative)
- [ ] Power + Interest + Support rated per stakeholder
- [ ] Power dimensions beyond hierarchy considered
- [ ] Blockers have conversion plans
- [ ] HP/LI stakeholders have light-engagement plan
- [ ] Champions have ammunition + tasks
- [ ] DACI applied to major decisions
- [ ] Engagement cadence + owner per quadrant
- [ ] Refresh date scheduled
- [ ] Map built with someone politically savvy (not solo)
