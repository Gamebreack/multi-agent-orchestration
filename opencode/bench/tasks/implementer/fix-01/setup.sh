#!/usr/bin/env bash
# Plants a logic bug: adjusting stock down to exactly zero is incorrectly
# rejected (off-by-one on the boundary condition).
set -euo pipefail
run_dir="$1"

sed -i 's/if new_quantity < 0:/if new_quantity <= 0:/' "$run_dir/inventory/ledger.py"
