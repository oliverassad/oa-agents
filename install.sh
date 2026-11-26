#!/bin/sh
# Bootstrap rtk and the team plugin (Claude Code) or extension (Gemini CLI).
#   curl -fsSL https://raw.githubusercontent.com/oliverassad/oa-claude/main/install.sh | sh
# caveman and ponytail are installed separately (their own one-liners).
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
ln -sf "$HOME/.local/bin/rtk" /usr/local/bin/rtk 2>/dev/null  # on PATH for later shells, where allowed

if command -v claude >/dev/null 2>&1; then
  rtk init --global --auto-patch
  claude plugin marketplace add oliverassad/oa-claude
  claude plugin install team@oa-claude
fi

if command -v gemini >/dev/null 2>&1; then
  rtk init --gemini --global --auto-patch
  gemini extensions install https://github.com/oliverassad/oa-claude --consent --auto-update
fi
