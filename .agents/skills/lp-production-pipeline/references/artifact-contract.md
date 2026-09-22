# Artifact contract

All paths are relative to the exact output directory.

| Stage | Required artifacts |
|---|---|
| Intake | `pipeline-state.json` |
| Research | `research/references.md` |
| Strategy | `strategy/marketing-brief.md` |
| Copy | `content/lp-copy.json` |
| Visual | `design/wireframe.png`, `design/wireframe-spec.json`, `design/assets-manifest.json`, `design/desktop.png`, `design/mobile.png`, `design/design-spec.json`, assets under `assets/generated/` |
| Creative gate | `reviews/creative-review.json` |
| Implementation | `index.html`, `styles.css`, `script.js`, `content.json`, `review.md`, `implementation/screenshots/desktop.png`, `implementation/screenshots/mobile.png` |
| Implementation gate | `reviews/implementation-review.json` |

`pipeline-state.json` must contain the job ID, `status`, timestamps, and a `stages` object. Each stage records `owner`, `status`, `attempts`, `inputs`, and `outputs`. Allowed stage status values are `pending`, `running`, `pass`, `fail`, `blocked`, and `invalidated`. Job status values are `running`, `needs_human`, `ready_for_preview`, and `failed`.

The desktop design targets 1440px width. The mobile design targets 390px width. Screenshots must use the same viewport widths so the reviewer can compare them.

