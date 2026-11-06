# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html); see CONTRIBUTING.md (Releasing).

## [Unreleased]

## [0.2.1] - 2026-11-06

Tightens how changes get verified and documents how MAO is released. Re-run `mao-setup` to pick up the `core/AGENTS.md` change.

### Fixed
- **Starter stage contracts are consistent:** stage-relative paths in every Inputs/Outputs table, stage 04 routes BLOCKER and SHOULD-FIX findings back to stage 03, and the stage 05 ledger format matches `done.md`. (#7)
- **Verification ladder has one runtime home:** `core/AGENTS.md` now holds the full ladder. It adds a pre-release rung (a verifier run plus an independent panel, before tagging a version), gives every non-trivial change and every tracked work item at least a fresh verifier, checks changes to the ladder under the base branch's ladder at the significant rung or higher, says the highest rung applies when several match, limits the trivial self-check to low-risk edits outside a tracked work item, and no longer contradicts itself. Stage 04 points to it instead of restating it. Re-run `mao-setup` to pick up the `core/AGENTS.md` change. (#8)

### Added
- **`CHANGELOG.md` and a release procedure** (CONTRIBUTING.md, Releasing); the pull request template asks for a changelog entry. (#8)

## [0.2.0] - 2026-11-04

Makes MAO easier to pick up from outside. There are no changes to the role charters or to how setup behaves.

### Added
- **`flow-map` optional dependency:** `mao-setup` offers the [flow-map](https://github.com/Gamebreack/flow-map) skill (y/N), linked like `verify` and `megaplan`. (#4)
- **`flow-map.md`:** three Mermaid diagrams showing how MAO works from clone to a verified commit: what happens, who talks to whom, and the life of one task. (#5)
- **`CONTRIBUTING.md`, plus PR and issue templates (bug, idea)**, which point to the canonical rules instead of restating them. (#5)

### Changed
- **README rewritten for newcomers** (#5, #6):
  - It says what MAO does for you and what install changes on your machine.
  - It covers the clone, update, dry-run and per-harness uninstall steps.
  - The ASCII role tree is now a Mermaid role chart.
- **Starter workspace:** it says exactly what to copy, defines ICM, and says MAO must be installed first. The questionnaire no longer names a vendor's instructions file. (#5)
- **Fewer duplicated rules:** contributor docs, the glossary and the README now link to `AGENTS.md` and `docs/policies.md` instead of copying them. (#5)

## [0.1.0] - 2026-11-04

First tagged release of MAO: one set of instructions and role skills that your agent installs into whatever harness it runs in. No vendor, model ID, or machine-specific path is baked in.

### What's in it
- **`core/AGENTS.md`**: global instructions covering BLUF communication, the main agent as planner, roles by tier (fast / standard / deep), delegation, the verification ladder, and committing rules.
- **Seven role skills** (`core/skills/mao-*`): scout, mechanical, implementer, hard-implementer, reviewer, verifier, documenter.
- **`mao-setup`**: an install/uninstall procedure the agent runs. It builds a plan from the live harness docs, shows it, applies it only with your approval, records every action in a manifest for uninstall, and checks the install with a smoke test against the enforcement the plan declared.
- **Optional dependencies**, each offered y/N: OpenSpec CLI, `verify`, `megaplan`, `grilling` / `grill-me`.
- **`starter/`**: a copyable hybrid-ICM workspace (numbered stage contracts plus a megaplan backlog).

### Highlights since the per-harness toolkit
- Per-harness installers are replaced by one agent-run, harness-agnostic setup (b08).
- Setup waits for subagents to register before the smoke test, and sets numeric turn caps.
- The smoke test checks against the declared enforcement instead of a blanket rule.

[Unreleased]: https://github.com/Gamebreack/multi-agent-orchestration/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/Gamebreack/multi-agent-orchestration/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/Gamebreack/multi-agent-orchestration/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Gamebreack/multi-agent-orchestration/releases/tag/v0.1.0
