# Proposal

## Why

The repo is changing direction: it now keeps hybrid ICM (its own way of
working and the reusable starter) and builds agent-core (see the
`agent-core` change). The per-harness toolkits (Claude Code, OpenCode,
Antigravity) and their docs no longer fit and would mislead readers and
agents. Removing them first leaves a clean base for agent-core.

## What Changes

- **Remove** the harness toolkits: `agents/`, `hooks/`, `opencode/`,
  `antigravity/`, `install.sh`, `uninstall.sh`.
- **Remove** all of `docs/` except `docs/megaplan/`: `policies.md`,
  `validation.md`, `harness-comparison.md`, `opencode.md`, `antigravity.md`,
  `claude-code-observations.md`.
- **Remove** files that exist only for the toolkits: `.env.example` (bench
  collector) and the bench/Python entries in `.gitignore`.
- **Edit** kept files so no reference points at a removed path:
  `AGENTS.md`, `CONTEXT.md`, `README.md` (rewritten for the new direction),
  `starter/README.md`, `docs/megaplan/glossary.md` (tier names keep plain
  definitions, no file pointers), `docs/megaplan/megaplan.md` ("what already
  exists" rewritten to current truth).
- **Keep untouched**: `stages/`, the rest of `starter/`, `openspec/`,
  `.claude/`, `.agents/`, and `docs/megaplan/done.md` (operator-only; its
  history lines stay as written).

Removed files remain reachable in git history.

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
<!-- none: no spec-level behavior changes; skip_specs is set -->

## Impact

- About 135 tracked files are deleted; no runtime code depends on them.
- Anyone using `install.sh` to set up a harness loses that path; the last
  commit before this change keeps it recoverable.
- The stage contracts keep naming agent tiers (explore, mechanical,
  implementer, verifier, reviewer); their definitions move from
  `docs/policies.md` to the glossary.
