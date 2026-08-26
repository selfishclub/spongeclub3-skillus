#!/usr/bin/env bash
# 홍보덱 만들기 — 이미지 경로는 절대경로여야 해서 여기서 채운다.
#   bash promo/build.sh   →  promo/out/index.html
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
sed "s|__HERE__|$HERE|g" "$HERE/brief.json" > "$HERE/.brief.built.json"
ENG="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/공유회-OS/engine"
[ -f "$ENG/generate_deck.py" ] || { echo "먼저 설치하세요:  bash install.sh"; exit 1; }
bash "$ENG/build-deck.sh" "$HERE/.brief.built.json" "$HERE/out" bold-color
rm -f "$HERE/.brief.built.json"
echo "확인:  cd $HERE/out && python3 -m http.server 8955"
