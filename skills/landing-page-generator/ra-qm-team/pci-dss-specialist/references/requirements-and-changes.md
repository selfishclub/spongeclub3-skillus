# PCI DSS v4.0 Overview, 12 Requirements Deep-Dive, and v4.0 Changes

Read this when you need the narrative explanation of PCI DSS, the objective and implementation guidance for each of the 12 requirements, or a summary of what changed from v3.2.1 (including the future-dated requirements now mandatory). For the tabular sub-requirement / testing-procedure reference, see [pci-dss-requirements-guide.md](pci-dss-requirements-guide.md).

---

## PCI DSS v4.0 Overview

### What Is PCI DSS?

The Payment Card Industry Data Security Standard (PCI DSS) is a global security standard developed by the PCI Security Standards Council (PCI SSC), founded by American Express, Discover, JCB, Mastercard, and Visa. It applies to all entities that store, process, or transmit cardholder data (CHD) or sensitive authentication data (SAD).

### PCI DSS v4.0 Timeline

| Date | Milestone |
|------|-----------|
| March 2022 | PCI DSS v4.0 published |
| March 2024 | v3.2.1 retired; v4.0 is the only active version |
| March 31, 2025 | All future-dated requirements become mandatory |

**All organizations must now comply with the full PCI DSS v4.0 standard, including all previously future-dated requirements.**

### What Data Is Protected

**Cardholder Data (CHD):**
- Primary Account Number (PAN) — the credit/debit card number
- Cardholder Name (when stored with PAN)
- Service Code
- Expiration Date

**Sensitive Authentication Data (SAD):** Must NEVER be stored after authorization, even if encrypted.
- Full track data (magnetic stripe, chip)
- CVV/CVC/CAV2/CID (card verification codes)
- PIN and PIN block

---

## 12 Requirements Deep-Dive

### Requirement 1: Install and Maintain Network Security Controls

**Objective:** Protect the cardholder data environment through network security controls.

**Key Sub-Requirements:**
- **1.2.1** — Network security controls (NSCs) are configured and maintained
- **1.2.5** — All services, protocols, and ports allowed are identified and approved
- **1.2.8** — NSC configuration files are secured and synchronized
- **1.3.1** — Inbound traffic to the CDE is restricted to only necessary traffic
- **1.3.2** — Outbound traffic from the CDE is restricted to only necessary traffic
- **1.4.1** — NSCs are implemented between trusted and untrusted networks
- **1.4.5** — Disclosure of internal IP addresses is prevented
- **1.5.1** — Security controls on all computing devices connecting via untrusted networks

**Implementation Guidance:**
- Deploy next-generation firewalls (NGFW) at CDE boundaries
- Implement Web Application Firewalls (WAF) for web-facing payment applications
- Use network segmentation to isolate CDE from corporate network
- Restrict inbound to CDE: only necessary ports/protocols from known sources
- Restrict outbound from CDE: only approved destinations (payment processor, updates)
- Document all firewall rules with business justification
- Review firewall rules at least every 6 months
- Implement micro-segmentation where possible

---

### Requirement 2: Apply Secure Configurations to All System Components

**Objective:** Ensure all systems are configured securely with no unnecessary default settings.

**Key Sub-Requirements:**
- **2.2.1** — Configuration standards developed for all system components
- **2.2.2** — Vendor default accounts managed (changed, disabled, or removed)
- **2.2.3** — Primary functions requiring different security levels are managed (one primary function per server or use containerization)
- **2.2.4** — Only necessary services, protocols, daemons, and functions are enabled
- **2.2.5** — Insecure services are secured if present
- **2.2.6** — System security parameters are configured to prevent misuse
- **2.2.7** — Non-console administrative access is encrypted

**Implementation Guidance:**
- Apply CIS Benchmarks as baseline configurations
- Change ALL vendor default passwords before deployment
- Remove or disable unnecessary services, protocols, and daemon
- Harden operating systems using DISA STIGs or CIS Benchmarks
- Enforce encrypted administrative access (SSH, HTTPS, TLS 1.2+)
- Use configuration management tools for consistency (Ansible, Chef, Puppet)
- Deploy from hardened golden images

---

### Requirement 3: Protect Stored Account Data

**Objective:** Minimize stored data and protect it with strong cryptography.

**Key Sub-Requirements:**
- **3.2.1** — Data retention and disposal policies implemented
- **3.3.1** — SAD not retained after authorization (even if encrypted)
- **3.3.2** — SAD that is stored before authorization is encrypted using strong cryptography
- **3.4.1** — PAN is masked when displayed (show only first 6 and last 4 digits max)
- **3.5.1** — PAN is rendered unreadable anywhere it is stored (encryption, tokenization, truncation, or hashing)
- **3.6.1** — Cryptographic key management procedures are defined and implemented
- **3.7.1-3.7.9** — Comprehensive key management lifecycle

**Implementation Guidance:**
- Minimize PAN storage — do not store unless absolutely necessary
- Use tokenization to replace PANs with non-reversible tokens
- Encrypt stored PAN with AES-256 (or equivalent)
- Never store SAD (CVV, track data, PIN) after authorization — period
- Mask PAN in all displays: show max first 6 / last 4 digits
- Implement HSM-based key management for encryption keys
- Rotate encryption keys at least annually
- Use split knowledge and dual control for key management
- Maintain key inventory with custodian assignments
- Use DUKPT or ANSI X9.24 for key management in POS environments

**Tokenization vs Encryption Decision:**

| Factor | Tokenization | Encryption |
|--------|-------------|------------|
| Reversibility | Non-reversible (preferred) | Reversible with key |
| Scope reduction | Removes systems from CDE scope | Systems remain in scope |
| Performance | Faster lookup (token maps) | Encryption/decryption overhead |
| Use case | Card-on-file, recurring billing | Data that must be recovered |
| Recommendation | Prefer tokenization when possible | Use when PAN recovery is required |

---

### Requirement 4: Protect Cardholder Data with Strong Cryptography During Transmission

**Objective:** Encrypt CHD whenever transmitted over open, public networks.

**Key Sub-Requirements:**
- **4.2.1** — Strong cryptography and security protocols protect CHD during transmission over open, public networks
- **4.2.1.1** — Trusted certificates for PAN transmission over open, public networks
- **4.2.1.2** — Wireless networks transmitting PAN use industry best practices for strong cryptography
- **4.2.2** — PAN is secured with strong cryptography whenever sent via end-user messaging technologies

**Implementation Guidance:**
- Use TLS 1.2 as minimum, prefer TLS 1.3
- Disable SSL, TLS 1.0, TLS 1.1 entirely
- Use strong cipher suites (ECDHE key exchange, AES-GCM)
- Implement certificate pinning for mobile payment apps
- Deploy HSTS (HTTP Strict Transport Security) on all payment pages
- Use mTLS (mutual TLS) between internal CDE components
- Monitor certificate expiration and automate renewal
- Never send PAN via email, chat, or SMS unencrypted

---

### Requirement 5: Protect All Systems and Networks from Malicious Software

**Objective:** Defend all systems against malware.

**Key Sub-Requirements:**
- **5.2.1** — Anti-malware solution(s) deployed on all system components
- **5.2.2** — Anti-malware solution performs periodic and real-time scans
- **5.2.3** — For systems not commonly affected by malware, periodic evaluations performed
- **5.3.1** — Anti-malware mechanisms are kept current
- **5.3.2** — Anti-malware performs periodic and real-time scans
- **5.3.3** — For removable media, anti-malware scans automatically upon insertion
- **5.3.4** — Audit logs for anti-malware are enabled and retained
- **5.3.5** — Anti-malware cannot be disabled or altered by users (except case-by-case with management approval for limited time, logged)
- **5.4.1** — Mechanisms detect and protect against phishing attacks

**Implementation Guidance:**
- Deploy EDR/XDR on all endpoints (workstations, servers, POS terminals)
- Ensure real-time scanning with automatic definition updates
- Enable email-based anti-phishing controls (SPF, DKIM, DMARC, sandbox)
- Implement application allowlisting on POS and critical CDE systems
- Log all anti-malware events and integrate with SIEM
- For Linux/Unix systems: document risk evaluation and deploy appropriate controls

---

### Requirement 6: Develop and Maintain Secure Systems and Software

**Objective:** Protect against vulnerabilities through secure development and timely patching.

**Key Sub-Requirements:**
- **6.2.1** — Custom software developed securely (OWASP, CERT, SANS)
- **6.2.2** — Developer training in secure coding at least annually
- **6.2.3** — Custom software reviewed before release to identify vulnerabilities
- **6.2.4** — Software engineering techniques prevent common vulnerabilities (OWASP Top 10)
- **6.3.1** — Security vulnerabilities identified and managed (vulnerability management process)
- **6.3.2** — Software inventory maintained to enable vulnerability management
- **6.3.3** — Critical and high vulnerabilities patched within defined timeframes
- **6.4.1** — Public-facing web apps protected against known attacks (WAF or code review)
- **6.4.2** — Public-facing web apps have automated technical solution to detect and prevent web-based attacks (WAF in blocking mode)
- **6.4.3** — All payment page scripts managed, authorized, and integrity-ensured
- **6.5.1-6.5.6** — Change management procedures for all CDE system changes

**Implementation Guidance:**
- Implement SDLC with security gates (design review, code review, security testing)
- Train developers annually on secure coding (OWASP Top 10, CWE/SANS Top 25)
- Deploy WAF in blocking mode for all public-facing payment applications
- Patch critical vulnerabilities within 30 days, high within 60 days
- Implement Content Security Policy (CSP) and Subresource Integrity (SRI) for payment pages
- Monitor and authorize all JavaScript on payment pages (6.4.3 is critical for e-commerce)
- Conduct code reviews (manual or automated SAST) for all custom payment code
- Maintain complete software inventory with versions

---

### Requirement 7: Restrict Access to System Components and Cardholder Data by Business Need to Know

**Objective:** Limit access to CHD to only those with a legitimate business need.

**Key Sub-Requirements:**
- **7.2.1** — Access control model defined and includes all system components
- **7.2.2** — Access assigned based on job classification and function
- **7.2.3** — Required privileges approved by authorized personnel
- **7.2.4** — All user accounts and related access privileges reviewed at least every 6 months
- **7.2.5** — All application and system accounts assigned and managed based on least privilege
- **7.2.5.1** — Access for application and system accounts reviewed periodically
- **7.2.6** — All user access to query repositories of stored CHD is restricted

**Implementation Guidance:**
- Implement role-based access control (RBAC) for all CDE systems
- Document access control policy with defined roles and permissions
- Enforce least privilege — users get minimum access needed
- Review all CDE access every 6 months and recertify
- Restrict database query access to CHD (no ad hoc SELECT * from card_data)
- Separate duties — no single person should control all aspects of a transaction
- Use automated identity governance for access provisioning and reviews

---

### Requirement 8: Identify Users and Authenticate Access to System Components

**Objective:** Ensure all access to CDE is identified and strongly authenticated.

**Key Sub-Requirements:**
- **8.2.1** — All users assigned a unique ID before access
- **8.2.2** — Group, shared, or generic accounts not used (exceptions must be documented)
- **8.3.1** — All user access to CDE authenticated with at least one factor
- **8.3.2** — Strong cryptography used for all authentication factors
- **8.3.4** — Invalid authentication attempts limited (lockout after max 10 attempts for min 30 minutes)
- **8.3.6** — New passwords/passphrases: minimum 12 characters (or 8 if system cannot support 12), containing both numeric and alphabetic
- **8.3.9** — Passwords/passphrases changed at least every 90 days (or continuous risk-based approach)
- **8.4.1** — MFA implemented for all non-console access into CDE for administrative access
- **8.4.2** — MFA implemented for all access into the CDE
- **8.4.3** — MFA for all remote network access originating from outside the entity's network
- **8.5.1** — MFA implementation not susceptible to replay attacks, cannot be bypassed
- **8.6.1** — Interactive login for system/service accounts managed, disabled when not needed
- **8.6.2** — Passwords/passphrases for system/service accounts not hard-coded in scripts
- **8.6.3** — Passwords/passphrases for system/service accounts changed periodically and upon suspicion of compromise

**Implementation Guidance:**
- MFA is mandatory for ALL access into the CDE (not just admin) — this is a v4.0 change
- Use phishing-resistant MFA (FIDO2/WebAuthn, hardware keys) where possible
- Minimum 12-character passwords with complexity requirements
- Implement account lockout after 10 failed attempts
- Never use shared accounts in the CDE
- Manage service accounts — no hard-coded passwords, rotate periodically
- Deploy PAM for administrative access to CDE systems
- Log all authentication events and integrate with SIEM

---

### Requirement 9: Restrict Physical Access to Cardholder Data

**Objective:** Prevent unauthorized physical access to systems that store, process, or transmit CHD.

**Key Sub-Requirements:**
- **9.2.1** — Appropriate facility entry controls for CDE
- **9.2.3** — Physical access to wireless access points, gateways, and networking devices restricted
- **9.2.4** — Console access to sensitive areas controlled
- **9.3.1** — Authorization for physical access reviewed at least every 6 months
- **9.3.2** — Procedures for visitor identification and management
- **9.3.3** — Visitor badges or identification surrendered upon departure
- **9.4.1** — Media with CHD physically secured
- **9.4.5** — Inventory of electronic media with CHD maintained
- **9.4.6** — Hard-copy materials with CHD destroyed when no longer needed (cross-cut shred, incinerate)
- **9.4.7** — Electronic media with CHD rendered unrecoverable (degauss, crypto-erase, destroy)
- **9.5.1** — POI (Point of Interaction) devices protected from tampering and substitution

**Implementation Guidance:**
- Implement badge access to server rooms and data centers housing CDE
- Deploy CCTV with 90-day retention for CDE physical locations
- Maintain visitor logs with escort requirements
- Inspect POS terminals regularly for skimming devices (daily/weekly)
- Cross-cut shred all paper containing CHD
- Cryptographically erase or physically destroy media before disposal
- Restrict access to network infrastructure components

---

### Requirement 10: Log and Monitor All Access to System Components and Cardholder Data

**Objective:** Create comprehensive audit trails for all access to CDE and CHD.

**Key Sub-Requirements:**
- **10.2.1** — Audit logs capture all individual user access to CHD
- **10.2.1.1** — Audit logs capture all individual access to CHD
- **10.2.1.2** — All actions by any individual with administrative access are logged
- **10.2.1.3** — Access to all audit logs
- **10.2.1.4** — Invalid logical access attempts
- **10.2.1.5** — Changes to identification and authentication mechanisms
- **10.2.1.6** — Initialization, stopping, or pausing of audit logs
- **10.2.1.7** — Creation and deletion of system-level objects
- **10.2.2** — Audit logs include required details (user ID, event type, date/time, success/failure, origin, data/component affected)
- **10.3.1** — Read access to audit logs is restricted
- **10.3.2** — Audit log files are protected from modification
- **10.3.3** — Audit log files are backed up to a central log server
- **10.3.4** — File integrity monitoring on audit logs
- **10.4.1** — Audit logs reviewed at least daily for security events
- **10.4.1.1** — Automated mechanisms perform audit log reviews
- **10.4.2** — Logs of all CDE components are reviewed periodically
- **10.5.1** — Retain audit log history for at least 12 months (3 months immediately available)
- **10.6.1** — System clocks synchronized using NTP
- **10.6.2** — Time data protected
- **10.6.3** — Time settings received from industry-accepted sources

**Implementation Guidance:**
- Deploy SIEM for centralized log collection and automated review
- Log all access to CHD, administrative actions, and security events
- Protect log integrity with WORM storage or blockchain-based logging
- Retain logs for 12 months minimum (3 months online, remainder archived)
- Synchronize all system clocks to NTP (stratum 2 or better)
- Review logs daily using automated correlation rules
- Alert on suspicious patterns (multiple failed logins, after-hours access, bulk data access)

---

### Requirement 11: Test Security of Systems and Networks Regularly

**Objective:** Regularly test security controls, systems, and networks to verify they work.

**Key Sub-Requirements:**
- **11.2.1** — Authorized and unauthorized wireless access points managed
- **11.2.2** — Wireless analyzer scans at least quarterly
- **11.3.1** — Internal vulnerability scans at least quarterly
- **11.3.1.1** — All other applicable vulnerabilities (non-critical/high) addressed and rescanned
- **11.3.1.3** — Internal scans after significant changes
- **11.3.2** — External vulnerability scans by ASV at least quarterly
- **11.4.1** — External penetration testing at least annually and after significant changes
- **11.4.3** — Internal penetration testing at least annually and after significant changes
- **11.4.4** — Vulnerabilities found during penetration testing are corrected
- **11.4.5** — Network segmentation tested at least annually (every 6 months for service providers)
- **11.5.1** — IDS/IPS deployed to monitor traffic into and within CDE
- **11.5.1.1** — IDS/IPS alerts generated for suspected compromises
- **11.5.2** — Change-detection mechanism (file integrity monitoring) deployed on critical files
- **11.6.1** — A change and tamper-detection mechanism deployed for payment pages

**Implementation Guidance:**
- Quarterly internal vulnerability scans with all high/critical resolved before pass
- Quarterly external ASV scans (must achieve passing scan)
- Annual external and internal penetration tests (by qualified tester)
- Pen tests must test network layer and application layer
- Deploy IDS/IPS at CDE perimeter and critical internal points
- FIM on critical system files, configuration files, and content files
- Wireless scanning quarterly to detect rogue access points
- Test network segmentation annually to verify CDE isolation
- Deploy change/tamper detection on payment page scripts (ties to 6.4.3)

---

### Requirement 12: Support Information Security with Organizational Policies and Programs

**Objective:** Maintain an information security policy that addresses all PCI DSS requirements.

**Key Sub-Requirements:**
- **12.1.1** — Information security policy established, published, maintained, disseminated
- **12.1.2** — Roles and responsibilities defined for all requirements
- **12.1.3** — Information security policy reviewed at least annually
- **12.2.1** — Acceptable use policies for end-user technologies
- **12.3.1** — Targeted risk analysis for each requirement with customized approach flexibility
- **12.3.2** — Targeted risk analysis for each requirement met with customized approach
- **12.4.1** — Executive management establishes responsibility for protection of CHD
- **12.4.2** — Reviews performed at least quarterly (service providers: operations compliance)
- **12.5.1** — PCI DSS scope documented and confirmed annually
- **12.5.2** — PCI DSS scope documented and confirmed upon significant changes
- **12.5.3** — Significant changes resulting in scope changes trigger assessment
- **12.6.1** — Security awareness program implemented
- **12.6.2** — Awareness program reviewed at least annually
- **12.6.3** — Personnel receive awareness training upon hire and at least annually
- **12.6.3.1** — Training includes awareness of threats (phishing, social engineering)
- **12.8.1-12.8.5** — TPSPs (Third-Party Service Providers) managed
- **12.9.1** — TPSPs acknowledge responsibility for CHD security
- **12.10.1** — Incident response plan created and ready for activation
- **12.10.2** — IRP reviewed and tested at least annually
- **12.10.4** — Personnel with incident response responsibilities are trained
- **12.10.5** — IRP includes monitoring and responding to alerts
- **12.10.6** — IRP is updated based on lessons learned and industry developments
- **12.10.7** — Incident response procedures are in place to respond to detection of stored PAN anywhere not expected

**Implementation Guidance:**
- Create comprehensive security policy covering all 12 requirements
- Conduct targeted risk analysis for any customized approach implementations
- Confirm PCI DSS scope annually and after any significant changes
- Deliver security awareness training at hire and annually
- Include phishing awareness, social engineering, and CHD handling in training
- Manage all third-party service providers (maintain list, require compliance attestation)
- Maintain and test incident response plan at least annually
- Include specific procedures for unauthorized PAN discovery

---

## v4.0 Changes from v3.2.1

### Major Changes

**1. Customized Approach (NEW)**
Organizations can now meet PCI DSS requirements using a "customized approach" rather than the traditional "defined approach." This allows organizations to design their own security controls, provided they meet the security objective of each requirement. Requires targeted risk analysis documentation and validation by QSA.

**2. Targeted Risk Analysis**
v4.0 requires organizations to perform documented, targeted risk analyses for certain requirements (e.g., frequency of activities, password/passphrase policies). This replaces the "one-size-fits-all" approach.

**3. Enhanced Authentication Requirements**
- MFA required for ALL access into the CDE (not just remote admin)
- Minimum password length increased to 12 characters (from 7)
- 90-day password rotation or continuous risk-based authentication

**4. Payment Page Script Security (6.4.3)**
All scripts on payment pages must be managed, authorized, and monitored for integrity. This addresses Magecart-style attacks.

**5. Anti-Phishing Mechanisms (5.4.1)**
Organizations must implement automated anti-phishing mechanisms (e.g., DMARC, email sandbox).

**6. Encryption of PAN Over Trusted Internal Networks (4.2.1)**
PAN must now be encrypted during transmission over ALL networks, not just public networks. Internal network encryption required.

**7. Automated Log Review (10.4.1.1)**
Automated mechanisms must perform audit log reviews — manual-only review no longer sufficient.

### Summary of Future-Dated Requirements (Now Mandatory)

All of the following became mandatory as of March 31, 2025:

| Requirement | What Changed |
|---|---|
| 3.3.2 | SAD encrypted before authorization if stored |
| 3.5.1.2 | Disk-level encryption no longer satisfies requirement (must be above disk) |
| 5.3.3 | Anti-malware scans on removable media |
| 5.4.1 | Anti-phishing mechanisms required |
| 6.3.2 | Software inventory for vulnerability management |
| 6.4.2 | WAF in blocking mode for public web apps |
| 6.4.3 | Payment page script management |
| 8.3.6 | 12-character minimum passwords |
| 8.4.2 | MFA for all CDE access |
| 8.5.1 | MFA replay attack protection |
| 8.6.1-3 | System/service account management |
| 10.4.1.1 | Automated log review |
| 10.7.2 | Detect failures of critical security controls |
| 11.3.1.1 | Manage all vulnerabilities (not just high/critical) |
| 11.4.7 | Multi-tenant service provider pen testing |
| 11.5.1.1 | IDS/IPS alerts for suspected compromise |
| 11.6.1 | Payment page tamper detection |
| 12.3.1 | Targeted risk analysis |
| 12.6.3.1 | Phishing/social engineering in awareness training |
| 12.10.7 | Respond to unexpected stored PAN |
