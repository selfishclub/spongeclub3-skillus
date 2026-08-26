# Channel Conflict Resolution

Reference for handling overlapping or competing channel claims: deal registration process, conflict patterns (direct-vs-partner, partner-vs-partner, marketplace-vs-direct), arbitration mechanisms, and the conflict-of-interest disclosure practices that keep partners honest.

---

## What channel conflict looks like

Common patterns:

| Pattern | Example |
|---------|---------|
| **Race conditions** | Direct rep and partner both register same account same week |
| **Surprise overlap** | Partner closes deal that direct rep was pursuing for 3 months (or vice versa) |
| **Marketplace vs direct pricing** | Customer can buy via AWS Marketplace at $X or direct at $Y |
| **Partner competing with partner** | Two resellers both pursue same enterprise account |
| **Direct deal poached** | Partner brings customer who was already negotiating direct |
| **Marketplace credit issue** | Customer buys via marketplace; direct rep gets no credit; rep refuses to support deal |
| **Renewal hijack** | Direct sells initial; partner attempts to take over renewal |
| **MFN cross-channel** | Customer got marketplace pricing; demands same direct |

Unresolved channel conflict produces:
- Sales reps refusing to work with partners ("they steal my deals")
- Partners stopping investment in your product ("we can't trust we'll close")
- Confusing customer experience ("why am I getting calls from 3 people about the same product?")
- Margin erosion ("everyone discounts to win the deal")
- Trust collapse between channel team + direct team

---

## Deal registration as primary defense

Deal registration is the standard mechanism: partners (or direct reps) "register" deals they're working; first-to-register typically gets priority.

### Standard deal-registration process

```
1. Partner identifies opportunity
2. Partner submits deal registration:
   - Customer name + key contact
   - Estimated ACV
   - Expected close date
   - Brief opportunity description ("competing with X, pilot starting Q2")
3. Vendor (you) reviews within 2-3 business days:
   - Approve: opportunity protected; partner gets right of first refusal
   - Deny: opportunity already direct OR registered by another partner OR insufficient evidence partner is actively pursuing
   - Pending: need more info
4. Approved registrations:
   - Valid for 90-180 days (specified in partner agreement)
   - Partner gets exclusive engagement on this opportunity
   - Direct sales team can't pursue without partner agreement
5. Partner closes (or doesn't) within registration window
   - Closes: standard partner discount applies; commission tracked
   - Doesn't close: registration expires; account becomes open
```

### Common deal-registration rules

| Rule | Why |
|------|-----|
| First-to-register wins (with vendor approval) | Simple, defensible, encourages partner-side urgency |
| Registration requires customer engagement evidence | Prevents "land-grab" registration of every prospect in CRM |
| Registration is account-specific, not company-wide | One subsidiary doesn't block another |
| Renewal protection: incumbent partner gets first-look on renewals | Rewards partner that won the initial; prevents pirating |
| Registration window has explicit expiry | Forces movement; releases stalled opportunities |
| Partial registration possible (one BU only) | Multi-BU customers can have multiple partners |
| Vendor reserves right to override for strategic deals | Sometimes direct must lead (regulated industries, strategic logos) |

### Anti-gaming protections

| Risk | Mitigation |
|------|-----------|
| Partner registers every prospect they know | Require evidence (recent meeting, pilot in progress, RFP submitted) |
| Partner registers, sits on deal | 90-day expiration; require activity check at 30/60 days |
| Multiple partners register same deal | Vendor adjudicates: first-registered + active engagement wins |
| Direct rep poaches registered deal | Direct cannot pursue without partner sign-off; if conflict, escalate to channel + sales VPs |
| Partner registers competitor's customer | Verify partner has actual relationship; deny if speculative |

---

## Pattern: direct-vs-partner conflict

### Scenario A: New opportunity, both pursue

- Both submit interest within days of each other
- **Resolution**: First-to-register wins **unless** other party has documented prior engagement (CRM records, prior touch points)
- **If close call**: VP Sales + VP Channel adjudicate

### Scenario B: Partner brings opportunity to direct rep

Partner says "hey, I have this account, but they want to talk to you directly."

- **Best practice**: Partner gets registered; direct rep is the technical resource; commission split or full partner credit per agreement
- **Common bad practice**: Direct rep takes over, partner gets nothing; partner stops bringing leads

### Scenario C: Customer asks for direct after partner POC

Customer worked with partner during evaluation; now wants to negotiate with you directly.

- **Resolution**: Honor partner registration; partner remains in deal until close
- **Customer relationship**: Direct overlay rep + partner rep both work the deal; commission per partner agreement
- **At renewal**: Re-evaluate based on who's been operationally engaged

### Scenario D: Direct deal in flight, partner shows up

Direct rep has been pursuing for 3 months; partner submits registration for same account.

- **Resolution**: Direct's prior engagement wins; partner registration denied (with reasoning)
- **Cushion**: Vendor may offer partner an alternative account or lead-share

---

## Pattern: partner-vs-partner conflict

### Scenario A: Two resellers, same account, both registered

- **First-to-register wins** is the default
- **Exception**: if the later-registering partner has a vertical or geographic specialization that materially benefits the customer (and earlier-registering partner lacks it), some vendors allow swap

### Scenario B: Geographic vs vertical specialist

US-region reseller and healthcare-vertical reseller both pursue a Boston healthcare company.

- **Vertical typically wins** when vertical expertise is what customer values
- **Geographic typically wins** when local presence / support is differentiator
- **Document the policy** so partners know upfront

### Scenario C: New partner pursues incumbent partner's customer

Customer has been served by Partner A for 2 years. Partner B submits registration to expand.

- **Incumbent right-of-first-refusal**: Partner A has 90 days to register the expansion themselves
- **If Partner A declines**: Partner B can proceed
- **If both want**: customer chooses; vendor doesn't pick favorites

---

## Pattern: marketplace-vs-direct conflict

### The pricing question

If list price is $100k direct and $100k on marketplace (after 3% AWS fee, you net $97k), customer chooses based on procurement preference:
- Buy direct → standard 12-month contract, your AR
- Buy via marketplace → AWS handles billing, faster procurement, counts toward AWS committed spend

If you discount direct ($85k) but not marketplace ($100k), customer who would prefer marketplace gets punished. Bad.

### Pricing-parity practice

- **Same price across direct and marketplace** (customer doesn't choose based on price; chooses based on procurement)
- **Same discount structure across channels** (if 20% off available direct, 20% off via marketplace too)
- **Direct rep gets quota credit for marketplace deals they influenced** (so rep isn't disincentivized)

### Marketplace credit attribution

When customer buys via marketplace:
- AWS Marketplace shows the sale to AWS, not to your rep
- Your rep may have done all the work (introduced, evaluated, technical-validated)
- **Need explicit credit policy**: rep gets quota credit + commission for marketplace deals where they were primary

Without this, reps actively discourage marketplace purchases — destroys the channel.

### Co-sell programs

AWS Co-Sell, Azure Co-Sell, GCP Co-Sell: these let cloud-provider sales teams jointly pursue your accounts. Substantial deal flow when done well.

- **Register accounts** in co-sell to surface to cloud sales teams
- **Joint sales motion**: cloud account team + your team
- **Credit shared**: both teams get credit
- **Customer benefit**: cloud-provider sales team accelerates procurement (already have relationship)

---

## Arbitration mechanism

When channel conflict can't be resolved at the channel-manager + direct-sales-manager level, escalation:

### Standard arbitration ladder

```
Level 1: Channel Manager + Direct Sales Manager
  - Goal: agree within 3 business days
  - Tool: deal-registration data + activity history
  
Level 2: VP Channel + VP Sales (regional)
  - When Level 1 can't agree
  - Goal: decision within 5 business days
  - Considers: precedent risk, customer-relationship impact, strategic value

Level 3: CRO
  - For high-value or strategic deals only
  - Goal: decision within 3 business days
  - Final
```

### Arbitration principles

1. **Speed matters** — long arbitration kills the deal
2. **Process visibility** — both parties see the decision + reasoning
3. **Loser-side cushion** — alternative leads, MDF, lead-share to preserve relationship
4. **Document precedent** — similar future cases reference this decision
5. **No retaliation** — partner that "loses" arbitration shouldn't suffer in other deals

---

## Conflict-of-interest disclosure

Partners often work with competing vendors. Standard disclosure:

### What partners disclose

- Other vendors in your product category they sell (annually + as new relationships form)
- Customers where competing products are being discussed
- Any equity / financial relationship with you or with competitors

### Why it matters

- You can assess partner alignment (50% loyalty isn't 100% loyalty)
- You can avoid funding partner enablement for competitors
- You can scope deal protection appropriately (partner selling X and Y → can't claim "exclusive" rep)

### Reciprocal disclosure

You disclose to partners:
- Direct sales pursuit of accounts the partner is registered on (proactively)
- Other partners in their territory or vertical
- Strategic moves that affect their business (acquisitions, product retirements)

Trust requires reciprocity.

---

## Special cases

### Renewals

Standard practice:
- Whoever sold initial deal owns renewal for 1-2 contract cycles
- After that, account can transfer if compelling reason
- Renewal compression conflict: incumbent partner asks for renewal discount they can't get → escalate to direct overlay

### Strategic / first-of-kind deals

Sometimes the deal is so strategic (named logo in target vertical, first major regional deal, transformative reference) that the standard registration process is overridden.

- **Process**: CRO can declare a deal "strategic-direct" or "strategic-partner-led" — overrides registration
- **Use sparingly**: overriding the rules undermines them; document reasoning
- **Compensate channel** for strategic-direct designations (lost opportunity for partner; offer alternative)

### Acquisitions

Customer A acquires Customer B. Customer B was a registered partner deal; Customer A is direct.

- **Resolution**: Often combined; partner retains involvement for B's existing usage; A drives expansion
- **Document** for future acquisition cases

### Subsidiaries

Customer has 20 subsidiaries. Are subsidiaries separate registrations or umbrella?

- **Default**: each subsidiary separate (large subsidiary may have own buying authority)
- **Exception**: customer requests central procurement → consolidate

---

## Operational requirements for healthy conflict management

### Tooling

| Capability | Why |
|------------|-----|
| Deal-registration portal (or CRM integration) | Partners submit; channel team reviews; partners see status |
| Activity tracking | Validates "active engagement" claims |
| Audit log | Decision trail for arbitration |
| Reporting | Quarterly conflict frequency, resolution time, win/loss tracking |

### Cadence

- **Daily**: Channel team monitors new registrations; flags potential conflicts
- **Weekly**: Channel + Direct sync on overlapping accounts
- **Monthly**: Conflict-resolution metrics review; trend analysis
- **Quarterly**: Policy review; precedent update

### Metrics

| Metric | Healthy | Warning |
|--------|---------|---------|
| Deal-registration response time | < 3 business days | > 7 days |
| Conflict resolution time | < 5 business days | > 10 days |
| % deals with conflict | < 10% | > 25% |
| Partner satisfaction with conflict resolution (NPS) | > 30 | < 0 |
| Conflicts requiring CRO escalation | < 5% | > 20% |

---

## Cheat sheet

| Situation | Action |
|-----------|--------|
| Partner registers a new deal | Approve within 3 BD if customer engagement evidence is real |
| Two partners want the same deal | First-to-register wins; exceptions for vertical/geographic specialization |
| Direct rep finds deal partner already registered | Defer to partner; direct rep is technical overlay if useful |
| Customer wants to buy via marketplace and direct rep is on the deal | Same price both channels; direct rep gets quota credit for marketplace deal |
| Partner brings deal to direct rep | Partner registered; partner gets full credit per agreement |
| Customer worked with partner pilot, asks for direct closing | Honor partner registration; direct overlay if helpful; partner gets credit |
| Renewal coming up, partner who sold initial wants exclusive | Standard: incumbent partner protected for 1-2 cycles |
| New partner wants to expand into existing partner's customer | Incumbent right-of-first-refusal for 90 days |
| Conflict escalates to VP level | 5 BD resolution; documented decision; precedent recorded |
| Conflict pattern repeats | Update registration policy or partner agreement to prevent next time |
