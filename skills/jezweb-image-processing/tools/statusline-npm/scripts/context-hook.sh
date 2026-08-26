#!/bin/bash
# Context awareness hook for Claude Code
# Reads context level from statusline's persisted file and injects a note
# when crossing 100k thresholds.
#
# Install as a UserPromptSubmit hook in settings.json:
#   "hooks": { "UserPromptSubmit": [{ "matcher": "", "hooks": [
#     { "type": "command", "command": "bash ~/.claude/context-hook.sh" }
#   ]}]}

CONTEXT_FILE="$HOME/.claude/context-level.json"
LAST_THRESHOLD_FILE="$HOME/.claude/context-last-threshold"

# Read stdin (required by hook protocol)
cat > /dev/null

# Check if context file exists and is recent (< 60 seconds old)
if [[ ! -f "$CONTEXT_FILE" ]]; then
  exit 0
fi

# Parse the JSON
FREE_100K=$(python3 -c "import json; print(json.load(open('$CONTEXT_FILE'))['free100k'])" 2>/dev/null)
USAGE_PCT=$(python3 -c "import json; print(json.load(open('$CONTEXT_FILE'))['usagePct'])" 2>/dev/null)
TOTAL_K=$(python3 -c "import json; print(json.load(open('$CONTEXT_FILE'))['totalK'])" 2>/dev/null)

if [[ -z "$FREE_100K" ]]; then
  exit 0
fi

# Read last reported threshold
LAST_THRESHOLD=""
if [[ -f "$LAST_THRESHOLD_FILE" ]]; then
  LAST_THRESHOLD=$(cat "$LAST_THRESHOLD_FILE")
fi

# Only inject when crossing a new 100k boundary (or first time)
if [[ "$FREE_100K" == "$LAST_THRESHOLD" ]]; then
  exit 0
fi

# Save current threshold
echo "$FREE_100K" > "$LAST_THRESHOLD_FILE"

# Build the message based on how much is left
if [[ "$FREE_100K" -ge 700 ]]; then
  echo "<context-status>Context: ~${FREE_100K}k tokens remaining (${USAGE_PCT}% used of ${TOTAL_K}k). Plenty of room — work freely.</context-status>"
elif [[ "$FREE_100K" -ge 400 ]]; then
  echo "<context-status>Context: ~${FREE_100K}k tokens remaining (${USAGE_PCT}% used of ${TOTAL_K}k). Comfortable — continue normally.</context-status>"
elif [[ "$FREE_100K" -ge 200 ]]; then
  echo "<context-status>Context: ~${FREE_100K}k tokens remaining (${USAGE_PCT}% used of ${TOTAL_K}k). Getting fuller — consider delegating heavy reads to sub-agents.</context-status>"
elif [[ "$FREE_100K" -ge 100 ]]; then
  echo "<context-status>Context: ~${FREE_100K}k tokens remaining (${USAGE_PCT}% used of ${TOTAL_K}k). Running low — be surgical with file reads, delegate to sub-agents, checkpoint progress.</context-status>"
else
  echo "<context-status>Context: ~${FREE_100K}k tokens remaining (${USAGE_PCT}% used of ${TOTAL_K}k). Critical — wrap up current task, save learnings, prepare for compaction.</context-status>"
fi

exit 0
