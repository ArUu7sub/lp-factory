# 24H AI LP production orchestration

This repository controls repeatable LP production. The published page remains in the target repository; this factory stores reusable agents, stage contracts, validators, and operating guidance.

## Trigger and boundary

```text
Google Form submit
  -> Apps Script installed onFormSubmit trigger
  -> GitHub repository_dispatch: lp_form_submitted
  -> Windows-hosted WSL self-hosted runner
  -> Codex CLI root orchestrator
  -> specialist agents and review gates
  -> Draft PR
  -> Vercel Preview
  -> Discord notification after Preview succeeds
```

Selecting a dropdown or moving to the next Google Form section does not start production. A completed form submission starts it.

`vault` is the knowledge system, `lp-factory` is the production controller, and `line-harness-auto-webinar-lp` is the publication repository. Do not mix their responsibilities.

## Specialist stages

| Stage | Direct specialist | Required output | Next gate |
|---|---|---|---|
| Intake validation | root orchestrator | `pipeline-state.json` | research |
| Reference research | `lp-reference-researcher` | `research/references.md` | strategy |
| Marketing design | `lp-marketing-strategist` | `strategy/marketing-brief.md` | copy |
| Writing | `lp-copywriter` | `content/lp-copy.json` | visual production |
| Wireframe, inserted images, full design | `lp-imagegen-designer` | wireframe, assets, desktop/mobile design and specs | creative review |
| Creative review | `lp-creative-reviewer` | `reviews/creative-review.json` | implementation or visual revision |
| Frontend implementation | `lp-frontend-builder` | HTML/CSS/JS and desktop/mobile screenshots | implementation review |
| Design/code review | `lp-design-reviewer` | `reviews/implementation-review.json` | code revision or delivery |
| Delivery audit | `lp-delivery-auditor` | final state and evidence check | Preview readiness |

The root orchestrator owns ordering, handoffs, retry counts, state updates, and the final evidence summary. It does not certify its own work.

## Stage sequence

1. Validate the normalized job and create the output structure.
2. Research current public references relevant to the audience, industry, desired tone, and supplied references. Use `references/lp-research-sources.md` as the standard Japanese LP gallery list, select direct example pages, and record URLs, observed patterns, dates, and how each reference may influence the LP without copying it.
3. Define audience, problem priority, value proposition, proof boundaries, message hierarchy, objections, and the role of each fixed section.
4. Write concise Japanese copy for all six sections. Keep unverified claims out of public copy.
5. Use the built-in `imagegen` path to create:
   - a full-page wireframe image and a structured wireframe specification;
   - section-specific inserted images listed in an asset manifest;
   - a desktop full-page design and a mobile full-page design;
   - a structured design specification with colors, typography, spacing, dimensions, and responsive behavior.
6. Have the independent creative reviewer return `PASS` or `FAIL`. On `FAIL`, send the findings back to the visual owner and review again.
7. After creative `PASS`, implement from `hero` downward, using the approved copy, design specification, and generated assets. Generate an additional image only when the approved design requires one and the manifest proves it is missing.
8. Render and save desktop and mobile screenshots.
9. Have the independent design reviewer compare approved designs against screenshots and verify responsiveness, accessibility, links, and asset loading. On `FAIL`, return findings to the frontend owner and review again.
10. Mark `ready_for_preview` only after both gates pass. GitHub Actions then creates or updates a Draft PR. Vercel creates a Preview; a deployment-status workflow sends the Discord notice.

## Review rules

- Reviews use `schemas/review.schema.json`.
- Reviewers must use observed evidence and name exact files or screen areas.
- `PASS` means no blocking issue remains. Minor optional ideas belong in `notes` and do not become silent production changes.
- `FAIL` must name the owner and concrete fixes.
- Maximum three attempts per gate. Exceeding it produces `needs_human`.
- A changed upstream artifact invalidates dependent downstream stages.

## Required output tree

```text
generated/<job-id>/
├── index.html
├── styles.css
├── script.js
├── content.json
├── review.md
├── pipeline-state.json
├── research/references.md
├── strategy/marketing-brief.md
├── content/lp-copy.json
├── design/wireframe.png
├── design/wireframe-spec.json
├── design/desktop.png
├── design/mobile.png
├── design/design-spec.json
├── design/assets-manifest.json
├── assets/generated/
├── implementation/screenshots/desktop.png
├── implementation/screenshots/mobile.png
└── reviews/
    ├── creative-review.json
    └── implementation-review.json
```

## Delivery boundary

Automation may create a Draft PR, Vercel Preview, and Discord notification. It must not merge the PR or create a production deployment. The person reviewing the Preview supplies the final official LINE URL and authorizes publication separately.
