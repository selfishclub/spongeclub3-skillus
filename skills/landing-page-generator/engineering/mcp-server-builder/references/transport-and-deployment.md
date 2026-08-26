# Transport and Deployment

Read this when wiring a server into a client (stdio, SSE, remote HTTP) and managing tool versions across releases.

## Client Configuration

### Claude Code (claude_desktop_config.json)

```json
{
  "mcpServers": {
    "project-tools": {
      "command": "node",
      "args": ["dist/index.js"],
      "cwd": "/path/to/mcp-server",
      "env": {
        "PROJECT_ROOT": "/path/to/project",
        "DATABASE_URL": "postgresql://..."
      }
    },
    "remote-api-tools": {
      "url": "https://mcp.mycompany.com/sse",
      "headers": {
        "Authorization": "Bearer ${MCP_API_TOKEN}"
      }
    }
  }
}
```

## Versioning Strategy

- **Additive changes** (new tools, new optional parameters): non-breaking, bump minor version
- **Tool removal or rename**: breaking, requires deprecation period + major version bump
- **Required parameter addition**: breaking, consider making it optional with a default instead
- **Response format changes**: potentially breaking, document in changelog
