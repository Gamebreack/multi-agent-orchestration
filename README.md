# multi-agent-orchestration

Two things live here:

- **Hybrid ICM workflow** — numbered stages organize each work item;
  specialist agents execute the stage work. This repo runs it live, and
  `starter/` is the copyable template for using it in other projects.
- **agent-core** (in specification) — a generic agent factory: define any
  agent once (prompt, model provider, allowed tools and MCPs, who may use
  it), package it as a container, and deploy it to any Docker host
  reachable over SSH.

## What is where

| You want... | Go to |
|---|---|
| Repo conventions | [AGENTS.md](AGENTS.md) |
| Repo routing and workflow | [CONTEXT.md](CONTEXT.md), stages/ |
| Start a new project with this workflow | [starter/README.md](starter/README.md) |
| agent-core proposal | [openspec/changes/agent-core/proposal.md](openspec/changes/agent-core/proposal.md) |
| Work backlog | [docs/megaplan/backlog.md](docs/megaplan/backlog.md) |

Nothing here carries personal config: no MCP endpoints, no credentials, no
machine-specific paths.
