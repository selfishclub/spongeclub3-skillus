# PM 1:1 Templates, Feedback & Workflow

Read this when you need the full per-partner agenda templates, the Radical Candor feedback frame, the kickoff conversation script, the run-the-system workflow, or the troubleshooting/success-criteria detail. The SKILL.md keeps only the lean map; everything operational lives here.

---

## Core principles for PM 1:1s

Five principles that apply across all 1:1 types:

### 1. The 1:1 belongs to the other person

The default for a 1:1 with your manager: their agenda first. The default for a 1:1 with your report: their agenda first. PMs often invert this and turn 1:1s into status meetings; resist that.

### 2. Status updates do not need a 1:1

If the conversation is "here's what's happening on project X", that's a written update. The 1:1 is for what cannot be written: trust-building, growth, judgment calls, feedback.

### 3. Care personally, challenge directly (Radical Candor)

The strongest 1:1 relationships combine personal care with direct challenge. Avoid the two failure modes: "ruinous empathy" (care without challenge -- you never give hard feedback) and "obnoxious aggression" (challenge without care -- feedback feels brutal).

### 4. Cadence matters

Weekly is the default for direct working relationships. Bi-weekly for partner-of-partner. Monthly for tier-3 stakeholders. Cancelled 1:1s are an anti-pattern; reschedule, don't skip.

### 5. Document agreements, not transcripts

Capture what was decided and what the next step is. Don't transcribe the whole conversation -- it kills psychological safety.

## 1:1 type templates

### Type A: With your manager

**Cadence:** Weekly, 30-45 minutes.

**Default agenda:**

| Time | Section | Owner |
|------|---------|-------|
| 5 min | What's top of mind for you (your manager) | Manager |
| 15-20 min | What's top of mind for me | You |
| 5-10 min | Growth / longer-term discussion | Both |
| 5 min | Action items + next 1:1 | You |

**Your default questions for them:**

- "What feedback do you have for me from the past week?"
- "What's worrying you that you haven't shared?"
- "What's on your plate I could take off?"
- "How is leadership feeling about [project / area]?"

**Your default agenda items to raise:**

- One judgment call you're working through
- One piece of feedback you have for your manager (if relevant)
- One growth-related question
- One people-related update (team dynamic, hire, etc.)
- One escalation if needed

**What NOT to do:**

- Read off your status update
- Use the 1:1 to negotiate scope changes (do that async with a written proposal)
- Bring 8 topics (3-4 is the sweet spot)

### Type B: With your engineering manager partner

**Cadence:** Weekly, 30 minutes.

**Purpose:** Operational coordination, partnership health, escalations.

**Default agenda:**

| Time | Section |
|------|---------|
| 5 min | Personal check-in |
| 10 min | What's happening on shared projects |
| 10 min | What's worrying me / what's worrying you |
| 5 min | Actions for the week |

**Key questions:**

- "Is there anything I'm doing that's making your team's job harder?"
- "Where are you over-extended right now?"
- "What's an opinion you have about the roadmap you haven't shared yet?"
- "Where are we mis-aligned on priorities?"

**Topics to rotate weekly:**

- Roadmap and priorities
- Team health and capacity
- Technical debt and platform investments
- Quality (incidents, on-call, regression)
- Process changes
- Hiring

### Type C: With your design lead

**Cadence:** Weekly to bi-weekly, 30 minutes.

**Purpose:** Product quality, user research, craft conversations.

**Default agenda:**

| Time | Section |
|------|---------|
| 5 min | Personal check-in |
| 10 min | Current designs in flight |
| 10 min | User research / craft conversation |
| 5 min | Actions |

**Key questions:**

- "Is there a design direction we should debate that we haven't?"
- "Where am I over- or under-specifying in PRDs?"
- "What user research should we be running that we're not?"
- "What's a customer pain that's nagging you?"

### Type D: With a direct report (PM)

**Cadence:** Weekly, 45-60 minutes.

**Purpose:** Growth, judgment-building, feedback, blockers.

**Default agenda:**

| Time | Section |
|------|---------|
| 5 min | Personal check-in |
| 20-25 min | Their topics: work, judgment calls, blockers |
| 10-15 min | Growth and feedback |
| 5 min | Actions + next 1:1 |

**Coaching with GROW (Whitmore):**

When a report brings a problem, resist the urge to solve it. Use GROW:

- **G**oal -- What outcome are you trying to reach?
- **R**eality -- What's the current state? What have you tried?
- **O**ptions -- What options have you considered?
- **W**ay forward -- What will you do next?

GROW develops judgment. Solving problems for reports stunts their development.

**Default questions for them:**

- "What's gone well this week?"
- "What's the hardest decision you're facing?"
- "What do you need from me?"
- "What feedback do you have for me?"

**Growth conversation cadence:**

- Monthly: deeper growth conversation tied to their growth plan
- Quarterly: rubric calibration against the next level
- Annually: career planning (12-24 month horizon)

### Type E: With cross-functional partners (sales, support, data, marketing, legal)

**Cadence:** Monthly, 30 minutes (more often during launches).

**Purpose:** Alignment, mutual context, early-warning signal.

**Default agenda:**

| Time | Section |
|------|---------|
| 5 min | What's happening on your side |
| 10 min | What's happening on my side |
| 10 min | Mutual blockers / requests |
| 5 min | Actions |

**Key questions (rotate):**

- "What's a customer signal you're seeing that I should know about?"
- "What's a question you've been getting that we should answer?"
- "Where is our messaging mis-aligned with what customers experience?"
- "What's coming up that you need from product?"

## The 1:1 kickoff conversation

When starting any new 1:1 relationship, have a kickoff conversation explicitly:

1. **What this 1:1 is for** -- Status? Growth? Coordination? Trust-building?
2. **Cadence and format** -- Weekly? Bi-weekly? In-person? Async sometimes?
3. **Who owns the agenda** -- Default = the other person, but clarify
4. **How we'll give each other feedback** -- Frequency, format, examples
5. **What "good" looks like in 6 months** -- Define success for the partnership

See `assets/kickoff_template.md` for a full script.

## Feedback in 1:1s (Radical Candor)

The hardest part of any 1:1 is giving direct feedback. Kim Scott's Radical Candor framework provides a 2x2:

|  | Care Personally HIGH | Care Personally LOW |
|--|--|--|
| **Challenge Directly HIGH** | Radical Candor (target) | Obnoxious Aggression (avoid) |
| **Challenge Directly LOW** | Ruinous Empathy (avoid) | Manipulative Insincerity (avoid) |

Strong 1:1 feedback:

- Is specific to a behavior or moment, not a generalization
- Is timely (same week beats next month)
- Frames the impact: "When you did X, the impact on the team was Y"
- Invites response: "How did you experience that moment?"
- Closes with a desired change: "Next time, what would you try differently?"

Weak feedback patterns to avoid:

- The "feedback sandwich" (positive-negative-positive) -- it dilutes the message
- Generalizations ("You always...")
- Feedback delivered as humor or via someone else
- Sitting on feedback for weeks (compound interest works against you)

## Workflow

1. **Audit your current 1:1s.** List every 1:1 you run weekly. For each, name the type (A-E above) and whether it has a working structure.
2. **Pick the highest-leverage one to fix first.** Usually the manager 1:1 or your weakest direct-report 1:1.
3. **Have a kickoff conversation.** Use `assets/kickoff_template.md` to reset expectations explicitly.
4. **Adopt the template.** Use the partner-type agenda for 4 weeks consistently.
5. **Capture decisions and actions.** Use `assets/1on1_notes_template.md`. Keep the running doc.
6. **Review quarterly.** Are the 1:1s producing trust, growth, and unblocking? If not, change the format.

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| 1:1s turn into status updates | No structured agenda; default behavior takes over | Adopt the partner-type template; move status to a written async update; reclaim the 1:1 for what cannot be written |
| Your direct report leaves 1:1s frustrated | You are solving instead of coaching | Adopt GROW; resist the urge to answer until you've asked 3 questions; when stuck, ask "What do you think?" before "Here's what I think" |
| Your manager cancels your 1:1s frequently | Lower priority on their side, or you've not made them valuable | Make them tighter (30 min, 3 topics); pre-send the agenda; make sure they leave with one thing they didn't have before |
| You haven't given hard feedback in 6+ months | Ruinous empathy mode (Scott) | Pick the one piece of feedback you've been sitting on; deliver it in the next 1:1 using the situation-behavior-impact format |
| The 1:1 with your EM partner is tense | Misaligned priorities or accumulated unspoken issues | Schedule a 60-minute "operating model reset" 1:1; bring the partnership-health questions; ask each other explicitly "what's not working?" |
| You don't have time for monthly 1:1s with all cross-functional partners | Over-scheduled OR too many partners on your map | Tier the list -- weekly for 5 people, monthly for 8, quarterly for the rest; replace monthly meetings with bi-monthly written updates where possible |
| Your direct reports don't bring you their hardest problems | Trust gap; they expect to be judged rather than coached | Ask explicitly: "What's something you're avoiding telling me?"; demonstrate non-reactivity when they share something hard once; trust builds from there |

## Success Criteria

- Every 1:1 has a clear type (manager / EM partner / designer / report / cross-functional)
- Every 1:1 has a working agenda template the participants both know
- You have given at least one piece of direct feedback per month to each Tier 1 partner
- Your direct reports (if any) leave 1:1s with a clearer next step, not a solved problem
- Quarterly, you and your manager have a growth-focused 1:1 (not just operational)
- You document decisions and actions in every 1:1; you do not transcribe the conversation
- Your cancellation rate of 1:1s is <10% (if higher, the cadence is wrong)
