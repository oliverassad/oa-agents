#!/usr/bin/env python3
"""Fail when the generated outputs change but the plugin version does not.

Installed copies update only when `version` in claude/manifest/plugin.json changes.
Usage: python3 -I scripts/version_guard.py <base-ref>   (for example origin/main)
"""
import json
import subprocess
import sys

OUTPUTS = ("plugins/team/", "gemini-extension.json", "GEMINI.md")
MANIFEST = "claude/manifest/plugin.json"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def version_at(ref: str) -> str:
    return json.loads(git("show", f"{ref}:{MANIFEST}"))["version"]


def decide(changed: list[str], old: str, new: str) -> str | None:
    if not any(path.startswith(OUTPUTS) for path in changed):
        return None
    if old == new:
        return f"plugin files changed but version is still {new}; bump it in {MANIFEST}"
    return None


def main() -> int:
    base = sys.argv[1]
    changed = git("diff", "--name-only", f"{base}...HEAD").splitlines()
    reason = decide(changed, version_at(base), version_at("HEAD"))
    print(reason or "version guard: ok")
    return 1 if reason else 0


if __name__ == "__main__":
    sys.exit(main())
