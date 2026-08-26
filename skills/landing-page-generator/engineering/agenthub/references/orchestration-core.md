# Orchestration Core Concepts, Workflows & Patterns

Read this when defining a workflow DAG, writing the workflow JSON, understanding agent states/execution order, or running the define/execute/evaluate workflows.

## Core Concepts

### Workflow DAG

A workflow is a directed acyclic graph where:
- **Nodes** are agent tasks with a defined scope, inputs, and expected outputs
- **Edges** are dependencies: agent B cannot start until agent A completes
- **Root nodes** have no dependencies and start immediately
- **Terminal nodes** have no dependents and feed into the merge step

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ Research  │────>│ Analysis │────>│  Merge   │
│  Agent    │     │  Agent   │     │  Agent   │
└──────────┘     └──────────┘     └──────────┘
                       ▲
┌──────────┐           │
│ Data      │──────────┘
│ Agent     │
└──────────┘
```

### Workflow Definition Format

```json
{
  "name": "market-analysis",
  "description": "Comprehensive market analysis for product launch",
  "agents": {
    "researcher": {
      "task": "Research competitor landscape and market size",
      "inputs": ["product_description"],
      "outputs": ["competitor_list", "market_size"],
      "dependencies": []
    },
    "data_collector": {
      "task": "Collect pricing and feature data from competitors",
      "inputs": ["competitor_list"],
      "outputs": ["pricing_data", "feature_matrix"],
      "dependencies": ["researcher"]
    },
    "analyst": {
      "task": "Analyze positioning opportunities and pricing strategy",
      "inputs": ["pricing_data", "feature_matrix", "market_size"],
      "outputs": ["positioning_report", "pricing_recommendation"],
      "dependencies": ["data_collector", "researcher"]
    },
    "writer": {
      "task": "Write executive summary combining all findings",
      "inputs": ["positioning_report", "pricing_recommendation"],
      "outputs": ["executive_summary"],
      "dependencies": ["analyst"]
    }
  },
  "config": {
    "max_parallel": 3,
    "timeout_per_agent": 300,
    "retry_on_failure": true,
    "quality_threshold": 0.7
  }
}
```

### Agent States

| State | Description |
|-------|-------------|
| `PENDING` | Waiting for dependencies to complete |
| `READY` | All dependencies met, queued for execution |
| `RUNNING` | Currently executing |
| `COMPLETED` | Finished successfully |
| `FAILED` | Failed after all retries |
| `SKIPPED` | Skipped due to upstream failure |
| `EVALUATING` | Output being evaluated for quality |

### Execution Strategy

1. **Topological sort** the DAG to determine execution order
2. **Identify parallel groups**: nodes with no inter-dependencies run simultaneously
3. **Execute root nodes** first (no dependencies)
4. **Chain results**: completed node outputs become inputs for dependents
5. **Evaluate outputs** at quality gates
6. **Merge terminal outputs** into final result

## Workflows

### Workflow 1: Define and Validate

```
1. Define agents with tasks, inputs, outputs, dependencies
2. Run dag_analyzer.py to validate:
   - No cycles in the dependency graph
   - All referenced inputs are produced by upstream agents
   - No unreachable nodes
   - Critical path length is acceptable
3. Estimate execution time based on agent count and dependencies
```

### Workflow 2: Execute Orchestration

```
1. Load workflow definition
2. Initialize session (session_manager.py)
3. Topological sort to determine execution order
4. For each parallel group:
   a. Spawn agents (up to max_parallel)
   b. Monitor progress on board
   c. Collect outputs on completion
   d. Evaluate outputs against quality threshold
5. Pass outputs to downstream agents as inputs
6. Merge final outputs
7. Generate execution report
```

### Workflow 3: Evaluate and Iterate

```
1. Collect all agent outputs
2. Run quality evaluation (eval sub-skill)
3. Rank outputs by quality score (result_ranker.py)
4. If any output below threshold:
   a. Retry the agent with adjusted instructions
   b. Or flag for human review
5. Merge passing outputs into final result
```

## Common Patterns

### Fan-Out / Fan-In

Multiple independent agents work in parallel, then a single agent merges results:
```
Task A ──┐
Task B ──┼──> Merge
Task C ──┘
```

### Pipeline

Sequential agents where each transforms the previous output:
```
Extract ──> Transform ──> Load ──> Validate
```

### Reducer

Multiple agents produce competing outputs, ranked and best one selected:
```
Agent 1 ──┐
Agent 2 ──┼──> Rank ──> Best Output
Agent 3 ──┘
```

### Validator Chain

Each agent validates the previous agent's work:
```
Generate ──> Review ──> Fix ──> Approve
```
