---
name: agent-orchestrator
description: The standard workflow for any change. The main session runs it - ticket first in Linear, then it picks the pipeline (patch, milestone, content, research), names the branch, fans out the role agents in parallel lanes, integrates, tests, audits, and holds the operator gates. Use at the start of any ask that changes code, docs, content or infrastructure.
---

# Agent orchestrator

The main session is the orchestrator: a subagent cannot dispatch another. It writes no application code; roles do. It decides, verifies and lands.

## 0. Boot (every session)

1. Modes: ponytail ultra and caveman ultra lines in context (BOOT BT-2). Missing: call both skills now.
2. Composio loaded (BOOT AC-2).
3. Project facts: read `AGENTS.md`. Note `## Tracker`, `## Stack`, `## Commands`, `## Area to suites`, `## Roles`.
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
| One small change, one area | Patch: 4, 6, 9, 10 |
| Several tickets or areas | Milestone: 3 to 11 |
| Article, guide, figure | Content (below) |
| Question, investigation | Research: `docs-scout` or Explore, no branch |
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

`auditor` runs once per milestone, read-only: nine angles, then the gate. Findings go back to the owning engineer; re-audit only the fixed angles.

## 10. Pull request (operator gate)

1. `git fetch origin && git merge origin/<integration>`, then the project check. A check run before the merge does not prove the merged code.
2. Ask the operator before push and pull request (GIT GS-5). One pull request per milestone into the integration branch. Body: STYLE CM-8.
3. Tickets go In Review; Review / Results gets the evidence (LINEAR LN-6).

## 11. After merge

Check the deploy and journey runs of the merge commit (`gh run list`, `gh run view --log-failed`). Red: report and open a fix ticket; never re-apply infrastructure by hand. Green: tickets go Done.

## Content pipeline

1. Ticket and brief: tell the operator the topic, the outputs and the figures; wait for a yes.
2. `content-writer` writes `<topic>.md`.
3. In parallel: `graphics-content-architect` briefs each figure, then `graphics-builder` builds it; the project's own publishing role (if any) turns the md into drafts.
4. `design-auditor` only when the operator asks.
5. Report the outputs and paths. The operator publishes.

## Dispatch rules

- Role resolution: use the project agent `<role>` when `.claude/agents/<role>.md` exists, else `team:<role>`.
- Models come from the agent definition. Pass no model by hand unless the operator asks.
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
| `auditor` | nine-angle review | read-only |
| `scribe` | docs, ADRs | write |
| `design-import` | design prints into the repo | write |
| `content-writer` | `<topic>.md` | write |
| `graphics-content-architect` | figure brief | no writes |
| `graphics-builder` | SVG figures | write |
| `design-auditor` | figure audit, on request | read-only |
