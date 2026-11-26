# Team rules

Shared rules for every project and every agent. The project's own `AGENTS.md` wins on conflict.

## Boot checklist

Run these checks at the start of every session and every agent run, before the first other tool call.

1. `CAVEMAN MODE ACTIVE` and `PONYTAIL MODE ACTIVE` are in context. Missing: call Skill `caveman:caveman` and Skill `ponytail:ponytail`.
2. The project `AGENTS.md` is read: Tracker, stack, commands, paths, models.
3. The task has a Linear ticket, or it is a read-only question.
4. The branch name comes from the ticket. You are not on `main`.
5. A plan exists in `.agents/plans/` for a milestone, and you know your section of it.
6. Composio tools are loaded if the task touches an outside service.

## Modes

- caveman and ponytail are on. Chat answers are caveman. Code changes are ponytail: shortest diff, YAGNI, reuse.
- rtk rewrites shell commands. Call tools by name, never by absolute path.
- Text a person reads later (docs, tickets, commits, comments) follows Skill `my-voice`.

## Services

- Every outside service (Linear, GitHub, Notion, Slack, Gmail, Drive, Firecrawl) goes through Composio: search with `COMPOSIO_SEARCH_TOOLS`, run with `COMPOSIO_MULTI_EXECUTE_TOOL`.
- Never report a service unreachable before the Composio search.

## Work

1. Ticket first. Every change starts from a Linear ticket or milestone. The board comes from `## Tracker` in the project `AGENTS.md`. None: ask which board, then write it there.
2. Branch per ticket or milestone. Never commit to `main`.
3. Docs first. Read the official docs of a library before coding against it.
4. Failing test first. Never skip or disable a test to get green.
5. Report what happened, with the failing output. Never wave a red check through.

## Plans and memory

- **Plans:** one file per milestone, `.agents/plans/<milestone>.md`, written by `architect` and committed on the milestone branch. The Linear milestone links to it. Library briefs go to `.agents/briefs/<ticket>.md`.
- **Memory:** no memory folder and no memory agent. Facts that every agent needs go in the project `AGENTS.md`. At the end of a milestone, the main session moves each trap that happened twice into `AGENTS.md`. Notes for one machine stay in local memory tools.

## Safety

- Ask before anything outward-facing: push, pull request, merge, comment, Linear write, publish.
- Never force-push, never rewrite published history, never print a secret.
- Deleting a file, branch or table is a decision: confirm first.

## Agents

- The main session orchestrates (Skill `orchestrator`). Subagents cannot dispatch other agents.
- A subagent reports; the main session decides and lands the change.
- Report: verdict first, one line per finding with its path, 5 lines at most.
- Models: `MODELS.md` in this plugin.
