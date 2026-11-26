# Svelte and SvelteKit

- SV-1: Svelte 5 runes only (`$state` `$derived` `$effect` `$props` `$bindable`). No `export let`, no `$:`.
- SV-2: Secrets and authentication are server-only. Nothing secret reaches a `.svelte` file.
- SV-3: A heavy client view gates its client work behind `onMount`.
- SV-4: In a Bun project, Vite runs under Bun: every dev script carries `--bun`.
- SV-5: One component, one file. A part used only inside its parent is a snippet.
