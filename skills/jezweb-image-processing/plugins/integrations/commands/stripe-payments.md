---
description: Add Stripe payments to a web app — checkout, subscriptions, webhooks, billing portal
argument-hint: "[checkout: one-time payment | subscription: recurring billing | webhook: event handler | portal: customer self-service | pricing: pricing page]"
---

Load the `stripe-payments` skill.

Parse $ARGUMENTS for what to build:
- `checkout` — one-time payment via Checkout Sessions
- `subscription` — recurring billing via Checkout Sessions + subscription mode
- `webhook` — webhook handler with signature verification
- `portal` — customer billing portal (manage subscriptions)
- `pricing` — pricing page that reads from Stripe products

Default: ask what they need, or detect from the project (if Stripe is already installed, probably adding a webhook or subscription).

Examples: `/stripe-payments checkout`, `/stripe-payments subscription`, `/stripe-payments webhook`
