# Freedom-to-Operate & Patentability Reference

Reference for FTO analysis and patentability assessment.

## 1. FTO vs patentability — different questions

| Question | Patentability | FTO |
|----------|---------------|-----|
| Asks | Can I get a patent on my invention? | Can I make/use/sell my product without infringing? |
| About | Novelty + non-obviousness + utility | Active patents whose claims my product might practice |
| Driven by | Prior art (any date pre-filing) | Active patents only (typically 20 years from filing) |
| Outcome | Patent granted (or not) | Risk assessment + mitigations |
| Output | Patent claims | Risk register + legal opinion |

You can get a patent and still infringe someone else's patent. Both
analyses are necessary for different decisions.

## 2. FTO process

### Step 1: Identify candidate blocking patents
- Search patents in your product's technology area
- Focus on patents currently in force (not expired)
- Include patents owned by competitors + NPEs (patent assertion entities)
- Cover all jurisdictions you plan to sell in (IP is territorial)

### Step 2: Construe claims
- Read claims carefully
- Apply ordinary meaning to terms (or specification-defined meaning)
- Check prosecution history (file wrapper) for narrowing arguments
- Identify each claim element

### Step 3: Map to product
- Element-by-element comparison
- Does your product practice every element?
- Consider doctrine of equivalents

### Step 4: Risk classification
- **High risk:** likely infringement of valid claim
- **Medium risk:** some risk; design-around possible
- **Low risk:** product doesn't practice key elements
- **Cleared:** confident no infringement

### Step 5: Mitigations
- Design-around (modify product to avoid element)
- License the patent
- Challenge validity (IPR/PGR/litigation)
- Wait for expiration
- Abandon market segment
- Accept risk (legal opinion as defense)

### Step 6: Legal opinion
- Patent attorney issues formal opinion
- Provides defense against willful infringement (treble damages)
- Costs $5-30K depending on scope

## 3. The infringement test

For literal infringement, the accused product must practice **every element** of at least one claim.

If one element is missing, no literal infringement of that claim.

Doctrine of equivalents may still apply for substantially-similar elements.

## 4. Claim construction matters

How a claim is read affects infringement:

- **Plain meaning rule** — give terms their ordinary meaning
- **Specification informed** — if spec defines a term, use that
- **Prosecution history estoppel** — if inventor narrowed during prosecution, can't recapture in litigation
- **Doctrine of equivalents** — equivalent elements infringe

In litigation, claim construction (the "Markman hearing") is often outcome-determinative.

## 5. Patent validity challenges

If you face a problematic patent, consider:

### Inter Partes Review (IPR, US PTAB)
- Cost-effective challenge ($300K-$1M)
- Based on patents + printed publications only
- ~80% institution rate; ~60% of instituted claims canceled

### Post-Grant Review (PGR, US PTAB)
- Within 9 months of issue
- Broader grounds than IPR
- Less common

### Ex Parte Reexamination (US)
- Cheaper; less control
- Patent holder participates fully

### District court invalidity defense
- Counter-claim in infringement suit
- Most expensive route

### EPO opposition
- Within 9 months of grant
- Multi-party
- Cheaper than EU national invalidation

## 6. Patentability analysis

### Novelty (35 USC §102 / EPO Art. 54)
The invention must not be disclosed in any single prior art reference before the filing date.

Test: does ANY single reference disclose every element of the claim?

If yes → not novel; claim invalid / unpatentable.

### Non-obviousness / inventive step (§103 / Art. 56)
The invention must not be obvious to a person of ordinary skill in the art.

US Graham v. Deere factors:
- Scope and content of prior art
- Differences between claim and prior art
- Level of ordinary skill
- Secondary considerations (commercial success, long-felt need, unexpected results)

EU "problem-solution" approach:
- Identify closest prior art
- Determine differences and effects
- Define objective technical problem
- Would skilled person solve it this way (without invention)?

Most patents are rejected on §103 (obviousness), not §102 (novelty).

### Utility (§101 / industrial applicability)
- Must be useful (US: low bar; one specific use suffices)
- Must be capable of industrial application (EU)

### Subject matter eligibility (US §101 — major issue)
- Abstract ideas not patentable (Alice test)
- Mathematical algorithms alone not patentable
- Software claims must be tied to specific technical improvement
- Diagnostic methods often rejected
- "Significantly more" required beyond the abstract idea

### Enablement (§112)
- Description must enable skilled person to make + use the invention
- Without undue experimentation
- Genus claims need representative examples

### Definiteness (§112)
- Claim language must be clear enough that scope is determinable
- "Means-plus-function" claims have specific rules

## 7. Subject matter eligibility (US — tricky)

Two-step Alice/Mayo test:

### Step 1: Is the claim directed to a patent-ineligible concept?
- Abstract idea
- Law of nature
- Natural phenomenon

### Step 2: Does the claim include "significantly more"?
- Specific implementation
- Improvement to computer functioning
- Application that transforms the abstract idea

Software claims often fail Alice unless they:
- Improve computer technology specifically
- Solve a technical problem in a particular way
- Don't merely automate a known process

EU patent law is generally friendlier to software (technical character test).

## 8. Patentability scoring framework

A useful 5-dimension assessment:

| Dimension | Question | Pass criterion |
|-----------|----------|----------------|
| Novelty | Any single ref. discloses all elements? | No |
| Non-obvious | Obvious to skilled artisan? | No |
| Utility | Useful for a stated purpose? | Yes |
| Subject matter | Abstract idea / natural law? | No / "significantly more" |
| Enablement | Adequately described to enable? | Yes |

A patentable invention passes all five.

## 9. Defensive publication — the alternative

If filing isn't worth it (cost > value):

- Publish the invention publicly
- Becomes prior art against everyone (including you)
- Cheap (~$50 for a defensive publication on IP.com)
- Effective: prevents competitors from patenting it

Good for: ideas you want freedom to use but don't want to invest in patenting.

## 10. Trade secret as alternative

Sometimes trade secret is better than patent:

| Trade secret | Patent |
|--------------|--------|
| Indefinite duration | 20 years max |
| No filing cost | $30K-$100K+ |
| No public disclosure | Public after 18 months |
| Independent invention OK by others | Excludes all others |
| Reverse engineering = lost | Excludes even RE |
| Best for: processes, formulas | Best for: products, methods exposed in commercialization |

Coca-Cola formula: trade secret. Pharmaceutical compounds: patent.

## 11. Provisional patent application

- US-specific (1-year priority placeholder)
- Cheaper than utility (~$3-5K vs $20K+)
- No examination; no claims required
- 12 months to file utility application
- "Patent pending" status
- Good for: early-stage; trade-show disclosure; investor demos

Don't over-use provisionals: 60% of provisionals never convert. Strategic provisionals only.

## 12. Common pitfalls

- **Filing without prior-art search.** Examiner finds it; patent invalid.
- **Disclosing before filing.** Loses patentability outside US.
- **Confusing FTO with patentability.** Different analyses.
- **Skipping FTO before launch.** Surprise injunctions.
- **Ignoring NPE risk.** Patent assertion entities pursue successful products.
- **No legal opinion.** Treble damages on willful infringement.
- **Over-claiming.** Broad claims often invalidated; narrower may survive.
- **Forgetting continuations.** Maintaining pendency for strategic flexibility.
- **One-and-done landscape.** Patent landscapes shift constantly.
