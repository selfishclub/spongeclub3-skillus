# Pipelines

Runnable skill-chain pipelines that orchestrate multiple PM skills end-to-end.

Each pipeline is a standalone Python script (stdlib only) that calls the
underlying PM skill scripts via subprocess and emits a single summary plus
per-stage artifacts. Every pipeline supports `--demo` for a no-input dry
run with built-in sample data, `--format markdown|json` for the summary
output, and `--output <dir>` to save artifacts to a directory.

If a downstream skill's Python tool is not present, the pipeline writes a
stub artifact and continues -- this keeps the pipeline runnable in any
environment, while signaling which tools need to be installed.

Date: 2026-05-22

## The five pipelines

| Pipeline | When to use | Inputs | Outputs |
|---|---|---|---|
| [feature-end-to-end.py](feature-end-to-end.py) | Greenfield feature: discovery -> PRD -> OKRs -> backlog -> release | feature JSON (name, owner, target release, evidence) | 7 stage artifacts + summary |
| [weekly-cadence.py](weekly-cadence.py) | Friday/Monday cadence: status + flow metrics + dependencies | Jira or Linear export JSON | status.md, flow.md, deps.md + summary |
| [customer-discovery.py](customer-discovery.py) | Discovery sprint: interviews -> opportunity tree -> assumption map -> experiments -> NSM | interviews JSON | opportunities.json + 4 stage artifacts + summary |
| [post-mortem-flow.py](post-mortem-flow.py) | After an incident: RCA + follow-up risk classification + cross-team mitigations | incident JSON | post-mortem doc + followup-risks.json + summary |
| [launch-coordination.py](launch-coordination.py) | Coordinated launch: beta -> flags -> playbook -> release notes | launch JSON | 4 stage artifacts + go/no-go checklist + summary |

## Quick start

```bash
# Run any pipeline with built-in demo data
python pipelines/feature-end-to-end.py --demo --output /tmp/feature-demo
python pipelines/weekly-cadence.py --demo --output /tmp/weekly-demo
python pipelines/customer-discovery.py --demo --output /tmp/discovery-demo
python pipelines/post-mortem-flow.py --demo --output /tmp/postmortem-demo
python pipelines/launch-coordination.py --demo --output /tmp/launch-demo

# Or use your own JSON input
python pipelines/weekly-cadence.py --input jira-export.json --source jira --output ./this-week
python pipelines/customer-discovery.py --input interviews.json --output ./q2-discovery
```

## Pipeline structure

Every pipeline follows the same pattern:

1. Parse CLI args (`--demo`, `--input`, `--output`, `--format`).
2. Load context (either built-in demo data or the input JSON).
3. Derive lightweight intermediate artifacts (clustering, summaries) from
   the input data using stdlib only -- no LLM calls.
4. For each stage, invoke the underlying PM tool via `subprocess.run`
   with `--demo --format markdown --output <stage-artifact>`. If the tool
   is not present, write a stub artifact noting which tool was missing.
5. Emit a single summary (markdown or JSON) listing each stage, its
   artifact, run mode (ran / stub / skipped), and exit code.
6. Cross-reference the PM skills the pipeline chains.

## Integration points

- **Atlassian MCP**: pipelines do not call MCP directly; they emit
  markdown / JSON artifacts that the user (or a separate MCP-aware
  agent) can post into Jira / Confluence.
- **Linear**: same model -- pipelines produce Linear-compatible
  markdown (status updates, release notes) but do not call the GraphQL
  API.
- **Productboard**: discovery pipeline's `opportunities.json` is a
  feed candidate for the Productboard insights inbox.
- **Notion**: every artifact can be pushed to a Notion DB via
  `notion-pm/references/notion-api-patterns.md`.

## Pipeline -> Skills mapping

### feature-end-to-end.py

Chains seven PM skills in sequence:

- `discovery/identify-assumptions`
- `discovery/brainstorm-experiments`
- `discovery/pre-mortem`
- `execution/create-prd`
- `execution/brainstorm-okrs`
- `execution/prioritization-frameworks`
- `execution/release-notes`

### weekly-cadence.py

Three PM skills (plus built-in Jira / Linear adapters):

- `execution/status-update-generator`
- `execution/cycle-time-analyzer` (flow_metrics)
- `execution/dependency-map` (dependency_graph)

### customer-discovery.py

Four PM skills:

- `discovery/interview-synthesis`
- `discovery/identify-assumptions`
- `discovery/brainstorm-experiments`
- `execution/north-star-metric`

### post-mortem-flow.py

Three PM skills:

- `execution/post-mortem`
- `discovery/pre-mortem`
- `execution/dependency-map`

### launch-coordination.py

Four PM skills:

- `execution/beta-program`
- `execution/feature-flag-strategy`
- `execution/launch-playbook`
- `execution/release-notes`

## Design notes

- **Stdlib only**: each pipeline is one file, no extra dependencies.
- **Subprocess orchestration**: pipelines call PM tools as separate
  processes. This isolates failures and keeps the pipeline robust if a
  tool aborts.
- **Stub fallback**: when a tool is absent, the pipeline writes a stub
  artifact and continues. The summary shows `mode: stub` so users see
  what needs to be installed.
- **Timeouts**: each stage has a 60-second subprocess timeout to keep
  the pipeline responsive.
- **No external network calls**: pipelines do not hit Jira, Linear,
  Productboard, Notion, or Confluence APIs. They emit artifacts that
  the user pushes (manually or via a separate MCP agent).

See each pipeline's docstring for stage details and the corresponding
PM skill's `references/red-flags.md` for common failure modes.
