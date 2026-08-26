# Contract & Commercial Governance Reference

Practical reference for the contract lifecycle and commercial governance
half of the GC mandate.

## 1. Contract portfolio — what you must know

For each contract in the portfolio:

- Counterparty (customer or vendor)
- Type (MSA, order form, SOW, DPA, NDA, employment, IP license)
- Effective date, expiration, auto-renewal terms
- Total contract value (TCV) and annual contract value (ACV)
- Liability cap and indemnification scope
- Governing law and jurisdiction
- Special terms / deviations from standard
- Owner (legal + business)
- Renewal status (active, in-negotiation, expiring)

A contract portfolio you can't query like this becomes a liability.

## 2. Standard templates — the must-haves

Maintain a versioned library:

| Template | Owner | Cadence of review |
|----------|-------|-------------------|
| MSA (master service agreement) | GC | Annual |
| Order form / SOW | GC + Sales Ops | Annual |
| DPA (data processing addendum) | GC + DPO | Annual + on regulatory change |
| Mutual NDA | GC | Annual |
| Vendor MSA | GC + Procurement | Annual |
| Vendor DPA | GC + DPO | Annual |
| Employment agreement | GC + CHRO | Annual + jurisdiction additions |
| Independent contractor agreement | GC + CHRO | Annual |
| Equity grant docs | GC + Equity admin | Annual |
| Reseller / partner agreement | GC + Channel | Annual |

If you don't have these, your team is reinventing them every deal.

## 3. Contract tiering & approval thresholds

Tier contracts so risk-appropriate approval applies:

| Tier | Criteria | Approver |
|------|----------|----------|
| Tier 1 | Strategic, high ACV, unusual terms | GC + CEO/CFO |
| Tier 2 | High ACV or non-standard | GC + business sponsor |
| Tier 3 | Standard terms, standard tier ACV | Commercial counsel |
| Tier 4 | Self-serve with standard template | Self-serve (no legal review) |

Combine with **deviation authority matrix**: which deviations require GC,
which can be approved by commercial counsel, which can sales approve.
Publish the matrix; train sales on it.

## 4. The deviation framework

Tag every deviation from standard:

- **Approved deviation** — within authority, signed off
- **Material deviation** — high exposure; requires GC or higher
- **Conditional deviation** — fine for this counterparty/segment only
- **Forbidden deviation** — never agree (e.g., unlimited liability, full indemnity)

Track deviation rate by:
- Sales rep / team — outliers indicate training need
- Counterparty type — pattern indicates negotiating position weakness
- Term type — pattern indicates template inadequacy

If deviation rate > 50%, the template is wrong; update it.

## 5. Liability and indemnity

Two contract terms get more attention than all others combined.

### Limitation of liability
Standard SaaS posture:
- **Cap:** 12 months of fees paid in the trailing 12 months (typical)
- **Exclusions from cap:** indemnification, confidentiality breach, gross negligence, willful misconduct
- **Consequential damages excluded** for both parties

### Indemnification
Standard SaaS posture:
- Mutual indemnification for IP infringement claims
- Mutual indemnification for confidentiality breach
- One-way customer indemnification for misuse / their data
- Common carve-outs: customer materials, open-source components

When the counterparty asks for uncapped liability or full indemnification,
that's a Tier 1 decision. Don't let sales agree on the fly.

## 6. Other terms that matter

| Term | Standard | Watch for |
|------|----------|-----------|
| Auto-renewal | Typical | Some jurisdictions require explicit consent; check |
| Termination for convenience | Limited | Asymmetric clauses |
| Service levels (SLAs) | Defined per tier | Aggregating SLAs across products |
| Data usage rights | Limited | "Aggregated insights" carve-outs |
| Source code escrow | Sometimes | Heavy ongoing burden |
| Most-favored-nation pricing | Avoid if possible | Locks in pricing for all customers |
| Audit rights | Limited (third-party report typical) | Direct customer audit asks |
| Insurance requirements | Standard | Excessive amounts; specific carriers |
| Assignment / change of control | Notice required | M&A blocker if not |
| Governing law | Your jurisdiction | Strategic counterparties may push |

## 7. Contract Lifecycle Management (CLM)

A CLM system earns its keep at ≥ 500 contracts/year or material complexity.
Required capabilities:

- Template library with version control
- Contract repository (single source of truth)
- Workflow for review/approval routing
- Redline tracking and integration with the document editor
- Search across executed contracts (clause-level for the mature)
- Reporting on cycle time, exposure, deviations
- Integration with CRM, ERP, eBilling
- Renewals dashboard with reminders

Common picks: Ironclad, Agiloft, ContractWorks, Linksquares, SimpleLegal.
The best CLM is the one your business actually uses.

## 8. Self-serve and automation

Move the low-risk volume off legal's desk:

- NDA generator (self-serve with standard template + 3 pre-approved variants)
- Vendor onboarding workflow (DPA + security questionnaire)
- Equity grants automation (Carta / Pulley)
- Employee separation document generation (with HR review)
- Order forms below threshold (no legal review needed)

Each item moved to self-serve frees commercial counsel for higher-leverage work.

## 9. GenAI in the contract workflow

Useful, with strict guardrails:

| Use case | Quality |
|----------|---------|
| First-pass review of incoming counter-redlines | Good |
| Summarizing long agreements | Good (with verification) |
| Drafting from playbook | Acceptable with review |
| Extracting key terms across a portfolio | Good |
| Generating playbook responses | Acceptable |
| Final review on Tier 1 contracts | Not yet |
| Negotiation strategy | Not yet |

Required guardrails:
- No-training contract terms with the AI vendor
- Vendor processes data in your jurisdiction
- Confidentiality preserved (privilege risk if not)
- Human review of every output before send
- Audit log of AI-assisted work

## 10. Commercial enablement — the sales-legal partnership

Sales success depends on legal throughput. Friction patterns:

- **Sales doesn't know what they can agree to** → publish the deviation matrix
- **Legal becomes the bottleneck** → tier contracts; deflect low-risk to self-serve
- **Sales bypasses legal** → make legal the easier path
- **Customer pushes hard** → playbook responses + escalation path
- **Renewal terms unfavorable** → renewal review process

Operating norms that work:
- Service-level commitment from legal (e.g., NDAs in 1 day; standard MSAs in 5 days)
- Embedded commercial counsel for top deals
- Battle cards for the top 10 customer redlines
- Pre-approval program for repeat customers

## 11. Renewals and upsells

Contract renewal is not just legal admin:
- Renewals as commercial moment — terms evolve, pricing changes
- Standard renewal motion: legal review 90 days out; negotiate at 60; close at 30
- Auto-renewal: friend (revenue protection) or foe (locked-in problems)
- Track renewal terms versus initial terms — drift indicator

## 12. Vendor and supplier contracts

Often less attention than customer contracts; equally important.

- Vendor risk assessment at intake
- DPA in place before processing personal data
- Security review (SOC 2, ISO 27001)
- Termination + exit clauses
- Audit rights (or third-party report acceptance)
- Insurance and indemnification scaled to risk
- Change-of-control notification

For AI / data vendors, mandatory additions:
- No-training clause covering inputs and outputs
- Data residency
- IP indemnification for outputs
- Deprecation notice for models in production

## 13. Common pitfalls

- **No standard templates.** Every deal bespoke; throughput dies.
- **Sales pre-approving terms.** Lose visibility; risk concentrates.
- **Auto-renewal without review trigger.** Locked into unfavorable terms.
- **CLM that no one uses.** Tooling without adoption = wasted money.
- **Liability cap on the wrong base.** "12 months fees" cap with prepaid multi-year = limited cap.
- **MFN clauses agreed casually.** Cripple future pricing.
- **Vendor DPA forgotten.** GDPR exposure waiting to happen.
- **Renewals as a finance task.** Lost negotiation leverage.
