#!/usr/bin/env python3
"""Add the shared team rules to the session or subagent context.

SessionStart gets the core rules. SubagentStart gets the core rules every agent needs plus the
rule files its role lists in roles.json, with language files kept only when the project uses
that language. A failure prints nothing: missing rules never stop a session.
"""
import json
import os
import sys
from pathlib import Path

RULES = Path(__file__).resolve().parent.parent / "rules"
SESSION = ["core/BOOT", "core/STYLE", "core/GIT", "core/SESSION", "core/DELEGATION", "core/LINEAR"]
AGENT = ["core/BOOT", "core/STYLE", "core/GIT", "core/DELEGATION"]
FOREIGN = ["core/BOOT", "core/STYLE"]  # built-in or other plugins' agents: modes and tools only
MARKERS = {
    "lang/typescript": ["package.json", "tsconfig.json"],
    "lang/svelte": ["svelte.config.js", "svelte.config.ts"],
    "lang/python": ["pyproject.toml", "requirements.txt", "setup.py"],
}


def used(rule: str, root: Path) -> bool:
    markers = MARKERS.get(rule)
    # Root and two levels down, for monorepos (apps/web/svelte.config.js).
    return markers is None or any(next(root.glob(g + m), None) for m in markers for g in ("", "*/", "*/*/"))


def files_for(event: str, payload: dict) -> list[str]:
    if event == "SessionStart":
        return SESSION
    role = str(payload.get("agent_type", "")).split(":")[-1]
    roles = json.loads((RULES / "roles.json").read_text(encoding="utf-8"))
    if role not in roles:
        return FOREIGN
    root = Path(payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or ".")
    return AGENT + [r for r in roles[role] if r not in AGENT and used(r, root)]


def main() -> None:
    event = sys.argv[1]
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    payload = json.loads(raw) if raw.strip() else {}
    names = files_for(event, payload)
    text = "\n\n".join((RULES / f"{n}.md").read_text(encoding="utf-8") for n in names)
    text += f"\n\nShared rule files: {RULES} (lang/, area/). Read one when your ticket enters its area."
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}))


if __name__ == "__main__":
    try:
        main()
    except Exception:  # noqa: BLE001 - a hook must never block the session; print nothing
        sys.exit(0)
