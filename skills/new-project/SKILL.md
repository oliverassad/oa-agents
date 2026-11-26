---
name: new-project
description: Prepares a repository for the team - writes the project AGENTS.md with the facts agents need (Tracker, stack, commands, paths). Use when a project has no AGENTS.md.
---

# New project

1. Read what exists: `AGENTS.md`, `CLAUDE.md`, manifests, scripts, CI files. Never overwrite; add missing sections.
2. Write `AGENTS.md` with these sections, filled from the repo:

```markdown
# <project>

## Tracker
Linear team <KEY>, project <name>.

## Stack
<languages, frameworks, data, hosting>

## Commands
Install: <cmd>. Check: <cmd>. Test: <cmd>. Deploy: <how>. Rollback: <how>.

## Paths
<area>: <path> - <owner agent>
```

3. Ask the operator for the Linear board (list teams and projects through Composio). Write it into `## Tracker`.
4. If `CLAUDE.md` exists without it, add `@AGENTS.md` as its first line.
5. List the files written. Do not commit unless asked.
