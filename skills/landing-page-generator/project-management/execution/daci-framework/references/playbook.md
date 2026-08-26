# DACI Framework Playbook

> Read this when building or running a DACI chart: role definitions and rules, the 7-step build sequence (working group → roles → decisions → current-state → pain points → target-state → transition plan), governance health metrics, troubleshooting, and success criteria.

## DACI Role Definitions

| Role | Symbol | Definition | Rules |
|---|---|---|---|
| **Driver** | D | The person driving the decision to closure. Responsible for process, timeline, and ensuring a decision gets made. | Exactly one per decision. |
| **Approver** | A | The person(s) with authority to approve or veto. Their sign-off is required. | 1-2 maximum per decision. |
| **Contributor** | C | People who provide input, expertise, or implementation effort. Their input shapes the decision but they don't have veto power. | As many as needed. |
| **Informed** | I | People who are notified of the decision outcome. Not part of the decision-making process. | As many as needed. |

### Key DACI Principles

1. **Every decision has exactly one Driver.** If two people are driving, nobody is driving.
2. **Approvers have veto power.** Limit to 1-2 to avoid gridlock.
3. **Contributors influence but don't block.** Their input is valued but the Driver decides how to use it.
4. **Informed means notified, not consulted.** Don't confuse notification with input.
5. **DACI is about decisions, not tasks.** Map decisions, not work items.

## Building a DACI Chart

### Step 1: Identify the Working Group

Define the team, business unit, or cross-functional group this DACI covers.

### Step 2: List Job Titles / Roles

Enumerate all roles involved in product decisions. Common roles:

- Executive Management
- Product Manager
- Product Owner
- Engineering Lead
- UX / Design Lead
- Product Marketing
- Scrum Master
- Sales & Marketing
- Customer Support / Professional Services
- Legal / Compliance

### Step 3: Define Decisions

List the key decisions this group makes. Common product decisions:

| Decision | Description |
|---|---|
| What problem are we solving? | Problem definition and validation |
| Who is the primary user? | Persona and segment selection |
| What is the product vision? | Long-term direction and strategy |
| What is the value proposition? | Differentiation and positioning |
| What are the JTBD? | Jobs-to-be-done identification |
| What goes into the backlog? | Story selection and prioritization |
| What is the release plan? | Timing, scope, and sequencing |
| What experiments to run? | Discovery and validation activities |
| How is the product built? | Architecture and technical decisions |
| How is the product delivered? | Deployment and rollout strategy |
| What data do we collect? | Analytics and instrumentation |
| How do we price the product? | Pricing model and strategy |
| What is the GTM strategy? | Go-to-market planning |

### Step 4: Build Current-State DACI

Map how decisions are made **today** (not how you want them to be made):

| Decision | Exec Mgmt | PM | PO | Eng Lead | Design | Marketing | Support | Legal |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Problem definition | A | D | C | C | C | I | C | |
| User/segment selection | I | D | C | | C | A | C | |
| Product vision | A | D | C | C | C | I | | |
| Value proposition | I | D | | | C | A | | |
| Backlog priorities | I | A | D | C | C | | | |
| Release plan | I | A | D | C | | I | I | |
| Experiments | | D | C | C | C | | | |
| Architecture | I | C | | D | | | | A |
| Pricing | A | C | | | | D | | C |
| GTM strategy | A | C | | | | D | C | I |

**Rules:**
- Each row has exactly one `D`.
- Each row has 1-2 `A` maximum.
- Use `D`, `A`, `C`, `I`, or blank only.
- Add Notes column for non-obvious assignments.

### Step 5: Identify Pain Points

From the current-state chart, identify common failure patterns:

| Failure Pattern | Symptom | Business Impact |
|---|---|---|
| **No Driver** | Decision stalls for weeks | Missed market windows |
| **Too many Approvers** | Endless review cycles | Slow time-to-market |
| **Driver lacks authority** | Decision made but not respected | Rework and confusion |
| **Informed treated as Approver** | Late objections derail decisions | Scope creep and delays |
| **Missing Contributors** | Decisions made without key input | Poor outcomes, rework |

### Step 6: Design Target-State DACI

Based on pain points, redesign decision ownership:

- Ensure every row has exactly one D.
- Reduce Approvers to 1-2 per decision.
- Move chronic blockers from A to C or I.
- Add missing Contributors.
- Document changes in Notes column.

### Step 7: Create Transition Plan

| Timeframe | Action |
|---|---|
| **First 30 days** | Align on first 3 high-impact decision changes; communicate new roles |
| **60 days** | Expand to all decisions; run first decision under new DACI |
| **90 days** | Full adoption; retrospective on decision speed and quality |

## DACI Health Metrics

Track these metrics to monitor governance effectiveness:

| Metric | Target | How to Measure |
|---|---|---|
| Decision cycle time | <5 business days for P0 decisions | Time from decision identified to resolved |
| Decision reversal rate | <10% | Decisions overturned within 30 days |
| Stakeholder satisfaction | >80% | Survey: "Do you know who makes decision X?" |
| Escalation rate | <15% | Decisions escalated past intended Approver |
| Decision coverage | 100% | All recurring decisions have a DACI row |

## Integration with Other Skills

- Use `create-prd/` to document decisions made via DACI in PRD Section 2 (Contacts).
- Use `identify-assumptions/` to surface assumptions about decision authority.
- Use `brainstorm-okrs/` to align DACI decisions with quarterly objectives.
- Use `summarize-meeting/` to capture decision outcomes in meeting notes.

## Troubleshooting

| Problem | Likely Cause | Resolution |
|---|---|---|
| Decisions still stall after DACI rollout | Driver lacks confidence or authority in practice | Coach Drivers on decision-making process; ensure Approvers respect the framework |
| Everyone is marked as Contributor | Team avoids accountability by defaulting to C | Force each person to commit to D, A, C, or I -- no "everyone contributes" |
| DACI chart exists but nobody references it | Document not integrated into workflows | Post DACI in team Confluence/Notion; reference it in kickoff meetings |
| Approvers overrule without explanation | Authority without accountability | Require Approvers to document veto rationale; review in retrospectives |
| New decisions not added to chart | DACI treated as one-time exercise | Review and update DACI quarterly; add new decisions as they emerge |

## Success Criteria

- 100% of recurring product decisions have a DACI row with exactly one Driver
- Decision cycle time reduced by 30%+ after DACI implementation
- <10% of decisions reversed within 30 days of being made
- >80% of team members can identify the Driver for any given decision
- DACI chart reviewed and updated at least quarterly
