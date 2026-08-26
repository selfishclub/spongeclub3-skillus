---
description: Audit and generate in-app user guidance — onboarding, empty states, tours, help content
argument-hint: "[audit: find gaps | generate: produce code | both: audit then generate]"
---

Load the `onboarding-ux` skill.

Parse $ARGUMENTS for:
- **Mode**: `audit` (find gaps only), `generate` (produce content/code), `both` (audit then generate). Default: both
- **URL**: app to audit. If not provided, check for deployed URL or running dev server.

Examples: `/onboarding-ux both https://lmi.flared.au`, `/onboarding-ux audit`, `/onboarding-ux generate`
