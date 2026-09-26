#!/usr/bin/env bash
# Plants a None/missing-key handling bug: loading items whose JSON record has
# no "tags" key crashes instead of defaulting to an empty list.
set -euo pipefail
run_dir="$1"

sed -i 's/tags=record.get("tags", \[\]),/tags=record["tags"],/' "$run_dir/inventory/storage.py"
