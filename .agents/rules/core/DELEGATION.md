# DELEGATION: roles and reports

## DL: delegation

- DL-1: The main session is the orchestrator (Skill `agent-orchestrator`). A subagent cannot dispatch another.
- DL-2: Planning goes to `architect`. Never plan a build inline.
- DL-3: Review goes to `auditor`, once per milestone.
- DL-4: Implementation and TDD go to an engineer role. The engineer uses ponytail: shortest cut, YAGNI.
- DL-5: An agent reports. The main session decides and lands the change. No agent writes to the production branch, Linear or another lane on its own.
- DL-6: A delegated answer is evidence, not authority. Verify before it reaches a ticket or a commit.
- DL-7: Report shape: verdict first, one line per finding with its path, 5 lines unless the prompt asks for more. Quote an excerpt only when the caller cannot act without the exact bytes.

## RA: every role agent

- RA-1: First read the project `AGENTS.md` (or `CLAUDE.md`), then `.agents/roles/<role>.md` if it exists. Both win over the agent file.
- RA-2: Read only the docs of your area.
- RA-3: Docs first: read the brief the prompt names (`.agents/briefs/<ticket>.md`); none, say so. Never code an external API from memory. `docs: none (internal)` plus a reason is a valid brief.
- RA-4: Failing test first. Shortest diff. Commit to the branch or worktree the prompt names.
- RA-5: Run the tests the project names for your area. Never the full suite unless the project says so.
- RA-6: Out of scope: report it, never widen the ticket.
- RA-7: Never push, never `--no-verify`, never touch production, never read a production secret.
