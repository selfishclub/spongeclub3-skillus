# Confluence Templates Library

Read this when you need a ready-to-use Confluence page template. Copy the block, replace the bracketed placeholders, and adjust macros for your space.

### 1. Meeting Notes Template
```markdown
---
**Meeting Title**: [Meeting Name]
**Date**: {date:format=dd MMM yyyy}
**Time**: [Time]
**Attendees**: @user1, @user2, @user3
**Facilitator**: @facilitator
**Note Taker**: @notetaker
---

{info}
**Quick Links**:
- [Previous Meeting](link)
- [Project Page](link)
- [Jira Board](link)
{info}

## Agenda
1. [Topic 1] - [Duration] - [Owner]
2. [Topic 2] - [Duration] - [Owner]
3. [Topic 3] - [Duration] - [Owner]

## Discussion & Notes

### [Topic 1]
**Presenter**: @owner
**Discussion**:
- Key point 1
- Key point 2

**Decisions Made**:
{panel:title=Decision|borderColor=#00875a}
[Decision description]
**Decided by**: @decisionmaker
{panel}

### [Topic 2]
[Continue pattern]

## Action Items
{tasks}
- [ ] [Action item 1] - @owner - Due: [Date]
- [ ] [Action item 2] - @owner - Due: [Date]
- [ ] [Action item 3] - @owner - Due: [Date]
{tasks}

## Parking Lot
{note}
Topics to discuss in future meetings:
- [Deferred topic 1]
- [Deferred topic 2]
{note}

## Next Meeting
**Date**: [Next meeting date]
**Focus**: [Next meeting focus areas]
```

### 2. Project Charter Template
```markdown
{panel:title=Project Overview|borderColor=#0052cc}
**Project Name**: [Project Name]
**Project Code**: [PROJ]
**Status**: {status:colour=Blue|title=Planning}
**Owner**: @projectowner
**Sponsor**: @sponsor
**Start Date**: [DD/MM/YYYY]
**Target End Date**: [DD/MM/YYYY]
{panel}

## Executive Summary
[2-3 paragraphs summarizing the project purpose, scope, and expected outcomes]

## Business Case

### Problem Statement
[Describe the problem or opportunity]

### Objectives
1. [SMART Objective 1]
2. [SMART Objective 2]
3. [SMART Objective 3]

### Success Criteria
{info}
**Definition of Success**:
- [Measurable outcome 1]
- [Measurable outcome 2]
- [Measurable outcome 3]
{info}

## Scope

### In Scope
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3]

### Out of Scope
- [Explicitly excluded item 1]
- [Explicitly excluded item 2]

## Stakeholders

| Name | Role | Responsibility | Influence |
|------|------|----------------|-----------|
| @user1 | Sponsor | Funding & approval | High |
| @user2 | PM | Day-to-day management | High |
| @user3 | Tech Lead | Technical direction | Medium |

**RACI Matrix**: [Link to detailed RACI]

## Timeline & Milestones

{timeline}
| Phase | Start | End | Deliverables |
|-------|-------|-----|--------------|
| Discovery | DD/MM | DD/MM | Requirements doc |
| Design | DD/MM | DD/MM | Design specs |
| Development | DD/MM | DD/MM | MVP |
| Testing | DD/MM | DD/MM | Test report |
| Launch | DD/MM | DD/MM | Production release |
{timeline}

## Budget
**Total Budget**: $XXX,XXX

| Category | Estimated Cost | Notes |
|----------|----------------|-------|
| Personnel | $XX,XXX | FTE allocation |
| Software/Tools | $XX,XXX | Licenses & subscriptions |
| External Services | $XX,XXX | Contractors, vendors |
| Contingency (10%) | $X,XXX | Risk buffer |

## Risks & Assumptions

### Top Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| [Risk 1] | Medium | High | [Mitigation strategy] |
| [Risk 2] | Low | High | [Mitigation strategy] |

### Assumptions
- [Critical assumption 1]
- [Critical assumption 2]

## Resources & Links
- [Jira Project](#)
- [Confluence Space](#)
- [Design Files](#)
- [Technical Docs](#)
```

### 3. Sprint Retrospective Template
```markdown
{panel:title=Sprint Retrospective|borderColor=#00875a}
**Sprint**: Sprint [Number]
**Sprint Dates**: [Start Date] - [End Date]
**Team**: [Team Name]
**Facilitator**: @facilitator
**Date**: {date}
{panel}

## Sprint Overview
**Sprint Goal**: [Sprint goal]
**Completed Stories**: [X/Y]
**Velocity**: [XX points]
**Carry Over**: [X stories]

## Ceremony: What Went Well? 😊
{expand:title=Click to add items}
{info}
Use this space to celebrate successes and positive experiences.
{info}

- [Positive item 1]
- [Positive item 2]
- [Positive item 3]
{expand}

## Ceremony: What Didn't Go Well? 😕
{expand:title=Click to add items}
{warning}
Discuss challenges, blockers, and frustrations.
{warning}

- [Challenge 1]
- [Challenge 2]
- [Challenge 3]
{expand}

## Ceremony: Ideas & Actions 💡
{expand:title=Click to add items}
{note}
Brainstorm improvements and define actionable next steps.
{note}

| Idea | Votes | Action Owner | Target Sprint |
|------|-------|--------------|---------------|
| [Improvement idea 1] | ⭐⭐⭐ | @owner | Sprint X+1 |
| [Improvement idea 2] | ⭐⭐ | @owner | Sprint X+2 |
{expand}

## Action Items (Committed)
{tasks}
- [ ] [Action 1 - High Priority] - @owner - Due: [Date]
- [ ] [Action 2 - Medium Priority] - @owner - Due: [Date]
- [ ] [Action 3 - Low Priority] - @owner - Due: [Date]
{tasks}

## Action Items from Previous Retro - Status Check
{panel:title=Previous Action Items}
| Action | Owner | Status | Notes |
|--------|-------|--------|-------|
| [Previous action 1] | @owner | {status:colour=Green|title=Done} | [Completion notes] |
| [Previous action 2] | @owner | {status:colour=Yellow|title=In Progress} | [Progress notes] |
{panel}

## Team Mood
{info}
Use emojis or numeric scale (1-10) to capture team sentiment.
{info}

**Overall Sprint Mood**: [😊 😐 😕]
**Team Energy**: [X/10]

## Next Retro
**Date**: [Next retro date]
**Focus**: [Special focus if any]
```

### 4. Product Requirements Document (PRD) Template
```markdown
{panel:title=PRD Overview|borderColor=#0052cc}
**Feature Name**: [Feature Name]
**PRD ID**: PRD-XXX
**Author**: @author
**Status**: {status:colour=Blue|title=Draft}
**Last Updated**: {date}
**Epic Link**: {jira:Epic Key}
{panel}

## Problem Statement
[Describe the user problem or business need. Answer: What problem are we solving and for whom?]

## Goals & Success Metrics

### Goals
1. [Primary goal]
2. [Secondary goal]

### Success Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| [Metric 1] | [Target value] | [How to measure] |
| [Metric 2] | [Target value] | [How to measure] |

## User Stories & Use Cases

### Primary User Story
**As a** [user type]
**I want** [capability]
**So that** [benefit]

**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### Use Cases
1. **Use Case 1**: [Scenario name]
   - **Actor**: [User role]
   - **Preconditions**: [What must be true]
   - **Flow**: [Step-by-step]
   - **Postconditions**: [End state]

## Requirements

### Functional Requirements
| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-1 | [Requirement description] | Must Have | |
| FR-2 | [Requirement description] | Should Have | |
| FR-3 | [Requirement description] | Nice to Have | |

### Non-Functional Requirements
| ID | Requirement | Target | Notes |
|----|-------------|--------|-------|
| NFR-1 | Performance | <2s load time | |
| NFR-2 | Scalability | 10K concurrent users | |
| NFR-3 | Availability | 99.9% uptime | |

## Design & User Experience

### User Flow
[Insert diagram or link to design files]

### Wireframes/Mockups
[Embed images or link to Figma]

### UI Specifications
- [Key UI element 1]
- [Key UI element 2]

## Technical Considerations

### Architecture
[High-level architecture overview or diagram]

### Dependencies
- [System dependency 1]
- [Service dependency 2]
- [Third-party integration]

### Technical Constraints
- [Constraint 1]
- [Constraint 2]

## Release Plan

### Phases
| Phase | Features | Target Date | Status |
|-------|----------|-------------|--------|
| MVP (v1.0) | [Core features] | [Date] | {status:colour=Blue|title=Planned} |
| v1.1 | [Additional features] | [Date] | {status:colour=Gray|title=Future} |

### Rollout Strategy
[Describe rollout approach: beta, phased, full launch]

## Open Questions
{warning}
- [ ] [Question 1 requiring resolution]
- [ ] [Question 2 requiring resolution]
{warning}

## Appendix
- [Related Documents](#)
- [Research & Data](#)
- [Competitive Analysis](#)
```

### 5. Decision Log Template
```markdown
{panel:title=Decision Record|borderColor=#ff5630}
**Decision ID**: [PROJ]-DEC-[XXX]
**Date**: {date}
**Status**: {status:colour=Green|title=Approved}
**Decision Maker**: @decisionmaker
**Stakeholders**: @stakeholder1, @stakeholder2
{panel}

## Context & Background
[Provide background on what led to this decision. Include relevant history, constraints, and why a decision is needed now.]

## Problem Statement
[Clearly articulate the problem or question that requires a decision]

## Options Considered

### Option 1: [Option Name]
**Description**: [Detailed description]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Cost/Effort**: [Estimate]

### Option 2: [Option Name]
**Description**: [Detailed description]

**Pros**:
- [Advantage 1]
- [Advantage 2]

**Cons**:
- [Disadvantage 1]
- [Disadvantage 2]

**Cost/Effort**: [Estimate]

### Option 3: [Option Name]
[Continue pattern]

## Decision Matrix
| Criteria | Weight | Option 1 | Option 2 | Option 3 |
|----------|--------|----------|----------|----------|
| Cost | 30% | 7/10 | 5/10 | 8/10 |
| Time to Implement | 25% | 6/10 | 9/10 | 5/10 |
| Scalability | 25% | 8/10 | 6/10 | 9/10 |
| Risk | 20% | 7/10 | 8/10 | 5/10 |
| **Total Score** | | **X.X** | **Y.Y** | **Z.Z** |

## Decision
{info}
**Chosen Option**: [Option X]

**Rationale**: [Explain why this option was selected. Reference the decision matrix and key factors.]
{info}

## Consequences & Trade-offs
**Positive Consequences**:
- [Expected benefit 1]
- [Expected benefit 2]

**Negative Consequences/Trade-offs**:
- [Known limitation 1]
- [Known limitation 2]

**Mitigation Plans**:
- [How to address limitation 1]

## Implementation Plan
{tasks}
- [ ] [Implementation step 1] - @owner - [Date]
- [ ] [Implementation step 2] - @owner - [Date]
- [ ] [Implementation step 3] - @owner - [Date]
{tasks}

## Success Criteria
[How will we know if this decision was the right one?]
- [Metric/outcome 1]
- [Metric/outcome 2]

## Review Date
**Scheduled Review**: [Date to revisit this decision]

## Related Decisions
- [Link to related decision 1]
- [Link to related decision 2]

## References
- [Supporting document 1]
- [Research/data source]
```
