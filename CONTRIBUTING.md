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

## Releasing

Versions follow SemVer: patch for fixes and wording; minor for a new skill, optional dependency, stage or setup behavior; major for breaking changes to role names, the setup manifest or the install layout.

1. In a pull request, move the `[Unreleased]` entries in `CHANGELOG.md` under `## [X.Y.Z] - YYYY-MM-DD` and update the compare links.
2. Run the pre-release verification from the verification ladder (global instructions, Delegation step 8) on that pull request while it is up to date with `main`, and merge only after it passes with no open BLOCKER or SHOULD-FIX finding (for example a PASS or PASS WITH NOTES verdict). If any change other than recording the verdict lands on the pull request or on `main` after the check, run it again, so the tagged tree is the checked tree plus, at most, the recorded verdict.
3. Only with the operator's approval, which covers this step and the next: after the pull request merges, tag the merge commit on `main` as `vX.Y.Z` and push the tag.
4. Create the GitHub release with that version's changelog section as its notes: `gh release create vX.Y.Z --verify-tag --title "vX.Y.Z — <summary>" --notes-file <section>`. `--verify-tag` stops the release if the tag from step 3 is not on the remote.
