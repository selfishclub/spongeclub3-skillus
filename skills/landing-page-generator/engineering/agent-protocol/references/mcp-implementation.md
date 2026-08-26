# MCP Tool Schema Design & Server Implementation

Tool schema anatomy, naming/description rules, and TypeScript MCP server
implementations (stdio and authenticated SSE). Read this when building an MCP
server or designing tool schemas for an LLM client.

## MCP Tool Schema Design

### Anatomy of a Well-Designed Tool

```json
{
  "name": "search_documents",
  "description": "Search the knowledge base for documents matching a query. Returns ranked results with titles, snippets, and relevance scores. Use this when the user asks a question that requires looking up information from stored documents.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Natural language search query. Be specific — 'Q4 2025 revenue projections' works better than 'revenue'."
      },
      "limit": {
        "type": "integer",
        "description": "Maximum number of results to return.",
        "default": 10,
        "minimum": 1,
        "maximum": 50
      },
      "filters": {
        "type": "object",
        "description": "Optional filters to narrow results.",
        "properties": {
          "date_after": {
            "type": "string",
            "format": "date",
            "description": "Only return documents created after this date (YYYY-MM-DD)."
          },
          "document_type": {
            "type": "string",
            "enum": ["report", "memo", "presentation", "spreadsheet"],
            "description": "Filter by document type."
          }
        }
      }
    },
    "required": ["query"]
  }
}
```

### Tool Naming Rules

```
GOOD tool names (verb_noun, specific):
  search_documents      — clear action + target
  create_github_issue   — includes the service for disambiguation
  get_user_profile      — standard CRUD verb
  analyze_pr_diff       — describes the analysis action
  send_slack_message    — action + channel type

BAD tool names (vague, ambiguous, or too generic):
  search                — search what?
  do_thing              — meaningless
  handler               — not a verb_noun
  processData           — camelCase breaks conventions
  get_stuff             — too vague for LLM selection
```

### Description Engineering

The description is the single most important field for agent tool selection. An LLM reads the description to decide whether to call this tool.

```
EFFECTIVE description pattern:
"[What it does]. [What it returns]. [When to use it]."

Example:
"Search the knowledge base for documents matching a query. Returns ranked
results with titles, snippets, and relevance scores. Use this when the
user asks a question that requires looking up stored documents."

INEFFECTIVE descriptions:
"Searches documents."           — too short, no usage guidance
"This tool is used for..."      — wastes tokens on filler
"A powerful search engine..."   — marketing copy, not instructions
```

## MCP Server Implementation (TypeScript)

### Minimal Server with Tool and Resource

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "project-tools",
  version: "1.0.0",
  capabilities: {
    tools: {},
    resources: {},
  },
});

// Tool: search codebase
server.tool(
  "search_codebase",
  "Search the project codebase for files matching a pattern. Returns file paths and line numbers with matching content. Use when looking for implementations, definitions, or usage of specific code patterns.",
  {
    pattern: z.string().describe("Regex or glob pattern to search for"),
    file_type: z.enum(["ts", "py", "go", "rs", "all"]).default("all")
      .describe("Filter by file extension"),
    max_results: z.number().int().min(1).max(100).default(20)
      .describe("Maximum results to return"),
  },
  async ({ pattern, file_type, max_results }) => {
    // Implementation: run ripgrep or similar
    const results = await searchFiles(pattern, file_type, max_results);
    return {
      content: [{
        type: "text",
        text: JSON.stringify(results, null, 2),
      }],
    };
  }
);

// Resource: project structure
server.resource(
  "project://structure",
  "project://structure",
  async (uri) => ({
    contents: [{
      uri: uri.href,
      mimeType: "application/json",
      text: JSON.stringify(await getProjectStructure()),
    }],
  })
);

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### MCP Server with Authentication (SSE Transport)

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import express from "express";

const app = express();

// Authentication middleware
function authenticateAgent(req, res, next) {
  const token = req.headers.authorization?.replace("Bearer ", "");
  if (!token || !verifyAgentToken(token)) {
    return res.status(401).json({ error: "Invalid agent credentials" });
  }
  req.agentId = extractAgentId(token);
  next();
}

// Rate limiting per agent
const rateLimiter = new Map<string, { count: number; resetAt: number }>();
function rateLimit(agentId: string, maxPerMinute = 60): boolean {
  const now = Date.now();
  const entry = rateLimiter.get(agentId) || { count: 0, resetAt: now + 60000 };
  if (now > entry.resetAt) {
    entry.count = 0;
    entry.resetAt = now + 60000;
  }
  entry.count++;
  rateLimiter.set(agentId, entry);
  return entry.count <= maxPerMinute;
}

app.use("/mcp", authenticateAgent);

app.get("/mcp/sse", (req, res) => {
  if (!rateLimit(req.agentId)) {
    return res.status(429).json({ error: "Rate limit exceeded" });
  }
  const transport = new SSEServerTransport("/mcp/messages", res);
  server.connect(transport);
});

app.listen(3001, () => console.log("MCP server on :3001"));
```
