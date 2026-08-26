# Webhooks — Idempotent Event Handling

Read this when building or auditing the Stripe webhook endpoint. This is the most critical code in your billing system — get signature verification, idempotency, and retry safety right.

## Webhook Handler (Idempotent)

This is the most critical code in your billing system. Get this right.

```typescript
// app/api/webhooks/stripe/route.ts
import { NextResponse } from "next/server";
import { headers } from "next/headers";
import { stripe } from "@/lib/stripe";
import { db } from "@/lib/db";
import type Stripe from "stripe";

// Idempotency: track processed events to handle Stripe retries
async function isProcessed(eventId: string): Promise<boolean> {
  return !!(await db.stripeEvent.findUnique({ where: { id: eventId } }));
}

async function markProcessed(eventId: string, type: string) {
  await db.stripeEvent.create({
    data: { id: eventId, type, processedAt: new Date() },
  });
}

export async function POST(req: Request) {
  const body = await req.text();
  const signature = headers().get("stripe-signature");

  if (!signature) {
    return NextResponse.json({ error: "Missing signature" }, { status: 400 });
  }

  // Step 1: Verify webhook signature
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(
      body, signature, process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    console.error("Webhook signature verification failed:", err);
    return NextResponse.json({ error: "Invalid signature" }, { status: 400 });
  }

  // Step 2: Idempotency check
  if (await isProcessed(event.id)) {
    return NextResponse.json({ received: true, deduplicated: true });
  }

  // Step 3: Handle events
  try {
    switch (event.type) {
      case "checkout.session.completed":
        await handleCheckoutCompleted(event.data.object as Stripe.Checkout.Session);
        break;
      case "customer.subscription.created":
      case "customer.subscription.updated":
        await handleSubscriptionChange(event.data.object as Stripe.Subscription);
        break;
      case "customer.subscription.deleted":
        await handleSubscriptionDeleted(event.data.object as Stripe.Subscription);
        break;
      case "invoice.payment_succeeded":
        await handlePaymentSucceeded(event.data.object as Stripe.Invoice);
        break;
      case "invoice.payment_failed":
        await handlePaymentFailed(event.data.object as Stripe.Invoice);
        break;
      case "customer.subscription.trial_will_end":
        await handleTrialEnding(event.data.object as Stripe.Subscription);
        break;
      default:
        // Log unhandled events for monitoring
        console.log(`Unhandled webhook: ${event.type}`);
    }

    await markProcessed(event.id, event.type);
    return NextResponse.json({ received: true });
  } catch (err) {
    console.error(`Webhook processing failed [${event.type}]:`, err);
    // Return 500 so Stripe retries. Do NOT mark as processed.
    return NextResponse.json({ error: "Processing failed" }, { status: 500 });
  }
}

// --- Handler implementations ---

async function handleCheckoutCompleted(session: Stripe.Checkout.Session) {
  if (session.mode !== "subscription") return;

  const userId = session.metadata?.userId;
  if (!userId) throw new Error("Missing userId in checkout metadata");

  // Always re-fetch from Stripe API -- event data may be stale
  const subscription = await stripe.subscriptions.retrieve(
    session.subscription as string
  );

  await db.user.update({
    where: { id: userId },
    data: {
      stripeCustomerId: session.customer as string,
      stripeSubscriptionId: subscription.id,
      stripePriceId: subscription.items.data[0].price.id,
      stripeCurrentPeriodEnd: new Date(subscription.current_period_end * 1000),
      subscriptionStatus: subscription.status,
      hasHadTrial: true,
    },
  });
}

async function handleSubscriptionChange(subscription: Stripe.Subscription) {
  // Find user by subscription ID first, fall back to customer ID
  const user = await db.user.findFirst({
    where: {
      OR: [
        { stripeSubscriptionId: subscription.id },
        { stripeCustomerId: subscription.customer as string },
      ],
    },
  });
  if (!user) {
    console.warn(`No user for subscription ${subscription.id}`);
    return;  // Don't throw -- this may be a subscription we don't manage
  }

  await db.user.update({
    where: { id: user.id },
    data: {
      stripeSubscriptionId: subscription.id,
      stripePriceId: subscription.items.data[0].price.id,
      stripeCurrentPeriodEnd: new Date(subscription.current_period_end * 1000),
      subscriptionStatus: subscription.status,
      cancelAtPeriodEnd: subscription.cancel_at_period_end,
    },
  });
}

async function handleSubscriptionDeleted(subscription: Stripe.Subscription) {
  await db.user.updateMany({
    where: { stripeSubscriptionId: subscription.id },
    data: {
      subscriptionStatus: "canceled",
      stripePriceId: null,
      stripeCurrentPeriodEnd: null,
      cancelAtPeriodEnd: false,
    },
  });
}

async function handlePaymentSucceeded(invoice: Stripe.Invoice) {
  if (!invoice.subscription) return;

  await db.user.updateMany({
    where: { stripeSubscriptionId: invoice.subscription as string },
    data: {
      subscriptionStatus: "active",
      stripeCurrentPeriodEnd: new Date(invoice.period_end * 1000),
    },
  });
}

async function handlePaymentFailed(invoice: Stripe.Invoice) {
  if (!invoice.subscription) return;

  await db.user.updateMany({
    where: { stripeSubscriptionId: invoice.subscription as string },
    data: { subscriptionStatus: "past_due" },
  });

  // Dunning: send appropriate email based on attempt count
  const attemptCount = invoice.attempt_count || 1;
  if (attemptCount === 1) {
    // First failure: gentle reminder
    await sendDunningEmail(invoice.customer_email!, "first_failure");
  } else if (attemptCount === 2) {
    // Second failure: more urgent
    await sendDunningEmail(invoice.customer_email!, "second_failure");
  } else if (attemptCount >= 3) {
    // Final failure: last chance before cancellation
    await sendDunningEmail(invoice.customer_email!, "final_notice");
  }
}

async function handleTrialEnding(subscription: Stripe.Subscription) {
  // Stripe sends this 3 days before trial ends
  const user = await db.user.findFirst({
    where: { stripeSubscriptionId: subscription.id },
  });
  if (user?.email) {
    await sendTrialEndingEmail(user.email, subscription.trial_end!);
  }
}
```
