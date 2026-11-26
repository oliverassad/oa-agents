---
name: orchestrator
description: Standard workflow for any change - ticket in Linear first, plan, fan out engineers in parallel, review with /code-review, pull request. Use at the start of any ask that changes code, docs or infrastructure.
---

# Orchestrator

The main session runs this. It writes no product code; agents do.

1. **Ticket.** Find the Linear ticket or milestone. None: `ticket-writer` drafts it, the operator approves, create it through Composio (Backlog, or In Progress to start now).
2. **Docs.** `docs-scout` per external library, in parallel.
3. **Plan.** `architect` once per milestone. Skip for a one-file patch.
4. **Build.** Blocking tickets first. Then independent tickets in parallel: one `engineer` per ticket, one worktree per lane (`git worktree add <path> -b <lane> <branch>`). The prompt names the ticket, the worktree, the plan section and the brief.
5. **Merge.** Merge the lanes into the milestone branch. Stop on a conflict.
6. **Test.** `tester` runs the slow suites on the merged branch.
7. **Review.** Run `/code-review` on the branch. Send each finding to its engineer. Review the fixes again.
8. **Pull request.** Ask the operator, push, open one pull request. Tickets go In Review.
9. **After merge.** Check the deploy run. Red: `debugger` finds the cause, revert first if production is broken, open a fix ticket. Green: tickets go Done.

Agent names: use the project agent `<role>` when the project defines one, else `team:<role>`.
Run independent agents in one message. Verify every report before it reaches a ticket or a commit.
