#!/usr/bin/env bash
# Idempotent cloud environment setup for Antigravity / agent containers.
# Installs rtk and links skills from oa-claude, caveman, and ponytail into ~/.agents/skills.
set -euo pipefail

# Ensure non-interactive bash shells (including BASH_ENV) load ~/.local/bin
sed -i '/case \$- in/,/esac/d' "$HOME/.bashrc" 2>/dev/null || true
grep -qxF 'export PATH="$HOME/.local/bin:$PATH"' "$HOME/.bashrc" || \
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
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

# Locate oa-claude skills (current checkout, mounted workspace, or fallback clone)
SCRIPT_DIR=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

if [ -n "$SCRIPT_DIR" ] && [ -d "$SCRIPT_DIR/skills" ]; then
  OA_CLAUDE_DIR="$SCRIPT_DIR"
elif [ -d "$HOME/oliverassad/oa-claude/skills" ]; then
  OA_CLAUDE_DIR="$HOME/oliverassad/oa-claude"
else
  if [ ! -d "$PLUGINS_DIR/oa-claude/.git" ]; then
    git clone --depth 1 https://github.com/oliverassad/oa-claude.git "$PLUGINS_DIR/oa-claude"
  fi
  OA_CLAUDE_DIR="$PLUGINS_DIR/oa-claude"
fi

# 3. Link skills into ~/.agents/skills
for d in "$OA_CLAUDE_DIR"/skills/*/; do
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
