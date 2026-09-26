This is a small Python inventory-tracking tool with a plugin-style registry of
report formatters (see `inventory/plugins.py`, and how `"text"` and `"csv"`
formatters are registered in `inventory/cli.py`).

Add a new `markdown` report format:

1. In `inventory/report.py`, implement a function `format_markdown(items)` that
   renders a Markdown table:
   - Header row: `| id | name | quantity | price |`
   - Separator row: `| --- | --- | --- | --- |`
   - One row per item, sorted by `id` ascending, e.g.
     `| a1 | Anvil | 1 | 100.00 |` (price formatted with exactly 2 decimals).
   - Rows are joined with `\n`, no trailing newline.
2. In `inventory/cli.py`, register it under the name `"markdown"` using the
   existing `register_formatter` mechanism, the same way `"text"` and `"csv"`
   are registered, so that `inventory report --format markdown` works.

Do not modify anything under `tests/`.
