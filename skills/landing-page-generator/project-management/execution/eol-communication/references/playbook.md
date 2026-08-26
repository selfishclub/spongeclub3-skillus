# EOL Communication Playbook

> Read this when crafting a sunset announcement: the 4-phase EOL framework (planning → message → segment & distribute → support & monitor), the messaging template and writing rules, segment/channel matrix, internal support FAQ, monitoring checklist, timeline best practices, troubleshooting, and success criteria.

## EOL Communication Framework

### Phase 1: Pre-Announcement Planning

Before writing any communication, answer these questions:

| Question | Answer Required |
|---|---|
| What is being discontinued? | Specific product, feature, or service name |
| What is the replacement path? | Alternative product, migration path, or "none" |
| Why is this happening? | Honest reason framed around customer benefit |
| Who is affected? | Customer segments and estimated count |
| What is the timeline? | Key dates (announcement, deprecation, final shutdown) |
| What support is available? | Migration tools, documentation, customer success resources |
| What are the risks? | High-value accounts, contractual obligations, regulatory requirements |

### Phase 2: Craft the EOL Message

#### EOL Messaging Template

```markdown
## Product Transition Narrative

**We are**: [Company and relationship to the product being phased out]
- [Commitment to customers]
- [Product evolution context]
- [Future vision]

**Announcing**: [Single clear sentence stating EOL and introducing replacement]

**Because**:
- [Reason focused on customer benefit 1]
- [Reason focused on customer benefit 2]
- [Reason focused on customer benefit 3]

**Which means for you**: [Customer-centered impact and benefit summary]

## Current Product Context

**[Product name]**
- is a [brief description and primary function]
- that has served [target customer] for [timeframe]
- by providing [key benefits]

## Customer Impact

**We understand this may affect you by:**
- [Impact 1 -- be honest about inconvenience]
- [Impact 2 -- acknowledge disruption]
- [Impact 3 -- recognize switching costs]

## Transition Solution

**For** [affected customers]
- that currently use [discontinued product],
- [replacement product]
- is a [product category]
- that [benefit statement focused on continuity and improvements].

## Differentiation and Continuity

- Like [discontinued product], [replacement] provides [continuity of key benefits]
- While also offering [new benefits that justify the transition]

## Support and Next Steps

**To ensure a smooth transition, we will:**
- [Support measure 1 -- e.g., free migration tool]
- [Support measure 2 -- e.g., dedicated migration support team]
- [Support measure 3 -- e.g., extended parallel operation period]

## Timeline

| Date | Milestone |
|---|---|
| [Date 1] | Announcement and migration tools available |
| [Date 2] | New sign-ups disabled; existing users continue |
| [Date 3] | Feature freeze on old product |
| [Date 4] | Final data export deadline |
| [Date 5] | Product shutdown |

## Call to Action

- [Clear next step for customers]
- [Contact information for questions]
- [Link to migration guide]
```

### Writing Rules

1. **Lead with empathy, not defensiveness.** Acknowledge the disruption honestly.
2. **Focus on customer continuity.** Explain what stays the same, then what improves.
3. **Be specific about dates.** Vague timelines ("coming months") create anxiety.
4. **Provide concrete support.** Tools, documentation, and human help.
5. **Avoid corporate euphemisms.** "Sunsetting" and "streamlining" feel dishonest. Say "discontinuing" or "replacing."
6. **One clear call to action.** Don't overwhelm with options.

### Phase 3: Segment and Distribute

Different customer segments need different messages:

| Segment | Message Emphasis | Channel |
|---|---|---|
| Enterprise / High-value | Personal outreach, dedicated migration support, contract review | Direct email from account manager, followed by call |
| SMB / Mid-market | Self-serve migration tools, clear documentation | Email + in-app notification |
| Free / Low-tier | Simple transition guide, automated migration | Email + blog post |
| Developers / API users | Technical migration guide, deprecation timeline, SDK updates | Developer email list + docs site + changelog |

### Phase 4: Support and Monitor

#### Internal FAQ for Support Teams

Prepare your support team with answers to likely objections:

| Customer Objection | Recommended Response |
|---|---|
| "I don't want to switch" | Acknowledge frustration; emphasize what stays the same; offer migration help |
| "I need more time" | Explain timeline flexibility if any; offer extended access if possible |
| "The replacement doesn't have feature X" | Document the gap; provide workaround or roadmap commitment |
| "I want a refund" | Follow refund policy; escalate if needed; preserve relationship |
| "Why wasn't I consulted?" | Explain decision process; invite feedback on replacement |

#### Monitoring Checklist

- [ ] Track migration rate weekly (target: 80%+ by shutdown date)
- [ ] Monitor support ticket volume related to EOL
- [ ] Track churn across entire portfolio (not just EOL product)
- [ ] Monitor social media and community forums for sentiment
- [ ] Escalation path for high-risk accounts clear and documented

## EOL Timeline Best Practices

| Product Type | Minimum Notice Period | Recommended |
|---|---|---|
| Free product / feature | 30 days | 60 days |
| Paid product (monthly) | 60 days | 90 days |
| Paid product (annual) | End of contract term | 6+ months |
| Enterprise / API | 12 months | 18 months |
| Regulated industry | Per regulatory requirement | 12+ months |

## Integration with Other Skills

- Use `create-prd/` to document the replacement product requirements.
- Use `release-notes/` to communicate the final updates to the old product.
- Use `summarize-meeting/` to document EOL decision meetings.
- Use `senior-pm/` stakeholder mapping for high-risk account identification.

## Troubleshooting

| Problem | Likely Cause | Resolution |
|---|---|---|
| Customer backlash on social media | Message too corporate; lacked empathy | Rewrite with customer-first language; acknowledge impact honestly |
| Low migration rate | Migration path too complex or unclear | Simplify migration tools; offer hands-on support; extend timeline |
| Support team overwhelmed | FAQ not prepared; team not trained on responses | Conduct support team briefing before announcement; provide response scripts |
| Enterprise customers threaten legal action | Contractual obligations not reviewed | Involve Legal before announcement; honor contract terms |
| Replacement product not ready | EOL announced before replacement was production-ready | Delay EOL timeline; run products in parallel until replacement is stable |
| Internal teams learn about EOL from customers | Communication leaked before internal alignment | Brief internal teams 1-2 weeks before external announcement |

## Success Criteria

- EOL message reviewed by Legal, Support, and Customer Success before publication
- 80%+ of affected customers migrated before shutdown date
- Support ticket volume related to EOL decreases week-over-week after announcement
- No increase in churn for non-EOL products (brand trust preserved)
- Zero contractual violations during EOL process
- Post-EOL retrospective conducted within 30 days of shutdown
