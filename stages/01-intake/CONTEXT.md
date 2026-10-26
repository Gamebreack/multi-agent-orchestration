# Stage 01 — intake

Turn an operator request into a backlog item.

## Inputs
| Source | File/Location | Section/Scope | Why |
|---|---|---|---|
| Request | operator message / linked spec | Full | The work requested |
| Backlog | ../../docs/megaplan/backlog.md | Index | Next ID + live rows |
| Glossary | ../../docs/megaplan/glossary.md | All | Naming authority |

## Process
1. The main agent runs the megaplan interview — the
   operator answers — until every answer names something checkable.
2. The main agent restates the scope as what will NOT be touched; the
   operator confirms.
3. mao-mechanical creates the backlog row (next `b` ID) and, when
   the item needs a file, the item file from the template.
4. mao-mechanical logs the opening in the item's `## Log`.

## Outputs
| Artifact | Location | Format |
|---|---|---|
| Backlog row | docs/megaplan/backlog.md | in-progress |
| Item file | docs/megaplan/backlog-items/<id>.md | megaplan template |

## Checkpoint
Operator confirms the scope restatement before the row exists. If corrected
twice and still wrong: stop, write nothing (megaplan rule).

## Audit
Row ID is one past the highest in backlog.md or done.md; no ID is reused;
the done ledger is untouched.
