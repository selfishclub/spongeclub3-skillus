#!/usr/bin/env python3
"""
linear_to_json.py — Pull data from Linear's GraphQL API and emit JSON for PM tools.

Stdlib only. Auth via env var.

Required env:
    LINEAR_API_KEY    Personal API key from linear.app/settings/api

Output formats:
    --format raw            Pass-through of GraphQL response
    --format status-update  Shape consumed by status_generator.py
    --format cycle-time     Shape consumed by flow_metrics.py
    --format dependency-map Shape consumed by dependency_graph.py

Usage:
    export LINEAR_API_KEY=lin_api_...
    python linear_to_json.py --team ENG --format status-update --cycle current
    python linear_to_json.py --team ENG --format cycle-time --cycle previous \\
      | python ../../project-management/execution/cycle-time-analyzer/scripts/flow_metrics.py --input -
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


SCHEMA = "pm/adapters/linear/v1"
LINEAR_GRAPHQL = "https://api.linear.app/graphql"


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

def _api_key() -> str:
    k = os.environ.get("LINEAR_API_KEY", "").strip()
    if not k:
        sys.exit("ERROR: LINEAR_API_KEY must be set in env (linear.app/settings/api)")
    return k


def _post_graphql(query: str, variables: dict | None = None, verbose: bool = False) -> dict:
    body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = Request(
        LINEAR_GRAPHQL,
        data=body,
        method="POST",
        headers={
            "Authorization": _api_key(),
            "Content-Type": "application/json",
        },
    )
    if verbose:
        print(f"[linear] POST {LINEAR_GRAPHQL} ({len(body)} bytes)", file=sys.stderr)
    try:
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")[:500]
        sys.exit(f"ERROR: Linear API {e.code}: {body_text}")
    except URLError as e:
        sys.exit(f"ERROR: Linear network: {e}")
    if "errors" in data:
        sys.exit(f"ERROR: Linear GraphQL: {json.dumps(data['errors'])[:500]}")
    return data.get("data", {})


# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------

ISSUES_BY_CYCLE = """
query IssuesByCycle($teamKey: String!, $cycleType: CycleFilter!) {
  team(id: $teamKey) {
    name
    cycles(filter: $cycleType, first: 1) {
      nodes {
        id
        name
        number
        startsAt
        endsAt
        issues(first: 100) {
          nodes {
            identifier
            title
            description
            priority
            priorityLabel
            state { name type }
            assignee { name email }
            createdAt
            startedAt
            completedAt
            labels(first: 20) { nodes { name } }
            history(first: 50) {
              nodes {
                createdAt
                fromState { name }
                toState { name }
              }
            }
            relations(first: 20) {
              nodes {
                type
                relatedIssue { identifier title team { key name } }
              }
            }
          }
        }
      }
    }
  }
}
"""


def fetch_issues(team_key: str, cycle: str, verbose: bool = False) -> list[dict]:
    """cycle in {'current', 'previous', 'next', 'all'}."""
    cycle_filter = {
        "current": {"isActive": {"eq": True}},
        "previous": {"isPrevious": {"eq": True}},
        "next": {"isNext": {"eq": True}},
        "all": {},
    }.get(cycle, {"isActive": {"eq": True}})

    data = _post_graphql(ISSUES_BY_CYCLE, {
        "teamKey": team_key,
        "cycleType": cycle_filter,
    }, verbose=verbose)
    team = data.get("team") or {}
    cycles = (team.get("cycles") or {}).get("nodes") or []
    if not cycles:
        return []
    issues = (cycles[0].get("issues") or {}).get("nodes") or []
    return issues


# ---------------------------------------------------------------------------
# Shape converters
# ---------------------------------------------------------------------------

def to_status_update(issues: list[dict], project: str, period: str) -> dict:
    highlights, blockers, risks, nxt = [], [], [], []
    for it in issues:
        ident = it.get("identifier", "")
        title = it.get("title", "").strip()
        state = (it.get("state") or {}).get("name", "")
        state_type = (it.get("state") or {}).get("type", "")
        priority_label = it.get("priorityLabel", "")
        assignee = (it.get("assignee") or {}).get("name", "")
        labels = [n.get("name","") for n in (it.get("labels") or {}).get("nodes", []) or []]

        if state_type == "completed":
            highlights.append({
                "title": title,
                "detail": f"Completed by {assignee or 'team'}.",
                "ticket": ident,
            })
        elif state.lower() in ("blocked", "on hold", "paused") or "blocked" in labels:
            blockers.append({
                "what": title,
                "blocked_by": "(see Linear issue for details)",
                "need": f"Unblock {ident}",
            })
        elif priority_label.lower() in ("urgent", "high") or "risk" in labels:
            risks.append({
                "risk": title,
                "likelihood": "M",
                "impact": "H" if priority_label.lower() == "urgent" else "M",
                "mitigation": f"Track {ident}",
                "owner": assignee or "PM",
                "due": (it.get("dueDate") or "TBD"),
            })
        elif state_type in ("started", "unstarted"):
            nxt.append({
                "title": title,
                "detail": f"Status: {state}. Owner: {assignee or 'unassigned'}.",
            })

    return {
        "period": period,
        "project": project,
        "author": "PM",
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
    out = []
    for it in issues:
        transitions = []
        for h in (it.get("history") or {}).get("nodes", []) or []:
            from_state = (h.get("fromState") or {}).get("name", "")
            to_state = (h.get("toState") or {}).get("name", "")
            if from_state or to_state:
                transitions.append({
                    "at": h.get("createdAt", ""),
                    "from": from_state,
                    "to": to_state,
                })
        out.append({
            "key": it.get("identifier", ""),
            "summary": it.get("title", ""),
            "created": it.get("createdAt", ""),
            "current_status": (it.get("state") or {}).get("name", ""),
            "transitions": transitions,
        })
    return {"issues": out}


def to_dependency_map(issues: list[dict]) -> dict:
    teams_seen = set()
    deps = []
    for it in issues:
        my_ident = it.get("identifier", "")
        my_team = my_ident.split("-")[0] if "-" in my_ident else "Unknown"
        teams_seen.add(my_team)
        for rel in (it.get("relations") or {}).get("nodes", []) or []:
            rel_type = rel.get("type", "")
            related = rel.get("relatedIssue") or {}
            other_team = (related.get("team") or {}).get("key", "") or (related.get("identifier","").split("-")[0] if related.get("identifier") else "Unknown")
            teams_seen.add(other_team)
            if rel_type == "blocks":
                deps.append({
                    "from_team": my_team,
                    "to_team": other_team,
                    "blocker": f"{my_ident}: {it.get('title','')}",
                    "tickets": [my_ident, related.get("identifier","")],
                })
            elif rel_type == "blocked_by":
                deps.append({
                    "from_team": other_team,
                    "to_team": my_team,
                    "blocker": f"{related.get('identifier','')}: {related.get('title','')}",
                    "tickets": [related.get("identifier",""), my_ident],
                })
    return {"teams": sorted(teams_seen), "dependencies": deps}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

FORMATS = ("raw", "status-update", "cycle-time", "dependency-map")


def main():
    p = argparse.ArgumentParser(
        prog="linear_to_json.py",
        description="Pull data from Linear GraphQL and emit JSON for PM tools.",
    )
    p.add_argument("--team", required=True, help="Linear team key (e.g. ENG, PROD)")
    p.add_argument("--cycle", choices=("current", "previous", "next", "all"), default="current")
    p.add_argument("--format", choices=FORMATS, default="raw")
    p.add_argument("--project", default="Project", help="Project name for status-update format")
    p.add_argument("--period", default=None, help="Period label override")
    p.add_argument("--output", default=None, help="Output file (default: stdout)")
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--dry-run", action="store_true", help="Print the request shape without calling Linear")
    args = p.parse_args()

    if args.dry_run:
        print(json.dumps({"url": LINEAR_GRAPHQL, "team": args.team, "cycle": args.cycle, "format": args.format}, indent=2))
        return

    issues = fetch_issues(args.team, args.cycle, verbose=args.verbose)

    if args.format == "raw":
        payload = {
            "schema": SCHEMA,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "team": args.team,
            "cycle": args.cycle,
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
