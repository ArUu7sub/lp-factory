# Review gates

## Creative gate

The source review checks all six sections, exact approved copy, semantic hierarchy, CSS type sizes and spacing, responsive one-column mobile behavior, intended audience fit, actual asset mappings, the fixed shared header, silent blank LINE placeholders, and agreement between the deterministic source and its structured specification. It also blocks any Hero outside the two approved modes, CSS-built Hero illustration, embedded copy inside generated images, a card-sized Hero visual, missing mobile crop evidence, reuse of the Hero as the CTA image, a missing CTA background, an unexplained section asset decision, or public preparation-state copy. After trusted rendering, the rendered creative review confirms that desktop and mobile PNGs visually match those claims. At 1440px and 390px it must block one-character orphan lines, isolated particles or punctuation, word-internal splits, and meaning units separated by awkward line breaks.

## Implementation gate

Compare approved deterministic design renders with public implementation screenshots at 1440px and 390px. Check section order, copy, fixed header, silent LINE placeholder behavior, phrase-aware Japanese line endings, Hero mode, exact desktop/mobile asset selection, image crop, CTA background, typography, spacing, colors, boundaries, responsive behavior, focus visibility, contrast, missing assets, console errors, horizontal overflow, and private-data exposure. Use implementation/render-evidence.json as browser evidence.

## Routing

- Strategy or claim issue: `lp-marketing-strategist`
- Copy issue: `lp-copywriter`
- Wireframe, asset, or visual issue: `lp-imagegen-designer`
- HTML/CSS/JS or rendered mismatch: `lp-frontend-builder`
- Missing evidence or exhausted retries: root orchestrator sets `needs_human`
