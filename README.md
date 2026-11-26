# oa-claude

Shared agents, skills and rules for every project, from one source:

- Claude Code: plugin `team` in marketplace `oa-claude`.
- Gemini CLI: this repo root is the extension (`gemini-extension.json`, `GEMINI.md`, `skills/`).
- Any tool that reads `AGENTS.md`: snapshot of the rules and skills (Skill `new-project`, step 7).

## What you get

- 18 role agents (`team:architect`, `team:engineer-ui`, `team:tester`, ...). See the roster in `skills/agent-orchestrator/SKILL.md`.
- Skills: `agent-orchestrator` (the standard workflow), `deploy-triage` (red deploys), `health-check` (weekly, schedulable), `bootstrap-project` (new project as milestone M0), `my-voice`, `svg-figures`, `new-project`.
- Rules by category: `core/` for everyone, `lang/` (TypeScript, Svelte, Python), `area/` (API, MCP, database, UI, testing, dependencies, infrastructure, content).
- Hooks: core rules at session start; role and language rules at each subagent start; rtk rewrite and an absolute-path guard.

## Install

One line, for every agent CLI on the machine (Claude Code, Gemini CLI). It installs rtk the official way, the caveman and ponytail plugins or extensions, this team, and sets both modes to ultra:

```bash
curl -fsSL https://raw.githubusercontent.com/oliverassad/oa-claude/main/install.sh | sh
```

One CLI only: append `-s -- claude` or `-s -- gemini` after `sh`. The per-CLI steps are in `install/claude.sh` and `install/gemini.sh`.

Cloud environment: put the same line in the environment's setup script. Then every session in it starts with everything installed.

Per repository (so a project also works for people who did not run the line): run Skill `new-project`. It writes `.claude/settings.json` with the plugins and modes, plus `AGENTS.md`, `CLAUDE.md` and `.agents/roles/`.

## Models

`.agents/models.json` is the one place that says which model runs which role: `roles` maps a role to a tier, `tiers` maps a tier to a model per tool. Agents name no model.

| Tier | Claude | Roles |
| --- | --- | --- |
| main | opus, effort high | main session: orchestrator, code-review |
| plan-deep | fable, effort medium | architect, debugger |
| plan | opus | graphics-content-architect, ticket-writer |
| build | sonnet | engineers, tester, scribe, docs-scout, design-import, design-auditor, content-writer, graphics-builder |
| cheap | haiku | integrator |

A project overrides roles or tiers in its own `.agents/models.json`; the orchestrator passes the model on each dispatch. `CLAUDE_CODE_SUBAGENT_MODEL` in a project's settings forces one model on every subagent.

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
