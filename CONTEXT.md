# Where work goes

| You want to... | Go to |
|---|---|
| Read repo conventions | AGENTS.md (layer 0) |
| Start or resume a work item | docs/megaplan/backlog.md, then the item's file |
| Know how an item flows | stages/ (below) |
| Work on OpenCode agents | opencode/ |
| Work on Claude Code assets | agents/, hooks/ |
| Work on Antigravity assets | antigravity/ |
| Install or remove a harness's orchestration layer | install.sh, uninstall.sh |
| Start a new project with this workflow | starter/ |
| Compare harnesses | docs/harness-comparison.md |
| Run model benchmarks | opencode/bench/ (results are git-ignored) |

## Stage routing

Each stage contract (its CONTEXT.md) defines Inputs / Process / Outputs and
names the executing agent tier:

| Stage | Job | Executed by | Operator checkpoint |
|---|---|---|---|
| stages/01-intake/ | request → backlog item | orchestrator + mechanical worker | scope confirmed |
| stages/02-design/ | inspect + proposal | explore / scout + mechanical worker | plan approved |
| stages/03-implement/ | delegated edits | mechanical / implementer / hard-implementer (delegated by orchestrator) | — |
| stages/04-verify/ | independent check | verifier / reviewer + mechanical worker | verdict read |
| stages/05-release/ | ledger + commit + push | orchestrator + worker | push authorized |

Handoff state between stages: the item file's `## Log`, the backlog row's
status, and the working tree. Nothing else carries state.
