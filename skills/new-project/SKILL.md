---
name: new-project
description: Prepares a repository for the team - writes the project AGENTS.md with the facts agents need (Tracker, stack, commands, paths). Use when a project has no AGENTS.md, or its AGENTS.md lacks one of these sections.
---

# New project

1. Read what exists: `AGENTS.md`, `CLAUDE.md`, manifests, scripts, CI files. Never overwrite; add missing sections.
2. Write `AGENTS.md` with these sections, filled from the repo. Write `none` where the repo has no answer. Never guess a command.

```markdown
# <project>

## Tracker
Linear team <KEY>, project <name>.

## Stack
<languages, frameworks, data, hosting>

## Commands
Install: <cmd>. Check: <cmd>. Test: <cmd>. Generate: <cmd>. Deploy: <how>. Rollback: <how>.

## Slow suites
<area path>: <command> (one line per area; tester runs only the rows a milestone touches)

## Paths
<area>: <path> - <owner agent>
Generated files: <paths>
Design reference: <path>
```

3. Ask the operator for the Linear board (list teams and projects through Composio). Write it into `## Tracker`.
4. Claude Code loads `CLAUDE.md`, not `AGENTS.md`. Make `@AGENTS.md` the first line of `CLAUDE.md`. Create the file if it is missing.
5. Add `.worktrees/` to `.gitignore`. The orchestrator puts the lane worktrees there.
6. List the files written. Do not commit unless asked.
