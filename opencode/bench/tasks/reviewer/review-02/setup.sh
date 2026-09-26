#!/usr/bin/env bash
set -euo pipefail
run_dir="$1"
task_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cp "$task_dir/REVIEW_TARGET.diff" "$run_dir/REVIEW_TARGET.diff"
