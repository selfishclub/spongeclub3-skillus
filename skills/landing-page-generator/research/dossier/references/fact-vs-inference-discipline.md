# Fact vs Inference Discipline

Reference for separating facts, inferences, and speculation in dossiers
and intelligence reports.

## 1. The three categories

### Fact
A verifiable claim supported by evidence.

Examples:
- "Company X reported $50M ARR in Q1 2026."
- "Smith joined the board in March 2025."
- "The product launched on May 15."

Requires: sourced; verifiable; specific.

### Inference
A reasoned conclusion drawn from facts + analytical framework.

Examples:
- "Likely targeting enterprise segment, based on hiring 12 enterprise AEs."
- "The platform shift suggests preparation for acquisition."
- "Decision pace implies a single-decision-maker structure."

Requires: clearly labeled; supporting facts cited; alternative interpretations considered.

### Speculation
A guess with limited evidence.

Examples:
- "Might pivot to AI next year."
- "Probably planning to file an S-1."
- "Could be acquired by Big Co."

Requires: explicitly labeled; flagged as uncertain; usually relegated to "Open questions" section.

## 2. Why the separation matters

Mixing the three:
- Reader can't calibrate confidence
- Recommendations based on speculation get acted on as if confirmed
- Reputation of the dossier author erodes
- Decisions based on the dossier become brittle

Separating them:
- Reader can act with appropriate confidence
- Bad decisions (acting on speculation) are flagged in advance
- Dossier earns continued use
- Updates focused on the right tier (new facts vs new inferences)

## 3. Writing patterns

### Fact-as-fact
> "Company X reported $50M ARR in Q1 2026."

Just state it. Source separately.

### Inference-from-fact
> "**Inference:** Likely targeting enterprise segment, based on hiring 12 enterprise AEs in Q1 (LinkedIn) and 60% of recent press citing enterprise wins (trade press, Q1 2026)."

Use "likely," "suggests," "appears" — and cite the underlying facts.

### Speculation-as-speculation
> "**Speculation:** Possible IPO preparation in 2027. Limited supporting evidence beyond the recent CFO hire who has IPO experience."

Use "possible," "might," "could" — and explicitly note the limited evidence.

## 4. Common mistakes

### Treating opinion as fact
WRONG: "Their strategy is wrong."
RIGHT: "**Inference:** Their strategy of X conflicts with market trend Y, based on [evidence]."

### Hidden inferences
WRONG: "They're focused on enterprise."
RIGHT (if inference): "**Inference:** They appear focused on enterprise based on [signals]."

### Over-confident speculation
WRONG: "They're going to pivot to AI."
RIGHT: "**Speculation:** Possible AI pivot, based on recent hires; not yet a confirmed direction."

### Burying uncertainty
WRONG: "Funding is healthy."
RIGHT: "Funding raised: $50M Series B (TechCrunch, March 2026). Runway not publicly disclosed (estimated 18-24 months based on burn assumptions)."

## 5. Confidence labels

A useful 5-level confidence labeling:

| Label | When |
|-------|------|
| **Confirmed** | Multiple independent sources; verified |
| **Strong inference** | Inference from confirmed facts; alternatives considered |
| **Weak inference** | Inference from single source or limited facts |
| **Speculation** | Limited evidence; flagged for further research |
| **Unknown** | Reader should know we don't know |

Apply per claim, not per section.

## 6. The "what we don't know" section

A trustworthy dossier explicitly lists what's unknown:

```
OPEN QUESTIONS
1. [Question 1] — why unknown / what we tried
2. [Question 2] — research needed to answer
3. [Question 3] — may not be knowable from outside
```

A dossier that claims to know everything is suspect.

## 7. Negative evidence

Include disconfirming evidence too:

- "Customer X is reportedly a key reference (per press release). However, Glassdoor reviews from Customer X employees suggest dissatisfaction."
- "Funding was announced as $50M (TechCrunch). The SEC filing shows the round structured as $30M equity + $20M debt facility."

Negative evidence isn't always determinative; reporting it shows research rigor.

## 8. Source attribution per statement

Inline attribution earns trust:

WORSE:
> "Smith joined as CEO in March."

BETTER:
> "Smith joined as CEO in March 2026 (company press release, March 15; LinkedIn profile updated March 18)."

The reader can decide whether to dig further.

## 9. Inference cousins to flag

Look out for and label:

- **Implicit framework:** "obviously they're behind" — what's "obvious" assumes a framework
- **Causal claims:** "X happened because Y" — usually inference, often weak
- **Counterfactual:** "If only they had X, then Y" — speculation often disguised
- **Reading minds:** "They believe X" — usually inference; sometimes speculation
- **Universal:** "They always do X" — overgeneralization, usually speculation

## 10. Examples — calibrating language

| Avoid | Use instead |
|-------|------------|
| "Their strategy is to X" | "Strategy appears to be X based on [evidence]" |
| "They're targeting Y" | "Hiring suggests focus on Y" |
| "They'll succeed" | "Factors supporting success include X; risks include Y" |
| "Everyone knows X" | "[Source] reports X" |
| "Clearly Z" | "Indicates Z" |
| "Cannot fail" | "High likelihood of [outcome] absent [specific risk]" |

Specific > vague; cited > unsourced; labeled > implied.

## 11. Reader-side awareness

A reader of an intelligence document should:

- Check confidence labels per claim
- Look for source attribution
- Notice "speculation" tags
- Read the "open questions" section
- Discount unsupported inferences
- Probe surprisingly-confident claims

A dossier author should write so the reader can do all of this easily.

## 12. Common pitfalls

- **No fact / inference labels.** Reader can't calibrate.
- **Burying uncertainty.** Decisions over-confident.
- **Cherry-picking confirming evidence.** Hidden bias.
- **Inferences without supporting facts.** Just opinions.
- **Speculation in conclusion section.** Speculation should be flagged + isolated.
- **No "open questions" section.** Implies completeness.
- **Adversarial framing presented as neutral.** Bias.
- **One source for major claims.** Anecdote.
