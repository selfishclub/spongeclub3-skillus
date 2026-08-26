# Audience-Specific Roadmap Formats

Templates and patterns for each common roadmap audience.

## 1. Board / executive roadmap section

### Structure (1 page)
```
[Title: Product roadmap — Q3 2026]

## Strategic bets (3-5)
1. Theme 1 — bet, KPI moved, status
2. Theme 2 — bet, KPI moved, status
...

## Recently shipped (last quarter)
- Initiative 1 — outcome metric moved
- Initiative 2 — outcome metric moved

## Shipping next quarter
- Initiative A — confidence (commit/plan)
- Initiative B — confidence

## Strategic risks
- Risk 1 — mitigation
- Risk 2 — mitigation

## Asks of the board
- [Specific ask]
```

### Tone
- Tight, structured, business-outcome-oriented
- Don't drown in features
- Surface risks honestly

### Common mistakes
- Listing every shipped feature
- Hiding misses
- No tie to business KPIs

## 2. Customer / public roadmap

### Structure
```
[Title: What's coming in Acme]

## Now shipping
- [Feature] — what it means for you
- ...

## In development
- [Capability theme] — expected this quarter
- ...

## Exploring
- [Area] — we're investigating; no committed date
- ...

## Recently launched
- [Recent feature] — link to docs / changelog

[Footer: We update this monthly. Have a request? Email roadmap@acme.com.]
```

### Tone
- Outcome-language, not feature-name language
- "You'll be able to X" not "We're adding Y"
- Confidence-labeled
- Inviting feedback

### What NOT to include
- Internal team names
- Specific commit-level dates beyond the immediate quarter
- Aspire items as if they're committed
- Competitive positioning

## 3. Sales-facing roadmap

### Structure (2-3 pages)
```
## Strategic themes (this quarter)
1. Theme 1: why customers care
   - Confirmed: features, target dates
   - In dev: themes, expected timing
   - Coming: directions

## Customer-ask coverage
- Top 10 sales-requested features
  - [feature] — status, owner, ETA, talk track

## Competitive positioning
- Win themes (where we're moving fastest)
- Defensive themes (where competitors are pressing)

## Recently shipped
- [Feature] — talk track, customer impact
- [Feature] — talk track, customer impact

## What to NOT promise
- [Feature] — under exploration; do not commit to customers
- [Feature] — confidence too low for sales commitment

## Asks of sales
- Surface deals blocked by [missing capability]
- Help prioritize [area X vs area Y]
```

### Tone
- Action-oriented (talk tracks)
- Honest about what's not committed
- Practical (date estimates, even loose)

## 4. Engineering roadmap

### Structure
```
## Quarterly themes
- Theme 1: [outcome metric we're moving]
  - Q3 commits (specific features + dates)
  - Q3 stretch
- Theme 2: ...

## Cross-team dependencies
- [Capability] depends on [team Y] for [thing]
- Need decision by [date] from [team Z]

## Resource asks
- Hire roles for [skills]
- Budget for [tooling]

## Open technical decisions
- [Decision] — owner, decision needed by [date]

## Reliability + tech debt allocation
- [Project] — % of capacity
- [Project] — % of capacity
```

### Tone
- Specific commits (engineering can't ship vagueness)
- Surface dependencies early
- Tie themes to outcome metrics
- Honest about what's at risk

## 5. Internal company-wide roadmap

### Structure
```
## What we're building (and why)
- Theme 1: [outcome] — [business reason]
- Theme 2: [outcome] — [business reason]

## What we shipped (last update)
- [Initiative] — what's different now

## What's coming (this quarter)
- [Initiative] — expected timing

## How you can help
- [Department X]: please [specific ask]
- All: please [feedback request]
```

### Tone
- Inclusive (everyone has a stake)
- Honest about what's hard
- Specific asks per department

## 6. Partner / integrator roadmap

### Structure
```
## API changes (this quarter)
- New endpoints
- Deprecated endpoints (with sunset dates)
- Breaking changes (with migration path + dates)

## SDK roadmap
- Version X.Y release notes
- Version X.Z+1 expected timing

## Webhook / event changes
- New events
- Schema changes

## Partner program updates
- Tiering changes
- Co-marketing opportunities
- Certification updates

## Documentation
- New docs published
- Docs improvement roadmap
```

### Tone
- Technical, specific
- Breaking changes flagged early (60-90 day notice minimum)
- Migration paths concrete

## 7. Investor-facing roadmap (when fundraising)

### Structure (in deck)
- Slide: "Where we are"
- Slide: "Where we're going" (themes + bets)
- Slide: "Year 1-2 outcomes" (concrete revenue / product milestones)
- Slide: "Strategic risks + mitigations"
- Slide: "Why now"

### Tone
- Strategic, not tactical
- Ambitious but defensible
- Risks acknowledged

## 8. Customer-specific roadmap (key accounts)

For QBR / EBR with named accounts:

### Structure
- Their must-haves (status)
- Their nice-to-haves (status)
- Themes affecting their domain
- Asks of the customer (input, beta, reference)

### Tone
- Personalized
- Honest about misses
- Engage them as a partner

## 9. Translation between formats

The same roadmap content in different formats:

### Internal commit
> "PROJ-1234: Implement WebSocket-based real-time editing for files;
> target ship May 15; behind FEATURE_COLLAB_RT flag; rollout to 1% on
> May 16, ramp to 100% by May 31."

### Sales talk track
> "Real-time collaborative editing is shipping this May. We're rolling
> out gradually starting mid-May, full availability by June 1. Tell us
> if your customers want early access."

### Customer announcement
> "Real-time editing is coming! Multiple people can edit the same file
> simultaneously, see each other's cursors, and resolve conflicts
> automatically. Available to all customers in June 2026."

### Board summary
> "Collaboration theme: real-time editing shipping in Q2. Targets +5pt
> NRR lift in Mid-Market segment based on usage drivers."

Same fact; different audience-appropriate language.

## 10. Common pitfalls

- **One format for all audiences.** Misses the point.
- **Engineering jargon in customer comms.** Confuses, doesn't inform.
- **Customer-friendly themes in eng comms.** Engineers need specifics.
- **Same roadmap from board pack and customer blog.** Mismatch in detail level.
- **No mechanism to update roadmap as it changes.** Stale roadmap loses trust.
- **Roadmap = wishlist.** Audience can't tell what's real.
