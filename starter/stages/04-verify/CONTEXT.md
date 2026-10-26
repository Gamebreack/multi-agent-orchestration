# Stage 04 — verify

Independent check in fresh context.

## Inputs
| Source | File/Location | Section/Scope | Why |
|---|---|---|---|
| Acceptance criteria | `../../<items dir>/<id>.md` | Outcome + Scope | What must hold |
| Changed files | working tree (uncommitted changes) | Full diff | The result |

## Process
1. A fresh mao-verifier (never the author) checks each criterion: PASS/FAIL
   with exact commands and output.
2. Ordinary items: mao-verifier. Significant / cross-cutting / risky items:
   mao-reviewer plus mao-verifier; pre-release: an independent panel.
3. mao-mechanical logs the verdict and sets the index row to
   review.

## Outputs
| Artifact | Location | Format |
|---|---|---|
| Verdict | item file log | per-criterion PASS/FAIL + overall |
| Row status | work index | review |

## Checkpoint
Operator reads the verdict; OPTIONAL findings may go back to stage 03.

## Audit
Verification never edits; any fix routes back through stage 03 as delegated
work, never as a "quick fix".
