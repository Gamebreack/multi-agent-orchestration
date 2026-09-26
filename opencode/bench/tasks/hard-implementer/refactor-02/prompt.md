Add a persisted adjustment history to this inventory tool. Today,
`Ledger` keeps its transaction history only in memory (`self.history`);
it's lost as soon as the process exits, even though `Storage` already
supports saving and loading items to/from a JSON file. Thread a proper
audit trail through the whole stack:

1. `inventory/models.py`: move the `Transaction` dataclass here (fields
   `item_id: str`, `delta: int`, `reason: str`) — it's a persisted domain
   object now, not an implementation detail of `Ledger`.

2. `inventory/validation.py`: add `MAX_REASON_LENGTH = 200` and a function
   `validate_reason(reason) -> None` that raises `ValidationError` if
   `reason` is not a `str`, or if it's longer than `MAX_REASON_LENGTH`
   characters.

3. `inventory/storage.py`: `Storage` becomes the source of truth for
   transactions, not `Ledger`:
   - `record_transaction(txn)` appends a `Transaction`.
   - `transactions_for(item_id)` returns the transactions for that item, in
     the order they were recorded.
   - `all_transactions()` returns every recorded transaction, in order.
   - `save(path)` must also persist transactions, as a `"transactions"` key
     in the JSON payload (a list of `{"item_id", "delta", "reason"}`
     objects), alongside the existing `"version"` and `"items"` keys.
   - `load(path)` must restore transactions from that key. **Backwards
     compatibility constraint:** JSON files saved before this change have
     no `"transactions"` key at all. Loading such a file must keep working
     and simply result in an empty transaction list — do not assume or
     require the key's presence.

4. `inventory/ledger.py`: `Ledger.adjust(item_id, delta, reason="")` must
   call `validate_reason(reason)` before applying the delta, and record the
   resulting `Transaction` via `self.storage.record_transaction(...)`
   instead of appending to a list of its own. `Ledger.transactions_for`
   must delegate to `self.storage.transactions_for(...)`, so that a fresh
   `Ledger` built over a `Storage` that was reloaded from disk sees the
   transactions recorded before the save. Keep `Ledger(storage)` and
   `balance(item_id)` as they are.

5. `inventory/report.py`: add `format_history(transactions) -> str` that
   renders one line per transaction as `f"{t.item_id}\t{t.delta:+d}\t{t.reason}"`
   (note the explicit `+`/`-` sign on delta), joined with `\n`, with no
   trailing newline. An empty list renders as `""`.

6. `inventory/cli.py`: add a `history <id>` subcommand that prints
   `report.format_history(ledger.transactions_for(args.id))`. **Exit-code
   contract:** unlike `adjust` on an unknown item (which must keep raising
   `ValidationError`, exit code 1), `history` on an item with no recorded
   transactions — including one that was never added at all — must NOT
   raise. It simply returns `""`, the same as any item with an empty
   history, so the process exits 0.

Preserve all existing behavior: `add`, `adjust`, and `report` must keep
working exactly as before, and the existing test suite must keep passing
unmodified.

Do not modify anything under `tests/`.
