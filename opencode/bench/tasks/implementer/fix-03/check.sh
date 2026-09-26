#!/usr/bin/env bash
# Passes (score 1.0) iff: tests/ is untouched, the full suite passes, AND
# the only inventory/*.py file that differs from the fixture is the
# root-cause file (storage.py). If the suite passes but some other file
# (typically ledger.py or cli.py) was also/instead patched, that's a
# symptom fix rather than a root-cause fix -- scored 0.5. Anything else
# (suite still failing, or tests/ modified) scores 0.0.
set -euo pipefail
run_dir="$1"
task_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fixture_dir="$task_dir/../../../fixture"

mismatch=0
for f in "$fixture_dir"/tests/*.py; do
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
if ! (cd "$run_dir" && python3 -m unittest discover -s tests -q) >"$out_file" 2>&1; then
  echo '{"score": 0.0, "detail": "suite still failing"}'
  exit 1
fi

other_changed=0
for f in cli.py ledger.py models.py plugins.py report.py validation.py; do
  if ! cmp -s "$fixture_dir/inventory/$f" "$run_dir/inventory/$f"; then
    other_changed=1
  fi
done

if [ "$other_changed" -eq 0 ]; then
  echo '{"score": 1.0, "detail": "suite passes; only the root-cause file (storage.py) was changed"}'
  exit 0
else
  echo '{"score": 0.5, "detail": "suite passes, but a non-root-cause file was also patched (symptom fix)"}'
  exit 1
fi
