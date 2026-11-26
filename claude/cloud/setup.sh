#!/bin/bash
# Setup script for the Claude Code cloud environment "oa-team".
# Paste it into the environment's setup script on claude.ai (Code > Environments).
#
# It makes every cloud session in this environment start like a local one:
#   1. rtk 1.2.1 (pinned, checksum-verified) in ~/.local/bin
#   2. plugins caveman, ponytail and team (private oliverassad/oa-claude) at user scope.
#      The automatic install from project settings skips a private marketplace, so the
#      install happens here, before the session starts.
#   3. caveman and ponytail at level ultra (env in ~/.claude/settings.json)
# The rtk rewrite hook comes from the team plugin (hooks/rtk_rewrite.sh).
# It never fails the environment: each failure is logged and the session still starts.
set -u

log() { echo "[oa-team setup] $*"; }

RTK_VERSION="1.2.1"
declare -A RTK_SHA256=(
  [x86_64]="75f64525711be935657a6b228d929c24bd9d1ab7d640ea374a8b913e5b5bac05"
  [aarch64]="cae1a911eda9e898dbb90039436e9d53922b20afb1e3e4ae341f749eb62b7781"
)

install_rtk() {
  if command -v rtk >/dev/null 2>&1; then
    log "rtk present: $(rtk --version)"
    return
  fi
  local arch sha asset tmp
  arch="$(uname -m)"
  sha="${RTK_SHA256[$arch]:-}"
  [ -n "$sha" ] || { log "no pinned rtk build for $arch"; return; }
  asset="rtk-${arch}-unknown-linux-musl.tar.gz"
  tmp="$(mktemp -d)"
  curl -fsSL -o "$tmp/$asset" "https://github.com/rtk-ai/rtk/releases/download/v${RTK_VERSION}/${asset}" \
    || { log "rtk download failed"; return; }
  echo "$sha  $tmp/$asset" | sha256sum -c --status \
    || { log "rtk checksum mismatch; not installed"; return; }
  mkdir -p "$HOME/.local/bin"
  tar -xzf "$tmp/$asset" -C "$tmp" && install -m 0755 "$(find "$tmp" -type f -name rtk | head -1)" "$HOME/.local/bin/rtk" \
    && log "rtk installed: $("$HOME/.local/bin/rtk" --version)" || log "rtk install failed"
  rm -rf "$tmp"
}

install_plugins() {
  command -v claude >/dev/null 2>&1 || { log "claude CLI not found; skipping plugins"; return; }
  claude plugin marketplace add JuliusBrussee/caveman || log "caveman marketplace failed"
  claude plugin marketplace add DietrichGebert/ponytail || log "ponytail marketplace failed"
  claude plugin marketplace add oliverassad/oa-claude || log "oa-claude marketplace failed"
  for p in caveman@caveman ponytail@ponytail team@oa-claude; do
    claude plugin install "$p" || log "install $p failed"
  done
}

set_modes() {
  # Merge, never overwrite: keep every key already in the user settings.
  python3 -I - <<'PY' || log "could not set modes"
import json
from pathlib import Path
path = Path.home() / ".claude" / "settings.json"
path.parent.mkdir(parents=True, exist_ok=True)
settings = json.loads(path.read_text()) if path.exists() and path.read_text().strip() else {}
settings.setdefault("env", {}).update({"CAVEMAN_DEFAULT_MODE": "ultra", "PONYTAIL_DEFAULT_MODE": "ultra"})
path.write_text(json.dumps(settings, indent=2) + "\n")
print("[oa-team setup] modes set to ultra in", path)
PY
}

install_rtk
install_plugins
set_modes
command -v claude >/dev/null 2>&1 && claude plugin list 2>&1 | grep -E '^\s+. (team|caveman|ponytail)@' || true
exit 0
