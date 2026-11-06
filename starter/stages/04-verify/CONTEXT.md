# Stage 04 — verify

Independent check in fresh context.

## Inputs
| Source | File/Location | Section/Scope | Why |
|---|---|---|---|
| Acceptance criteria | `../../<items dir>/<id>.md` | Outcome + Scope | What must hold |
| Changed files | working tree (uncommitted changes) | Full diff | The result |

## Process
1. Pick the verification rung from the verification ladder in the global
   instructions (MAO's core/AGENTS.md, Delegation step 8).
2. The chosen check reports per criterion PASS/FAIL with exact commands
   and output.
3. mao-mechanical logs the verdict in the item's log and sets the index
   row to review.

## Outputs
| Artifact | Location | Format |
|---|---|---|
| Verdict | item file log | per-criterion PASS/FAIL + overall |
| Row status | `../../<work index>` | review |

## Checkpoint
Operator reads the verdict. BLOCKER and SHOULD-FIX findings go back to
stage 03; OPTIONAL findings go back only if the operator chooses.

## Audit
Verification never edits; any fix routes back through stage 03 as delegated
work, never as a "quick fix".
