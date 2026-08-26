# Approval Thresholds and Routing

Reference for designing the approval-threshold matrix, regional variants, escalation paths, and routing automation patterns. The matrix is the operational backbone of the deal-desk function.

---

## Matrix design principles

A good approval matrix balances **speed** (fewer approvers = faster) against **risk control** (more approvers = more accountability). The right answer depends on company stage, ACV distribution, and risk tolerance.

### Five design principles

1. **Default delegation.** Push decision authority as low as possible. CRO shouldn't approve every $50k deal.
2. **Stack the highest needed.** When multiple non-standard items apply, the highest-approval-level item wins (not all items needing approval; just the top one).
3. **Separate financial and legal approvals.** Financial concessions go through CRO/CFO; legal concessions go through GC. Independently.
4. **Single-threaded ownership.** Each approval level has ONE primary approver + ONE named back-up. No "anyone on the leadership team can approve."
5. **Sunset thresholds.** Thresholds set 18 months ago at startup stage are wrong now. Quarterly review.

---

## Standard approval matrix

This is a starting template. Customize for your ACV distribution and authority preferences.

| Deal characteristic | Rep | Sales Mgr | Director | VP Sales | CRO | CFO | CEO |
|---------------------|-----|-----------|----------|----------|-----|-----|-----|
| **Discount %** | | | | | | | |
| 0-10% | ✓ | | | | | | |
| 10-20% | | ✓ | | | | | |
| 20-30% | | | ✓ | | | | |
| 30-40% | | | | ✓ | | | |
| 40-50% | | | | | ✓ | | |
| > 50% | | | | | | | ✓ |
| **ACV size** | | | | | | | |
| < $100k | ✓ | | | | | | |
| $100k-$250k | | ✓ | | | | | |
| $250k-$1M | | | ✓ | | | | |
| $1M-$5M | | | | ✓ | | | |
| > $5M | | | | | | | ✓ |
| **Contract length** | | | | | | | |
| 12 months (standard) | ✓ | | | | | | |
| 24 months | | ✓ | | | | | |
| 36 months | | | ✓ | | | | |
| > 36 months | | | | ✓ | | | |
| **Payment terms** | | | | | | | |
| Net 30 (standard) | ✓ | | | | | | |
| Net 45-60 | | ✓ | | | | | |
| Net 90+ | | | | | | ✓ | |
| Custom milestone-based | | | | | | ✓ | |
| **Ramp deals** | | | | | | | |
| Ramp ≤ 3 months | | ✓ | | | | | |
| Ramp 3-12 months | | | ✓ | | | | |
| Ramp > 12 months | | | | ✓ | | | |
| **Legal / commercial terms** | | | | | | | |
| Standard MSA | ✓ | | | | | | |
| Pre-approved MSA modifications | | | | | (Legal must concur) | | |
| Custom MSA language | | | | | (Legal must approve) | | |
| Liability cap > 1x annual fees | | | | | | (Legal + CFO) | |
| Customer-favorable termination | | | | (Legal concur) | | | |
| MFN clause | | | | | | ✓ (+Legal) | |
| Custom IP / source code escrow | | | | | | | (CTO + Legal + CEO) |
| Acceptance criteria / payment-on-acceptance | | | | | | ✓ | |
| Customer audit rights | | | | | (Legal concur) | | |
| **SLA / operational** | | | | | | | |
| Standard SLA | ✓ | | | | | | |
| Enhanced SLA tier | | ✓ (+CS) | | | | | |
| Custom SLA with penalties | | | | (CS + Eng concur) | | | |
| Dedicated infrastructure | | | | | (CTO concur) | | |
| Custom security commitments | | | | | (CISO concur) | | |
| **Strategic** | | | | | | | |
| First deal with strategic logo | | ✓ | | | | | |
| Public reference / case study commitment | | ✓ (+Marketing concur) | | | | | |
| Whitelabel / OEM rights | | | | | | | (CEO + Legal) |
| Multi-product / cross-BU bundle | | (each BU lead approves separately) | | | | | |
| **Channel / partner** | | | | | | | |
| Standard partner discount | ✓ | | | | | | |
| Custom partner discount | | ✓ | | | | | |
| Co-sell registration | | (Channel Mgr) | | | | | |

---

## Stacking rule (worked example)

A deal:
- $1.2M ACV
- 35% discount
- 36-month contract
- Custom SLA (99.95% with credits)
- Customer reseller involvement

Approvers per item:
- ACV $1.2M → VP Sales
- 35% discount → VP Sales
- 36 months → Director (already covered by VP Sales)
- Custom SLA → VP Sales + CS + Eng concur
- Reseller → Channel Manager

Stacked approvers: **VP Sales + CS + Eng + Channel Manager** (all in parallel; whoever signs last sets timestamp).

Note: stacking isn't additive (you don't need Sales Manager + Director + VP Sales — just VP Sales, the highest needed). But cross-functional concurs (Legal, CS, Eng, CISO, etc.) are additive — they each need to sign for the specific concern.

---

## Regional variants

International deal desks need regional context:

### Geography-specific approvers

| Region | Additional approver(s) |
|--------|------------------------|
| EU | Regional GC for GDPR-related custom terms; DPO for data residency |
| UK | Regional GC for UK-specific contract terms |
| Germany | Regional GC for German law specifics (e.g., warranty terms) |
| APAC | Regional CFO for foreign exchange risk on long-term contracts |
| Latin America | Regional CFO for FX + payment terms |
| Public sector / Government | Public Sector Lead (separate from commercial) |
| Federal (US) | Contracts Lead with FAR/DFARS expertise |

### Currency and FX

Multi-year contracts in non-USD have FX exposure. Either:
- Bake FX into pricing (Indians and Europeans pay in local currency, you assume the FX risk)
- Add FX clause (price re-baseline annually or quarterly per FX rate)
- Require USD-denominated contracts (customer assumes FX risk; harder sell)

Whichever you pick, deal desk enforces consistency.

### Time-zone awareness

If deal desk is in one region, approvers in others, SLA calculations must account for overlap windows. Helpful patterns:
- Regional deal desks for major regions
- "Follow-the-sun" model with explicit handoff at end-of-shift
- Async approval mechanism (no real-time meeting needed)

---

## Escalation paths

When the standard matrix doesn't cleanly apply or the approver is unavailable, escalation kicks in.

### Standard escalation rules

1. **Primary approver unavailable** (PTO, sick): named back-up approves. Approval matrix lists primary + back-up for every role.
2. **Disagreement between approvers**: escalate to common manager. Document the disagreement + final decision.
3. **Above the matrix**: deals that exceed all standard categories go to the highest approver (CEO or Board), with full deal-desk recommendation.
4. **Time-critical with no approver available**: Deal Desk Lead has temporary authority to approve up to one tier above the standard threshold, with documented reasoning + sponsor notification post-fact.

### Escalation anti-patterns

- **Escalate everything to the CEO**: makes the CEO the bottleneck. Force decisions at the appropriate level.
- **Never escalate, always say no**: protects the function but starves the business. Some deals need exec judgment.
- **Email approvals**: untraceable. Always use formal CRM-recorded approvals.
- **Verbal approvals**: same problem; document.

---

## Routing automation

Manual routing scales poorly. Automation patterns:

### Pattern 1: Static rule engine

Per deal: examine fields (discount %, ACV, terms), look up matrix, emit list of required approvers, send approval requests.

```python
def required_approvers(deal):
    approvers = set()
    # Discount tier
    if deal.discount_pct > 50: approvers.add("CEO")
    elif deal.discount_pct > 40: approvers.add("CRO")
    elif deal.discount_pct > 30: approvers.add("VP Sales")
    elif deal.discount_pct > 20: approvers.add("Director")
    elif deal.discount_pct > 10: approvers.add("Sales Manager")
    # ACV tier
    if deal.acv > 5_000_000: approvers.add("CEO")
    elif deal.acv > 1_000_000: approvers.add("VP Sales")
    elif deal.acv > 250_000: approvers.add("Director")
    elif deal.acv > 100_000: approvers.add("Sales Manager")
    # Legal flags
    if deal.has_custom_legal: approvers.add("General Counsel")
    if deal.liability_cap_multiplier > 1: approvers.add("CFO")
    # ... etc.
    return approvers
```

`scripts/discount_authority_router.py` implements this pattern.

### Pattern 2: Serial vs parallel approval

- **Serial**: First approver decides, then next, then next. Slow but each approver has full context (sees prior approvals/conditions).
- **Parallel**: All approvers see request simultaneously. Faster but approvers may approve without seeing others' concerns.

Hybrid is common: technical/legal/security in parallel; financial executives in serial.

### Pattern 3: Quorum / committee approval

For very large or risky deals, route to a **Deal Review Committee** (CRO + CFO + GC + CEO meeting weekly).
- Lower per-deal overhead than getting each exec individually
- Higher latency (waits for next committee meeting)
- Better cross-functional discussion

Use for deals > $5M, deals setting precedent, deals in new verticals.

### Pattern 4: Reminders + auto-escalation

When SLA timer fires:
- 50% of SLA: courtesy reminder to approver
- 75%: escalation notice to approver's manager
- 100%: auto-escalate to back-up approver
- Beyond: Deal Desk Lead intervenes

Keep humans in the loop — never auto-approve.

---

## Matrix quarterly review

Every quarter, examine:

1. **Approval rate by tier** — if 95%+ of discount-30% deals approved, threshold too low. Move to 35%.
2. **Win rate by discount band** — if 30% discounts win at same rate as 20% discounts, you're giving away margin for no win-rate lift.
3. **SLA performance by approver** — bottleneck approvers (CFO always last) signal need to delegate or restructure.
4. **Approval distribution** — if VP Sales does 80% of approvals and CRO does 5%, threshold misaligned. Either delegate more (raise threshold) or rebalance.
5. **Discount drift** — average discount % over quarters should be stable or shrinking. Increasing trend = pricing power eroding.
6. **Outlier audit** — deals with discount > 2 stdev of mean for their ACV bracket; review qualitatively.

Document the changes; communicate to sales; update training.

---

## Approver SLA expectations

The matrix only works if approvers actually approve within SLA.

### Setting approver expectations

- Each approver knows their typical decision count per week
- Each approver has named back-up; back-up auto-routes after 4h non-response
- Approvers see deal-desk dashboard with their queue + aging
- Approvers held accountable to SLA in their performance review

### When approvers consistently miss SLA

- Reassess threshold: if VP Sales is overwhelmed at $250k threshold, raise to $500k
- Add another approver at that tier: parallel co-approver instead of single
- Move to async-friendly format: written context in CRM record instead of meeting required

---

## Special cases

### Renewals

Renewal logic is different from new business:
- Standard renewal at published renewal terms: no deal desk
- Renewal with > 20% expansion: deal desk reviews (could be standard new-product approval)
- Renewal with > 10% contraction: deal desk reviews (could be churn risk; CS-led)
- Renewal with discount > standard: deal desk reviews; tougher bar than new business (renewal price is reference point)

### Multi-year deals

Multi-year deals raise specific concerns:
- Discount on year-1 ACV vs total contract value
- Whether discount is locked in or escalators apply
- Whether customer can terminate without penalty
- Whether features promised in years 2-3 are guaranteed

Approval matrix should treat multi-year deals as more sensitive than equivalent-ACV single-year deals.

### Partner / reseller deals

Partner-mediated deals route through:
- Channel Manager (validates partner status, registration)
- Deal Desk (validates terms)
- Possibly additional approvers if margin to partner is non-standard

See [channel-economics.md](../../channel-economics/SKILL.md) for partner-economics patterns.

### Strategic / first-of-kind deals

Some deals defy the matrix entirely:
- First deal in a new vertical
- First deal with a particular tech stack
- First contract using a new product
- Deal with a customer who will be a major reference

These often warrant a custom approval flow: deal desk + leadership offsite + Board awareness. Don't try to force them into the standard matrix.

---

## Cheat sheet

| Question | Answer |
|----------|--------|
| Who approves a 25% discount on a $500k deal? | Director (discount) + Director (ACV) → single Director sign-off |
| Who approves a 45% discount with custom MSA on a $200k deal? | CRO (discount) + GC (custom MSA) |
| What if the approver is on vacation? | Named back-up approves; their authority equivalent to primary |
| What if the deal is $10M? | CEO + Board awareness; deal desk recommends; formal committee approval |
| What if rep needs decision in 2 hours? | Expedite request to Deal Desk Lead; granted only with valid urgency (not just rep panic) |
| What if customer threatens to walk if we don't drop 10% more? | Re-route to higher approver; document customer leverage |
| What if a competitor just discounted us out of the deal? | Same as above; document competitive context in packet |
| What if exec approves outside the matrix (verbally)? | Deal Desk Lead must document + add to CRM; surface to sponsors at quarterly review |
| What if we say no and the rep escalates above us? | Escalation is fine; deal-desk recommendation is documented; if exec overrides, exec owns the outcome |
