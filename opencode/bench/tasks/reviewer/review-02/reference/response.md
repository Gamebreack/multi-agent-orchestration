Findings:

```json
[
  {"file": "inventory/pricing.py", "line": 18, "summary": "PriceTag explicitly sets __hash__ = object.__hash__ (identity-based) while __eq__ compares by value, violating the equal-objects-must-hash-equal contract; equal tags in a set/dict silently fail to match."},
  {"file": "inventory/pricing.py", "line": 21, "summary": "apply_discount uses a mutable default argument (seen_tags=set()); the same set is reused and accumulates across calls that don't pass their own seen_tags."},
  {"file": "inventory/pricing.py", "line": 43, "summary": "int(total_cents) truncates instead of rounding, silently losing fractions of a cent instead of rounding to the nearest cent."},
  {"file": "inventory/pricing.py", "line": 59, "summary": "except Exception: pass swallows any error while writing the CSV (including malformed item data), so callers get no indication the export was incomplete."},
  {"file": "inventory/pricing.py", "line": 61, "summary": "rows is a generator already fully consumed by the for-loop above; `sum(1 for _ in rows)` iterates it again and always returns 0 regardless of how many rows were written."},
  {"file": "inventory/pricing.py", "line": 66, "summary": "safe_export has a check-then-act race: os.path.exists(path) and the later open(path, \"w\") are not atomic, so a file created between the two can be silently overwritten."}
]
```
