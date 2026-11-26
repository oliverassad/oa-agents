---
name: bootstrap-project
description: Starts a new project from zero as milestone M0 - stack decision (ADR-001), repo skeleton, CI and deploy with a tested rollback, design tokens, domain and testing docs, the quality gate, and the project facts in AGENTS.md. The main session runs it and fans out the role agents. Use for a new repository, or a repository with no AGENTS.md and no CI.
---

# Bootstrap project (milestone M0)

The main session runs this as a normal milestone (Skill `agent-orchestrator`), with these tickets. Templates are in `templates/` beside this file; the project-facts templates are in the sibling skill `new-project/templates/`.

## 0. Intake (operator, one message)

Ask once, all together, with a recommendation for each:

1. Name, one-line purpose, the first users.
2. Surfaces: web app, admin, API, MCP server, CLI, content site.
3. Constraints: cloud, budget, data residency, languages the operator wants.
4. Design input: prints, a brand, or "none yet".
5. Linear: existing team and project, or create a new project.

## 1. Repository

No repository yet: propose the name and visibility (private by default), then create it after the operator's yes (`gh repo create`). Then run Skill `new-project` for settings, `AGENTS.md`, `CLAUDE.md`, roles and the Tracker.

## 2. Milestone M0 in Linear

Create the milestone (Working unit: an empty app that deploys. Must land: the tickets below. Demo: a merge deploys to dev, the gate is green, a rollback was tried once. Design: the prints, or "None") and these tickets (agent `ticket-writer`):

| # | Ticket | Role | Output | Depends on |
| --- | --- | --- | --- | --- |
| 1 | Stack decision | `architect` (with `docs-scout` briefs) | `docs/adr/ADR-001-stack.md` from the template | none |
| 2 | Repo skeleton | `engineer` | workspace layout, manifests with exact pins, `.gitignore`, formatter | 1 |
| 3 | Quality gate | `engineer` | `check` and `gate` commands, pre-push hook, one passing test per package | 2 |
| 4 | CI | `engineer-infra` | `.github/workflows/ci.yml` from the template, the required check on the integration branch | 3 |
| 5 | Deploy and rollback | `engineer-infra` | IaC for dev, deploy workflow, health check, `## Deploy` in `AGENTS.md`, a rollback tried once | 4 |
| 6 | Design system | `engineer-ui` (`design-import` when prints exist) | token package, one component with its story, `docs/reference/` | 2 |
| 7 | Domain and surfaces | `scribe` | `docs/product/DOMAIN.md`, `docs/product/SURFACES.md` from the templates | 1 |
| 8 | Testing guide | `scribe` | `docs/TESTING.md` and `## Area to suites` in `AGENTS.md` | 3, 4 |

Skip a ticket the surfaces do not need (no UI: skip 6) and say so in the milestone.

## 3. Build

Run the orchestrator steps 3 to 11. Lanes: 1 and 7 first; then 2; then 3 and 6 in parallel; then 4; then 5 and 8. The operator applies infrastructure (area/infra IN-3).

## 4. Done when

- `AGENTS.md` has every section filled, with no `<placeholder>` left (`grep -n '<' AGENTS.md` shows none outside code).
- The required check is green on the integration branch, and a merge deployed to dev.
- The rollback in `## Deploy` was run once and its output is in ticket 5.
- Step 12 (lessons) ran: anything general goes back to oa-claude.
