# Where work goes

| You want to... | Go to |
|---|---|
| Read repo conventions | AGENTS.md (layer 0) |
| Start or resume a work item | docs/megaplan/backlog.md, then the item's file |
| Know how an item flows | stages/ (below) |
| Change the global instructions or a role charter | core/AGENTS.md, core/skills/mao-<role>/ |
| Change the install/uninstall procedure | core/skills/mao-setup/ |
| Change the optional second-brain template | core/skills/second-brain-interface/ |
| Start a new project with this workflow | starter/ |
| Read the shared policies (roles, tiers, access) | docs/policies.md |
| Compare harness capabilities | docs/harness-comparison.md |

## Stage routing

Each stage contract (its CONTEXT.md) defines Inputs / Process / Outputs and
names the executing agent tier:

| Stage | Job | Executed by | Operator checkpoint |
|---|---|---|---|
| stages/01-intake/ | request → backlog item | main agent + mao-mechanical | scope confirmed |
| stages/02-design/ | inspect + proposal | mao-scout + main agent + mao-mechanical | plan approved |
| stages/03-implement/ | delegated edits | mao-mechanical / mao-implementer / mao-hard-implementer (delegated by main agent) | — |
| stages/04-verify/ | independent check | mao-verifier / mao-reviewer + mao-mechanical | verdict read |
| stages/05-release/ | ledger + commit + push | main agent + mao-implementer | push authorized |

Handoff state between stages: the item file's `## Log`, the backlog row's
status, and the working tree. Nothing else carries state.
