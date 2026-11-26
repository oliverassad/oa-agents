#!/usr/bin/env bash
# Antigravity / Gemini cloud environment setup ONLY.
# Do NOT use automatically for Claude Code or other agents — Claude Code uses
# install.sh and native marketplace plugins (hooks, subagents, MCP) instead.
# Installs rtk and links skills from oa-agents, caveman, and ponytail into ~/.agents/skills.
set -euo pipefail

# Non-interactive bash shells (including BASH_ENV) load ~/.local/bin: the line goes
# first, above the interactive guard, so no part of ~/.bashrc is deleted.
LINE='export PATH="$HOME/.local/bin:$PATH"'
if ! grep -qxF "$LINE" "$HOME/.bashrc" 2>/dev/null; then
  { echo "$LINE"; cat "$HOME/.bashrc" 2>/dev/null || true; } > "$HOME/.bashrc.new" && mv "$HOME/.bashrc.new" "$HOME/.bashrc"
fi
export PATH="$HOME/.local/bin:$PATH"

# 1. Install rtk if missing
if ! command -v rtk >/dev/null 2>&1; then
  curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh
fi

# 2. Clone plugin skill repos
PLUGINS_DIR="$HOME/.local/share/plugins"
SKILLS_DIR="$HOME/.agents/skills"
mkdir -p "$PLUGINS_DIR" "$SKILLS_DIR"

if [ ! -d "$PLUGINS_DIR/caveman/.git" ]; then
  git clone --depth 1 https://github.com/JuliusBrussee/caveman.git "$PLUGINS_DIR/caveman"
fi
if [ ! -d "$PLUGINS_DIR/ponytail/.git" ]; then
  git clone --depth 1 https://github.com/DietrichGebert/ponytail.git "$PLUGINS_DIR/ponytail"
fi

# Locate oa-agents skills (current checkout, mounted workspace, or fallback clone)
SCRIPT_DIR=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

if [ -n "$SCRIPT_DIR" ] && [ -d "$SCRIPT_DIR/skills" ]; then
  OA_AGENTS_DIR="$SCRIPT_DIR"
elif [ -d "$HOME/oliverassad/oa-agents/skills" ]; then
  OA_AGENTS_DIR="$HOME/oliverassad/oa-agents"
else
  if [ ! -d "$PLUGINS_DIR/oa-agents/.git" ]; then
    git clone --depth 1 https://github.com/oliverassad/oa-agents.git "$PLUGINS_DIR/oa-agents"
  fi
  OA_AGENTS_DIR="$PLUGINS_DIR/oa-agents"
fi

# 3. Link skills into ~/.agents/skills
for d in "$OA_AGENTS_DIR"/skills/*/; do
  [ -d "$d" ] || continue
  ln -sfn "${d%/}" "$SKILLS_DIR/$(basename "$d")"
done

for repo in caveman ponytail; do
  for f in "$PLUGINS_DIR/$repo"/skills/*/SKILL.md; do
    [ -f "$f" ] || continue
    d=$(dirname "$f")
    ln -sfn "$d" "$SKILLS_DIR/$(basename "$d")"
  done
done
