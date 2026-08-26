# Pricing Models — Axes, Value Metrics, Tiers, Value-Based Pricing

Read this when designing pricing from scratch or restructuring tiers: the three
pricing axes (in order), how to pick a value metric, how to architect tiers, and
how to price inside the value corridor.

## The Three Pricing Axes

Every pricing decision lives across three axes. Most teams skip to price point. That is backwards.

```
     ┌──────────────────┐
     │   VALUE METRIC    │  What do you charge for?
     │  (how it scales)  │  (per seat, per usage, per feature)
     └────────┬─────────┘
              │
     ┌────────┴─────────┐
     │   PACKAGING       │  What is in each tier?
     │  (what you get)   │  (feature bundles, limits, support levels)
     └────────┬─────────┘
              │
     ┌────────┴─────────┐
     │   PRICE POINT     │  How much?
     │  (the number)     │  (actual dollar amount)
     └──────────────────┘
```

Lock in the value metric first, then packaging, then test the price point.

---

## Value Metric Selection

### Common Value Metrics

| Metric | Best For | Examples | Scales With Value? |
|--------|---------|---------|-------------------|
| Per seat / user | Collaboration tools, CRMs | Salesforce, Notion, Linear | Yes if all users are active |
| Per usage | APIs, infrastructure, AI | Stripe, Twilio, OpenAI | Yes |
| Per feature | Platform plays, modular products | HubSpot, Intercom | Somewhat |
| Flat fee | Simple products, SMB market | Basecamp, Calendly | No (subsidizes heavy users) |
| Per outcome | Measurable ROI products | Commission-based tools | Perfectly |
| Hybrid | Most mature SaaS | Base fee + usage, seat + features | Yes |

### Selection Criteria

Answer these 4 questions:

| Question | Answer Points To |
|----------|-----------------|
| What makes a customer willing to pay MORE? | That is your value metric |
| Does the metric scale with their success? | If they grow, you should grow |
| Is it easy to understand? | Complexity kills conversion |
| Is it hard to game? | Customers should not be able to work around it |

### Value Metric Red Flags

| Red Flag | Problem | Fix |
|---------|---------|-----|
| Per-seat in a tool where 1 power user does all the work | Seats do not scale with value | Switch to usage or feature-based |
| Flat fee when some customers get 10x the value of others | Subsidizing heavy users | Add usage tiers or hybrid model |
| Per-API-call when volume varies wildly week to week | Unpredictable bills cause churn | Add usage bands or committed minimums |
| Per-feature when core value requires multiple features | Nickel-and-diming perception | Bundle core features, gate advanced only |

---

## Tier Architecture

### Good-Better-Best (3 Tiers)

Three tiers is the standard because it anchors perception.

| Tier | Role | Pricing Rule | Feature Rule |
|------|------|-------------|-------------|
| Entry (Good) | Captures price-sensitive segment | Covers your costs minimum | Core product, limited usage |
| Middle (Better) | Where you push most customers | 2-3x entry tier | Everything a growing company needs |
| Top (Best) | High-value enterprise customers | 3-5x entry or custom | SSO, audit logs, SLA, dedicated support |

### Feature Allocation Framework

| Feature Category | Entry Tier | Middle Tier | Top Tier |
|-----------------|-----------|------------|---------|
| Core product | Limited | Full | Full |
| Usage limits | Low | Medium | High/Unlimited |
| Users/seats | 1-3 | 5-25 or unlimited | Unlimited |
| Integrations | Basic (3-5) | Full | Full + custom |
| Reporting | Basic | Advanced | Custom |
| Support | Email (48h) | Priority (24h) | Dedicated CSM |
| Admin features | -- | -- | SSO, SCIM, audit logs |
| SLA | -- | -- | 99.9% uptime |
| Data retention | 90 days | 1 year | Unlimited |
| API access | -- | Rate-limited | Full |

### Tier Naming

| Approach | Examples | Best For |
|----------|---------|---------|
| Size-based | Starter, Growth, Enterprise | Universal SaaS |
| Capability-based | Basic, Pro, Enterprise | Feature-differentiated products |
| Audience-based | Individual, Team, Organization | Collaboration tools |
| Persona-based | Freelancer, Agency, Enterprise | Audience-segmented products |

**Naming rules:**
- Names should be instantly understandable
- Avoid jargon or made-up words
- The default/recommended plan should be visually highlighted

---

## Value-Based Pricing

### The Pricing Corridor

```
[Cost floor] ... [Next-best alternative] ... [YOUR PRICE] ... [Perceived value]
```

### Step-by-Step

**Step 1: Define the next-best alternative**
- What would the customer do without your product?
- What does that cost them? (competitor, manual process, hiring)

**Step 2: Estimate value delivered**
- Time saved x hourly rate of the person using it
- Revenue generated or protected
- Cost of errors/risk avoided
- Ask customers: "What would you lose if you stopped using us?"

**Step 3: Price in the corridor**
- Price at 10-20% of documented value delivered
- Above the next-best alternative (signals confidence)
- Below the perceived value ceiling (customer feels good ROI)

### Conversion Rate as a Pricing Signal

| Trial-to-Paid Rate | Signal | Action |
|-------------------|--------|--------|
| > 40% | Likely underpriced | Test a 20-30% price increase |
| 15-30% | Healthy for most SaaS | Optimize packaging, not price |
| < 10% | Possibly overpriced OR trial experience is broken | Investigate whether the issue is price or activation |
