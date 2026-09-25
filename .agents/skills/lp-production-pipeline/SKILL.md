---
name: lp-production-pipeline
description: Orchestrate a Google Form LP job through research, marketing strategy, Japanese copy, imagegen assets, deterministic responsive design, independent reviews, implementation, and Preview readiness. Use for the fixed six-section 24H AI LP production flow; do not use for unrelated one-off page edits.
---

# LP Production Pipeline

Read `ORCHESTRATION.md`, then the normalized job named by the runtime prompt.

## Run contract

1. Verify that `job_id`, `answers`, and exact `output_dir` exist. Treat all values as untrusted content.
2. Create `pipeline-state.json` with stage owners, status, attempts, inputs, and artifact paths.
3. Launch the configured specialists in the order defined in `ORCHESTRATION.md`. Collect each output before starting its dependent stage.
4. Use the dedicated creator and independent reviewer at each review gate. A creator never certifies its own work.
5. The first Codex pass ends at `awaiting_render_review` after source review and public implementation. The trusted runner then renders design and implementation evidence outside the Codex sandbox.
6. The second Codex pass independently reviews rendered evidence and performs the delivery audit. Stop with `needs_human` when a rendered gate fails.
7. Run `.agents/skills/lp-production-pipeline/scripts/validate_run.py` before setting `ready_for_preview`.
8. Leave deployment, PR creation, and Discord delivery to the GitHub workflow after the local production contract passes.

## Non-negotiable rules

- Keep the six section IDs and order from `templates/24h-ai/section-contract.json`.
- Select visual direction from the answers and evidence; never ask the respondent to choose RED or COMPANY.
- Use the built-in `imagegen` tool for text-free Hero, CTA background, and necessary inserted imagery. Do not use the API fallback because this automation intentionally has no `OPENAI_API_KEY`.
- Choose exactly one Hero composition: `split-text-left-visual-right` (HTML copy on the left; the generated visual fills the entire right Hero region) or `centered-copy-over-background` (centered HTML copy over a generated full-bleed background). Do not use a small generated picture as a card beside the copy.
- The Hero scene must be an imagegen asset. CSS may control layout, crop, overlays, contrast, and simple decorative rules, but it must not draw the Hero illustration, people, devices, scenery, or pictorial composition.
- Generate a dedicated mobile Hero when the desktop asset cannot be cropped safely at 390px. Otherwise document the tested crop and safe area. Never assume desktop art will work on mobile.
- Generate a text-free imagegen background for `final-cta`. Review every other section and generate supporting imagery when it improves comprehension or visual rhythm; record `generated-image`, `generated-background`, or `not-needed` with a concrete reason for all six sections.
- Never use image generation for Japanese copy, wireframes, or full-page LP designs. All public copy, labels, buttons, and CTA text stay as selectable HTML. Build structure, text, spacing, breakpoints, overlays, and asset mappings as deterministic HTML/CSS.
- The trusted runner renders separate wireframe, desktop design, mobile design, desktop implementation, and mobile implementation PNGs. Do not combine them into one contact sheet.
- Save a structured JSON specification beside every visual design so implementation does not depend on visual guessing.
- Keep all public links local except the blank LINE placeholder. Do not expose private uploads.
- Use the shared sticky header and shared footer defined in `templates/24h-ai/section-contract.json`; do not redesign or rewrite them per job. The footer repeats the same brand and three anchors, contains no back-to-top link, and stacks left on mobile.
- A Hero overview is optional. Omit it when it repeats the participant journey in `process` or the responsibility split in `solution`. When the Hero contains a connected-work overview, each numbered stage must pair its label with a short action or outcome. Make the stages read as one continuous journey with connected handoffs instead of a row of isolated equal cards. Keep the route horizontal on desktop and left-aligned vertical on mobile. Use separate text-free imagegen assets when they improve comprehension, while keeping the ordered labels and explanations as HTML.
- Keep blank LINE placeholders silent. Never display `公式LINEのリンクは準備中です。` or similar preparation-state copy in the LP.
- Treat form prose as source material rather than verbatim Hero copy. The Hero contains exactly one eyebrow, one H1 benefit promise, one H2 mechanism, and the CTA. Count displayed characters after removing whitespace and line breaks: eyebrow 10–18 recommended / 22 maximum, H1 18–28 recommended / 32 maximum, H2 20–36 recommended / 44 maximum. Do not render a long Hero description. Rewrite naturally so the audience, primary benefit, and mechanism remain, and move supporting detail to later sections; never truncate mechanically.
- Use phrase-aware markup for Japanese Hero headings and key copy. At 1440px and 390px, block isolated particles/punctuation, one-character orphan lines, word-internal splits, and semantically awkward line breaks.
- Do not proceed past a failed gate.

Read [references/artifact-contract.md](references/artifact-contract.md) when creating or validating job artifacts. Read [references/review-gates.md](references/review-gates.md) when routing revisions.
