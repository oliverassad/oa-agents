---
name: deploy-triage
description: What to do when a deploy or a post-deploy check goes red - read the failed run, classify the cause, revert first when production is broken, and draft the fix ticket with the proving log line. The orchestrator runs it from step 11; use it for any red deploy, release or journey run.
---

# Deploy triage

The main session runs this. Facts come from `## Deploy` in the project `AGENTS.md` (deploy command, rollback command, health check, environments). No `## Deploy` section: stop, tell the operator, and draft a ticket to add one (area/infra IN-7).

## 1. Read (2 minutes)

1. Find the run of the merge commit: `gh run list --branch <branch> --limit 5`, matched to `git rev-parse origin/<branch>`.
2. Read only the failure: `gh run view <id> --log-failed`. Keep the one log line that proves the cause.
3. Note which job failed (build, apply, smoke, journeys) and which environment it touched.

## 2. Classify

| Class | Signal | Owner |
| --- | --- | --- |
| App bug | a test, smoke or journey fails on app behaviour | the engineer of the area |
| Infrastructure | plan or apply error, quota, permission, state lock | `engineer-infra` (plan), operator (apply) |
| Config or secret | missing variable, wrong key, expired token | operator (never print the value) |
| Flake | passes on one rerun, and the log shows a timing or network cause | `tester` |
| External | provider outage on its status page | nobody; wait and recheck |

A second red on rerun is real until proven flake (area/testing TG-9). Rerun once at most: `gh run rerun <id> --failed`, with the operator's yes (outward-facing).

## 3. Contain (production only)

Production broken (health check red, users affected):

1. Revert first, fix second. Propose the rollback the project names, or a pull request that reverts the merge (`git revert -m 1 <merge-sha>` on a branch `fix/<TICKET>-revert-<slug>`).
2. Ask the operator before any push, pull request or rollback (GIT GS-5). Give: what broke, since when, the rollback, and what it undoes.
3. Never run `apply`, never change a provider console, never re-run a deploy by hand.

Integration environment only: no revert unless the operator asks. Block the next milestone pull request until it is green.

## 4. Ticket

Draft a fix ticket (agent `ticket-writer`) with: the run URL, the proving log line, the class, the commit, the environment, the containment done. Priority Urgent when production was broken. Create it through Composio after the operator's yes.

## 5. Report (five lines)

`DEPLOY RED: <env> <job> | class: <class> | cause: <log line> | contained: <yes/no, how> | ticket: <id or draft>`
