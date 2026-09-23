# Artifact contract

All paths are relative to the exact output directory.

| Stage | Required artifacts |
|---|---|
| Intake | `pipeline-state.json` |
| Research | `research/references.md` |
| Strategy | `strategy/marketing-brief.md` |
| Copy | `content/lp-copy.json` |
| Visual source | `design/wireframe.html`, `design/prototype/index.html`, `design/prototype/styles.css`, `design/wireframe-spec.json`, `design/assets-manifest.json`, `design/design-spec.json`, assets under `assets/generated/` |
| Source creative gate | `reviews/creative-source-review.json` |
| Implementation source | `index.html`, `styles.css`, `script.js`, `content.json` |
| Trusted runner render | `assets/fonts/NotoSansJP-Variable.ttf`, `assets/fonts/OFL.txt`, `design/wireframe.png`, `design/desktop.png`, `design/mobile.png`, `implementation/screenshots/desktop.png`, `implementation/screenshots/mobile.png`, `implementation/render-evidence.json` |
| Rendered creative gate | `reviews/creative-review.json` |
| Implementation gate | `reviews/implementation-review.json` |
| Delivery | `review.md` and `pipeline-state.json` with `ready_for_preview` |

`pipeline-state.json` must contain the job ID, `status`, timestamps, and a `stages` object. Each stage records `owner`, `status`, `attempts`, `inputs`, and `outputs`. Allowed stage status values are `pending`, `running`, `pass`, `fail`, `blocked`, and `invalidated`. Job status values are `running`, `awaiting_render_review`, `needs_human`, `ready_for_preview`, and `failed`.

`design/assets-manifest.json` uses schema `2.0` and `visual_policy_version: 2`. It must record:

- Hero layout: `split-text-left-visual-right` or `centered-copy-over-background`;
- desktop Hero asset ID;
- mobile strategy: `responsive-crop` with a tested crop reason, or `dedicated-asset` with a mobile asset ID;
- a separate `final-cta` background asset ID;
- an asset decision and rationale for every fixed section;
- one record per generated file with path, dimensions, checksum, imagegen generator, prompt, text-free and no-embedded-copy flags, safe area, crop behavior, and usage;
- design and public paths for every mapped asset.

The Hero and CTA images are visual layers only. Japanese copy, headings, labels, buttons, and CTA text must remain in HTML. CSS may place and crop assets and add contrast overlays, but must not construct pictorial Hero art.

The desktop design targets 1440px width. The mobile design targets 390px width. The trusted renderer uses the same viewport widths for design and implementation so the reviewer can compare them directly. It checksum-verifies and bundles Noto Sans JP, waits for `document.fonts.ready`, and records both font readiness and the computed body font family for every capture.
