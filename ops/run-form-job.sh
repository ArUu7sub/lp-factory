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
trap 'rm -f "$prompt_file"' EXIT

cat "$factory_root/pipeline/run-job.md" > "$prompt_file"
cat >> "$prompt_file" <<EOF

Runtime values:
- TARGET_WORKSPACE: $target_workspace
- JOB_FILE: $job_file
- OUTPUT_DIR: $output_dir
EOF

codex --search -a never exec \
  --ephemeral \
  --sandbox workspace-write \
  --ignore-rules \
  --color never \
  -C "$factory_root" \
  --add-dir "$target_workspace" \
  --output-last-message "$target_workspace/automation/jobs/codex-output.md" \
  - < "$prompt_file"

python3 "$factory_root/.agents/skills/lp-production-pipeline/scripts/validate_run.py" \
  "$job_file" "$target_workspace"

