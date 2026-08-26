# Status Update Structure & Workflow

Read this when you need the full definition of each of the six sections, the traffic-light rules and anti-patterns, the SBNR shorthand mapping, or the step-by-step authoring workflow.

## The status update structure

Every update produced by this skill has the same six sections, in this order. Consistency is the point -- exec readers should be able to scan to the section they care about in under 5 seconds.

### Section 1: Header

- **Period**: the date range covered (e.g., "Week of 2026-05-18")
- **Project / team**: the name of the team or initiative
- **Author**: the PM or engineering lead
- **Status (R / Y / G)**: the single overall traffic-light verdict
- **Status rationale**: one sentence explaining why this color

### Section 2: Highlights

Three to five bullet points describing the most important things that shipped, decided, or moved this week. Highlights are **outcome-led**: name what changed for the user or the business, not the activity.

**Bad:** "Shipped PR-1234"
**Good:** "Search latency dropped from 480ms p95 to 210ms p95 after the index rebuild (PR-1234)"

Each highlight should pass the **"so what?" test**: a busy exec who reads only this bullet should understand why it matters.

### Section 3: Blockers

Things currently stopping the team. Each blocker has three parts:

- **What is blocked**: the work item or workstream
- **Who/what is blocking**: the team, vendor, decision, or dependency
- **What we need**: a specific ask or decision

A blocker without a specific ask is a complaint, not a blocker. Promote it to Risks or strike it.

### Section 4: Risks

Things that could become blockers if we do not act. Each risk follows the format:

`<Risk> -- Likelihood (H/M/L) x Impact (H/M/L) -- Mitigation: <action> -- Owner: <name> -- Due: <date>`

This is the format used by `senior-pm/risk_matrix_analyzer.py` so risks can be lifted directly into the portfolio risk register.

### Section 5: Asks

Specific decisions, approvals, resources, or introductions needed from the audience. Each ask names:

- **What you want**
- **By when**
- **From whom**
- **Consequence of delay**

An update without an "Asks" section trains readers that updates require no action. Always include the section, even if the answer is "none this week."

### Section 6: What's Next

The 3-5 most important things planned for the coming week. Same outcome-led style as Highlights. This is the closing read -- it sets expectations for next week's update.

## Traffic-light status (R / Y / G)

| Color | Definition | Rule |
|-------|------------|------|
| **Green** | On track. No active blockers; risks are manageable; commitments will be met. | Use sparingly. Two consecutive Green updates with no new highlights is suspicious. |
| **Yellow** | At risk. There is an issue, but the team has a credible mitigation in flight. | The Risks section must name the mitigation, the owner, and the deadline. |
| **Red** | Off track. Intervention from leadership is required. | A Red update requires an explicit Ask. Red without an Ask means the PM has not done their job. |

### Anti-patterns

- **Watermelon status** -- Green outside, Red inside. The most common failure. Surface the bad news in the rationale sentence.
- **Always-Yellow** -- if every update is Yellow, the team has not made the decision to commit (Green) or to escalate (Red).
- **Color creep** -- the bar for Red should not move week to week. Document the criteria in the team wiki.

## SBNR shorthand

Some teams use SBNR (Status / Blockers / Next / Risks) as a compressed version for daily or async standup. SBNR maps to this skill's sections as follows:

| SBNR field | Section in this skill |
|------------|----------------------|
| **S**tatus | Section 1 (Header) + Section 2 (Highlights) |
| **B**lockers | Section 3 (Blockers) |
| **N**ext | Section 6 (What's Next) |
| **R**isks | Section 4 (Risks) |

The Asks section is unique to the weekly executive variant -- daily SBNR typically does not include explicit asks.

## Workflow

1. **Export ticket data.** Pull from Jira (via JQL or the Atlassian MCP), Linear (via GraphQL or the Linear MCP), or any source that can emit JSON matching the input schema (see Tool Reference).
2. **Augment with narrative.** The PM adds 1-2 sentences of context to each highlight that goes beyond what the ticket title says.
3. **Run `status_generator.py`.** Use `--input status_data.json --format markdown` to render the update. Use `--format confluence` or `--format notion` to push directly to a wiki.
4. **Set the traffic-light status.** This is a human judgment, not a calculation. Document the rationale.
5. **Distribute.** Send via the agreed channel. Always include the Asks section, even if "none this week."
6. **Archive.** Save dated copies. The weekly archive becomes the monthly packet and the quarterly retrospective input.
