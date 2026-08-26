#!/usr/bin/env python3
"""Batch create command files and fix compatibility fields across all skill repos."""
import os
import re

# ============================================================
# 1. COMMAND FILES TO CREATE (claude-skills)
# ============================================================
CLAUDE_SKILLS = "/Users/jez/Documents/claude-skills"

claude_skills_commands = {
    "cloudflare": {
        "cloudflare-worker-builder": {
            "description": "Scaffold and deploy a Cloudflare Worker with Hono routing",
            "argument-hint": "[project-name]",
            "body": "Load the `cloudflare-worker-builder` skill.\n\nIf $ARGUMENTS contains a project name, use it. Otherwise ask.\n\nScaffolds a Cloudflare Worker with Hono routing, Vite plugin, and static assets.",
        },
        "vite-flare-starter": {
            "description": "Scaffold a full-stack Cloudflare app from vite-flare-starter",
            "argument-hint": "[project-name]",
            "body": "Load the `vite-flare-starter` skill.\n\nIf $ARGUMENTS contains a project name, use it. Otherwise ask.\n\nClones vite-flare-starter, configures bindings, and deploys.",
        },
        "d1-drizzle-schema": {
            "description": "Generate a Drizzle ORM schema for Cloudflare D1",
            "argument-hint": "[table-names...]",
            "body": "Load the `d1-drizzle-schema` skill.\n\nIf $ARGUMENTS contains table names, use them as starting points. Otherwise analyse the project.",
        },
        "d1-migration": {
            "description": "Run D1 migration workflow — generate, inspect, apply",
            "argument-hint": "[generate|apply|fix|status]",
            "body": "Load the `d1-migration` skill.\n\nParse $ARGUMENTS for action:\n- `generate` — generate migration from schema changes\n- `apply` — apply pending migrations (local + remote)\n- `fix` — fix stuck or failed migrations\n- `status` — show migration status\n\nDefault: `status` if no argument.",
        },
        "hono-api-scaffolder": {
            "description": "Scaffold Hono API routes for a Cloudflare Worker",
            "argument-hint": "[resource-name...]",
            "body": "Load the `hono-api-scaffolder` skill.\n\nIf $ARGUMENTS contains resource names (e.g. users, posts), scaffold routes for them. Otherwise analyse the project.",
        },
        "db-seed": {
            "description": "Generate database seed scripts with realistic data",
            "argument-hint": "[small|medium|large] [dev|demo|test]",
            "body": "Load the `db-seed` skill.\n\nParse $ARGUMENTS for:\n- **Volume**: `small` (5-10 rows), `medium` (20-50), `large` (100+). Default: small\n- **Purpose**: `dev`, `demo`, or `test`. Default: dev\n\nExamples: `/db-seed large demo`, `/db-seed`, `/db-seed test`",
        },
    },
    "frontend": {
        "landing-page": {
            "description": "Generate a deployable landing page from a brief",
            "argument-hint": "[business-name]",
            "body": "Load the `landing-page` skill.\n\nIf $ARGUMENTS contains a business name, use it. Otherwise ask for a brief.\n\nProduces a single self-contained HTML file with Tailwind CDN.",
        },
        "shadcn-ui": {
            "description": "Install and configure shadcn/ui components",
            "argument-hint": "[component-name...]",
            "body": "Load the `shadcn-ui` skill.\n\nIf $ARGUMENTS contains component names (e.g. button dialog table), install them. Otherwise guide component selection.",
        },
        "tailwind-theme-builder": {
            "description": "Set up Tailwind v4 theming with CSS variables and dark mode",
            "argument-hint": "[hex-color]",
            "body": "Load the `tailwind-theme-builder` skill.\n\nIf $ARGUMENTS contains a hex colour, use it as the primary brand colour. Otherwise ask or use defaults.",
        },
        "product-showcase": {
            "description": "Generate a marketing site from a running app with real screenshots",
            "argument-hint": "[url]",
            "body": "Load the `product-showcase` skill.\n\nIf $ARGUMENTS contains a URL, use it as the app to showcase. Otherwise check for a running dev server or ask.",
        },
    },
    "design-assets": {
        "ai-image-generator": {
            "description": "Generate AI images using Gemini or GPT APIs",
            "argument-hint": "[hero|icon|og|illustration] [description]",
            "body": "Load the `ai-image-generator` skill.\n\nParse $ARGUMENTS for:\n- **Purpose**: `hero`, `icon`, `og`, `illustration` (optional)\n- **Description**: what to generate\n\nExamples: `/ai-image-generator hero modern office space`, `/ai-image-generator icon wrench tool`",
        },
        "color-palette": {
            "description": "Generate an accessible colour palette from a hex value",
            "argument-hint": "[hex-color]",
            "body": "Load the `color-palette` skill.\n\nIf $ARGUMENTS contains a hex colour (e.g. #1E40AF), generate a full palette from it. Otherwise ask for a brand colour.",
        },
        "favicon-gen": {
            "description": "Generate a favicon package from a logo or brand",
            "argument-hint": "[logo-path|text|hex-color]",
            "body": "Load the `favicon-gen` skill.\n\nParse $ARGUMENTS for a logo file path, text initials, or hex colour to generate from. Otherwise ask.",
        },
        "icon-set-generator": {
            "description": "Generate a cohesive SVG icon set for a project",
            "argument-hint": "[icon-names...]",
            "body": "Load the `icon-set-generator` skill.\n\nIf $ARGUMENTS contains icon names (e.g. home settings user), generate those. Otherwise analyse the project for needed icons.",
        },
        "image-processing": {
            "description": "Resize, convert, or optimise images for web",
            "argument-hint": "[image-path] [operation]",
            "body": "Load the `image-processing` skill.\n\nParse $ARGUMENTS for an image path and operation (resize, convert, trim, optimise). Otherwise ask what to process.",
        },
    },
    "dev-tools": {
        "project-docs": {
            "description": "Generate project documentation from codebase analysis",
            "argument-hint": "[all|architecture|api|database]",
            "body": "Load the `project-docs` skill.\n\nParse $ARGUMENTS for which docs to generate:\n- `all` — ARCHITECTURE.md + API_ENDPOINTS.md + DATABASE_SCHEMA.md\n- `architecture` — ARCHITECTURE.md only\n- `api` — API_ENDPOINTS.md only\n- `database` — DATABASE_SCHEMA.md only\n\nDefault: detect what's needed based on project type.",
        },
        "app-docs": {
            "description": "Generate a user guide with screenshots from a running app",
            "argument-hint": "[quick|standard|thorough] [url]",
            "body": "Load the `app-docs` skill.\n\nParse $ARGUMENTS for:\n- **Depth**: `quick` (~10 screenshots), `standard` (~30), `thorough` (~80+). Default: standard\n- **URL**: app to document. If not provided, check for a running dev server or ask.",
        },
        "brains-trust": {
            "description": "Get a second opinion from other AI models",
            "argument-hint": "[question or topic]",
            "body": "Load the `brains-trust` skill.\n\nIf $ARGUMENTS contains a question, use it as the topic. Otherwise ask what they want a second opinion on.\n\nQueries models via OpenRouter, Gemini, or OpenAI APIs.",
        },
        "git-workflow": {
            "description": "Guided git workflows — PRs, branch cleanup, conflict resolution",
            "argument-hint": "[pr|clean|conflicts|tag]",
            "body": "Load the `git-workflow` skill.\n\nParse $ARGUMENTS for action:\n- `pr` — prepare a pull request\n- `clean` — clean up merged/stale branches\n- `conflicts` — resolve merge conflicts\n- `tag` — create a version tag\n\nDefault: detect what's needed from git status.",
        },
        "responsiveness-check": {
            "description": "Test responsive layout across viewport widths",
            "argument-hint": "[url]",
            "body": "Load the `responsiveness-check` skill.\n\nIf $ARGUMENTS contains a URL, test it. Otherwise check for a running dev server or ask.",
        },
        "agent-browser": {
            "description": "Browser automation for web interaction and testing",
            "argument-hint": "[url]",
            "body": "Load the `agent-browser` skill.\n\nIf $ARGUMENTS contains a URL, navigate to it. Otherwise ask what to do.\n\nUses playwright-cli for browser automation.",
        },
    },
    "integrations": {
        "gws-setup": {
            "description": "Set up the Google Workspace CLI from scratch",
            "argument-hint": "",
            "body": "Load the `gws-setup` skill.\n\nGuides through GCP project creation, OAuth credentials, authentication, and installing agent skills.",
        },
        "gws-install": {
            "description": "Install Google Workspace CLI on a new machine",
            "argument-hint": "",
            "body": "Load the `gws-install` skill.\n\nQuick install of gws using existing OAuth credentials from a previous setup.",
        },
        "google-chat-messages": {
            "description": "Send Google Chat messages via webhook",
            "argument-hint": "[webhook-url] [message]",
            "body": "Load the `google-chat-messages` skill.\n\nIf $ARGUMENTS contains a webhook URL and message, send it. Otherwise guide through webhook setup.",
        },
        "google-apps-script": {
            "description": "Build Google Apps Script automation",
            "argument-hint": "[spreadsheet-url|project-name]",
            "body": "Load the `google-apps-script` skill.\n\nIf $ARGUMENTS contains a spreadsheet URL or project name, use it. Otherwise ask what to automate.",
        },
        "elevenlabs-agents": {
            "description": "Build a conversational AI voice agent with ElevenLabs",
            "argument-hint": "[agent-name]",
            "body": "Load the `elevenlabs-agents` skill.\n\nIf $ARGUMENTS contains an agent name, use it. Otherwise ask about the agent's purpose.",
        },
        "mcp-builder": {
            "description": "Build an MCP server with FastMCP",
            "argument-hint": "[server-name]",
            "body": "Load the `mcp-builder` skill.\n\nIf $ARGUMENTS contains a server name, use it. Otherwise ask what tools/resources the server should expose.",
        },
    },
    "web-design": {
        "seo-local-business": {
            "description": "Generate SEO setup for a local business website",
            "argument-hint": "[business-name]",
            "body": "Load the `seo-local-business` skill.\n\nIf $ARGUMENTS contains a business name, use it. Otherwise ask for business details.\n\nGenerates JSON-LD schema, meta tags, robots.txt, and sitemap.",
        },
    },
    "knowledge-cortex": {
        "cortex-mine": {
            "description": "Mine Gmail history into a local knowledge base",
            "argument-hint": "[dry-run|from DATE]",
            "body": "Load the `cortex-mine` skill.\n\nParse $ARGUMENTS:\n- `dry-run` — preview what would be extracted without saving\n- `from YYYY-MM-DD` — only process emails from this date\n\nDefault: incremental mine from last run.",
        },
        "cortex-query": {
            "description": "Search your mined knowledge base",
            "argument-hint": "[search-term]",
            "body": "Load the `cortex-query` skill.\n\nIf $ARGUMENTS contains a search term, query for it. Otherwise show stats or ask what to search for.",
        },
    },
    "social-media": {
        "social-media-posts": {
            "description": "Create platform-specific social media posts",
            "argument-hint": "[linkedin|facebook|instagram|reddit|all] [topic]",
            "body": "Load the `social-media-posts` skill.\n\nParse $ARGUMENTS for:\n- **Platform**: `linkedin`, `facebook`, `instagram`, `reddit`, or `all`. Default: all\n- **Topic**: what to post about\n\nExamples: `/social-media-posts linkedin new feature launch`, `/social-media-posts all`",
        },
    },
    "writing": {
        "aussie-business-english": {
            "description": "Australian business English writing style",
            "argument-hint": "",
            "body": "Load the `aussie-business-english` skill.\n\nApply Australian business English conventions to the current writing task. EN-AU spelling, warm direct tone.",
        },
        "us-business-english": {
            "description": "American business English writing style",
            "argument-hint": "",
            "body": "Load the `us-business-english` skill.\n\nApply American business English conventions to the current writing task. EN-US spelling, direct action-oriented tone.",
        },
        "uk-business-english": {
            "description": "British business English writing style",
            "argument-hint": "",
            "body": "Load the `uk-business-english` skill.\n\nApply British business English conventions to the current writing task. EN-GB spelling, polished understated tone.",
        },
        "nz-business-english": {
            "description": "New Zealand business English writing style",
            "argument-hint": "",
            "body": "Load the `nz-business-english` skill.\n\nApply New Zealand business English conventions to the current writing task. EN-NZ spelling, warm inclusive tone.",
        },
        "resume-cover-letter": {
            "description": "Write a resume/CV or cover letter for a job application",
            "argument-hint": "[resume|cover-letter|both]",
            "body": "Load the `resume-cover-letter` skill.\n\nParse $ARGUMENTS for mode:\n- `resume` — resume/CV only\n- `cover-letter` — cover letter only\n- `both` — both documents\n\nDefault: both.",
        },
        "proposal-writer": {
            "description": "Write a client proposal or quote",
            "argument-hint": "[client-name]",
            "body": "Load the `proposal-writer` skill.\n\nIf $ARGUMENTS contains a client name, use it. Otherwise ask for project details.",
        },
        "award-application": {
            "description": "Write an award submission or grant application",
            "argument-hint": "[award-name]",
            "body": "Load the `award-application` skill.\n\nIf $ARGUMENTS contains an award name, use it. Otherwise ask for award details and criteria.",
        },
        "strategy-document": {
            "description": "Write a strategic business document",
            "argument-hint": "[swot|plan|okrs|competitive]",
            "body": "Load the `strategy-document` skill.\n\nParse $ARGUMENTS for document type:\n- `swot` — SWOT analysis\n- `plan` — lean business plan\n- `okrs` — OKR goal framework\n- `competitive` — competitive analysis\n\nDefault: ask what type of strategic document.",
        },
    },
    "shopify": {
        "shopify-setup": {
            "description": "Set up Shopify CLI auth and Admin API access",
            "argument-hint": "[store-url]",
            "body": "Load the `shopify-setup` skill.\n\nIf $ARGUMENTS contains a store URL, use it. Otherwise ask for the store.",
        },
        "shopify-products": {
            "description": "Create and manage Shopify products",
            "argument-hint": "[product-name|csv-path]",
            "body": "Load the `shopify-products` skill.\n\nIf $ARGUMENTS contains a product name or CSV path, use it. Otherwise ask what products to manage.",
        },
        "shopify-content": {
            "description": "Create Shopify pages, blog posts, and content",
            "argument-hint": "[page|blog|nav] [title]",
            "body": "Load the `shopify-content` skill.\n\nParse $ARGUMENTS for content type and title. Otherwise ask what content to create.",
        },
    },
    "wordpress": {
        "wordpress-setup": {
            "description": "Connect to a WordPress site via WP-CLI or REST API",
            "argument-hint": "[domain]",
            "body": "Load the `wordpress-setup` skill.\n\nIf $ARGUMENTS contains a domain, use it. Otherwise ask for the WordPress site.",
        },
        "wordpress-content": {
            "description": "Create and manage WordPress posts, pages, and media",
            "argument-hint": "[post|page] [title]",
            "body": "Load the `wordpress-content` skill.\n\nParse $ARGUMENTS for content type and title. Otherwise ask what to create.",
        },
        "wordpress-elementor": {
            "description": "Edit Elementor pages and manage templates",
            "argument-hint": "[page-url|page-id]",
            "body": "Load the `wordpress-elementor` skill.\n\nIf $ARGUMENTS contains a page URL or ID, edit it. Otherwise ask which page to edit.",
        },
    },
}

# ============================================================
# 2. COMMAND FILES TO CREATE (jez-skills)
# ============================================================
JEZ_SKILLS = "/Users/jez/Documents/jez-skills"

jez_skills_commands = {
    "jez": {
        "jezmail": {
            "description": "Newsletter workflow — draft, images, test, send, social posts",
            "argument-hint": "[draft|send|test|social|subscribers]",
            "body": "Load the `jezmail` skill.\n\nParse $ARGUMENTS for step:\n- `draft` — draft a new newsletter\n- `send` — send a drafted newsletter\n- `test` — send a test email\n- `social` — generate social posts from sent newsletter\n- `subscribers` — manage subscriber list\n\nDefault: show workflow options.",
        },
        "site-audit": {
            "description": "Comprehensive site health check — DNS, SSL, SEO, performance",
            "argument-hint": "<domain>",
            "body": "Load the `site-audit` skill.\n\nUse $ARGUMENTS as the domain to audit. Required — ask if not provided.",
        },
        "domain-dns-ops": {
            "description": "Manage domains and DNS records across Cloudflare and Synergy",
            "argument-hint": "[lookup|update|health] <domain>",
            "body": "Load the `domain-dns-ops` skill.\n\nParse $ARGUMENTS for action and domain:\n- `lookup example.com` — check DNS records\n- `update example.com` — modify records\n- `health example.com` — full health check (SSL, DNSSEC, propagation)\n\nDefault: lookup if just a domain provided.",
        },
        "web-scraper": {
            "description": "Build a purpose-specific web scraper",
            "argument-hint": "[url-or-description]",
            "body": "Load the `web-scraper` skill.\n\nIf $ARGUMENTS contains a URL or description, use it as the scraping target. Otherwise ask what to scrape.",
        },
        "flare-ai-app": {
            "description": "Scaffold an AI analytics app from vite-flare-ai-starter",
            "argument-hint": "[project-name]",
            "body": "Load the `flare-ai-app` skill.\n\nIf $ARGUMENTS contains a project name, use it. Otherwise ask for the app concept.",
        },
    },
    "l2chat": {
        "create-l2chat-agent": {
            "description": "Create and deploy a new L2Chat per-client agent",
            "argument-hint": "[client-name|domain]",
            "body": "Load the `create-l2chat-agent` skill.\n\nIf $ARGUMENTS contains a client name or domain, use it. Otherwise ask for the client details.",
        },
    },
}

# ============================================================
# 3. COMPATIBILITY FIXES (add claude-code-only where missing)
# ============================================================
add_compatibility = [
    # claude-skills
    f"{CLAUDE_SKILLS}/plugins/cloudflare/skills/d1-migration/SKILL.md",
    f"{CLAUDE_SKILLS}/plugins/cloudflare/skills/db-seed/SKILL.md",
    f"{CLAUDE_SKILLS}/plugins/dev-tools/skills/project-docs/SKILL.md",
    f"{CLAUDE_SKILLS}/plugins/dev-tools/skills/git-workflow/SKILL.md",
    f"{CLAUDE_SKILLS}/plugins/dev-tools/skills/agent-browser/SKILL.md",
    f"{CLAUDE_SKILLS}/plugins/frontend/skills/landing-page/SKILL.md",
    f"{CLAUDE_SKILLS}/plugins/frontend/skills/shadcn-ui/SKILL.md",
    f"{CLAUDE_SKILLS}/plugins/frontend/skills/tailwind-theme-builder/SKILL.md",
    f"{CLAUDE_SKILLS}/plugins/design-assets/skills/ai-image-generator/SKILL.md",
    f"{CLAUDE_SKILLS}/plugins/design-assets/skills/color-palette/SKILL.md",
    f"{CLAUDE_SKILLS}/plugins/design-assets/skills/favicon-gen/SKILL.md",
    f"{CLAUDE_SKILLS}/plugins/design-assets/skills/icon-set-generator/SKILL.md",
    f"{CLAUDE_SKILLS}/plugins/integrations/skills/google-apps-script/SKILL.md",
    f"{CLAUDE_SKILLS}/plugins/integrations/skills/google-chat-messages/SKILL.md",
    f"{CLAUDE_SKILLS}/plugins/integrations/skills/elevenlabs-agents/SKILL.md",
    f"{CLAUDE_SKILLS}/plugins/knowledge-cortex/skills/cortex-mine/SKILL.md",
    f"{CLAUDE_SKILLS}/plugins/knowledge-cortex/skills/cortex-query/SKILL.md",
    # jez-skills
    f"{JEZ_SKILLS}/plugins/jez/skills/jezmail/SKILL.md",
    f"{JEZ_SKILLS}/plugins/jez/skills/site-audit/SKILL.md",
    f"{JEZ_SKILLS}/plugins/jez/skills/wordpress-site-setup/SKILL.md",
    f"{JEZ_SKILLS}/plugins/l2chat/skills/create-l2chat-agent/SKILL.md",
]


def create_command_file(base_dir, plugin, skill, config):
    cmd_dir = os.path.join(base_dir, "plugins", plugin, "commands")
    os.makedirs(cmd_dir, exist_ok=True)
    cmd_file = os.path.join(cmd_dir, f"{skill}.md")

    if os.path.exists(cmd_file):
        print(f"  SKIP {plugin}:{skill} (already exists)")
        return False

    lines = ["---"]
    lines.append(f'description: {config["description"]}')
    if config.get("argument-hint"):
        lines.append(f'argument-hint: "{config["argument-hint"]}"')
    lines.append("---")
    lines.append("")
    lines.append(config["body"])
    lines.append("")

    with open(cmd_file, "w") as f:
        f.write("\n".join(lines))

    print(f"  CREATE {plugin}:{skill}")
    return True


def add_compatibility_field(filepath):
    if not os.path.exists(filepath):
        print(f"  SKIP {filepath} (not found)")
        return False

    with open(filepath, "r") as f:
        content = f.read()

    if "compatibility:" in content:
        print(f"  SKIP {os.path.basename(os.path.dirname(filepath))} (already has compatibility)")
        return False

    # Add compatibility after the last frontmatter field before ---
    # Find the closing --- of frontmatter
    lines = content.split("\n")
    closing_idx = None
    in_frontmatter = False
    for i, line in enumerate(lines):
        if line.strip() == "---":
            if not in_frontmatter:
                in_frontmatter = True
            else:
                closing_idx = i
                break

    if closing_idx is None:
        print(f"  ERROR {filepath} (no frontmatter found)")
        return False

    lines.insert(closing_idx, "compatibility: claude-code-only")

    with open(filepath, "w") as f:
        f.write("\n".join(lines))

    short = filepath.split("/skills/")[1].split("/SKILL.md")[0] if "/skills/" in filepath else filepath
    print(f"  ADD compatibility: claude-code-only → {short}")
    return True


# ============================================================
# EXECUTE
# ============================================================
print("=== Creating command files (claude-skills) ===")
created_cs = 0
for plugin, skills in claude_skills_commands.items():
    for skill, config in skills.items():
        if create_command_file(CLAUDE_SKILLS, plugin, skill, config):
            created_cs += 1

print(f"\n=== Creating command files (jez-skills) ===")
created_js = 0
for plugin, skills in jez_skills_commands.items():
    for skill, config in skills.items():
        if create_command_file(JEZ_SKILLS, plugin, skill, config):
            created_js += 1

print(f"\n=== Adding compatibility: claude-code-only ===")
fixed = 0
for filepath in add_compatibility:
    if add_compatibility_field(filepath):
        fixed += 1

print(f"\n=== SUMMARY ===")
print(f"Commands created (claude-skills): {created_cs}")
print(f"Commands created (jez-skills): {created_js}")
print(f"Compatibility fields added: {fixed}")
