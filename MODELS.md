# Models

One map for every agent. Agent files name no model, so the same file works in Claude Code and Gemini CLI.

- **Claude Code:** the main session passes the Claude model on each dispatch (`model` parameter). If that model is not available, it passes the fallback.
- **Gemini CLI:** `install.sh` writes the Gemini column to `~/.gemini/settings.json` (`agents.overrides`). If that model is not available, the agent inherits the main session model.
- Gemini model names come from the Gemini CLI docs. Check them with `/model` in Gemini CLI.

| Agent | Claude | Claude fallback | Gemini |
| --- | --- | --- | --- |
| architect | fable | opus | gemini-3-preview |
| debugger | fable | opus | gemini-3-preview |
| ticket-writer | opus | sonnet | gemini-3-preview |
| graphics-architect | opus | sonnet | gemini-3-preview |
| editor | opus | sonnet | gemini-3-preview |
| engineer | sonnet | haiku | gemini-3-flash-preview |
| engineer-ui | sonnet | haiku | gemini-3-flash-preview |
| engineer-api | sonnet | haiku | gemini-3-flash-preview |
| engineer-db | sonnet | haiku | gemini-3-flash-preview |
| engineer-mcp | sonnet | haiku | gemini-3-flash-preview |
| engineer-infra | sonnet | haiku | gemini-3-flash-preview |
| tester | sonnet | haiku | gemini-3-flash-preview |
| docs-scout | sonnet | haiku | gemini-3-flash-preview |
| scribe | sonnet | haiku | gemini-3-flash-preview |
| content-writer | sonnet | haiku | gemini-3-flash-preview |
| graphics-builder | sonnet | haiku | gemini-3-flash-preview |
| design-auditor | sonnet | haiku | gemini-3-flash-preview |
| design-import | sonnet | haiku | gemini-3-flash-preview |
| integrator | haiku | sonnet | gemini-3-flash-preview |

A project can override a row in its own `AGENTS.md` under `## Models`.
