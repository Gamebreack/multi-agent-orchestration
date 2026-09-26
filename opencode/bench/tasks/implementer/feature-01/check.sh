#!/usr/bin/env bash
# Copies the hidden feature test into the run dir and runs the full suite.
set -euo pipefail
run_dir="$1"
task_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cp "$task_dir/hidden_tests/test_feature_markdown.py" "$run_dir/tests/test_feature_markdown.py"

out_file="$(mktemp)"
trap 'rm -f "$out_file"' EXIT

if (cd "$run_dir" && python3 -m unittest discover -s tests -q) >"$out_file" 2>&1; then
  echo '{"score": 1.0, "detail": "markdown formatter implemented, full suite passes"}'
  exit 0
else
  echo '{"score": 0.0, "detail": "suite failing after hidden markdown test added"}'
  exit 1
fi
