# Tools, Quick Start & Workflows

Read this when running the generator scripts, wiring up the import-based Python API, or executing an end-to-end tenant operation (setup, hardening, offboarding).

## Quick Start

### Generate Security Audit Script

```bash
python scripts/powershell_generator.py --action audit --output audit_script.ps1
```

### Create Bulk User Provisioning Script

```bash
python scripts/user_management.py --action provision --csv users.csv --license E3
```

### Configure Conditional Access Policy

```bash
python scripts/powershell_generator.py --action conditional-access --require-mfa --include-admins
```

---

## Tools

### powershell_generator.py

Generates ready-to-use PowerShell scripts for Microsoft 365 administration.

**Usage:**

```bash
# Generate security audit script
python scripts/powershell_generator.py --action audit

# Generate Conditional Access policy script
python scripts/powershell_generator.py --action conditional-access \
  --policy-name "Require MFA for Admins" \
  --require-mfa \
  --include-users "All"

# Generate bulk license assignment script
python scripts/powershell_generator.py --action license \
  --csv users.csv \
  --sku "ENTERPRISEPACK"
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--action` | Yes | Script type: `audit`, `conditional-access`, `license`, `users` |
| `--policy-name` | No | Name for Conditional Access policy |
| `--require-mfa` | No | Require MFA in policy |
| `--include-users` | No | Users to include: `All` or specific UPNs |
| `--csv` | No | CSV file path for bulk operations |
| `--sku` | No | License SKU for assignment |
| `--output` | No | Output file path (default: stdout) |

**Output:** Complete PowerShell scripts with error handling, logging, and best practices.

### user_management.py

Automates user lifecycle operations and bulk provisioning.

**Usage:**

```bash
# Provision users from CSV
python scripts/user_management.py --action provision --csv new_users.csv

# Offboard user securely
python scripts/user_management.py --action offboard --user john.doe@company.com

# Generate inactive users report
python scripts/user_management.py --action report-inactive --days 90
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--action` | Yes | Operation: `provision`, `offboard`, `report-inactive`, `sync` |
| `--csv` | No | CSV file for bulk operations |
| `--user` | No | Single user UPN |
| `--days` | No | Days for inactivity threshold (default: 90) |
| `--license` | No | License SKU to assign |

### tenant_setup.py

Initial tenant configuration and service provisioning automation.

**Usage:**

```bash
# Generate tenant setup checklist
python scripts/tenant_setup.py --action checklist --company "Acme Inc" --users 50

# Generate DNS records configuration
python scripts/tenant_setup.py --action dns --domain acme.com

# Generate security baseline script
python scripts/tenant_setup.py --action security-baseline
```

---

## Workflows

### Workflow 1: New Tenant Setup

**Step 1: Generate Setup Checklist**

```bash
python scripts/tenant_setup.py --action checklist --company "Company Name" --users 100
```

**Step 2: Configure DNS Records**

```bash
python scripts/tenant_setup.py --action dns --domain company.com
```

**Step 3: Apply Security Baseline**

```bash
python scripts/powershell_generator.py --action audit > initial_audit.ps1
```

**Step 4: Provision Users**

```bash
python scripts/user_management.py --action provision --csv employees.csv --license E3
```

### Workflow 2: Security Hardening

**Step 1: Run Security Audit**

```bash
python scripts/powershell_generator.py --action audit --output security_audit.ps1
```

**Step 2: Create MFA Policy**

```bash
python scripts/powershell_generator.py --action conditional-access \
  --policy-name "Require MFA All Users" \
  --require-mfa \
  --include-users "All"
```

**Step 3: Review Results**

Execute generated scripts and review CSV reports in output directory.

### Workflow 3: User Offboarding

**Step 1: Generate Offboarding Script**

```bash
python scripts/user_management.py --action offboard --user departing.user@company.com
```

**Step 2: Execute Script with -WhatIf**

```powershell
.\offboard_user.ps1 -WhatIf
```

**Step 3: Execute for Real**

```powershell
.\offboard_user.ps1 -Confirm:$false
```

---

## Tool Reference

### powershell_generator.py

**Purpose:** Generates production-ready PowerShell scripts for Microsoft 365 administration including security audits, Conditional Access policies, and bulk license assignment.

**Module:** `PowerShellScriptGenerator` class (import and instantiate, not a CLI tool)

**Initialization:**

```python
from powershell_generator import PowerShellScriptGenerator

generator = PowerShellScriptGenerator(tenant_domain="company.com")
```

**Methods:**

#### `generate_security_audit_script()`

Generates a comprehensive 7-category security audit PowerShell script that checks MFA status, admin role assignments, inactive users, guest users, license usage, mailbox delegations, and Conditional Access policies.

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| *(none)* | -- | -- | Uses `tenant_domain` from constructor |

**Example:**

```python
generator = PowerShellScriptGenerator("company.com")
script = generator.generate_security_audit_script()
print(script)  # Complete PowerShell script with Connect-MgGraph, 7 audit checks, CSV export
```

**Output:** PowerShell script string that produces CSV reports in a timestamped `SecurityAudit_` directory: `MFA_Status.csv`, `Admin_Roles.csv`, `Inactive_Users.csv`, `Guest_Users.csv`, `License_Usage.csv`, `Mailbox_Delegations.csv`, `ConditionalAccess_Policies.csv`.

#### `generate_conditional_access_policy_script(policy_config)`

Generates a PowerShell script to create a Conditional Access policy in report-only mode.

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `policy_config` | Yes | `Dict[str, Any]` | Policy configuration dictionary |
| `policy_config["name"]` | No | `str` | Policy display name (default: `"MFA Policy"`) |
| `policy_config["require_mfa"]` | No | `bool` | Whether to require MFA (default: `True`) |
| `policy_config["include_users"]` | No | `str` | Users to include (default: `"All"`) |
| `policy_config["exclude_users"]` | No | `List[str]` | UPNs to exclude (default: `[]`) |

**Example:**

```python
script = generator.generate_conditional_access_policy_script({
    "name": "Require MFA for Admins",
    "require_mfa": True,
    "include_users": "All",
    "exclude_users": ["breakglass@company.com"]
})
```

**Output:** PowerShell script string that creates a Conditional Access policy via `New-MgIdentityConditionalAccessPolicy` in `enabledForReportingButNotEnforced` state.

#### `generate_bulk_license_assignment_script(users_csv_path, license_sku)`

Generates a PowerShell script for assigning a license SKU to users listed in a CSV file.

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `users_csv_path` | Yes | `str` | Path to CSV file (must contain `UserPrincipalName` column) |
| `license_sku` | Yes | `str` | License SKU part number (e.g., `"ENTERPRISEPACK"` for E3) |

**Example:**

```python
script = generator.generate_bulk_license_assignment_script("users.csv", "ENTERPRISEPACK")
```

**Output:** PowerShell script string that imports the CSV, checks for existing licenses, assigns the specified SKU, and exports results to `LicenseAssignment_Results_<timestamp>.csv` with `Status` and `Message` columns.

---

### user_management.py

**Purpose:** Manages user lifecycle operations including bulk provisioning, secure offboarding, license recommendations, group membership, and data validation.

**Module:** `UserLifecycleManager` class (import and instantiate, not a CLI tool)

**Initialization:**

```python
from user_management import UserLifecycleManager

manager = UserLifecycleManager(domain="company.com")
```

**Methods:**

#### `generate_user_creation_script(users)`

Generates a PowerShell script for bulk user provisioning with license assignment.

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `users` | Yes | `List[Dict[str, Any]]` | List of user dictionaries |
| `users[].username` | Yes | `str` | Username (without domain) |
| `users[].display_name` | Yes | `str` | Full display name |
| `users[].first_name` | Yes | `str` | Given name |
| `users[].last_name` | Yes | `str` | Surname |
| `users[].job_title` | No | `str` | Job title |
| `users[].department` | No | `str` | Department name |
| `users[].license_sku` | No | `str` | License SKU (default: `"Microsoft_365_Business_Standard"`) |

**Example:**

```python
script = manager.generate_user_creation_script([
    {"username": "jdoe", "display_name": "Jane Doe", "first_name": "Jane",
     "last_name": "Doe", "job_title": "Engineer", "department": "Engineering",
     "license_sku": "ENTERPRISEPACK"}
])
```

**Output:** PowerShell script string that creates users via `New-MgUser`, assigns licenses, and exports results to `UserCreation_Results_<timestamp>.csv`.

#### `generate_user_offboarding_script(user_email)`

Generates a comprehensive 11-step secure offboarding PowerShell script.

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `user_email` | Yes | `str` | UPN of the user to offboard |

**Example:**

```python
script = manager.generate_user_offboarding_script("john.doe@company.com")
```

**Output:** PowerShell script string that disables sign-in, revokes sessions, removes group memberships, removes devices, converts mailbox to shared, sets auto-reply, removes licenses, hides from GAL, and exports an offboarding report CSV.

#### `generate_license_assignment_recommendations(user_role, department)`

Returns license recommendation based on role and department matching.

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `user_role` | Yes | `str` | Job title or role (matched against keywords: CEO, CTO, admin, manager, contractor, etc.) |
| `department` | Yes | `str` | Department name (matched against: legal, finance, hr, accounting) |

**Example:**

```python
rec = manager.generate_license_assignment_recommendations("Security Analyst", "IT")
# Returns: {"recommended_license": "Microsoft 365 E5", "justification": "...", "features_needed": [...], "monthly_cost": 57.00}
```

**Output:** Dictionary with `recommended_license`, `justification`, `features_needed` (list), and `monthly_cost` (float).

#### `generate_group_membership_recommendations(user)`

Recommends security and distribution groups based on user attributes.

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `user` | Yes | `Dict[str, Any]` | User dictionary with `department`, `location`, `job_title`, `needs_sharepoint_access`, `needs_project_access` |

**Example:**

```python
groups = manager.generate_group_membership_recommendations({
    "department": "Engineering", "location": "NYC", "job_title": "Director of Engineering"
})
# Returns: ["DL-Engineering", "SG-Engineering", "SG-Location-Nyc", "SG-Management"]
```

**Output:** List of recommended group name strings using naming conventions `DL-` (distribution list), `SG-` (security group).

#### `validate_user_data(user_data)`

Validates user data before provisioning, checking required fields, username format, and email format.

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `user_data` | Yes | `Dict[str, Any]` | Dictionary with `first_name`, `last_name`, `username` (required); `email`, `display_name`, `license_sku` (optional) |

**Example:**

```python
result = manager.validate_user_data({"first_name": "Jane", "last_name": "Doe", "username": "jdoe"})
# Returns: {"is_valid": True, "errors": [], "warnings": ["Display name not provided, will use: Jane Doe", ...]}
```

**Output:** Dictionary with `is_valid` (bool), `errors` (list of strings), and `warnings` (list of strings).

---

### tenant_setup.py

**Purpose:** Manages initial Microsoft 365 tenant configuration including setup checklists, DNS record generation, PowerShell setup scripts, and license distribution recommendations.

**Module:** `TenantSetupManager` class (import and instantiate, not a CLI tool)

**Initialization:**

```python
from tenant_setup import TenantSetupManager

manager = TenantSetupManager(tenant_config={
    "company_name": "Acme Inc",
    "domain_name": "acme.com",
    "user_count": 50,
    "industry": "technology",
    "compliance_requirements": ["GDPR"],  # optional: "GDPR", "HIPAA"
    "licenses": {}
})
```

| Config Key | Required | Type | Description |
|------------|----------|------|-------------|
| `company_name` | Yes | `str` | Organization display name |
| `domain_name` | Yes | `str` | Primary custom domain |
| `user_count` | Yes | `int` | Total expected user count |
| `industry` | No | `str` | Industry vertical (default: `"general"`) |
| `compliance_requirements` | No | `List[str]` | Compliance frameworks: `"GDPR"`, `"HIPAA"` |
| `licenses` | No | `Dict` | Existing license inventory |

**Methods:**

#### `generate_setup_checklist()`

Generates a phased tenant setup checklist (4-5 phases depending on compliance requirements).

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| *(none)* | -- | -- | Uses constructor config |

**Example:**

```python
checklist = manager.generate_setup_checklist()
# Returns list of phase dicts, each with "phase", "name", "priority", "tasks"
```

**Output:** List of dictionaries. Each phase contains `phase` (int), `name` (str), `priority` (`"critical"` or `"high"`), and `tasks` (list of dicts with `task`, `details`, `estimated_time`). Phases: Initial Configuration, Custom Domain, Security Baseline, Service Configuration, and optionally Compliance Configuration.

#### `generate_dns_records()`

Generates all required DNS records for Microsoft 365 services.

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| *(none)* | -- | -- | Uses `domain_name` from constructor |

**Example:**

```python
records = manager.generate_dns_records()
# Keys: "mx_records", "txt_records", "cname_records", "srv_records"
```

**Output:** Dictionary with four keys, each containing a list of record dictionaries with `type`, `name`, `value`, `ttl`, `purpose`, and record-type-specific fields (`priority` for MX/SRV, `port`/`weight` for SRV).

#### `generate_powershell_setup_script()`

Generates a complete PowerShell script for initial tenant configuration covering Graph, Exchange Online, SharePoint, and Teams.

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| *(none)* | -- | -- | Uses constructor config |

**Example:**

```python
script = manager.generate_powershell_setup_script()
print(script)  # PowerShell script connecting to Graph, Exchange, Teams with 7 setup steps
```

**Output:** PowerShell script string that connects to Microsoft Graph, Exchange Online, and Teams; configures organization settings, security defaults, audit logging, Exchange policies, and Teams messaging policies.

#### `get_license_recommendations()`

Calculates license distribution recommendations and cost estimates based on user count and compliance requirements.

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| *(none)* | -- | -- | Uses `user_count` and `compliance_requirements` from constructor |

**Example:**

```python
recs = manager.get_license_recommendations()
# Returns: {"recommendations": {...}, "suggested_distribution": {"E5": 5, "E3": 10, ...},
#           "estimated_monthly_cost": 1234.50, "estimated_annual_cost": 14814.00}
```

**Output:** Dictionary with `recommendations` (license tier details), `suggested_distribution` (dict mapping SKU tier to user count), `estimated_monthly_cost` (float), and `estimated_annual_cost` (float). Distribution adjusts automatically when compliance requirements are specified.
