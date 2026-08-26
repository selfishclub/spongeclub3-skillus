# Testing & Troubleshooting

Read this when testing the integration locally with the Stripe CLI, reviewing against common pitfalls, diagnosing a billing bug, or validating against success criteria before shipping.

## Testing with Stripe CLI

```bash
# Install and authenticate
brew install stripe/stripe-cli/stripe
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Trigger specific events
stripe trigger checkout.session.completed
stripe trigger customer.subscription.updated
stripe trigger invoice.payment_failed
stripe trigger customer.subscription.trial_will_end

# Test card numbers
# Success:               4242 4242 4242 4242
# Requires 3D Secure:    4000 0025 0000 3155
# Declined:              4000 0000 0000 0002
# Insufficient funds:    4000 0000 0000 9995
# Expired card:          4000 0000 0000 0069

# View recent events
stripe events list --limit 10

# Inspect a specific event
stripe events retrieve evt_xxx
```

---

## Common Pitfalls

| Pitfall | Consequence | Prevention |
|---------|-------------|------------|
| Trusting webhook event data | Stale data, race conditions | Always re-fetch from Stripe API in handlers |
| No idempotency on webhooks | Double-charges, duplicate records | Track processed event IDs in database |
| Missing metadata on checkout | Cannot link subscription to user | Always pass `userId` in metadata |
| Proration surprises | Users charged unexpected amounts | Always preview proration before upgrade |
| Not handling `past_due` | Users lose access without warning | Implement dunning emails on payment failure |
| Skipping trial abuse prevention | Users create multiple accounts for free trials | Store `hasHadTrial: true`, check on checkout |
| Customer Portal not configured | Portal returns blank page | Enable features in Stripe Dashboard first |
| Webhook endpoint not idempotent | Stripe retries cause duplicate processing | Idempotency table with event ID dedup |
| Not pinning API version | Breaking changes on Stripe updates | Pin `apiVersion` in client constructor |
| Ignoring `trial_will_end` event | Users surprised when trial ends | Send reminder email 3 days before |

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Webhook returns 400 on all events | Webhook signing secret mismatch between environments | Verify `STRIPE_WEBHOOK_SECRET` matches the endpoint in Stripe Dashboard; use `stripe listen` output secret for local dev |
| Checkout session redirects to blank page | `success_url` or `cancel_url` missing `{CHECKOUT_SESSION_ID}` template or pointing to wrong domain | Ensure URLs use `APP_URL` env var and include the session ID template literal for retrieval |
| Subscription shows `incomplete` status | First payment requires 3D Secure but was never completed | Handle `checkout.session.async_payment_failed` and send the customer a link to complete authentication |
| Proration invoice charges full price instead of difference | Using `create_prorations` instead of `always_invoice` or not passing existing subscription item ID | Use `always_invoice` proration behavior and update the existing `items[0].id` rather than adding a new line item |
| Usage records return "Cannot create usage record" | Reporting usage on a non-metered price or after subscription cancellation | Confirm the price uses `recurring.usage_type: "metered"` and the subscription is active before reporting |
| Customer Portal shows no options | Portal configuration not enabled in Stripe Dashboard | Navigate to Stripe Dashboard > Settings > Billing > Customer Portal and enable subscription management features |
| Duplicate webhook processing despite idempotency table | `markProcessed` called before handler completes, then handler throws on retry | Move `markProcessed` to after the handler succeeds (as shown in the webhook handler pattern above) |

---

## Success Criteria

- **Webhook reliability:** 99.9%+ webhook processing success rate with zero duplicate side effects over a 30-day window
- **Checkout conversion:** End-to-end checkout flow completes in under 3 seconds (redirect to Stripe and back)
- **Idempotency coverage:** 100% of webhook handlers are idempotent, verified by replaying the same event ID twice with no state change on the second pass
- **Subscription state accuracy:** Database subscription status matches Stripe source of truth within 60 seconds of any state change
- **SCA compliance:** All European payment flows pass 3D Secure challenges without manual intervention or dropped transactions
- **Dunning recovery:** Automated dunning emails recover at least 30% of failed payments within the retry window (typically 7-21 days)
- **Zero hardcoded price IDs:** All Stripe price IDs are sourced from environment variables, enabling test/production parity without code changes
