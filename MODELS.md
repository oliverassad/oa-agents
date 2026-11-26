# Models

One map for every agent. Agent files name no model and no effort, so the same file works in Claude Code and Gemini CLI.

- **Claude Code:** the main session passes `model` and `effort` from this table on each dispatch. On a model error, it retries once with the fallback.
- **Gemini CLI:** `install.sh` writes the model to `agents.overrides` and the thinking level to `modelConfigs.overrides` in `~/.gemini/settings.json`. Gemini has no per-agent fallback: switch the row by hand if a model is not available.
- Gemini 4 models from the Gemini API docs (Firecrawl, 2026-11-26). No preview models. `gemini-4-argon` is left out: Gemini CLI is not optimized for it.
- A project overrides a row in its own `AGENTS.md` under `## Models`.

| Agent | Claude | Claude effort | Claude fallback | Gemini | Gemini thinking | Gemini fallback |
| --- | --- | --- | --- | --- | --- | --- |
| architect | fable | high | opus | gemini-4-carbon | high | gemini-4-neon |
| debugger | fable | high | opus | gemini-4-carbon | high | gemini-4-neon |
| ticket-writer | opus | high | sonnet | gemini-4-neon | high | gemini-4-hydrogen |
| graphics-architect | opus | high | sonnet | gemini-4-neon | high | gemini-4-hydrogen |
| editor | opus | medium | sonnet | gemini-4-neon | medium | gemini-4-hydrogen |
| engineer | sonnet | medium | opus | gemini-4-hydrogen | high | gemini-4-neon |
| engineer-ui | sonnet | medium | opus | gemini-4-hydrogen | high | gemini-4-neon |
| engineer-api | sonnet | medium | opus | gemini-4-hydrogen | high | gemini-4-neon |
| engineer-db | sonnet | medium | opus | gemini-4-hydrogen | high | gemini-4-neon |
| engineer-mcp | sonnet | medium | opus | gemini-4-hydrogen | high | gemini-4-neon |
| engineer-infra | sonnet | high | opus | gemini-4-hydrogen | high | gemini-4-neon |
| content-writer | sonnet | medium | opus | gemini-4-hydrogen | high | gemini-4-neon |
| graphics-builder | sonnet | medium | opus | gemini-4-hydrogen | medium | gemini-4-neon |
| scribe | sonnet | low | haiku | gemini-4-hydrogen | medium | gemini-4-neon |
| tester | sonnet | low | haiku | gemini-4-hydrogen | low | gemini-4-neon |
| docs-scout | sonnet | low | haiku | gemini-4-hydrogen | low | gemini-4-neon |
| design-auditor | sonnet | medium | opus | gemini-4-hydrogen | medium | gemini-4-neon |
| design-import | haiku | low | sonnet | gemini-4-hydrogen | low | gemini-4-neon |
| integrator | haiku | low | sonnet | gemini-4-hydrogen | low | gemini-4-neon |

| Tier | Claude | Gemini |
| --- | --- | --- |
| Deep planning, root cause | fable, high | gemini-4-carbon, high |
| Judgement, writing | opus, high | gemini-4-neon, high |
| Building | sonnet, medium | gemini-4-hydrogen, high |
| Mechanical | haiku or sonnet, low | gemini-4-hydrogen, low |
