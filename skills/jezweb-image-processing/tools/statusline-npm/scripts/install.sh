#!/bin/bash

# Claude Code Status Line - Installation Script
# Installs cross-platform Node.js statusline (works on macOS, Linux, Windows)

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
STATUSLINE_SCRIPT="$SCRIPT_DIR/statusline.js"
INSTALL_PATH="$HOME/.claude/statusline.js"
SETTINGS_FILE="$HOME/.claude/settings.json"
BACKUP_SUFFIX=".backup-$(date +%Y%m%d-%H%M%S)"

echo "Installing Claude Code Custom Status Line..."
echo ""

# Check dependencies
echo "Checking dependencies..."
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is required but not installed."
    echo "   Claude Code requires Node.js, so this should already be available."
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "Warning: git not found. Git info will not be available."
fi

echo "Dependencies OK (Node.js + git)"
echo ""

# Backup existing statusline script if it exists
for old in "$HOME/.claude/statusline.js" "$HOME/.claude/statusline.sh"; do
    if [[ -f "$old" ]]; then
        echo "Backing up existing status line: $old"
        cp "$old" "${old}${BACKUP_SUFFIX}"
        echo "   Backup saved: ${old}${BACKUP_SUFFIX}"
    fi
done

# Copy statusline script
echo "Installing status line script..."
mkdir -p "$HOME/.claude"
cp "$STATUSLINE_SCRIPT" "$INSTALL_PATH"
chmod +x "$INSTALL_PATH"
echo "   Installed: $INSTALL_PATH"

# Copy context awareness hook
HOOK_SCRIPT="$SCRIPT_DIR/context-hook.sh"
HOOK_INSTALL_PATH="$HOME/.claude/context-hook.sh"
if [[ -f "$HOOK_SCRIPT" ]]; then
    cp "$HOOK_SCRIPT" "$HOOK_INSTALL_PATH"
    chmod +x "$HOOK_INSTALL_PATH"
    echo "   Installed: $HOOK_INSTALL_PATH"
fi
echo ""

# Update settings.json
if [[ -f "$SETTINGS_FILE" ]]; then
    echo "Updating settings.json..."

    # Backup settings
    cp "$SETTINGS_FILE" "${SETTINGS_FILE}${BACKUP_SUFFIX}"
    echo "   Backup saved: ${SETTINGS_FILE}${BACKUP_SUFFIX}"

    # Check for jq (needed to update settings)
    if command -v jq &> /dev/null; then
        jq '.statusLine = {
            "type": "command",
            "command": "node ~/.claude/statusline.js",
            "padding": 0
        }' "$SETTINGS_FILE" > "${SETTINGS_FILE}.tmp" && mv "${SETTINGS_FILE}.tmp" "$SETTINGS_FILE"
        echo "   Settings updated"
    else
        echo "   jq not found — please manually update statusLine.command in settings.json to:"
        echo "   \"node ~/.claude/statusline.js\""
    fi
else
    echo "Creating settings.json..."
    cat > "$SETTINGS_FILE" <<'EOF'
{
  "statusLine": {
    "type": "command",
    "command": "node ~/.claude/statusline.js",
    "padding": 0
  }
}
EOF
    echo "   Settings created: $SETTINGS_FILE"
fi

echo ""
echo "Installation complete!"
echo ""
echo "Your 3-line status bar shows:"
echo "   Line 1: Model, repo:branch, git status, agent name, worktree"
echo "   Line 2: Latest commit + lines changed"
echo "   Line 3: Context bricks, percentage, free tokens, duration, cost"
echo ""
echo "Context awareness hook installed at ~/.claude/context-hook.sh"
echo "To enable it, add to your ~/.claude/settings.json:"
echo '   "hooks": { "UserPromptSubmit": [{ "matcher": "", "hooks": ['
echo '     { "type": "command", "command": "bash ~/.claude/context-hook.sh" }'
echo '   ]}]}'
echo ""
echo "Restart Claude Code to see your new status line!"
