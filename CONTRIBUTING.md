# Contributing

## How to propose a change

1. For anything beyond a small fix, open an issue first and describe the problem.
2. Then open a pull request against `main`. Every change lands through a pull request.

## Rules a change must keep

Every change keeps the rules in [AGENTS.md](AGENTS.md) and the portability boundary in [docs/policies.md](docs/policies.md#portability-boundary). Changes that alter the flow follow the update rule at the end of [flow-map.md](flow-map.md).

## Working on this repo

Maintainers track work in `stages/` and `docs/megaplan/`; contributors can ignore both.

## Testing a change to `mao-setup`

Point your agent at the `SKILL.md` in your changed checkout and ask for a dry run. Check that the plan's repo path is that checkout: an existing install may point it at an older clone (setup prefers the repo path in `~/.config/mao/installed.json`). Paste the plan into the pull request, with local paths redacted.
