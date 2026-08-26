# Error Handling, Testing & Quality Standards

Structured error responses, the error code taxonomy, tool/schema validation and
integration testing patterns, plus common pitfalls, best practices,
troubleshooting, and success criteria. Read this when hardening a protocol for
production or diagnosing agent tool-calling failures.

## Error Handling Standards

### Structured Error Responses

Every protocol should return errors in a consistent format that agents can parse and recover from.

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "Too many requests. Retry after 30 seconds.",
    "retryable": true,
    "retry_after_seconds": 30,
    "details": {
      "limit": 60,
      "window": "1m",
      "current": 62
    }
  }
}
```

### Error Code Taxonomy

| Code | Meaning | Agent Action |
|------|---------|-------------|
| `INVALID_INPUT` | Bad parameters | Fix input and retry |
| `NOT_FOUND` | Resource missing | Try alternative or report |
| `AUTH_FAILED` | Credentials invalid | Refresh token and retry |
| `AUTH_EXPIRED` | Token expired | Refresh and retry once |
| `RATE_LIMITED` | Too many requests | Wait `retry_after` then retry |
| `UPSTREAM_ERROR` | External service failed | Retry with backoff |
| `INTERNAL_ERROR` | Server bug | Report, do not retry |
| `CAPABILITY_UNAVAILABLE` | Tool/skill disabled | Use alternative tool |

## Testing Agent Protocols

### Tool Schema Validation

```python
import jsonschema

def validate_mcp_tool(tool_def: dict) -> list[str]:
    """Validate an MCP tool definition for common issues."""
    issues = []

    if not tool_def.get("name"):
        issues.append("Missing tool name")
    elif not tool_def["name"].replace("_", "").isalnum():
        issues.append(f"Tool name '{tool_def['name']}' should use snake_case with alphanumeric chars")

    desc = tool_def.get("description", "")
    if len(desc) < 20:
        issues.append("Description too short — LLMs need clear usage guidance")
    if not any(word in desc.lower() for word in ["use when", "returns", "use this"]):
        issues.append("Description should explain when to use the tool and what it returns")

    schema = tool_def.get("inputSchema", {})
    if schema.get("type") != "object":
        issues.append("inputSchema must be type: object")

    for prop_name, prop_def in schema.get("properties", {}).items():
        if not prop_def.get("description"):
            issues.append(f"Property '{prop_name}' missing description")
        if prop_def.get("type") == "string" and not prop_def.get("description"):
            issues.append(f"String property '{prop_name}' needs description for LLM context")

    return issues
```

### Integration Testing Pattern

```python
import subprocess
import json

def test_mcp_server_tools():
    """Verify MCP server starts and lists expected tools."""
    proc = subprocess.Popen(
        ["node", "dist/index.js"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # Send initialize request
    init_msg = json.dumps({
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "test"}},
        "id": 1,
    }) + "\n"
    proc.stdin.write(init_msg.encode())
    proc.stdin.flush()

    # Send tools/list
    list_msg = json.dumps({
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {},
        "id": 2,
    }) + "\n"
    proc.stdin.write(list_msg.encode())
    proc.stdin.flush()

    # Read and validate response
    # (In production, use proper JSON-RPC response parsing)
    proc.terminate()
```

## Common Pitfalls

- **Vague tool descriptions** that cause the LLM to select the wrong tool or skip it entirely
- **Missing required field declarations** leading to agents sending incomplete parameters
- **No error codes** in responses, forcing agents to parse error messages with heuristics
- **Exposing internal implementation details** in tool schemas instead of user-intent abstractions
- **No rate limiting** on MCP servers, allowing runaway agent loops to exhaust resources
- **Mixing transport concerns with protocol logic** instead of keeping them separate
- **No capability versioning** making it impossible to evolve tools without breaking clients
- **Synchronous-only design** that blocks on long-running operations instead of using task lifecycle

## Best Practices

1. **Description-first design** — write the tool description before the implementation
2. **One intent per tool** — a tool that does three things gets selected for the wrong reason
3. **Validate inputs on the server** — never trust that the LLM sent correct types
4. **Return structured errors** with codes, not string messages
5. **Version your protocol** — use capability negotiation at connection time
6. **Log every tool call** with agent ID, inputs, outputs, and latency for debugging
7. **Test tool selection** — present your tool list to an LLM and verify it picks the right one
8. **Use protocol bridges** at boundaries rather than forcing all agents onto one protocol

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| LLM never selects the correct tool | Tool description is vague or missing usage guidance | Rewrite description using the "[What it does]. [What it returns]. [When to use it]." pattern |
| MCP server connects but no tools appear | Missing `tools` in server capabilities declaration | Add `capabilities: { tools: {} }` to the `McpServer` constructor options |
| A2A task stuck in `working` state indefinitely | Agent has no timeout or heartbeat mechanism | Implement `max_polls` and `poll_interval` in `wait_for_completion`; add server-side task TTLs |
| `AUTH_EXPIRED` errors after token refresh | Refreshed token not propagated to in-flight requests | Store tokens centrally and read from shared state per-request rather than caching on the client instance |
| Protocol bridge drops artifacts from A2A responses | Bridge only extracts `text` parts, ignoring `file` or `data` parts | Extend `_a2a_result_to_mcp_response` to handle all artifact part types including binary and structured data |
| Rate limiting triggers during normal multi-tool calls | Per-agent rate limit is too low for parallel tool execution | Increase the per-minute ceiling or implement token-bucket rate limiting with burst allowance |
| Tool schema validation passes but agent sends wrong types | JSON Schema `type` is correct but lacks `format`, `enum`, or `pattern` constraints | Add tighter constraints (e.g., `"format": "date"`, `"pattern": "^[A-Z]{3}$"`) to catch malformed inputs early |

## Success Criteria

- **Tool selection accuracy >= 95%**: LLMs select the intended tool on the first attempt when presented with the full tool list and a matching user query.
- **Schema validation coverage = 100%**: Every deployed tool passes `validate_mcp_tool()` with zero issues reported.
- **Error response consistency**: All protocol endpoints return structured error objects with `code`, `message`, and `retryable` fields — no raw exception strings.
- **Discovery latency < 500ms**: Agent card retrieval (A2A) and `tools/list` (MCP) responses complete within 500ms at the 95th percentile.
- **Protocol bridge translation fidelity >= 99%**: Cross-protocol calls preserve all input parameters and output artifacts without data loss or type coercion errors.
- **Authentication failure recovery < 2 retries**: Token refresh flows resolve `AUTH_EXPIRED` errors within a single retry cycle without user intervention.
- **Mean time to integrate a new tool < 30 minutes**: A developer with access to this skill can define, validate, and deploy a new MCP or A2A tool in under 30 minutes.
