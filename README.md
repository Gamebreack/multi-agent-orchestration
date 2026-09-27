# Delegation-first multi-agent orchestration

A portable agent setup for three harnesses in which the primary agent only
plans, delegates and reconciles — it never modifies the repository — and
all edits, verification and review happen in scoped specialist subagents.
Work on this repo itself follows an ICM structure: see [CONTEXT.md](CONTEXT.md)
for routing and stages/ for the workflow.

```
                         MANAGER  (fable, high) — orchestration only
                            │
          ┌─────────────────┼──────────────────┐
          │                 │                  │
      explorer         implementers        verification
       haiku                │                  │
                    ┌───────┼────────┐    ┌────┴─────┐
                    │       │        │    │          │
            mechanical-  worker  hard-  reviewer  verifier
              worker     sonnet  worker   opus     sonnet
               haiku              opus
```

## What is where

| You want... | Go to |
|---|---|
| The shared policies (roles, permissions, verification, models) | [docs/policies.md](docs/policies.md) |
| How the three harnesses compare | [docs/harness-comparison.md](docs/harness-comparison.md) |
| Optional model presets | opencode/presets/ + opencode/oc-preset |
| OpenCode setup | [docs/opencode.md](docs/opencode.md) |
| Antigravity setup | [docs/antigravity.md](docs/antigravity.md) |
| Claude Code notes and history | [docs/claude-code-observations.md](docs/claude-code-observations.md) |
| Repo routing and workflow | [CONTEXT.md](CONTEXT.md), stages/ |
| Work backlog | docs/megaplan/ |
| Model benchmarks | opencode/bench/ (results are git-ignored) |

## Quick start

1. Clone this repo.
2. Pick your harness:
   - **Claude Code**: `./install.sh claude` (agents + hook + settings merge;
     needs jq; remove with `./uninstall.sh claude`). Launch: `claude --agent manager`.
   - **OpenCode**: `./install.sh opencode` (agents, oc-preset, presets, AGENTS.md);
     wire `opencode/opencode.jsonc` per docs/opencode.md, then pick models
     with `opencode/oc-preset`.
   - **Antigravity**: `./install.sh antigravity` (plugin + `agyo`); enable the
     plugin per docs/antigravity.md.
   Uninstall skips files you edited since installing; add --purge to remove them anyway (backed up first).
3. Read [docs/policies.md](docs/policies.md) before changing anything.

## Support status

Linux validated end-to-end on all three harnesses. macOS and WSL:
untested — see docs/megaplan/backlog.md (b06 validation matrix).

Nothing here auto-installs personal config: no MCP endpoints, no
credentials — only commented placeholders (see docs/policies.md,
Provider prerequisites).
