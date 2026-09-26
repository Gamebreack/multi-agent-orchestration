You are planning work (not implementing it) for this small Python
inventory-tracking project (source under `inventory/`, tests under
`tests/`).

Feature request: add a low-stock alert to the report command.

- `inventory.models.Item` should gain a method `is_low_stock(threshold)` that
  returns whether the item's quantity is at or below `threshold`.
- `inventory.report` should gain a function `low_stock(items, threshold)`
  that returns the items (sorted by id) whose `is_low_stock(threshold)` is
  true, and a function `format_alert(items)` that renders those items with a
  warning marker for display.
- `inventory.plugins` should register a new `"alert"` formatter, backed by
  `report.format_alert`, using the existing registration mechanism.
- `inventory.cli` should add a `--low-stock N` option to the `report`
  subcommand: when given, the report command filters to low-stock items
  (via `report.low_stock`) before formatting them with whichever `--format`
  is selected.

Produce an execution plan: a set of tasks, each touching one file, in an
order that respects real dependencies between them (a task that uses a
function must come after the task that adds that function).

Do not implement anything. Output your plan as a single fenced code block of
JSON, containing an object with this exact shape, and nothing else inside
the block:

```json
{"tasks": [{"id": "t1", "files": ["inventory/models.py"], "depends_on": [], "summary": "..."}]}
```

Rules for the plan:
- Every task's `files` list must contain exactly one file, and every file
  must be owned by exactly one task (no file split across two tasks, no file
  claimed by two tasks).
- `depends_on` is a list of the `id`s of tasks that must land first.
- Cover all four files that need to change: `inventory/models.py`,
  `inventory/report.py`, `inventory/plugins.py`, `inventory/cli.py`. Do not
  include files that don't need to change.

If you output more than one such code block, only the last one will be
graded.
