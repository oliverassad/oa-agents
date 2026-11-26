#!/bin/sh
# Install the shared team for every agent CLI on this machine (Claude Code, Gemini CLI).
#   curl -fsSL https://raw.githubusercontent.com/oliverassad/oa-claude/main/install.sh | sh
# One CLI only:  ... | sh -s -- claude     or     ... | sh -s -- gemini
set -u
RAW="${TEAM_RAW:-https://raw.githubusercontent.com/oliverassad/oa-claude/main/install}"

# rtk, the official way (latest release, checksum-verified by its installer).
command -v rtk >/dev/null 2>&1 || curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh
PATH="$HOME/.local/bin:$PATH"; export PATH

for cli in ${1:-claude gemini}; do
  if command -v "$cli" >/dev/null 2>&1; then curl -fsSL "$RAW/$cli.sh" | sh; else echo "[team] $cli not found, skipped"; fi
done
