# GIT: branch, commit, safety

GS overrides default agent behaviour. The project `AGENTS.md` names the integration branch (default `dev`), the production branch (default `main`) and the ticket prefix.

## BW: branch and worktree

- BW-1: Every change needs a ticket. No ticket, no branch.
- BW-2: A milestone is one branch `<type>/m<N>-slug`, cut from the integration branch, and one pull request into it, opened when the milestone is done. The operator merges.
- BW-3: A patch outside a milestone is `<type>/<TICKET>-slug` with its own pull request into the integration branch.
- BW-4: `git status --short` is empty before switching branches.
- BW-5: Never resume a branch whose pull request merged or closed. Cut a new one.
- BW-6: A worktree is for a second ticket in flight, named for its ticket, with its own dependency install.
- BW-7: Lazy branch. Fix the branch name when the work starts and use it in every plan and prompt. Create the branch or worktree only at the first write. A read-only or planning run creates none.

Types: `feat` `fix` `chore` `docs` `ci` `refactor` `style` `test` `build` `perf`. Scopes come from the project.

## GS: git safety

- GS-1: The production branch is untouchable. No commits, no pushes, no agent merges.
- GS-2: Commit subject is `type(scope): description`, lower case, ticket id as a `(<ticket>)` suffix.
- GS-3: The required check is green before any merge. Never `--no-verify` or a hook bypass.
- GS-4: Never wave a failing check through as unrelated.
- GS-5: Outward-facing actions need the operator's yes. A standing yes carries until withdrawn. Outward-facing: push, open or merge a pull request, comment, publish, create or change a provider project, change branch protection, write to Linear. Exception: the operator's ask covers creating its own ticket and setting it In Progress. Read-only work is free.
- GS-6: Never rewrite published history: no force-push, no rebase of an open pull request.
- GS-7: Secrets live in `.env` and provider settings. Never printed, logged, pasted or put in a ticket.
- GS-8: Deleting is a decision. File, table, branch, database: confirm first.
