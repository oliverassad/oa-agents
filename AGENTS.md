# AGENTS.md: oa-claude

This repository holds the shared agents, skills and rules for every project of the operator. It is the source for the Claude Code plugin `team` and the Gemini CLI extension `team`.

## Layout

- `.agents/agents/<role>/agent.md`: one role, tool-neutral. Frontmatter: `name`, `description`, `access` (`write`, `read-only`, `no-write`), `rules` (rule files the role gets).
- `.agents/skills/<name>/SKILL.md`: skills in the Agent Skills format.
- `.agents/rules/`: `core/` (every session and agent), `lang/` (per language), `area/` (per area: api, mcp, db, ui, testing, deps, infra, content).
- `.agents/models.json`: the model map. `roles` (role to tier) and `tiers` (tier to model per tool). Every agent needs a role entry; the build fails otherwise.
- `claude/`: Claude-only sources (plugin manifest, hooks).
- `plugins/team/`, `dist/gemini/`: generated. Never edit them by hand.

## Change a role, skill or rule

1. Edit the source under `.agents/` or `claude/`.
2. Run `python3 -I scripts/build.py`.
3. Run `python3 -I -m unittest discover -s scripts`.
4. Bump `version` in `claude/manifest/plugin.json` whenever the outputs change, so installed copies update. CI (`scripts/version_guard.py`) fails otherwise.
5. Commit sources and outputs together. CI fails when they drift.

## Rules for this repo

- Shared files hold the method. Project facts (paths, commands, Linear board) belong in each project's `AGENTS.md` and `.agents/roles/<role>.md`.
- Never put a secret, a token or a private path in this repo.
- The team rules (`.agents/rules/core/`) apply to work here too.
