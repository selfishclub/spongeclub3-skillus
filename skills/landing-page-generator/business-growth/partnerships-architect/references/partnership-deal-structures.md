# Partnership Deal Structures

Reference for negotiating and structuring specific partnership deals: term sheets, key business terms, deal patterns by type, negotiation guides, common contentious clauses.

---

## What deals to structure (and what to keep simple)

| Partnership | Standard agreement / can use template | Custom-negotiated |
|-------------|---------------------------------------|-------------------|
| Standard reseller | Yes — standard partner agreement | No (unless tier above gold) |
| Affiliate / referral | Yes — standard affiliate terms | No |
| Marketplace listing | Yes — marketplace operator's terms | No |
| Tech / integration partner | Mostly template; light customization | Maybe for strategic |
| VAR / specialized reseller | Some template, some customization | For top-tier partners |
| OEM / Embedded | No template works; full custom | Always |
| Strategic Alliance | No template; full custom | Always |
| JV / Strategic Investment | No template; legal-heavy | Always |

Reserve custom negotiation for relationships > $1M annual value or > 3-year commitment.

---

## Term sheet — the foundational document

Before writing a contract, write a term sheet. 1-3 pages capturing key business terms. Both parties sign as non-binding intent → de-risks legal-heavy contract drafting.

### Standard term sheet sections

```
1. Parties
2. Purpose of partnership
3. Term (length, renewal, termination)
4. Scope (what's in / out)
5. Exclusivity (if any)
6. Compensation / economics
7. Mutual commitments (resources, deliverables)
8. Intellectual property (ownership, license, joint inventions)
9. Confidentiality
10. Governance (steering committee, escalation)
11. Termination terms + transition
12. Conditions to definitive agreement (legal review, board approval, due diligence)
```

---

## Term-by-term negotiation guide

### Term length

| Length | When |
|--------|------|
| 1 year | Tactical / proof-of-concept; high uncertainty |
| 2-3 years | Standard channel / co-sell |
| 3-5 years | Strategic alliance |
| 5-7 years | OEM (substantial mutual investment justifies longer) |
| Open-ended | Strategic alliance with annual review (rare) |

**Negotiation:** Partner pushes for longer (locks you in); you push for shorter (preserves flexibility). Middle ground: shorter initial term with renewal options.

### Renewal terms

| Pattern | Trade-offs |
|---------|------------|
| Auto-renew + 90-day notice | Convenient; risk of stale partnership |
| Mutual opt-in at renewal | More work; explicit re-commitment |
| Performance-gated renewal | Only renews if metrics hit |

**Recommendation**: Performance-gated renewal for material partnerships; mutual opt-in for strategic alliances.

### Exclusivity

| Type | When acceptable |
|------|-----------------|
| Full exclusive | Almost never; only for strategic / paid exclusivity |
| Category exclusive (e.g., "only partner in CRM space") | Rarely; requires partner to commit substantial resources |
| Geographic exclusive (e.g., "only partner in Japan") | Common; requires partner to demonstrate market commitment |
| Customer-segment exclusive (e.g., "only partner for enterprise > 5000 employees") | Common; segment-specific commitment |
| First right of refusal | More flexible than exclusive; preserves your options |

**Anti-pattern**: open-ended exclusivity without performance gates. Lose flexibility for nothing in return.

### Compensation / economics

#### Reseller / VAR

- Discount % per tier
- Rebate structure (back-end)
- MDF allocation
- Deal-reg protection

#### OEM

- Royalty rate (% of partner revenue) OR per-instance fee OR fixed annual
- Minimum commitment (partner commits to minimum royalty regardless of actual)
- Maximum cap (your protection: partner's success doesn't bankrupt them)
- Reporting + audit rights

#### Strategic alliance

- Shared budget (e.g., $X each per year for joint marketing)
- Resource commitments (e.g., 2 FTEs each)
- No direct revenue exchange but contractual commitments

#### JV / Investment

- Ownership / equity stakes
- Founders' contributions
- Capital calls
- Distribution waterfall

### Intellectual property

| Element | Standard |
|---------|----------|
| Pre-existing IP | Each party retains all rights |
| Jointly developed IP | Usually each party gets full license to use; new patent owned jointly or by primary developer |
| Improvements to one party's product | Owned by that party |
| Trademark license | Limited license to use partner logos in approved ways |

**Negotiation pain points:**
- "Joint inventions" disputes: who owns what built collaboratively
- Background IP: confirming neither party's existing IP gets accidentally transferred
- Subsequent partner deals: can partner share what they learned with your competitors?

### Confidentiality

Standard mutual NDA terms:
- Definition of confidential information
- Permitted disclosures (employees, advisors, regulatory)
- Duration (typically 3-5 years post-termination)
- Carve-outs (public info, independently developed, prior known)

### Governance

For strategic / OEM partnerships:
- **Steering committee**: senior execs from each side, meet quarterly
- **Operational committee**: day-to-day owners, meet monthly
- **Escalation path**: when committee disagrees → who decides

### Termination

#### For convenience

- Length of notice (30/60/90/180 days, sometimes 12-24 months for OEM)
- Effect on in-flight work (committed deals honored, in-progress integrations completed)

#### For cause

- Material breach + cure period (typically 30 days to cure)
- Bankruptcy / insolvency
- Change of control (acquisition by competitor)

#### Transition

- Customer transition rights (can vendor serve partner-served customers post-termination?)
- License continuity (can partner continue using IP post-termination?)
- Knowledge transfer obligations
- Wind-down period

**Most contentious clauses:** change-of-control termination (especially for OEM), customer transition rights, post-termination license.

---

## Deal patterns by type

### Pattern A: Standard reseller

```markdown
Term Sheet: [Partner Name] — Reseller Agreement

1. Parties: [Vendor] and [Partner]
2. Purpose: Partner authorized to resell Vendor's products in [territory]
3. Term: 2 years, auto-renew unless 90-day notice
4. Scope: All Vendor products; territory = [geography]
5. Exclusivity: Non-exclusive
6. Compensation:
   - Standard tier: 15% discount; auto-promote to Silver at $100k/yr; Gold at $500k/yr
   - Quarterly back-end rebate of 5% above Gold threshold
   - MDF allocation: 1% of partner revenue, approved quarterly
7. Commitments:
   - Partner: 3 certified sales reps within 90 days; quarterly business review attendance
   - Vendor: Channel manager assigned; partner portal access; standard MDF program
8. IP: Standard
9. Confidentiality: Standard mutual NDA, 3 years post-termination
10. Governance: Quarterly business review with regional VP
11. Termination: For convenience with 90-day notice; for cause with 30-day cure period
12. Conditions: Partner signs Vendor MSA; certification of 3 reps within 90 days
```

### Pattern B: OEM agreement

```markdown
Term Sheet: [Partner Name] — OEM Agreement

1. Parties: [Vendor] and [Partner]
2. Purpose: Vendor's [product] embedded in Partner's [product] under Partner's brand
3. Term: 5 years; renewable
4. Scope: Embedded in [Partner product line]; for [Partner's target market]
5. Exclusivity:
   - Vendor exclusive to Partner in [specific market segment]
   - Partner non-exclusive (can offer alternatives)
   - Carve-out: Vendor can sell directly outside [market segment]
6. Compensation:
   - Per-instance royalty: $X per Partner customer per year
   - Minimum commitment: Partner pays for minimum 1,000 customers regardless of actual
   - Maximum cap: $Y annual; beyond which terms re-negotiated
   - Audit rights: Annual, by mutually-agreed auditor
7. Commitments:
   - Vendor: API stability commitment; dedicated technical support tier; 99.9% SLA on embedded service
   - Partner: Quarterly customer count reporting; co-development meetings; joint roadmap input
8. IP:
   - Each party retains pre-existing IP
   - Source code escrow: Yes, with neutral escrow agent
   - Customer data: Owned by Partner; Vendor processes per Partner's instructions
9. Confidentiality: Standard mutual; 5 years post-termination
10. Governance:
    - Executive steering committee: quarterly; VP-level
    - Technical committee: monthly; engineering-level
11. Termination:
    - For convenience: 12-month notice
    - For cause: 30-day cure period
    - Change of control: Either party can terminate within 60 days of acquisition announcement
    - Transition: 18-month wind-down with continued service to existing customers
12. Conditions: Definitive agreement requires legal review (90 days); board approval both sides
```

### Pattern C: Strategic alliance

```markdown
Term Sheet: [Partner Name] — Strategic Alliance

1. Parties: [Vendor] and [Partner]
2. Purpose: Joint go-to-market in [target market]; combined positioning
3. Term: 2 years; renewable annually
4. Scope:
   - Joint thought leadership (4 pieces per year)
   - Joint events (2 major + 4 regional per year)
   - Joint customer wins (target: 10 in year 1)
   - Joint product integration (planned for Q3)
5. Exclusivity: Mutual reasonable best efforts in [target market]; not exclusive
6. Compensation:
   - No direct revenue exchange
   - Shared marketing budget: $200k/year each
   - Mutual referral commissions: 10% of first-year ACV for partner-sourced deals
7. Commitments:
   - Each party: 2 dedicated FTEs (1 strategic, 1 marketing)
   - Quarterly Joint Steering Committee: VP-level
   - Annual executive review: CEO + CMO + CRO from each side
   - Specific deliverables tracked quarterly
8. IP: Standard mutual license to use logos / brands in approved joint marketing
9. Confidentiality: Standard mutual
10. Governance:
    - Joint Steering Committee: quarterly
    - Operational sync: monthly
    - Escalation: respective Chiefs of Staff
11. Termination: 90-day notice for convenience; 30-day cure for breach
12. Conditions: Term sheet signed → definitive agreement within 60 days; joint kickoff event within 90 days
```

---

## Most contentious clauses

### Change of control (especially for OEM)

**Problem:** Partner gets acquired by your competitor. Now you're embedded in your competitor's product.

**Standard protection:** Right to terminate within 30-90 days of acquisition announcement. Survival of customer obligations.

**Negotiation:** Partner wants this only triggerable by "direct competitor" (defined narrowly). You want broader trigger.

### MFN (Most Favored Nation)

**Problem:** Partner demands you give them best-available pricing forever. Constrains your future pricing flexibility.

**Standard mitigation:** Scope tightly (same product, same volume, same term length, same geo). Disclosure-only (we tell you our other prices; you can match). Exclude pilot / launch pricing.

### Audit rights

**Problem:** Partner wants ability to audit your records. You don't want disruption / disclosure.

**Standard:** Audit allowed annually, by mutually-agreed third-party auditor, with confidentiality protections, at audit-requester's cost (unless discrepancy > 5%, then audited party pays).

### Source code escrow (OEM)

**Problem:** Partner wants source code held in escrow in case you go bankrupt.

**Standard:** Yes, with neutral escrow agent. Release triggers: bankruptcy, material breach of support obligations, sustained product failure.

### Liability cap

**Problem:** Partner wants higher liability cap. You want standard (1x annual fees).

**Standard:** Standard cap unless specifically warranted. Higher cap (2-3x annual) for OEM where partner has substantial customer-side liability. Carve-outs for IP infringement, gross negligence.

### Non-compete

**Problem:** Partner wants you to not work with their competitors. You want freedom to pursue all markets.

**Standard:** Non-compete only in defined market segment if any. Time-limited (e.g., 12 months post-termination). Geographic scope limited.

---

## Negotiation principles

### Walk-away points

Before negotiating, decide internally:
- Minimum acceptable terms (your walk-away)
- Target terms (your aim)
- Ideal terms (your opening position)

Don't reveal walk-away. Open at ideal; settle at or above target.

### Reciprocity

Every concession trades for a concession.
- Longer term ← higher discount
- Wider exclusivity ← higher commitment
- Higher liability cap ← higher revenue commitment

If you concede without getting reciprocally, you're being squeezed.

### "Standard" is negotiable

Partner says "this is standard for us." Yours might be standard for you. Standards are starting points, not endpoints.

### Time pressure

The party with more time pressure loses. Don't manufacture urgency you don't have. Use deadlines strategically.

### Bring in the right people

- Term-sheet negotiation: business leads (your VP / their VP)
- Definitive agreement: legal-led (both sides)
- Closing meeting: both sides' executive sponsors

---

## Term sheet template

```markdown
# Term Sheet: [Partnership Name]

**Date:** YYYY-MM-DD
**Parties:** [Vendor], [Partner]
**Status:** Draft / Signed (non-binding intent)

## 1. Purpose
[1-2 sentences]

## 2. Term
[Length, renewal, termination]

## 3. Scope
**In-scope:**
- ...

**Out-of-scope:**
- ...

## 4. Exclusivity
[Detailed terms]

## 5. Compensation / Economics
[Detailed terms]

## 6. Mutual Commitments
**Vendor will:**
- ...

**Partner will:**
- ...

## 7. IP
[Pre-existing, joint, license terms]

## 8. Confidentiality
[Standard mutual NDA]

## 9. Governance
[Committees, cadence]

## 10. Termination
[For convenience, for cause, transition]

## 11. Conditions to Definitive Agreement
- Legal review (target: 60 days)
- Board approval (each side)
- Due diligence: [specifics]

## 12. Non-binding
This term sheet expresses the parties' intent. Definitive
agreement(s) supersede this document and contain binding terms.

Signed:
[Vendor]: ____________
[Partner]: ____________
```

---

## Cheat sheet

| Question | Answer |
|----------|--------|
| Start with term sheet or contract? | Term sheet — saves legal time if business terms don't align |
| Exclusivity for free? | Almost never. Match exclusivity to commitment. |
| What's the OEM royalty norm? | 30-50% of partner revenue per end-customer; varies by category |
| What term length for OEM? | 3-7 years; longer = more mutual investment justified |
| Performance gates on renewal? | Yes for material partnerships; binary mutual opt-in for strategic |
| When does legal need to be involved? | Term sheet: light touch. Definitive agreement: full legal. |
| What's our walk-away on exclusivity? | Pre-decide; don't negotiate from a moving baseline |
| When do we kill a partnership? | When 12-month metrics show < 25% of plan AND no clear path forward |
