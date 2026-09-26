#!/usr/bin/env bash
# 1. tests/ must be untouched.
# 2. The existing (unmodified) suite must still pass -- behavior-preserving
#    is mandatory; if it regressed, score 0.0 regardless of the feature.
# 3. Each of the 3 hidden test files (storage/ledger/cli layers) is run in
#    isolation; score = (number of layers whose hidden tests all pass) / 3.
#    pass requires score >= 0.9, i.e. all 3 layers.
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
  echo '{"score": 0.0, "detail": "existing suite regressed"}'
  exit 1
fi

cp "$task_dir/hidden_tests/test_hidden_storage.py" "$run_dir/tests/test_hidden_storage.py"
cp "$task_dir/hidden_tests/test_hidden_ledger.py" "$run_dir/tests/test_hidden_ledger.py"
cp "$task_dir/hidden_tests/test_hidden_cli.py" "$run_dir/tests/test_hidden_cli.py"

passed=0
groups=""
for mod in test_hidden_storage test_hidden_ledger test_hidden_cli; do
  if (cd "$run_dir" && python3 -m unittest "tests.$mod" -q) >"$out_file" 2>&1; then
    passed=$((passed + 1))
    groups="${groups}${mod}=pass "
  else
    groups="${groups}${mod}=fail "
  fi
done

score=$(python3 -c "print(round(${passed} / 3, 2))")
detail="existing suite passes; hidden layers: ${groups}"

echo "{\"score\": ${score}, \"detail\": \"${detail}\"}"
if [ "$passed" -eq 3 ]; then
  exit 0
else
  exit 1
fi
