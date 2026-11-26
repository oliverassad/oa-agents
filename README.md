# oa-claude

Shared rules, agents and skills for every project. One repository is both a Claude Code plugin (`team@oa-claude`) and a Gemini CLI extension (`team`).

| Path | What | Claude | Gemini |
| --- | --- | --- | --- |
| `AGENTS.md` | the rules and the boot checklist | loaded at session and subagent start (hook in `plugin.json`) | context file |
| `MODELS.md` | model per agent: Claude, Claude fallback, Gemini | loaded at session start; passed per dispatch | written to `agents.overrides` by `install.sh` |
| `agents/` | 19 agents, one per job (see `skills/orchestrator/SKILL.md`) | `team:<name>` | loaded |
| `skills/` | orchestrator, new-project, my-voice, svg-figures | `team:<name>` | auto-discovered |

This repository does not install three things that the team needs: the caveman plugin, the ponytail plugin and the Composio MCP server. Connect Linear, GitHub and Firecrawl in Composio. Project facts (Linear board, stack, commands) live in each project's `AGENTS.md`. Skill `new-project` writes that file.

## Install

Local machine or cloud environment setup script:

```bash
curl -fsSL https://raw.githubusercontent.com/oliverassad/oa-claude/main/install.sh | sh
```

It installs rtk, then the team plugin for Claude Code and the extension for Gemini CLI, whichever is present. For Gemini CLI it also adds `AGENTS.md` to `context.fileName`, so Gemini loads the project `AGENTS.md`. Run it again to update.

To install only the plugin from inside Claude Code:

```
/plugin install team --marketplace oliverassad/oa-claude
```

## Change

Agent files carry no `model` (Gemini refuses Claude names); `MODELS.md` holds the map.

Edit the files, bump `version` in `.claude-plugin/plugin.json` and `gemini-extension.json`, push, then publish a GitHub release `v<version>` (`gh release create v<version>`). Gemini installs and updates from the latest release, not from `main`.
