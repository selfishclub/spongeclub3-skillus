#!/bin/sh
# UserPromptSubmit hook. Cheap by design, and entirely local — no network, no API keys.
# Always-on rules live in .claude/rules/spec-guard.md, loaded ONCE per session and cached.
# Scoring rules and the score history ride along only on turns that are actually about scoring.
s="$(dirname "$0")"
d="${CLAUDE_PROJECT_DIR:-$PWD}/.claude"
[ -f "$d/SPEC-LOCK.md" ] || exit 0

printf 'spec-guard on. SPEC-LOCK is binding: no silent assumptions, flag 외부결제/되돌리기/노출 risks before being asked.\n'

p=$(sed -n 's/.*"user_input"[[:space:]]*:[[:space:]]*"\(.*\)/\1/p' | head -c 2000)
case "$p" in
  *점*|*평가*|*완료*|*끝*|*됐*|*배포*|*마무리*|*체크*|*검수*|*score*|*done*|*ship*)
    printf '<spec-guard-scoring>\n'
    cat "$s/RULES-scoring.md"
    if [ -f "$d/SCORE-LOG.md" ]; then
      printf '\n직전 회차 — 점수가 다르면 어느 항목이 왜 뒤집혔는지 밝힐 것.\n<last-score>\n'
      tail -25 "$d/SCORE-LOG.md"
      printf '\n</last-score>\n'
    fi
    printf '</spec-guard-scoring>\n'
    ;;
esac
