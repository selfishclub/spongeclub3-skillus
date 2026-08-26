# Ethics, Best Practices & Quality

Read this when deciding whether a technique crosses the line into manipulation, hardening an implementation against pitfalls, or defining what "good" looks like — covers ethical guidelines, best practices, the troubleshooting table, and success criteria.

## Ethical Guidelines

### The Line Between Persuasion and Manipulation

**Persuasion (ethical):** Helping people make decisions that are genuinely good for them, using psychological insights to remove barriers and communicate value clearly.

**Manipulation (unethical):** Exploiting cognitive biases to trick people into decisions that are not in their interest.

### Principles for Ethical Application

1. **Transparency** — If you would be embarrassed to explain the technique to the customer, do not use it.
2. **Alignment** — Every psychological technique should help the customer reach a decision that is genuinely good for them.
3. **Reversibility** — If the customer changes their mind, make it easy to reverse the decision (easy cancellation, refunds).
4. **Honesty** — Scarcity must be real. Social proof must be real. Claims must be verifiable.
5. **Proportionality** — Do not use high-pressure techniques for low-stakes decisions.

### Specific Ethical Boundaries

- **Scarcity:** Only use when the constraint is real (limited seats, deadline pricing, inventory).
- **Social proof:** Only show real testimonials, real numbers, real logos with permission.
- **Urgency:** Only create urgency when a genuine deadline exists.
- **Dark patterns:** Never hide unsubscribe options, pre-check unwanted options, or make cancellation deliberately difficult.

## Best Practices

1. **Diagnose before prescribing** — Understand what behavioral barrier exists before applying a principle. Random psychology application is noise.

2. **Apply 2-3 principles, not 20** — Overloading a page with every psychological technique creates cognitive overwhelm.

3. **Test everything** — Psychology provides hypotheses. Data provides answers. A/B test every change.

4. **Context matters** — Social proof that works for consumer SaaS may not work for enterprise. Adapt to your audience.

5. **Ethics first** — If a technique feels manipulative, it probably is. Long-term trust outperforms short-term conversion.

6. **Combine principles** — The most effective implementations combine 2-3 complementary principles (e.g., social proof + scarcity + loss aversion near CTA).

7. **Specificity wins** — "2,847 teams" is more psychologically compelling than "thousands of teams" because specific numbers trigger credibility bias.

8. **Study the science** — Read Kahneman, Cialdini, Ariely, and Thaler for deep understanding. Surface-level application produces surface-level results.

9. **Monitor for diminishing returns** — Psychological techniques lose effectiveness over time as audiences become desensitized. Refresh regularly.

10. **Document learnings** — Every A/B test teaches something about your audience's psychology. Build a knowledge base of what works for your specific audience.

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Page feels persuasive but doesn't convert | Missing trust cascade (visual > relevance > credibility > risk) | Build trust in sequence. Run `persuasion_auditor.py` to find gaps. |
| Pricing page has high drop-off | No anchoring, no decoy, no recommended plan | Run `pricing_psychology_analyzer.py`. Add 3-tier structure with highlighted middle tier. |
| Social proof present but not working | Generic testimonials without specificity | Replace "Great product!" with named testimonials + specific metrics + outcomes. |
| Scarcity messaging feels manipulative | Fake constraints (countdown timers, fake "limited") | Only use scarcity when genuine. Fake scarcity erodes trust permanently. |
| Too many principles applied at once | Cognitive overload from stacking 10+ techniques | Apply 2-3 complementary principles, not everything. Less is more. |
| Loss-framed headlines not performing | Audience is solution-aware, not problem-aware | Match framing to awareness level. Solution-aware audiences respond to gain framing. |
| Users abandon during long forms | Friction too high, no progress indicators | Apply Zeigarnik effect: add progress bars. Reduce fields to minimum. |

## Success Criteria

- Cialdini principle coverage: 4+ of 7 principles applied on key conversion pages
- Every pricing page uses anchoring, recommended plan highlight, and risk reversal
- A/B test running on every psychology-based change (hypothesis + measurement)
- Loss-framed and gain-framed headline variants tested (loss framing typically wins 60-70%)
- Social proof includes specific numbers (not "thousands" but "2,847 teams")
- Ethical guidelines followed: all scarcity real, all claims verifiable, easy cancellation
- Document learnings: build audience-specific psychology knowledge base from test results
