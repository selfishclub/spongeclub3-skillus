# AI Strategy Framework

A practical reference for Chief AI Officers building or refreshing an AI
strategy. Designed to be opinionated rather than exhaustive — use it to
make decisions faster, then localize to your context.

## 1. What an AI strategy must answer

A defensible AI strategy answers seven questions. If you can't answer any
one of them in a sentence, you don't have a strategy yet — you have a budget.

1. **Where does AI move the P&L?** (revenue, cost, retention, speed, risk)
2. **What is our right to win?** (data, distribution, domain, talent)
3. **What's the operating model?** (centralize, federate, hub-and-spoke)
4. **How do we build vs buy vs partner?** (per-capability, not company-wide)
5. **How do we govern risk?** (model risk, regulatory, brand)
6. **What's the talent + L&D plan?** (hire, retrain, partner)
7. **What does success look like in 12 months?** (3–5 KPIs, attributable)

If your strategy reads like "we will be an AI-first company," rewrite it.
That's positioning, not strategy.

## 2. Strategic themes (pick 3–5)

Most AI portfolios crowd into the same 6–8 themes. Choose a small number
intentionally; resist adding a ninth.

### Internal productivity (the low-risk default)
- **Engineering productivity** — code assist, code review, test generation
- **Knowledge work** — drafting, summarization, search, meeting capture
- **Operations** — ticket routing, classification, triage
- **Risk profile:** low (mostly internal) — but the AUP must be clear

### Customer-facing product
- **Embedded AI features** — search, recommendations, in-product chat
- **Net-new AI products** — copilots, agents, generative experiences
- **Risk profile:** medium-high — eval, monitoring, and red-teaming are required

### Decision support
- **Forecasting, scoring, prioritization** — credit risk, churn, fraud, lead score
- **Risk profile:** medium — falls under model risk management at most enterprises

### Process automation
- **Document understanding** — claims, invoices, contracts
- **Workflow agents** — multi-step automations across systems
- **Risk profile:** medium — agents acting in systems-of-record need strict guardrails

### Platform + infra
- **Foundation model access** — multi-provider, fallback, cost controls
- **MLOps + evals** — model registry, eval harness, monitoring
- **Risk profile:** low directly; high indirectly (single point of failure)

### Governance + safety
- **Model risk management** — registers, controls, audits
- **AI assurance** — third-party reviews, certifications, model cards
- **Risk profile:** the enabler — without it, the rest can't ship in regulated industries

## 3. Operating-model patterns

### Pattern A — Centralized AI org
One AI/ML group owns models, infra, eval, and shipping.

| When it fits | When it breaks |
|--------------|----------------|
| Early maturity, <500 engineers | BUs feel blocked, build shadow ML teams |
| High regulatory exposure | Bottleneck on the central team |
| Few high-value use cases | Distance from product context creates the wrong models |

### Pattern B — Federated AI
Each business unit owns its ML practitioners.

| When it fits | When it breaks |
|--------------|----------------|
| Mature org, strong BU autonomy | No shared platform, every BU rebuilds |
| Diverse use cases per BU | Governance gaps, inconsistent risk posture |
| Engineering culture is decentralized already | Vendor sprawl, no economies of scale |

### Pattern C — Hub-and-spoke (recommended default)
A central platform + governance group (the hub) sets standards, owns
infra, runs the eval harness, and reviews high-risk systems. Embedded
ML squads (the spokes) own product outcomes inside BUs.

The hub owns:
- AI/ML platform (training, serving, observability)
- Eval harness (shared benchmarks + per-use-case test sets)
- Model registry and approval workflow
- AI governance program (committees, policy, training)
- Vendor management (foundation model contracts, tooling RFPs)

The spokes own:
- Use-case definition and prioritization
- Model selection (within approved set) and prompt design
- Application UX
- Business KPIs and adoption

A common failure mode: the hub becomes a tollbooth. Prevent this with
clear SLAs (e.g., new model approval ≤2 weeks for low/medium-risk; ≤6
weeks for high-risk) and a self-service path for sanctioned patterns.

## 4. Build vs buy vs partner — per capability

Apply this decision per capability, not company-wide.

| Capability | Default |
|------------|---------|
| Foundation model | Buy/partner — don't train your own LLM unless you have a unique reason |
| Vector store | Buy — well-served by 5+ vendors |
| LLM orchestration framework | Buy or open source — avoid bespoke unless you have unusual scale |
| Eval harness | Build the wrapper, buy the components |
| Retrieval over your data | Build — this is where your differentiation lives |
| Application UX / agents | Build — this is your product |
| Domain fine-tunes | Build if and only if eval shows base + retrieval can't get there |
| Annotation / labeling | Buy + audit — pure outsourcing has quality problems; managed services with your QA layer work |

## 5. Prioritization heuristics

### The 3-bucket portfolio

For each potential AI initiative, place it in one bucket:

- **Bucket 1 — Run the business.** Productivity gains, table-stakes features. ~50% of capacity.
- **Bucket 2 — Grow the business.** Differentiating product features. ~35%.
- **Bucket 3 — Transform the business.** New product lines, new business models. ~15%.

Strategy = the mix. A 90/10/0 portfolio means you're a follower. A 20/30/50
portfolio means you're betting the company.

### Scoring lens

For comparable initiatives within a bucket, score on:

| Dimension | Weight (illustrative) |
|-----------|----------------------|
| Strategic fit (theme alignment) | 25% |
| Value (rev/cost impact, attributable) | 30% |
| Confidence (data quality, prior art) | 15% |
| Risk (model, regulatory, reputational) | 15% (penalty) |
| Time-to-value | 15% |

This is encoded in `ai_investment_planner.py`. Override weights to match
your context.

### Kill criteria (publish in advance)

A project gets killed if any of:

- Eval doesn't reach the published target within 1 quarter of the planned ship date
- The economics flip (LLM cost > 3× projection at unit volume)
- A change in regulation makes the use case non-viable
- Adoption stalls below 20% of intended user base for 2 quarters post-launch

## 6. KPIs that matter

Pick 3–5 max. Common picks:

- **Production AI systems** (count, with risk-tier breakdown)
- **AI-attributable revenue or cost saving** ($, audited methodology)
- **Eval pass rate** for the production set (e.g., %≥0.85 on the shared benchmark)
- **Mean time to model approval** (governance bottleneck check)
- **Adoption** of priority internal-productivity tools (DAU/MAU)
- **Incidents** (count + severity), recoverable vs material

Avoid:
- "Number of AI projects" — incentivizes pilots that never ship
- "Models trained" — incentivizes training over reuse
- "Engineers using Copilot" without an adoption depth measure

## 7. The 90/180/360 plan

A useful structure for the first year:

**Day 0–90 — Inventory and stabilize**
- Inventory existing AI systems (Z-score risk; classify under EU AI Act)
- Stand up a baseline governance committee (exec + technical review board)
- Publish an interim AUP for LLM tools
- Pick the 3–5 strategic themes; ratify with the exec team

**Day 91–180 — Platform and policy**
- Pick the AI platform stack (FM access, vector store, observability, eval)
- Publish v1 of the model approval workflow
- Run a tabletop on an AI incident (model drift; prompt injection; PII leak)
- Sign the 2–3 anchor vendor contracts; consolidate spend

**Day 181–360 — Ship and measure**
- Ship the first 2–3 production systems on the new platform
- Publish KPIs to the board; show first quarter of trend
- Externalize an AI principles statement (helps with sales, hiring, regulators)
- Plan the year-2 investment from the platform you've now proven

## 8. Common executive frictions and how to handle them

| Friction | Move |
|----------|------|
| CFO wants ROI per initiative; AI cost is bundled | Push for per-product cost allocation with a clear methodology |
| CTO wants AI in the engineering org; you want a peer function | Run the hub-and-spoke pattern with shared infra ownership |
| CISO blocks foundation-model access | Co-author the acceptable-use + data-handling policy; pilot a sanctioned tool |
| GC won't approve high-risk deployments | Engage them earlier; AIIA + post-market monitoring de-risk most concerns |
| BUs run their own GenAI pilots without governance | Don't block — offer a fast-path approval for low-risk pilots, then ratchet |
| Board asks "are we behind on AI?" | Don't react; show the portfolio (themes × bets × KPIs) and the platform |
