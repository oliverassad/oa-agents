# User interface, design system and accessibility

## DS: design system

- DS-1: Every colour, size, space, radius, typeface and shadow comes from the project's design tokens.
- DS-2: In app code: no hex, `rgb()`, `oklch()`, `hsl()`, no raw `px`, `rem`, `em`, no `style=`, no bespoke `<style>`.
- DS-3: Add to the component library first, then consume. Never inline "just this once".
- DS-4: A heading uses a type role from the kit, never an ad-hoc size.
- DS-5: Build a screen 1:1 against its print (design reference). The print is the contract; a deviation is a recorded row.
- DS-6: One component, one file. A component that no print draws is not built.

## AX: accessibility

- AX-1: Every interactive element shows a focus ring on `:focus-visible`, drawn once in the token layer.
- AX-2: State is never shown by colour alone.
- AX-3: Labels, focus order, contrast at least 4.5:1 in both themes.
- AX-4: What the automatic check cannot see is checked by hand and recorded in the pull request.

## Evidence

- UI-1: Every library component carries a story beside it. A story is a test: headless, drives the component, checks accessibility.
- UI-2: A route a person walks carries an end-to-end spec. A story does not prove a screen.
- UI-3: A ticket with a print carries a fidelity probe at a named viewport in both themes. A string match on a source file is not a probe.
- UI-4: Surface evidence is an artefact (screenshot pair, viewport, command output) in Review / Results.
