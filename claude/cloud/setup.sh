#!/bin/bash
# Setup script for the Claude Code cloud environment "claude-team".
# Paste ALL of it into the environment's setup script on claude.ai (Code > Environments).
#
# It makes every cloud session in this environment start like a local one:
#   1. rtk, latest release, installed and hooked into Claude Code the official way
#   2. plugins caveman, ponytail and team (private oliverassad/oa-claude) at user scope
#   3. caveman and ponytail at level ultra (env in ~/.claude/settings.json)
#
# Why it works this way (cloud checks on branches test/cloud-plugin-check and -2):
#   - The cloud CLI skips plugins that only repo settings enable, and the session runs
#     with SKIP_PLUGIN_MARKETPLACE=true. So the install runs here, with that variable
#     unset, and the marketplaces and plugins are also written to the USER settings.
#   - The environment log does not keep script output, so everything goes to
#     /tmp/oa-team-setup.log as well.
# It never fails the environment: each failure is logged and the session still starts.
set -u

LOG=/tmp/oa-team-setup.log
exec > >(tee -a "$LOG") 2>&1
log() { echo "[oa-team setup] $*"; }
log "start $(date -u +%FT%TZ) user=$(id -un) HOME=$HOME SKIP_PLUGIN_MARKETPLACE=${SKIP_PLUGIN_MARKETPLACE:-unset}"

MARKETPLACES=(JuliusBrussee/caveman DietrichGebert/ponytail oliverassad/oa-claude)
PLUGINS=(caveman@caveman ponytail@ponytail team@oa-claude)

install_rtk() {
  # Official way (github.com/rtk-ai/rtk): the installer takes the latest release, checks
  # its SHA-256 against checksums.txt and refuses unsafe archive paths. Then `rtk init --global`
  # adds the Claude Code hook to the user settings (--auto-patch: no prompt).
  if ! command -v rtk >/dev/null 2>&1; then
    curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh | sh \
      || { log "rtk install failed"; return; }
    # Sessions may not have ~/.local/bin on PATH; a link in /usr/local/bin covers that.
    ln -sf "$HOME/.local/bin/rtk" /usr/local/bin/rtk 2>/dev/null || export PATH="$HOME/.local/bin:$PATH"
  fi
  log "rtk: $(rtk --version 2>&1)"
  rtk init --global --auto-patch || log "rtk init failed"
}

write_user_settings() {
  # Merge, never overwrite. User settings (not repo settings) declare the marketplaces and
  # enable the plugins, so the CLI may install them at start-up if the step below fails.
  python3 -I - <<'PY' || log "could not write user settings"
import json
from pathlib import Path
path = Path.home() / ".claude" / "settings.json"
path.parent.mkdir(parents=True, exist_ok=True)
raw = path.read_text() if path.exists() else ""
settings = json.loads(raw) if raw.strip() else {}
settings.setdefault("env", {}).update({"CAVEMAN_DEFAULT_MODE": "ultra", "PONYTAIL_DEFAULT_MODE": "ultra"})
repos = {"caveman": "JuliusBrussee/caveman", "ponytail": "DietrichGebert/ponytail", "oa-claude": "oliverassad/oa-claude"}
known = settings.setdefault("extraKnownMarketplaces", {})
for name, repo in repos.items():
    known.setdefault(name, {"source": {"source": "github", "repo": repo}})
enabled = settings.setdefault("enabledPlugins", {})
for plugin in ("caveman@caveman", "ponytail@ponytail", "team@oa-claude"):
    enabled.setdefault(plugin, True)
path.write_text(json.dumps(settings, indent=2) + "\n")
print(f"[oa-team setup] user settings written: {path}")
PY
}

install_plugins() {
  command -v claude >/dev/null 2>&1 || { log "claude CLI not found; plugins left to start-up"; return; }
  log "claude $(claude --version 2>&1 | head -1)"
  for m in "${MARKETPLACES[@]}"; do
    env -u SKIP_PLUGIN_MARKETPLACE claude plugin marketplace add "$m" || log "marketplace add $m failed"
  done
  for p in "${PLUGINS[@]}"; do
    env -u SKIP_PLUGIN_MARKETPLACE claude plugin install "$p" --scope user || log "install $p failed"
  done
  claude plugin list 2>&1 | grep -E '(team|caveman|ponytail)@' || log "no core plugin listed after install"
}

install_rtk
write_user_settings
install_plugins
log "done $(date -u +%FT%TZ)"
exit 0
