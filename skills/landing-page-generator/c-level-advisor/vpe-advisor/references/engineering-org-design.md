# Engineering Org Design Reference

Practical reference for designing or restructuring an engineering organization
at any stage from 5 to 5000 engineers.

## 1. Org shapes (by stage)

### Stage 1: < 30 engineers — Functional or single team
- One pool of engineers; specialization emerges informally
- Single tech lead; founder often plays VPE/CTO
- Hiring: focus on generalists who can ship end-to-end
- Org risk: bottleneck on the founder/lead

### Stage 2: 30–100 engineers — Squad emergence
- 4–8 product squads of 4–8 engineers
- Squads paired with product manager + designer
- Platform / DevOps team forms (3–6 people)
- Roles: engineering manager (EM) per squad; founding VPE
- Org risk: weak EM bench; squad sprawl

### Stage 3: 100–500 engineers — Multi-squad with platform
- Squads grouped into pillars or domains
- Platform team graduates into platform org (15–30 people)
- Dedicated infrastructure, security, data, ML engineering
- VPE + CTO are clearly separate roles
- Layered EM structure (Director level emerges)
- Org risk: cross-team dependencies; platform becoming blocker

### Stage 4: 500–2000 engineers — Pillar + business unit
- Engineering org mirrors business structure
- Multiple platform sub-teams (FE platform, BE platform, data platform)
- Multiple specialist teams (security, SRE, ML, growth)
- VPs of Engineering per BU; SVPE or CTO over all
- Org risk: standards drift; fragmented eng culture

### Stage 5: 2000+ engineers — Enterprise engineering
- Domain-aligned engineering orgs
- Centralized platforms with strong product mindset
- Dedicated developer experience function
- Multiple CTOs/VPEs across product lines
- Org risk: bureaucracy; reorg-driven attrition

## 2. Common org pitfalls

### "Two-pizza" myth at scale
The classic 6-person squad doesn't scale beyond ~50 engineers without
a coordination layer. At 100+ engineers, the *coordination structure*
matters more than squad size.

### Platform as a service catalog with no UX
Many platform teams ship tools that engineers technically can use but
don't want to. Treat the platform as a product with internal users.

### Specialists in product squads
Embedded specialists (e.g., ML engineer, security engineer) work when
the squad has steady demand. Otherwise, they become an expensive
generalist. Pool them centrally and assign on-demand.

### Re-org as a productivity strategy
Re-orgs cost ~1–2 quarters of velocity. Use them to fix structural
problems, not to look like you're doing something.

## 3. Roles and titles

### Individual contributor (IC) track
- **Sr Engineer** (~3-5y) — owns features end-to-end; mentors juniors
- **Staff Engineer** (~6-10y) — sets technical direction for a domain; mentors seniors; partners with EMs
- **Sr Staff Engineer** (~10y+) — technical direction across multiple domains
- **Principal Engineer** — organization-wide impact; sets engineering-wide standards
- **Distinguished / Fellow** — exceptional cross-org influence; external presence

### Manager track
- **Engineering Manager (EM)** — manages 5-8 engineers; pairs with product / design
- **Sr EM** — manages 8-12 engineers; or 2 EMs
- **Director** — manages 3-5 EMs (~25-50 engineers)
- **Sr Director** — manages multiple Directors
- **VP** — owns a pillar / org (~50-200 engineers)
- **SVP / CTO / VPE** — owns the engineering function

### Career ladder principles
- IC and EM tracks should be equal in pay and prestige
- IC track must offer growth without forcing management
- Promotion criteria must be transparent and consistent
- Calibration sessions across managers prevent drift

## 4. Hiring sequence by stage

### Stage 1 — < 30 engineers
- Hire generalists (full-stack, can deploy infra)
- Hire for ramp-up speed and judgment
- Avoid early specialists (ML, security, SRE) unless core to the product

### Stage 2 — 30–100 engineers
- Hire founding VPE if founder hasn't earned the role
- Add EMs as squad count grows past 4
- First specialist hires: SRE, security, data engineer
- Begin formal interview training

### Stage 3 — 100–500 engineers
- Distinct CTO + VPE
- First Director of Engineering hire
- Specialist functions: ML, growth, mobile, infra
- Dedicated recruiting + sourcing function
- Begin platform investment

### Stage 4 — 500–2000 engineers
- VPs of Engineering per pillar / BU
- Heads of: SRE, Security, Data Engineering, ML Engineering, Platform, DevEx
- Engineering Operations / Chief of Staff role
- Performance management / promotion calibration becomes formal

### Stage 5 — 2000+ engineers
- Multiple SVPs / VPEs
- Distinguished / Fellow engineers as recognized senior IC
- Dedicated developer relations
- Internal engineering brand + external

## 5. Squad design principles

### Size: 4–8 engineers
- Below 4: bus risk; on-call unsustainable
- Above 8: communication overhead grows quadratically
- Sweet spot is 5–7

### Cross-functional pairing
- Squad pairs with PM + designer (when product-facing)
- Platform squads may not need PM but need a clear customer

### Mission clarity
- Each squad has a 1-page mission: what they own, what they don't,
  who they serve, success metrics

### Stable membership
- Squads form for a quarter+ minimum; rotation hurts more than it helps
- Exception: rotation rotations to platform / pairing assignments

### On-call ownership
- Squad owns on-call for its services
- 6–8 engineers minimum for sustainable rotation
- Shared on-call across multiple squads as fallback

## 6. Platform engineering — what to build

A modern platform team owns the "developer paved path":

- CI/CD pipeline (templates, opinions, fast)
- Service templates with built-in observability + security
- Infrastructure abstractions (Kubernetes, serverless, where appropriate)
- Internal developer portal (Backstage-style)
- Secret management
- Observability stack (metrics, logs, traces)
- Security tooling (SAST, dependency scanning, SBOM)
- Cost attribution
- Deployment safety (feature flags, canaries — see `engineering/feature-flags-architect`)

A successful platform team:
- Measures adoption (% of services on the paved path)
- Treats internal engineers as customers (NPS, friction interviews)
- Has a product manager (yes, even for internal tools)
- Is staffed at ~10–15% of total engineering

## 7. The Engineering Manager role

A good EM does five things, in priority order:

1. **People** — 1-on-1s, career growth, conflict, hiring, performance
2. **Delivery** — squad is shipping the right things on the right cadence
3. **Quality** — technical decisions are sound; on-call is healthy
4. **Process** — squad rituals work; not too heavy, not too light
5. **Strategy** — squad mission is clear; partners with PM on prioritization

EMs that focus only on delivery become project managers. EMs that focus
only on people become career coaches. The good EMs do both.

### EM-to-engineer ratios
- New EM: 4–6 reports
- Experienced EM: 6–8 reports
- > 10 reports = drowning; split the team

### EM promotion criteria
- Demonstrated coaching outcomes (engineers promoted, regrettable retention)
- Squad delivery health (DORA, on-call)
- Hiring outcomes (offers accepted, ramp time)
- Org influence (improving processes beyond own squad)

## 8. Performance management

### Cadence
- 1-on-1: weekly
- Formal check-in: monthly or quarterly
- Performance review: semi-annual or annual
- Calibration: at each review cycle

### Performance distribution
- ~10–15% top performers (strong promote / extra reward)
- ~70–80% solid contributors (continued investment)
- ~5–10% improvement needed (PIP or restructured scope)
- Force-ranking is poisonous; use distributions as a check, not a target

### PIP (Performance Improvement Plan) discipline
- PIPs are real; people pass them when given the chance
- Document expectations; weekly check-ins; clear endpoint
- If PIP is a euphemism for "we want them out," skip it and offer severance

## 9. Engineering culture — what actually matters

Culture is built through:
- **Hiring bar** — who you hire and reject
- **Promotion criteria** — what gets rewarded
- **Code review norms** — kindness + rigor; not gatekeeping
- **Incident response** — blameless postmortems with action items
- **On-call** — equitable, supported, with rotation discipline
- **Decision-making** — who decides, on what basis, who knows
- **Documentation** — what's written down vs tribal

Culture is NOT built through:
- Slogans
- Team-building exercises
- Perks
- Conference talks
- Carving "what we believe" into a wall

## 10. Diversity, equity, inclusion

A mature engineering org takes DEI seriously, operationally:

- Diverse interview panels
- Calibrated rubrics for hiring + promotion
- Inclusive on-call (don't penalize parents / different time zones)
- Sponsorship programs that go beyond mentorship
- Comp transparency (at minimum: bands by level)
- Demographic data tracked and reviewed (with privacy care)
- Inclusion is in scope for managers' performance reviews

## 11. Distributed / remote / hybrid

### Fully remote
- Async-first culture
- Documentation is mandatory
- Synchronous time is for collaboration, not status
- Geographic diversity is a strength

### Hybrid
- Specify in-office days clearly
- Design for hybrid meetings (camera + audio quality)
- Manage proximity bias in promotion

### In-office
- Increasingly rare past 2024
- Justify with specifics, not "culture"

## 12. Common pitfalls

- **EM track without IC track.** Forces strong engineers into management.
- **One-size-fits-all squad model.** Different teams need different shapes.
- **Re-org as productivity intervention.** Costs more than it saves.
- **Platform team without product manager.** Builds what engineers want, not what they need.
- **No on-call rotation discipline.** Burns out top engineers.
- **Specialist roles embedded too early.** Underutilized; expensive.
- **Hiring bar lowered in growth pushes.** Quality debt compounds.
- **Skipping calibration.** Promotion drift; comp inequity.
