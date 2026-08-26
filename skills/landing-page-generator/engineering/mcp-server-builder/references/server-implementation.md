# Server Implementation

Read this when writing the actual MCP server — full TypeScript and Python server code, plus OpenAPI-to-MCP conversion logic.

## TypeScript MCP Server

### Complete Server with Tools, Resources, and Prompts

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "project-tools",
  version: "1.0.0",
});

// ──── TOOLS ────

server.tool(
  "search_codebase",
  "Search project files for a regex pattern. Returns file paths, line numbers, and matching lines. Use when looking for code patterns, function definitions, or usage of specific identifiers.",
  {
    pattern: z.string().describe("Regex pattern to search for. Example: 'async function handle'"),
    file_glob: z.string().default("**/*.{ts,tsx,js,jsx}")
      .describe("File glob pattern to filter. Example: '**/*.test.ts' for test files only"),
    max_results: z.number().int().min(1).max(100).default(20)
      .describe("Maximum results to return"),
  },
  async ({ pattern, file_glob, max_results }) => {
    const { execSync } = await import("child_process");
    try {
      const output = execSync(
        `rg --json -e '${pattern.replace(/'/g, "\\'")}' --glob '${file_glob}' --max-count ${max_results}`,
        { cwd: process.env.PROJECT_ROOT || ".", timeout: 10000 }
      ).toString();

      const matches = output
        .split("\n")
        .filter(Boolean)
        .map((line) => JSON.parse(line))
        .filter((entry) => entry.type === "match")
        .map((entry) => ({
          file: entry.data.path.text,
          line: entry.data.line_number,
          content: entry.data.lines.text.trim(),
        }));

      if (matches.length === 0) {
        return { content: [{ type: "text", text: `No matches found for pattern: ${pattern}` }] };
      }

      const formatted = matches
        .map((m) => `${m.file}:${m.line}  ${m.content}`)
        .join("\n");

      return {
        content: [{ type: "text", text: `Found ${matches.length} matches:\n\n${formatted}` }],
      };
    } catch (error) {
      return {
        content: [{ type: "text", text: `Search failed: ${error.message}` }],
        isError: true,
      };
    }
  }
);

server.tool(
  "run_tests",
  "Run the project test suite or specific test files. Returns pass/fail results with failure details. Use when verifying code changes or checking test coverage.",
  {
    file_pattern: z.string().optional()
      .describe("Optional test file pattern. Example: 'auth' to run only auth-related tests"),
    coverage: z.boolean().default(false)
      .describe("Include coverage report in output"),
  },
  async ({ file_pattern, coverage }) => {
    const { execSync } = await import("child_process");
    const args = [file_pattern, coverage ? "--coverage" : ""].filter(Boolean).join(" ");

    try {
      const output = execSync(`pnpm test ${args}`, {
        cwd: process.env.PROJECT_ROOT || ".",
        timeout: 120000,
        env: { ...process.env, CI: "true" },
      }).toString();

      return { content: [{ type: "text", text: output }] };
    } catch (error) {
      return {
        content: [{ type: "text", text: `Tests failed:\n\n${error.stdout?.toString() || error.message}` }],
        isError: true,
      };
    }
  }
);

// ──── RESOURCES ────

server.resource(
  "project://readme",
  "project://readme",
  async (uri) => {
    const fs = await import("fs/promises");
    const content = await fs.readFile("README.md", "utf-8");
    return {
      contents: [{ uri: uri.href, mimeType: "text/markdown", text: content }],
    };
  }
);

// ──── PROMPTS ────

server.prompt(
  "review_code",
  "Generate a code review prompt for the given file",
  { file_path: z.string().describe("Path to the file to review") },
  async ({ file_path }) => {
    const fs = await import("fs/promises");
    const content = await fs.readFile(file_path, "utf-8");
    return {
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Review this code for bugs, security issues, and improvement opportunities:\n\n\`\`\`\n${content}\n\`\`\``,
          },
        },
      ],
    };
  }
);

// ──── START SERVER ────
const transport = new StdioServerTransport();
await server.connect(transport);
```

## Python MCP Server

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import subprocess
import json

server = Server("project-tools")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="search_codebase",
            description="Search project files for a regex pattern. Returns file paths, line numbers, and matching content. Use when looking for code patterns or definitions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Regex pattern to search for",
                    },
                    "file_type": {
                        "type": "string",
                        "enum": ["py", "ts", "go", "rs", "all"],
                        "default": "all",
                        "description": "Filter by file type",
                    },
                },
                "required": ["pattern"],
            },
        ),
        Tool(
            name="run_command",
            description="Run a shell command in the project directory. Returns stdout and stderr. Use for running tests, linting, or build commands. Only allows pre-approved commands.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "enum": ["test", "lint", "build", "typecheck", "format"],
                        "description": "Pre-approved command to run",
                    },
                },
                "required": ["command"],
            },
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "search_codebase":
        return await _search_codebase(arguments)
    elif name == "run_command":
        return await _run_command(arguments)
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

COMMAND_MAP = {
    "test": "python -m pytest -v",
    "lint": "ruff check .",
    "build": "python -m build",
    "typecheck": "mypy src/",
    "format": "ruff format --check .",
}

async def _run_command(args: dict) -> list[TextContent]:
    cmd = COMMAND_MAP.get(args["command"])
    if not cmd:
        return [TextContent(type="text", text=f"Unknown command: {args['command']}")]
    try:
        result = subprocess.run(
            cmd.split(), capture_output=True, text=True, timeout=120
        )
        output = result.stdout + ("\n" + result.stderr if result.stderr else "")
        return [TextContent(type="text", text=output or "Command completed with no output.")]
    except subprocess.TimeoutExpired:
        return [TextContent(type="text", text="Command timed out after 120 seconds.")]

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## OpenAPI to MCP Conversion

### Conversion Rules

```
OpenAPI Element          → MCP Element
─────────────────────────────────────────────
operationId              → Tool name (snake_case)
summary + description    → Tool description
parameters + requestBody → inputSchema
responses.200            → Tool output format
securitySchemes          → Server auth config
servers[0].url           → Base URL for requests
```

### Conversion Script Pattern

```python
def openapi_operation_to_mcp_tool(operation: dict, path: str, method: str) -> dict:
    """Convert a single OpenAPI operation to an MCP tool definition."""
    # Derive tool name from operationId or path
    name = operation.get("operationId")
    if not name:
        name = f"{method}_{path.replace('/', '_').strip('_')}"
    name = name.replace("-", "_").lower()

    # Build description from summary + description
    summary = operation.get("summary", "")
    description = operation.get("description", "")
    tool_description = f"{summary}. {description}".strip(". ") + "."

    # Build input schema from parameters and request body
    properties = {}
    required = []

    for param in operation.get("parameters", []):
        prop = {
            "type": param["schema"].get("type", "string"),
            "description": param.get("description", ""),
        }
        if "enum" in param["schema"]:
            prop["enum"] = param["schema"]["enum"]
        if "default" in param["schema"]:
            prop["default"] = param["schema"]["default"]
        properties[param["name"]] = prop
        if param.get("required"):
            required.append(param["name"])

    # Request body properties
    body_schema = (
        operation.get("requestBody", {})
        .get("content", {})
        .get("application/json", {})
        .get("schema", {})
    )
    if body_schema.get("properties"):
        properties.update(body_schema["properties"])
        required.extend(body_schema.get("required", []))

    return {
        "name": name,
        "description": tool_description,
        "inputSchema": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
    }
```
