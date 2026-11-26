# Role files

One file per role that needs project facts: `.agents/roles/<role>.md` (for example `engineer-ui.md`). The `team:<role>` agent reads it after `AGENTS.md`, and it wins over the agent file.

Put here: the paths the role owns, the docs it reads, the exact commands, the traps. Do not repeat the shared rules.

Example `engineer-db.md`:

```markdown
# engineer-db

- Area: `packages/db`. Store: Firestore and GCS.
- Docs: `docs/GCP.md`.
- Emulators: `bun run emulators up`, then export the hosts it prints.
- Trap: the dev project is shared; never point a test at it.
```
