# Where work goes — fill the angle-bracket placeholders from setup/questionnaire.md
`<One sentence: what this workspace is for — questionnaire item 1>`

| You want to... | Go to |
|---|---|
| Read project conventions | `<AGENTS.md or your conventions file>` |
| Start or resume a work item | `<work index>`, then the item's file |
| Know how an item flows | stages/ (below) |
| Understand the domain | `<your reference docs>` |

## Stage routing

| Stage | Job | Executed by | Operator checkpoint |
|---|---|---|---|
| stages/01-intake/ | request → work item | orchestrator + mechanical worker | scope confirmed |
| stages/02-design/ | inspect + proposal | explore / scout + orchestrator + mechanical worker | plan approved |
| stages/03-implement/ | delegated edits | mechanical / implementer / hard-implementer (delegated by orchestrator) | — |
| stages/04-verify/ | independent check | verifier / reviewer + mechanical worker | verdict read |
| stages/05-release/ | record + ship | orchestrator + worker | release authorized |

Handoff state between stages: the item's log, the index row's status, and
the working tree. Nothing else carries state.

## Boundaries — inherited by every work item

- Out of scope: `<what work here never touches — questionnaire item 3>`
- Never enters this workspace: `<secrets policy, portability boundary — questionnaire item 8>`
