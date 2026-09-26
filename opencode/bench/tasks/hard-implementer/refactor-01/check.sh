#!/usr/bin/env bash
# Overwrites tests/{test_storage,test_ledger,test_cli}.py with the original
# class-based Storage tests (hidden ground truth), then runs the full suite.
# Also reports how many of the 3 core files the model actually changed.
set -euo pipefail
run_dir="$1"
task_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

changed=0
for f in inventory/storage.py inventory/ledger.py inventory/cli.py; do
  if ! cmp -s "$task_dir/planted/$f" "$run_dir/$f"; then
    changed=$((changed + 1))
  fi
done

cp "$task_dir/hidden_tests/test_storage.py" "$run_dir/tests/test_storage.py"
cp "$task_dir/hidden_tests/test_ledger.py" "$run_dir/tests/test_ledger.py"
cp "$task_dir/hidden_tests/test_cli.py" "$run_dir/tests/test_cli.py"

out_file="$(mktemp)"
trap 'rm -f "$out_file"' EXIT

if (cd "$run_dir" && python3 -m unittest discover -s tests -q) >"$out_file" 2>&1; then
  echo "{\"score\": 1.0, \"detail\": \"suite passes after refactor; ${changed} of 3 core files changed\"}"
  exit 0
else
  echo "{\"score\": 0.0, \"detail\": \"suite failing after refactor; ${changed} of 3 core files changed\"}"
  exit 1
fi
