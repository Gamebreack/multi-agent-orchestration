This project's inventory storage layer (`inventory/storage.py`) uses ad-hoc
module-level global state: a single module-level dict plus a handful of free
functions (`add_item`, `get_item`, `remove_item`, `all_items`, `save_items`,
`load_items`, `reset`). `inventory/ledger.py` and `inventory/cli.py` call
those free functions directly.

Refactor `inventory/storage.py` to expose a `Storage` class that encapsulates
the item collection as instance state, with these methods:

- `add(item)`
- `get(item_id)` -> item or `None`
- `remove(item_id)`
- `all()` -> list of items
- `save(path)`
- `load(path)`

Then update the callers:

- `inventory/ledger.py`: `Ledger` should take a `Storage` instance in its
  constructor (`Ledger(storage)`) and use it instead of the module-level
  functions.
- `inventory/cli.py`: construct a `Storage` instance instead of relying on
  global state. `run()` should accept an optional `storage` parameter
  (defaulting to a fresh `Storage()` when not given).

Preserve all existing behavior: the `add`, `adjust`, and `report` CLI
commands, item validation, and the save/load JSON round trip must keep
working exactly as before.

You may rewrite `tests/test_storage.py`, `tests/test_ledger.py`, and
`tests/test_cli.py` to match the new API if you find it useful — they will be
replaced by the grader regardless, so it doesn't affect scoring either way.

Do not change `inventory/models.py`, `inventory/validation.py`,
`inventory/report.py`, or `inventory/plugins.py`.
