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
  # Agent models: the Gemini column of MODELS.md into agents.overrides.
  python3 - "$HOME/.gemini/extensions/team/MODELS.md" <<'PY'
import json, pathlib, sys
rows = [l.split("|")[1:-1] for l in open(sys.argv[1]) if l.startswith("| ") and "---" not in l][1:]
path = pathlib.Path.home() / ".gemini" / "settings.json"
settings = json.loads(path.read_text() or "{}") if path.exists() else {}
overrides = settings.setdefault("agents", {}).setdefault("overrides", {})
for agent, _, _, gemini in (map(str.strip, r) for r in rows):
    overrides.setdefault(agent, {})["modelConfig"] = {"model": gemini}
path.write_text(json.dumps(settings, indent=2) + "\n")
PY
fi
