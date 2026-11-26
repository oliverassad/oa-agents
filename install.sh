#!/bin/sh
# Bootstrap rtk and the team plugin (Claude Code) or extension (Gemini CLI).
#   curl -fsSL https://raw.githubusercontent.com/oliverassad/oa-agents/main/install.sh | sh
# caveman and ponytail are installed separately (their own one-liners).
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
ln -sf "$HOME/.local/bin/rtk" /usr/local/bin/rtk 2>/dev/null  # on PATH for later shells, where allowed

if command -v claude >/dev/null 2>&1; then
  rtk init --global --auto-patch
  claude plugin marketplace add oliverassad/oa-agents
  claude plugin install team@oa-agents
  # A second run updates.
  claude plugin marketplace update oa-agents
  claude plugin update team@oa-agents
fi

if command -v gemini >/dev/null 2>&1; then
  rtk init --gemini --global --auto-patch
  gemini extensions install https://github.com/oliverassad/oa-agents --consent --auto-update
  # Agent models and thinking levels from MODELS.md; project AGENTS.md as a context file.
  python3 - "$HOME/.gemini/extensions/team/MODELS.md" <<'PY'
import json, pathlib, sys
rows = [[c.strip() for c in l.split("|")[1:-1]] for l in open(sys.argv[1]) if l.startswith("| ") and "---" not in l]
rows = [r for r in rows if len(r) == 7 and r[0] != "Agent"]
path = pathlib.Path.home() / ".gemini" / "settings.json"
settings = json.loads(path.read_text() or "{}") if path.exists() else {}
settings.setdefault("context", {}).setdefault("fileName", ["AGENTS.md", "GEMINI.md"])
overrides = settings.setdefault("agents", {}).setdefault("overrides", {})
configs = settings.setdefault("modelConfigs", {}).setdefault("overrides", [])
configs[:] = [c for c in configs if c.get("match", {}).get("overrideScope") not in {r[0] for r in rows}]
for agent, _, _, _, model, thinking, _ in rows:
    overrides.setdefault(agent, {})["modelConfig"] = {"model": model}
    configs.append({"match": {"overrideScope": agent},
                    "modelConfig": {"generateContentConfig": {"thinkingConfig": {"thinkingLevel": thinking}}}})
path.write_text(json.dumps(settings, indent=2) + "\n")
PY
fi
