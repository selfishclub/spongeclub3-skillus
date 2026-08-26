#!/usr/bin/env python3
"""SessionStart hook: surface a notice if the skill registry is stale.

Compares registry.json's generated_at timestamp against the newest SKILL.md
mtime. If any SKILL.md is newer than the registry, the registry is stale and
the user should regenerate via:

    python scripts/build_manifest.py

Output goes to stdout as a short status line (no JSON envelope) so it lands
in the session-start preamble without interrupting the user.

Stdlib-only. No network calls. Fails open (silent) on any error.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def main() -> int:
    root = repo_root()
    registry = root / "registry.json"
    if not registry.exists():
        print(
            "[skill-check] registry.json not found — run "
            "`python scripts/build_manifest.py` to generate it."
        )
        return 0

    try:
        data = json.loads(registry.read_text(encoding="utf-8"))
        generated_at = datetime.fromisoformat(data["generated_at"])
    except (json.JSONDecodeError, KeyError, ValueError):
        return 0

    registry_ts = generated_at.timestamp()
    newest_skill_mtime = 0.0
    newest_skill_path = ""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if not d.startswith(".") and d not in {"node_modules", "__pycache__"}
        ]
        for fname in filenames:
            if fname != "SKILL.md":
                continue
            p = Path(dirpath) / fname
            try:
                mtime = p.stat().st_mtime
            except OSError:
                continue
            if mtime > newest_skill_mtime:
                newest_skill_mtime = mtime
                newest_skill_path = str(p.relative_to(root))

    if newest_skill_mtime > registry_ts + 5:
        delta_h = (newest_skill_mtime - registry_ts) / 3600
        print(
            f"[skill-check] registry.json is stale "
            f"({delta_h:.1f}h behind {newest_skill_path}). "
            f"Run `python scripts/build_manifest.py` to refresh."
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
