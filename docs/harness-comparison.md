# One idea, three harnesses

The goal is the same everywhere: **the agent you talk to cannot change the repository.**
It reads, plans, delegates, and reconciles; only subagents edit, and verification runs in a
fresh context. This page compares how Claude Code, OpenCode and Antigravity CLI let you
express that, as of September 2026.

| | Claude Code 2.1.263 | OpenCode 2.x (validated 2.0.14) | Antigravity CLI 1.1.27 |
|---|---|---|---|
| Agent definition | `~/.claude/agents/<name>.md` (frontmatter + prompt) | `~/.config/opencode/agents/<name>.md` + `opencode.jsonc` | `agents/<name>/agent.md` (markdown + frontmatter), global, workspace or plugin; shared `rules/AGENTS.md` |
| Orchestrator selection | `claude --agent manager` (per-project default possible via `.claude/settings.json`) | `default_agent` in config | `agy --agent orchestrator-agent` on every launch; falls back silently, so use the `agyo` wrapper |
| Read-only enforcement | frontmatter `tools:` **plus** a `PreToolUse` hook (allow-list, fail-closed) | per-agent permissions arrays, `"*"/"*" → deny` first | frontmatter `tools:` whitelist (verified after the 2026-09-08 rewrite; the earlier JSON format never loaded) |
| Granularity | tool name; MCP by server prefix in the hook | tool name, shell per command pattern, read per file glob, MCP per prefix | tool name |
| Who may spawn | manager only: `Agent(<six roles>)` | `subagent` rules on the orchestrator; `experimental.subagent_depth: 1` | orchestrator has `invoke_subagent`; workers do not |
| Model per role | `model` alias + `effort` | one provider, `model#variant` | `customAgent.model`, else session model |
| Cheap tier | haiku explorer/mechanical-worker with `maxTurns` | none (variant `medium`) | none pinned |
| Worker runs its own tests | yes (worker has Bash) | yes, allow-listed commands; others `ask` | **no** — writer has no shell; reviewer runs tests |
| Independent verification | `verifier` (sonnet) + `reviewer` (opus) | `reviewer` on request | `reviewer-agent`, mandatory in the loop |
| Retry policy | prompt policy, manager decides | resume same `task_id` with feedback | hard circuit breaker: 3 heal iterations, then escalate |
| Worktree isolation | native `isolation: "worktree"` per Agent call | not used | not used |
| Remaining shell loophole | verifier Bash (policy-only) | none for read-only roles; implementer bash is `ask` | reviewer `run_command` (policy-only) |

## What each harness taught us

**Claude Code** needs two layers because frontmatter `tools:` alone is not checked for MCP
servers, renamed tools, or the `Agent` target type; the hook covers those. In exchange it is
the only one of the three where the *main* session identifies itself to hooks
(`agent_type`), so a single global hook can enforce the boundary without touching other
sessions. Its failure modes were about hooks and auto mode, not about the agents
(see [claude-code-observations.md](claude-code-observations.md)).

**OpenCode** has the most complete permission model and needed no extra mechanism: deny by
default, allow per tool, per bash pattern, per file glob, per MCP prefix, and restrict which
subagents an agent may `subagent`. Its trap is discoverability: an MCP server that is connected
but not allow-listed simply has no tools, with no error
(see [opencode.md](opencode.md)).

**Antigravity** enforces through a tool whitelist, which is simple and effective but coarse:
there is no "bash but only tests", so the writer gets no shell at all and every verification
is a second agent. Its trap is the silent fallback when `--agent` names a non-existent agent
(see [antigravity.md](antigravity.md)).

## Design choices that carried across all three

* Read-only orchestrator with **no shell at all**; no attempt to classify commands as safe.
* Delegation depth of one: no worker can spawn workers.
* Review and verification always in a **fresh** agent, never by the author.
* Workers get a self-contained brief: goal, in/out-of-scope paths, acceptance criteria,
  required verification, and must report files changed + commands run + failures.
* Prompt-level rules that no harness enforces yet: no overlapping edits between concurrent
  workers, no worker commits (push is hard-denied on OpenCode), a cap on concurrent implementers.

## What the logs say about each boundary in practice

* **Claude Code**: the hook never had to deny a manager edit; what fired was auto-mode's
  classifier on *worker* commands, and a pre-existing Stop hook inside subagents.
* **OpenCode**: the orchestrator never attempted `edit`/`bash` in 17 sessions. The rule that
  did fire was `external_directory: deny`, and the implementer routed around it with
  `bash` + `python -c`, so a directory boundary only holds for agents without a shell.
* **Antigravity**: until 2026-09-08 no boundary existed. The plugin's `agent.json` files were
  not the format the CLI scans (it wants `agents/<name>/agent.md`), so every `--agent
  orchestrator-agent` launch silently fell back to the default, fully privileged agent, which
  read the plugin's rules, claimed to be the orchestrator, and built its own write-enabled
  subagents with `define_subagent`. After the markdown rewrite the `tools:` whitelist holds
  (verified by tool listing, a delegation smoke test and a scoping probe). The terminal
  sandbox blocked the reviewer's `git commit` with a read-only `.git`.

Details and numbers: [opencode.md](opencode.md#observations-from-the-session-logs),
[antigravity.md](antigravity.md#observations-from-the-conversation-logs),
[claude-code-observations.md](claude-code-observations.md).

## Pending

Subjective assessments (orchestration quality, reviewer value, latency of the mandatory
review hop in Antigravity) are deferred to a follow-up discussion.
