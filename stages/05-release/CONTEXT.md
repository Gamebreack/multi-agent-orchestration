# Stage 05 — release

Ledger, close-out commit, push.

## Inputs
| Source | File/Location | Section/Scope | Why |
|---|---|---|---|
| Verdict | ../../docs/megaplan/backlog-items/<id>.md | `## Log` (latest) | Release evidence |
| Ledger | ../../docs/megaplan/done.md | Table | Where the line goes |

## Process
1. The operator writes the done-ledger line (ID, date, one sentence).
2. Close-out in one commit, with explicit operator authorization: the
   orchestrator delegates the edits and commit to a worker (the operator
   approves the permission prompts) — delete the backlog row, delete the
   item file (it stays reachable in git history), update megaplan.md if
   the item changed what exists.
3. The operator pushes (push is operator-only; see AGENTS.md hard rules).

## Outputs
| Artifact | Location | Format |
|---|---|---|
| Ledger line | docs/megaplan/done.md | operator-written |
| Close-out commit | git history | row + item file deleted |

## Checkpoint
Operator authorizes the commit and runs the push. Nothing ships without
both.

## Audit
The done-ledger line exists before the close-out commit. The backlog row
and the item file are deleted in the same commit, and the item file remains
reachable in git history. The push was run by the operator.
