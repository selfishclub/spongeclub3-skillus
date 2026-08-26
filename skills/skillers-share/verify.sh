#!/usr/bin/env bash
# 공유회-OS 번들 구조 검증. 실패하면 무엇이 왜 틀렸는지 출력하고 exit 1.
set -uo pipefail
cd "$(dirname "$0")"
fail=0

err() { echo "  ✗ $1"; fail=1; }
ok()  { echo "  ✓ $1"; }

echo "[1] 필수 파일"
for f in SKILL.md install.sh README.md \
         references/types.md references/titles.md references/interview.md \
         references/timeline.md references/script.md references/themes.md \
         engine/share-extend.css engine/share-extend.js \
         engine/build-deck.sh engine/deploy.sh; do
  [ -f "$f" ] && ok "$f" || err "$f 없음"
done

echo "[2] SKILL.md 프론트매터"
if [ -f SKILL.md ]; then
  head -1 SKILL.md | grep -q '^---$' || err "SKILL.md 1행이 --- 가 아님"
  grep -q '^name: 공유회-OS$' SKILL.md || err "SKILL.md에 'name: 공유회-OS' 없음"
  grep -q '^description: ' SKILL.md || err "SKILL.md에 description 없음"
fi

echo "[3] 플레이스홀더"
# docs/ 는 규칙 자체를 설명하는 문서라 제외한다 (금지어를 인용한다)
if grep -rnE '(TBD|TODO|추후 (작성|보완)|채워야)' --include='*.md' \
     --exclude-dir=docs --exclude-dir=design-concepts --exclude-dir=bundled . ; then
  err "플레이스홀더 발견"
else
  ok "플레이스홀더 없음"
fi

echo "[4] 동봉 스킬"
for d in 훅카피 크리틱디렉터 spec-guard; do
  [ -f "bundled/$d/SKILL.md" ] && ok "bundled/$d" || err "bundled/$d/SKILL.md 없음"
done
for d in webdeck proposal-lite; do
  [ -d "$d" ] && err "$d 는 동봉하지 않는다 (엔진은 install.sh 가 받는다)" || ok "$d 미동봉"
done

echo "[5] webdeck 원본 무수정"
if [ -f engine/generate_deck.py ]; then
  curl -fsSL https://raw.githubusercontent.com/Koo-bon/webdeck/main/webdeck/generate_deck.py \
    -o /tmp/gd_upstream.py 2>/dev/null
  if [ -s /tmp/gd_upstream.py ]; then
    diff -q /tmp/gd_upstream.py engine/generate_deck.py >/dev/null \
      && ok "generate_deck.py 원본과 동일" \
      || err "generate_deck.py 가 원본과 다름 — 확장은 share-extend.* 에만"
  else
    ok "generate_deck.py (원본 대조 건너뜀 — 네트워크 없음)"
  fi
fi

echo "[6] 모든 질문에 탈출구"
if [ -f references/interview.md ]; then
  q=$(grep -c '^### Q' references/interview.md)
  e=$(grep -cE '모르겠어요|알아서' references/interview.md)
  [ "$e" -ge "$q" ] && ok "질문 $q개 / 탈출구 $e개" \
    || err "질문 $q개인데 탈출구가 $e개뿐"
fi

echo
[ "$fail" -eq 0 ] && echo "PASS" || echo "FAIL"
exit $fail
