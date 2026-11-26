# Building MCP servers

- MCP-1: Scope palettes decide which tools exist. Add a tool only for a scope that needs it.
- MCP-2: No publish tool and no delete tool unless the project says so. Agents write drafts; people publish.
- MCP-3: Tool descriptions teach the model: terse and exact. They are generated from the project docs where the project has a generator; keep the drift tests green.
- MCP-4: Count the token cost of each tool output. Return the least the caller needs.
- MCP-5: Validate every tool input at the boundary. A tool error names the fix.
- MCP-6: Resources for read-only reference material; tools for actions.
