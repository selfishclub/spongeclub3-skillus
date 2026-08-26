# Best Practices, Pitfalls, Troubleshooting & Success Criteria

Read this when designing agent scopes, debugging a stuck or incoherent workflow, or validating an orchestration against the quality bar.

## Best Practices

1. **Small, focused agent scopes** -- each agent should have a single clear objective
2. **Explicit inputs/outputs** -- never rely on implicit shared state between agents
3. **Quality gates between stages** -- evaluate before passing outputs downstream
4. **Timeout per agent** -- prevent runaway agents from blocking the workflow
5. **Retry with context** -- when retrying a failed agent, include the failure reason
6. **Merge strategy documented** -- how competing or complementary outputs combine
7. **Critical path awareness** -- optimize the longest dependency chain first
8. **Idempotent agents** -- agents should produce the same output given the same input

## Common Pitfalls

| Pitfall | Why It Happens | Fix |
|---------|---------------|-----|
| Cycle in DAG | Agent A depends on B which depends on A | Run dag_analyzer.py before execution |
| Output format mismatch | Agent B expects JSON, Agent A produces markdown | Define explicit output schemas per agent |
| Single bottleneck agent | One agent depends on everything | Restructure DAG to parallelize dependencies |
| Lost context between agents | Outputs too terse for downstream use | Require structured output with context preservation |
| Quality degradation in merge | Naive concatenation loses coherence | Use a dedicated merge agent with synthesis instructions |
| Runaway execution time | No timeouts, retry loops | Set timeout_per_agent and max retries |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Workflow hangs at agent N | Dependency not met or agent timeout | Check board for PENDING agents; verify upstream completed; check timeout config |
| Merged output is incoherent | No merge strategy defined | Use the merge sub-skill with explicit synthesis instructions |
| Agent produces wrong format | Input/output contract unclear | Define JSON schemas for agent inputs and outputs |
| DAG validation fails with cycle | Circular dependency in definition | Use dag_analyzer.py to identify the cycle; restructure the dependency chain |
| Quality eval fails everything | Threshold too strict for task complexity | Lower threshold or add a revision step before eval |

## Success Criteria

- **DAG validation passes** on every workflow definition before execution
- **Parallel execution utilization above 60%** -- agents running in parallel most of the time
- **Quality gate pass rate above 80%** -- agent outputs meet threshold on first attempt
- **End-to-end execution time within 2x critical path** -- parallelization delivers real speedup
- **Zero lost outputs** -- every agent's output is captured and available for merge/review
- **Merge coherence score above 0.7** -- final merged output reads as a unified deliverable
