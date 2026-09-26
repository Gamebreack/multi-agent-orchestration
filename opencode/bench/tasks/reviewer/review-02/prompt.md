A teammate opened `REVIEW_TARGET.diff` in this directory, a proposed change
that adds bulk pricing utilities (discounts, totals, CSV/plain-text export)
to this inventory tool. Review it the way you would in a code review: read
the diff carefully and find defects in the new code.

There are multiple real defects of different kinds, for example: concurrency
issues, mutable/shared state bugs, error-handling problems that hide
failures, iterator/generator misuse, numeric precision issues, and object
contract violations (e.g. equality vs. hashing). Not everything that looks
unusual is actually wrong — some patterns in this diff are unconventional
but correct, and flagging those as defects will cost you points.

For each defect you find, report:
- `file`: the path as shown in the diff.
- `line`: the line number within the new file's content (i.e. count from the
  top of the new file's `+` lines starting at 1), not any other numbering.
- `summary`: a one-sentence description of the defect.

When you are done, output your findings as a single fenced code block of
JSON, containing a JSON list, and nothing else inside the block:

```json
[{"file": "inventory/pricing.py", "line": 12, "summary": "..."}]
```

If you output more than one such code block, only the last one will be
graded.
