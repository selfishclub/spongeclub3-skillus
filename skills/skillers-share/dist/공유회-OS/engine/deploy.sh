#!/usr/bin/env bash
# 만든 덱을 인터넷 주소로 올린다. 명령 한 줄.
#
#   bash deploy.sh <덱폴더> [저장소이름]
#
# 저장소 이름을 안 주면 폴더 이름을 쓴다.
# 끝나면 https://<계정>.github.io/<저장소이름>/ 이 나온다.
set -euo pipefail

DIR="${1:?덱 폴더 경로가 필요합니다. 예: bash deploy.sh ~/공유회/2026-08-06-내발표/out}"
[ -f "$DIR/index.html" ] || { echo "✗ $DIR 안에 index.html 이 없습니다. 덱 폴더가 맞나요?"; exit 1; }

NAME="${2:-$(basename "$(cd "$DIR/.." && pwd)")}"
# 깃허브 저장소 이름은 영숫자·하이픈만 된다. 한글은 사라지므로 그대로 쓰면
# "2026-08-03-내발표" 가 "2026-08-03" 이 돼 같은 날 발표끼리 충돌한다.
SAFE=$(echo "$NAME" | tr -c 'a-zA-Z0-9._-' '-' | sed 's/--*/-/g;s/^-//;s/-$//')
# 한글이 날아가 남은 게 부실하면(8자 미만) 시각을 붙여 반드시 유일하게 만든다
if [ "${#SAFE}" -lt 8 ]; then
  SAFE="deck-$(date +%Y%m%d-%H%M)"
elif [ -n "${2:-}" ]; then
  :                                   # 사용자가 직접 준 이름은 그대로 존중
else
  SAFE="deck-${SAFE}"                 # 자동 생성이면 접두사로 다른 저장소와 구분
fi

echo "덱 폴더 : $DIR"
echo "저장소   : $SAFE"
echo

# ── gh 없으면 여기서 멈추고 대안을 알려준다
if ! command -v gh >/dev/null 2>&1; then
  cat <<EOF
✗ gh(깃허브 명령도구)가 없어 자동 업로드를 못 합니다.

두 가지 방법이 있습니다.

  [A] gh 설치하고 다시 실행 (한 번만 하면 다음부턴 자동)
      brew install gh
      gh auth login          ← 브라우저가 열립니다. 로그인하세요
      bash deploy.sh "$DIR"

  [B] 손으로 올리기
      1. github.com 에서 저장소 '$SAFE' 를 Public 으로 만드세요
      2. 아래를 그대로 붙여넣으세요

         cd "$DIR"
         git init -b main && git add -A && git commit -m "deck"
         git remote add origin https://github.com/<내계정>/$SAFE.git
         git push -u origin main

      3. 저장소 Settings → Pages → Source 를 'main / (root)' 로 저장

지금은 이 주소로 직접 열어 볼 수 있습니다:
  cd "$DIR" && python3 -m http.server 8080
EOF
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "✗ 깃허브 로그인이 안 돼 있습니다. 아래를 실행한 뒤 다시 시도하세요."
  echo "    gh auth login"
  exit 1
fi

USER=$(gh api user --jq .login)

cd "$DIR"
[ -d .git ] || git init -b main -q
git add -A
git commit -q -m "deck: $(date +%Y-%m-%d)" || echo "· 바뀐 내용이 없어 커밋은 건너뜁니다"

if gh repo view "$USER/$SAFE" >/dev/null 2>&1; then
  echo "· 저장소가 이미 있습니다. 덮어씁니다"
  git remote remove origin 2>/dev/null || true
  git remote add origin "https://github.com/$USER/$SAFE.git"
  git push -q -u origin main --force
else
  echo "· 저장소를 새로 만듭니다"
  gh repo create "$SAFE" --public --source=. --push
fi

# ── Pages 켜기 (이미 켜져 있으면 조용히 넘어감)
gh api -X POST "repos/$USER/$SAFE/pages" \
  -f "source[branch]=main" -f "source[path]=/" >/dev/null 2>&1 || true

URL="https://$USER.github.io/$SAFE/"
echo
echo "✓ 올렸습니다"
echo "  $URL"
echo
echo "※ 처음 올리면 화면에 뜨기까지 1~2분 걸립니다. 바로 안 보여도 정상입니다."
echo "※ 발표 중 단축키 — S 발표자 노트 · T 구간 타이머 · Shift+R 타이머 리셋"
