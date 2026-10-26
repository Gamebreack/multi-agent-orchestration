# Stage 03 — implement

Delegated edits by specialist workers.

## Inputs
| Source | File/Location | Section/Scope | Why |
|---|---|---|---|
| Approved proposal | `../../<items dir>/<id>.md` | log (latest proposal) | The plan |
| Working files | paths the proposal names | As named | Edit targets |

## Process
1. The main agent delegates each unit to the tier the work needs:
   deterministic edits → mao-mechanical; ordinary work → mao-implementer;
   genuinely difficult → mao-hard-implementer. At most 3 concurrent workers; group tiny
   edits by file ownership, never one worker per edit.
2. Workers report files changed, verification run, failures. On failure the
   main agent resumes the same task with feedback; escalation only after
   a retry fails.
3. mao-mechanical logs what happened (not what was intended).

## Outputs
| Artifact | Location | Format |
|---|---|---|
| Edits | working tree | smallest complete change |
| Worker reports | item file log | dated entries |

## Audit
This stage produces working-tree edits only; shipping happens in stage 05.
Worker self-verification is a claim, not evidence — stage 04 checks it.
