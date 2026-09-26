#!/usr/bin/env bash
set -euo pipefail
run_dir="$1"
task_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$task_dir/grade.py" "$run_dir/.bench/response.md"
