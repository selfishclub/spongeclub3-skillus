# Optimization, Metrics & Operations

Read this when diagnosing a stalled program, benchmarking metrics, running the scripts, troubleshooting, or checking success criteria and anti-patterns. Includes output artifacts and the tool reference.

## Optimization Playbook

### Diagnose Before Optimizing

| Metric | Benchmark | If Below | Fix |
|--------|-----------|----------|-----|
| Program awareness | > 40% of active users know it exists | Promote in-app, post-activation emails, dashboard widget |
| Active referrers | 5-15% of active users | Improve trigger moments, timing, and incentive |
| Share rate | 20-40% of those who see the prompt | Simplify share flow, improve message copy |
| Referred conversion rate | 15-25% | Improve referral landing page, add incentive |
| Reward redemption | > 70% within 30 days | Reduce redemption friction, send reminders |

### Optimization Priority

1. **Fix awareness first** -- If users do not know the program exists, nothing else matters
2. **Fix the share flow** -- If users know but do not share, the friction is too high
3. **Fix the referred experience** -- If users share but referrals do not convert, the landing page fails
4. **Optimize the incentive** -- Only change the reward after the mechanics work

---

## Metrics and Benchmarks

### Key Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Referral rate | Referrals sent / Active users | 5-15% |
| Active referrers % | Users who sent 1+ referral / Active users | 5-15% |
| Referral conversion rate | Referred signups / Referrals sent | 15-25% |
| Referral CAC | Total reward cost / Referral-acquired customers | < 50% of other CAC |
| Referral revenue % | Revenue from referred customers / Total revenue | 10-25% |
| K-factor | Invitations per user x Conversion rate | 0.3-0.7 |
| Referred customer LTV | LTV of referred vs non-referred | Referred should be higher |

### Revenue Impact Model

```
Monthly referral revenue = Active users x Referral rate x Conversion rate x ACV / 12

Example:
  10,000 active users x 10% referral rate x 20% conversion rate x $600 ACV / 12
  = $10,000/month in new referral-driven MRR

  Annual impact: $120,000 in new ARR
  Reward cost (at $50/referral): 200 referrals x $50 = $10,000
  ROI: 12x return on reward investment
```

---

## Output Artifacts

| Artifact | Format | Description |
|----------|--------|-------------|
| Referral Program Design | Full spec | Loop design, incentive structure, trigger moments, share mechanics |
| Incentive ROI Model | Revenue calculation | Reward sizing against LTV/CAC with multiple scenarios |
| Program Copy Set | Complete copy | In-app prompts, emails, share messages, landing page |
| Affiliate Program Spec | Structure + toolkit | Commission model, tiers, recruitment list, partner assets |
| K-Factor Model | Calculation + improvement plan | Current K, target K, lever-by-lever improvement plan |
| Optimization Audit | Metric scorecard | Current metrics vs benchmarks with prioritized fixes |
| Dashboard Specification | UI design | Referral stats, link sharing, progress tracking |

---

## Tool Reference

### 1. referral_economics_calculator.py

Calculates referral program economics including reward sizing, K-factor, referral CAC, ROI projections, and break-even analysis. Models double-sided vs single-sided reward structures.

```bash
python scripts/referral_economics_calculator.py program.json --format text
python scripts/referral_economics_calculator.py program.json --format json
```

| Flag | Type | Description |
|------|------|-------------|
| `program.json` | positional | Path to JSON file with program economics data |
| `--format` | optional | Output format: `text` (default) or `json` |

### 2. referral_funnel_analyzer.py

Analyzes the 4-stage referral loop (trigger, share, convert, reward) with stage-over-stage conversion, identifies the weakest stage, and provides prioritized improvement recommendations.

```bash
python scripts/referral_funnel_analyzer.py funnel.json --format text
python scripts/referral_funnel_analyzer.py funnel.json --format json
```

| Flag | Type | Description |
|------|------|-------------|
| `funnel.json` | positional | Path to JSON file with referral funnel metrics |
| `--format` | optional | Output format: `text` (default) or `json` |

### 3. affiliate_commission_modeler.py

Models affiliate program commission structures across tier levels. Calculates per-tier economics, lifetime partner value, and compares commission models (flat fee vs recurring percentage).

```bash
python scripts/affiliate_commission_modeler.py affiliate.json --format text
python scripts/affiliate_commission_modeler.py affiliate.json --format json
```

| Flag | Type | Description |
|------|------|-------------|
| `affiliate.json` | positional | Path to JSON file with affiliate program data |
| `--format` | optional | Output format: `text` (default) or `json` |

---

## Troubleshooting

| Problem | Likely Cause | Resolution |
|---------|-------------|------------|
| Program awareness below 40% of active users | Referral program is buried in settings or only mentioned in email footers | Add persistent dashboard widget, post-activation prompt, and post-NPS trigger; desktop sharing now outperforms mobile (2026 data) |
| Users see prompt but share rate is below 20% | Share flow has too much friction or pre-filled message is not compelling | Add one-click copy link, native share sheet on mobile, pre-filled first-person message; ensure multiple channels (email, Slack, social) |
| Referrals sent but conversion rate below 15% | Referral landing page lacks personalization or incentive is not prominent | Add referrer name/photo, display incentive above fold, reduce signup friction; mobile-referred users convert 2-3x (2026 data) |
| K-factor below 0.1 | Fundamental program design issue -- either low awareness, high friction, or weak incentive | Diagnose in sequence: fix awareness first, then share flow, then landing page, then incentive (optimize mechanics before rewards) |
| Reward redemption below 70% | Reward delivery is delayed or redemption process is complicated | Auto-apply credits immediately, send instant notification, make redemption one-click; show running total in dashboard |
| Referred customers churn faster than organic | Referral incentive attracts low-intent users or onboarding for referred users is inadequate | Shift from cash/discount rewards to product-value rewards (feature unlock, extended trial); add referred-user onboarding path |
| Affiliate partners not producing conversions | Partners lack proper toolkit or audience mismatch | Provide pre-written copy, banner assets, comparison tables, and dedicated landing pages; audit partner audience fit |

---

## Success Criteria

- K-factor reaches 0.3-0.7 range within 90 days of program launch (strong referral contribution without requiring virality)
- Referral CAC is below 50% of other acquisition channel CAC
- Active referrer percentage reaches 5-15% of active users
- Referral-sourced revenue contributes 10-25% of total new revenue within 6 months
- Referred customer LTV exceeds non-referred customer LTV (typical: 16-25% higher per industry data)
- Reward redemption rate exceeds 70% within 30 days of earning
- Double-sided program achieves 2x+ conversion rate compared to single-sided (validate within first 1,000 referrals)

---

## Anti-patterns

| Anti-pattern | Failure mode | Fix |
|--------------|--------------|-----|
| Asking at signup instead of after the aha moment | Referrer has no value experience to share; share rates under 2% | Fire the trigger after activation or milestone — never before value is delivered |
| "Refer a friend" link buried in the account menu | Discovery rate near zero; program appears to "not work" | Surface at trigger moments in-product (modal, banner, post-action), not in settings |
| Single-sided reward where only the referrer benefits | Referred users feel exploited; conversion on referral landing page drops | Use double-sided rewards — both sides get value, aligned with program positioning |
| Reward sized larger than first-payment margin | Program grows but unit economics invert; CAC exceeds LTV | Cap reward at 30% of first payment (or <1 payback period); model before launch with referral_economics_calculator.py |
| Manual reward fulfillment | Delay between referral and reward kills the loop; referrer disengages | Automate reward delivery with in-app notification; trigger within 24 hours of referred user's qualifying event |
| Confusing affiliate program with customer referral | Wrong activation (customers don't behave like affiliates); wrong attribution (affiliates don't behave like advocates) | Decide the program type first using the Referral vs Affiliate Decision table; don't merge |
| Ignoring K-factor, optimizing only for share count | Shares grow but referred conversions don't; false sense of progress | Track K = shares × conversion rate; optimize the weakest stage, not the most visible one |
| Generic monthly "invite friends" email with no trigger | Becomes inbox noise; unsubscribe lift with no conversion lift | Event-triggered emails only — milestone, renewal, support-win, team-growth |
