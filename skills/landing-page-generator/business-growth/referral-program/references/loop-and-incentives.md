# Referral Loop & Incentive Design

Read this when designing the core program: choosing referral vs affiliate, building the 4-stage loop, sizing rewards, and architecting trigger moments.

## Referral vs Affiliate Decision

| Factor | Customer Referral | Affiliate Program |
|--------|------------------|-------------------|
| Who promotes | Your existing customers | External partners, bloggers, influencers |
| Motivation | Loyalty, reward, social currency | Commission, audience monetization |
| Best for | B2C, prosumer, SMB SaaS | B2B SaaS, high LTV, content-heavy niches |
| Activation | Triggered by product satisfaction | Recruited and onboarded proactively |
| Payout | Account credit, discount, or cash reward | Revenue share or flat fee per conversion |
| CAC impact | Low -- reward is typically < 30% of first payment | Variable -- commission determines economics |
| Scale | Scales with active user base | Scales with partner recruitment |

**Decision rule:** If your customers are enthusiastic and social, start with customer referrals. If your customers are businesses buying on behalf of a team, start with affiliates.

---

## The 4-Stage Referral Loop

Every referral program runs on this loop. If any stage is weak, the entire program underperforms. Work the stages in order — a broken Stage 1 (trigger) can't be fixed by better rewards at Stage 4.

```
[Trigger Moment] → [Share Action] → [Referred User Converts] → [Reward Delivered] → Loop
```

- *Validate Stage 1:* trigger fires on a real satisfaction event, not at signup or in a generic monthly email
- *Validate Stage 2:* share friction is <3 taps/clicks and pre-filled copy is channel-specific
- *Validate Stage 3:* referred user lands on a referral-specific page, not the generic homepage
- *Validate Stage 4:* reward delivery is automatic and notified (manual reward ops kill the loop)

### Stage 1: Trigger Moment

When you ask customers to refer. Timing is everything.

**High-signal trigger moments:**

| Trigger | Why It Works | When to Fire |
|---------|-------------|-------------|
| After aha moment | User just experienced core value, highest satisfaction | After activation event |
| After milestone | Celebrates achievement, creates social sharing impulse | "You just saved your 100th hour" |
| After great support | Gratitude creates sharing impulse | Post-resolution, NPS 9-10 |
| After renewal/upgrade | Commitment signal, satisfied customer | Day of renewal |
| After public win | Customer tweets about you or posts a case study | Within 24 hours |
| After team growth | New team members = new potential referrers | After Nth team member joins |

**What does NOT work:**
- Asking at signup (no value experienced yet)
- Asking in every email footer (becomes invisible)
- Asking during onboarding (too early, too distracted)
- Generic monthly "refer a friend" email (no trigger, no urgency)

### Stage 2: Share Action

Remove every point of friction between wanting to share and actually sharing.

**Required share mechanics:**
- Personal referral link (unique per user, trackable)
- Pre-filled share message (editable, not locked)
- Multiple share channels: email invite, link copy, social share
- For B2B: Slack/Teams share option
- One-click send on mobile (native share sheet)

**Share message rules:**
- Written in first person (sounds like it is from a friend, not marketing)
- Includes the specific benefit the referrer experienced
- Short (2-3 sentences max)
- Includes the referral link with clear CTA

### Stage 3: Referred User Converts

The referred user lands on your product. Their experience must:

- Show personalization: "Your friend [Name] invited you"
- Display the incentive clearly above the fold
- Reduce signup friction (pre-fill email if available, offer SSO)
- Track attribution from landing through conversion (multi-session)

### Stage 4: Reward Delivered

The reward must be fast and clear. Delayed rewards break the loop.

| Action | Implementation |
|--------|---------------|
| Immediate confirmation | "Your friend just signed up! Here's your reward" |
| In-product visibility | Dashboard: "2 friends joined -- you've earned $40" |
| Email notification | Instant notification when referral converts |
| Easy redemption | Auto-applied credit or one-click claim |

---

## Incentive Design

### Single-Sided vs Double-Sided

| Type | When to Use | Cost | Conversion Impact |
|------|-------------|------|------------------|
| Single-sided (referrer only) | Strong viral hooks, enthusiastic users | Lower | Moderate |
| Double-sided (both get rewarded) | Need to overcome inertia on both sides | Higher | Higher |

**Decision rule:** If referral rate < 1%, go double-sided. If > 5%, single-sided is more profitable.

### Reward Types

| Type | Best For | Examples | Sizing Guideline |
|------|---------|---------|-----------------|
| Account credit | SaaS, subscription | "$20 credit toward your bill" | 10-20% of monthly plan |
| Discount | E-commerce, usage-based | "1 month free" | 1 month or 15-25% of annual |
| Cash | High LTV, B2C | "$50 for each referral" | < 30% of first payment |
| Feature unlock | Freemium products | "Unlock advanced analytics" | Feature value > cost |
| Status/recognition | Community products | "Ambassador badge" | Zero cost, high perceived value |
| Charity donation | Enterprise, mission-driven | "$25 to a cause you choose" | Similar to cash amount |

### Tiered Rewards (Gamification)

For referrers who go beyond 1 referral:

| Tier | Reward | Design Rule |
|------|--------|-------------|
| 1 referral | $20 credit | Easy to reach, immediate gratification |
| 3 referrals | $75 credit + bonus feature | Meaningful step-up, not just 3x |
| 10 referrals | $300 cash + ambassador status | Significant reward, social recognition |

**Rules:**
- Maximum 3 tiers (more is confusing)
- Each tier should feel meaningfully better, not just marginally
- Show progress toward next tier in the dashboard

### Reward Economics

```
Maximum reward per referral = LTV x Target referral CAC ratio

Example:
  Average LTV: $2,000
  Target referral CAC: 15% of LTV
  Maximum reward: $300

  If double-sided:
    Referrer reward: $150
    Referred reward: $150 (or equivalent credit/discount)
```

---

## Trigger Moment Architecture

### In-Product Trigger Points

| Location | Trigger Type | Copy Example |
|----------|-------------|-------------|
| Dashboard widget | Persistent, low-key | "Know someone who'd love [Product]? Give $20, get $20" |
| Post-milestone modal | Celebration moment | "You just hit 1,000 contacts! Share [Product] with a colleague?" |
| Settings/account page | Always available | "Referral Program: Earn $20 for every friend who joins" |
| Success state | After positive outcome | "Great results! Know someone who'd find this useful?" |
| Team invite flow | Natural sharing moment | "Or invite them via referral link and you both get $20" |

### Email Trigger Points

| Trigger | Email Content | Timing |
|---------|-------------|--------|
| Post-activation (first value delivered) | "Loving [Product]? Share it and earn rewards" | 3-5 days after activation |
| Post-NPS (score 9-10) | "Glad you love us! Here's an easy way to share" | Immediately after NPS |
| Post-renewal | "Thanks for staying with us! Share the love" | Day of renewal |
| Monthly digest | "Your referral status: [N] referrals, $[X] earned" | Monthly |
