#!/bin/sh
# PreToolUse on Bash: hand the command to rtk for its token-saving rewrite.
# Skips when rtk is missing, or when user or project settings already run `rtk hook claude`
# (two rewrites of one command would double the hook).
command -v rtk >/dev/null 2>&1 || exit 0
for f in "$HOME/.claude/settings.json" "${CLAUDE_PROJECT_DIR:-.}/.claude/settings.json"; do
  grep -q 'rtk hook claude' "$f" 2>/dev/null && exit 0
done
exec rtk hook claude
