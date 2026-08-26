#!/usr/bin/env python3
"""
notion_to_json.py — Query a Notion database and emit JSON for PM tools.

Stdlib only. Auth via env var.

Required env:
    NOTION_TOKEN      Integration token (notion.so/my-integrations)
    NOTION_VERSION    Optional, default 2022-06-28

Output formats:
    --format raw       Pass-through of Notion's /query response
    --format prds      Shape for a PRDs database (status, owner, target date, OKR relation)
    --format okrs      Shape for an OKRs database (type, parent, KR target/current, confidence)
    --format roadmap   Shape for a Roadmap database (horizon, status, owner, dates)
    --format feedback  Shape for a Feedback / Insights database (channel, customer, raw text)

Usage:
    export NOTION_TOKEN=secret_...
    python notion_to_json.py --database-id <uuid> --format prds
    python notion_to_json.py --database-id <uuid> --format feedback \\
      | python ../../project-management/execution/customer-feedback-triage/scripts/feedback_triage.py --input -
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


SCHEMA = "pm/adapters/notion/v1"
NOTION_API = "https://api.notion.com/v1"


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

def _token() -> str:
    t = os.environ.get("NOTION_TOKEN", "").strip()
    if not t:
        sys.exit("ERROR: NOTION_TOKEN must be set in env (notion.so/my-integrations)")
    return t


def _version() -> str:
    return os.environ.get("NOTION_VERSION", "2022-06-28").strip()


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {_token()}",
        "Notion-Version": _version(),
        "Content-Type": "application/json",
    }


def _post(path: str, body: dict, verbose: bool = False) -> dict:
    url = f"{NOTION_API}{path}"
    req = Request(url, data=json.dumps(body).encode("utf-8"), method="POST", headers=_headers())
    if verbose:
        print(f"[notion] POST {url}", file=sys.stderr)
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        msg = e.read().decode("utf-8", errors="replace")[:500]
        sys.exit(f"ERROR: Notion API {e.code}: {msg}")
    except URLError as e:
        sys.exit(f"ERROR: Notion network: {e}")


def query_database(database_id: str, filter_: dict | None = None, sorts: list | None = None,
                   verbose: bool = False) -> list[dict]:
    """Paginate /databases/{id}/query and collect all pages."""
    results: list[dict] = []
    cursor = None
    while True:
        body: dict = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        if filter_:
            body["filter"] = filter_
        if sorts:
            body["sorts"] = sorts
        data = _post(f"/databases/{database_id}/query", body, verbose=verbose)
        results.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
        if not cursor:
            break
    return results


# ---------------------------------------------------------------------------
# Property extractors
# ---------------------------------------------------------------------------

def _prop_value(prop: dict | None):
    """Extract a normalized value from a Notion property object."""
    if not prop:
        return None
    t = prop.get("type")
    v = prop.get(t)
    if v is None:
        return None
    if t == "title":
        return "".join(part.get("plain_text", "") for part in v)
    if t == "rich_text":
        return "".join(part.get("plain_text", "") for part in v)
    if t in ("select", "status"):
        return (v or {}).get("name")
    if t == "multi_select":
        return [item.get("name") for item in v]
    if t == "date":
        return (v or {}).get("start")
    if t == "people":
        return [p.get("name") for p in v]
    if t == "number":
        return v
    if t == "checkbox":
        return v
    if t == "url":
        return v
    if t == "email":
        return v
    if t == "relation":
        return [r.get("id") for r in v]
    if t == "formula":
        ftype = (v or {}).get("type")
        return (v or {}).get(ftype)
    if t == "rollup":
        rtype = (v or {}).get("type")
        return (v or {}).get(rtype)
    if t == "unique_id":
        prefix = (v or {}).get("prefix", "")
        num = (v or {}).get("number")
        return f"{prefix}-{num}" if prefix else num
    return v


def _row_props(page: dict) -> dict:
    """Flatten a Notion page's properties into {prop_name: value}."""
    flat = {}
    for name, prop in (page.get("properties") or {}).items():
        flat[name] = _prop_value(prop)
    return flat


# ---------------------------------------------------------------------------
# Format converters
# ---------------------------------------------------------------------------

def to_prds(pages: list[dict]) -> dict:
    rows = []
    for p in pages:
        f = _row_props(p)
        rows.append({
            "id": p.get("id"),
            "title": f.get("Title") or f.get("Name") or "",
            "status": f.get("Status"),
            "owner": (f.get("Owner") or [None])[0] if isinstance(f.get("Owner"), list) else f.get("Owner"),
            "priority": f.get("Priority"),
            "target_date": f.get("Target Date"),
            "approved_on": f.get("Approved On"),
            "shipped_on": f.get("Shipped On"),
            "linear_project": f.get("Linear Project"),
            "jira_epic": f.get("Jira Epic"),
            "okr_ids": f.get("OKR") if isinstance(f.get("OKR"), list) else [],
        })
    return {"prds": rows}


def to_okrs(pages: list[dict]) -> dict:
    rows = []
    for p in pages:
        f = _row_props(p)
        rows.append({
            "id": p.get("id"),
            "title": f.get("Title") or f.get("Name") or "",
            "type": f.get("Type"),
            "parent_objective_ids": f.get("Parent Objective") if isinstance(f.get("Parent Objective"), list) else [],
            "quarter": f.get("Quarter"),
            "owner": (f.get("Owner") or [None])[0] if isinstance(f.get("Owner"), list) else f.get("Owner"),
            "status": f.get("Status"),
            "confidence": f.get("Confidence"),
            "target": f.get("Target"),
            "current": f.get("Current"),
            "progress": f.get("Progress"),
        })
    return {"okrs": rows}


def to_roadmap(pages: list[dict]) -> dict:
    rows = []
    for p in pages:
        f = _row_props(p)
        rows.append({
            "id": p.get("id"),
            "title": f.get("Title") or f.get("Name") or "",
            "horizon": f.get("Horizon"),
            "status": f.get("Status"),
            "owner": (f.get("Owner") or [None])[0] if isinstance(f.get("Owner"), list) else f.get("Owner"),
            "customer_outcome": f.get("Customer Outcome"),
            "start": f.get("Start"),
            "end": f.get("End"),
            "confidence": f.get("Confidence"),
            "audience": f.get("Audience"),
        })
    return {"items": rows}


def to_feedback(pages: list[dict]) -> dict:
    """Feedback / Insights database -> feedback_triage.py input shape."""
    items = []
    for p in pages:
        f = _row_props(p)
        items.append({
            "id": p.get("id"),
            "channel": f.get("Channel") or f.get("Source") or "notion",
            "customer": f.get("Customer") or f.get("Account") or "",
            "raw": f.get("Note") or f.get("Insight") or f.get("Title") or "",
            "segment": f.get("Segment") or f.get("Tier") or "",
            "area": f.get("Area") or f.get("Feature Area") or "",
            "created_at": f.get("Created Time") or p.get("created_time"),
        })
    return {"items": items}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

CONVERTERS = {
    "prds": to_prds,
    "okrs": to_okrs,
    "roadmap": to_roadmap,
    "feedback": to_feedback,
}


def main():
    p = argparse.ArgumentParser(
        prog="notion_to_json.py",
        description="Query a Notion database and emit JSON for PM tools.",
    )
    p.add_argument("--database-id", required=True, help="Notion database UUID")
    p.add_argument("--format", choices=["raw"] + sorted(CONVERTERS.keys()), default="raw")
    p.add_argument("--filter", default=None, help="Inline JSON filter (passed to Notion query)")
    p.add_argument("--output", default=None)
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    filter_obj = None
    if args.filter:
        try:
            filter_obj = json.loads(args.filter)
        except json.JSONDecodeError as e:
            sys.exit(f"ERROR: --filter must be valid JSON: {e}")

    if args.dry_run:
        print(json.dumps({
            "url": f"{NOTION_API}/databases/{args.database_id}/query",
            "filter": filter_obj,
            "format": args.format,
        }, indent=2))
        return

    pages = query_database(args.database_id, filter_=filter_obj, verbose=args.verbose)

    if args.format == "raw":
        payload = {
            "schema": SCHEMA,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "database_id": args.database_id,
            "count": len(pages),
            "results": pages,
        }
    else:
        payload = CONVERTERS[args.format](pages)

    out = json.dumps(payload, indent=2) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
    else:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
