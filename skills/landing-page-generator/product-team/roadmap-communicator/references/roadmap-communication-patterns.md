# Roadmap Communication Patterns

Reference for the formats and patterns of roadmap communication.

## 1. Pattern catalog

### Now / Next / Later
Most flexible; works for most audiences.

- **Now:** in progress this quarter; commit-level
- **Next:** planned next quarter; plan-level
- **Later:** anticipated 6-12 months; aspire-level

### Themes + commitments
Organize by strategic theme; nested items.

```
Theme: Better collaboration
  - Now: Real-time editing for X
  - Next: @-mentions improvements
  - Later: Multi-org workspaces
Theme: Reliability
  - Now: Reduce P95 latency by 30%
  - ...
```

### Quarterly cadence
Quarter-by-quarter with named initiatives.

- Q1: X, Y
- Q2: Z, W
- Q3: A, B
- Q4: C, D

Risk: looks like dates → looks like commits → over-promise.

### OKR-driven
Roadmap = objectives + key results.

- O: Improve activation by 30%
  - KR1: Reduce time-to-first-value to <5 min
  - KR2: Activation funnel completion >60%

Works internally; less useful externally.

### Strategic-intent narrative
Long-form prose explaining direction without specific commits.

- Best for: vision documents, board strategy
- Worst for: customer-facing comms with specific asks

### Status-tracked initiative list
Initiative by initiative, with current state.

- Initiative 1: 80% complete; on track for May
- Initiative 2: 30% complete; risk on dependency Y
- ...

Works in update / progress contexts; less useful for "what's coming" comms.

## 2. Format pitch: which to use

| Audience | Primary | Secondary |
|----------|---------|-----------|
| Board / exec | Themes + bets + KPIs | Strategic intent narrative |
| Customers | Now / Next / Later (themes) | Strategic intent (vision) |
| Sales | Themes + customer-ask coverage | Now / Next / Later |
| Engineering | Quarterly cadence (specific) | Themes + commitments |
| Partners | API-relevant changes | Breaking-change calendar |
| Internal company | Now / Next / Later + asks | Themes |

## 3. Confidence bands — language for each

### Commit-level
- "We will ship [X] by [date]."
- "Available in [month] for all [segment] customers."
- "Live next sprint."

### Plan-level
- "Plan to ship [X] in [quarter]."
- "Targeting [month]; we'll confirm by [earlier date]."
- "In development; expected [window]."

### Aspire-level
- "Investigating [problem]; no committed date."
- "Exploring [approach]; will share more if it moves to development."
- "On our radar; depends on [dependency]."

### Strategic intent
- "We believe [direction] matters; investing in [area]."
- "Long-term: [vision statement]."

## 4. The right level of detail

Too much detail:
- Specific feature names customers don't recognize
- Internal team names
- Specific dates that aren't commits
- Implementation details

Too little detail:
- Generic themes everyone can claim
- No tie to customer-visible outcome
- No timeline grounding

The right level:
- Outcome-oriented ("you'll be able to X")
- Time-bounded ("this quarter / next quarter / this year")
- Confidence-labeled
- Mapped to a concrete capability

## 5. Communicating changes

When the roadmap changes, communicate explicitly:

### Added
- "We added [X] because [reason]."

### Slipped
- "[X] is moving from [old] to [new] because [reason]. Mitigation: [Y]."

### Removed / killed
- "[X] is no longer in our roadmap because [reason]. We are now focused on [Y]."

### Re-prioritized
- "We're now prioritizing [X] over [Y] because [reason]."

Always give the reason. "We changed our mind" is OK; vague silence isn't.

## 6. Update cadence

| Audience | Cadence | Format |
|----------|---------|--------|
| Customers | Quarterly | Newsletter + community |
| Sales | Monthly | Email + slack |
| Engineering | Bi-weekly | Notion + standup |
| Board | Quarterly | Deck section |
| Public / blog | As-shipped + quarterly | Blog post + status page |

Silence between updates breeds speculation; over-update breeds noise.

## 7. Roadmap as a tool for negotiation

The roadmap is also a tool for the PM to use:

- "We could add X if we cut Y." (forces a trade-off)
- "X depends on Z; if Z slips, X slips." (surfaces dependency)
- "If we want Q3 launch, we need decision on Y by [date]." (forces decision)

A static roadmap loses this leverage; an interactive conversation
preserves it.

## 8. Public roadmap considerations

### Pros
- Customer transparency
- Differentiator from less-open competitors
- Sales-friendly
- Reduces "are you working on X" support tickets

### Cons
- Competitive intelligence (competitors see plans)
- Hard to evolve without explaining (slipped items)
- Sets expectations (legal risk if mis-stated)
- Maintenance burden

### When public works
- Strong PM discipline on confidence bands
- Mature product where roadmap doesn't reveal core strategy
- Customer relationship benefits outweigh competitive cost

Common pattern: themes + high-level commitments public; details internal.

## 9. Roadmap and contractual commitments

Be careful: public roadmap statements can become contractual.

- Add caveats: "Roadmap is aspirational; commitments require contract."
- Don't promise specific features in sales pursuits unless they're committed.
- Customer contracts that reference roadmap items should be reviewed by legal.
- "Roadmap-promised" features that don't ship can trigger lawsuits.

## 10. The "asks" section

Every roadmap update should have asks:

- Decision needed by [exec / board]
- Resource request (headcount, budget)
- Cross-team partnership ask
- Customer input request

A roadmap without asks is just status. A roadmap with asks engages the
audience.

## 11. Common pitfalls

- **One roadmap for all audiences.** Misses everyone.
- **Dates without confidence bands.** Over-promise.
- **Aspire-level items communicated as commits.** Trust erodes.
- **Silent roadmap.** Speculation fills the void.
- **Annual roadmap with no quarterly delta.** Reality changes.
- **Feature names instead of outcomes.** Customers don't recognize them.
- **Roadmap that never gets updated.** Reflects yesterday's strategy.
- **No mechanism for customer / sales input.** Disconnect from market.
