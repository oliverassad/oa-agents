#!/usr/bin/env python3
"""Generate the tool-specific outputs from the neutral sources in `.agents/`.

Sources: .agents/agents/<role>/agent.md, .agents/skills/, .agents/rules/, .agents/models.json,
claude/hooks/. Outputs: plugins/team/ (Claude Code plugin) and dist/gemini/ (Gemini CLI
extension). The outputs are committed, because a plugin install copies only the plugin folder.

Usage: python3 -I scripts/build.py          write the outputs
       python3 -I scripts/build.py --check  write nothing; exit 1 when the outputs drift
"""
import filecmp
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / ".agents"
FRONT = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)
NO_WRITE = "Write, Edit, NotebookEdit"
GEMINI_CONTEXT = ["core/BOOT", "core/STYLE", "core/GIT", "core/SESSION", "core/DELEGATION", "core/LINEAR"]


def parse(path: Path) -> tuple[dict, str]:
    match = FRONT.match(path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"{path}: no frontmatter")
    meta = dict(line.split(": ", 1) for line in match.group(1).splitlines())
    meta["rules"] = [r.strip() for r in meta.get("rules", "[]").strip("[]").split(",") if r.strip()]
    return meta, match.group(2)


def claude_agent(meta: dict, body: str, tiers: dict) -> str:
    tier = tiers[meta["tier"]]
    lines = [f"name: {meta['name']}", f"description: {meta['description']}", f"model: {tier['claude']}"]
    lines += [f"effort: {tier['effort']}"] if "effort" in tier else []
    lines += [f"disallowedTools: {NO_WRITE}"] if meta["access"] in ("read-only", "no-write") else []
    first = (f"First read the project `AGENTS.md` (or `CLAUDE.md`), then `.agents/roles/{meta['name']}.md`"
             " if it exists. Both win over this file. Shared rules arrive by hook.\n\n")
    return "---\n" + "\n".join(lines) + "\n---\n\n" + first + body.lstrip()


def build_claude(out: Path, agents: list, tiers: dict) -> None:
    plugin = out / "plugins" / "team"
    (plugin / "agents").mkdir(parents=True)
    for meta, body in agents:
        (plugin / "agents" / f"{meta['name']}.md").write_text(claude_agent(meta, body, tiers), encoding="utf-8")
    shutil.copytree(SRC / "skills", plugin / "skills")
    shutil.copytree(SRC / "rules", plugin / "rules")
    roles = {meta["name"]: meta["rules"] for meta, _ in agents}
    (plugin / "rules" / "roles.json").write_text(json.dumps(roles, indent=2) + "\n", encoding="utf-8")
    shutil.copytree(ROOT / "claude" / "hooks", plugin / "hooks")
    shutil.copytree(ROOT / "claude" / "manifest", plugin / ".claude-plugin")


def build_gemini(out: Path, version: str) -> None:
    ext = out / "dist" / "gemini"
    ext.mkdir(parents=True)
    manifest = {"name": "team", "version": version, "contextFileName": "GEMINI.md"}
    (ext / "gemini-extension.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    rules = [(SRC / "rules" / f"{n}.md").read_text(encoding="utf-8") for n in GEMINI_CONTEXT]
    (ext / "GEMINI.md").write_text("\n\n".join(rules), encoding="utf-8")
    shutil.copytree(SRC / "skills", ext / "skills")
    shutil.copytree(SRC / "rules", ext / "rules")


def build(out: Path) -> None:
    tiers = json.loads((SRC / "models.json").read_text(encoding="utf-8"))["tiers"]
    agents = [parse(p) for p in sorted((SRC / "agents").glob("*/agent.md"))]
    for meta, _ in agents:
        unknown = [r for r in meta["rules"] if not (SRC / "rules" / f"{r}.md").exists()]
        if meta["tier"] not in tiers or unknown or meta["access"] not in ("write", "read-only", "no-write"):
            raise ValueError(f"{meta['name']}: bad tier, access or rules {unknown}")
    version = json.loads((ROOT / "claude" / "manifest" / "plugin.json").read_text())["version"]
    build_claude(out, agents, tiers)
    build_gemini(out, version)


def same(a: Path, b: Path) -> bool:
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.funny_files:
        return False
    _, mismatch, errors = filecmp.cmpfiles(a, b, cmp.common_files, shallow=False)
    return not mismatch and not errors and all(same(a / d, b / d) for d in cmp.common_dirs)


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        build(Path(tmp))
        targets = [Path("plugins/team"), Path("dist/gemini")]
        if "--check" in sys.argv:
            drift = [str(t) for t in targets if not (ROOT / t).exists() or not same(Path(tmp) / t, ROOT / t)]
            print(f"drift: {', '.join(drift)}; run python3 -I scripts/build.py" if drift else "outputs up to date")
            return 1 if drift else 0
        for t in targets:
            shutil.rmtree(ROOT / t, ignore_errors=True)
            shutil.copytree(Path(tmp) / t, ROOT / t)
    print("built plugins/team and dist/gemini")
    return 0


if __name__ == "__main__":
    sys.exit(main())
