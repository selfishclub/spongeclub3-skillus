#!/bin/bash

# Claude Code Custom Status Line — Context Bricks
# v4.0.0 - 3-line layout with agent name, worktree, output style, extended context warning
#
# Line 1: [Model:style] repo:branch status | @agent | wt
# Line 2: [commit] message | +lines/-lines
# Line 3: [■■■■□□□□] 73%! | 52k free | 2h15m | $12.50
#
# Uses percentage fields (Claude Code 2.1.6+) with fallback to current_usage calculation.

# Read JSON from stdin
input=$(cat)

# Parse Claude data
model=$(echo "$input" | jq -r '.model.display_name // "Claude"' | sed 's/Claude //')
current_dir=$(echo "$input" | jq -r '.workspace.current_dir // env.PWD')
lines_added=$(echo "$input" | jq -r '.cost.total_lines_added // 0')
lines_removed=$(echo "$input" | jq -r '.cost.total_lines_removed // 0')
agent_name=$(echo "$input" | jq -r '.agent.name // empty')
output_style=$(echo "$input" | jq -r '.output_style.name // empty')
exceeds_200k=$(echo "$input" | jq -r '.context_window.exceeds_200k_tokens // false')

# Abbreviate output style
style_abbrev=""
if [[ -n "$output_style" && "$output_style" != "default" ]]; then
    case "$output_style" in
        explanatory) style_abbrev="expl" ;;
        concise)     style_abbrev="conc" ;;
        verbose)     style_abbrev="verb" ;;
        *)           style_abbrev="${output_style:0:4}" ;;
    esac
fi

# Get git information
cd "$current_dir" 2>/dev/null || cd "$HOME"

if git rev-parse --git-dir > /dev/null 2>&1; then
    repo_name=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" || echo "")
    branch=$(git branch --show-current 2>/dev/null || echo "detached")
    commit_short=$(git rev-parse --short HEAD 2>/dev/null || echo "")
    commit_msg=$(git log -1 --pretty=%s 2>/dev/null | cut -c1-50 || echo "")

    # Worktree detection
    git_dir=$(git rev-parse --git-dir 2>/dev/null)
    in_worktree=false
    if echo "$git_dir" | grep -q '/worktrees/'; then
        in_worktree=true
    fi

    # Git status indicators
    git_status=""
    if [[ -n $(git status --porcelain 2>/dev/null) ]]; then
        git_status="*"
    fi

    # Check ahead/behind remote
    upstream=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null)
    if [[ -n "$upstream" ]]; then
        ahead=$(git rev-list --count "$upstream"..HEAD 2>/dev/null || echo "0")
        behind=$(git rev-list --count HEAD.."$upstream" 2>/dev/null || echo "0")
        [[ "$ahead" -gt 0 ]] && git_status="${git_status}↑${ahead}"
        [[ "$behind" -gt 0 ]] && git_status="${git_status}↓${behind}"
    fi
else
    repo_name=""
    branch=""
    commit_short=""
    commit_msg=""
    git_status=""
    in_worktree=false
fi

# ── Line 1: Session identity ──────────────────────────────────
line1=""

# Model in brackets, with optional style suffix
if [[ -n "$style_abbrev" ]]; then
    line1+="\033[1;36m[$model:$style_abbrev]\033[0m"
else
    line1+="\033[1;36m[$model]\033[0m"
fi

# Repo:Branch
if [[ -n "$repo_name" ]]; then
    line1+=" \033[1;32m$repo_name\033[0m"
    if [[ -n "$branch" ]]; then
        line1+=":\033[1;34m$branch\033[0m"
    fi
fi

# Git status indicators
if [[ -n "$git_status" ]]; then
    line1+=" \033[1;31m$git_status\033[0m"
fi

# Agent name
if [[ -n "$agent_name" ]]; then
    line1+=" | \033[1;35m@$agent_name\033[0m"
fi

# Worktree indicator
if [[ "$in_worktree" == "true" ]]; then
    line1+=" | \033[1;33mwt\033[0m"
fi

# ── Line 2: Git state ─────────────────────────────────────────
line2=""

# Commit info
if [[ -n "$commit_short" ]]; then
    line2+="\033[2;37m[\033[0m\033[1;33m$commit_short\033[0m\033[2;37m]\033[0m"
    if [[ -n "$commit_msg" ]]; then
        line2+=" $commit_msg"
    fi
fi

# Lines changed
if [[ "$lines_added" -gt 0 || "$lines_removed" -gt 0 ]]; then
    if [[ -n "$line2" ]]; then
        line2+=" | "
    fi
    line2+="\033[0;32m+$lines_added\033[0m/\033[0;31m-$lines_removed\033[0m"
fi

# ── Line 3: Context bricks + metrics ──────────────────────────
# Get session duration
duration_ms=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')
duration_hours=$((duration_ms / 3600000))
duration_min=$(((duration_ms % 3600000) / 60000))

# Get session cost
cost_usd=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')

# Get context window data
total_tokens=$(echo "$input" | jq -r '.context_window.context_window_size // 200000')

# Prefer v2.1.6+ percentage fields, fallback to calculation
used_pct_raw=$(echo "$input" | jq -r '.context_window.used_percentage // null')
remaining_pct_raw=$(echo "$input" | jq -r '.context_window.remaining_percentage // null')

if [[ "$used_pct_raw" != "null" && -n "$used_pct_raw" ]]; then
    usage_pct=${used_pct_raw%.*}
    remaining_pct=${remaining_pct_raw%.*}
    used_tokens=$(( (total_tokens * usage_pct) / 100 ))
    free_tokens=$(( (total_tokens * remaining_pct) / 100 ))
else
    current_usage=$(echo "$input" | jq -r '.context_window.current_usage // null')
    if [[ "$current_usage" != "null" ]]; then
        input_tokens=$(echo "$current_usage" | jq -r '.input_tokens // 0')
        cache_creation=$(echo "$current_usage" | jq -r '.cache_creation_input_tokens // 0')
        cache_read=$(echo "$current_usage" | jq -r '.cache_read_input_tokens // 0')
        used_tokens=$((input_tokens + cache_creation + cache_read))
    else
        used_tokens=0
    fi
    free_tokens=$((total_tokens - used_tokens))
    if [[ $total_tokens -gt 0 ]]; then
        usage_pct=$(( (used_tokens * 100) / total_tokens ))
    else
        usage_pct=0
    fi
fi

# Token display in 'k' format
free_k=$(( free_tokens / 1000 ))

# Generate brick visualization (40 bricks)
total_bricks=40
if [[ $total_tokens -gt 0 ]]; then
    used_bricks=$(( (used_tokens * total_bricks) / total_tokens ))
else
    used_bricks=0
fi
free_bricks=$((total_bricks - used_bricks))

# Build brick bar
line3="["
for ((i=0; i<used_bricks; i++)); do
    line3+="\033[0;36m■\033[0m"
done
for ((i=0; i<free_bricks; i++)); do
    line3+="\033[2;37m□\033[0m"
done
line3+="]"

# Percentage — yellow with ! when exceeding 200k
if [[ "$exceeds_200k" == "true" ]]; then
    line3+=" \033[1;33m${usage_pct}%!\033[0m"
else
    line3+=" \033[1m${usage_pct}%\033[0m"
fi

# Free space
line3+=" | \033[1;32m${free_k}k free\033[0m"

# Duration
line3+=" | ${duration_hours}h ${duration_min}m"

# Cost (only if non-zero)
if command -v bc &> /dev/null; then
    if (( $(echo "$cost_usd > 0" | bc -l 2>/dev/null || echo "0") )); then
        cost_formatted=$(printf "%.2f" "$cost_usd" 2>/dev/null || echo "0.00")
        line3+=" | \033[0;33m\$${cost_formatted}\033[0m"
    fi
else
    if [[ "$cost_usd" != "0" && "$cost_usd" != "0.0" && "$cost_usd" != "0.00" && -n "$cost_usd" ]]; then
        line3+=" | \033[0;33m\$${cost_usd}\033[0m"
    fi
fi

# Output all three lines
echo -e "$line1"
echo -e "$line2"
echo -e "$line3"
