---
name: orchestrator
description: How the main session runs any task - decide the kind of work, size code work as a Backlog ticket or a milestone, fan out the agents, fast checks per lane, slow suites and one audit per milestone before the pull request. Use at the start of every task.
---

# Orchestrator

The main session decides, dispatches, checks reports and talks to the operator. Agents do the work. Fan out: every agent that does not wait on another runs in the same message. An operator wait is free time: start the work that does not need the answer.

## 1. Fork first

| Kind | Ticket | Path |
| --- | --- | --- |
| Question | no | Answer. A library fact: `docs-scout` |
| Content (article, guide, figure, slides) | no | Section 4 |
| Small code or infra change | one Backlog ticket | Section 2 |
| Heavy code or infra change | a Linear milestone | Section 3 |
| Failure with no clear cause | after the cause | `debugger`, then section 2 or 3 |

Small: one area, one engineer, no new shared contract. Everything else is heavy. Default to small; if the ticket draft holds more than one unit of work, it is heavy.

## 2. Small change (Backlog ticket)

1. **Ticket.** The ask names the files or the behaviour: the main session drafts the ticket itself. Scoping needs a code read: `ticket-writer`. One operator yes covers "create the ticket and build it".
2. **Build.** One engineer on the ticket branch. It fetches its own snippets (no `docs-scout`) and runs its fast checks: typecheck, lint, package tests.
3. **Review.** `/code-review` on the diff. Findings go back to the engineer.
4. **Pull request.** Ask the operator. Slow suites run in CI on the pull request; no `tester`.

## 3. Heavy change (milestone)

1. **Design.** In one message: `architect` (the ask in, the whole milestone out: tickets T1..Tn, contracts, waves) and one `docs-scout` per library the ask names.
2. **Approve once.** Show the operator the milestone in ten lines at most. While waiting: one `docs-scout` per library the plan adds.
3. **Create.** On the yes, in one turn: all Linear writes in one Composio batch (milestone and tickets), replace T1..Tn with the real ids in the plan, commit the plan and briefs, create the milestone branch and one worktree per ticket (`git worktree add .worktrees/<ticket> -b <ticket-branch> <milestone-branch>`). Never `isolation: worktree`: it refuses `rtk git`.
4. **Build.** Wave 1: the contract tickets. Wave 2: every other ticket, all in one message, one engineer each. A third wave needs a reason in the plan. Each engineer runs its fast checks before handover.
5. **Merge.** The main session merges each finished lane into the milestone branch and runs the project check. `integrator` only for a generated-file or real conflict.
6. **Prove once.** `git merge origin/main` into the milestone branch. Then in the same turn: `tester` in the background on the slow suites of the touched areas only, and `/code-review` (plus `/security-review` for auth, secrets, input or infrastructure) in the main session. Merge both finding sets into one fix round: one engineer per owner, in one message, in the kept lane worktrees. Then rerun only the red suites and review only the fix commits.
7. **Pull request.** Ask the operator. One yes covers push, one pull request and moving every ticket to In Review. Remove the worktrees after the merge.
8. **After merge.** Deploy red: `debugger`, revert first if production broke. Green: tickets Done. Move each trap seen twice into the project `AGENTS.md`.

## When each check runs

| When | Who | What |
| --- | --- | --- |
| Before each handover | engineer | typecheck, lint, tests of its package |
| Small change, on the pull request | CI | slow suites |
| Milestone, after `origin/main` is merged | `tester` and main session, in parallel | slow suites of touched areas; `/code-review` and `/security-review`, once |
| After the merge to `main` | main session | deploy run |

## 4. Content

1. `content-writer` writes `<topic>.md` and lists its figure requests.
2. In one message: `editor` on the text, one `graphics-architect` per figure request.
3. In one message: one `graphics-builder` per brief.
4. The operator reviews and publishes. `design-auditor` only on request. Repo docs: `scribe`.

If the ask already names the figures, start the `graphics-architect` briefs in step 1.

## Who to ask

| Need | Ask |
| --- | --- |
| Scope, publish, push, merge, delete, new dependency | Operator |
| How a library works today | `docs-scout` |
| Milestone design and waves | `architect` |
| A single ticket that needs a code read | `ticket-writer` |
| Why it fails | `debugger` |
| Does it work, is it safe | `tester`, `/code-review`, `/security-review` |
| Does the text read right | `editor` |
| What a figure says | `graphics-architect` |

## Dispatch

- Name: the project agent `<role>` if the project has one, else `team:<role>`.
- Engineer: from `## Paths` in the project `AGENTS.md` (`engineer-ui`, `engineer-api`, `engineer-db`, `engineer-mcp`, `engineer-infra`), else `engineer`.
- Pass `model` and `effort` from `MODELS.md` on every dispatch. On a model error, retry once with the fallback.
- An agent sees only its file, the team rules and your prompt. Give it every item in the `## Context` list of its agent file. For an engineer:

```
TICKET: <id> - <title>
DESCRIPTION: <current state, what to build, files it owns, traps>
DEFINITION OF DONE:
- [ ] <line>
BRANCH: <branch, or worktree path>
PLAN: .agents/plans/<milestone>.md, section <ticket id> | none
BRIEFS: .agents/briefs/<library>.md, ... | none
COMMANDS: <install, typecheck, lint, test>
```

- Check each report against its Definition of Done; a missing box goes back.
- To resume, read the plan, the ticket states and `git worktree list` first.
