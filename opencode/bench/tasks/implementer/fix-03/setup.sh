#!/usr/bin/env bash
# Plants a defensive-copy bug in Storage.get(): it returns a copy of the
# stored Item instead of the live object. This is invisible to
# tests/test_storage.py (which only checks value equality, never identity or
# mutation-through-a-previous-reference), but breaks any code that mutates
# the object returned by get() and expects the change to persist -- namely
# Ledger.adjust(). The resulting failures surface in tests/test_ledger.py and
# tests/test_cli.py, even though the actual bug lives in inventory/storage.py.
set -euo pipefail
run_dir="$1"
task_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cp "$task_dir/planted/inventory/storage.py" "$run_dir/inventory/storage.py"
