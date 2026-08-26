# PM Live Data Adapters

Thin Python scripts that pull data from Jira / Linear / Notion APIs and emit JSON in the shape PM Python tools expect.

**Why:** PM skills' Python tools (`status_generator.py`, `flow_metrics.py`, `dependency_graph.py`, `feedback_triage.py`) all need JSON input. Without these adapters, you'd have to extract the data manually. Now you can pipe:

```bash
python tools/adapters/jira_to_json.py --jql "project = PROJ AND sprint in openSprints()" --format status-update \
  | python project-management/execution/status-update-generator/scripts/status_generator.py --input /dev/stdin
```

**Stdlib only.** No `pip install` required.

## Adapters

| Adapter | Source | Auth env vars |
|---|---|---|
| `jira_to_json.py` | Atlassian Jira Cloud REST API v3 | `JIRA_URL`, `JIRA_USER`, `JIRA_TOKEN` |
| `linear_to_json.py` | Linear GraphQL API | `LINEAR_API_KEY` |
| `notion_to_json.py` | Notion REST API | `NOTION_TOKEN`, optional `NOTION_VERSION` |

## Output formats

Every adapter supports `--format`:

| Format | Output shape | Consumes which PM tool? |
|---|---|---|
| `raw` | Pass-through of the source API response | (debugging) |
| `status-update` | `{period, project, highlights, blockers, risks, asks, next}` | `status_generator.py` |
| `cycle-time` | `{issues: [{key, created, started, completed, transitions}]}` | `flow_metrics.py` |
| `dependency-map` | `{teams, dependencies}` | `dependency_graph.py` |
| `feedback` | `{items: [{channel, customer, raw, segment, area}]}` | `feedback_triage.py` |

Not every adapter emits every format — see each adapter's `--help`.

## Auth setup

### Jira

```bash
export JIRA_URL=https://acme.atlassian.net
export JIRA_USER=you@acme.com
export JIRA_TOKEN=$(cat ~/.jira-token)   # generated at id.atlassian.com/manage-profile/security/api-tokens
```

### Linear

```bash
export LINEAR_API_KEY=lin_api_...          # generated at linear.app/settings/api
```

### Notion

```bash
export NOTION_TOKEN=secret_...             # integration token from notion.so/my-integrations
# Optional:
export NOTION_VERSION=2022-06-28
```

## Conventions

- Adapters never write secrets to stdout — only API responses
- `--dry-run` prints the request shape without making the call
- `--verbose` logs to stderr so stdout stays pipe-clean
- All adapters honor `--output <path>` (defaults to stdout)

## Pipelines

See `pipelines/` for runnable end-to-end flows that chain adapters with the PM Python tools.
