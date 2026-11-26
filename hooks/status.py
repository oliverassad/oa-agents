"""SessionStart hook: the boot status block (REC-1954).

Prints one JSON object. Claude Code shows `systemMessage` to the operator and
adds `additionalContext` for Claude. Fields: https://code.claude.com/docs/en/hooks
"""
import json
import os
import re
import subprocess
from pathlib import Path

HOME = Path.home()
CLAUDE = HOME / ".claude"


def read(path):
    try:
        return Path(path).read_text()
    except OSError:
        return ""


def run(*cmd, cwd=None):
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=3).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def found(path):
    return "ok" if Path(path).is_file() else "missing"


def count(root, pattern):
    return len(list(Path(root).glob(pattern))) if Path(root).is_dir() else 0


def servers(path):
    try:
        return list(json.loads(read(path) or "{}").get("mcpServers", {}))
    except (ValueError, AttributeError):
        return [f"unreadable {Path(path).name}"]


def mcp_servers(project):
    names = servers(HOME / ".claude.json") + servers(Path(project) / ".mcp.json")
    return ", ".join(sorted(set(names))) or "none"


def settings():
    return read(CLAUDE / "settings.json")


def tracker(project):
    m = re.search(r"^## Tracker\s*\n+(.+)", read(Path(project) / "AGENTS.md"), re.M)
    return m.group(1).strip() if m else "missing (no ## Tracker in AGENTS.md)"


def github(project):
    url = run("git", "remote", "get-url", "origin", cwd=project)
    m = re.search(r"github\.com[:/](.+?)(\.git)?$", url)
    branch = run("git", "branch", "--show-current", cwd=project)
    return f"{m.group(1)} on {branch or 'detached'}" if m else "missing (no GitHub origin)"


def modes():
    caveman = read(CLAUDE / ".caveman-active").strip() or "off"
    ponytail = os.environ.get("PONYTAIL_DEFAULT_MODE", "unset")
    on = lambda key: "on" if f'"{key}": true' in settings() else "off"
    rtk = run("rtk", "--version").removeprefix("rtk ") or "missing"
    hook = "hook on" if "rtk hook claude" in settings() else "hook off"
    return f"caveman {caveman} (plugin {on('caveman@caveman')}), ponytail {ponytail} (plugin {on('ponytail@ponytail')}), rtk {rtk} ({hook})"


def block(plugin, project):
    lines = [
        f"Rules: team AGENTS.md {found(Path(plugin) / 'AGENTS.md')}, MODELS.md {found(Path(plugin) / 'MODELS.md')}, project AGENTS.md {found(Path(project) / 'AGENTS.md')}",
        f"Agents and skills: team {count(plugin, 'agents/*.md')} agents, {count(plugin, 'skills/*/SKILL.md')} skills; project {count(Path(project) / '.claude', 'agents/*.md')} agents, {count(Path(project) / '.claude', 'skills/*/SKILL.md')} skills; MCP servers: {mcp_servers(project)}",
        f"Modes: {modes()}",
        f"Linear: {tracker(project)}",
        f"GitHub: {github(project)}",
    ]
    return "Boot status\n" + "\n".join(f"{i}. {l}" for i, l in enumerate(lines, 1))


def output(plugin, project):
    text = block(plugin, project)
    rule = "Team rule: the first reply of this session opens with this boot status block, verbatim, before any work on the request.\n\n"
    return {
        "systemMessage": text,
        "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": rule + text},
    }


if __name__ == "__main__":
    plugin = os.environ.get("CLAUDE_PLUGIN_ROOT", str(Path(__file__).resolve().parent.parent))
    project = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    print(json.dumps(output(plugin, project)))
