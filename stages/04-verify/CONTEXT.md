# Stage 04 — verify

Independent check in fresh context.

## Inputs
| Source | File/Location | Section/Scope | Why |
|---|---|---|---|
| Acceptance criteria | ../../docs/megaplan/backlog-items/<id>.md | Outcome + Scope | What must hold |
| Changed files | working tree (git diff vs HEAD) | Full diff | The result |

## Process
1. A fresh mao-verifier (never the author) checks each criterion: PASS/FAIL
   with exact commands and output.
2. Ordinary items: mao-verifier. Significant / cross-cutting / risky items:
   mao-reviewer plus mao-verifier; pre-release: an independent panel.
3. mao-mechanical logs the verdict in the item's `## Log` and
   sets the row to `review`, as directed by the main agent.

## Outputs
| Artifact | Location | Format |
|---|---|---|
| Verdict | item file `## Log` | per-criterion PASS/FAIL + overall |
| Row status | docs/megaplan/backlog.md | review |

## Checkpoint
Operator reads the verdict; OPTIONAL findings may be sent back to stage 03.

## Audit
Verification never edits (permission-denied by design); any fix routes
back through stage 03 as delegated work, never as a "quick fix".
