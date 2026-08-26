#!/usr/bin/env bash
# claude.ai(웹·데스크톱 앱·폰) 업로드용 self-contained 스킬 패키지를 만든다.
# 터미널의 install.sh 는 ~/.claude/skills 에만 넣어서 claude.ai엔 스킬이 안 뜬다.
# 이 스크립트는 엔진(webdeck 포함)까지 통째로 담은 폴더 + zip 을 dist/ 에 만든다 → claude.ai에 업로드.
#
#   bash make-cloud-package.sh
#
# ※ claude.ai 업로더는 zip 안 '경로'에 한글(비ASCII)이 있으면 거부한다
#   ("Zip file contains path with invalid characters"). 그래서 폴더·파일명은 전부 ASCII로 바꾼다.
#   파일 '내용'의 한글은 문제없다 — 경로만 ASCII.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
DIST="$HERE/dist"
PKG="$DIST/skillers-share"          # ASCII 폴더명 (원래 공유회-OS)
ZIP="$DIST/skillers-share-claude-ai.zip"

echo "1/5  엔진 조립 (install.sh 를 임시 폴더에 실행 — webdeck 최신 포함)…"
TMP="$(mktemp -d)"
CLAUDE_SKILLS_DIR="$TMP" bash "$HERE/install.sh" >/dev/null 2>&1
[ -f "$TMP/공유회-OS/engine/generate_deck.py" ] || { echo "엔진 조립 실패 — 네트워크 확인"; exit 1; }

echo "2/5  패키지 폴더 구성 (self-contained)…"
rm -rf "$PKG"; mkdir -p "$PKG"
cp -R "$TMP/공유회-OS/." "$PKG/"      # SKILL.md + references + engine[webdeck 포함]
mkdir -p "$PKG/bundled"
cp -R "$HERE/bundled/." "$PKG/bundled/"

echo "3/5  경로 ASCII화 (claude.ai 요구)…"
# 부르는 스킬 폴더의 한글 이름 → ASCII (내용/frontmatter의 한글 name은 그대로 둔다)
[ -d "$PKG/bundled/훅카피" ]      && mv "$PKG/bundled/훅카피"      "$PKG/bundled/hookcopy"
[ -d "$PKG/bundled/크리틱디렉터" ] && mv "$PKG/bundled/크리틱디렉터" "$PKG/bundled/critic-director"
# (spec-guard 는 이미 ASCII)

# claude.ai는 zip에 SKILL.md가 '정확히 1개'만 있어야 한다. 번들 스킬의 SKILL.md → INSTRUCTIONS.md 로 바꿔
# 메인(skillers-share/SKILL.md) 하나만 남긴다. (메인 SKILL.md가 INSTRUCTIONS.md 를 읽도록 안내해 둠)
for b in "$PKG"/bundled/*/SKILL.md; do
  [ -f "$b" ] && mv "$b" "$(dirname "$b")/INSTRUCTIONS.md"
done

# claude.ai는 스킬 name(=루트 디렉토리명)도 영숫자·밑줄·하이픈만 허용한다.
# frontmatter의 한글 name(공유회-OS) → ASCII 슬러그. (트리거는 description에 있어 호출엔 영향 없음)
python3 - "$PKG/SKILL.md" <<'PY'
import sys, re
p = sys.argv[1]
t = open(p, encoding='utf-8').read()
t = re.sub(r'(?m)^name:\s*.*$', 'name: gongyuhoe-os', t, count=1)
open(p, 'w', encoding='utf-8').write(t)
PY

echo "4/5  업로드 안내 파일…"
cat > "$PKG/UPLOAD-README.txt" <<'TXT'
공유회-OS — claude.ai 업로드용 패키지 (skillers-share)

■ 올리는 곳
  claude.ai → Settings(설정) → 사용자 지정 → 스킬 → [추가 ▾] → 스킬 업로드
  이 폴더의 zip(skillers-share-claude-ai.zip)을 올린다. 같은 계정이면 웹·데스크톱 앱·폰에서 자동으로 뜬다.

■ 부르는 법
  "공유회 준비해줘"  (터미널과 동일)

■ 웹·앱에서 달라지는 것 (딱 2개 — 산출물 품질은 동일)
  · 대화 기록 자동 스캔 없음 → 발표 주제를 직접 알려주면 됨
  · 인터넷 링크 자동 배포 없음 → 덱이 HTML 파일(또는 Artifact)로 나옴, 그걸 공유
  나머지(질문·제목·목차·덱 디자인·발표 대본·검수)는 터미널과 같게 나온다.

■ 부르는 스킬은 이 폴더 bundled/ 안에 함께 들어있다 (hookcopy=훅카피, critic-director=크리틱디렉터, spec-guard).
TXT

echo "5/5  경로 무결성 검사 + zip…"
# 남은 non-ASCII 경로가 있으면 업로드가 또 거부되므로 여기서 잡는다
BADPATHS="$(cd "$DIST" && find skillers-share | LC_ALL=C grep -nP '[^\x00-\x7F]' || true)"
if [ -n "$BADPATHS" ]; then
  echo "✗ 아직 한글(비ASCII) 경로가 남아 있습니다 — 업로드가 거부됩니다:"; echo "$BADPATHS"; exit 1
fi
# SKILL.md 는 '정확히 1개'여야 한다 (claude.ai 규칙)
NSKILL="$(cd "$DIST" && find skillers-share -name SKILL.md | wc -l | tr -d ' ')"
if [ "$NSKILL" != "1" ]; then
  echo "✗ SKILL.md 가 $NSKILL 개입니다 — 정확히 1개여야 업로드됩니다."; exit 1
fi
# 스킬 name 이 영숫자·밑줄·하이픈만인지 (claude.ai 루트 디렉토리명 규칙)
NAMELINE="$(grep -m1 '^name:' "$PKG/SKILL.md" | sed 's/^name:[[:space:]]*//')"
if ! printf '%s' "$NAMELINE" | LC_ALL=C grep -qE '^[A-Za-z0-9_-]+$'; then
  echo "✗ 스킬 name '$NAMELINE' 에 허용 안 되는 문자가 있습니다 (영숫자·_·- 만)."; exit 1
fi
( cd "$DIST" && rm -f "$(basename "$ZIP")" && zip -qr "$(basename "$ZIP")" "skillers-share" )
rm -rf "$TMP"

echo
echo "완료 (경로 전부 ASCII 확인됨):"
echo "  폴더  $PKG"
echo "  zip   $ZIP"
echo "→ 이 zip 을 claude.ai 설정의 스킬 업로드에 올리세요 (웹·데스크톱 앱·폰 공용)."
