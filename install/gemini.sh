#!/bin/sh
# Gemini CLI: rtk hook, the caveman, ponytail and team extensions, both modes at ultra.
set -u
rtk init --gemini --global --auto-patch
for repo in JuliusBrussee/caveman DietrichGebert/ponytail oliverassad/oa-claude; do
  gemini extensions install "https://github.com/$repo" --consent --auto-update
done
mkdir -p "$HOME/.gemini"
grep -q CAVEMAN_DEFAULT_MODE "$HOME/.gemini/.env" 2>/dev/null \
  || printf 'CAVEMAN_DEFAULT_MODE=ultra\nPONYTAIL_DEFAULT_MODE=ultra\n' >> "$HOME/.gemini/.env"
echo "[team] gemini ready"
