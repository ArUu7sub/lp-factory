# Review gates

## Creative gate

Check that all six sections exist, information priority matches the marketing brief, Japanese text remains readable, whitespace is sufficient, visual style fits the intended audience, inserted assets are consistent, desktop and mobile designs agree, and the structured specification describes what the images show.

## Implementation gate

Compare approved designs with rendered screenshots at 1440px and 390px. Check section order, copy, image crop, typography, spacing, colors, boundaries, responsive behavior, focus visibility, contrast, missing assets, console errors, horizontal overflow, and private-data exposure.

## Routing

- Strategy or claim issue: `lp-marketing-strategist`
- Copy issue: `lp-copywriter`
- Wireframe, asset, or visual issue: `lp-imagegen-designer`
- HTML/CSS/JS or rendered mismatch: `lp-frontend-builder`
- Missing evidence or exhausted retries: root orchestrator sets `needs_human`

