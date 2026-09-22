#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 TARGET_WORKSPACE JOB_FILE" >&2
  exit 2
fi

factory_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target_workspace="$(realpath "$1")"
job_file="$(realpath "$2")"

readarray -t job_values < <(python3 - "$job_file" <<'PY'
import json, sys
from pathlib import Path
job = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(job.get("job_id", ""))
print(job.get("output_dir", ""))
PY
)

job_id="${job_values[0]}"
output_rel="${job_values[1]}"
if [[ -z "$job_id" || "$output_rel" != "generated/$job_id" ]]; then
  echo "Invalid normalized job: expected output_dir generated/<job_id>" >&2
  exit 1
fi

output_dir="$target_workspace/$output_rel"
mkdir -p "$output_dir" "$target_workspace/automation/jobs"
prompt_file="$(mktemp)"
review_prompt_file="$(mktemp)"
diagnostic_dir="/tmp/lp-factory-diagnostics/$job_id"
diagnostic_log="$diagnostic_dir/run.log"
mkdir -p "$diagnostic_dir"

collect_diagnostics() {
  local exit_code=$?
  printf '{"job_id":"%s","github_run_id":"%s","github_job":"%s","exit_code":%d,"collected_at":"%s"}\n' \
    "$job_id" "${GITHUB_RUN_ID:-}" "${GITHUB_JOB:-}" "$exit_code" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    > "$diagnostic_dir/metadata.json"
  for relative in \
    "pipeline-state.json" \
    "review.md" \
    "reviews/creative-source-review.json" \
    "reviews/creative-review.json" \
    "reviews/implementation-review.json" \
    "implementation/render-evidence.json"
  do
    if [[ -f "$output_dir/$relative" ]]; then
      mkdir -p "$diagnostic_dir/$(dirname "$relative")"
      cp "$output_dir/$relative" "$diagnostic_dir/$relative"
    fi
  done
  for name in codex-output-production.md codex-output.md; do
    if [[ -f "$target_workspace/automation/jobs/$name" ]]; then
      cp "$target_workspace/automation/jobs/$name" "$diagnostic_dir/$name"
    fi
  done
  chmod -R a+rX "$diagnostic_dir" 2>/dev/null || true
  rm -f "$prompt_file" "$review_prompt_file"
}
trap collect_diagnostics EXIT
exec > >(tee "$diagnostic_log") 2>&1

runtime_root="${LP_BROWSER_RUNTIME_ROOT:-${HOME}/.cache/lp-factory-browser}"
bash "$factory_root/ops/ensure-browser-runtime.sh"
node_root="$runtime_root/node-v24.21.0-linux-x64"
export PATH="$node_root/bin:$PATH"
export NODE_PATH="$runtime_root/package/node_modules"
export PLAYWRIGHT_BROWSERS_PATH="$runtime_root/browsers"
export LP_JAPANESE_FONT_PATH="$runtime_root/fonts/NotoSansJP-Variable.ttf"
export LP_JAPANESE_FONT_LICENSE_PATH="$runtime_root/fonts/OFL.txt"

node - <<'NODE'
const {chromium} = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
(async () => {
  const fontPath = process.env.LP_JAPANESE_FONT_PATH;
  const checkPath = path.join(path.dirname(fontPath), 'browser-font-check.html');
  fs.writeFileSync(checkPath, '<!doctype html><meta charset="utf-8"><style>@font-face{font-family:"LP Noto Sans JP";src:url("./NotoSansJP-Variable.ttf") format("truetype");font-weight:100 900;font-style:normal;font-display:block}html,body{font-family:"LP Noto Sans JP",sans-serif}</style><p>日本語表示確認</p>');
  const browser = await chromium.launch({headless: true});
  const page = await browser.newPage({viewport: {width: 390, height: 844}});
  await page.goto(pathToFileURL(checkPath).href, {waitUntil: 'load'});
  await page.evaluate(() => document.fonts.ready);
  const japaneseFontReady = await page.evaluate(() => document.fonts.check('16px "LP Noto Sans JP"', '日本語表示確認'));
  if (!japaneseFontReady) throw new Error('Japanese font failed to load in Chromium.');
  await browser.close();
  console.log('LP browser runtime and Japanese font launch check passed.');
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
NODE

cat "$factory_root/pipeline/run-job.md" > "$prompt_file"
cat >> "$prompt_file" <<EOF

Runtime values:
- TARGET_WORKSPACE: $target_workspace
- JOB_FILE: $job_file
- OUTPUT_DIR: $output_dir
- BROWSER_RUNTIME: Playwright is preinstalled and verified. Use node with require('playwright'); do not install another browser package.
- PLAYWRIGHT_BROWSERS_PATH: $PLAYWRIGHT_BROWSERS_PATH
EOF

codex --search -a never exec \
  --ephemeral \
  --sandbox workspace-write \
  --ignore-rules \
  --color never \
  -C "$factory_root" \
  --add-dir "$target_workspace" \
  --output-last-message "$target_workspace/automation/jobs/codex-output-production.md" \
  - < "$prompt_file"

python3 "$factory_root/.agents/skills/lp-production-pipeline/scripts/validate_pre_render.py" \
  "$job_file" "$target_workspace"

node "$factory_root/ops/capture-lp.cjs" "$output_dir"

cat "$factory_root/pipeline/review-rendered.md" > "$review_prompt_file"
cat >> "$review_prompt_file" <<EOF

Runtime values:
- TARGET_WORKSPACE: $target_workspace
- JOB_FILE: $job_file
- OUTPUT_DIR: $output_dir
- RENDER_EVIDENCE: $output_dir/implementation/render-evidence.json
EOF

codex --search -a never exec \
  --ephemeral \
  --sandbox workspace-write \
  --ignore-rules \
  --color never \
  -C "$factory_root" \
  --add-dir "$target_workspace" \
  --output-last-message "$target_workspace/automation/jobs/codex-output.md" \
  - < "$review_prompt_file"

python3 - "$output_dir/review.md" <<'PY'
from pathlib import Path
import sys

review_path = Path(sys.argv[1])
if review_path.is_file():
    review = review_path.read_text(encoding="utf-8")
    marker = "APPROVAL_STATUS: pending"
    if marker not in review:
        review_path.write_text(f"{marker}\n\n{review}", encoding="utf-8")
PY

python3 "$factory_root/.agents/skills/lp-production-pipeline/scripts/validate_run.py" \
  "$job_file" "$target_workspace"
