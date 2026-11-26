---
name: new-project
description: Sets up a repository to use the shared team - writes AGENTS.md, CLAUDE.md, .claude/settings.json (team, caveman, ponytail plugins, ultra modes) and .agents/roles/, then asks for the Linear board. Use when starting a new project or adopting the team in an existing one.
---

# New project

Run in the root of the target repository. Templates are in the `templates/` folder beside this file (the base directory shown when this skill loads).

1. **Look first.** Read any existing `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`. Never overwrite: merge.
2. **Settings.** Merge `templates/settings.json` into `.claude/settings.json`: add the marketplaces, the enabled plugins and the `env` keys that are missing. Keep every existing key.
3. **AGENTS.md.** None: copy `templates/AGENTS.md` and fill what the repo shows (stack from manifests, commands from scripts, branches from `git`). Existing: add only the missing sections (`Tracker`, `Stack`, `Branches`, `Commands`, `Area to suites`, `Roles`) and the First actions block.
4. **CLAUDE.md.** None: write `@AGENTS.md`. Existing without that import: add it as the first line.
5. **Roles.** Create `.agents/roles/README.md` from the template. Move stack facts from existing project agents into `.agents/roles/<role>.md` when the operator asks to adopt the shared agents.
6. **Tracker.** Ask the operator for the Linear team and project (list them through Composio). Write them into `## Tracker`.
7. **Other tools (on request).** For Gemini, Codex or Cursor, copy the shared rules and skills into `.agents/team/` as a snapshot and link them from `AGENTS.md`. Say that the snapshot does not update by itself.
8. **Report.** List the files written. Do not commit unless the operator asks.
