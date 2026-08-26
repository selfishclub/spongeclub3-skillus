# Channel Models: Direct, Partner, Marketplace

Deep reference on the six core channel models — direct sales, reseller / VAR, distributor, marketplace, embedded / OEM / ISV, MSP / managed service. For each: economic structure, typical margin splits, sales motion, when it works, when it fails, contract patterns, ops requirements.

---

## Channel model 1: Direct sales

**What:** Your sales team sells your product directly to the end customer. No intermediary.

**Sub-types:**
- **Self-serve / PLG (Product-Led Growth)**: customer signs up via web, expands organically
- **Inside sales / SDR-led**: SDRs prospect, AEs close — usually mid-market
- **Field sales / Enterprise**: account-based, multi-month cycles, high-touch

### Economic structure

- 100% revenue to you
- All sales costs (CAC) to you
- All implementation costs (or charged separately as services)
- COGS standard

### When it works

- Product / market fit established; buyer journey understood
- High enough ACV to justify the sales investment ($25k+ for SDR-led; $100k+ for field)
- Brand / discovery isn't dependent on partner relationships
- You can build sales / marketing capability faster than partner can scale

### When it fails

- Geographic / language barriers (US sales team selling into Japan)
- Vertical expertise required that you don't have (selling to defense, you need cleared people)
- Buyer has procurement preference to buy via existing vendor
- Product complexity requires hand-holding implementation that's not your specialty

### Typical contract

Your standard MSA with customer. Standard terms apply.

### Ops requirements

- Marketing demand-gen team
- SDR / AE team
- Sales engineering for technical validation
- CSM team for retention / expansion
- Marketing ops + sales ops

### Per-deal economics (example: $100k ACV)

| Line | Amount |
|------|--------|
| Customer revenue | $100,000 |
| COGS | -$15,000 |
| Sales cost (CAC, allocated) | -$25,000 |
| Marketing cost (allocated) | -$10,000 |
| CSM cost (year 1) | -$5,000 |
| **Net contribution** | **$45,000 (45%)** |

---

## Channel model 2: Reseller / VAR

**What:** A partner organization sells your product (sometimes alongside others), takes a cut, may add services / configuration / consulting.

**Distinction:**
- **Reseller**: minimal added value; primarily transactional
- **VAR (Value-Added Reseller)**: substantial added value (configuration, integration, training, support)

### Economic structure

- Customer pays reseller; reseller pays you (less the discount)
- OR customer pays you; you pay reseller commission (varies by partner agreement)
- Typical reseller discount: 15-25%
- Typical VAR discount: 25-40% (more value-add justifies higher cut)

### When it works

- Geographic / language coverage you can't build (local language, in-country support)
- Vertical / domain expertise (regulated industries, niche markets)
- Established customer relationships you'd take years to build
- Implementation-heavy product where partner is the integrator

### When it fails

- Partner sells competitors (their loyalty is unclear)
- Partner-driven deals get reseller markup that prices you out
- Partner promises features / SLAs you don't actually offer
- Customer relationship is owned by partner; you have no visibility / leverage

### Typical contract

- **Partner Agreement** (master): governs the relationship — partner status, terms, mutual obligations
- **Deal-level addendum**: per-customer terms (often standard MSA flowed through)
- **Pricing exhibit**: discount tiers, rebate structures, MFN-like clauses (if any)

### Ops requirements

- Channel manager (CMs) — 1 per 10-15 active partners
- Deal registration system
- Partner certification / training program
- Partner portal (deal reg, MDF, training, marketing materials)
- Co-marketing / MDF approval workflow

### Per-deal economics (example: $100k ACV reseller, 25% discount)

| Line | Amount |
|------|--------|
| Customer payment | $100,000 |
| Reseller margin (25%) | -$25,000 |
| Revenue to us | $75,000 |
| COGS | -$11,250 |
| Channel-allocated sales cost | -$5,000 |
| Channel-allocated marketing | -$8,000 |
| Partner enablement (amortized) | -$3,000 |
| Channel ops (amortized) | -$2,000 |
| CSM cost (year 1) | -$3,000 |
| **Net contribution** | **$42,750 (42.75% of $100k or 57% of $75k revenue)** |

---

## Channel model 3: Distributor

**What:** A high-volume aggregator that resells to other partners (resellers, VARs, retailers). One layer removed from end customer.

**Common in:** Hardware, infrastructure software, consumer goods, telecom.

### Economic structure

- Distributor takes 5-15% margin
- You get larger volumes than direct could deliver
- Distributor handles invoicing, AR, sometimes logistics
- Reseller margin layered on top (so customer-side pricing: list × distributor cut × reseller cut)

### When it works

- High volume / low ACV product (selling to thousands of small businesses via long tail of resellers)
- Geographic spread that direct relationships can't serve
- Standardized SKUs that need no configuration

### When it fails

- Highly customizable products
- Direct customer relationship matters
- Brand differentiation requires direct visibility
- Margins too tight to support multiple intermediaries

### Typical contract

- **Distributor Agreement**: long-term, exclusive or non-exclusive territory rights
- **SKU pricing**: distributor wholesale price; MSRP recommended
- **Inventory / forecasting commitments**: distributor commits to volume

### Ops requirements

- Distribution manager
- Logistics / fulfillment integration
- Channel inventory management
- Co-op marketing programs (often per-distributor)

---

## Channel model 4: Marketplace

**What:** Customer buys through a marketplace platform (AWS Marketplace, Azure Marketplace, GCP Marketplace, Salesforce AppExchange, Shopify App Store, etc.). Marketplace handles billing; takes a fee; you get the rest.

### Economic structure

- Marketplace fee: typically 3-15% (AWS / Azure / GCP: ~3%; Salesforce AppExchange: 15-25%)
- Customer payment terms = marketplace's terms (usually fast)
- Marketplace gets the customer relationship technically (you see the contract, but customer-of-record is sometimes the marketplace)
- Co-sell programs (AWS Co-Sell, Azure Co-Sell) provide direct sales support from the marketplace operator

### When it works

- Buyer already procures heavily on that marketplace (saves a procurement cycle = real value to buyer)
- Marketplace's co-sell motion brings introductions you couldn't make
- Marketplace pulls budget from a different bucket (cloud committed-spend) that you couldn't access

### When it fails

- Marketplace listing built once, never optimized — generates no demand
- Marketplace fee on top of all the direct costs (you didn't reduce sales effort, just added a fee)
- Customer concentration in non-marketplace verticals — no buyers there

### Typical contract

- **Marketplace operator agreement** (one-time, governs all listings)
- **Customer-side**: usually marketplace's standard terms with optional EULA addendum

### Ops requirements

- Marketplace ops lead (one person can usually handle multiple marketplaces)
- Co-sell program engagement (deal registration, joint pursuit)
- Listing optimization (SEO, screenshots, customer reviews)
- Integration with marketplace billing / metering

### Per-deal economics (example: $100k ACV via AWS Marketplace, 3% fee)

| Line | Amount |
|------|--------|
| Customer payment | $100,000 |
| AWS Marketplace fee (3%) | -$3,000 |
| Revenue to us | $97,000 |
| COGS | -$14,550 |
| Sales cost (lower; AWS co-sell brought lead) | -$8,000 |
| Marketing cost (listing maintenance) | -$5,000 |
| Marketplace ops (amortized) | -$1,500 |
| CSM cost | -$5,000 |
| **Net contribution** | **$62,950 (63% of $100k)** |

Marketplace can be more profitable than direct *per deal* — but volume / conversion is the question. Investment in listing optimization + co-sell engagement is what makes the channel work.

---

## Channel model 5: Embedded / OEM / ISV

**What:** Your product is embedded inside another vendor's product (white-labeled, OEM'd, or as a component). The customer doesn't see you (white-label) or sees you as an embedded brand (powered-by).

### Sub-types

- **OEM (Original Equipment Manufacturer)**: your product white-labeled inside partner's product; customer sees only partner's brand
- **Embedded**: your product clearly visible inside partner's (e.g., "Powered by [your name]")
- **ISV (Independent Software Vendor) on a platform**: your product runs on someone's platform (Salesforce AppExchange, Microsoft 365, Shopify) — usually exposed to customer

### Economic structure

- Often royalty / revenue-share: partner pays you % of their resale revenue
- OR per-seat / per-instance fees scaled to partner's customer base
- OR fixed annual fee for unlimited use up to some cap
- ASP can be lower than direct (you're a feature, not the whole product) but volume can be huge

### When it works

- Your product is a feature, not a standalone (e.g., authentication, billing, AI capabilities)
- Partner's GTM is much stronger than yours
- Embedded volume justifies lower per-unit price

### When it fails

- Customer becomes partner's customer; you lose direct relationship
- Partner's growth lags expectations; lock-in cost was high
- Partner cancels embedded relationship (rebuilds in-house); your revenue vanishes
- Partner uses your product without paying / out of scope

### Typical contract

- **OEM / Embedded Agreement**: long-term (3-7 years), often exclusive in defined market
- **Revenue / royalty model**: tracked + audited quarterly
- **Co-development rights**: if applicable

### Ops requirements

- Strategic alliance team (often 1-2 senior people per major OEM partner)
- Embedded-product technical support (different SLAs from direct customers)
- Royalty tracking / audit
- Joint roadmap sessions

### Per-deal economics

Hard to model on per-deal basis; better to model annually:
- Partner has 10,000 customers
- ASP per customer (in OEM context): $50/year (vs $500 direct)
- Annual revenue from OEM: $500k
- Total cost of supporting OEM: $200k (engineering + alliance team)
- Net contribution: $300k

Compare to direct: would we have sold $500k of direct revenue with $200k of customer acquisition? Often yes; sometimes no (OEM reaches markets you couldn't).

---

## Channel model 6: MSP / managed service

**What:** Managed Service Provider operates your product on behalf of the customer. Customer pays MSP; MSP pays you (or holds the contract with you, charges customer for service).

**Common in:** Security (MSSP), networking, observability, backup, compliance.

### Economic structure

- MSP buys at significant discount (often 30-50% off list)
- MSP charges customer for the managed service (your product + their labor)
- Customer doesn't see your invoicing; MSP is the vendor of record

### When it works

- Product needs operational expertise customers don't have
- Customer prefers "managed" model (no in-house team for this domain)
- MSP brings industry expertise (security firm specializing in healthcare)

### When it fails

- MSP is incompetent at operating your product → bad experience reflects on you
- MSP overcommits SLAs you can't deliver underneath
- Customer eventually wants direct relationship; MSP resists transition

### Typical contract

- **MSP Agreement**: terms similar to reseller + operational requirements (certification, SLA flow-down)
- **Per-customer addendum**: as MSP onboards each customer, deals registered

### Ops requirements

- MSP-specific support tier (24/7 ops support that MSP can call)
- MSP certification (operators need to know the product)
- Customer-success oversight (you want visibility into how MSP customers are doing)

---

## Hybrid models (most common in practice)

Most companies use 2-4 channel models simultaneously:

| Customer segment | Primary channel | Secondary |
|------------------|-----------------|-----------|
| SMB | PLG / Self-serve | Marketplace |
| Mid-market | Inside sales | Reseller / VAR |
| Enterprise | Field sales | SI / Integrator |
| Vertical (regulated) | VAR / Specialist | Direct overlay |
| Geographic (non-home market) | Reseller / Distributor | Marketplace |

The key: **define each customer segment's primary channel**. Channel conflict happens when no one segment owns each customer.

---

## When NOT to use channels

- **Pre-PMF**: build direct first. You need to learn the buyer / message / pricing. Partners can't do that for you.
- **Sub-scale GTM**: channel programs require investment (channel manager, MDF, certification) — break-even at $5M-$10M ARR in channel-attributed revenue.
- **High-touch white-glove**: very high-ACV deals where customer specifically wants you = stay direct.
- **Highly competitive vendor-driven market**: when buyer chooses on vendor reputation, channel adds confusion not value.

---

## Channel evaluation framework (when adding a new channel)

Before adding a channel, answer:

1. **Strategic rationale**: what gap does this channel fill? (geography, vertical, capacity, customer preference)
2. **Economic case**: net contribution margin > direct? OR new revenue we couldn't get direct?
3. **Investment required**: channel manager hire, MDF budget, technology (deal reg portal), training program
4. **Time to scale**: 12-18 months minimum from launch to material contribution
5. **Conflict resolution**: how does this channel coexist with direct + existing channels?
6. **Exit path**: if it doesn't work, how do we wind down without burning bridges?

If you can't answer 4 of 6 confidently, don't launch.

---

## Quick comparison matrix

| Model | Cust. relationship | Margin to us | Speed to market | Investment to scale |
|-------|---------------------|--------------|-----------------|---------------------|
| Direct | Owned | High (50-60%) | Slow | High (sales hires) |
| Reseller | Shared | Medium (40-50%) | Medium | Medium (channel ops) |
| Distributor | Lost | Lower (30-40%) | Fast | Low (per existing distrib relationships) |
| Marketplace | Mixed | High per deal (60%+) | Medium | Medium (listing + co-sell investment) |
| OEM / Embedded | Lost | Variable (depends on volume) | Slow (long deal cycles) | High (strategic alliance) |
| MSP | Lost | Lower (30-40%) | Medium | Medium (cert + support tier) |

---

## Cheat sheet

| Question | Answer |
|----------|--------|
| Where to start? | Direct, until PMF + $5M+ ARR |
| First channel to add? | Usually marketplace (low-investment, listing-driven) or 2-3 strategic resellers (vertical/geographic) |
| When to add OEM / embedded? | When a partner approaches you with credible volume + you have product-market fit |
| When to add distributor? | When you have high-volume / low-ACV product and geographic spread needed |
| When to add MSP? | When operational complexity is a barrier and managed-service-loving customers exist |
| How many channels can we support? | 1 channel per $20M+ of channel-attributed revenue justifies dedicated investment |
