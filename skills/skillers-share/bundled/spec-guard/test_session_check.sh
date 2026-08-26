#!/bin/sh
# Run: sh ~/.claude/skills/spec-guard/test_session_check.sh
set -e
h="$(cd "$(dirname "$0")" && pwd)/session-check.sh"
mk() { d=$(mktemp -d); mkdir -p "$d/.claude"; echo "합격 기준: x" > "$d/.claude/SPEC-LOCK.md"; echo "$d"; }
run() { CLAUDE_PROJECT_DIR="$1" sh "$h"; }

# 1. no SPEC-LOCK -> silent (never nags an unrelated project)
d=$(mktemp -d); out=$(run "$d"); [ -z "$out" ] || { echo "FAIL: fired without SPEC-LOCK"; exit 1; }; rm -rf "$d"

# 2. the PAZX case: real work, no git at all -> must warn
d=$(mk); echo "code" > "$d/app.js"
out=$(run "$d")
case "$out" in *"git 저장소가 아니다"*) ;; *) echo "FAIL: missing no-git warning"; exit 1;; esac
rm -rf "$d"

# 3. git repo, committed, has remote -> silent (the healthy case must cost 0 tokens)
d=$(mk); cd "$d"; git init -q -b main; echo x > a.txt; git add -A
git -c user.name=t -c user.email=t@t commit -qm init
git remote add origin https://example.com/x.git
git update-ref refs/remotes/origin/main HEAD
cd /; out=$(run "$d")
[ -z "$out" ] || { echo "FAIL: healthy repo should be silent, got: $out"; exit 1; }
rm -rf "$d"

# 4. git repo with no remote -> warn about single copy
d=$(mk); cd "$d"; git init -q -b main; echo x > a.txt; git add -A
git -c user.name=t -c user.email=t@t commit -qm init
cd /; out=$(run "$d")
case "$out" in *"원격 저장소가 없다"*) ;; *) echo "FAIL: missing no-remote warning"; exit 1;; esac
rm -rf "$d"

echo "OK: all 4 cases pass"
