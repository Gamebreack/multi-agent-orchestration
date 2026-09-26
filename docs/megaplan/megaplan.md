# Multi-agent orchestration toolkit + ICM starter workspace

## What this is

A portable multi-agent orchestration toolkit: replicate the agent experience and structure of this
repo on other PCs and environments — across OpenCode, Claude Code and Antigravity, on Linux, macOS
and WSL — excluding personal configs, MCP connections and credentials. It doubles as a reusable
starter workspace for ICM (Interpretable Context Methodology, Jake Van Clief —
https://github.com/RinDig/Interpreted-Context-Methdology), where ICM's folder structure acts as the
agent orchestration.

## What already exists

As-built, no backlog rows for any of this:

- Eight OpenCode agent definitions (`opencode/agents/`) + an `AGENTS.md` note + the `oc-preset`
  model-switching helper (`opencode/oc-preset`) + openai/go presets (`opencode/presets/`).
- Claude Code manager setup: seven agents (`agents/`) + the `manager-boundary.sh` hook (`hooks/`)
  + `install.sh`/`uninstall.sh` scripts at the repo root.
- Antigravity CLI assets (`antigravity/`).
- Harness comparison and per-harness docs (`docs/harness-comparison.md`, `docs/opencode.md`,
  `docs/claude-code-observations.md`, `docs/antigravity.md`).
- docs/megaplan/ planning system (megaplan skill): backlog (b03 in progress; b04–b07 pending), glossary, done
  ledger — b01 closed 2026-09-25 with the hybrid ICM architecture decision (ICM stages organize
  work, specialist agents execute it).
- Hybrid ICM structure (b02, 2026-09-26): root AGENTS.md (layer 0) + CONTEXT.md (layer 1) + stages/01-intake…05-release stage contracts; work items flow intake → design → implement → verify → release
- Benchmark harness (`opencode/bench/`), results git-ignored.
- Git repo on `main` with origin remote
  `https://github.com/Gamebreack/multi-agent-orchestration.git`, initial commit made 2026-09-25,
  nothing pushed; `.gitignore` excludes generated artifacts; `.env.example` documents the bench
  collector env var.
- Negatives: no OpenCode installer, no starter workspace, no cross-platform
  validation, nothing pushed.

When an item changes what exists, edit the line it affects rather than appending a new one.
