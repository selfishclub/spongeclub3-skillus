#!/usr/bin/env bash
# daily-log 설치 스크립트 (macOS / Linux)
# 사용법: bash install.sh
set -e
echo "== daily-log 스킬 설치 =="

SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills/daily-log"

mkdir -p "$DEST/scripts"
cp "$SRC/SKILL.md" "$DEST/"
cp "$SRC/scripts/build_log.py" "$DEST/scripts/"
[ -f "$SRC/README.md" ] && cp "$SRC/README.md" "$DEST/"
echo "[OK] 스킬 복사 완료 -> $DEST"

# Python 확인
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  PY=""
fi

if [ -z "$PY" ]; then
  echo "[주의] python 을 찾지 못했습니다. python 을 먼저 설치하세요."
else
  echo "[OK] Python 발견: $($PY --version 2>&1)"
  echo "PDF 엔진(reportlab) 설치를 시도합니다..."
  if $PY -m pip install --quiet reportlab; then
    echo "[OK] reportlab 준비 완료 (PDF 사용 가능)"
  else
    echo "[주의] reportlab 설치 실패. MD/HTML은 정상 동작하며 PDF는 나중에 자동 재시도됩니다."
  fi
fi

echo ""
echo "설치 끝! Claude Code 를 새로 켠 뒤 '오늘 로그 정리해줘' 라고 해보세요."
