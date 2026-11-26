# oa-agents

Shared rules, agents and skills for every project. One repository is both a Claude Code plugin (`oa-agents@oa-agents`) and a Gemini CLI extension (`oa-agents`).

| Path | What | Claude | Gemini |
| --- | --- | --- | --- |
| `AGENTS.md` | the rules and the boot checklist | loaded at session and subagent start (hook in `plugin.json`) | context file |
| `MODELS.md` | model per agent: Claude, Claude fallback, Gemini | loaded at session start; passed per dispatch | written to `agents.overrides` by `install.sh` |
| `agents/` | 19 agents, one per job (see `skills/orchestrator/SKILL.md`) | `oa-agents:<name>` | loaded |
| `skills/` | orchestrator, new-project, my-voice, svg-figures | `oa-agents:<name>` | auto-discovered |

`install.sh` also installs the caveman and ponytail plugins for Claude Code (Gemini needs them separately). It does not install the Composio MCP server. Connect Linear, GitHub and Firecrawl in Composio. Project facts (Linear board, stack, commands) live in each project's `AGENTS.md`. Skill `new-project` writes that file.

## Install

Local machine or cloud environment setup script:

```bash
curl -fsSL https://raw.githubusercontent.com/oliverassad/oa-agents/main/install.sh | sh
```

It installs rtk, then the oa-agents plugin for Claude Code and the extension for Gemini CLI, whichever is present. For Gemini CLI it also adds `AGENTS.md` to `context.fileName`, so Gemini loads the project `AGENTS.md`. Run it again to update.

> **Antigravity / Gemini cloud only:** [`cloud-setup.sh`](cloud-setup.sh) and [`.agents/environment.json`](.agents/environment.json) are exclusively for Antigravity / Gemini cloud VMs (which do not run Claude Code plugins or hooks). Do not run them automatically for Claude Code or other agents.

To install only the plugin from inside Claude Code:

```
/plugin install oa-agents --marketplace oliverassad/oa-agents
```

## Boot status

At the start of each session, `hooks/status.py` shows a six-line status: rules, agents and skills, MCP (servers in the config files, and the Composio check), modes (caveman, ponytail, rtk), the Linear project (`## Tracker` in the project `AGENTS.md`, else the repository name) and the GitHub repository. The hook runs while the other plugins still start. The agent fixes each `off` or `missing` line, checks Composio, runs `python3 hooks/status.py --text` again and opens its first reply with that block, every line green. Test: `python3 hooks/test_status.py`.

## Change

Agent files carry no `model` (Gemini refuses Claude names); `MODELS.md` holds the map.

Edit the files on a branch and bump `version` in `.claude-plugin/plugin.json` and `gemini-extension.json`. Open a pull request and squash-merge it: the `Protect main` ruleset blocks direct pushes, force-pushes and other merge methods, and every review thread must be resolved. Then publish a GitHub release `v<version>` (`gh release create v<version>`). Gemini installs and updates from the latest release, not from `main`. The `Protect release tags` ruleset blocks a move or delete of a `v*` tag, so a bad release gets a new version.
