#!/usr/bin/env bash
# 덱 한 번에 만들기 — 생성 + 확장 주입 + 검증까지.
#
#   bash build-deck.sh <brief.json> <출력폴더> <테마> [notes.json]
#   테마: minimal-bw | bold-color | soft | editorial | dark-tech
#
# 수동으로 하면 share-extend 복사나 data-sd-theme 주입을 빠뜨리기 쉽다.
# 그러면 발표자 노트(S)·타이머(T)·테마 폰트가 통째로 안 붙은 덱이 나간다.
set -euo pipefail
ENG="$(cd "$(dirname "$0")" && pwd)"
BRIEF="${1:?brief.json 경로가 필요합니다}"
OUT="${2:?출력폴더가 필요합니다}"
THEME="${3:?테마가 필요합니다 — minimal-bw|bold-color|soft|editorial|dark-tech}"
NOTES="${4:-}"

case "$THEME" in
  minimal-bw|bold-color|soft|editorial|dark-tech) ;;
  *) echo "✗ 알 수 없는 테마: $THEME"; exit 1 ;;
esac

python3 "$ENG/generate_deck.py" "$BRIEF" "$OUT" >/dev/null
cp "$ENG/share-extend.css" "$ENG/share-extend.js" "$OUT/"
# 이미 출력 폴더 안의 파일을 가리키면 복사하지 않는다 (cp 가 자기 자신을 복사하려다 죽는다)
if [ -n "$NOTES" ] && [ "$(cd "$(dirname "$NOTES")" && pwd)/$(basename "$NOTES")" != "$(cd "$OUT" && pwd)/notes.json" ]; then
  cp "$NOTES" "$OUT/notes.json"
fi

python3 - "$OUT" "$THEME" <<'PY'
import pathlib, sys
out, theme = sys.argv[1], sys.argv[2]
p = pathlib.Path(out, 'index.html'); h = p.read_text()
if 'data-sd-theme' not in h:
    h = h.replace('<body', '<body data-sd-theme="%s"' % theme, 1)
if 'share-extend.css' not in h:
    h = h.replace('</body>',
        '<link rel="stylesheet" href="share-extend.css">\n'
        '<script src="share-extend.js"></script>\n</body>', 1)
p.write_text(h)
PY

# ── 검증: 빠뜨린 게 있으면 여기서 잡는다
fail=0
grep -q "data-sd-theme=\"$THEME\"" "$OUT/index.html" || { echo "✗ 테마 속성 주입 실패"; fail=1; }
grep -q 'share-extend.css' "$OUT/index.html" || { echo "✗ CSS 주입 실패"; fail=1; }
grep -q 'share-extend.js'  "$OUT/index.html" || { echo "✗ JS 주입 실패"; fail=1; }
[ -f "$OUT/share-extend.css" ] || { echo "✗ CSS 파일 없음"; fail=1; }
[ -f "$OUT/notes.json" ] || echo "⚠ notes.json 없음 — 발표자 노트가 비어 있습니다"

# brief 의 슬라이드 수와 필수 필드 확인
python3 - "$BRIEF" <<'PY' || fail=1
import json,sys
s=json.load(open(sys.argv[1]))['slides']
bad=[i+1 for i,x in enumerate(s) if x.get('type') in ('core','ending') and 'lines' not in x]
print("슬라이드 %d장" % len(s))
if bad:
    print("✗ lines 누락 — 이 슬라이드가 덱 전체를 죽입니다:", bad); raise SystemExit(1)
if not (25 <= len(s) <= 35):
    print("⚠ 1시간 권장은 25~35장입니다")
PY

[ "$fail" -eq 0 ] && echo "✓ 완료: $OUT/index.html" || { echo "FAIL"; exit 1; }
echo
echo "확인:  cd $OUT && python3 -m http.server 8080"
echo "발표 중:  S 노트 · T 타이머 · Shift+R 리셋"
