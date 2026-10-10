# Proposal

## Why

Today the repo ships agent definitions per harness (Claude Code, OpenCode,
Antigravity); each harness enforces policy differently and only partly.
The operator wants an agent factory they own: define any agent once, give it
exactly the tools, MCPs and users it may have, and deploy it to any host —
building an ecosystem of compatible agents rather than configuring third-party
harnesses.

## What Changes

- New **agent-core**: a generic, TypeScript agent factory built on the
  Strands Agents TypeScript SDK as its single shared engine (not swappable),
  so every agent it produces is compatible with every other.
- An agent is defined by one folder: `agent.yaml` (model/provider, allowed
  tools, MCP servers and their allowed tools, access), `prompt.md` (system
  prompt), and `tools/*.ts` (custom tools in code). Rules and access live in
  data so agent-core can check them without running agent code.
- Tool and MCP access is deny-by-default and enforced in code per agent
  (allowlists + pre-tool-call gate). Calling another agent is an ordinary
  tool, governed by the same rules — no separate inter-agent mechanism.
- Model provider is chosen per agent (Bedrock, Anthropic, OpenAI, Gemini
  natively; others via an adapter).
- Identity via OIDC, copying the megabrain auth pattern (not sharing its
  code): one auth server per ecosystem issues short-lived tokens; each agent
  verifies them and checks the caller's role **for that agent** on every
  call; identity and permission stay separate; every action records its actor.
- Each agent is packaged as its own container image and deployed with Kamal
  to any Docker host (VPS, Railway, AWS, GCP).
- A CLI is the first interface; other interfaces (HTTP API, chat, web) can be
  added later without changing the core.
- Hybrid ICM is unchanged: it remains this repo's way of working and the
  reusable starter.

## Capabilities

### New Capabilities
- `agent-definition`: the agent folder format (`agent.yaml`, `prompt.md`, `tools/`), its schema and validation.
- `tool-access-control`: per-agent tool and MCP allowlists, deny-by-default gate before every tool call, agent-as-tool calls.
- `agent-runtime`: building and running an agent from its definition on the shared Strands engine with its chosen provider.
- `identity-access`: OIDC login, token verification, per-agent roles revalidated on each call, actor provenance.
- `agent-deploy`: one container image per agent, deployed with Kamal to any Docker host.
- `agent-cli`: the command-line interface to define, run, build and deploy agents.

### Modified Capabilities
<!-- none: no specs exist yet -->

## Impact

- New TypeScript codebase (location in this repo vs a separate repo still to
  decide in design).
- New dependencies: Strands Agents TS SDK, an OIDC provider library, a JWT
  verification library, Postgres for accounts/roles, Docker, Kamal.
- Existing harness toolkits (`agents/`, `opencode/`, `antigravity/`),
  `stages/` and `starter/` are not modified by this change.
- Open questions for design: whether Strands TS can load agents from config
  or agent-core translates `agent.yaml` into code; Ollama/LiteLLM via the
  Vercel AI SDK adapter is unverified.
