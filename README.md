# oa-claude

Shared rules, agents and skills for every project. One repository is both a Claude Code plugin (`team@oa-claude`) and a Gemini CLI extension (`team`).

| Path | What | Claude | Gemini |
| --- | --- | --- | --- |
| `AGENTS.md` | the rules | loaded at session and subagent start (hook in `plugin.json`) | context file |
| `agents/` | architect, engineer, tester, debugger, docs-scout, ticket-writer | `team:<name>` | not supported |
| `skills/` | orchestrator, new-project, my-voice, svg-figures | `team:<name>` | auto-discovered |

Expects caveman and ponytail to be installed. Project facts (Linear board, stack, commands) live in each project's `AGENTS.md`.

## Install

Local machine or cloud environment setup script:

```bash
curl -fsSL https://raw.githubusercontent.com/oliverassad/oa-claude/main/install.sh | sh
```

It installs rtk, then the team plugin for Claude Code and the extension for Gemini CLI, whichever is present.

## Change

Edit the files, bump `version` in `.claude-plugin/plugin.json` and `gemini-extension.json`, push, tag `v<version>`.
