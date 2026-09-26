# Backlog — Multi-agent orchestration toolkit + ICM starter workspace

The **operator** is the human who owns this project: they answer the interview, confirm scope, and
write `done.md`. The agent does everything else, including maintaining this file.

## Statuses

| Status | Meaning |
|---|---|
| `pending` | Defined, not started |
| `in-progress` | Being worked now |
| `review` | Believed complete, waiting on the operator |
| `superseded` | Replaced by another item, and not delivered |

An item leaves this file when the operator writes its line in `done.md` — whether it was finished or
superseded. The agent then edits `megaplan.md` under "what already exists" if the item changed what
exists, and deletes both the row here and the item file. This file is live work only.

## Index

| ID | Title | Status | Item file |
|---|---|---|---|
| b04 | Harness-explicit, backup-aware installation and safe uninstall for all three harnesses | pending | — |
| b05 | Reusable ICM starter workspace with onboarding and one worked example | pending | — |
| b06 | Independent review and isolated validation with tested-vs-pending OS/harness support matrix | pending | — |
| b07 | OpenCode V2 shared-permissions migration: convert the 8 agent permission maps to the V2 `permissions` array and collapse the 4 duplicated worker bash maps into one top-level `permissions` block in opencode.jsonc (scout-verified: agent rules append after global, last match wins) | pending | — |
