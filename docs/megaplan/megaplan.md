# ICM starter workspace + agent-core

## What this is

Two things. First, a hybrid ICM workflow (Interpretable Context Methodology, Jake Van Clief —
https://github.com/RinDig/Interpreted-Context-Methdology), where ICM's folder structure organizes
work and specialist agents execute it: this repo runs it live and ships it as a reusable starter
for other projects. Second, agent-core: a generic agent factory that defines any agent once
(prompt, model provider, allowed tools and MCPs, who may use it), packages each agent as a
container, and deploys it to any Docker host — so agents form a compatible ecosystem. Personal
configs, MCP connections and credentials stay out of the repo.

## What already exists

As-built, no backlog rows for any of this:

- Reusable ICM starter workspace (b05, 2026-09-27): starter/ — a copyable template (CONTEXT.md + five generalized stage contracts + setup questionnaire); this repo's own structure is the worked example
- docs/megaplan/ planning system (megaplan skill): backlog empty (all items closed), glossary, done
  ledger — b01 closed 2026-09-25 with the hybrid ICM architecture decision (ICM stages organize
  work, specialist agents execute it).
- Hybrid ICM structure (b02, 2026-09-26): root AGENTS.md (layer 0) + CONTEXT.md (layer 1) + stages/01-intake…05-release stage contracts; work items flow intake → design → implement → verify → release
- OpenSpec (2026-10-10): openspec/ holds the active agent-core change (generic agent factory; proposal written). The archived repo-cleanup change (openspec/changes/archive/) removed the per-harness toolkits, installers and their docs; they remain in git history
- Git repo on `main` with origin remote
  `https://github.com/Gamebreack/multi-agent-orchestration.git`, initial commit made 2026-09-25;
  `.gitignore` excludes secrets and editor/OS clutter.
- Negatives: nothing pushed.

When an item changes what exists, edit the line it affects rather than appending a new one.
