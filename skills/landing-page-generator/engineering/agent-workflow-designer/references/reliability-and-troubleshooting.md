# Reliability Engineering & Troubleshooting

Read this when hardening a workflow for production or diagnosing failures.

## Circuit Breaker

```python
import time

class CircuitBreaker:
    """Prevent cascading failures when an agent/model is down."""

    def __init__(self, failure_threshold: int = 5, recovery_time: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failures = 0
        self.state = "closed"  # closed = healthy, open = failing, half-open = testing
        self.last_failure_time = 0.0

    def can_execute(self) -> bool:
        if self.state == "closed":
            return True
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_time:
                self.state = "half-open"
                return True
            return False
        return True  # half-open: allow one test request

    def record_success(self):
        self.failures = 0
        self.state = "closed"

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "open"
```

## Common Pitfalls

- **Over-orchestration** — if a single prompt can handle it, adding agents adds cost and latency, not value
- **Circular dependencies** in subtask graphs causing infinite loops; always validate DAG structure before execution
- **Context bleed** — passing entire previous outputs to every stage; summarize or extract only what is needed
- **No timeout enforcement** — a stuck agent blocks the entire pipeline; set wall-clock timeouts at every boundary
- **Silent failures** — agent returns plausible but incorrect output; add validation stages for critical paths
- **Ignoring cost** — 10 parallel Opus calls is expensive; model selection is a cost decision, not just a quality one
- **Stateless retries** on stateful operations — ensure idempotency before enabling automatic retries
- **Single point of failure** in orchestrator — if the orchestrator agent fails, the entire workflow fails

## Best Practices

1. **Start with a single prompt** — only add agents when you prove one cannot handle the task
2. **Type your handoffs** — use dataclasses or TypedDicts for inter-agent data, not raw strings
3. **Budget context upfront** — calculate token allocations before running the pipeline
4. **Use cheap models for routing** — Haiku for classification costs 10x less than Sonnet
5. **Validate DAG structure** at build time, not runtime
6. **Log every agent call** with input hash, output hash, tokens, latency, and cost
7. **Set SLAs per stage** — if research takes >30s, timeout and use cached results
8. **Test with production-scale inputs** — a pipeline that works on 100 words may fail on 10,000

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Pipeline hangs indefinitely | Missing timeout enforcement on one or more agent stages | Add `asyncio.wait_for()` with explicit `timeout_seconds` at every agent boundary; use the Circuit Breaker pattern to fail fast |
| Circular dependency error at runtime | Subtask graph contains a cycle (e.g., task A depends on B which depends on A) | Validate DAG structure at build time with topological sort; the `_batch_by_dependencies` method catches this but validation should happen earlier |
| Context window exceeded mid-pipeline | Intermediate outputs grow beyond the model's token limit | Use the `ContextBudget` class to allocate tokens per stage; summarize or truncate outputs before passing to the next stage |
| Fan-out tasks return inconsistent formats | Each parallel agent interprets the output schema differently | Define a shared `TypedDict` or `dataclass` for all fan-out results; add a validation step before the merge function |
| Orchestrator plan creates too many subtasks | The planning prompt does not constrain subtask count, leading to over-decomposition | Add explicit constraints in the planner system prompt (e.g., "maximum 5 subtasks"); review and approve plans before execution in high-stakes workflows |
| Consensus never reaches quorum | Validators disagree consistently or confidence scores are too low | Lower the `quorum` threshold, add a tiebreaker agent, or revise validator prompts to align on evaluation criteria |
| Cost spikes on parallel workflows | Expensive models (Opus) used for all fan-out branches instead of routing by complexity | Apply cost-aware routing: use Haiku for classification and simple tasks, Sonnet for most work, Opus only for final synthesis or high-stakes decisions |

## Success Criteria

- Pipeline end-to-end latency stays within the defined SLA (e.g., under 60 seconds for a 5-stage workflow) with no stage exceeding its individual timeout
- Agent routing accuracy exceeds 90% when measured against a labeled test set of at least 100 representative requests
- Fan-out/fan-in workflows complete with fewer than 5% task failures across all parallel branches under normal operating conditions
- Total token cost per workflow run decreases by at least 40% after applying model tiering (Haiku for routing, Sonnet for core work, Opus for synthesis)
- Circuit breakers trigger correctly within 5 consecutive failures and recover automatically after the defined recovery window
- Context window utilization stays below 85% of model limits at every pipeline stage, with no truncation-related quality degradation
- All inter-agent handoffs pass schema validation with zero type errors across 100 consecutive workflow executions
