#!/bin/sh
# Run: sh ~/.claude/skills/spec-guard/test_inject.sh
set -e
h="$(dirname "$0")/inject.sh"
d=$(mktemp -d)
run() { printf '{"hook_event_name":"UserPromptSubmit","user_input":"%s"}' "$1" | CLAUDE_PROJECT_DIR="$d" sh "$h"; }

# 1. no SPEC-LOCK -> silent, exit 0 (must never touch an unrelated project)
out=$(run "안녕") || { echo "FAIL: nonzero exit without SPEC-LOCK"; exit 1; }
[ -z "$out" ] || { echo "FAIL: expected empty output, got: $out"; exit 1; }

mkdir -p "$d/.claude"
echo "합격 기준: 모바일 375px 안 깨짐" > "$d/.claude/SPEC-LOCK.md"
echo "## 2026-07-28 — 3/5" > "$d/.claude/SCORE-LOG.md"

# 2. ordinary turn -> short reminder only, no score log (this is the cost guarantee)
out=$(run "이 파일 읽어줘")
case "$out" in *"spec-guard on"*) ;; *) echo "FAIL: reminder missing"; exit 1;; esac
case "$out" in *"3/5"*) echo "FAIL: score log injected on an ordinary turn"; exit 1;; esac
case "$out" in *"근거 없는 점수"*) echo "FAIL: scoring rules injected on an ordinary turn"; exit 1;; esac
[ "${#out}" -lt 200 ] || { echo "FAIL: ordinary turn too big (${#out}B)"; exit 1; }

# 3. scoring turn -> previous score carried in, so a new score can't silently contradict it
out=$(run "이거 몇 점이야")
case "$out" in *"근거 없는 점수"*) ;; *) echo "FAIL: scoring rules missing on scoring turn"; exit 1;; esac
case "$out" in *"3/5"*"</last-score>"*) ;; *) echo "FAIL: score log not injected on scoring turn"; exit 1;; esac

# 4. scoring turn with no log yet -> reminder still fires, no empty block
rm "$d/.claude/SCORE-LOG.md"
out=$(run "다 됐어?")
case "$out" in *"spec-guard on"*) ;; *) echo "FAIL: reminder missing"; exit 1;; esac
case "$out" in *"<last-score>"*) echo "FAIL: empty last-score block"; exit 1;; esac
case "$out" in *"근거 없는 점수"*) ;; *) echo "FAIL: scoring rules should still load"; exit 1;; esac

rm -rf "$d"
echo "OK: all 4 cases pass"
