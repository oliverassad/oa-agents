#!/bin/bash
# Setup script for a Claude Code cloud environment ("oa-team").
# Paste this into the environment's setup script on claude.ai (Code > Environments).
# It installs the private team plugin before the session starts, because the automatic
# install from project settings skips a private marketplace (docs/cloud-check on branch
# test/cloud-plugin-check). It never fails the environment: a missing plugin is reported
# in the setup log and the session still starts.
set -u

log() { echo "[oa-team setup] $*"; }

if ! command -v claude >/dev/null 2>&1; then
  log "claude CLI not found; skipping plugin install"
  exit 0
fi

claude plugin marketplace add oliverassad/oa-claude || log "marketplace add failed"
claude plugin install team@oa-claude || log "plugin install failed"
claude plugin list 2>&1 | grep -A3 'team@oa-claude' || log "team@oa-claude not installed"
exit 0
