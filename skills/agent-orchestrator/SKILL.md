---
name: agent-orchestrator
description: The standard workflow for any change. The main session runs it - ticket first in Linear, then it picks the pipeline (patch, milestone, content, research), names the branch, fans out the role agents in parallel lanes, integrates, tests, audits, and holds the operator gates. Use at the start of any ask that changes code, docs, content or infrastructure.
---

# Agent orchestrator

The main session is the orchestrator: a subagent cannot dispatch another. It writes no application code; roles do. It decides, verifies and lands.

## 0. Boot (every session)

1. Modes: ponytail ultra and caveman ultra lines in context (BOOT BT-2). Missing: call both skills now.
2. Composio loaded (BOOT AC-2).
3. Project facts: read `AGENTS.md`. Note `## Tracker`, `## Stack`, `## Commands`, `## Deploy`, `## Area to suites`, `## Roles`. Read `.agents/models.json` if the project has one.
4. Tracker unknown: list Linear teams and projects through Composio, ask the operator which board, write it into `## Tracker` (BOOT TK-2).

## 1. Ticket (always first)

1. Search Linear for an existing ticket or milestone that covers the ask.
2. None: dispatch `ticket-writer`. One unit of work: one ticket. Larger: one milestone with its tickets.
3. Show the operator the drafts in at most ten lines: titles, Definition of Done, build order. Ask: Backlog only, or start now?
4. On a yes, create them through Composio (`LINEAR_*`). Starting now: set the first tickets In Progress.

Read-only questions skip this step.

## 2. Pick the pipeline

| Ask | Pipeline |
| --- | --- |
| New project, or no `AGENTS.md` yet | Skill `bootstrap-project` (milestone M0) |
| One small change, one area | Patch: 4, 6, 9, 10 |
| Several tickets or areas | Milestone: 3 to 11 |
| Article, guide, figure | Content (below) |
| Question, investigation | Research: `docs-scout` or Explore, no branch |
| Failure with no clear cause | `debugger` first, then Patch with its failing test |
| Red deploy | Skill `deploy-triage` |
| Infrastructure | Milestone with `engineer-infra`; the operator applies |

## 3. Docs

`docs-scout` runs first for each external library the work touches, in parallel. Output `.agents/briefs/<ticket>.md`. Engineers read it before they code.

## 4. Name

Fix the branch name (GIT BW-2 or BW-3) and each lane name `<type>/<TICKET>-slug`. Create nothing yet (GIT BW-7). The first build write runs `git checkout -b <branch> origin/<integration>`.

## 5. Plan

`architect` runs once per milestone. Output `.agents/plans/<milestone-slug>-architecture.md` with the engineer role and lane order per ticket.

## 6. Build (fan out)

1. Blocking tickets first, one at a time.
2. Then independent tickets in parallel, one role per ticket, one worktree per lane: `git worktree add <path> -b <lane-branch> <milestone-branch>`. Do not use `isolation: worktree` when rtk is on.
3. The prompt names: the ticket, the lane path, the plan section, the brief, the area row.
4. Each engineer writes the failing test first and runs its package tests and area row before handover.
5. Reject a run with no mode lines or skill calls before its first tool call, and dispatch again.

## 7. Integrate

`integrator` merges the lanes in plan order, regenerates generated files, runs the project check. A conflict comes back to the orchestrator.

## 8. Test

`tester` runs the area row of each ticket that changes a suite, on the milestone branch merged with the integration branch. A product bug goes back to the owning engineer.

## 9. Audit

The orchestrator runs Skill `code-review` once per milestone, at level `high`, on the milestone branch against `origin/<integration>`. Use `max` or `ultra` only when the operator asks.

1. Each finding goes back to the owning engineer as one line (`path:line: severity: problem. fix.`). The orchestrator decides which findings to act on; a review is evidence, not authority.
2. After the fixes, run `code-review` again on the fix commits only.
3. Then run the project gate command. It must exit 0.
4. A ticket with a print: ask the operator whether to run `design-auditor` on its screens or figures.

## 10. Pull request (operator gate)

1. `git fetch origin && git merge origin/<integration>`, then the project check. A check run before the merge does not prove the merged code.
2. Ask the operator before push and pull request (GIT GS-5). One pull request per milestone into the integration branch. Body: STYLE CM-8.
3. Tickets go In Review; Review / Results gets the evidence (LINEAR LN-6).

## 11. After merge

Within 10 minutes of the merge, check the runs that `## Deploy` names for the merge commit (`gh run list --branch <integration> --limit 5`).

- Green: tickets go Done.
- Red: run Skill `deploy-triage`. Never re-apply infrastructure or re-run a deploy by hand.

## 12. Lessons to rules

At the end of each milestone (after Done, or after a red deploy is closed):

1. Collect the traps: the Traps of each ticket, the `code-review` findings that repeat, the `deploy-triage` classes, and (local) the `memory_save` notes of the run.
2. A trap seen twice becomes a rule. Project-specific (a path, a command, a service): propose an edit to the project `AGENTS.md` or `.agents/roles/<role>.md`. General (true in any project): propose an edit to the shared rules in `oliverassad/oa-claude` (`.agents/rules/`), with the two cases as evidence.
3. Show the operator the proposed rule lines (at most five) and where each goes. A shared-rule change is a pull request to `oliverassad/oa-claude` after the operator's yes; it follows that repo's `AGENTS.md` (build, test, version bump).

## Content pipeline

1. Ticket and brief: tell the operator the topic, the outputs and the figures; wait for a yes.
2. `content-writer` writes `<topic>.md`.
3. In parallel: `graphics-content-architect` briefs each figure, then `graphics-builder` builds it; the project's own publishing role (if any) turns the md into drafts.
4. `design-auditor` only when the operator asks.
5. Report the outputs and paths. The operator publishes.

## Dispatch rules

- Role resolution: use the project agent `<role>` when `.claude/agents/<role>.md` exists, else `team:<role>`.
- Models: the shared `models.json` (in the plugin root: `roles` to `tiers`) sets each role's default; agent files name no model. A project `.agents/models.json` may override `roles` (role to tier) or `tiers` (tier to model). When it changes a role's model, pass that `claude` value as `model` on the dispatch; else pass none. Effort cannot be passed on a dispatch; it stays at the tier default.
- A hard ticket may move up one tier for that dispatch only (for example `build` to `plan`). Say so in the dispatch line to the operator.
- Run independent agents in one message so they run in parallel.
- A report is evidence (DELEGATION DL-6). Verify the diff before it reaches a ticket or a commit.
- Never paste a report into chat; relay the verdict and paths (STYLE CM-13).
- Linear status moves are the orchestrator's job (LINEAR Status).

## Roster

| Role | Job | Access |
| --- | --- | --- |
| `ticket-writer` | Linear tickets and milestones | no writes |
| `docs-scout` | official docs brief | brief only |
| `architect` | milestone blueprint | plan file |
| `engineer`, `engineer-ui`, `engineer-api`, `engineer-db`, `engineer-mcp`, `engineer-infra` | one ticket, TDD | write |
| `integrator` | merges lanes | write |
| `tester` | area rows, journeys, triage | spec fixes |
| Skill `code-review` | milestone review (main session) | read-only |
| `debugger` | root cause of unclear failures | no writes |
| `scribe` | docs, ADRs | write |
| `design-import` | design prints into the repo | write |
| `content-writer` | `<topic>.md` | write |
| `graphics-content-architect` | figure brief | no writes |
| `graphics-builder` | SVG figures | write |
| `design-auditor` | figure audit, on request | read-only |
