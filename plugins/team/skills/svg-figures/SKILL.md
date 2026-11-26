---
name: svg-figures
description: Rules and a verifier for themed SVG figures used in slides, guides and docs - site tokens only, standard viewBoxes, text caps and floors, no forbidden elements. Use before drawing or reviewing any SVG figure.
---

# SVG figures

Read before you draw. The project design reference wins on conflict (its tokens, its sizes). Verify every file:

```bash
python3 -I <skill-dir>/verify_svg.py <figure.svg>
```

`<skill-dir>` is the base directory shown when this skill loads. Exit 0 is a pass; fix every error.

## 1. Colour

1. Site tokens only, never hex, rgb or a named colour: `var(--foreground)` text and strokes; `var(--muted-foreground)` notes; `var(--primary)` accent; `var(--border)` lines; `var(--muted)` box fills; `var(--background)` ground; `var(--card)` panels; `var(--destructive)` errors.
2. Write a fallback: `var(--primary, #d9d047)`, shown only when the SVG loads as an image.
3. Declare no tokens: no `:root`, `html`, `body` or `*` rule.
4. `currentColor` for icons that take the text colour.
5. Never rely on a fixed light or dark look.

## 2. Structure

6. One root `<svg>` with a `viewBox` and a `<title>` (and `<desc>` when needed). No `width` or `height`.
7. One `<style>` block with plain class selectors, or presentation attributes.
8. `font-family: var(--font-sans)` or `var(--font-mono)` only. No `@font-face`.
9. Under 200 KB, 5,000 elements and 20 levels.

## 3. Animation

10. `@keyframes` and SMIL may change `fill`, `stroke`, `opacity`, `stroke-dashoffset`, `transform`. Always add `@media (prefers-reduced-motion: reduce) { * { animation: none } }`.
11. Do not animate `href`, `class`, `id`, `style` or position properties.

## 4. Forbidden

12. `<script>`, `<foreignObject>`, `on*` handlers, `javascript:` and `data:` links.
13. External resources: no `http(s)` in `href`, `url()`, `@import`, `<image>`, `<use>`, fonts.
14. `url()` only for same-file fragments.
15. No `class`, `id`, `role`, `data-*` or `aria-*` aimed at the host page.
16. No `position: fixed`, no `z-index`, no selector starting with `+` or `~`.

## 4b. Output

17. Give the figure alt text: its accessible name.
18. Transparent ground: no opaque background rect.
19. Text contrast at least 4.5:1 in both themes; nothing clipped at 2480 px or 375 px wide.

## 5. Size and viewBox

20. Default `viewBox="0 0 1600 900"` (16:9).
21. Other shapes, all 900 high: pipeline 2100 x 900, single focus 1200 x 900, icon 900 x 900.
22. Crop to the content plus 16 units at most. `preserveAspectRatio="xMidYMid meet"`.
23. No `width` or `height` attributes.

## 6. Space

24. Outer padding 16 units at most. Gaps between groups 24 units at least, in multiples of 8.
25. Inside a box: padding 12 units.
26. Key content stays in the central 90 percent.

## 7. Text

27. 8 text items at most, 4 words a label, no sentences.
28. Three sizes: title 44, label 30, note 24 units. Never below 24.
29. Foreground for labels, muted-foreground for notes, primary for the one thing to look at.
30. Text width = characters x font-size x 0.55 (sans) or 0.62 (mono). The box is that plus 24 units at least.
31. `text-anchor="middle"` for labels, `start` for lists. One line a label.
32. 16 units free around every text item. Where text must cross a line, add a halo: `paint-order="stroke" stroke="var(--background)" stroke-width="8"`.
33. One focal point, one animated flow at most.

## 8. Minimal graphics

34. Stroke 4 units for lines, 6 for the focal element, 3 at least. Icons 64 units at least.
35. Six colour roles at most. No gradient, shadow or filter.
36. Prefer shapes and icons to text.

## 9. Verify before delivery

37. Render in a browser at 1600 x 900 and 540 x 304, light and dark, when a browser is available.
38. No two `<text>` elements intersect; each sits inside its container minus 12 units.
39. Report `viewBox`, text item count, smallest font size and the verifier status.
