#!/usr/bin/env bash
# 스킬러스 공유회 설치.
#
#   bash install.sh          이미 있는 스킬은 건드리지 않는다
#   bash install.sh --force  이미 있어도 백업하고 최신으로 교체한다
#
# 함께 쓰는 스킬 3종은 설치할 때마다 원본 저장소에서 최신을 받아온다.
# 네트워크가 없으면 bundled/ 의 동봉본으로 떨어진다.
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
STAMP="$(date +%Y%m%d-%H%M%S)"
FORCE=0
[ "${1:-}" = "--force" ] && FORCE=1

# ── 0) 부트스트랩 — checkout 밖에서 실행되면(예: curl | bash) 저장소를 받아 다시 실행한다.
#     그래서 "한 줄 설치"가 가능하다:
#       curl -fsSL https://raw.githubusercontent.com/Koo-bon/skillers-share/main/install.sh | bash
if [ ! -f "$SRC/SKILL.md" ] || [ ! -f "$SRC/engine/build-deck.sh" ]; then
  command -v git >/dev/null 2>&1 || { echo "git 이 필요합니다. 맥: xcode-select --install"; exit 1; }
  echo "공유회-OS 저장소를 받는 중… (git clone)"
  BOOT="$(mktemp -d)"
  git clone --depth 1 https://github.com/Koo-bon/skillers-share.git "$BOOT/repo" >/dev/null 2>&1 \
    || { echo "클론 실패 — 인터넷 연결을 확인하세요."; exit 1; }
  exec bash "$BOOT/repo/install.sh" "$@"
fi

WEBDECK_RAW="https://raw.githubusercontent.com/Koo-bon/webdeck/main"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# ── 1) 공유회-OS 본체
mkdir -p "$DEST/공유회-OS/engine"
cp "$SRC/SKILL.md" "$DEST/공유회-OS/"
cp -R "$SRC/references" "$DEST/공유회-OS/"
cp "$SRC/engine/share-extend.css" "$SRC/engine/share-extend.js" \
   "$SRC/engine/build-deck.sh" "$SRC/engine/deploy.sh" "$DEST/공유회-OS/engine/"
chmod +x "$DEST/공유회-OS/engine/build-deck.sh" "$DEST/공유회-OS/engine/deploy.sh"

# ── 2) webdeck 덱 엔진 (항상 원본에서, 무수정)
echo "webdeck 엔진 내려받는 중…"
for f in index.html generate_deck.py brief_template.json; do
  curl -fsSL "$WEBDECK_RAW/webdeck/$f" -o "$DEST/공유회-OS/engine/$f"
done
mkdir -p "$DEST/공유회-OS/engine/references"
curl -fsSL "$WEBDECK_RAW/webdeck/references/slide-types.md" \
  -o "$DEST/공유회-OS/engine/engine-slide-types.tmp" \
  && mv "$DEST/공유회-OS/engine/engine-slide-types.tmp" \
        "$DEST/공유회-OS/engine/references/slide-types.md"

# ── 3) 함께 쓰는 스킬 3종
# 원본 tarball 을 받아 최신을 쓰고, 실패하면 동봉본을 쓴다.
echo
echo "함께 쓰는 스킬 확인 중…"

fetch_latest() {  # $1=스킬명 → $TMP/latest/<스킬명> 에 놓이면 0
  local name="$1"
  case "$name" in
    훅카피|크리틱디렉터)
      curl -fsSL "https://github.com/Koo-bon/webdeck/archive/refs/heads/main.tar.gz" \
        -o "$TMP/webdeck.tgz" 2>/dev/null || return 1
      tar xzf "$TMP/webdeck.tgz" -C "$TMP" 2>/dev/null || return 1
      [ -d "$TMP/webdeck-main/$name" ] || return 1
      mkdir -p "$TMP/latest" && cp -R "$TMP/webdeck-main/$name" "$TMP/latest/" ;;
    spec-guard)
      curl -fsSL "https://github.com/Koo-bon/spec-guard/archive/refs/heads/main.tar.gz" \
        -o "$TMP/sg.tgz" 2>/dev/null || return 1
      tar xzf "$TMP/sg.tgz" -C "$TMP" 2>/dev/null || return 1
      [ -f "$TMP/spec-guard-main/SKILL.md" ] || return 1
      mkdir -p "$TMP/latest/spec-guard"
      cp "$TMP/spec-guard-main/SKILL.md" "$TMP/spec-guard-main/RULES"*.md \
         "$TMP/spec-guard-main/"*.sh "$TMP/latest/spec-guard/" 2>/dev/null ;;
  esac
  [ -f "$TMP/latest/$name/SKILL.md" ]
}

for s in 훅카피 크리틱디렉터 spec-guard; do
  if [ -d "$DEST/$s" ] && [ "$FORCE" -eq 0 ]; then
    echo "  · $s — 이미 있음, 그대로 둡니다 (교체하려면 --force)"
    continue
  fi

  if fetch_latest "$s"; then
    from="$TMP/latest/$s"; src_label="원본 최신"
  else
    from="$SRC/bundled/$s";  src_label="동봉본 (네트워크 실패)"
  fi

  if [ -d "$DEST/$s" ]; then
    mv "$DEST/$s" "$DEST/$s.backup-$STAMP"
    echo "  · $s — $src_label 으로 교체 (기존 것은 $s.backup-$STAMP)"
  else
    echo "  · $s — 설치 ($src_label)"
  fi
  rm -rf "$DEST/$s" && cp -R "$from" "$DEST/$s"
done

echo
echo "설치 완료: $DEST"
echo
echo "Claude Code(터미널)에서 부르세요:  공유회 준비해줘"
echo "  ※ 터미널이 가장 완전 (기록 자동 스캔·인터넷 배포까지)"
echo "  ※ claude.ai 웹·앱·폰에서도 쓰려면(업로드 1회, 채팅 링크 설치는 claude.ai가 지원 안 함):"
echo "     릴리스 zip 받기 → 설정→사용자 지정→스킬→추가→스킬 업로드에 드래그"
echo "     https://github.com/Koo-bon/skillers-share/releases/latest/download/skillers-share-claude-ai.zip"
echo "나중에 최신으로 올리려면:    bash install.sh --force"
