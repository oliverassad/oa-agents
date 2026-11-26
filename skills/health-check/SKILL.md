---
name: health-check
description: Weekly repository health check - outdated and vulnerable dependencies, a security review, and stale pins - with findings drafted as Linear Backlog tickets. Built to run as a scheduled cloud routine; it fixes nothing.
---

# Health check

Runs unattended (a scheduled routine) or on request. It reads and reports; it never changes code, never pushes, never merges.

## 1. Setup

1. Read the project `AGENTS.md` (`## Tracker`, `## Stack`, `## Commands`).
2. Install dependencies with the project install command.

## 2. Checks

1. **Vulnerabilities**: the audit command of each package manager in the repo (`bun audit` or `npm audit --omit=dev`, `pip-audit`, `terraform` provider versions). Record each advisory with its severity and the fixed version.
2. **Outdated pins**: `bun outdated` or `npm outdated`, `pip list --outdated`. Compare with the latest stable on the registry (area/deps DP-1, DP-2). Flag major versions apart and pins older than 6 months.
3. **Security review**: run Skill `security-review` on the integration branch against the last release tag (or the last 7 days of commits when there is no tag).
4. **Required check**: the last run of the required CI check on the integration branch is green (`gh run list --branch <integration> --limit 1`).

## 3. Tickets

1. Search Linear for an open ticket on the same package or finding first. Found: add a comment line only when the severity changed.
2. New finding: one ticket per package (not per advisory), state Backlog, label `health-check`, eight sections (LINEAR). Critical and High advisories get priority High.
3. Unattended run: create the Backlog tickets (the routine's prompt is the operator's standing yes for Backlog tickets only). Never move a ticket out of Backlog, never open a pull request.

## 4. Report

One summary line per check, then the ticket ids: `HEALTH <repo> <date> | vulns: n (critical n) | outdated: n | security: n findings | ci: green/red | tickets: ...`.

## Schedule it

Use Skill `schedule` to create a weekly routine per repository (Monday 07:00 local), prompt: `Run Skill team:health-check for this repository.` The repository needs `.claude/settings.json` with the team plugin (Skill `new-project`).
