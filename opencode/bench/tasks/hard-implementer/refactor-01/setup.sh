#!/usr/bin/env bash
# Replaces the class-based storage layer with an ad-hoc dict-based one, and
# rewrites its direct callers/tests to match, so the fixture starts from a
# working-but-badly-designed state that the model must refactor.
set -euo pipefail
run_dir="$1"
task_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cp "$task_dir/planted/inventory/storage.py" "$run_dir/inventory/storage.py"
cp "$task_dir/planted/inventory/ledger.py" "$run_dir/inventory/ledger.py"
cp "$task_dir/planted/inventory/cli.py" "$run_dir/inventory/cli.py"
cp "$task_dir/planted/tests/test_storage.py" "$run_dir/tests/test_storage.py"
cp "$task_dir/planted/tests/test_ledger.py" "$run_dir/tests/test_ledger.py"
cp "$task_dir/planted/tests/test_cli.py" "$run_dir/tests/test_cli.py"
