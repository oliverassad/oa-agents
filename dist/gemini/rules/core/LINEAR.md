# LINEAR: the ticket contract

Write each ticket so an agent with no tribal knowledge can execute it without asking. Team and project: `## Tracker` in the project `AGENTS.md` (BOOT TK-2).

## LN: rules

- LN-1: Every change starts from a ticket. No ticket, no branch.
- LN-2: A ticket carries all eight sections below.
- LN-3: The Description states the current state with real paths, file names and numbers, and names the files the ticket owns.
- LN-4: The Definition of Done is checkboxes, each checkable by a command or by looking at a file.
- LN-5: Testing Scenarios are numbered; each proves one line of the Definition of Done.
- LN-6: Review / Results starts as a placeholder and is filled on completion with evidence: command output, counts, links. A claim is not evidence.
- LN-7: Name the traps. An unrecorded trap costs the next agent the same hour.
- LN-8: Ticket bodies are normal prose (STYLE CM-6). No secret value: name the variable, never its value.
- LN-9: One ticket is one unit of work. Split rather than widen.
- LN-10: A ticket with a user interface needs a design reference: a print path, a screenshot, or an explicit "None". Such a ticket carries an evidence gate in its Definition of Done (fidelity probe at a named viewport in both themes, the end-to-end journey, the artefacts) and cannot reach In Review without it.
- LN-11: Writing to Linear is outward-facing (GIT GS-5), except creating the operator's own ticket and setting it In Progress.
- LN-12: Move the status as the work moves. Merged work is never left In Review.

## The eight sections

1. **Description**: context, current state, what to build, the files the ticket owns, the traps.
2. **Definition of Done**: checkboxes.
3. **Expected Outcome**: the demoable result, one or two sentences.
4. **Testing Scenarios**: numbered, each proving one Definition of Done line.
5. **Review / Results**: placeholder until done, then evidence and anything deferred.
6. **Dependencies**: tickets that must land first, and why.
7. **Copy policy**: what may be lifted from older code, what is written fresh.
8. **Design**: the design reference, or "None".

## Status

| Event | Status |
| --- | --- |
| Ticket created, not started | Backlog |
| The agent starts the ticket | In Progress |
| Its pull request is open | In Review |
| Its pull request is merged | Done |

Whoever hands out a ticket sets In Progress and moves it when the agent lands: a subagent may lack Linear.

## Milestones

A milestone description has four parts: **Working unit**, **Must land**, **Demo**, **Design** (references or "None"). Work fans out inside a milestone where dependencies allow. Do not start the next milestone before the current demo is green.
