# oa-claude

Shared agents, skills and rules for every project, from one source:

- Claude Code: plugin `team` in marketplace `oa-claude`.
- Gemini CLI: extension in `dist/gemini/` (rules as context, skills).
- Any tool that reads `AGENTS.md`: snapshot of the rules and skills (Skill `new-project`, step 7).

## What you get

- 17 role agents (`team:architect`, `team:engineer-ui`, `team:tester`, ...). See the roster in `.agents/skills/agent-orchestrator/SKILL.md`.
- Skills: `agent-orchestrator` (the standard workflow), `my-voice`, `svg-figures`, `new-project`.
- Rules by category: `core/` for everyone, `lang/` (TypeScript, Svelte, Python), `area/` (API, MCP, database, UI, testing, dependencies, infrastructure, content).
- Hooks: core rules at session start; role and language rules at each subagent start; rtk rewrite and an absolute-path guard.

## Install

One step (Claude Code 2.1.275 or later):

```bash
/plugin install team --marketplace oliverassad/oa-claude
```

On one machine, for every project: add this to `~/.claude/settings.json`.

```json
{
  "extraKnownMarketplaces": {
    "oa-claude": { "source": { "source": "github", "repo": "oliverassad/oa-claude" } }
  },
  "enabledPlugins": { "team@oa-claude": true }
}
```

For cloud sessions too: run Skill `new-project` in the repository. It writes `.claude/settings.json` with the `team`, `caveman` and `ponytail` plugins and the ultra modes, plus `AGENTS.md`, `CLAUDE.md` and `.agents/roles/`.

The repository is private. Claude Code uses your git credentials (`gh auth login`). Background auto-update needs `GITHUB_TOKEN`. A cloud session needs the Claude GitHub App to have access to this repository.

## Project facts

Agents hold the method; each project holds its facts:

- `AGENTS.md`: Tracker (Linear team and project), Stack, Branches, Commands, Area to suites.
- `.agents/roles/<role>.md`: paths, docs, commands and traps for one role.

Both win over the shared files. A project agent named `<role>` is used before `team:<role>`.

## Develop

```bash
python3 -I scripts/build.py
```

```bash
python3 -I -m unittest discover -s scripts
```
