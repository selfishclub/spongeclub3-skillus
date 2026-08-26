# WWAS Format Detail, Examples & INVEST Gates

Read this when you need the full Why/What/Acceptance writing rules with good/bad examples, the INVEST quality-gate table, the item template, the worked example, the objective-mapping table, the troubleshooting table, or the success criteria. The SKILL.md keeps only the lean map; the operational detail lives here.

---

## The WWAS Format

Every backlog item has three parts.

### 1. Why (Strategic Context)

1-2 sentences that connect this work item to the team's objectives and business strategy. The Why answers:

- **What business objective does this support?** (e.g., "Reduce churn by 10% in Q2")
- **Why now?** What makes this item timely or important relative to other work?

**The Why is the most important part.** It prevents the team from building features disconnected from strategy. If you cannot articulate the Why, the item should not be in the backlog.

**Good Why examples:**

- "Our Q2 objective is to reduce time-to-value for new users from 14 days to 3 days. Onboarding is the biggest lever -- 60% of churned users never completed setup."
- "Enterprise customers have cited lack of SSO as the top reason for not upgrading. This directly supports our revenue expansion target of $2M ARR growth in H1."
- "Support ticket volume for billing issues increased 40% last quarter. Resolving this frees up 2 support FTEs to focus on onboarding assistance, which supports our activation goal."

**Bad Why examples (avoid):**

- "Because the customer asked for it." (No strategic context)
- "It's a best practice." (No connection to team objectives)
- "We need this for the release." (Circular reasoning)

### 2. What (Description)

A short description of what needs to be built or changed. This section is a **reminder of the discussion, not a detailed specification.**

**Guidelines:**

- 1-2 paragraphs maximum.
- Describe the change at a level that reminds the team of what was discussed during refinement.
- Include a link to the design file if one exists.
- Do not write implementation details, technical specifications, or step-by-step instructions.
- The team should be able to read the What and say "Yes, I remember what we agreed to build."

**Good What examples:**

- "Add a guided setup wizard that walks new users through connecting their data source, inviting a teammate, and creating their first dashboard. The wizard should be skippable and resumable. [Design: Figma link]"
- "Replace the current billing FAQ page with an interactive troubleshooter that guides users through common billing issues (failed payments, plan changes, invoice requests) and resolves 80% of cases without a support ticket."

**Bad What examples (avoid):**

- A multi-page specification with wireframes, API contracts, and database schemas (too detailed -- that belongs in a design doc).
- "Build SSO." (Too vague -- the team cannot recall what was discussed).

### 3. Acceptance Criteria

High-level, observable outcomes that define when the item is done. These are not detailed test cases -- they are the minimum set of conditions that must be true for the item to be accepted.

**Guidelines:**

- 4 or more acceptance criteria per item.
- Each criterion describes an **observable outcome**, not an implementation step.
- Focus on what the user or system should do, not how it is built.
- Include the most important edge cases, but save exhaustive test cases for QA.

**Good acceptance criteria examples:**

1. New users who complete the setup wizard activate within 3 days (measured by creating their first dashboard).
2. The wizard is accessible on mobile and desktop browsers.
3. Users can skip the wizard at any step and resume later from where they left off.
4. Users who skip the wizard can access it again from the help menu.

**Bad acceptance criteria examples (avoid):**

- The API returns a 200 status code with a JSON payload containing... (implementation detail)
- The React component passes all unit tests (internal quality, not user outcome)
- It works on Chrome (too vague; specify what "works" means)

## INVEST Quality Gates

Before a WWAS item enters a sprint, it must pass the INVEST criteria:

| Criterion | Question | Action If Failing |
|-----------|----------|-------------------|
| **Independent** | Can this item be delivered without waiting for another item? | Reorder the backlog or combine dependent items. |
| **Negotiable** | Is the What open to discussion on implementation approach? | Remove implementation prescriptions from the What. |
| **Valuable** | Does the Why connect to a real business objective? | Rewrite the Why or deprioritize the item. |
| **Estimable** | Can the team estimate effort with reasonable confidence? | Add more context to the What or conduct a spike. |
| **Small** | Can this be completed within one sprint? | Split the item (by outcome, by scope, or by user segment). |
| **Testable** | Can the acceptance criteria be verified? | Rewrite criteria to be observable and specific. |

## Item Template

```markdown
### [Title]

**Why:**
[1-2 sentences connecting to strategic objective and explaining why this matters now.]

**What:**
[1-2 paragraphs describing the change. Reminder of the discussion, not a specification.]

[Design: link or "TBD"]

**Acceptance Criteria:**

1. [ ] [Observable outcome]
2. [ ] [Observable outcome]
3. [ ] [Observable outcome]
4. [ ] [Observable outcome]
```

## Worked Example

### Guided Onboarding Wizard

**Why:**
Our Q2 North Star is reducing time-to-value from 14 days to 3 days. User research shows that 60% of churned users never completed the initial setup, and the top reason cited is "I did not know what to do next." A guided onboarding flow directly addresses this by walking users through the critical first steps.

**What:**
Add a step-by-step setup wizard that appears on first login and guides new users through three milestones: connecting a data source, inviting a teammate, and creating their first dashboard. The wizard should be skippable at any point (some users prefer to explore on their own) and resumable if the user leaves before finishing. Each step includes a brief explanation of why it matters and a direct action button.

[Design: figma.com/file/abc123]

**Acceptance Criteria:**

1. [ ] The wizard appears automatically on first login for new users.
2. [ ] Users can skip the wizard at any step and return to it later from the help menu.
3. [ ] Each milestone (data source, teammate, dashboard) can be completed independently and in any order.
4. [ ] Users who complete all three milestones see a completion confirmation with suggested next steps.
5. [ ] The wizard does not appear for existing users who have already completed setup.
6. [ ] The wizard is functional on both desktop and mobile browsers.

## Connecting Why to Business Objectives

The strength of WWAS is the explicit strategic connection. Use this mapping to write strong Why statements:

| Objective Level | Example Objective | Why Framing |
|----------------|-------------------|-------------|
| **Company OKR** | Grow ARR to $10M | "This supports our $10M ARR target by..." |
| **Team OKR** | Reduce churn to <5% monthly | "Our team's Q2 churn target requires..." |
| **Product theme** | Self-serve onboarding | "As part of the self-serve onboarding theme..." |
| **Customer feedback** | Top 3 requested feature | "This is the #1 requested feature from enterprise customers, blocking $500K in pipeline..." |
| **Operational** | Reduce support load | "Support ticket volume for this issue is X/month, costing Y hours..." |

## Troubleshooting

| Problem | Likely Cause | Resolution |
|---------|-------------|------------|
| "Why" statements are generic ("Because the customer asked for it") | PM did not connect the request to a business objective; strategic context unclear | Require every Why to reference a specific OKR, metric, or business case; use the objective-level mapping table in this skill |
| "What" descriptions are either too vague or too detailed | Team unclear on the "reminder of discussion" principle; no refinement session occurred | Run a refinement session before writing the What; enforce the 1-2 paragraph limit; link to design docs for details |
| Acceptance criteria describe implementation steps | Engineering team wrote criteria without user-facing framing | Apply the "would the user care?" filter; rewrite every criterion as an observable outcome; remove API/database references |
| Items consistently fail the INVEST-S (Small) gate | Scope creep during refinement; team reluctant to split items | Practice vertical slicing: split by user segment, by scenario, or by outcome; target items completable in 3-5 days |
| Backlog items lose strategic connection over time | Why statements written once and never revisited; OKRs shift without backlog update | Review backlog alignment quarterly; update or retire items whose Why no longer connects to current objectives |
| Team finds WWAS format overhead compared to simple user stories | Format adds friction without perceived value; team already has strong strategic context | Use WWAS for high-priority items and features; allow simpler formats for bugs and technical tasks; demonstrate value by showing how Why prevents wasted work |
| Acceptance criteria are too few or too shallow | Team rushes through refinement; criteria treated as a checkbox exercise | Set minimum of 4 acceptance criteria per item; include at least 1 edge case and 1 error state criterion |

## Success Criteria

- 100% of feature backlog items include a Why statement referencing a specific business objective or OKR
- What descriptions are 1-2 paragraphs and link to design documentation when applicable
- Every item has at least 4 acceptance criteria focused on observable user outcomes
- All sprint-ready items pass the full INVEST quality gate before entering a sprint
- Stakeholders can read any backlog item's Why and confirm strategic alignment without additional context
- Items written in WWAS format have a 30%+ lower rejection rate at sprint review compared to items without strategic context
- Backlog alignment review occurs at least quarterly, with outdated items retired or updated
