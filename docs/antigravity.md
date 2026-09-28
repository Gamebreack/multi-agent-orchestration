# Antigravity CLI (`agy`): the `multitask-team` plugin

Files: [`antigravity/multitask-team/`](../antigravity/multitask-team) — `plugin.json`,
`rules/AGENTS.md`, `agents/<name>/agent.md`.
Install with `./install.sh antigravity` (copies the plugin to `~/.gemini/config/plugins/multitask-team/` and `agyo` to `~/.local/bin/`, backing up any existing file that differs; `GEMINI_CONFIG_DIR`/`AGYO_BIN_DIR` override the targets).
Enable it in `~/.gemini/config/config.json`
(`{"plugins": {"multitask-team": {"enabled": true}}}`). Launch with
[`antigravity/agyo`](../antigravity/agyo), a wrapper that refuses to start unless
`agy agents` lists the orchestrator (plain `agy --agent orchestrator-agent` falls back to the
default agent silently, see below). Built against Antigravity CLI **1.1.27**.

```
                orchestrator-agent  — read + search + invoke_subagent; no write, no run_command
                        │
     ┌─────────┬────────┼──────────┬─────────────┐
  writer    reviewer  researcher  documenter   planner (Gemini 3.1 Pro High)
  write      run_cmd   web+read    write docs   read-only
  no shell   no write  no write    no shell
```

## How the boundary is enforced

Agents are markdown files with frontmatter; the `tools:` list is a **whitelist**: a tool not
listed does not exist for that agent (verified: the orchestrator, asked to list its tools,
reports exactly its eleven declared tools plus the always-present `manage_task`). There is no
per-agent permission map and no hook, so the whitelist is the whole enforcement layer:

| Agent | `tools:` (summary) | can write | can run shell |
|---|---|---|---|
| `orchestrator-agent` | view_file, list_dir, grep_search, find_by_name, search_web, read_url_content, ask_question, invoke_subagent, manage_subagents, send_message, schedule | no | no |
| `writer-agent` | view_file, write_to_file, replace_file_content, multi_replace_file_content, send_message | yes | **no** |
| `reviewer-agent` | view_file, grep_search, run_command, manage_task, send_message | no | yes |
| `researcher-agent` | view_file, list_dir, grep_search, find_by_name, search_web, read_url_content, send_message | no | no |
| `documenter-agent` | same as writer | yes (docs only, by prompt) | no |
| `planner-agent` | view_file, list_dir, grep_search, send_message, ask_question | no | no |

Two consequences differ from the other harnesses:

* **The writer cannot run tests.** Verification is always a second hop through
  `reviewer-agent`, which is the only agent with `run_command`. The `rules/AGENTS.md`
  protocol turns that into a fixed loop: baseline run → write → review/test → up to
  **3 heal iterations**, then hard stop and escalate to the user.
* **The reviewer's shell can write.** `run_command` is not read-only; the prohibition on
  `>`, `sed -i`, `rm`, `mv`, `tee` etc. lives in its prompt and in the rules file only.
  Same policy-only gap as Claude's `verifier` Bash.

`rules/AGENTS.md` is loaded for every agent of the plugin and states the protocol once,
which is where the delegation matrix and circuit breaker are written.

## Model routing

Per-agent model is set with `config.customAgent.model` and only `planner-agent` pins one
(`Gemini 3.1 Pro (High)`). Every other agent inherits the session model from
`~/.gemini/antigravity-cli/settings.json` (`"model": "Gemini 3.8 Flash (Medium)"` at the time
of writing). Which model should orchestrate (3.1 Pro vs 3.8 Flash) was researched in-session
and not settled.

## Global settings that matter

In `~/.gemini/antigravity-cli/settings.json`: `agentMode: accept-edits`,
`toolPermission: always-proceed`, `enableTerminalSandbox: true`, and a `permissions.allow`
list of `command(<name>)` entries (echo, find, ls, cat, git log/status/diff, pytest, ruff,
mypy). These are session-wide, not per agent: the per-agent restriction comes only from
`toolNames`.

## Observations from the conversation logs

Source: `~/.gemini/antigravity-cli/history.jsonl`, `log/cli-*.log`, and the per-conversation
SQLite files under `conversations/` (protobuf payloads, read with a strings scan, so counts
are approximate).

**How it was built.** The plugin dates from 2026-07-07 (first `planner-agent`); the current
orchestrator/writer/reviewer/researcher/documenter set and `rules/AGENTS.md` were produced on
2026-09-06 in a single 10-minute conversation: request → `/plan review it adversarially` →
`/plan go`. Two harness limits surfaced while the agent wrote the plugin: `write_to_file`
refused a path with "is not a valid artifact path; artifacts must be in `~/.gemini/`", and
the agent ran `strings agentapi | grep -i defaultagent` looking for a default-agent setting
and found none, which is why launch is `agy --agent orchestrator-agent`.

**Root cause: the plugin agents were never loaded. Wrong file format.** Every launch
with `--agent orchestrator-agent` in the logs (2026-09-07 10:07, 2026-09-08 16:52, 16:53,
18:15) produced
`overrides.go:39] Agent "orchestrator-agent" not found, falling back to default`, and
`agy agents` lists nothing for this plugin. Verified on 1.1.27 with two probes:

| probe | discovered by `agy agents`? |
|---|---|
| `~/.gemini/config/agents/<name>.md` (markdown + frontmatter) | yes |
| `~/.gemini/config/plugins/<p>/agents/<name>.md` | yes |
| `~/.gemini/config/plugins/<p>/agents/<name>/agent.json` with `config.customAgent` (what `multitask-team` ships) | **no** |

The official page for the `/agents` command documents `~/.gemini/config/agents/<name>/agent.md`
and `<workspace>/.agents/agents/<name>/agent.md` with `name` and `description` frontmatter;
the changelog adds a `model` option and `subagent: false` (1.1.5), and notes that agent
definitions moved from JSON to Markdown in 1.0.16. The `agent.json` + `customAgent` +
`toolNames` shape used here came from web-search summaries during the design session, which
themselves hedged ("some implementations require `customAgentSpec` instead of
`customAgent` depending on the CLI version"). It matches an internal proto name that appears
in the binary, not the on-disk format the CLI scans.

What actually ran in every "orchestrator" session, therefore, was the **default agent**:

* the plugin's `rules/AGENTS.md` *is* loaded (rules are a supported plugin part), so the
  default agent read "when running as the Orchestrator, never edit" and answered
  "Yes, I am the orchestrator (`orchestrator-agent`)" when asked;
* `invoke_subagent writer-agent` fails with `subagent "writer-agent" not found or not
  allowed to be invoked`, so the agent calls `define_subagent` and creates ad-hoc
  `writer-agent` / `reviewer-agent` with `enable_write_tools: true` (shell included, for the
  reviewer too); `define_subagent` appears in every one of these conversations;
* the main agent kept itself read-only only because the rules text said so, and confinement
  to the workspace was not in effect (one ad-hoc writer populated a user-wide directory).

Nothing in the TUI distinguishes this from the real plugin. The only reliable check is the
log line: `grep 'not found, falling back' ~/.gemini/antigravity-cli/cli.log` after launch.

**Fix applied 2026-09-08.** Each agent was rewritten as `agents/<name>/agent.md`
(frontmatter `name`, `description`, `tools`, `subagent`, `hidden`, `model: pro` for the
planner; body = former prompt sections). The old JSON is kept under
`antigravity/legacy-json/` as the record of what did not load. Verified after install:

* `agy agents` lists all six agents; no `not found, falling back` line in the launch logs.
* Orchestrator tool list, reported headlessly: the eleven declared tools + `manage_task`; no
  `write_to_file`, `replace_file_content`, `run_command`, `define_subagent`.
* Delegation smoke test: "create a file containing PASS, you must not write yourself" produced
  the file via `writer-agent`; the orchestrator's trajectory has no write or command calls.
* Subagent scoping: `invoke_subagent general-purpose` and a made-up name both fail with
  `not found or not allowed to be invoked`, so the orchestrator can reach only registered
  plugin/global agents. Workers carry `subagent: true` + `hidden: true`.

**The terminal sandbox makes `.git` read-only for delegated commands.** With
`enableTerminalSandbox: true`, the reviewer-agent's `git add`, `git commit` and
`git checkout -b` were blocked (`SANDBOX_COMMAND_BLOCKED`, output
`Unable to create '.git/index.lock': Read-only file system`, `cannot lock ref`). The commits
and the pushed branch do exist afterwards, so the retry path outside the sandbox worked, but
the mechanism of that retry was not captured in the logs. Since the writer has no shell and
the reviewer is the only agent with `run_command`, every commit in this layout goes through
the sandbox first.

**Model routing was questioned, not settled.** A 30-minute conversation on 2026-09-07 asked
which model each agent runs and whether Gemini 3.1 Pro or 3.8 Flash should orchestrate; the
orchestrator researched benchmarks (some fetches 404'd), grew verbose enough to be told to be
brief, and the question stayed open. The same conversation logged two
`503 No capacity available for model gemini-3.1-flash-lite` errors from a background model
the plugin does not name, so capacity errors can come from the harness's own helpers.

**Real delegated tasks (2026-09-08).**

1. From `~/Projects`, an evidence-based audit of the operator's work across several local
   repositories: two `reviewer-agent` runs did the read-only git analysis (39 and 150
   `run_command` calls), one `documenter-agent` run wrote the report (5 `write_to_file`),
   the orchestrator itself only viewed and listed files. No errors, no circuit-breaker trips.
2. In a Python project, a full change cycle: baseline reviewer runs (`git status`, unit
   tests, CLI checks), a **panel of five parallel `reviewer-agent` instances** each given a
   different question (acceptance, test adequacy, regression, contract boundaries,
   invariants; one returned a BLOCKER plus two SHOULD_FIX), a `writer-agent` run applying
   the atomic fix list (44 `replace_file_content`), re-verification, then commit, push and a
   PR on a new branch via the reviewer's shell. About 18 sub-conversations in 50 minutes.
   The plugin roles composed with the operator's own verification methodology without
   changes to the agents.

That is the layout working as designed: reads in the orchestrator, shell in the reviewer,
writes in the writer/documenter. The reviewer's prompt-only shell-write prohibition was
exercised only by the orchestrator's own choice to route commits through it; no
`>`/`sed -i`/`rm` appears in reviewer commands.

**`agy agents` prints nothing outside a logged-in interactive session**, so the roster has to
be read from the plugin directory.

**Still to discuss.** Whether the mandatory writer → reviewer hop is worth the latency on
small edits, and how the writer copes without any shell on projects with formatters.
