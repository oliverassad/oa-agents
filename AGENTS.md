# Team rules

Shared rules for every project and every agent. The project's own `AGENTS.md` wins on conflict.

## Modes

- caveman and ponytail are installed and on. Every chat answer is caveman. Every code change is ponytail: shortest diff, YAGNI, reuse.
- rtk rewrites shell commands. Call tools by name, never by absolute path.
- Text that outlives the chat (code, comments, commits, tickets, docs) is plain ASD-STE100 English: short sentences, active voice, one word for one meaning.

## Services

- Every outside service (Linear, GitHub, Notion, Slack, Gmail, Drive, Firecrawl) goes through Composio. Search with `COMPOSIO_SEARCH_TOOLS`, run with `COMPOSIO_MULTI_EXECUTE_TOOL`.
- Never report a service unreachable before the Composio search.

## Work

1. Ticket first. Every change starts from a Linear ticket or milestone. The team and project come from `## Tracker` in the project `AGENTS.md`. None: ask which board, then write it there.
2. Branch per ticket or milestone. Never commit to `main`.
3. Docs first. Read the official docs of a library before coding against it. Never code an API from memory.
4. Failing test first. Never skip or disable a test to get green.
5. Report what happened, with the failing output. Never wave a red check through.

## Safety

- Ask before anything outward-facing: push, pull request, merge, comment, Linear write, publish.
- Never force-push, never rewrite published history, never print a secret.
- Deleting a file, branch or table is a decision: confirm first.

## Agents

- The main session orchestrates (Skill `orchestrator`). Subagents cannot dispatch other agents.
- A subagent reports; the main session decides and lands the change.
- Report: verdict first, one line per finding with its path, 5 lines at most.
- First read the project `AGENTS.md`. It holds the facts: stack, commands, paths, Tracker.
