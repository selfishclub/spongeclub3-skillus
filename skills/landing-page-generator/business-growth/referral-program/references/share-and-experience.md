# Share Mechanics, Referred User Experience & Copy

Read this when building the sharing flow, the referred-user landing experience, and the program copy set (in-app prompts, emails, share messages).

## Share Mechanics

### Share Channel Priority

| Channel | B2C Priority | B2B Priority | Implementation |
|---------|-------------|-------------|----------------|
| Email invite | High | Highest | Pre-filled email with referral link |
| Copy link | High | High | One-click copy with confirmation |
| Twitter/X | High | Medium | Pre-filled tweet with referral link |
| LinkedIn | Low | High | Pre-filled post with referral link |
| WhatsApp | High | Low | Deep link to WhatsApp with message |
| Slack/Teams | Low | High | Integration or copyable message |
| SMS | Medium (mobile) | Low | Pre-filled text message |

### Share Message Templates

**Email (B2B):**
```
Subject: I think you'd like [Product]

Hey [Name],

I've been using [Product] for [task/workflow] and it's saved me [specific benefit].
Thought you might find it useful too.

Here's my referral link -- you'll get [referred benefit] when you sign up:
[Referral Link]

[Referrer Name]
```

**Social (B2C):**
```
Been using [Product] for [timeframe] and I'm genuinely impressed.
[Specific thing I love about it].

If you want to try it, use my link and we both get [reward]:
[Referral Link]
```

---

## Referred User Experience

### Referral Landing Page

```
┌──────────────────────────────────────────┐
│  [Referrer Name] invited you to          │
│  [Product]                               │
│                                          │
│  [Referrer's photo if available]         │
│                                          │
│  Your reward: [Incentive details]        │
│                                          │
│  [Sign Up and Claim Your Reward]         │
│                                          │
│  What [Product] does:                    │
│  - Benefit 1                            │
│  - Benefit 2                            │
│  - Benefit 3                            │
│                                          │
│  "Quote from a customer"                │
└──────────────────────────────────────────┘
```

### Attribution Rules

| Scenario | Attribution |
|----------|-----------|
| User clicks link and signs up same session | Attributed to referrer |
| User clicks link, returns 3 days later, signs up | Attributed (30-day cookie) |
| User clicks link but signs up via Google search | Attributed if within cookie window |
| User receives two referral links from different people | First click wins (or last click -- choose one rule) |
| Referred user was already a lead in CRM | Exclude from referral program |

---

## Program Copy Templates

### In-App Prompt

```
Know someone who'd love [Product]?

Give [reward], Get [reward]

Share your unique link and you'll both get [reward] when they sign up.

[Share Now]  [Learn More]
```

### Referral Dashboard

```
Your Referral Stats

Referrals Sent: [N]
Friends Joined: [N]
Rewards Earned: $[X]

[Share Your Link]

Your link: [referral-url]  [Copy]

Progress to next reward:
[Progress bar: 2 of 3 referrals for Silver tier]
```

### Referral Email (Post-Activation)

```
Subject: Share [Product] and earn [reward]

Hi [Name],

Glad you're enjoying [Product]!

Share your personal referral link with colleagues, and you'll both get [reward]:

[Referral Link]

So far, you've earned $[X] from [N] referrals.

[Share Now]
```
