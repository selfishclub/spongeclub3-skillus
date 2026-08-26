# AI Org & Talent Reference

Patterns for organizing the AI function, hiring the right roles in the
right order, and developing AI literacy across the company.

## 1. The AI org — three core groups

A mature AI organization usually contains three groups, regardless of
reporting structure:

### A) AI Platform
Owns infra, tools, and shared services that every applied team uses.

- Foundation-model gateway (multi-provider, caching, rate limit, cost attribution)
- Eval harness and benchmark management
- Model registry and approval workflow
- Vector store, retrieval pipeline, document processing
- Observability (latency, cost, quality, drift)
- Annotation and data-labeling tooling
- Fine-tuning and training infrastructure (if needed)

### B) Applied AI / Embedded ML
Owns delivery — usually embedded in product or business teams.

- Use-case definition with product/BU
- Model selection (within approved set)
- Prompt design, retrieval design, agent design
- Eval design for the use case
- Application UX (often paired with product engineering)
- Adoption and value measurement

### C) AI Governance + Risk
Owns the trust posture.

- Policy and standards
- Model approval gates and risk review
- Incident response process
- Regulatory tracking (EU AI Act, sector-specific)
- Third-party AI vendor reviews
- AI literacy program

These are roles, not necessarily separate teams. In a 50-person company,
all three may live inside one team of 5–10. In a 5000-person company,
they're separate functions reporting to the CAIO.

## 2. Hiring sequence (by org size)

### Stage 1 — < 100 engineers
Hire **one senior applied ML engineer** with breadth (eval, prompt, retrieval,
deployment). They double as the platform lead and the governance lead.

Common mistake: hiring an ML researcher when you need someone who ships.

### Stage 2 — 100–500 engineers
Add:
- A **second applied ML engineer** to start the embedded model
- A **platform engineer** (infra background; doesn't need ML depth) for the gateway, observability, cost
- A **part-time AI policy lead** (often inside legal/compliance, dotted-line to AI)

You don't yet need a CAIO — a head of AI or principal engineer can carry the weight.

### Stage 3 — 500–2000 engineers
Add:
- A **head of AI** (or CAIO at this stage) with full P&L for the function
- **Embedded ML leads** per major product area (1 per 50–80 engineers in that area is a healthy ratio)
- A **dedicated AI governance lead** (full time)
- A **data quality / data engineering** counterpart
- **Annotation operations** lead

### Stage 4 — 2000+ engineers
Add:
- **Platform manager** (separate from head of AI)
- **Red team lead**
- **Vendor management** specialist
- **AI security** engineer (paired with CISO org)
- **AI product manager(s)** at the platform and at major product areas

## 3. Role definitions

### Chief AI Officer
- Owns AI strategy, portfolio, and risk
- Peer to CTO, CIO, CISO; reports to CEO (preferred) or COO/CTO
- Operates through the AI Council + Model Risk Board
- Outside view (regulators, partners, customers) is part of the role

### Head of AI Platform
- Owns the gateway, eval harness, registry, infra
- Sets standards every applied team consumes
- Manages foundation-model vendor relationships
- Manages platform cost and capacity

### Applied ML / GenAI Engineer
- Builds production AI features end-to-end
- Designs evals; iterates prompts/retrieval; ships
- Pairs with product, design, and backend engineers
- Owns post-launch monitoring with platform

### ML / Data Scientist
- Predictive modeling, classical ML, decision support
- Stronger statistics + experimentation than GenAI engineers
- Often partners with analytics for impact measurement

### MLOps / Platform Engineer
- Infra, CI/CD, observability, cost
- Backend mindset; doesn't need to train models
- Owns reliability of training and serving

### AI Governance / Risk Lead
- Owns risk register, AIIAs, approval workflow
- Liaises with GC, privacy, CISO, regulators
- Builds the literacy program

### AI Red Team Lead
- Adversarial evaluation, jailbreak testing
- Threat modeling for new systems
- Maintains the adversarial test set in the eval harness

### AI Product Manager
- Use-case prioritization, requirements, eval criteria
- Adoption strategy
- Roadmap and stakeholder alignment

## 4. Compensation realities (2026)

Rough comp ranges in US-tier markets, for calibration only:

| Role | Base | Total comp (approx.) |
|------|------|----------------------|
| Sr applied ML engineer | $200k–$280k | $350k–$500k |
| Staff applied ML engineer | $260k–$360k | $500k–$800k |
| Head of AI (post-Series C) | $300k–$420k | $600k–$1.1M |
| AI governance lead | $200k–$280k | $300k–$450k |
| MLOps engineer | $180k–$260k | $300k–$500k |
| CAIO (mid-stage) | $400k+ | $800k–$2M+ equity-heavy |

European markets generally run 50–70% of US numbers. Frontier-lab competition
inflates the top end.

## 5. Build vs buy — the talent angle

You **can't out-hire** the frontier labs for foundation-model research talent.
What you can hire for:

- **Applied** engineers who understand your domain, data, and product
- **Eval-driven** practitioners who write tests before code
- **Platform** engineers who can run reliable AI infra at your scale
- **Governance** practitioners with regulated-industry experience

Stop trying to hire researchers unless you have a genuine research thesis
and a 5-year capital runway for it.

## 6. AI literacy across the company

A practical curriculum, tiered by role:

### Tier 1 — All employees (60–90 min)
- What AI tools we sanction and why
- What you can and can't put into a prompt (acceptable-use)
- How to escalate a suspected incident
- Where to find the AI policy

### Tier 2 — Engineers and product (4–8 hours)
- Foundation models 101 (capabilities, limits, evals)
- The shared eval harness and how to use it
- Prompt + retrieval patterns from our cookbook
- How to ship a low-risk AI feature
- When to escalate to the Model Risk Board

### Tier 3 — ML practitioners (ongoing)
- Internal eng meeting weekly
- Externally: paper reading group, conferences, open-source contribution
- Annual offsite for the AI org

### Tier 4 — Execs and managers (2 hours, refreshed quarterly)
- Strategy themes and our position
- Risk taxonomy and what to escalate
- The board narrative; how to talk about AI externally

## 7. AI org failure modes

### "Innovation theater"
Big AI team, lots of demos, no production systems.

**Fix:** publish a public production-system count and AI-attributable
business metric. If neither moves, restructure the team around delivery.

### "Center of excellence" without delivery
A central AI team writes whitepapers, runs lunch-and-learns, never ships.

**Fix:** dissolve into embedded squads + a small platform group. The
"COE" pattern almost always fails.

### "Shadow AI" everywhere
Every BU has its own LLM tool, its own vendor, its own (or no) governance.

**Fix:** offer a sanctioned, fast-path option that's better than what
they'd build themselves. Lead with carrots; use sticks selectively.

### Single point of expertise
One staff engineer knows the entire system. They leave.

**Fix:** insist on internal docs, runbooks, eval transparency, and
shared on-call from day one.

### Wrong manager profile at the top
The head of AI is a researcher who hasn't shipped production software.

**Fix:** the head of AI must be a builder. If your top candidate has
no production deployment experience, hire a strong COO/EM as the #2.

## 8. AI / human work — what the team does NOT do

Be explicit. Common boundaries:

- **AI is not a replacement** for engineering judgment in approval flows
- **AI is not a hiring decision-maker** (even if it scores candidates)
- **AI is not a sole compliance source** (it informs; humans decide)
- **AI is not a replacement** for security review on its own outputs (prompt-injection world)

Publishing these explicitly head off both fear and over-reliance.

## 9. Career ladders — what to expect

A typical Sr → Staff → Principal ladder for applied ML/GenAI roles emphasizes:

- **Sr:** ships features end-to-end; runs evals; owns one production system
- **Staff:** sets technical direction for a domain (e.g., search, agents); mentors
- **Principal:** organization-wide impact; drives platform standards; external presence

Avoid creating a separate "AI ladder" — it ghettoizes the function and
limits mobility. Use the engineering ladder with AI-specific examples.

## 10. Outsourcing the right pieces

Things that outsource well:

- **Annotation and labeling** (with your QA layer)
- **Penetration testing and red-teaming** (engaged quarterly)
- **Third-party audits** (SOC 2, ISO 42001)
- **Domain-specific fine-tuning** for adjacent capabilities (e.g., a vendor's medical-coding model)

Things that don't outsource well:

- **AI strategy** (too company-specific)
- **Use-case prioritization** (requires deep product context)
- **Governance program ownership** (you're accountable; agents help, not own)
- **Eval design** for your differentiating use cases (encodes your IP)
