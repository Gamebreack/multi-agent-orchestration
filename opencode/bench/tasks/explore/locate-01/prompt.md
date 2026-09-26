This is a small Python inventory-tracking project rooted at the current
directory (source under `inventory/`, tests under `tests/`). Answer the
following 5 questions by locating the relevant code. Do not modify any
files.

- q1: Which file and function/property computes the total monetary value of a
  single item (quantity times price)?
- q2: Which file and function validates the shape and values of an item data
  dict (id, name, quantity, price) before it's stored?
- q3: Which file defines the constant for the maximum allowed length of an
  item name, and what is the constant's name?
- q4: Which file and method raises `ValidationError` when a stock adjustment
  would take an item's quantity below zero?
- q5: Which file and function renders a list of items as a CSV string?

Report each answer as the file path (relative to the current directory) and
the symbol name (function, method as `Class.method`, or constant name).

When you are done, output your answers as a single fenced code block of
JSON, containing an object with keys `q1`..`q5`, and nothing else inside the
block:

```json
{"q1": {"file": "inventory/models.py", "symbol": "Item.total_value"}, "q2": {"file": "...", "symbol": "..."}, "q3": {"file": "...", "symbol": "..."}, "q4": {"file": "...", "symbol": "..."}, "q5": {"file": "...", "symbol": "..."}}
```

(The example above is illustrative formatting only, not necessarily a
correct answer.) If you output more than one such code block, only the last
one will be graded.
