#!/bin/sh
# SessionStart hook: verify the safety net actually exists, instead of assuming it does.
# Silent when everything is fine — costs zero tokens on a healthy project.
# ponytail: git only. Add other prerequisites (env file, deploy target) when one actually burns you.
d="${CLAUDE_PROJECT_DIR:-$PWD}"
[ -f "$d/.claude/SPEC-LOCK.md" ] || exit 0
cd "$d" 2>/dev/null || exit 0

w=""
add() { w="$w- $1
"; }

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  n=$(find . -type f -not -path './.claude/*' 2>/dev/null | head -20 | wc -l | tr -d ' ')
  add "**git 저장소가 아니다.** 파일 ${n}개+ 가 버전 관리·백업 없이 있다. 실수로 지우면 복구 수단이 없음. \`git init\` 할지 물어라."
else
  if ! git rev-parse HEAD >/dev/null 2>&1; then
    add "**커밋이 하나도 없다.** git init만 되어 있고 저장된 스냅샷이 없다."
  else
    c=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    [ "$c" -gt 20 ] && add "커밋 안 된 변경 ${c}개. 마지막 저장 지점이 오래됐다."
  fi
  if [ -z "$(git remote 2>/dev/null)" ]; then
    add "**원격 저장소가 없다.** 이 컴퓨터가 유일한 사본 — 기기 고장 시 전부 소실."
  else
    u=$(git log --branches --not --remotes --oneline 2>/dev/null | wc -l | tr -d ' ')
    [ "$u" -gt 0 ] && add "푸시 안 된 커밋 ${u}개. 원격에 백업되지 않았다."
  fi
fi

[ -n "$w" ] || exit 0
printf '<spec-guard-precondition>\n이 프로젝트의 안전장치 점검 결과 문제가 있다. 사용자가 묻기 전에 첫 답변에서 먼저 알리고, 고칠지 물어라.\n%s</spec-guard-precondition>\n' "$w"
