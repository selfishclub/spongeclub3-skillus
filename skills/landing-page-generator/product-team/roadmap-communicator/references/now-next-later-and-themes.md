# Now / Next / Later and Themes

Reference for the two most-useful structural patterns in roadmap
communication.

## 1. Now / Next / Later — the workhorse

### When to use
- Most external-facing comms
- Most internal-facing comms
- When you want flexibility without being vague

### Structure

#### Now
- In progress this quarter
- Confidence: commit (with caveats)
- Audience expectation: "Will arrive soon"

#### Next
- Planned for the following 1-2 quarters
- Confidence: plan (will probably ship; not yet final)
- Audience expectation: "We're planning to do this"

#### Later
- Anticipated for 2-4 quarters out
- Confidence: aspire (direction, not commit)
- Audience expectation: "Exploring; let us know what you think"

### Why it works
- Confidence implied by position (no need to label every item)
- Audience knows what to depend on
- Flexible at the back; firm at the front

### What to avoid
- Putting aspire items in "Now"
- Vague "later" items that never move forward
- No items in "Next" (creates a cliff)

## 2. Themes — the strategic frame

### What a theme is
A strategic intent that organizes multiple initiatives under a single
banner.

Good themes:
- "Better collaboration" (clear, customer-language)
- "Faster onboarding" (outcome-oriented)
- "Enterprise readiness" (segment-targeted)
- "Reliability + scale" (operational)

Bad themes:
- "Improving the product" (everyone's theme)
- "Engineering excellence" (internal-only)
- "Notifications" (a feature, not a theme)

### Why themes work
- Audience can react to themes ("yes, that matters" / "no, focus on X instead")
- Themes survive feature pivots
- Themes ladder to KPIs

### How many themes
- 3-5 strategic themes per quarter / year
- Below 3: too narrow; above 5: too diffuse
- Each theme has 2-5 initiatives

### Theme refresh cadence
- Quarterly review (still relevant?)
- Annual rewrite (themes evolve with strategy)
- Don't refresh more than quarterly (audience fatigue)

## 3. Combining: themes + now/next/later

The most robust pattern:

```
Theme A: Better collaboration
  Now: Real-time editing
  Now: @-mention improvements
  Next: Workspaces for cross-org work
  Later: Mobile collaboration parity

Theme B: Faster onboarding
  Now: New welcome flow
  Next: Auto-import from competitors
  Later: AI-assisted setup

Theme C: Reliability + scale
  Now: 99.95% SLA on core API
  Next: Multi-region failover
  Later: Active-active across regions
```

This combines strategic clarity (themes) with time-bounded confidence
(now/next/later).

## 4. The strategic intent layer

Beyond themes, sometimes you need a layer that's even further out:

- **Strategic intent:** "We believe X matters" — direction
- **Theme:** "Better collaboration" — area of investment
- **Initiative:** "Real-time editing" — specific bet
- **Feature:** "WebSocket-based cursor sharing" — implementation

Pick the right altitude per audience:
- Board: strategic intent + theme
- Customer: theme + initiative
- Sales: initiative + feature (with talk track)
- Engineering: initiative + feature + ticket

## 5. Themes as KPI containers

Each theme should be tied to a KPI it moves:

- Theme: "Better collaboration" → KPI: WAU/MAU + multi-user usage rate
- Theme: "Faster onboarding" → KPI: time-to-first-value, activation rate
- Theme: "Reliability + scale" → KPI: uptime, P95 latency

If a theme has no associated KPI, it's decoration.

## 6. Initiative sizing within themes

For each theme, distribute investment across:

- **Sustaining (~50%):** improvements to existing capabilities
- **Differentiating (~35%):** new capabilities that move the theme
- **Transforming (~15%):** ambitious bets within the theme

Heavy sustain = stuck; heavy transform = fragile.

## 7. Anti-themes (counter-positioning)

Sometimes the most useful framing is what you're NOT doing.

- "We are not building [feature competitors have]."
- "We're not optimizing for [segment]."
- "We won't compete on [dimension] because [reason]."

Explicit anti-themes clarify strategy and reduce internal debate.

## 8. The roadmap "spine"

A useful artifact: a single 1-pager that lives across communication
formats. The spine has:

- Themes (3-5)
- For each theme: top 1-3 initiatives + status
- KPI per theme
- Open question or risk

Format-adapt for each audience; the spine doesn't change.

## 9. When themes change

Don't change themes lightly. When you do:

- Communicate explicitly: "We are sunsetting [theme] and investing in [theme]"
- Explain why: market signal, learning, strategic shift
- Map prior initiatives to the new theme structure (or kill them honestly)

Frequent theme changes signal lack of strategy; rare theme changes
signal confidence.

## 10. Audience expectations and confidence

| Audience | Reads "Now" as | Reads "Next" as | Reads "Later" as |
|----------|----------------|-----------------|------------------|
| Customer | "Will arrive soon" | "Planning" | "Exploring" |
| Sales | "Sellable now" | "Sellable with caveats" | "Don't pitch yet" |
| Engineering | "Sprint commit" | "Quarterly commit" | "Capacity planning input" |
| Board | "Current quarter" | "Following quarter" | "Strategic direction" |

Same labels; different mental models. Format-adapt the language.

## 11. Common pitfalls

- **Themes that are just feature names.** Themes are strategic.
- **No themes — just a feature list.** No strategic frame.
- **15 themes.** No focus.
- **Themes don't tie to KPIs.** Decoration.
- **Now / Next / Later with everything in "Later".** No real commitment.
- **Aspire items in "Now".** Over-promise.
- **No anti-themes.** Internal debate continues indefinitely.
- **Theme changes every quarter.** Strategy is reactive, not directional.
