# Spec to Ticket Decomposition

Patterns for translating a PRD or feature brief into a clean ticket tree.

## 1. The decomposition order

A useful order for breaking down a spec:

1. **User-facing capabilities** — what can the user do that they couldn't before?
2. **System surfaces** — which APIs, screens, infra change?
3. **Vertical slices** — smallest user-visible improvement end-to-end
4. **Cross-cutting work** — telemetry, docs, accessibility, security review
5. **Rollout work** — feature flag, canary, monitoring, comms

This order keeps the user value visible. Decomposing by tech layer first
produces strange artifacts ("backend can't ship until frontend ships" or
vice versa).

## 2. The vertical-slice principle

Best ticket: ships a small piece of user value end-to-end.

### Why
- Lets you ship even before the full feature is complete
- Real user feedback informs the next slice
- Fewer "stuck waiting" tickets
- PR is reviewable in isolation

### How
- For each user capability, identify BE + FE + tests + telemetry + docs
- Combine into the ticket if it's a single PR's worth (~200-400 lines)
- Split into 2 tickets if PR would exceed 400 lines (e.g., BE PR + FE PR)
- Use feature flags to ship pieces independently

### When vertical slicing doesn't work
- Major schema migrations (do these standalone, ahead of time)
- Cross-cutting refactors (do these in their own epic)
- Brand-new infrastructure (scaffolding ticket comes first)

## 3. Ticket templates

### Story ticket
```
## User capability
[as a {persona}, I can {action} so that {outcome}]

## Acceptance criteria
- [ ] Criterion 1 (testable)
- [ ] Criterion 2
- [ ] Criterion 3

## Out of scope
- Item 1
- Item 2

## Implementation notes
- [link to design]
- [link to API spec]

## Definition of done
- [ ] Code reviewed + merged
- [ ] Tests added
- [ ] Telemetry events firing in staging
- [ ] Docs updated
- [ ] Feature flag configured (if applicable)
```

### Technical ticket
```
## Goal
[what changes; why]

## Approach
[brief; link to design doc if longer]

## Risks
[what could go wrong]

## Definition of done
- [ ] Implemented
- [ ] Tested
- [ ] Migration runbook (if data changes)
- [ ] Rollback plan
```

### Investigation / spike ticket
```
## Question
[what we need to figure out]

## Deliverable
[a doc, a benchmark, a PoC]

## Timebox
[N days]

## Decision needed
[what we'll decide after the spike]
```

## 4. Common decomposition antipatterns

### "Build the system" mega-ticket
A ticket called "Build notifications system" is not a ticket; it's the epic.

Fix: break into user-visible capabilities (each <3 days).

### Backend-first / frontend-second sequential
"Backend ticket (2 days) blocks frontend ticket (3 days)."

Fix: vertical-slice; use feature flag; or design API first so both can
start in parallel.

### "Cleanup ticket" with no scope
"Clean up notifications code."

Fix: specific changes with acceptance criteria. Or scope it as a spike
that produces a decomposition.

### Ticket sized by guess
"This is medium." Without a breakdown, "medium" is wishful thinking.

Fix: bullet the steps; estimate per step; sum + 30% buffer.

### Hidden dependency
"Just need the data team to add a column."

Fix: cross-team dependencies become their own tickets with explicit
coordination. Surface in decomposition, not at sprint planning.

## 5. The "T-shirt size" trap

S/M/L/XL is useful in early estimation but rots without grounding:

- S in your team = how many engineer-days?
- L in your team = how many engineer-days?
- Don't redefine these silently — calibrate quarterly

Better than nothing; not a substitute for breaking down to engineer-days
when uncertainty is high.

## 6. Acceptance criteria — how specific?

Specific enough that an engineer can implement without asking the PM 5 questions.

### Good acceptance criterion
"When a user mutes a channel, no notifications from that channel reach
the user (push, email, in-app) for the duration of the mute period.
Sender sees no indication that the recipient muted."

### Weak acceptance criterion
"Users can mute notifications." (Mute what? For how long? Visible to whom?)

### Acceptance vs detailed design
Acceptance describes the user-visible behavior; the design doc describes
HOW. Don't bury implementation in acceptance criteria; don't bury
user-visible behavior in design.

## 7. Edge cases — surface them upfront

For each ticket, list at least 3 edge cases:
- Empty state
- Error state (timeout, server error, validation error)
- Concurrent action
- Permission edge case
- Localization (text expansion, RTL)
- Accessibility (screen reader, large text, no mouse)

Surfaced edge cases become acceptance criteria; unsurfaced edge cases
become production bugs.

## 8. Telemetry as a first-class deliverable

Every ticket that adds behavior should specify the telemetry:

- What events fire?
- What properties are captured?
- What dashboard / alert is updated?
- How will success be measured?

Skip this and you'll discover, at launch + 7 days, that you can't measure
the impact.

## 9. Tests as a first-class deliverable

For each ticket, specify the tests required:

- Unit (what units; what edge cases)
- Integration (which boundaries)
- E2E (which user journeys)
- Visual regression (if UI)
- Performance (if perf-sensitive)
- Security (if auth / data sensitive)
- Accessibility (if UI)

"We'll add tests later" usually means "we'll add them never."

## 10. Documentation as a first-class deliverable

Per ticket, specify the docs that need updating:

- User-facing docs (help center, in-product)
- API docs (if API changes)
- Internal runbooks (if operational changes)
- Architecture docs (if design changes meaningful)
- Onboarding for new engineers (if new system)

Docs that ship with the code stay accurate. Docs that ship later don't.

## 11. The PRD-to-tickets workshop

A useful 60-90 min session before sprint planning:

### Roles
- PM + lead engineer + designer + tester

### Agenda
1. PM walks through the spec (15 min)
2. Engineer asks clarifying questions (15 min)
3. Designer walks through interactions (10 min)
4. Group decomposes into tickets on a whiteboard (30 min)
5. Group identifies risks + dependencies (10 min)
6. Group commits to definition of done (10 min)

Output:
- Ticket tree in the tracker
- Definition-of-done checklist
- Risk + dependency list
- Estimated rough effort

## 12. Common pitfalls

- **Decomposition that ignores the team's real velocity.** Plan for the team you have.
- **Tickets that don't include tests / docs / telemetry.** They never get done.
- **Cross-team work as a single ticket.** Make the handoff a ticket itself.
- **Acceptance criteria that aren't testable.** "Users like it" isn't.
- **Edge cases discovered in QA.** Surface in decomposition.
- **No rollout plan for risky changes.** Surprise launches surprise on-call.
- **One big PR for the entire feature.** Split.
