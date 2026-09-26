# Stage 03 — implement

Delegated edits by specialist workers.

## Inputs
| Source | File/Location | Section/Scope | Why |
|---|---|---|---|
| Approved proposal | ../../docs/megaplan/backlog-items/<id>.md | `## Log` (latest proposal) | The plan |
| Working files | paths the proposal names | As named | Edit targets |

## Process
1. Orchestrator delegates each unit to the tier the work needs:
   deterministic edits → mechanical; ordinary work → implementer; genuinely
   difficult → hard-implementer. At most 3 concurrent workers; group tiny
   edits by file ownership, never one worker per edit.
2. Workers report files changed, verification run, failures. On failure the
   coordinator resumes the same task with feedback; escalation only after
   a retry fails.
3. Log what happened (not what was intended) in the item's `## Log`.

## Outputs
| Artifact | Location | Format |
|---|---|---|
| Edits | working tree | smallest complete change |
| Worker reports | item file `## Log` | dated entries |

## Audit
This stage produces working-tree edits only; commits happen in stage 05. Worker self-verification is a claim,
not evidence — stage 04 checks it in fresh context.
