# Multi-agent orchestration toolkit + ICM starter workspace

## What this is

A portable, harness-agnostic agent setup: tool-neutral global instructions, role skills (`mao-*`)
and an agent-run setup procedure that translates them into each harness's native local config.
Nothing harness-specific and no model IDs are committed. It doubles as a reusable starter
workspace for ICM (Interpretable Context Methodology, Jake Van Clief —
https://github.com/RinDig/Interpreted-Context-Methdology), where ICM's folder structure acts as the
agent orchestration.

## What already exists

As-built, no backlog rows for any of this:

- Portable core (b08): `core/AGENTS.md` (global instructions, roles by tier), seven role skills
  (`core/skills/mao-{scout,mechanical,implementer,hard-implementer,reviewer,verifier,documenter}`),
  `core/skills/mao-setup` (agent-run install/uninstall procedure with backups and a manifest) and
  the opt-in `core/skills/second-brain-interface` template.
- Harness capability snapshot dated 2026-10-26 (`docs/harness-comparison.md`) and shared policies
  (`docs/policies.md`: roles, tiers, access levels, permission philosophy).
- Reusable ICM starter workspace (b05, 2026-09-27): starter/ — a copyable template (CONTEXT.md + five
  generalized stage contracts + setup questionnaire); this repo's own structure is the worked example.
- docs/megaplan/ planning system (megaplan skill): glossary, done ledger — b01 closed 2026-09-25 with
  the hybrid ICM architecture decision (ICM stages organize work, role agents execute it).
- Hybrid ICM structure (b02, 2026-09-26): root AGENTS.md (layer 0) + CONTEXT.md (layer 1) +
  stages/01-intake…05-release stage contracts; work items flow intake → design → implement → verify →
  release.
- Git repo on `main` with origin remote `https://github.com/Gamebreack/multi-agent-orchestration.git`.
- Negatives: no installer scripts, no per-harness files, no manager/orchestrator role, no model IDs
  outside `docs/harness-comparison.md`.

When an item changes what exists, edit the line it affects rather than appending a new one.
