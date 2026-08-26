# Infrastructure Controls and 12-Month Compliance Roadmap

Read this when implementing the technical controls behind PCI DSS (network segmentation, DNS/TLS, endpoint/POS, cloud, containers, API, tokenization, key management) or when planning a phased compliance program. For deeper architecture patterns (reference network diagrams, cloud-by-cloud build-outs, mPOS, e-commerce script controls, Kubernetes manifests), see [pci-infrastructure-security.md](pci-infrastructure-security.md).

---

## Infrastructure Controls

### Network Segmentation Validation

**Purpose:** Verify CDE is properly isolated from non-CDE networks.

**Testing Methods:**
- Firewall rule review — verify only approved traffic can cross CDE boundary
- Penetration testing from non-CDE segments attempting to reach CDE
- Traffic analysis confirming no unintended data flows
- VLAN hopping tests
- ARP spoofing tests

**Frequency:** Annually (every 6 months for service providers)

### DNS Security for Payment Systems

- Implement DNSSEC for all CDE domain names
- Use internal DNS servers for CDE (not public resolvers)
- Monitor DNS queries from CDE for data exfiltration indicators
- Restrict CDE DNS queries to approved destinations only
- Implement DNS sinkholing for known malicious domains

### TLS Configuration for Payment Channels

- Minimum TLS 1.2, prefer TLS 1.3 for all payment communications
- Strong cipher suites only: ECDHE key exchange, AES-GCM
- HSTS with long max-age on all payment-related web pages
- Certificate transparency monitoring for payment domains
- Automated certificate renewal (Let's Encrypt, ACME protocol)
- mTLS between CDE microservices
- Certificate pinning for mobile payment applications

### Endpoint Security for POS Systems

- Harden POS operating systems (application allowlisting)
- Deploy endpoint protection with anti-tamper capabilities
- Implement POS-specific network segmentation
- Regular POS terminal inspection for skimming devices
- Remote POS management via encrypted channels only
- Disable USB ports and external interfaces on POS terminals
- Monitor POS terminal integrity

### Cloud Security for Payment Processing

**AWS:**
- Use VPC with private subnets for CDE workloads
- AWS KMS or CloudHSM for encryption key management
- GuardDuty for threat detection in CDE
- Config rules for CDE compliance monitoring
- S3 bucket policies preventing public access to CHD
- Restrict IAM roles accessing CDE resources

**Azure:**
- Azure Virtual Network with NSGs for CDE isolation
- Azure Key Vault (HSM-backed) for key management
- Microsoft Defender for Cloud for CDE monitoring
- Azure Policy for CDE compliance enforcement
- Storage Service Encryption with customer-managed keys

**GCP:**
- VPC Service Controls for CDE isolation
- Cloud KMS or Cloud HSM for key management
- Security Command Center for CDE visibility
- Organization policies restricting CDE resource configuration
- BigQuery with column-level encryption for analytics on payment data

### Container/Kubernetes Security in CDE

- Scan container images for vulnerabilities before deployment
- Use private container registries with signed images
- Implement Kubernetes RBAC with CDE-specific namespaces
- Pod Security Standards (Restricted) for CDE pods
- Network policies isolating CDE pods
- No privileged containers in CDE
- Secrets management via external vault (not Kubernetes secrets)
- Service mesh (Istio, Linkerd) with mTLS for CDE pod-to-pod traffic
- Runtime security monitoring (Falco, Sysdig)

### API Security for Payment APIs

- OAuth 2.0 / OpenID Connect for API authentication
- API rate limiting and throttling
- Input validation and output encoding for all API parameters
- API gateway with WAF protection
- API versioning with deprecated version retirement
- Mutual TLS for server-to-server API calls
- PCI-compliant API logging (mask PAN in logs)
- API security testing (DAST) in CI/CD pipeline

### Tokenization Architecture

```
┌───────────────┐     ┌──────────────────┐     ┌────────────────┐
│   Customer     │────▶│   Payment Page    │────▶│ Token Service  │
│   (Browser)    │     │   (Merchant)      │     │ (Processor)    │
└───────────────┘     └──────────────────┘     └──────┬─────────┘
                                                       │
                                              ┌────────▼────────┐
                                              │   Token Vault    │
                                              │   (PAN → Token)  │
                                              └────────┬────────┘
                                                       │
                                              ┌────────▼────────┐
                                              │  Card Network    │
                                              │  (Detokenize)    │
                                              └─────────────────┘
```

**Key Points:**
- Token format should be indistinguishable from PAN (same length, passes Luhn check is optional)
- Token vault must be PCI DSS compliant
- Tokens should be non-reversible without access to the vault
- Use format-preserving tokens when legacy systems require card-like values

### Encryption Key Management

**DUKPT (Derived Unique Key Per Transaction):**
- Used in POS environments
- Each transaction uses a unique encryption key
- Derived from a Base Derivation Key (BDK)
- Protects against mass compromise from single key exposure

**P2PE (Point-to-Point Encryption):**
- Encrypts at the terminal (point of interaction)
- Decrypts only at the processor's secure environment
- Validated P2PE solutions listed on PCI SSC website
- Significantly reduces merchant's CDE scope

**Key Lifecycle:**
- Generation: Use HSM or certified key generation
- Distribution: Split knowledge, dual control
- Storage: HSM or encrypted key storage
- Usage: Track key usage and enforce permitted operations
- Rotation: Annual rotation minimum; immediately upon suspected compromise
- Destruction: Cryptographic erase with verification

---

## PCI DSS Compliance Roadmap

### Phase 1: Scope and Assess (Months 1-2)

1. **Determine Merchant/SP Level** — Transaction volume determines assessment type
2. **Define CDE Scope** — Map all systems that store, process, or transmit CHD
3. **Identify SAQ Type** — Use the scope analyzer tool
4. **Conduct Gap Assessment** — Use the compliance checker tool
5. **Document Scope** — Create CDE inventory and data flow diagram

**Deliverables:**
- CDE scope document with data flow diagrams
- Gap assessment report with prioritized findings
- SAQ type determination
- Project plan and budget estimate

### Phase 2: Quick Wins and Critical Gaps (Months 3-4)

1. **Stop storing SAD** — Eliminate any storage of CVV, track data, PIN immediately
2. **Enable MFA for CDE** — Deploy MFA for all CDE access (Req 8.4.2)
3. **Enable encryption** — Encrypt stored PAN and PAN in transit (Req 3, 4)
4. **Deploy logging** — Centralize logs from CDE systems (Req 10)
5. **Update passwords** — Enforce 12-character minimum (Req 8.3.6)

### Phase 3: Core Controls (Months 5-7)

1. **Network segmentation** — Isolate CDE, deploy firewalls, restrict traffic (Req 1)
2. **Hardening** — Apply CIS Benchmarks to all CDE systems (Req 2)
3. **Access controls** — Implement RBAC, least privilege, access reviews (Req 7)
4. **Vulnerability management** — Deploy scanning, establish patch SLAs (Req 6, 11)
5. **Anti-malware** — Deploy EDR/XDR, anti-phishing controls (Req 5)

### Phase 4: Advanced Controls (Months 8-10)

1. **WAF deployment** — Deploy in blocking mode for payment web apps (Req 6.4.2)
2. **Payment page security** — Manage scripts, deploy tamper detection (Req 6.4.3, 11.6.1)
3. **Penetration testing** — External and internal pen tests (Req 11.4)
4. **IDS/IPS** — Deploy at CDE perimeter and internal segments (Req 11.5)
5. **Physical security** — Secure data centers, POS terminals, media (Req 9)

### Phase 5: Policy, Training, and Validation (Months 11-12)

1. **Security policy** — Comprehensive policy covering all 12 requirements (Req 12)
2. **Awareness training** — Deploy training program with phishing simulation (Req 12.6)
3. **Third-party management** — Assess and document all TPSPs (Req 12.8)
4. **Incident response** — Develop and test IRP (Req 12.10)
5. **Formal assessment** — Complete SAQ or schedule QSA for ROC
