# Google A2A Protocol & Protocol Bridges

Agent card discovery, the A2A task lifecycle, a full Python A2A client, and the
Protocol Bridge pattern for translating MCP tool calls into A2A tasks. Read this
when building agent-to-agent communication or bridging heterogeneous protocols.

## Google A2A Protocol Implementation

### Agent Card (Discovery)

```json
{
  "name": "Research Agent",
  "description": "Performs web research and synthesizes findings into structured reports.",
  "url": "https://research-agent.example.com",
  "provider": {
    "organization": "Acme Corp",
    "url": "https://acme.example.com"
  },
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false,
    "stateTransitionHistory": true
  },
  "authentication": {
    "schemes": ["Bearer"],
    "credentials": "oauth2"
  },
  "defaultInputModes": ["text/plain"],
  "defaultOutputModes": ["text/plain", "application/json"],
  "skills": [
    {
      "id": "web-research",
      "name": "Web Research",
      "description": "Search the web and synthesize findings into a structured report with citations.",
      "tags": ["research", "web", "synthesis"],
      "examples": [
        "Research the latest trends in AI agent frameworks",
        "Find competitive pricing data for SaaS products in the CRM space"
      ]
    }
  ]
}
```

### A2A Task Lifecycle

```
Client                           Agent
  │                                │
  ├─ POST /tasks/send ────────────►│ Create task
  │◄──────── task (submitted) ─────┤
  │                                │
  ├─ GET /tasks/{id} ─────────────►│ Poll status
  │◄──────── task (working) ───────┤
  │                                │
  │  (agent processes...)          │
  │                                │
  ├─ GET /tasks/{id} ─────────────►│ Poll status
  │◄──────── task (completed) ─────┤
  │         + artifacts            │
```

### A2A Client Implementation

```python
import httpx
import json
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class TaskState(Enum):
    SUBMITTED = "submitted"
    WORKING = "working"
    INPUT_REQUIRED = "input-required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"

@dataclass
class A2AClient:
    base_url: str
    auth_token: str
    timeout: float = 30.0

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }

    def discover(self) -> dict:
        """Fetch the agent card for capability discovery."""
        resp = httpx.get(
            f"{self.base_url}/.well-known/agent.json",
            headers=self._headers(),
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()

    def send_task(self, message: str, task_id: Optional[str] = None) -> dict:
        """Send a task to the agent. Returns task object with status."""
        payload = {
            "jsonrpc": "2.0",
            "method": "tasks/send",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"type": "text", "text": message}],
                },
            },
            "id": task_id or self._generate_id(),
        }
        resp = httpx.post(
            f"{self.base_url}/a2a",
            json=payload,
            headers=self._headers(),
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()["result"]

    def get_task(self, task_id: str) -> dict:
        """Poll task status."""
        payload = {
            "jsonrpc": "2.0",
            "method": "tasks/get",
            "params": {"id": task_id},
            "id": self._generate_id(),
        }
        resp = httpx.post(
            f"{self.base_url}/a2a",
            json=payload,
            headers=self._headers(),
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()["result"]

    def wait_for_completion(self, task_id: str, poll_interval: float = 2.0, max_polls: int = 60) -> dict:
        """Poll until task reaches a terminal state."""
        import time
        terminal_states = {TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELED}
        for _ in range(max_polls):
            task = self.get_task(task_id)
            if TaskState(task["status"]["state"]) in terminal_states:
                return task
            time.sleep(poll_interval)
        raise TimeoutError(f"Task {task_id} did not complete within {max_polls * poll_interval}s")

    @staticmethod
    def _generate_id() -> str:
        import uuid
        return str(uuid.uuid4())
```

## Protocol Bridge Pattern

When your system uses multiple protocols, implement a bridge that translates between them.

```python
class ProtocolBridge:
    """Translates between MCP tool calls and A2A task delegation."""

    def __init__(self, a2a_agents: dict[str, A2AClient]):
        self.agents = a2a_agents  # skill_id -> A2AClient

    def mcp_tool_to_a2a_task(self, tool_name: str, arguments: dict) -> dict:
        """Convert an MCP tool call into an A2A task send."""
        agent_id, skill = self._resolve_agent(tool_name)
        client = self.agents[agent_id]

        message = self._format_task_message(tool_name, arguments)
        task = client.send_task(message)
        result = client.wait_for_completion(task["id"])

        return self._a2a_result_to_mcp_response(result)

    def _resolve_agent(self, tool_name: str) -> tuple[str, str]:
        """Map MCP tool name to A2A agent + skill."""
        routing = {
            "search_web": ("research-agent", "web-research"),
            "analyze_data": ("analytics-agent", "data-analysis"),
            "generate_code": ("code-agent", "code-generation"),
        }
        if tool_name not in routing:
            raise ValueError(f"No A2A agent registered for tool: {tool_name}")
        return routing[tool_name]

    def _format_task_message(self, tool_name: str, arguments: dict) -> str:
        return json.dumps({"tool": tool_name, "arguments": arguments})

    def _a2a_result_to_mcp_response(self, task: dict) -> dict:
        """Convert A2A task result to MCP tool response format."""
        if task["status"]["state"] == "completed":
            artifacts = task.get("artifacts", [])
            text_parts = []
            for artifact in artifacts:
                for part in artifact.get("parts", []):
                    if part["type"] == "text":
                        text_parts.append(part["text"])
            return {"content": [{"type": "text", "text": "\n".join(text_parts)}]}
        else:
            error_msg = task["status"].get("message", "Task failed")
            return {"content": [{"type": "text", "text": f"Error: {error_msg}"}], "isError": True}
```
