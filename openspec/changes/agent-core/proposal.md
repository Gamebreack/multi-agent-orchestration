# Proposal

## Why

Third-party agent harnesses gave only partial, harness-specific control over
what an agent may touch and who may use it, and that toolkit is now removed
(archived repo-cleanup change), leaving this repo nothing to build or deploy
agents with. The operator wants an agent factory they own: define any agent
once with exactly the tools, MCPs and users it may have, and deploy it as
part of an ecosystem of compatible agents.

## What Changes

- New **agent-core**: a generic, TypeScript agent factory built on the
  Strands Agents TypeScript SDK as its single shared engine (not swappable)
  and one task protocol, so every agent it produces is compatible with every
  other.
- An agent is defined by one folder: `agent.yaml` (model/provider, allowed
  tools, MCP servers and their allowed tools, the agent's roles and what each
  role may do), `prompt.md` (system prompt), and `tools/*.ts` (custom tools
  in code). Rules live in data so agent-core can check them without running
  agent code.
- Tool and MCP access is deny-by-default and enforced in code per agent
  (allowlists + pre-tool-call gate), narrowed further by the caller's role.
  Calling another agent is an ordinary tool — agent-core's gateway client —
  governed by the same rules; no separate inter-agent mechanism.
- Model provider is chosen per agent from those the Strands TS SDK supports.
- Identity via OIDC with email + password login. One auth server per
  ecosystem; the token proves who the caller is, and which role a person
  holds on each agent is stored in the database and checked on every task.
  Each agent is its own access domain: a call from agent A to agent B runs
  as the original person, so it fails unless that person holds a role on B.
  Every task records its actor.
- Tasks reach agents through a **gateway** and a **Postgres-backed queue**:
  callers (the CLI, other agents) send a task with their token to the
  gateway; the gateway has the caller's role on the target agent checked
  and enqueues the task with that role and actor attached; the agent's
  container takes it from the queue and returns the result the same way.
  Each agent's database login can only take its own tasks and write its own
  results — it cannot enqueue tasks or read accounts and role grants.
- Each agent is packaged as its own container image and deployed with Kamal
  to any Docker host reachable over SSH (a VPS, AWS or GCP VMs), alongside
  the gateway, auth server and Postgres. Hosted platforms without SSH access
  (e.g. Railway) are out of scope for now.
- A CLI is the first interface, used to define, run, build and deploy
  agents and to send them tasks; other interfaces (chat, web) can be added
  later on top of the gateway without changing the core.

## Capabilities

### New Capabilities
- `agent-definition`: the agent folder format (`agent.yaml`, `prompt.md`, `tools/`), its schema and validation.
- `tool-access-control`: per-agent tool and MCP allowlists, per-role limits within them, deny-by-default gate before every tool call, agent-call tool.
- `agent-runtime`: building and running an agent from its definition on the shared Strands engine with its chosen provider.
- `identity-access`: email + password OIDC login, token verification, per-agent role grants and the check against them, acting as the original person across agent calls, actor provenance.
- `task-dispatch`: the gateway (which calls the identity-access check) and the Postgres-backed queue that carries tasks, with role and actor, to agents and results back; least-privilege queue access.
- `agent-deploy`: one container image per agent, plus gateway, auth server and Postgres, deployed with Kamal to any SSH-reachable Docker host.
- `agent-cli`: the command-line interface to define, run, build and deploy agents and send them tasks.

### Modified Capabilities
<!-- none: no specs exist yet -->

## Impact

- New TypeScript codebase (location in this repo vs a separate repo still to
  decide in design).
- New dependencies: Strands Agents TS SDK, Docker, Kamal, Postgres (accounts,
  role grants and the task queue); OIDC server, token-verification and queue
  libraries (choices in design).
- `stages/` and `starter/` (hybrid ICM) are not modified by this change.
- Strands TS support for what this proposal relies on was confirmed by
  reading the SDK source (typescript/v1.20.0, 2026-10-08), not by running it:
  pre-tool-call cancel hook (`strands-ts/src/hooks/events.ts`), per-server MCP
  tool allow/reject filters and stdio/HTTP transports (`strands-ts/src/mcp/`),
  built-in Bedrock, Anthropic, OpenAI and Gemini providers
  (`strands-ts/src/models/`) — all in
  https://github.com/strands-agents/harness-sdk. (Strands' agent-as-tool
  wraps a local agent; agent-core's agent-call tool goes through the gateway
  instead.)
- Open questions for design: whether Strands TS can load agents from config
  or agent-core translates `agent.yaml` into code; Ollama/LiteLLM via the
  Vercel AI SDK adapter is unverified; how results stream back to the CLI
  while a task runs; whether a local development `run` skips the gateway.
