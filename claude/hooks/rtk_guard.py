#!/usr/bin/env python3
"""PreToolUse on Bash: refuse an rtk-supported tool called by absolute path.

`rtk hook claude` rewrites `git status` to `rtk git status` but does not see `/usr/bin/git status`.
Runs only when rtk is installed.
"""
import json
import re
import shutil
import sys

# ponytail: checked-in subset of `rtk --help`; add a name when `rtk discover` shows a miss.
TOOLS = "git|gh|ls|tree|cat|find|grep|rg|wc|diff|curl|wget|psql|bun|bunx|npm|npx|node|tsc|prettier|docker|kubectl|terraform|python3"
ABSOLUTE = re.compile(rf"(?:^|[\s;&|(])/\S*/({TOOLS})(?=\s|$)")


def main() -> None:
    if not shutil.which("rtk"):
        return
    command = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    match = ABSOLUTE.search(command)
    if match:
        tool = match.group(1)
        reason = f"use `{tool}` or `rtk {tool}`; absolute paths bypass the rtk rewrite."
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": reason}}))


if __name__ == "__main__":
    try:
        main()
    except Exception:  # noqa: BLE001 - never block on a hook fault
        sys.exit(0)
