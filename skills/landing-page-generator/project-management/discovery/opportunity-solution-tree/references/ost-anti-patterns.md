# OST — Anti-Patterns + Fixes

## A1 — Outcome = output
**Symptom:** "Outcome: ship the new dashboard."

**Fix:** Outcomes are behaviors / metrics that change. Recast:
- Was: "ship dashboard"
- Now: "lift admin task efficiency 30%; current 18 min → target 12 min"

## A2 — Opportunities are solutions
**Symptom:** "Opportunity: add bulk CSV import."

**Fix:** Rewrite as customer pain/need:
- Was: "add bulk CSV import"
- Now: "admins want to invite many users without 1-by-1 effort (6 of 8 interviews)"

## A3 — Single solution per opportunity
**Symptom:** Each opportunity has one solution; team's first idea wins.

**Fix:** Force 3+ alternatives. Constraints:
- "What if we couldn't build CSV upload?"
- "How do enterprise tools solve this?"
- "What's the lazy / hacky approach?"

## A4 — No assumption tests
**Symptom:** Solutions listed but no test plan.

**Fix:** Per top solution:
- Value test (5 interviews)
- Usability test (prototype with 5 users)
- Time-box: 1 week

## A5 — Static tree
**Symptom:** OST created in Q1, untouched in Q3.

**Fix:** Weekly 15-min review. Add: new interview insights; recent test results.
Move: validated solutions to roadmap; failed solutions to graveyard.

## A6 — Tree built without customer input
**Symptom:** Opportunities are PM's guesses; no interview evidence cited.

**Fix:** Require evidence per opportunity (interview / ticket / data link).
If no evidence, run interviews first.

## A7 — Too many opportunities
**Symptom:** 15+ opportunities under one outcome.

**Fix:** Cluster + prioritize. Top 5; rest goes to backlog.

## A8 — One huge outcome
**Symptom:** Outcome = "improve product experience"

**Fix:** Decompose to specific metric + segment + window.
- Was: "improve product experience"
- Now: "lift mobile app retention from D7 16% → D7 22% in segment X by Q3"

## A9 — Tree without roadmap link
**Symptom:** OST exists; roadmap exists; they don't reference each other.

**Fix:** Roadmap items must link back to OST solutions. Solutions on roadmap
must have passed assumption tests.

## A10 — Hidden bias
**Symptom:** Solutions list contains the PM's pre-chosen favorite + 2 obvious losers.

**Fix:** External challenger (engineer / designer / outside team) red-teams
the tree. Force genuinely viable alternatives.

## Worked example — strong vs weak OST

### Weak

```
Outcome: improve onboarding
  Opportunity: users need better onboarding
    Solution: redesign onboarding flow
      Test: ship and see
```

Vague outcome. Opportunity = solution. Single solution. No real test.

### Strong

```
Outcome: lift week-1 activation rate from 28% → 40% by Q3

Opportunity 1: Trial users drop off at email-verification (35%)
  (Evidence: funnel data + 4 interview quotes "I forgot to come back")
  
  Solutions:
  S1: Skip email verification; require at first save
    Test: A/B 50/50, measure W1 activation + abuse rate
  S2: Magic link instead of verification code
    Test: 1-week eng spike; prototype with 10 trials
  S3: SSO-first signup
    Test: 5 interviews — is this what they want?

Opportunity 2: First-experience confusion ("I don't know what to do")
  (Evidence: 6 interview transcripts; support tickets in onboarding tag)
  
  Solutions:
  S4: In-product checklist
    Test: prototype with 5 users; time-on-task
  S5: Personalized welcome based on signup source
    Test: 5 interviews to validate desire
  S6: Interactive demo with sample data
    Test: 1-week feasibility spike

Opportunity 3: No "aha moment" reaches user in week 1
  (Evidence: behavioral analytics — users who hit "aha" event activate 3.5x)
  
  Solutions:
  S7: Surface the "aha" event in onboarding flow
    Test: low-fi prototype; 5 user tests
  S8: Email drip sequence pushing to "aha" event
    Test: A/B 50/50, measure CTR + activation
  S9: In-product nudge after Y minutes inactivity
    Test: low-fi mock + 5 interviews
```

Strong example characteristics:
- Specific measurable outcome
- 3 opportunities (not too many)
- Each opportunity has evidence
- 3 solutions per opportunity
- Each solution has a cheap test
- Tests vary in cost

## OST review checklist

Before declaring an OST workable:

- [ ] Outcome: 1, specific, measurable, behavioral, bounded
- [ ] Opportunities: 3-7, written as customer needs (not solutions)
- [ ] Opportunities have evidence cited
- [ ] Each top opportunity has 3+ solutions
- [ ] Each top solution has 1+ assumption test designed
- [ ] Tests are time-bounded (1-2 weeks max for cheap tests)
- [ ] Tests have success criteria
- [ ] Weekly review scheduled
- [ ] Linked to roadmap (committed solutions only)
- [ ] Graveyard exists (failed solutions don't reappear)
