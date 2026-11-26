# TypeScript and JavaScript

For backend and frontend TS/JS. The project names its runtime (Bun or Node) and its validation library.

## CV: conventions

- CV-1: Native ESM only. `"type": "module"`. No CommonJS.
- CV-2: Named exports. Framework files that need a default export are the exception (routes, components, config).
- CV-3: Runtime built-ins first (Bun-native in a Bun project). `node:*` only where the runtime has no equivalent.
- CV-4: Workspace imports stay extensionless. Never add `.ts` to fix resolution.
- CV-5: `const` over `let`. Never `var`.
- CV-6: `.map`, `.filter`, `.reduce` over imperative loops.
- CV-7: No `class`, no `this`. Factory and arrow functions.
- CV-8: No `switch`. Object-literal dispatch. A long `if`/`else if` chain counts as one.
- CV-9: Functions under about 20 lines. Compose small pure functions.
- CV-10: Fail loudly. A `catch` logs, rethrows, or returns a checked value, with a comment saying which.
- CV-11: No stubs, no TODO markers for core behaviour. Build X means X works end to end.
- CV-12: Comments say why, not what. Match the density of the file.
- CV-13: Read a file before editing it. Fix the cause, never the symptom.
- CV-14: Validate external and contract data with a schema (Zod by default) at every boundary.
- CV-15: Untrusted content reaches the DOM only through the project's sanitizer.
- CV-16: Strict TypeScript. No `any` without a comment saying why. `tsc` is the static check; the project may add one linter.
