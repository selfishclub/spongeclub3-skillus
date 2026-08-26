#!/usr/bin/env python3
"""
jira_to_json.py — Pull Jira issues via JQL and emit JSON in the shape PM tools expect.

Stdlib only. Auth via env vars.

Required env:
    JIRA_URL    https://your-org.atlassian.net
    JIRA_USER   you@example.com
    JIRA_TOKEN  API token from id.atlassian.com/manage-profile/security/api-tokens

Output formats:
    --format raw            Pass-through of Jira's /search response
    --format status-update  Shape consumed by status_generator.py
    --format cycle-time     Shape consumed by flow_metrics.py
    --format dependency-map Shape consumed by dependency_graph.py

Usage:
    export JIRA_URL=https://acme.atlassian.net
    export JIRA_USER=you@acme.com
    export JIRA_TOKEN=...
    python jira_to_json.py --jql "project = PROJ AND sprint in openSprints()" --format status-update

    # Piped:
    python jira_to_json.py --jql "..." --format cycle-time \\
      | python ../../project-management/execution/cycle-time-analyzer/scripts/flow_metrics.py --input -
"""

import argparse
import base64
import json
import os
import sys
from datetime import datetime, timezone
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


SCHEMA = "pm/adapters/jira/v1"


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

def _auth_header() -> str:
    user = os.environ.get("JIRA_USER", "").strip()
    token = os.environ.get("JIRA_TOKEN", "").strip()
    if not user or not token:
        sys.exit("ERROR: JIRA_USER and JIRA_TOKEN must be set in env")
    raw = f"{user}:{token}".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def _api_base() -> str:
    url = os.environ.get("JIRA_URL", "").strip().rstrip("/")
    if not url:
        sys.exit("ERROR: JIRA_URL must be set in env (e.g. https://acme.atlassian.net)")
    return url


def _get(path: str, params: dict | None = None, verbose: bool = False) -> dict:
    base = _api_base()
    if params:
        qs = "&".join(f"{k}={quote(str(v))}" for k, v in params.items() if v is not None)
        url = f"{base}{path}?{qs}"
    else:
        url = f"{base}{path}"
    req = Request(url, headers={
        "Authorization": _auth_header(),
        "Accept": "application/json",
    })
    if verbose:
        print(f"[jira] GET {url}", file=sys.stderr)
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        sys.exit(f"ERROR: Jira API {e.code}: {body}")
    except URLError as e:
        sys.exit(f"ERROR: Jira network: {e}")


def _search(jql: str, fields: list[str], max_results: int = 200, verbose: bool = False) -> list[dict]:
    """Paginate /search and collect issues. Caps total at max_results."""
    issues: list[dict] = []
    start = 0
    page_size = 100
    while len(issues) < max_results:
        page = _get("/rest/api/3/search", {
            "jql": jql,
            "fields": ",".join(fields),
            "expand": "changelog",
            "startAt": start,
            "maxResults": min(page_size, max_results - len(issues)),
        }, verbose=verbose)
        batch = page.get("issues", []) or []
        issues.extend(batch)
        total = page.get("total", 0)
        if not batch or len(issues) >= total:
            break
        start += len(batch)
    return issues[:max_results]


# ---------------------------------------------------------------------------
# Shape converters
# ---------------------------------------------------------------------------

def _txt(adf: dict | str | None) -> str:
    """Flatten an Atlassian Document Format value (or string) to plain text."""
    if not adf:
        return ""
    if isinstance(adf, str):
        return adf.strip()
    out = []
    def walk(node):
        if not isinstance(node, dict):
            return
        if node.get("type") == "text":
            out.append(node.get("text", ""))
        for child in node.get("content", []) or []:
            walk(child)
    walk(adf)
    return " ".join(out).strip()


def to_status_update(issues: list[dict], project: str, period: str) -> dict:
    """Convert issues into the status_generator.py input shape.

    Heuristic mapping:
      - issues resolved this period -> highlights
      - issues with status Blocked / Impediment -> blockers
      - issues labeled "risk" or priority Highest -> risks
      - everything else (in progress) -> next
    """
    highlights, blockers, risks, nxt = [], [], [], []
    for it in issues:
        key = it.get("key", "")
        f = it.get("fields", {})
        status = (f.get("status", {}) or {}).get("name", "")
        summary = f.get("summary", "").strip()
        labels = [l for l in f.get("labels", []) or []]
        priority = (f.get("priority", {}) or {}).get("name", "")
        assignee = ((f.get("assignee") or {}).get("displayName") or "").strip()

        if status.lower() in ("done", "closed", "resolved", "shipped"):
            highlights.append({
                "title": summary,
                "detail": f"Closed by {assignee or 'team'}.",
                "ticket": key,
            })
        elif status.lower() in ("blocked", "impediment", "on hold"):
            blockers.append({
                "what": summary,
                "blocked_by": "(see Jira ticket for details)",
                "need": f"Unblock {key}",
            })
        elif "risk" in labels or priority.lower() in ("highest", "blocker"):
            risks.append({
                "risk": summary,
                "likelihood": "M",
                "impact": "H" if priority.lower() in ("highest", "blocker") else "M",
                "mitigation": f"Track {key}",
                "owner": assignee or "PM",
                "due": "TBD",
            })
        elif status.lower() in ("in progress", "in review", "to do"):
            nxt.append({
                "title": summary,
                "detail": f"Status: {status}. Owner: {assignee or 'unassigned'}.",
            })

    return {
        "period": period,
        "project": project,
        "author": os.environ.get("JIRA_USER", "PM"),
        "status": "yellow" if blockers else ("green" if highlights and not risks else "yellow"),
        "status_rationale": (
            f"{len(highlights)} shipped, {len(blockers)} blockers, {len(risks)} risks."
        ),
        "highlights": highlights[:5],
        "blockers": blockers[:5],
        "risks": risks[:5],
        "asks": [],
        "next": nxt[:5],
    }


def to_cycle_time(issues: list[dict]) -> dict:
    """Convert issues into the flow_metrics.py input shape (issue transitions)."""
    out = []
    for it in issues:
        key = it.get("key", "")
        f = it.get("fields", {})
        created = f.get("created", "")
        transitions: list[dict] = []
        for h in (it.get("changelog", {}) or {}).get("histories", []) or []:
            ts = h.get("created", "")
            for item in h.get("items", []) or []:
                if item.get("field") == "status":
                    transitions.append({
                        "at": ts,
                        "from": item.get("fromString", ""),
                        "to": item.get("toString", ""),
                    })
        out.append({
            "key": key,
            "summary": f.get("summary", ""),
            "created": created,
            "current_status": (f.get("status", {}) or {}).get("name", ""),
            "transitions": transitions,
        })
    return {"issues": out}


def to_dependency_map(issues: list[dict]) -> dict:
    """Convert issues with 'is blocked by' / 'blocks' links into a dependency graph."""
    teams_seen = set()
    deps = []
    for it in issues:
        key = it.get("key", "")
        f = it.get("fields", {})
        my_team = ((f.get("components") or [{}])[0] or {}).get("name", "") or "Unknown"
        teams_seen.add(my_team)
        for link in f.get("issuelinks", []) or []:
            link_type = (link.get("type") or {}).get("name", "")
            inward = link.get("inwardIssue")
            outward = link.get("outwardIssue")
            if inward and link_type.lower() in ("blocks", "depends",  "is blocked by"):
                from_team = "Unknown"
                fkey = inward.get("key", "")
                deps.append({
                    "from_team": from_team,
                    "to_team": my_team,
                    "blocker": f"{fkey}: {inward.get('fields',{}).get('summary','')}",
                    "due": "",
                    "tickets": [fkey, key],
                })
                teams_seen.add(from_team)
            if outward and link_type.lower() in ("blocks", "is depended on by"):
                to_team = "Unknown"
                okey = outward.get("key", "")
                deps.append({
                    "from_team": my_team,
                    "to_team": to_team,
                    "blocker": f"{okey}: {outward.get('fields',{}).get('summary','')}",
                    "due": "",
                    "tickets": [key, okey],
                })
                teams_seen.add(to_team)
    return {"teams": sorted(teams_seen), "dependencies": deps}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

FORMATS = {
    "raw": ["summary", "status", "priority", "labels", "assignee", "components", "issuelinks", "created", "updated"],
    "status-update": ["summary", "status", "priority", "labels", "assignee"],
    "cycle-time": ["summary", "status", "created"],
    "dependency-map": ["summary", "status", "components", "issuelinks"],
}


def main():
    p = argparse.ArgumentParser(
        prog="jira_to_json.py",
        description="Pull Jira issues via JQL and emit JSON for PM tools.",
    )
    p.add_argument("--jql", required=True, help="JQL query")
    p.add_argument("--format", choices=sorted(FORMATS.keys()), default="raw")
    p.add_argument("--project", default="Project", help="Project name (for status-update format)")
    p.add_argument("--period", default=None, help="Period label (e.g. 'Week of 2026-05-22')")
    p.add_argument("--max-results", type=int, default=200)
    p.add_argument("--output", default=None, help="Output file (default: stdout)")
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--dry-run", action="store_true", help="Print the request shape without calling Jira")
    args = p.parse_args()

    if args.dry_run:
        print(json.dumps({
            "url": _api_base() + "/rest/api/3/search",
            "jql": args.jql,
            "fields": FORMATS[args.format],
            "max_results": args.max_results,
        }, indent=2))
        return

    issues = _search(args.jql, FORMATS[args.format], max_results=args.max_results, verbose=args.verbose)

    if args.format == "raw":
        payload = {
            "schema": SCHEMA,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "jql": args.jql,
            "count": len(issues),
            "issues": issues,
        }
    elif args.format == "status-update":
        period = args.period or f"Week of {datetime.utcnow().strftime('%Y-%m-%d')}"
        payload = to_status_update(issues, args.project, period)
    elif args.format == "cycle-time":
        payload = to_cycle_time(issues)
    elif args.format == "dependency-map":
        payload = to_dependency_map(issues)

    out = json.dumps(payload, indent=2) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
    else:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
