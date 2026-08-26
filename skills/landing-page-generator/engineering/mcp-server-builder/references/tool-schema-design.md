# Tool Schema Design

Read this when designing tool names, descriptions, and input schemas so an LLM reliably selects and calls your tools.

## Naming Conventions

```
Pattern: verb_noun or verb_noun_qualifier

GOOD names:
  search_documents         — clear action + target
  create_github_issue      — includes service for disambiguation
  get_deployment_status    — standard CRUD verb
  run_database_query       — action implies execution
  list_pull_requests       — list for collection retrieval

BAD names:
  search                   — search what?
  documents                — not a verb_noun
  doSearch                 — camelCase, vague
  handle_request           — implementation detail, not intent
  helper                   — meaningless
```

## Description Engineering

The description determines whether an LLM selects your tool. Write it for the LLM, not for humans.

```
Template: "[What it does]. [What it returns]. [When to use it]."

EFFECTIVE:
"Search the codebase for files matching a regex pattern. Returns file paths,
line numbers, and matching content snippets ranked by relevance. Use when
looking for implementations, definitions, or usage of specific code patterns."

INEFFECTIVE:
"Searches files."           — no return value, no usage guidance
"A powerful search tool..." — marketing copy
"Wrapper around ripgrep"    — implementation detail
```

## Input Schema Best Practices

```json
{
  "name": "query_database",
  "description": "Execute a read-only SQL query against the application database. Returns up to 100 rows as a formatted table. Use when the user needs to look up data, run reports, or investigate database state. Only SELECT statements are allowed.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "sql": {
        "type": "string",
        "description": "SQL SELECT query to execute. Must be a read-only query. Example: SELECT id, email, created_at FROM users WHERE created_at > '2026-01-01' LIMIT 10"
      },
      "database": {
        "type": "string",
        "enum": ["primary", "analytics", "staging"],
        "default": "primary",
        "description": "Which database to query. Use 'analytics' for reporting queries on large datasets."
      },
      "format": {
        "type": "string",
        "enum": ["table", "json", "csv"],
        "default": "table",
        "description": "Output format. 'table' is best for display, 'json' for programmatic use."
      }
    },
    "required": ["sql"]
  }
}
```
