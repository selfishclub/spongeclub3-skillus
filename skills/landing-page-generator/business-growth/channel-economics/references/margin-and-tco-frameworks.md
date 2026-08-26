# Margin and TCO Frameworks for Channel Economics

Reference for building a true total-cost-of-ownership (TCO) model that lets you compare channel options apples-to-apples. Covers per-cost-line guidance, allocation patterns, "fully loaded" calculations, and the worked examples that turn rough-cut comparisons into defensible decisions.

---

## Why TCO matters

Naive channel comparison: "Reseller gets 25% margin, direct gets 100%, so direct is 4x better." This is wrong because it ignores:

- Direct still has sales cost (CAC)
- Direct still has marketing cost
- Reseller may bring leads we couldn't get
- Reseller may close faster (sales cycle)
- Reseller may bring implementation services we don't offer

A proper TCO comparison gets you to **net contribution margin** per channel — what we actually keep after every cost is allocated.

---

## The TCO formula

```
Net Contribution Margin (per channel)
  = Channel Revenue
  − COGS
  − Partner Margin / Channel Fee
  − Channel-attributed Sales Cost
  − Channel-attributed Marketing Cost
  − Channel-attributed CSM Cost
  − Partner Enablement Cost (amortized)
  − Channel Operations Cost (amortized)
  − Channel-attributed Support Cost
```

Each cost line has a specific allocation question. Let's walk through each.

---

## Cost line: COGS (Cost of Goods Sold)

**Definition:** Direct cost of delivering the product to one customer.

**For SaaS:** Hosting / infrastructure, third-party APIs called per customer, support tier-1 (if not separately allocated).

**Typical %:** 10-20% of revenue for mature SaaS; 20-35% for AI/ML-heavy or compute-intensive.

**Channel allocation:**
- Same across channels (a customer costs the same to serve regardless of how they bought)
- Exception: OEM / white-label can sometimes have lower per-instance cost if you batch hosting

**Common error:** Including S&M cost in COGS. Don't — COGS is delivery cost only.

---

## Cost line: Partner Margin / Channel Fee

**Definition:** What you pay the channel for the deal.

**Per-channel typical:**

| Channel | Partner margin / fee |
|---------|---------------------|
| Direct | 0% |
| Reseller | 15-30% off list |
| VAR | 25-40% off list |
| Distributor | 5-15% (often layered with reseller margin) |
| Marketplace (cloud) | 3-5% |
| Marketplace (app store) | 15-25% |
| OEM / Embedded | 30-60% (depends on volume) |
| MSP | 30-50% |
| Affiliate (one-time) | 10-25% (lower if recurring) |

**Allocation:** Direct deduction from channel revenue.

**Common errors:**
- Forgetting back-end rebates (front-end discount + rebate = real total cost)
- Not modeling tier thresholds (partner growth → higher discount tier → margin compression)
- SPIFFs / MDF treated as marketing, but really commission

---

## Cost line: Channel-attributed Sales Cost

**Definition:** What we spend on sales effort for this channel.

**Direct sales cost components:**
- AE compensation (base + commission) × % of time on this channel
- SE / Sales Engineer (if applicable)
- SDR / BDR for outbound prospecting
- Sales manager overhead allocation

**Reseller / VAR channel sales cost:**
- Channel manager compensation
- Channel SE (for partner technical enablement)
- Direct sales overlay (if direct rep co-sells on partner deals)

**Marketplace sales cost:**
- Often much lower per deal — marketplace's sales team brings leads
- Co-sell engagement (your team's time to co-pursue)

**Allocation methods:**

| Method | When to use |
|--------|-------------|
| **Direct attribution** | Deal-by-deal sales effort visible (large enterprise deals) |
| **% of capacity allocation** | Reps split time across channels |
| **Fully-loaded CAC** | When deal-level attribution isn't feasible; allocate total sales cost / total deals × this deal's contribution |
| **Marginal CAC** | When the incremental deal cost is what matters (marketplace adds lower marginal cost) |

**Typical fully-loaded sales cost as % of revenue:**

| Channel | Sales cost % |
|---------|-------------|
| Direct enterprise | 25-35% |
| Direct mid-market | 20-25% |
| Reseller | 5-10% (overlay + channel manager) |
| Marketplace | 5-15% (co-sell time) |
| OEM / Embedded | 5-10% (strategic alliance team) |
| MSP | 5-10% |

---

## Cost line: Channel-attributed Marketing Cost

**Definition:** Marketing spend attributable to this channel.

**Direct channel marketing:**
- Demand-gen campaigns (paid, content, events) for direct leads
- Brand campaigns (partially allocated)

**Partner / channel marketing:**
- MDF (Marketing Development Funds) given to partners
- Co-marketing campaigns (you + partner shared spend)
- Partner-conference sponsorships
- Partner-enablement marketing materials production
- Partner portal content + maintenance

**Marketplace marketing:**
- Listing optimization (designers, copywriters)
- Marketplace-specific paid placements
- Marketplace events (AWS re:Invent, etc.)

**Allocation:**
- Direct-attributable: campaign-source tagging
- Brand spend: allocate proportional to revenue or just exclude (call it "above-the-line")

**Typical marketing cost as % of revenue:**

| Channel | Marketing cost % |
|---------|------------------|
| Direct (with strong PMM) | 10-20% |
| Reseller | 5-15% (MDF + co-marketing) |
| Marketplace | 5-10% |
| OEM | 1-5% (lower; embedded marketing is partner's job mostly) |

---

## Cost line: Channel-attributed CSM Cost

**Definition:** Customer success cost for retention / expansion / support.

**Direct CSM:** Per-customer CSM ratio (1 CSM per 10-50 customers typical).
**Channel CSM:** Often lower-touch (partner provides T1 customer-facing support); CSM ratio higher (1 per 30-100).
**OEM:** Largely managed by partner; CSM minimal or per-partner instead of per-end-customer.

**Allocation:**
- CSM headcount × cost / # customers serviced
- Year-1 CSM cost typically higher than year-2+

**Typical CSM cost as % of revenue:**

| Channel | CSM cost % |
|---------|-----------|
| Direct enterprise | 5-10% |
| Direct mid-market | 3-8% |
| Reseller (partner-led CSM) | 1-3% |
| OEM | <1% |

---

## Cost line: Partner Enablement Cost

**Definition:** Investment in making partners successful — training, certification, technical resources.

**Components:**
- Partner training program (LMS, content creation, instructor time)
- Certification exam delivery
- Partner technical resources (architecture guides, code samples, demo environments)
- Annual partner conference

**Allocation:**
- Total enablement spend / active partner count = per-partner cost
- Per-deal allocation: per-partner cost / partner's deals per year

**Typical:** $50k-$500k per year for a partner program (depends on partner count + program ambition).

**Often forgotten:** This is real cost — many channel programs are unprofitable when this is properly counted.

---

## Cost line: Channel Operations Cost

**Definition:** Channel-program operational overhead — channel manager, channel ops, partner portal, deal-reg system, MDF approval workflow.

**Components:**
- Channel Manager compensation
- Channel ops headcount
- Partner portal software / development
- Deal registration system
- MDF approval workflow + administration

**Typical:** 1 CM per 10-15 active partners (managing). Plus 0.5-1.0 channel ops FTE per CM.

**Allocation:**
- Total channel ops cost / channel revenue = % overhead
- Per-deal allocation: total cost / # deals processed

**Typical:** 2-8% of channel revenue.

---

## Cost line: Channel-attributed Support Cost

**Definition:** Tier-1 / tier-2 support cost for this channel's customers.

**Direct:** Per-ticket cost × tickets per customer.
**Reseller / VAR:** Partner handles tier-1; you handle tier-2 → lower per-customer cost on your side.
**OEM:** Often custom support tier with dedicated team for partner technical contacts.

**Allocation:** Per-customer support cost × customers per channel × channel multiplier.

**Typical support cost as % of revenue:**

| Channel | Support cost % |
|---------|---------------|
| Direct | 3-8% |
| Partner-fronted | 1-3% |
| OEM | 5-15% (custom support tier) |

---

## Worked example: comparing 3 channels for a $100k deal

Assumptions:
- COGS: 15% of revenue
- Standard discount: 25% via reseller, 30% via OEM
- Direct: standard rep + SE

| Cost line | Direct | Reseller (25% off) | Marketplace (3%) | OEM (30% off) |
|-----------|--------|---------------------|------------------|----------------|
| Customer payment | $100,000 | $100,000 | $100,000 | $100,000 |
| Partner margin / fee | $0 | -$25,000 | -$3,000 | -$30,000 |
| Revenue to us | $100,000 | $75,000 | $97,000 | $70,000 |
| COGS (15%) | -$15,000 | -$11,250 | -$14,550 | -$10,500 |
| Sales cost | -$25,000 (25%) | -$5,000 (channel mgr overlay) | -$8,000 (co-sell time) | -$5,000 (alliance team) |
| Marketing cost | -$10,000 (10%) | -$5,000 (MDF) | -$3,000 (listing) | -$1,000 |
| Partner enablement | $0 | -$2,500 (amortized) | -$1,500 (amortized) | -$5,000 (per OEM partner) |
| Channel ops | $0 | -$1,500 (amortized) | -$1,000 (amortized) | -$3,000 (alliance) |
| CSM cost | -$5,000 | -$2,000 | -$3,000 | -$500 (partner-led) |
| Support cost | -$3,000 | -$1,500 | -$2,000 | -$5,000 (custom OEM tier) |
| **Net contribution** | **$42,000** | **$46,250** | **$63,950** | **$40,000** |
| **% of customer payment** | **42%** | **46.25%** | **64%** | **40%** |

**Insights:**
- Marketplace looks best per-deal — but volume?
- Reseller actually better than direct here — because direct CAC is high
- OEM looks worst per $100k deal — but you might do 1000x the volume

**The volume question:**
- Direct: 50 deals/year @ $42k contribution = $2.1M
- Reseller: 200 deals/year @ $46.25k = $9.25M
- Marketplace: 75 deals/year @ $64k = $4.8M
- OEM: 10,000 customers @ avg $5k → $2k per customer contribution × 10,000 = $20M

OEM wins at volume; direct loses on volume. Pick channels by total contribution, not per-deal.

---

## Allocation challenges

### Allocating shared costs

Brand marketing, exec team time, finance / legal / HR — these are shared. Options:

1. **Allocate by revenue share** — easy, defensible, slightly arbitrary
2. **Allocate by headcount supporting each channel** — more accurate, harder to measure
3. **Exclude from per-channel analysis** — say "this is gross-of-shared-cost" and acknowledge

Most companies use option 1 with note that it's an approximation.

### Marginal vs full cost

When evaluating "should we add this channel?":
- **Marginal cost** = incremental cost of adding this channel (if you reuse existing CSM, marketing team, etc., marginal is much lower than full)
- **Full cost** = if you scaled this channel, what would each deal really cost?

Use marginal for "should we test this channel" decisions; use full for "should we keep this channel" decisions.

### Year 1 vs steady-state

First year of any channel is expensive — enablement, ramp-up, learning. Year 2-3 is steady-state.

Show both in TCO models:
- Year 1 P&L
- Steady-state (year 3) P&L
- 3-year cumulative P&L

Don't kill a channel after year 1 just because year-1 economics are upside-down.

---

## How to use TCO models

### For new channel evaluation

1. Model the channel at expected steady-state volume
2. Compare contribution margin to direct alternative
3. If channel is more profitable per deal OR brings new revenue you couldn't get direct: green-light pilot
4. Re-model after 6 months of actual data
5. Decide: scale, sustain, or shutdown

### For existing channel review

Quarterly:
1. Actual contribution margin per channel
2. Trend vs prior quarter (improving, flat, declining)
3. Channel mix shift over time
4. Investment ROI per channel ($spent_on_channel / $contribution_from_channel)

Annually:
1. Full channel-strategy review with CRO / CFO
2. Rebalance investment (hire more CMs for high-ROI channels; reduce headcount on low-ROI)

### For specific deal evaluation

For each non-standard partner deal:
1. Calculate contribution at requested terms
2. Compare to direct alternative
3. Decision input for deal desk

`scripts/channel_margin_calculator.py` automates this calculation.

---

## Pitfalls

### Pitfall: Ignoring opportunity cost

If channel A's deals would have closed direct anyway, you're not gaining anything — you're paying margin for no incremental revenue.

**Detection:** Survey closed-won partner deals: "would you have bought direct if partner wasn't available?" Surprisingly often: yes.

### Pitfall: Stale cost assumptions

CSM ratio was 1:30 two years ago; now 1:50 because you scaled. Cost per customer has changed. Refresh annually.

### Pitfall: Treating MDF as marketing-only

MDF is a partner-incentive cost; channel-economics should include it in channel cost. Don't hide it in marketing budget where channel-margin looks artificially high.

### Pitfall: Conflating list price with realized price

Channel deals are almost always discounted. If your "list-price contribution" calculation assumes direct list, you're overstating direct profitability.

### Pitfall: Different cost categories per channel making comparison meaningless

Standardize the TCO template. Same categories, same allocation methods, across all channels. Otherwise comparing apples to oranges.

---

## Cheat sheet for channel TCO

| Question | Answer |
|----------|--------|
| What's the most important number? | Net contribution margin per channel — not gross revenue, not unit economics |
| Compare apples-to-apples — what's the trick? | Use same TCO template per channel; same categories, same allocation method |
| Year-1 economics terrible — kill the channel? | Look at steady-state (year 3) projection; year-1 is investment |
| Reseller margin lower than direct — kill resellers? | Compare to *fully loaded* direct economics; reseller saves CAC + brings new revenue often |
| Marketplace fee is small — should we list everywhere? | Listing without investment generates nothing; commit to optimization or skip |
| OEM contribution per deal is low — is it worth it? | Multiply by volume — OEM volume can dwarf per-deal margin difference |
| When to walk away from a channel? | When steady-state contribution < incremental cost OR when channel cannibalizes higher-margin direct |
