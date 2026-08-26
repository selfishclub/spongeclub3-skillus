#!/usr/bin/env bash
#
# build-dist.sh - Assemble the committed, browsable dist/ distribution folder.
#
# This is the folder users can navigate to at:
#   https://github.com/deanpeters/Product-Manager-Skills/tree/main/dist
#
# Layout produced (all tracked in git):
#   dist/README.md              plain-language landing page (renders on GitHub)
#   dist/CATALOG.md             browsable catalog of every skill, by category
#   dist/<skill>.zip            individual, upload-ready skill ZIPs (flat)
#   dist/packages/<pack>.zip    curated bundles + the Codex package
#
# It runs the existing build-release.sh (which validates + builds every
# artifact), then curates the tracked layout and regenerates the two docs.
# Nothing under dist/ is hand-maintained; re-run this to refresh it.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DIST="$ROOT/dist"

echo "[1/4] Building all release artifacts (validate + packs + codex + skill zips)"
bash "$SCRIPT_DIR/build-release.sh" >/dev/null
echo "  done"

echo "[2/4] Curating tracked layout"
# Clear the tracked parts (leave the ignored build scratch dirs in place)
find "$DIST" -maxdepth 1 -type f -name '*.zip' -delete 2>/dev/null || true
rm -rf "$DIST/packages"
mkdir -p "$DIST/packages"

# Individual skill ZIPs -> dist/ root (flat)
cp "$DIST"/skill-zips/*.zip "$DIST"/
skill_zip_count="$(find "$DIST" -maxdepth 1 -type f -name '*.zip' | wc -l | tr -d ' ')"

# Curated bundles + codex -> dist/packages/
for p in pm-skills-starter-pack 02-discovery-pack 03-strategy-pack \
         04-delivery-pack 05-ai-pm-pack 06-market-intel-pack \
         07-lifecycle-eol-pack 99-all-skills-pack; do
  cp "$DIST/claude-desktop/$p.zip" "$DIST/packages/"
done
cp "$DIST/codex/pm-skills-codex.zip" "$DIST/packages/"
echo "  $skill_zip_count individual skill ZIPs, $(find "$DIST/packages" -name '*.zip' | wc -l | tr -d ' ') packages"

echo "[3/4] Generating CATALOG.md and README.md"
python3 - "$ROOT" <<'PY'
import os, sys, glob
try:
    import yaml
except ImportError:
    sys.exit("PyYAML required (used elsewhere in this repo)")

root = sys.argv[1]
dist = os.path.join(root, "dist")
skills_dir = os.path.join(root, "skills")

def frontmatter(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    return yaml.safe_load(text[3:end]) or {}

skills = []
for p in sorted(glob.glob(os.path.join(skills_dir, "*", "SKILL.md"))):
    fm = frontmatter(p)
    name = fm.get("name") or os.path.basename(os.path.dirname(p))
    skills.append({
        "name": name,
        "type": (fm.get("type") or "other").lower(),
        "desc": (fm.get("description") or "").strip().strip('"'),
    })

TYPES = [
    ("component", "Component Skills", "Self-contained artifacts and templates."),
    ("interactive", "Interactive Skills", "Guided, multi-turn advisors that ask then recommend."),
    ("workflow", "Workflow Skills", "End-to-end processes that orchestrate other skills."),
]
by_type = {t: [s for s in skills if s["type"] == t] for t, _, _ in TYPES}
total = len(skills)

# ---- CATALOG.md ----
lines = [
    "# Skill Catalog",
    "",
    f"All **{total} skills** in this library. Each links to its individual "
    "download ZIP in this folder — click, download, unzip, and upload the "
    "`SKILL.md` to Claude. No terminal required.",
    "",
    "> New here? Read [`README.md`](README.md) first — it explains how to pick "
    "a pack and install.",
    "",
]
for key, title, blurb in TYPES:
    rows = sorted(by_type[key], key=lambda s: s["name"])
    if not rows:
        continue
    lines += [f"## {title} ({len(rows)})", "", f"_{blurb}_", "",
              "| Skill | What it does |", "|---|---|"]
    for s in rows:
        lines.append(f"| [`{s['name']}`]({s['name']}.zip) | {s['desc']} |")
    lines.append("")
open(os.path.join(dist, "CATALOG.md"), "w", encoding="utf-8").write("\n".join(lines))

# ---- README.md ----
readme = f"""# Product Manager Skills — Downloads

Welcome. This folder is the **easy download shelf** for the library — no code, no
terminal. Grab what you want, unzip it, and upload the skills to Claude.

There are **{total} skills** in total. Two ways to get them:

## 1. Grab a bundle (recommended)

Bundles live in [`packages/`](packages/). Download one ZIP, unzip it, and you'll
find upload-ready skill ZIPs inside.

| Bundle | Best for |
|---|---|
| [`pm-skills-starter-pack.zip`](packages/pm-skills-starter-pack.zip) | Most PMs — a small, practical starter set |
| [`02-discovery-pack.zip`](packages/02-discovery-pack.zip) | Understanding customers, problems, and opportunities |
| [`03-strategy-pack.zip`](packages/03-strategy-pack.zip) | Positioning, market thinking, product direction |
| [`04-delivery-pack.zip`](packages/04-delivery-pack.zip) | Stories, epics, PRDs, roadmap execution |
| [`05-ai-pm-pack.zip`](packages/05-ai-pm-pack.zip) | AI product work |
| [`06-market-intel-pack.zip`](packages/06-market-intel-pack.zip) | Competitive and market intelligence — the full suite |
| [`07-lifecycle-eol-pack.zip`](packages/07-lifecycle-eol-pack.zip) | Aging products — extend, replace, or retire, and how to sunset well |
| [`99-all-skills-pack.zip`](packages/99-all-skills-pack.zip) | Everything — all {total} skills |
| [`pm-skills-codex.zip`](packages/pm-skills-codex.zip) | OpenAI Codex users (`.agents/skills` + `AGENTS.md`) |

## 2. Grab one skill at a time

Every skill has its own ZIP right here in this folder. Browse them in
[`CATALOG.md`](CATALOG.md), then click the one you want.

## How to install (Claude Desktop / Web)

1. Download a bundle (or an individual skill ZIP).
2. If it's a bundle, unzip it to reveal the individual skill ZIPs.
3. In Claude, open **Skills** and upload the skill ZIP(s).
4. Start asking better product questions.

Full step-by-step guides live in [`../docs/`](../docs): `INSTALL-CLAUDE-DESKTOP.md`,
`INSTALL-CLAUDE-CODE.md`, and `INSTALL-CODEX.md`.

---

_This folder is generated by `scripts/build-dist.sh` from the canonical `skills/`
source. Don't edit files here by hand — re-run the script to refresh them._
"""
open(os.path.join(dist, "README.md"), "w", encoding="utf-8").write(readme)
print(f"  catalog + readme written ({total} skills)")
PY

echo "[4/4] dist/ assembled and ready to commit"
echo
echo "Tracked layout:"
echo "  dist/README.md"
echo "  dist/CATALOG.md"
echo "  dist/*.zip                ($skill_zip_count individual skills)"
echo "  dist/packages/*.zip       (bundles + codex)"
