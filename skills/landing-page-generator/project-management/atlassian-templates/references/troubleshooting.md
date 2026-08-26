# Troubleshooting & Success Criteria

Read this when a deployed template is misbehaving (low adoption, broken macros, version confusion, stale data) or when you need the measurable bar for "this skill did its job."

## Troubleshooting

| Problem | Likely Cause | Resolution |
|---------|-------------|------------|
| Users create pages from scratch instead of using templates | Templates not discoverable, or template names are unclear | Pin templates to space sidebar; use descriptive names (e.g., "Sprint Retro - Team Template"); send periodic reminders with usage links |
| Template produces inconsistent output across teams | Template has too many free-text sections without guidance; teams interpret placeholders differently | Add inline instructions within placeholders; provide a completed example alongside the blank template; standardize section headings |
| Confluence macros in templates break after product updates | Atlassian deprecated or renamed macros in a platform update | Subscribe to Atlassian release notes; test templates in sandbox after major updates; maintain a macro compatibility checklist |
| Template versioning creates confusion about which version to use | Multiple versions coexist without clear deprecation; naming does not indicate version | Use version suffix in template name (e.g., "PRD Template v2.1"); archive old versions immediately after migration; add deprecation banner to old templates |
| Jira issue templates do not apply consistently | Template applied at wrong level (project vs. issue type), or default values overridden by workflow post-functions | Verify template scope matches intended issue type and project; check for conflicting automation rules or post-functions |
| Template adoption rate is low despite training | Templates add friction rather than reducing it; too many required fields | Simplify templates to the minimum viable structure; make optional sections collapsible; gather user feedback and iterate quarterly |
| Dynamic macros (Jira queries, charts) show stale data | JQL filter references incorrect project, or cache settings are too aggressive | Verify JQL in each dynamic macro; adjust cache refresh intervals; test macros after any project key or filter changes |

## Success Criteria

- Template adoption rate exceeds 70% for targeted content types (measured by pages created from templates vs. blank pages)
- New template requests are evaluated and deployed within 10 business days
- All active templates have documented usage instructions and at least one completed example
- Template satisfaction score (from quarterly user survey) averages 4+/5
- Zero active templates older than 12 months without a documented review
- Template-created content passes quality checklist at 85%+ rate on first use
- Deprecated templates are archived within 30 days of replacement deployment
