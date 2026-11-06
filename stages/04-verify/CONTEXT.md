# Stage 04 — verify

Independent check in fresh context.

## Inputs
| Source | File/Location | Section/Scope | Why |
|---|---|---|---|
| Acceptance criteria | ../../docs/megaplan/backlog-items/<id>.md | Outcome + Scope | What must hold |
| Changed files | working tree (git diff vs HEAD) | Full diff | The result |

## Process
1. Pick the verification rung from the verification ladder in the global
   instructions (MAO's core/AGENTS.md, Delegation step 8).
2. The chosen check reports per criterion PASS/FAIL with exact commands
   and output.
3. mao-mechanical logs the verdict in the item's `## Log` and
   sets the row to `review`, as directed by the main agent.

## Outputs
| Artifact | Location | Format |
|---|---|---|
| Verdict | item file `## Log` | per-criterion PASS/FAIL + overall |
| Row status | ../../docs/megaplan/backlog.md | review |

## Checkpoint
Operator reads the verdict. BLOCKER and SHOULD-FIX findings go back to
stage 03; OPTIONAL findings go back only if the operator chooses.

## Audit
Verification never edits (permission-denied by design); any fix routes
back through stage 03 as delegated work, never as a "quick fix".
