# Stage 01 — intake

Turn a request into a work item.

## Inputs
| Source | File/Location | Section/Scope | Why |
|---|---|---|---|
| Request | operator message / linked spec | Full | The work requested |
| Work index | `../../<work index>` | Index | Next ID + live rows |
| Glossary | `<glossary if used>` | All | Naming authority |

## Process
1. The main agent runs the intake interview — the
   operator answers — until every answer names something checkable.
2. The main agent restates the scope as what will NOT be touched; the
   operator confirms.
3. mao-mechanical creates the index row (next ID) and, when the
   item needs a file, the item file.
4. mao-mechanical logs the opening in the item's log.

## Outputs
| Artifact | Location | Format |
|---|---|---|
| Index row | `<work index>` | in-progress |
| Item file | `<items dir>/<id>.md` | when needed |

## Checkpoint
Operator confirms the scope restatement before the row exists. If corrected
twice and still wrong: stop, write nothing.

## Audit
The row ID is one past the highest in the index or the done ledger; no ID is
reused; the done ledger is untouched.
