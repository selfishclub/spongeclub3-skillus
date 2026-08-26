---
description: Track parcels and check delivery status for Australian couriers
argument-hint: "[tracking-number|store-name]"
---

Load the `parcel-tracking` skill.

If $ARGUMENTS contains a tracking number, identify the carrier and build the tracking link. If it contains a store name, search Gmail for dispatch emails from that store. Otherwise search for all recent dispatch emails.
