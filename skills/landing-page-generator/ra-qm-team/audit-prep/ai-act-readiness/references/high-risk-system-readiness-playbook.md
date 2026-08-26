# High-Risk AI System Readiness Playbook

Deep dive on preparing a high-risk AI system for conformity assessment + ongoing compliance. Covers Annex III classification, technical file build-out, conformity-assessment options, EU database registration, post-market monitoring.

---

## Pre-readiness: confirm classification

A common failure: investing in high-risk readiness when the system isn't actually high-risk (or vice versa: thinking it's not when it is).

### Annex III high-risk areas (Articles 6.1 + Annex III)

For each of the 8 areas, specific sub-categories trigger high-risk status:

#### 1. Biometric identification
- Remote real-time biometric ID in public spaces (highly restricted)
- Post-event biometric ID
- Biometric categorization (gender, race, age, etc.) for non-consented purposes
- Emotion recognition (limited contexts)

#### 2. Critical infrastructure
- Safety components of road traffic
- Safety components of water/gas/electricity supply
- Safety components of digital infrastructure

#### 3. Education and vocational training
- Determining access/admission
- Evaluating learning outcomes
- Steering learning process
- Detecting prohibited conduct (proctoring AI)

#### 4. Employment
- Recruitment AI (CV screening, video interview analysis)
- Personnel evaluation
- Task allocation (gig-economy algorithmic management)
- Performance / behavior monitoring

#### 5. Access to essential services
- Eligibility for public benefits/services
- Creditworthiness / credit scoring (excluding fraud detection)
- Risk assessment / pricing for life/health insurance
- Emergency call dispatching

#### 6. Law enforcement
- Risk assessment of persons (victims/perpetrators)
- Polygraph/emotion detection
- Evidence reliability evaluation
- Profile-based crime prediction

#### 7. Migration, asylum, border control
- Risk assessment of natural persons
- Document verification
- Polygraph/emotion detection
- Asylum claim evaluation support

#### 8. Administration of justice
- Decision-support to judges
- Election influence (alternative interpretations)

### When Annex III doesn't apply (Article 6.3)

A system in Annex III is NOT high-risk if it:
- Performs narrow procedural task
- Improves output of prior human activity
- Detects decision-making patterns (no autonomous decisions)
- Performs preparatory tasks
AND
- Doesn't pose significant risk of harm

You must self-document why exemption applies. Risky to claim without genuine analysis.

---

## Build-out: technical documentation (Annex IV)

For high-risk systems, comprehensive technical file required.

### Annex IV content

1. **General description**
   - Intended purpose
   - Provider information
   - Date + version of system
   - Use cases authorized
   - Hardware specifications
   - Form (component, standalone, etc.)

2. **Detailed description of system elements**
   - System architecture
   - All software components (algorithms, models, libraries)
   - Computational resources
   - Data flow diagrams
   - Pre-trained / third-party components
   - Optimization techniques

3. **Detailed description of monitoring + control mechanisms**
   - How the system is monitored
   - Built-in mechanisms for accuracy + robustness
   - Cybersecurity measures

4. **Validation + testing**
   - Testing methodology
   - Datasets used (training, validation, test)
   - Metrics applied
   - Performance results

5. **Risk management**
   - Risk management methodology
   - Identified risks + mitigations
   - Residual risks acknowledged

6. **System modifications**
   - Change log
   - Re-validation per change

7. **Standards applied**
   - Harmonized standards (where used)
   - Common specifications

8. **EU Declaration of Conformity**
   - Per template (Annex V)

9. **Description of post-market monitoring**
   - Plan
   - Metrics
   - Communication channels

---

## Conformity assessment paths

### Path A: Internal control (Annex VI) — most common

Provider performs internal assessment + signs EU Declaration of Conformity.

Steps:
1. Technical documentation complete
2. QMS operating per Article 17
3. Self-assessment per Annex VI
4. Sign EU Declaration of Conformity
5. CE marking
6. EU database registration (Article 71)

Suitable when:
- System uses harmonized standards
- Or common specifications adopted by Commission
- Provider can demonstrate compliance internally

### Path B: Third-party (notified body) (Annex VII)

Provider engages notified body for assessment.

Steps:
1. Technical documentation complete
2. Notified body selected (registered, accredited)
3. Submit technical documentation
4. Notified body assesses + issues certificate
5. Quality system audit (annual)
6. Provider applies for certificate + CE marking

Required for:
- Remote real-time biometric ID
- Certain other specific high-risk systems

### Notified body process

- Initial assessment: 3-6 months typical
- Annual surveillance audits
- Re-assessment every 5 years
- Costs: €30k-€200k+ depending on complexity

---

## EU Database Registration (Article 71)

Before placing on market, register in EU database:

- Provider information
- System name + version
- High-risk area (Annex III)
- Intended use
- Description of basic functionality
- Conformity assessment outcome
- Standards applied
- Member states where placed on market
- Contact details

Updates required within 30 days of significant changes.

---

## Post-market monitoring + serious incident reporting

### Post-market monitoring plan

Continuous monitoring of:
- Performance metrics drift
- Bias drift
- Unexpected behaviors
- User-reported issues
- New risks identified

Quarterly review minimum; more frequent for safety-critical.

### Serious incident reporting (Article 73)

Within 15 days of serious incident (death, serious harm, malfunction with potential for serious harm):
- Notification to market surveillance authority
- Investigation
- Corrective actions

Within 2 days for:
- Widespread incident
- Death

---

## Common gaps in high-risk readiness

| Gap | Why it matters | Fix |
|-----|---------------|-----|
| Risk management treated as one-time | Article 9 requires continuous | Integrate into ML pipeline / governance cadence |
| Data governance vague | Article 10 has specific requirements | Per-dataset documentation; representativeness analysis |
| Technical documentation auto-generated boilerplate | Annex IV requires real content | Engineer + writer collaboration |
| Logging not enabled | Article 12 mandates | Enable + retain + access procedure |
| Human oversight design weak | Article 14 requires meaningful | Test the intervention; not just a button |
| Adversarial testing skipped | Article 15 requires robustness | Run adversarial suite; document |
| QMS missing | Article 17 mandatory | Document + operate; ISO 42001 compatible |
| Notified body not engaged early | Long process | Engage 6+ months before deadline |
| Database registration after deployment | Required before market placement | Register first |
| Post-market monitoring reactive | Article 72 requires active | Define metrics + cadence |

---

## Multi-stakeholder coordination

High-risk readiness requires:

| Role | Responsibility |
|------|----------------|
| AI / ML Engineering | Build documentation; ensure technical capabilities |
| Data Science / Governance | Data quality, bias testing, representativeness |
| Security | Cybersecurity per Article 15 |
| Legal | Conformity assessment path; documentation review |
| DPO (if personal data) | GDPR overlay |
| Product | User-facing transparency (Article 13) |
| HR | AI literacy training (Article 4) |
| Operations | Post-market monitoring (Article 72) |

---

## Cheat sheet

| Question | Answer |
|----------|--------|
| Is my system high-risk? | Run Annex III check; consider Article 6.3 exemptions |
| Internal control or notified body? | Most use internal control; biometric ID requires notified body |
| Time to readiness from scratch? | 6-12 months for high-risk; 2-3 months for limited-risk |
| EU database registration timing? | Before market placement |
| Annual review needed? | Yes; post-market monitoring + risk management + AI literacy |
| Cost of notified body? | €30k-€200k+ |
| AI literacy training scope? | Anyone working with AI systems (broad interpretation) |
| Most common pitfall? | Underestimating data governance + bias testing requirements |
