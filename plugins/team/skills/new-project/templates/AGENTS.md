# AGENTS.md: <project name>

Entry point for every agent and every tool. Shared rules, agents and skills come from the `team` plugin (oliverassad/oa-claude). This file holds the project facts and wins over the shared rules on conflict.

## First actions (every session, every agent)

1. Modes: rtk on; ponytail `ultra` and caveman `ultra` lines in context. Missing: Skill `ponytail:ponytail` ultra, then Skill `caveman:caveman` ultra, before any other tool call. Every answer passes both.
2. Composio first for every outside service: load `COMPOSIO_SEARCH_TOOLS` and `COMPOSIO_MULTI_EXECUTE_TOOL` with ToolSearch, search for the ask, run through `COMPOSIO_MULTI_EXECUTE_TOOL`.
3. Ticket first: every change starts from a Linear ticket or milestone on the board in `## Tracker`. Follow Skill `agent-orchestrator`.

## Tracker

- Linear team: <TEAM KEY> (ticket ids `<KEY>-123`)
- Linear project: <project name or URL>

Unknown: the orchestrator asks the operator and fills this section.

## Stack

- Languages: <TypeScript (Bun) | Python | ...>
- Frameworks: <SvelteKit | ...>
- Data: <Postgres | Firestore | ...>
- Hosting: <...>
- Spelling: <British | American>

## Branches

- Integration branch: `dev`
- Production branch: `main` (untouchable by agents)
- Commit scopes: <web, api, db, ...>

## Commands

- Install: `<bun install>`
- Check (fast, before push): `<bun run check>`
- Package tests: `<bun run test:affected>`
- Gate (auditor): `<bun run gate>`

## Area to suites

Which suites a changed area runs. A lane runs only its row.

- `<path/**>`: `<command>`

## Roles

All `team:*` roles apply. Project-only roles and role facts live in `.agents/roles/<role>.md`.

## Docs

- <Domain vocabulary>: `docs/...`
- <Design reference>: `docs/reference/...`
