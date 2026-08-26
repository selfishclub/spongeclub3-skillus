# Protocol Selection — Comparison Matrix

The full feature-by-feature comparison of MCP, A2A, OpenAI Functions, and
LangChain Tools. Read this when deciding which protocol fits a given system
before following the decision framework in `SKILL.md`.

## Protocol Comparison Matrix

| Feature | MCP | A2A | OpenAI Functions | LangChain Tools |
|---------|-----|-----|-----------------|-----------------|
| Transport | stdio/SSE/WebSocket | HTTP+JSON-RPC | HTTP REST | In-process |
| Discovery | Server capabilities | Agent cards | API spec | Registry |
| Streaming | SSE notifications | SSE streaming | Streaming deltas | Callbacks |
| Auth | OAuth 2.1 | Agent auth | API key | N/A |
| State | Resources + context | Task lifecycle | Conversation | Memory |
| Multi-turn | Sampling | Task updates | Thread context | Chain state |
| File handling | Resource URIs | Artifact parts | File search | Document loaders |
| Best for | Tool serving | Agent networks | Single-model tools | Python pipelines |
