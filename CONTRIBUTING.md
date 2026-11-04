# Contributing

## How to propose a change

1. For anything beyond a small fix, open an issue first and describe the problem.
2. Then open a pull request against `main`. `main` is protected, so every change goes
   through a pull request.

## Rules a change must keep

The hard rules in [AGENTS.md](AGENTS.md) apply to every change: the portability boundary
(no model names, harness config, credentials or machine paths), line limits, and one home
per fact. If a change alters the flow, update [flow-map.md](flow-map.md) in the same pull
request.

## Working on this repo

Maintainers run their work through the ICM stages in [`stages/`](stages/). Start at
[CONTEXT.md](CONTEXT.md). Contributors need only a clear issue or pull request.

## Testing a change to `mao-setup`

Run the change in dry-run mode in your harness: add `dry-run` to the setup prompt. Paste
the plan into the pull request, with local paths redacted.
