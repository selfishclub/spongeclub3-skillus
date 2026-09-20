#!/usr/bin/env python3
"""Measure whether this skill actually triggers, and which skill wins when several could.

Why this exists: skill-creator's `scripts/run_loop.py` cannot measure a skill that is
already installed. It fabricates a temporary slash command named `<skill>-skill-<uuid>`
and checks whether the model invoked *that* name — but an installed skill is invoked
under its real name, so every query scores 0 and the negatives "pass" by default.
A run that reports 10/20 in that setup has measured nothing.

Two things this script gets right, both learned the hard way:
  1. Only assistant `tool_use` blocks count. The `init` system event lists every
     installed skill AND the string "Skill" on one line, so any naive substring match
     reports a hit on the very first line of every run.
  2. Inspect the first few tool calls, not just the first. A vague prompt often starts
     with `ls`/`Read` to find the data before invoking the skill — stopping at call #1
     scores a correct run as a miss.

Usage:  python3 trigger-check.py cases.json [skill-name] [max-calls]
cases.json: [{"query": "...", "should_trigger": true}, ...]
"""
import json, os, subprocess, sys

SKILL = sys.argv[2] if len(sys.argv) > 2 else "ko-ja-bilingual"
MAX_CALLS = int(sys.argv[3]) if len(sys.argv) > 3 else 4
CWD = os.path.expanduser("~")


def tool_calls(query):
    env = dict(os.environ)
    env.pop("CLAUDECODE", None)  # allow nesting claude -p inside a session
    env["PATH"] = os.path.expanduser("~/.local/bin") + ":" + env["PATH"]
    p = subprocess.Popen(
        ["claude", "-p", query, "--output-format", "stream-json", "--verbose"],
        cwd=CWD, env=env, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    calls = []
    for line in p.stdout:
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("type") == "assistant":
            for c in d.get("message", {}).get("content", []):
                if c.get("type") == "tool_use":
                    calls.append((c.get("name"), str(c.get("input", {}).get("skill") or "")))
        if d.get("type") == "result" or len(calls) >= MAX_CALLS:
            break
    p.kill(); p.wait()
    return calls


def main():
    cases = json.load(open(sys.argv[1], encoding="utf-8"))
    ok = 0
    for c in cases:
        calls = tool_calls(c["query"])
        fired = any(n == "Skill" and SKILL in s for n, s in calls)
        won = next((s for n, s in calls if n == "Skill"), "-")
        good = fired == c["should_trigger"]
        ok += good
        print("%s expect=%-5s fired=%-5s won=%-24s %s"
              % ("OK " if good else "MISS", c["should_trigger"], fired, won[:24], c["query"][:44]))
    print("\n%d/%d" % (ok, len(cases)))


if __name__ == "__main__":
    main()
