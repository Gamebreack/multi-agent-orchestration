# Delegation-first multi-agent setup for Claude Code

A small, native Claude Code configuration (agents + one hook + one settings entry) in which
the foreground **Manager** only plans, delegates and reconciles, and **never modifies the
repository itself**. Built and validated on Claude Code **2.1.263**.

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

## 1. Architecture

* `manager` runs as the **main session** (`claude --agent manager`). Its system prompt
  replaces the default Claude Code prompt; your `CLAUDE.md` files still load.
* Every other role is a **subagent** the manager spawns with the `Agent` tool. Subagents
  get their own tool lists from their frontmatter, independent of the manager's list, so the
  manager can be tool-starved while workers keep Edit/Write/Bash (verified, see §12).
* Two enforcement layers keep the manager read-only: (a) its `tools:` frontmatter contains
  no Edit/Write/Bash/NotebookEdit and only `Agent(<six roles>)`; (b) the `PreToolUse` hook
  `manager-boundary.sh` denies anything outside an allow-list whenever the acting agent is
  `manager` (`agent_type` in the hook input).

## 2. Agents (`~/.claude/agents/*.md`)

| Role | Model | Effort | Tools | Purpose |
|---|---|---|---|---|
| `manager` | fable | high | Read, Grep, Glob, LSP, Agent(explorer, mechanical-worker, worker, hard-worker, reviewer, verifier), SendMessage, TaskStop, TodoWrite, WebFetch, WebSearch, Skill, ToolSearch, MCP resources, `mcp__asana`, `mcp__ai-memory`, `mcp__claude_ai_Supabase`, `mcp__supabase-dev`, `mcp__supabase-prod`, `mcp__n8n` | intent → decomposition → delegation → reconciliation |
| `explorer` | haiku | default | Read, Grep, Glob, LSP | read-only repository discovery (maxTurns 25) |
| `mechanical-worker` | haiku | default | Read, Grep, Glob, LSP, Edit, Write, NotebookEdit, Bash | cheap deterministic edits (maxTurns 40) |
| `worker` | sonnet | medium | Read, Grep, Glob, LSP, Edit, Write, NotebookEdit, Bash, WebFetch | default implementation |
| `hard-worker` | opus | high | same as worker | genuinely difficult implementation only |
| `reviewer` | opus | high | Read, Grep, Glob, LSP | independent adversarial review, read-only |
| `verifier` | sonnet | default | Read, Grep, Glob, LSP, Bash (Edit/Write/NotebookEdit disallowed) | tests / builds / lint / acceptance checks |

No role has the `Agent` tool except the manager, so there is no recursive delegation.
The two haiku roles carry a `maxTurns` cap so a looping cheap agent returns a partial
report for the manager to reroute instead of consuming the usage window.
`mechanical-worker` stayed on **haiku**: in validation it applied every edit correctly and
verified with its own `git diff`; switch `model: haiku` → `sonnet` in its file if it ever
proves unreliable on your codebase.

## 3. Model routing

```
repository discovery              -> explorer          (haiku)
tiny deterministic implementation -> mechanical-worker (haiku)
ordinary implementation           -> worker            (sonnet, medium)
difficult implementation          -> hard-worker       (opus, high)
independent assessment            -> reviewer          (opus, high)
runtime/build/test verification   -> verifier          (sonnet)
```
Aliases `fable`, `opus`, `sonnet`, `haiku` resolve in 2.1.263 to `claude-fable-5-1`, `claude-opus-5`, `claude-sonnet-5`,
`claude-haiku-4-5-20251001` (observed in `modelUsage` during validation).

## 4. Enforcement mechanism

`~/.claude/hooks/manager-boundary.sh` is a `PreToolUse` hook installed twice:

* **globally** in `~/.claude/settings.json` (matcher `*`, arg `--global`): acts only when
  the hook input has `agent_type == "manager"`; any other agent or a plain session passes
  untouched (exit 0, no output).
* **scoped** in `manager.md` frontmatter (arg `--scoped`): exists only while the manager
  runs; treats a missing `agent_type` as the manager itself. Redundant with the global
  entry in 2.1.263 (the main session does report `agent_type: manager`) but keeps the
  boundary if the settings entry is ever removed or the agents are copied elsewhere.

Decision (allow-list, fail-closed for the manager):

```
Read Grep Glob LSP WebFetch WebSearch TodoWrite Task* SendMessage Skill
ToolSearch AskUserQuestion plan-mode tools MCP-resource readers Cron*   -> allow
Agent with subagent_type exactly one of {explorer, mechanical-worker,
              worker, hard-worker, reviewer, verifier}                 -> allow
Agent with anything else (general-purpose, fork, none)                -> deny
mcp__asana__*, mcp__ai-memory__*, mcp__claude_ai_Supabase__*,
mcp__supabase-dev__*, mcp__supabase-prod__*, mcp__n8n__*                 -> allow
ANY other mcp__* (default deny; add coordination servers explicitly)   -> deny
Edit Write MultiEdit NotebookEdit Bash PowerShell Monitor Workflow
EnterWorktree ExitWorktree, and ANY unknown/renamed tool               -> deny
```
Bash is denied wholesale for the manager (no mutating/non-mutating classification), and
so is `Monitor`, whose `command` parameter is also a shell.
Denials return a reason telling the model to delegate. Set `MANAGER_BOUNDARY_LOG=/path`
to log every decision (`time  mode  agent_type  tool  decision`).

## 5. Burst policy (prompt policy)

At most **3 concurrent implementation agents**; group tiny edits by file ownership /
subsystem instead of one agent per change; explorers spawned deliberately; exceed 3 only
for genuinely independent work with a stated benefit. A platform cap exists too
(`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` env, default 20) but it is global to all your
sessions, so it is intentionally not set here.

## 6. Verification policy (prompt policy)

* trivial low-risk → worker's own check;
* ordinary feature → worker → verifier;
* significant / cross-cutting / risky → workers → reviewer → delegated fixes → verifier → manager reconciliation;
* architectural → explorer → decomposition → (reviewer on plan) → workers → reviewer → fixes → verifier.
Review/verification always in a fresh agent.

## 7. Isolation

Workers run in the current checkout by default. The manager passes
`isolation: "worktree"` on the `Agent` call for concurrent workers with overlapping git
state or substantial independent branches (native Claude Code worktree isolation: branched
from the default branch, changes stay in the worktree/branch). Integration back is itself
delegated to a worker (merge/cherry-pick) and then verified. Trivial single workers are not
put in worktrees.

## 8. Global vs project installation

* **Global (installed):** `./install.sh` copies `agents/*.md` → `~/.claude/agents/`,
  `hooks/manager-boundary.sh` → `~/.claude/hooks/`, and merges one `PreToolUse` entry into
  `~/.claude/settings.json` (backup in `~/.claude/backups/`). Idempotent; unrelated
  agents/hooks/settings are untouched.
* **Project-scoped alternative:** copy `agents/` to `<repo>/.claude/agents/` and the hook
  entry to `<repo>/.claude/settings.json` (project agents override user agents of the same name).
* The manager is **not** made the default for every session (that would make all your
  ordinary sessions unable to edit). To default it for one project, add to that project's
  `.claude/settings.json`:
  ```json
  { "agent": "manager" }
  ```

## 9. Launch

```bash
claude --agent manager            # interactive manager session in the current repo
alias cm='claude --agent manager' # optional
```

## 10. Inspect available agents

Inside a session: `/agents`. Files: `ls ~/.claude/agents/`. Validation runs also confirmed
the manager's own listing: explorer, hard-worker, mechanical-worker, reviewer, verifier,
worker (general-purpose explicitly unavailable).

## 11. Disable / uninstall

```bash
./uninstall.sh          # removes the 7 agents, the hook script and its settings entry only
```
Backups: `~/.claude/backups/settings.json.<timestamp>.bak`. To disable temporarily, just
start `claude` without `--agent manager`: the global hook is a no-op unless
`agent_type == manager`; the only visible difference in ordinary sessions is that the seven
roles appear in the Agent tool's list (see §13).

## 12. Guarantees: HARD vs PROMPT/POLICY

**HARD GUARANTEE (structural / runtime-enforced)**
* Manager has no Edit/Write/NotebookEdit/Bash/PowerShell/Monitor/Workflow/worktree tools (frontmatter) **and** the hook denies them even if present (`Edit`, `Write`, `Bash`, `Monitor`, unknown tools → deny; tested).
* Manager's `Agent` calls can only target the six declared roles (`Agent(...)` allowlist + exact-match hook check; `general-purpose`, `fork`, untyped → denied). See §13 for the SendMessage caveat.
* Manager's MCP access is an allow-list (Asana only); every other MCP server is denied for it.
* Explorer and reviewer have only Read/Grep/Glob/LSP; verifier has no Edit/Write/NotebookEdit (frontmatter `tools`/`disallowedTools`).
* Workers keep Edit/Write/Bash while the manager is denied them (validated end-to-end).
* No role except the manager can spawn subagents.

**PROMPT/POLICY CONVENTION (not technically enforced)**
* Burst cap of 3 concurrent implementation agents and grouping rules.
* Verification/escalation routing (which role handles what; when to review).
* Verifier not mutating the repo through Bash (Bash is not read-only; only prompt forbids it).
* Workers staying inside their assigned file scope and not committing/pushing.
* Worktree use decided per task by the manager.

## 13. Known limitations / remaining loopholes

* **Verifier Bash** could in principle modify files; policy-only.
* **MCP**: only `mcp__asana__*`, `mcp__ai-memory__*`, `mcp__claude_ai_Supabase__*`,
  `mcp__supabase-dev__*`, `mcp__supabase-prod__*` and `mcp__n8n__*` pass for the manager. They
  touch external systems, not the repository. Any other MCP server (including claude.ai
  connectors such as Drive, and any future file-editing server) is denied for the manager; add
  a server to the hook's `mcp__*` allow branch deliberately if the manager needs it.
* **SendMessage** (needed to resume its own workers) lets the manager message other Claude
  sessions/teammates that are not bound by this hook. The hook cannot tell a spawned worker
  from a peer session by name, so this stays **policy**: the manager prompt forbids it.
* **Agent visibility**: user-scope agents are listed in every session's Agent tool. The
  implementation roles carry a "For use by the manager orchestrator" prefix so ordinary
  sessions do not route to them; if you still see that, install project-scoped instead.
* **Renamed manager**: identification is exact-match on `agent_type == "manager"`. Renaming
  the agent file/name or packaging it as a plugin (`plugin:manager`) fails open; update the
  hook's match if you do.
* **LSP for background subagents**: Claude Code strips `LSP` from subagents that run in the
  background (the default), so explorer/reviewer may effectively have Read/Grep/Glob only.
* **Skills**: a skill running inside the manager's context is still hook-checked; a skill that
  itself launches a non-declared agent type would be denied at the `Agent` call, but a
  skill implementation that bypasses the Agent tool is not covered.
* `--agents <json>` at launch can define ad-hoc agents; that is the operator's action, not the manager's.
* Headless `-p` runs cannot answer permission prompts; use the interactive manager or `auto` mode.
* Hook input fields (`agent_type`) are the identification mechanism; if a future Claude
  Code version stops sending `agent_type` for the main session, the scoped frontmatter hook
  still enforces (missing `agent_type` ⇒ manager).

## 14. Same idea on other harnesses

The delegation-first layout was also built on **OpenCode** and **Antigravity CLI (`agy`)**;
the configs live in [`opencode/`](opencode) and [`antigravity/`](antigravity).

* [docs/harness-comparison.md](docs/harness-comparison.md) — how each harness enforces a
  read-only orchestrator, side by side.
* [docs/claude-code-observations.md](docs/claude-code-observations.md) — what broke and what
  had to be true in Claude Code (hooks, auto mode, subagent tools).
* [docs/opencode.md](docs/opencode.md) — OpenCode permission-map version.
* [docs/antigravity.md](docs/antigravity.md) — Antigravity `multitask-team` plugin version, and why its agents never loaded.
