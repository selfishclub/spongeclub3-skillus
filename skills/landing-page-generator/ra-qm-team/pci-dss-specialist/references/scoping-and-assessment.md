# CDE Scoping, SAQ Selection, Assessment Types, and Merchant/SP Levels

Read this when determining what is in scope, which Self-Assessment Questionnaire applies, what kind of assessment (SAQ vs ROC) is required, or how merchant/service-provider levels map to validation obligations.

---

## Cardholder Data Environment Scoping

### CDE Definition

The Cardholder Data Environment (CDE) includes:
1. **System components that store, process, or transmit CHD/SAD** — These are directly in scope
2. **System components on the same network segment** — These are in scope unless segmented
3. **System components that connect to or provide security services** — Connected-to and security-impacting systems

### System Classification

| Category | Definition | In Scope? | Examples |
|----------|-----------|-----------|---------|
| CDE Systems | Store, process, or transmit CHD | Yes — Full scope | Payment servers, databases with PAN, POS terminals |
| Connected-to | Direct connectivity to CDE | Yes — Full scope | DNS servers for CDE, AD/LDAP for CDE authentication |
| Security-Impacting | Provide security services to CDE | Yes — Full scope | SIEM, AV server, patch management for CDE systems |
| Out of Scope | No connectivity, no CHD, no security impact | No | Isolated HR systems, marketing servers |

### Scope Reduction Strategies

**1. Tokenization:** Replace PAN with non-reversible tokens. Systems that only handle tokens are out of scope.

**2. P2PE (Point-to-Point Encryption):** Validated P2PE solutions encrypt cardholder data at the point of interaction. Merchants using validated P2PE can use SAQ P2PE (reduced scope).

**3. Network Segmentation:** Isolate CDE on a separate network segment with firewalls and strict access controls. Non-CDE segments are out of scope.

**4. Outsource Processing:** Use third-party payment processors (Stripe, Braintree, Adyen) to handle all CHD. The merchant never touches cardholder data.

**5. iFrame/Redirect:** For e-commerce, use the payment processor's hosted payment page (iFrame or redirect). The merchant's systems never receive cardholder data.

---

## SAQ Types and Selection Guide

Self-Assessment Questionnaires (SAQs) are validation tools for merchants and service providers not required to undergo a full on-site assessment (ROC).

| SAQ Type | Applies To | CHD Handling | Questions |
|----------|-----------|-------------|-----------|
| **SAQ A** | E-commerce or MOTO merchants | All payment processing fully outsourced; no electronic storage/processing/transmission of CHD | ~30 |
| **SAQ A-EP** | E-commerce merchants | Payment page elements from third party, but merchant website impacts security of payment transaction | ~140 |
| **SAQ B** | Merchants with standalone POS (dial-out terminals) | Imprint-only or standalone dial-out terminals; no electronic CHD storage | ~40 |
| **SAQ B-IP** | Merchants with standalone IP-connected POS | Standalone POS terminals connected via IP; no electronic CHD storage | ~80 |
| **SAQ C** | Merchants with payment app systems connected to internet | Payment application connected to internet; no electronic CHD storage | ~160 |
| **SAQ C-VT** | Merchants with web-based virtual terminals | Manual entry via virtual terminal from processor's web-based solution; no electronic CHD storage | ~80 |
| **SAQ D (Merchant)** | All other merchants | Does not qualify for other SAQ types | ~330 |
| **SAQ D (Service Provider)** | Service providers | Service providers eligible for SAQ | ~330 |
| **SAQ P2PE** | Merchants using validated P2PE | Hardware terminals with validated P2PE solution; no electronic CHD storage | ~30 |

### SAQ Selection Decision Tree

```
Does your organization store, process, or transmit CHD?
├── No → Not subject to PCI DSS
└── Yes → Continue
    │
    Are you a Service Provider?
    ├── Yes → SAQ D (Service Provider) or ROC
    └── No (Merchant) → Continue
        │
        Do you store CHD electronically?
        ├── Yes → SAQ D (Merchant)
        └── No → Continue
            │
            E-commerce only?
            ├── Yes → Do you fully outsource all payment processing?
            │   ├── Yes (iFrame/redirect, no scripts on payment page) → SAQ A
            │   └── No (payment page on your server or scripts affecting payment) → SAQ A-EP
            ├── Card-present (POS)?
            │   ├── Using validated P2PE? → SAQ P2PE
            │   ├── Standalone dial-out terminal? → SAQ B
            │   ├── Standalone IP-connected terminal? → SAQ B-IP
            │   └── Payment application system? → SAQ C
            └── Virtual terminal only? → SAQ C-VT
```

---

## Assessment Types

### Self-Assessment Questionnaire (SAQ)

**Who:** Level 2-4 merchants (unless acquirer requires ROC)
**What:** Self-assessment using applicable SAQ type
**Frequency:** Annual
**Output:** Completed SAQ + Attestation of Compliance (AOC)

### Report on Compliance (ROC)

**Who:** Level 1 merchants, all Level 1 service providers
**What:** On-site assessment by Qualified Security Assessor (QSA)
**Frequency:** Annual
**Output:** ROC document + AOC

### Attestation of Compliance (AOC)

**Who:** All entities, accompanies SAQ or ROC
**What:** Executive summary confirming compliance status
**Frequency:** Annual, accompanies assessment
**Output:** Signed AOC form

---

## Merchant and Service Provider Levels

### Merchant Levels

| Level | Annual Visa Transactions | Assessment Required |
|-------|------------------------|-------------------|
| **Level 1** | Over 6 million | Annual ROC by QSA + quarterly ASV scan |
| **Level 2** | 1 million to 6 million | Annual SAQ + quarterly ASV scan |
| **Level 3** | 20,000 to 1 million (e-commerce) | Annual SAQ + quarterly ASV scan |
| **Level 4** | Under 20,000 (e-commerce) or up to 1 million (other) | Annual SAQ + quarterly ASV scan (recommended) |

**Note:** Card brands and acquirers may have different thresholds. Check with your acquirer.

### Service Provider Levels

| Level | Annual Transactions | Assessment Required |
|-------|-------------------|-------------------|
| **Level 1** | Over 300,000 | Annual ROC by QSA + quarterly ASV scan |
| **Level 2** | Under 300,000 | Annual SAQ D + quarterly ASV scan |
