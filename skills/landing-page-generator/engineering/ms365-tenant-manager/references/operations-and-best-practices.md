# Operations, Best Practices & Troubleshooting

Read this when hardening a tenant, reviewing anti-patterns, resolving errors, or checking the success bar / prerequisites.

## Best Practices

### Tenant Setup

1. Enable MFA before adding users
2. Configure named locations for Conditional Access
3. Use separate admin accounts with PIM
4. Verify custom domains before bulk user creation
5. Apply Microsoft Secure Score recommendations

### Security Operations

1. Start Conditional Access policies in report-only mode
2. Use `-WhatIf` parameter before executing scripts
3. Never hardcode credentials in scripts
4. Enable audit logging for all operations
5. Regular quarterly security reviews

### PowerShell Automation

1. Prefer Microsoft Graph over legacy MSOnline modules
2. Include try/catch blocks for error handling
3. Implement logging for audit trails
4. Use Azure Key Vault for credential management
5. Test in non-production tenant first

---

## Limitations

| Constraint | Impact |
|------------|--------|
| Global Admin required | Full tenant setup needs highest privilege |
| API rate limits | Bulk operations may be throttled |
| License dependencies | E3/E5 required for advanced features |
| Hybrid scenarios | On-premises AD needs additional configuration |
| PowerShell prerequisites | Microsoft.Graph module required |

### Required PowerShell Modules

```powershell
Install-Module Microsoft.Graph -Scope CurrentUser
Install-Module ExchangeOnlineManagement -Scope CurrentUser
Install-Module MicrosoftTeams -Scope CurrentUser
```

### Required Permissions

- **Global Administrator** - Full tenant setup
- **User Administrator** - User management
- **Security Administrator** - Security policies
- **Exchange Administrator** - Mailbox management

---

## Anti-Patterns

- **Using admin accounts for daily work** -- Global Admin accounts should use PIM (Privileged Identity Management) with JIT activation; use separate accounts for daily tasks
- **Skipping report-only mode** -- deploying Conditional Access policies directly to enforcement blocks legitimate users; always validate in report-only mode first
- **Hardcoding credentials in scripts** -- PowerShell scripts with embedded passwords are security incidents waiting to happen; use Azure Key Vault or environment variables
- **Using legacy MSOnline module** -- MSOnline is deprecated; all new scripts should use Microsoft Graph (`Connect-MgGraph`)
- **No break-glass account** -- excluding zero accounts from CA policies means a misconfiguration can lock out all admins; maintain at least one excluded emergency access account
- **Bulk operations without -WhatIf** -- running bulk user creation or license assignment without dry-run risks mass misconfiguration; always test with `-WhatIf` first

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `Connect-MgGraph` fails with "Insufficient privileges" | App registration missing required API permissions | Grant `Directory.ReadWrite.All`, `User.ReadWrite.All`, and `Policy.ReadWrite.ConditionalAccess` in Azure AD > App Registrations > API Permissions, then admin-consent |
| Bulk user creation silently skips users | CSV `UserPrincipalName` column missing or domain not verified in tenant | Verify custom domain is added and set as default; ensure CSV header matches exactly `UserPrincipalName` |
| License assignment returns "No available licenses" | All purchased seats consumed or SKU part number misspelled | Run `Get-MgSubscribedSku -All` to confirm `SkuPartNumber` and check `PrepaidUnits.Enabled - ConsumedUnits > 0` |
| Conditional Access policy created but not enforcing MFA | Policy state defaults to `enabledForReportingButNotEnforced` (report-only) | After validating sign-in logs, update policy state to `enabled` in Azure AD > Security > Conditional Access |
| Offboarding script fails at mailbox conversion | Exchange Online Management module not connected or mailbox already shared | Run `Connect-ExchangeOnline` before executing; check mailbox type with `Get-Mailbox -Identity user@domain.com` |
| DNS records configured but mail not flowing | MX record DNS propagation incomplete or SPF record missing `-all` suffix | Wait up to 48 hours for propagation; validate with `nslookup -type=MX domain.com` and confirm SPF ends with `-all` |
| Security audit reports empty CSV files | Microsoft Graph scopes not consented or audit log ingestion not enabled | Run `Set-AdminAuditLogConfig -UnifiedAuditLogIngestionEnabled $true` and re-consent scopes with `Connect-MgGraph -Scopes "AuditLog.Read.All"` |

---

## Success Criteria

- 100% of provisioned users have correct license SKU assigned matching their role and department
- Zero orphaned accounts: every disabled user has licenses removed, mailbox converted to shared, and sessions revoked within 24 hours of offboarding
- MFA enforcement covers 100% of enabled user accounts, verified by security audit script output showing zero users without MFA
- DNS records pass validation for all five service types (MX, SPF, DKIM, autodiscover, device registration) with zero propagation errors
- Conditional Access policies achieve report-only validation with less than 1% false-positive block rate before enforcement
- License utilization stays above 90% across all SKUs, with unused licenses identified and reclaimed quarterly
- Security audit generates complete CSV reports for all 7 audit categories (MFA, admin roles, inactive users, guests, licenses, mailbox delegations, Conditional Access) with zero script errors
