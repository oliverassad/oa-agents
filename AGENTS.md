# Team rules

Shared rules for every project and every agent. The project's own `AGENTS.md` wins on conflict.

## Boot checklist

Run these checks at the start of every session and every agent run, before the first other tool call.

1. `PONYTAIL MODE ACTIVE` is in context. Missing: call Skill `ponytail:ponytail` with `ultra`. Main session: `CAVEMAN MODE ACTIVE` too, else call Skill `caveman:caveman` with `ultra`. Subagents get no caveman hook: write reports caveman-short anyway.
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

## Docs: Firecrawl only

Every agent that writes code or commands against a library, API or tool gets the snippet from its current official docs. Never from memory, never from random research.

1. Read the version from the lockfile or manifest. No pin: use the latest stable release.
2. Load Firecrawl: ToolSearch `COMPOSIO_SEARCH_TOOLS`, then run `FIRECRAWL_SEARCH` and `FIRECRAWL_SCRAPE` through `COMPOSIO_MULTI_EXECUTE_TOOL` (or the Firecrawl MCP when it is present).
3. Search only the official docs domain or the project repository (`site:docs.example.com`). Then scrape the exact page.
4. Copy the snippet with its source URL and version into the brief or the code comment that needs it.
5. Never use WebSearch, WebFetch, blogs, Stack Overflow or forum answers for code. Firecrawl unavailable: stop and report.

## Agent run

Every subagent runs these steps in order.

1. **Boot.** The boot checklist above.
2. **Shell.** Run commands by bare name (`git`, `bun`, `npm`) so rtk rewrites them. Never an absolute path like `/usr/bin/git`.
3. **Read.** Read the ticket, your plan section, the brief, and every file you will change and its callers.
4. **Docs.** Firecrawl only, as above.
5. **Test.** Write the failing test. Run it. See it fail for the right reason.
6. **Build.** Shortest diff that passes (ponytail). Reuse what exists. No new dependency without the operator.
7. **Check.** Before handover: tests green, no stub or TODO, no debug output, no secret, only the files the ticket owns.
8. **Report.** Verdict, changed files, test command and result, anything not proven.

Common pitfalls: editing a generated file; `--no-verify`; a test that passes before the fix; widening the ticket; trusting an old summary without checking the code.

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
