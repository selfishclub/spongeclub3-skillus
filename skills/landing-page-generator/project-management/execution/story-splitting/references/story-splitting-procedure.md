# Story Splitting Procedure

> Read this when you are actually splitting a story: vertical vs horizontal slicing, the 9 canonical patterns with before/after examples, the top-down decision tree, the optional tenth pattern, the step-by-step workflow, an end-to-end worked example, troubleshooting, and success criteria. (For the deepest pattern-by-pattern catalog with multiple examples, see `splitting-patterns-guide.md`.)

## Vertical vs Horizontal Slicing

A common anti-pattern is to split stories by technical layer:

```
Story: Build search.
Split into:
  - Story A: Database schema for search index
  - Story B: API endpoint for search
  - Story C: UI for search results
```

This is **horizontal slicing**. Each slice is not shippable to users, none provides value alone, and you cannot demo any until all three are done.

**Vertical slicing** crosses every layer for a thin slice of functionality:

```
Story: Build search.
Split into:
  - Story A: Search by exact name match (DB + API + UI for one query type)
  - Story B: Search with autocomplete suggestions (extends UI + API + DB)
  - Story C: Search across multiple fields (broadens query type)
```

Each story is independently demoable and releasable. This is the goal.

## The 9 Canonical Splitting Patterns (Lawrence)

Richard Lawrence's 2009-2012 work on story splitting (the "Story Splitting Flowchart") identifies nine patterns that cover the vast majority of real splits. Try them in roughly this order.

### Pattern 1: Workflow Steps

If a story covers a multi-step workflow, split by step. Ship one step at a time.

**Before:** *"As a user, I want to onboard so I can use the product."*

**After:**
1. Confirm email (step 1)
2. Connect data source (step 2)
3. Invite teammates (step 3)
4. Create first dashboard (step 4)

Ship each step alone behind a feature flag or progressive disclosure.

### Pattern 2: Business Rule Variations

If a story embeds multiple business rules, split by rule. Ship the most common rule first.

**Before:** *"As an admin, I want to apply discounts to orders."*

**After:**
1. Flat-percent discount (most common case)
2. Buy-one-get-one
3. Tiered volume discount
4. Coupon-code discount with expiration

### Pattern 3: Happy / Unhappy Path

If a story includes both success and failure handling, split. Ship the happy path first; add unhappy path slices.

**Before:** *"As a user, I want to upload a CSV with full error handling."*

**After:**
1. Upload a valid CSV up to 10 MB (happy path)
2. Reject and explain invalid file types
3. Reject and explain CSVs that exceed size
4. Reject and explain malformed rows with line-numbered errors

### Pattern 4: Input/Output Variations (Interface Options)

If a story supports multiple input methods or output formats, split by variation.

**Before:** *"As a user, I want to export reports."*

**After:**
1. Export to CSV
2. Export to PDF
3. Schedule recurring export to email
4. Export via API

### Pattern 5: Data Variations

If a story handles multiple data types or sources, split.

**Before:** *"As a user, I want to connect a data source."*

**After:**
1. Connect Postgres
2. Connect MySQL
3. Connect Snowflake
4. Upload static CSV file

### Pattern 6: Data Entry Methods

If a story offers multiple ways to enter the same data, split by method.

**Before:** *"As a user, I want to add contacts to my CRM."*

**After:**
1. Manual single-contact entry
2. Bulk paste from spreadsheet
3. Import from CSV
4. Sync from email integration

### Pattern 7: Deferred Performance / Quality

If a story includes both functional behavior and performance/quality requirements, split. Ship working-but-slow first; add a performance slice.

**Before:** *"As a user, I want to load my dashboard in under 1 second."*

**After:**
1. Load my dashboard with any performance (functional baseline)
2. Optimize dashboard load to under 3 seconds (acceptable)
3. Optimize dashboard load to under 1 second (target)

The deferred-quality split is among the most useful and most underused. Most teams confuse "shipping at quality" with "shipping each story at final quality" -- they are not the same thing.

### Pattern 8: Operations (CRUD)

If a story implies multiple operations on the same entity, split by operation. Ship the most-needed operation first.

**Before:** *"As a user, I want to manage my saved searches."*

**After:**
1. View my saved searches (Read)
2. Save a new search (Create)
3. Delete a saved search (Delete)
4. Rename a saved search (Update)

The order is intentional: Read first (no risk of bad data); Create next (now there is data to interact with); Delete before Update (deletes are easier and unblocks user accidents); Update last.

### Pattern 9: Break Out a Spike

If the story carries enough technical uncertainty that the team cannot estimate or split it, the *first* slice is a timeboxed spike (research, prototype, proof-of-concept). The spike's output is enough learning to apply Patterns 1-8 to the rest.

**Before:** *"As a user, I want to authenticate with my company's SSO."*

**After:**
1. **Spike (2 days):** Investigate which SAML libraries we can use, test against our top 3 customer IdPs.
2. Authenticate via Okta (most common customer IdP)
3. Authenticate via Azure AD
4. Authenticate via Google Workspace

Spikes are not user-facing; they exist to enable subsequent vertical slices.

## The Splitting Decision Tree

When a story feels too big, walk this tree top-down. The first pattern that applies is the one to use. Most stories can be split by more than one; pick the one that produces the most usable first slice.

```
Is there enough technical certainty to plan?
  NO  -> Pattern 9 (Spike)
  YES -> continue

Does the story span multiple workflow steps?
  YES -> Pattern 1 (Workflow Steps)
  NO  -> continue

Does the story embed multiple business rules?
  YES -> Pattern 2 (Business Rule Variations)
  NO  -> continue

Does the story include happy + unhappy paths?
  YES -> Pattern 3 (Happy / Unhappy Path)
  NO  -> continue

Does the story support multiple input/output options?
  YES -> Pattern 4 (Input/Output Variations)
  NO  -> continue

Does the story handle multiple data types or sources?
  YES -> Pattern 5 (Data Variations)
  NO  -> continue

Does the story offer multiple entry methods for the same data?
  YES -> Pattern 6 (Data Entry Methods)
  NO  -> continue

Does the story include performance/quality requirements?
  YES -> Pattern 7 (Deferred Performance / Quality)
  NO  -> continue

Does the story imply multiple CRUD operations?
  YES -> Pattern 8 (Operations CRUD)
  NO  -> The story is probably actually small. Re-estimate.
```

## A Tenth Pattern (Optional): Major Effort First

Lawrence sometimes adds a tenth "Major Effort" pattern: ship the first instance of an expensive thing (which absorbs the setup cost), then ship the cheaper subsequent instances as separate stories. Example: build the first integration (which establishes the integration framework), then add each subsequent integration as a small story. Useful when the first story's effort is dominated by infrastructure setup.

## Workflow

1. **Identify the story to split.** Either it failed INVEST-S (Small), exceeded 85th-percentile cycle time, or "felt huge" in refinement.
2. **State the user value.** The original story expressed in one sentence. If you cannot state user value, the story needs problem framing, not splitting (see `create-prd/`).
3. **Walk the decision tree.** Stop at the first pattern that applies.
4. **Draft the slices.** Each slice is a user story in `wwas/` or `job-stories/` format.
5. **Verify each slice is vertical.** Each slice must cross all required layers and be independently demoable.
6. **Order the slices.** First slice = most user value with least effort. Subsequent slices add capability.
7. **Run INVEST check.** Each slice passes I-N-V-E-S-T (see `wwas/`).
8. **Update the backlog.** Replace the original story with the ordered slice list. Archive the original.

## Worked Example (End-to-End)

### Original Story

*"As a customer, I want to manage my subscription so that I can change my plan, pay, and cancel without contacting support."*

This story is too big. It has multiple operations (manage), multiple business rules (plan tiers, proration), input variations (payment methods), and happy/unhappy paths (failed payments).

### Walk the Tree

- Pattern 8 (Operations CRUD): clearly applicable -- view, change, pay, cancel.
- Pattern 2 (Business Rules): also applicable -- proration rules, downgrade vs upgrade.
- Pattern 3 (Happy/Unhappy): applicable -- payment failure handling.

Start with Pattern 8 to get the overall shape; apply Patterns 2 and 3 to the slices that need further splitting.

### After Splitting

1. **View my current subscription** (Read; happy path; no business rules)
2. **Cancel my subscription, effective end of period** (simplest write; one business rule)
3. **Upgrade my plan with immediate proration** (most common change)
4. **Downgrade my plan, effective end of period** (deferred downgrade rule)
5. **Update my payment method** (input variation: card vs bank vs invoice)
6. **Retry a failed payment** (unhappy path; recover existing customers)
7. **Cancel scheduled cancellation** (edge case; ship after the rest)

Each slice is independently shippable. The customer sees value at each step (slice 1 alone removes the support ticket "what plan am I on?"). The team can ship slice 1 in week 1, ship slice 2 in week 2, and so on.

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Splits all look like "build the back-end, then build the front-end" | Horizontal slicing; layers instead of behavior | Re-split using a Lawrence pattern; each slice must cross all layers |
| First slice is enormous; subsequent slices are tiny | Team treated the first slice as "everything that doesn't fit later" | Re-order; the first slice should be the smallest end-to-end value |
| Slices can only ship together | Slices are not actually independent; horizontal disguised as vertical | Apply Pattern 7 (deferred quality) or Pattern 3 (happy path only) to find an actually shippable first slice |
| Refinement takes 90+ minutes per story | Splitting attempted in the meeting, not before | Pre-split the largest 2-3 stories before refinement; use refinement to validate, not to discover |
| Spike (Pattern 9) becomes a black hole | Spike not timeboxed; outcome not defined | Spikes are 2-3 days max, with a written outcome statement ("at the end, we will know X") |
| Splits violate INVEST-V (Valuable) | Splitting too aggressively; slices no longer demonstrably valuable | Each slice must answer "what is the user payoff after this slice ships?"; if you can't answer, recombine |
| Same story splits the same way every time | Pattern fatigue; team converging on one comfortable pattern | Force a different pattern this time; review whether the convergence reflects real recurrence or laziness |

## Success Criteria

- Every story that fails INVEST-S gets split before sprint planning, not during.
- Each split slice is independently shippable and demoable to users.
- Slices are vertical (cross all layers), not horizontal (layer-by-layer).
- Each slice has a one-sentence statement of user value.
- The first slice in an ordered split is the smallest possible end-to-end value, not "everything that doesn't fit later."
- Spikes (Pattern 9) are timeboxed to 2-3 days with a written outcome statement.
- Team converges on a shared vocabulary of patterns; refinement conversations reference patterns by number.
