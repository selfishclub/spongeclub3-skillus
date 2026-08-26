# Insight Quality & Bias Reference

Reference for evaluating the quality of insights coming out of synthesis
and minimizing the biases that distort interpretation.

## 1. Insight quality dimensions

A good insight is high on all four dimensions:

### Confidence
- How many sources support it?
- How independent are those sources?
- How recent are they?

Low confidence: 1-2 sources, recent, narrow segment.
High confidence: 5+ sources across multiple segments, multiple recent rounds.

### Specificity
- Is the insight specific enough to action?
- Or could it apply to almost anything?

Low specificity: "Users want a better experience."
High specificity: "Users abandon checkout when they see the shipping cost
because they expected free shipping."

### Bias risk
- Was the sample / methodology / interpretation biased?
- Have you cross-checked with disconfirming evidence?

Low risk: diverse sample, second coder, disconfirming evidence checked.
High risk: convenience sample, single interpreter, only confirming
evidence cited.

### Decision impact
- Does this insight change anything we'd do?
- Or is it interesting but unactionable?

Low impact: "Users are sometimes frustrated."
High impact: "Users in segment A would pay more for feature X; current
pricing leaves money on the table."

## 2. Common insight quality failures

### "Insight" that's actually a recommendation
"We should add a notification feature." — that's a recommendation, not an insight.
The insight would be: "Users miss important events because there's no
notification."

### "Insight" that's actually a fact
"40% of users in our survey are on iOS." — that's a fact, not an insight.

### "Insight" that's actually a quote
"User X said 'I love it.'" — anecdote, not insight.

### "Insight" without an actor
"Performance is important." — to whom? in what context? with what consequence?

### "Insight" that hides variation
"Users want flexibility." — half wanted more options, half wanted fewer.
The insight is about the variation.

## 3. The bias catalog — in research synthesis

### Confirmation bias
**Symptom:** quotes match the hypothesis suspiciously well.
**Counter:** explicitly search for disconfirming evidence. Have a second coder.

### Recency bias
**Symptom:** the last interview shapes the interpretation disproportionately.
**Counter:** review all sessions in the same sitting, not chronologically.

### Anchor bias
**Symptom:** the first interview frames all subsequent interpretation.
**Counter:** synthesize after several sessions, not after each one.

### Availability bias
**Symptom:** the most-quoted users are over-represented (eloquent / extreme).
**Counter:** weight by behavior, not eloquence.

### Selection bias
**Symptom:** who participated isn't representative.
**Counter:** track recruiting source; analyze segment by segment; note
who was missing.

### Acquiescence bias
**Symptom:** participants agreed with everything.
**Counter:** ask negative-frame questions ("What didn't work?"); test for
sycophancy; ignore "great, I love it" without follow-up.

### Demand characteristics
**Symptom:** participants guessed the goal and shaped responses accordingly.
**Counter:** unbiased recruiting; mask the goal; observe behavior over
self-report.

### Recall bias
**Symptom:** participants describe what they thought they did, not what they did.
**Counter:** observe over interview when possible; cross-check with
analytics; ask specific recent events, not generalities.

### Survivorship bias
**Symptom:** you only talked to current users; never to those who churned.
**Counter:** explicitly recruit churned users; talk to non-users for
acquisition research.

### Halo effect
**Symptom:** users who love the product overlook issues; haters exaggerate.
**Counter:** segment by relationship to product; weight observations
appropriately.

## 4. Triangulation

Don't trust a single source. Cross-check qualitative findings with:

- **Other qualitative sources** (different interview rounds, different segments)
- **Analytics data** (do users actually do what they say?)
- **Support tickets** (what's hurting people enough to complain?)
- **Sales feedback** (what loses / wins deals?)
- **Customer success notes** (what predicts churn / expansion?)
- **Competitive observation** (what are others doing?)

When sources converge, confidence is high. When they diverge, the
divergence itself is interesting.

## 5. The N-of-1 problem

A single vivid user story is intellectually persuasive — and often
misleading. Counter by:

- Reporting the count alongside the quote
- Asking "is this generalizable?" before acting
- Treating N=1 as a hypothesis, not a finding

When N=1 is enough: when the user's behavior is structural (e.g., a
regulatory requirement they describe is the same for everyone in their
role).

## 6. Insight validation methods

### Internal validation
- Second coder reviews the same data; do you reach the same themes?
- Show themes to other PMs / designers; do they agree on names + scope?
- Have stakeholders react to themes; do they recognize what you're describing?

### External validation
- Surveys with quant follow-up (validate frequency)
- A/B tests of solutions implied by insights
- Customer feedback on synthesized findings (member-checking)

### Replication
- Re-run the study with a different cohort
- If the same themes emerge, confidence is high

## 7. Reporting quality honestly

A trustworthy research report includes:

- **N and recruiting source** (so reader can judge representativeness)
- **Dates of research** (so reader can judge recency)
- **Methodology** (interview length, format, who interviewed)
- **Themes with frequencies** (how many users supported each)
- **Disconfirming evidence** (what didn't fit the pattern)
- **Open questions** (what you couldn't answer with this data)
- **Confidence assessment** (rate each insight on quality)

Without these, the report is a marketing piece, not research.

## 8. When to commission more research vs decide

A judgment call. Defaults:

| Confidence | Decision impact | Move |
|------------|-----------------|------|
| High | High | Decide; ship |
| High | Low | Decide; minimal investment |
| Low | High | Get more data first |
| Low | Low | Decide cheaply; reversible bet |

The expensive mistake is acting on low-confidence insights for high-impact
decisions. The other expensive mistake is delaying low-impact decisions
for perfect data.

## 9. Communicating uncertainty

Researchers should explicitly communicate uncertainty:

- "Strong evidence" / "Some evidence" / "Limited evidence" labels per insight
- "We didn't research X" rather than implying you did
- Confidence intervals on numbers if quant
- "This was true in our sample; we'd want to validate broader" caveat
- "Open question" for things you couldn't answer

## 10. Stakeholder pressure to over-state

Common dynamic: stakeholders want certainty; researchers deliver caveat
sandwiches. Negotiation:

- Be confident in what you saw; uncertain about extrapolation
- Lead with the answer; methodology in appendix
- Separate "what we observed" from "what we recommend"
- Pre-commit to a "next question" list — stakeholders know what's still open

## 11. Common pitfalls

- **Inflating one user's experience to a "user need."** N=1 isn't a finding.
- **Quoting selectively.** Always state the count.
- **Hiding the methodology.** Readers must judge trust.
- **Insights without disconfirmation analysis.** Hidden bias.
- **Conflating "what users said" with "what users do."** Behavior beats self-report.
- **Treating synthesis as opinion.** Synthesis is interpretation grounded in data.
- **Insights that don't change anything.** Then it's not an insight.
