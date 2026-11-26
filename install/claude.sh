#!/bin/sh
# Claude Code: rtk hook, the caveman, ponytail and team plugins, both modes at ultra.
# Cloud sessions run with SKIP_PLUGIN_MARKETPLACE=true, so it is unset for the install.
set -u
rtk init --global --auto-patch
for repo in JuliusBrussee/caveman DietrichGebert/ponytail oliverassad/oa-claude; do
  env -u SKIP_PLUGIN_MARKETPLACE claude plugin marketplace add "$repo"
done
for plugin in caveman@caveman ponytail@ponytail team@oa-claude; do
  env -u SKIP_PLUGIN_MARKETPLACE claude plugin install "$plugin" --scope user
done
python3 - <<'PY'
import json, pathlib
p = pathlib.Path.home() / ".claude" / "settings.json"
p.parent.mkdir(exist_ok=True)
s = json.loads(p.read_text() or "{}") if p.exists() else {}
s.setdefault("env", {}).update(CAVEMAN_DEFAULT_MODE="ultra", PONYTAIL_DEFAULT_MODE="ultra")
p.write_text(json.dumps(s, indent=2) + "\n")
PY
echo "[team] claude ready"
