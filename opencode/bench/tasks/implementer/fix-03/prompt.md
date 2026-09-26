This is a small Python inventory-tracking tool. Its test suite is currently failing.

1. Run `python3 -m unittest discover -s tests -q` to see the failures.
2. The failing tests live under `tests/`, but the test file where a failure
   shows up is not necessarily the module that has the bug — a failure in
   `tests/test_ledger.py` or `tests/test_cli.py` can be caused by a defect in
   a completely different module that those tests merely happen to exercise.
   Find the actual root cause and fix it there, not by special-casing the
   symptom in whichever function happens to raise or return the wrong value.
3. Do not modify anything under `tests/`.
4. Do not add new files.

When you are done, the full test suite must pass.
