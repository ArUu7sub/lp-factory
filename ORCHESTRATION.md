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
| Wireframe, imagegen assets, full design source | `lp-imagegen-designer` | text-free Hero/CTA/section assets, deterministic HTML/CSS design source and specs | source creative review |
| Source creative review | `lp-creative-reviewer` | `reviews/creative-source-review.json` | implementation or visual revision |
| Frontend implementation | `lp-frontend-builder` | HTML/CSS/JS promoted from approved design source | trusted render |
| Trusted render | runner shell outside Codex sandbox | design PNGs, implementation screenshots, render evidence | rendered reviews |
| Rendered creative review | `lp-creative-reviewer` | `reviews/creative-review.json` | implementation review |
| Design/code review | `lp-design-reviewer` | `reviews/implementation-review.json` | delivery |
| Delivery audit | `lp-delivery-auditor` | final state and evidence check | Preview readiness |

The root orchestrator owns ordering, handoffs, retry counts, state updates, and the final evidence summary. It does not certify its own work.

## Stage sequence

1. Validate the normalized job and create the output structure.
2. Research current public references relevant to the audience, industry, desired tone, and supplied references. Use `references/lp-research-sources.md` as the standard Japanese LP gallery list, select direct example pages, and record URLs, observed patterns, dates, and how each reference may influence the LP without copying it.
3. Define audience, problem priority, value proposition, proof boundaries, message hierarchy, objections, and the role of each fixed section.
4. Write concise Japanese copy for all six sections. Keep unverified claims out of public copy.
5. Plan the visual assets before building the design. The Hero must use one of two layouts: (a) HTML copy on the left with a full-bleed imagegen visual filling the right side, or (b) centered HTML copy over a full-bleed imagegen background. The Hero scene itself must be generated with built-in `imagegen`; do not draw the scene, people, devices, or pictorial illustration in CSS. Generate a separate mobile Hero when a responsive crop cannot preserve the subject, contrast, and text-safe area. Generate a text-free imagegen background for `final-cta`, and decide for every other section whether a supporting image or background is needed. Record the decision and rationale in `design/assets-manifest.json`. Build the wireframe and full responsive design as local HTML/CSS with exact approved Japanese copy over the real assets. All headings, body copy, labels, buttons, and CTA text remain selectable HTML; generated images contain no copy. Save structured specs for colors, typography, spacing, dimensions, crop positions, overlays, safe areas, mappings, and responsive behavior.
6. Have the independent creative reviewer inspect the deterministic design source and return `PASS` or `FAIL` in `creative-source-review.json`. On `FAIL`, send the findings back to the visual owner and review again.
7. After source creative `PASS`, promote the approved prototype from `hero` downward into public HTML/CSS/JS. Do not launch a browser in the Codex sandbox. Set the job to `awaiting_render_review`.
8. The trusted runner renders the wireframe, desktop/mobile design, and desktop/mobile implementation screenshots outside the Codex sandbox, and records console, request, section-order, and overflow evidence.
9. A second Codex pass has the independent creative reviewer inspect the rendered design, then the independent design reviewer compare approved designs against implementation screenshots. The delivery auditor verifies the whole evidence set.
10. Mark `ready_for_preview` only after source creative, rendered creative, and implementation gates pass. GitHub Actions then creates or updates a Draft PR. Vercel creates a Preview; a deployment-status workflow sends the Discord notice.

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
├── design/wireframe.html
├── design/wireframe.png
├── design/wireframe-spec.json
├── design/prototype/index.html
├── design/prototype/styles.css
├── design/desktop.png
├── design/mobile.png
├── design/design-spec.json
├── design/assets-manifest.json
├── assets/generated/
├── implementation/screenshots/desktop.png
├── implementation/screenshots/mobile.png
├── implementation/render-evidence.json
└── reviews/
    ├── creative-source-review.json
    ├── creative-review.json
    └── implementation-review.json
```

## Delivery boundary

Automation may create a Draft PR, Vercel Preview, and Discord notification. It must not merge the PR or create a production deployment. The person reviewing the Preview supplies the final official LINE URL and authorizes publication separately.
