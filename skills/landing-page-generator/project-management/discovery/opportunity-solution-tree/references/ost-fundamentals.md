# OST — Fundamentals Reference

From Teresa Torres' *Continuous Discovery Habits*.

## 1. Why the OST exists

Most product teams jump from problem to solution. The OST forces a
deliberate exploration of multiple opportunities and multiple solutions
before committing.

Common failure mode without OST:
1. Problem identified
2. First solution proposed
3. Solution accepted
4. Build
5. Ship
6. Outcome doesn't move
7. Repeat

The OST surfaces the divergent thinking that prevents step 6.

## 2. The 4 layers

### Layer 1: Outcome
One specific, measurable target.

Discipline:
- ONE outcome per tree (not 3 outcomes)
- Behavioral or business (not output)
- Bounded timebox (this quarter / half)
- Team can influence (not "increase revenue" for an eng team)

### Layer 2: Opportunities
Customer needs, pains, desires.

Discipline:
- Written from customer point of view ("users can't X")
- Grounded in evidence (which interview / ticket / data point?)
- Not solutions
- 3-7 distinct opportunities per outcome (more = ineffective)

### Layer 3: Solutions
Candidate ways to address each opportunity.

Discipline:
- Multiple per opportunity (3-5 ideal)
- Not just one obvious one
- Varied in cost / effort / risk
- Don't promote to roadmap until tested

### Layer 4: Assumption tests
The experiments that validate or invalidate solutions.

Discipline:
- Cheapest test that gives confidence
- Test the riskiest assumption first
- Pre-define success criteria
- Time-bounded

## 3. Outcome examples

### Good outcomes
- "Lift week-1 activation from 28% → 40% by Q3"
- "Reduce admin time-on-task for invoicing from 18min → 8min"
- "Increase free-to-paid conversion in segment X from 4% → 7%"
- "Achieve NPS ≥ 55 from enterprise users (currently 38)"

### Bad outcomes
- "Improve user experience" — vague, unmeasurable
- "Build a new dashboard" — output
- "Hit $50M ARR" — company-level, not team-level
- "Be the best in our market" — aspirational
- "Make customers happy" — undefined

## 4. Opportunity examples

### Good opportunities
- "Trial users abandon during email-verification step (35% drop-off)"
- "Admins want to bulk-invite users from CSV (mentioned in 6 of 8 interviews)"
- "Customer-success teams can't find churn-risk customers fast enough"
- "Enterprise procurement blocks deals without SOC 2 evidence"

### Bad opportunities
- "Need to add CSV import" — solution
- "Users want better dashboard" — too vague
- "Improve email flow" — too vague
- "Customers want AI" — too generic

## 5. Solution examples

For opportunity "Admins want to bulk-invite users from CSV":

### Good solution alternatives
1. CSV upload UI with templated download
2. API endpoint for invite via existing tools (Okta, Workday)
3. Salesforce-style "import wizard" with field mapping
4. Office365/Google Workspace sync (auto-invite based on group)
5. SCIM / directory sync (enterprise-grade)

Each solves the same opportunity differently. Cost, effort, segment fit differ.

### Bad solution
1. "Build a feature for bulk invites"

Single, vague, no exploration.

## 6. Assumption test examples

Solution: "CSV upload UI with templated download"

### Assumption categories
- **Value:** "Admins will actually use this if available"
- **Usability:** "Admins can complete bulk invite in <5 min without help"
- **Feasibility:** "We can build it in 2 weeks"
- **Viability:** "Reduces support tickets, increases activation rate"

### Test the riskiest
Risk + evidence quadrant:
- High risk + low evidence = TEST NOW
- High risk + high evidence = ship; monitor
- Low risk + low evidence = test cheaply
- Low risk + high evidence = no test needed

### Cheap tests
- Value: 5 admin interviews; ask "have you ever wanted to bulk invite? what did you do?"
- Usability: paper prototype with 5 admins
- Feasibility: 1-day eng spike
- Viability: estimate support ticket reduction × admin time saved

## 7. The weekly OST rhythm

Teresa Torres recommends weekly interviews:

### Cadence
- 1+ customer interview per week
- 1 OST update per week (15-30 min team review)
- 1 assumption test in flight at any time
- Quarterly tree refresh (kill stale branches)

### Without weekly rhythm
- OST becomes stale
- Discovery becomes episodic
- Team falls back to feature factory

### Roles
- PM owns the OST
- Designer + engineer collaborate
- Researcher (if you have one) drives interviews
- Whole team reviews weekly

## 8. OST and roadmap

The OST informs the roadmap; the roadmap doesn't replace the OST.

- OST captures: outcome, opportunities, solutions, tests
- Roadmap captures: what we're committing to ship, when, with what risk

Solutions that pass assumption tests → graduated to roadmap.
Solutions still in test → stay in OST.
Solutions that failed tests → killed; opportunities remain (with new candidates).

## 9. Multiple OSTs across a team

A team might have 2-3 OSTs going if working on 2-3 outcomes. More than
3 = trying to do too much.

A company has multiple OSTs across teams, all rolling up to company OKRs.

## 10. Common Torres principles applied

- **Continuous, not episodic.** Discovery happens weekly, not quarterly.
- **Outcomes over outputs.** Measure success by behavior change, not by shipped features.
- **Multiple opportunities, multiple solutions.** Diverge before converging.
- **Test cheaply.** Cheapest test that resolves the highest risk.
- **Whole-team discovery.** PM + designer + engineer all participate.
- **Visualize.** The tree itself is the artifact.

## 11. Tools

Common OST tools:
- Miro / Mural (most popular for the visual layout)
- FigJam
- Whimsical
- Lucidchart
- Notion (text version)
- Spreadsheet (text version)

Tool < discipline. A spreadsheet-OST updated weekly > a Miro masterpiece updated quarterly.

## 12. When the OST gets stuck

### Symptom: no progress in a quarter
- Outcome unclear / unmeasurable
- Solutions chosen without testing
- Tree not updated

**Fix:** Re-check outcome; commit to one assumption test per week.

### Symptom: too many opportunities
- Trying to cover too much
- Outcome is too high-level

**Fix:** Decompose outcome to smaller; pick top 3 opportunities.

### Symptom: keeps coming back to same solution
- Team has bias / pre-decided
- Brainstorm isn't divergent enough

**Fix:** Bring outside perspective. Borrow from analogous problems.

### Symptom: assumption tests aren't run
- "Too busy" — actually means deprioritized
- Tests overdesigned (waiting for perfect)

**Fix:** Time-box test to 1 week max. Cheapest valid test.
