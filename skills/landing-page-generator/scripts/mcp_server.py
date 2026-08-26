#!/usr/bin/env python3
"""
Claude Skills MCP Server — Model Context Protocol over stdin/stdout.

Exposes the skills library as MCP tools via JSON-RPC 2.0.
No external dependencies — standard library only.

Usage:
    python3 scripts/mcp_server.py

Add to Claude Code settings (~/.claude/settings.json) or project .mcp.json:
    {
      "mcpServers": {
        "claude-skills": {
          "command": "python3",
          "args": ["scripts/mcp_server.py"],
          "cwd": "/path/to/Claude-Skills"
        }
      }
    }
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_JSON = REPO_ROOT / "skills.json"
PERSONAS_DIR = REPO_ROOT / "agents" / "personas"

SERVER_INFO = {
    "name": "claude-skills",
    "version": "1.0.0",
}

PROTOCOL_VERSION = "2024-11-05"

# ---------------------------------------------------------------------------
# Logging (stderr only — stdout is the JSON-RPC transport)
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    print(f"[mcp-server] {msg}", file=sys.stderr, flush=True)

# ---------------------------------------------------------------------------
# Catalog loader
# ---------------------------------------------------------------------------

_catalog = None

def load_catalog() -> dict:
    """Load skills.json once and cache it."""
    global _catalog
    if _catalog is not None:
        return _catalog
    try:
        with open(SKILLS_JSON, "r", encoding="utf-8") as f:
            _catalog = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        log(f"Failed to load skills.json: {exc}")
        _catalog = {"skills": [], "domains": {}}
    return _catalog

# ---------------------------------------------------------------------------
# Tool definitions (MCP schema)
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "name": "search_skills",
        "description": "Search skills by query string. Matches against name, description, and tags.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "domain": {"type": "string", "description": "Filter by domain (e.g. engineering, marketing)"},
                "limit": {"type": "number", "description": "Max results (default 10)"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_skill",
        "description": "Get full details for a skill including SKILL.md content, scripts, and references.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Skill name (e.g. api-design, churn-prevention)"},
            },
            "required": ["name"],
        },
    },
    {
        "name": "list_skills",
        "description": "List all skills in the library, optionally filtered by domain.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Filter by domain"},
            },
        },
    },
    {
        "name": "run_tool",
        "description": "Get instructions and --help output for running a Python tool from a skill.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "skill": {"type": "string", "description": "Skill name"},
                "tool": {"type": "string", "description": "Tool/script filename (e.g. analyze.py)"},
            },
            "required": ["skill", "tool"],
        },
    },
    {
        "name": "get_persona",
        "description": "Get a persona's markdown content from the agents/personas directory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Persona name (e.g. startup-cto, solo-founder)"},
            },
            "required": ["name"],
        },
    },
    {
        "name": "skill_stats",
        "description": "Get repository statistics: skill counts by domain, total tools, agents, etc.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
]

# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def _find_skill(name: str) -> dict | None:
    """Find a skill entry by name in the catalog."""
    catalog = load_catalog()
    name_lower = name.lower().strip()
    for skill in catalog.get("skills", []):
        if skill.get("name", "").lower() == name_lower:
            return skill
    return None


def _skill_dir(skill_entry: dict) -> Path:
    """Derive the skill directory from its catalog entry."""
    skill_path = skill_entry.get("path", "")
    return REPO_ROOT / Path(skill_path).parent


def tool_search_skills(args: dict) -> str:
    query = args.get("query", "").lower().strip()
    domain_filter = args.get("domain", "").lower().strip()
    limit = int(args.get("limit", 10))

    if not query:
        return json.dumps({"error": "query is required"})

    catalog = load_catalog()
    results = []

    for skill in catalog.get("skills", []):
        if domain_filter and skill.get("domain", "").lower() != domain_filter:
            continue

        # Score: check name, description, tags
        score = 0
        name = skill.get("name", "").lower()
        desc = skill.get("description", "").lower()
        tags = [t.lower() for t in skill.get("tags", [])]

        if query in name:
            score += 10
        if query in desc:
            score += 5
        for tag in tags:
            if query in tag:
                score += 3

        if score > 0:
            results.append((score, {
                "name": skill.get("name"),
                "description": skill.get("description", "")[:200],
                "domain": skill.get("domain"),
                "path": skill.get("path"),
                "tools": skill.get("tools", 0),
                "tags": skill.get("tags", []),
            }))

    results.sort(key=lambda x: x[0], reverse=True)
    matches = [r[1] for r in results[:limit]]
    return json.dumps({"count": len(matches), "results": matches}, indent=2)


def tool_get_skill(args: dict) -> str:
    name = args.get("name", "").strip()
    if not name:
        return json.dumps({"error": "name is required"})

    skill = _find_skill(name)
    if not skill:
        return json.dumps({"error": f"Skill '{name}' not found"})

    skill_dir = _skill_dir(skill)
    result = {
        "name": skill.get("name"),
        "domain": skill.get("domain"),
        "version": skill.get("version"),
        "description": skill.get("description"),
        "tags": skill.get("tags", []),
        "tools_count": skill.get("tools", 0),
    }

    # Read SKILL.md
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        try:
            result["skill_md"] = skill_md.read_text(encoding="utf-8")
        except Exception as exc:
            result["skill_md"] = f"(error reading: {exc})"
    else:
        result["skill_md"] = "(SKILL.md not found)"

    # List scripts
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.is_dir():
        result["scripts"] = sorted(f.name for f in scripts_dir.iterdir() if f.is_file())
    else:
        result["scripts"] = []

    # List references
    refs_dir = skill_dir / "references"
    if refs_dir.is_dir():
        result["references"] = sorted(f.name for f in refs_dir.iterdir() if f.is_file())
    else:
        result["references"] = []

    return json.dumps(result, indent=2)


def tool_list_skills(args: dict) -> str:
    domain_filter = args.get("domain", "").lower().strip()
    catalog = load_catalog()

    skills = []
    for skill in catalog.get("skills", []):
        if domain_filter and skill.get("domain", "").lower() != domain_filter:
            continue
        skills.append({
            "name": skill.get("name"),
            "domain": skill.get("domain"),
            "description": skill.get("description", "")[:120],
            "tools": skill.get("tools", 0),
        })

    return json.dumps({"count": len(skills), "skills": skills}, indent=2)


def tool_run_tool(args: dict) -> str:
    skill_name = args.get("skill", "").strip()
    tool_name = args.get("tool", "").strip()

    if not skill_name or not tool_name:
        return json.dumps({"error": "Both 'skill' and 'tool' are required"})

    skill = _find_skill(skill_name)
    if not skill:
        return json.dumps({"error": f"Skill '{skill_name}' not found"})

    skill_dir = _skill_dir(skill)
    script_path = skill_dir / "scripts" / tool_name

    if not script_path.exists():
        # Try with .py extension
        script_path = skill_dir / "scripts" / (tool_name + ".py")
        if not script_path.exists():
            available = []
            scripts_dir = skill_dir / "scripts"
            if scripts_dir.is_dir():
                available = sorted(f.name for f in scripts_dir.iterdir() if f.is_file())
            return json.dumps({
                "error": f"Tool '{tool_name}' not found in {skill_name}",
                "available_tools": available,
            })

    result = {
        "skill": skill_name,
        "tool": script_path.name,
        "path": str(script_path),
        "usage": f"python3 {script_path.relative_to(REPO_ROOT)}",
    }

    # Try to get --help output
    try:
        proc = subprocess.run(
            [sys.executable, str(script_path), "--help"],
            capture_output=True, text=True, timeout=10,
            cwd=str(REPO_ROOT),
        )
        help_text = (proc.stdout or proc.stderr or "").strip()
        if help_text:
            result["help"] = help_text
        else:
            result["help"] = "(no help output)"
    except subprocess.TimeoutExpired:
        result["help"] = "(timed out getting help)"
    except Exception as exc:
        result["help"] = f"(error: {exc})"

    return json.dumps(result, indent=2)


def tool_get_persona(args: dict) -> str:
    name = args.get("name", "").strip()
    if not name:
        return json.dumps({"error": "name is required"})

    # Normalize: add .md if missing
    filename = name if name.endswith(".md") else name + ".md"
    persona_path = PERSONAS_DIR / filename

    if not persona_path.exists():
        # List available personas
        available = []
        if PERSONAS_DIR.is_dir():
            available = sorted(f.stem for f in PERSONAS_DIR.iterdir() if f.suffix == ".md")
        return json.dumps({
            "error": f"Persona '{name}' not found",
            "available": available,
        })

    try:
        content = persona_path.read_text(encoding="utf-8")
        return json.dumps({"name": persona_path.stem, "content": content}, indent=2)
    except Exception as exc:
        return json.dumps({"error": f"Failed to read persona: {exc}"})


def tool_skill_stats(args: dict) -> str:
    catalog = load_catalog()
    domains = catalog.get("domains", {})

    total_skills = sum(d.get("count", 0) for d in domains.values())
    total_tools = sum(d.get("tools", 0) for d in domains.values())

    # Count agents
    agents_dir = REPO_ROOT / "agents"
    agent_count = 0
    if agents_dir.is_dir():
        agent_count = sum(
            1 for f in agents_dir.rglob("*.md")
            if f.name.startswith("cs-") or f.parent.name == "personas"
        )

    # Count personas
    persona_count = 0
    if PERSONAS_DIR.is_dir():
        persona_count = sum(1 for f in PERSONAS_DIR.iterdir() if f.suffix == ".md")

    domain_breakdown = {
        name: {"skills": info.get("count", 0), "tools": info.get("tools", 0)}
        for name, info in sorted(domains.items())
    }

    return json.dumps({
        "total_skills": total_skills,
        "total_tools": total_tools,
        "total_domains": len(domains),
        "agents": agent_count,
        "personas": persona_count,
        "version": catalog.get("version", "unknown"),
        "domains": domain_breakdown,
    }, indent=2)


# ---------------------------------------------------------------------------
# PM skill tool wrappers
# ---------------------------------------------------------------------------

# Maps an MCP tool name -> (script_relative_path, accepts_input_json, extra_flags)
PM_TOOLS = {
    "pm_create_prd": (
        "project-management/execution/create-prd/scripts/prd_scaffolder.py",
        False,  # uses --product-name --objective --segments rather than --input JSON
        {"product_name": "--product-name", "objective": "--objective", "segments": "--segments"},
    ),
    "pm_status_update": (
        "project-management/execution/status-update-generator/scripts/status_generator.py",
        True, {"period": "--period", "status": "--status"},
    ),
    "pm_funnel_analyze": (
        "project-management/execution/activation-funnel/scripts/funnel_analyzer.py",
        True, {},
    ),
    "pm_flow_metrics": (
        "project-management/execution/cycle-time-analyzer/scripts/flow_metrics.py",
        True, {},
    ),
    "pm_dependency_map": (
        "project-management/execution/dependency-map/scripts/dependency_graph.py",
        True, {},
    ),
    "pm_feedback_triage": (
        "project-management/execution/customer-feedback-triage/scripts/feedback_triage.py",
        True, {},
    ),
    "pm_nsm_tree": (
        "project-management/execution/north-star-metric/scripts/metric_tree_builder.py",
        True, {"nsm": "--nsm"},
    ),
    "pm_refinement_score": (
        "project-management/execution/backlog-refinement/scripts/refinement_scorer.py",
        True, {"threshold": "--threshold"},
    ),
    "pm_interview_synthesize": (
        "project-management/discovery/interview-synthesis/scripts/interview_synthesizer.py",
        True, {"outcome": "--outcome", "min_strength": "--min-strength"},
    ),
    "pm_prioritize": (
        "project-management/execution/prioritization-frameworks/scripts/prioritization_scorer.py",
        True, {"framework": "--framework"},
    ),
    "pm_okr_validate": (
        "project-management/execution/brainstorm-okrs/scripts/okr_validator.py",
        True, {},
    ),
    "pm_roadmap_transform": (
        "project-management/execution/outcome-roadmap/scripts/roadmap_transformer.py",
        True, {},
    ),
    "pm_pre_mortem": (
        "project-management/discovery/pre-mortem/scripts/risk_categorizer.py",
        True, {},
    ),
    "pm_release_notes": (
        "project-management/execution/release-notes/scripts/release_notes_generator.py",
        True, {"product_name": "--product-name", "version": "--version"},
    ),
    "pm_stakeholder_map": (
        "project-management/senior-pm/scripts/stakeholder_mapper.py",
        True, {},
    ),
}


def _run_pm_tool(tool_key: str, args: dict) -> str:
    """Generic dispatch for any PM_TOOLS entry."""
    spec = PM_TOOLS.get(tool_key)
    if not spec:
        return json.dumps({"error": f"Unknown PM tool: {tool_key}"})
    script_rel, accepts_input, extra_flags = spec
    script_path = REPO_ROOT / script_rel
    if not script_path.exists():
        return json.dumps({"error": f"Script not found: {script_rel}"})

    cmd = [sys.executable, str(script_path)]
    cleanup_path: Path | None = None

    # Format flag — shared across all PM tools
    fmt = (args.get("format") or "markdown").strip()
    cmd.extend(["--format", fmt])

    # Input handling
    inp = args.get("input")
    if accepts_input:
        if inp is None:
            cmd.append("--demo")
        elif isinstance(inp, (dict, list)):
            # Write to a tempfile and pass --input <path>
            import tempfile
            fd, tmp_path = tempfile.mkstemp(suffix=".json", prefix="pm-mcp-")
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    json.dump(inp, f)
                cmd.extend(["--input", tmp_path])
                cleanup_path = Path(tmp_path)
            except Exception as e:
                return json.dumps({"error": f"Failed writing temp input: {e}"})
        elif isinstance(inp, str):
            # Treat as path or as inline JSON string
            if os.path.exists(inp):
                cmd.extend(["--input", inp])
            else:
                try:
                    parsed = json.loads(inp)
                    import tempfile
                    fd, tmp_path = tempfile.mkstemp(suffix=".json", prefix="pm-mcp-")
                    with os.fdopen(fd, "w", encoding="utf-8") as f:
                        json.dump(parsed, f)
                    cmd.extend(["--input", tmp_path])
                    cleanup_path = Path(tmp_path)
                except json.JSONDecodeError:
                    return json.dumps({"error": "input must be a JSON object, JSON string, or file path"})

    # Extra named flags
    for arg_key, cli_flag in extra_flags.items():
        v = args.get(arg_key)
        if v is not None:
            cmd.extend([cli_flag, str(v)])

    # For non-input tools (e.g., create-prd), if no required args provided -> use --demo if it exists
    if not accepts_input and not any(extra_flags.get(k) and k in args for k in extra_flags):
        cmd.append("--demo")

    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30, cwd=str(REPO_ROOT),
        )
        out = (proc.stdout or "").strip()
        err = (proc.stderr or "").strip()
        if proc.returncode != 0:
            return json.dumps({"error": f"Tool exited {proc.returncode}", "stderr": err[:500]})
        return out or json.dumps({"warning": "no output", "stderr": err[:200]})
    except subprocess.TimeoutExpired:
        return json.dumps({"error": "Tool timed out after 30s"})
    except Exception as exc:
        return json.dumps({"error": f"Exec failed: {exc}"})
    finally:
        if cleanup_path and cleanup_path.exists():
            try: cleanup_path.unlink()
            except OSError: pass


# Generate a handler per PM tool — closure binds tool_key
def _make_pm_handler(tool_key):
    def handler(args):
        return _run_pm_tool(tool_key, args)
    return handler


# Append PM tool definitions to TOOLS list
_SHARED_FORMAT_PROP = {
    "type": "string",
    "enum": ["json", "markdown", "mermaid", "confluence", "notion", "linear"],
    "description": "Output format (default: markdown)",
}

PM_TOOL_DEFS = [
    ("pm_create_prd",
     "Scaffold an 8-section PRD. Provide product_name, objective, and segments.",
     {"product_name": {"type": "string"}, "objective": {"type": "string"},
      "segments": {"type": "string", "description": "Comma-separated segment list"},
      "format": _SHARED_FORMAT_PROP},
     ["product_name", "objective", "segments"]),
    ("pm_status_update",
     "Generate a weekly executive status update from structured input.",
     {"input": {"type": ["object", "string", "null"], "description": "Status data JSON; omit for demo"},
      "period": {"type": "string"}, "status": {"type": "string", "enum": ["green", "yellow", "red"]},
      "format": _SHARED_FORMAT_PROP},
     []),
    ("pm_funnel_analyze",
     "Analyze an AARRR / activation funnel and flag bottlenecks.",
     {"input": {"type": ["object", "string", "null"]}, "format": _SHARED_FORMAT_PROP}, []),
    ("pm_flow_metrics",
     "Compute lead time, cycle time, throughput, and CFD for issue history.",
     {"input": {"type": ["object", "string", "null"]}, "format": _SHARED_FORMAT_PROP}, []),
    ("pm_dependency_map",
     "Build a cross-team dependency graph and critical path.",
     {"input": {"type": ["object", "string", "null"]}, "format": _SHARED_FORMAT_PROP}, []),
    ("pm_feedback_triage",
     "Cluster, categorize (Kano), and score inbound customer feedback.",
     {"input": {"type": ["object", "string", "null"]}, "format": _SHARED_FORMAT_PROP}, []),
    ("pm_nsm_tree",
     "Build a North Star Metric + input metric tree.",
     {"input": {"type": ["object", "string", "null"]}, "nsm": {"type": "string"},
      "format": _SHARED_FORMAT_PROP}, []),
    ("pm_refinement_score",
     "Score backlog items against INVEST and Definition of Ready.",
     {"input": {"type": ["object", "string", "null"]}, "threshold": {"type": "number"},
      "format": _SHARED_FORMAT_PROP}, []),
    ("pm_interview_synthesize",
     "Synthesize customer interviews into an opportunity solution tree.",
     {"input": {"type": ["object", "string", "null"]}, "outcome": {"type": "string"},
      "min_strength": {"type": "number"}, "format": _SHARED_FORMAT_PROP}, []),
    ("pm_prioritize",
     "Score backlog items using RICE, ICE, MoSCoW, Opportunity Score, or Weighted.",
     {"input": {"type": ["object", "string", "null"]},
      "framework": {"type": "string", "enum": ["rice", "ice", "moscow", "opportunity", "weighted"]},
      "format": _SHARED_FORMAT_PROP}, []),
    ("pm_okr_validate",
     "Validate OKRs against SMART + Wodtke confidence model.",
     {"input": {"type": ["object", "string", "null"]}, "format": _SHARED_FORMAT_PROP}, []),
    ("pm_roadmap_transform",
     "Transform an output-heavy roadmap into an outcome-driven Now/Next/Later.",
     {"input": {"type": ["object", "string", "null"]}, "format": _SHARED_FORMAT_PROP}, []),
    ("pm_pre_mortem",
     "Classify pre-launch risks into Tiger / Paper Tiger / Elephant (Klein).",
     {"input": {"type": ["object", "string", "null"]}, "format": _SHARED_FORMAT_PROP}, []),
    ("pm_release_notes",
     "Generate user-facing release notes from shipped tickets.",
     {"input": {"type": ["object", "string", "null"]}, "product_name": {"type": "string"},
      "version": {"type": "string"}, "format": _SHARED_FORMAT_PROP}, []),
    ("pm_stakeholder_map",
     "Plot stakeholders on a Power/Interest grid (Mendelow) and recommend a comms plan.",
     {"input": {"type": ["object", "string", "null"]}, "format": _SHARED_FORMAT_PROP}, []),
]

for _name, _desc, _props, _req in PM_TOOL_DEFS:
    TOOLS.append({
        "name": _name,
        "description": _desc,
        "inputSchema": {"type": "object", "properties": _props,
                        **({"required": _req} if _req else {})},
    })


# Tool dispatch table
TOOL_HANDLERS = {
    "search_skills": tool_search_skills,
    "get_skill": tool_get_skill,
    "list_skills": tool_list_skills,
    "run_tool": tool_run_tool,
    "get_persona": tool_get_persona,
    "skill_stats": tool_skill_stats,
}

# Auto-register all PM tool handlers
for _name in PM_TOOLS:
    TOOL_HANDLERS[_name] = _make_pm_handler(_name)

# ---------------------------------------------------------------------------
# JSON-RPC helpers
# ---------------------------------------------------------------------------

def make_response(id, result: dict) -> dict:
    return {"jsonrpc": "2.0", "id": id, "result": result}


def make_error(id, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": id, "error": {"code": code, "message": message}}


# ---------------------------------------------------------------------------
# MCP method handlers
# ---------------------------------------------------------------------------

def handle_initialize(id, params: dict) -> dict:
    return make_response(id, {
        "protocolVersion": PROTOCOL_VERSION,
        "capabilities": {
            "tools": {},
        },
        "serverInfo": SERVER_INFO,
    })


def handle_tools_list(id, params: dict) -> dict:
    return make_response(id, {"tools": TOOLS})


def handle_tools_call(id, params: dict) -> dict:
    tool_name = params.get("name", "")
    arguments = params.get("arguments", {})

    handler = TOOL_HANDLERS.get(tool_name)
    if not handler:
        return make_response(id, {
            "content": [{"type": "text", "text": json.dumps({"error": f"Unknown tool: {tool_name}"})}],
            "isError": True,
        })

    try:
        result_text = handler(arguments)
        return make_response(id, {
            "content": [{"type": "text", "text": result_text}],
        })
    except Exception as exc:
        log(f"Error in tool {tool_name}: {exc}")
        return make_response(id, {
            "content": [{"type": "text", "text": json.dumps({"error": str(exc)})}],
            "isError": True,
        })


def handle_notifications_initialized(params: dict) -> None:
    """Handle the initialized notification (no response needed)."""
    log("Client initialized")


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

METHOD_HANDLERS = {
    "initialize": handle_initialize,
    "tools/list": handle_tools_list,
    "tools/call": handle_tools_call,
}

NOTIFICATION_HANDLERS = {
    "notifications/initialized": handle_notifications_initialized,
}


def send(msg: dict) -> None:
    """Write a JSON-RPC message to stdout."""
    raw = json.dumps(msg)
    sys.stdout.write(raw + "\n")
    sys.stdout.flush()


def main() -> None:
    log(f"Starting MCP server (repo: {REPO_ROOT})")
    log(f"Skills catalog: {SKILLS_JSON}")

    # Pre-load catalog
    catalog = load_catalog()
    log(f"Loaded {len(catalog.get('skills', []))} skills")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            msg = json.loads(line)
        except json.JSONDecodeError as exc:
            log(f"Malformed JSON: {exc}")
            send(make_error(None, -32700, f"Parse error: {exc}"))
            continue

        method = msg.get("method", "")
        params = msg.get("params", {})
        msg_id = msg.get("id")

        # Notifications have no id — don't send a response
        if msg_id is None:
            handler = NOTIFICATION_HANDLERS.get(method)
            if handler:
                handler(params)
            else:
                log(f"Unknown notification: {method}")
            continue

        handler = METHOD_HANDLERS.get(method)
        if handler:
            response = handler(msg_id, params)
            send(response)
        else:
            log(f"Unknown method: {method}")
            send(make_error(msg_id, -32601, f"Method not found: {method}"))


if __name__ == "__main__":
    main()
