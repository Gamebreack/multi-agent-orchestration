#!/usr/bin/env bash
# Passes iff: tests/ is untouched AND the full suite passes.
set -euo pipefail
run_dir="$1"
task_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fixture_tests="$task_dir/../../../fixture/tests"

mismatch=0
for f in "$fixture_tests"/*.py; do
  name="$(basename "$f")"
  if ! cmp -s "$f" "$run_dir/tests/$name"; then
    mismatch=1
  fi
done

if [ "$mismatch" -ne 0 ]; then
  echo '{"score": 0.0, "detail": "test files were modified"}'
  exit 1
fi

out_file="$(mktemp)"
trap 'rm -f "$out_file"' EXIT

if (cd "$run_dir" && python3 -m unittest discover -s tests -q) >"$out_file" 2>&1; then
  echo '{"score": 1.0, "detail": "suite passes, tests unmodified"}'
  exit 0
else
  echo '{"score": 0.0, "detail": "suite still failing"}'
  exit 1
fi
