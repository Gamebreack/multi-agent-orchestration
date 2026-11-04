# ICM starter workspace

Copy it into any project (see Use it) to get a staged workflow (ICM, Interpretable Context
Methodology): numbered stages organize each work item; specialist agents execute the stage work
(the mao-* role skills — see docs/policies.md in the multi-agent-orchestration
repo this starter came from). Needs MAO installed: the stages name mao-* roles.

## Use it

1. Copy `CONTEXT.md`, `stages/` and `setup/` from `starter/` into your project root.
2. Answer `setup/questionnaire.md` — all at once, one pass.
3. Fill the placeholders in `CONTEXT.md` from your answers.
4. Adapt the stage contracts under `stages/` to your domain (rename, add,
   remove stages; keep the Inputs/Process/Outputs shape) and fill their
   remaining placeholders. The `<id>` token is not a placeholder — it is the
   per-run work-item ID the intake stage mints.
5. Run work items through the stages; edit any stage output between stages —
   the next stage reads whatever you left there.

## Rules that travel with it

- The main agent plans and delegates (it may make a truly trivial edit
  itself); role agents execute stage work.
- Every stage contract has Inputs / Process / Outputs; keep each under 80
  lines; reference docs under 200.
- Work state lives in the item's log, the index row's status, and the working
  tree; nothing else carries state.
- Checkpoints (operator gates) sit in stages 01, 02, 04, 05; implement (03)
  runs without one.
- The starter assumes git for the release stage; adapt stage 05 for another
  version-control system.

## Worked example

The multi-agent-orchestration repo runs the same structure live: its root `CONTEXT.md`, `stages/`, and
`docs/megaplan/` (the work index) are the worked example.
