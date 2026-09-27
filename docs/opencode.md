# OpenCode: the same delegation-first layout

Files: [`opencode/opencode.jsonc`](../opencode/opencode.jsonc),
[`opencode/agents/*.md`](../opencode/agents), [`opencode/AGENTS.md`](../opencode/AGENTS.md).
Install with `./install.sh opencode` (copies agents/, oc-preset, presets/ and AGENTS.md to `~/.config/opencode/`, backing up any existing file that differs; `OPENCODE_CONFIG_DIR` overrides the target). Config wiring (opencode.jsonc) and personal MCP allow rules stay manual — see the orchestrator template's permissions comment.
Built against OpenCode **1.18.29**; the model split and `external_directory: ask` were applied on 2.0.14 (2026-09-22). Supported: OpenCode 2.x.

```
                 orchestrator  (primary, gpt-6-astra, high) — read-only, no shell
                       │  subagent: only these seven
   ┌────────┬──────────┼────────────┬──────────────────┬───────────┬──────────┐
 explore  scout   mechanical   implementer   hard-implementer   verifier   reviewer
 luna-fast luna     luna          terra            sol            terra       sol
 medium   medium   medium        medium           high           medium      high
 read     read    edit+shell    edit+shell      edit+shell    shell only   read
 only     only   (allow-list)  (allow-list)    (allow-list)  (allow-list)  only
```

## How the boundary is enforced

OpenCode has a **per-agent permission model built in**, so no hook is needed. Every agent
file's `permissions:` array starts with a `{ action: "*", resource: "*", effect: deny }`
item and then allows individual tools:

| Agent | mode | edit | shell | subagent (spawn) | notes |
|---|---|---|---|---|---|
| `orchestrator` | primary | deny | deny | the seven subagents below only | `question`, `todowrite`, `skill`, MCP prefixes allowed once the operator appends matching allow rules |
| `mechanical`, `implementer`, `hard-implementer` | subagent, hidden | allow | **ask** by default, allow-list of read-only git and test/lint/typecheck runners, explicit deny of push/reset/checkout/rm/sudo/deploy | deny | same permissions array, different model tier; reads `.env*` denied except `.env.example` |
| `verifier` | subagent, hidden | deny | same allow-list as the implementers | deny | runs checks, never edits |
| `reviewer` | subagent, hidden | deny | deny | deny | `question`/`todowrite` denied |
| `explore`, `scout` | subagent, hidden | deny | deny | deny | `.md` files, same as the rest |

Other structural settings in `opencode.jsonc`:

* `default_agent: orchestrator` makes the orchestrator the agent you talk to. This is the
  one thing Claude Code and Antigravity do not offer as a plain user-scope setting.
* `experimental.subagent_depth: 1` forbids subagents spawning subagents, the equivalent of
  no worker having the `Agent` tool in the Claude setup.
* The built-in `build`, `plan` and `general` agents are **disabled** via
  `agents.*.disabled: true` so nothing with write access is reachable from the primary
  session except through `implementer`.
* Subagents are `hidden: true` so they do not appear as selectable primary agents.
* `external_directory: ask` everywhere: a tool call outside the workspace prompts instead of
  failing. It was `deny` until 2026-09-22; see the observation below on why that was porous anyway.

## OpenCode 2.x pitfalls (found 2026-09-22)

* **Server restart, not TUI restart.** The background server (`opencode serve --service`, a
  systemd user unit) outlives the TUI. Config hot-reloads, but MCP tool discovery happens at
  server start, and a server that started before MCP auth holds zero MCP tools until
  `opencode service restart`.
* **`mcp.servers` form and `codemode: false`.** Legacy `mcp.<name>` entries are migrated with
  a v1 schema that drops `codemode`. Under `mcp.servers.<name>` the flag survives. With the
  default `codemode: true` MCP tools are only reachable through the Code Mode `execute` tool,
  which `"*": deny` hides; with `false` they are direct `<server>_<tool>` tools.
* **Rule order.** The `permissions:` array is an ordered ruleset where the last match wins. The
  agent's `- { action: <server>_<tool>, resource: "*", effect: allow }` items are appended
  after the `{ action: "*", resource: "*", effect: deny }` catch-all in the file, and the
  per-agent `tools:` map must not be used for MCP: the migrator emits its rules before the
  catch-all and drops the later duplicates, which hides every MCP tool again.
* Verified with a temporary plugin hooking the session `context` event: the orchestrator's
  request carried 48 MCP tools after the fixes, zero before.

## Model routing

One provider (`openai/…`) with the model tier doing what the Haiku / Sonnet / Opus / Fable
split does in the Claude Code layout, and the **variant** suffix doing what `effort` does.
Both live on a single frontmatter line, `model: provider/model#variant`:

| OpenCode agent | `model:` (`provider/model#variant`) | Claude Code counterpart |
|---|---|---|
| `orchestrator` | `openai/gpt-6-astra#high` | `manager` (fable) |
| `explore` | `openai/gpt-6-luna-fast#medium` | `explorer` (haiku) |
| `scout` | `openai/gpt-6-luna#medium` | `explorer` (haiku), web side |
| `mechanical` | `openai/gpt-6-luna#medium` | `mechanical-worker` (haiku) |
| `implementer` | `openai/gpt-5.6-terra#medium` | `worker` (sonnet) |
| `hard-implementer` | `openai/gpt-6-sol#high` | `hard-worker` (opus) |
| `verifier` | `openai/gpt-5.6-terra#medium` | `verifier` (sonnet) |
| `reviewer` | `openai/gpt-6-sol#high` | `reviewer` (opus) |

The premise is the same as in Claude Code: the orchestrator carries the judgment and the
cheap tiers do the volume. Until 2026-09-22 every agent ran on `gpt-5.6-luna`, the cheapest
tier, with `max`/`high`/`medium` variants as the only differentiation.

## Provider presets

[`opencode/presets/openai.tsv`](../opencode/presets/openai.tsv) and
[`opencode/presets/go.tsv`](../opencode/presets/go.tsv) list a 2-column
`agent<TAB>provider/model[#variant]` row per agent for
two providers; [`opencode/oc-preset`](../opencode/oc-preset) rewrites all 8 `agents/*.md` files
in one call:

```
~/.config/opencode/oc-preset go      # move every agent to OpenCode Go models
~/.config/opencode/oc-preset openai  # move back
~/.config/opencode/oc-preset         # show current models and which preset matches, if any
```

This only works because `model` lives in exactly one place: OpenCode resolves an
agent's model from `opencode.jsonc` before its `.md` frontmatter, so a value split across both
places would leave the JSON edit silently ignored. `explore` and `scout` were moved from
`opencode.jsonc` into `agents/*.md` for this reason (2026-09-22).

The `go.tsv` rows come from three bench rounds (`opencode/bench/results/20260922-161138`, `20260923-102656`, and `20260923-111846` for a MiMo rerun); 12 of 14 finalists passed every task, so choices were made on cost, speed and reliability rather than pass rate. glm-5.2 (orchestrator, reviewer: 10/10 tasks, fastest non-flash, same review recall as deepseek-v4-pro at ~1/6 the wall time) leads; hard-implementer uses mimo-v2.6-pro — 17/19 runs over three rounds, all completed runs 1.00, ~half the token cost of deepseek-v4-pro, chosen for cost; slower (210–300 s on refactor-02) with one provider stream error, deepseek-v4-pro offered as substitute. deepseek-v4.1-flash holds scout/explore (10/10, score 1.00, fastest and cheapest overall). Implementer, verifier, and mechanical use mimo-v2.6-flash — 17/19 runs across three rounds, every completed run scored 1.00, ~2× cheaper than deepseek-v4.1-flash, chosen by the user for cost; its two failures (a 600 s timeout and a provider stream error) were on read-heavy review tasks, which is why it does not hold the read-only seats. Excluded: kimi-k2.7-code (patched symptom in fix-03), kimi-k3/grok-4.7/qwen maxes (10–40× cost for equal results). Go metering is account-level; real spend ran 2.3–3.2× the catalog-price estimate.

## Compared with the Claude Code setup

* Same roles, one split: `explorer` → `explore` (local) + `scout` (web). `mechanical-worker`,
  `worker`, `hard-worker`, `verifier` and `reviewer` map one to one. The orchestrator prompt
  carries the same routing table and verification policy as the manager prompt.
* Enforcement is **declarative** (permissions array) instead of a `PreToolUse` hook. The
  granularity is finer than Claude's: shell commands are allow-listed per command pattern and
  file reads can be denied per glob.
* The orchestrator prompt carries the same policy items as the manager prompt: no
  overlapping edits across workers, resume the same task by `task_id` instead of spawning a
  duplicate, delegate instead of asking a read-only agent to write.

## Observations from the session logs

Source: OpenCode's local database (`~/.local/share/opencode/opencode.db`, tables `session`,
`message`, `part`), 29 sessions between 2026-09-06 and 2026-09-07. Numbers below come from
those rows.

**How it was built.** The whole design was done inside the built-in `plan` agent
(gpt-5.6-sol, medium) in one 22-hour session, which researched online, wrote the three agent
files, then validated them headlessly with `opencode run --pure --agent orchestrator "Smoke
test only ... delegate the edit to implementer"` in a temp directory. The built-in agents were
disabled afterwards.

**Smoke tests (2026-09-07 10:32–10:34).**

| Run | Outcome | Cause |
|---|---|---|
| 1 | failed | implementer pinned to `gpt-5.4`; provider replied `The 'gpt-5.4' model is not supported when using Codex with a ChatGPT account` |
| 2 | failed | implementer's `bash` to create the file hit `ask`; headless run cannot answer, so `The user rejected permission` |
| 3 | passed in 26 s | model switched to `gpt-5.6-luna`, run with `--auto` |

In both failures the orchestrator reported honestly ("Unable to complete: ... the file was not
created") instead of writing the file itself. Across all 17 orchestrator sessions there is
**no** `edit`, `bash` or `apply_patch` call from the orchestrator, denied or otherwise: the
permission map never had to fire because the prompt already kept it in role.

**Delegation shape.** 14 `task` calls in total: 10 to `implementer`, 2 to `explore`, 2 that
resumed an existing implementer task by `task_id` (the "same worker, more feedback" rule in
the orchestrator prompt is used in practice). Task wall-clock ranged from 26 s (smoke file) to
973 s (a config investigation that ended up running `strings` on the OpenCode binary).

**`external_directory: deny` is porous through bash.** The implementer was asked several
times to edit the *global* config under `~/.config/opencode/`, outside the workspace. `read`,
`glob` and `apply_patch` on those paths were denied by the rule (15 read errors, 5 glob
errors, 4 apply_patch errors in implementer sessions), so the agent fell back to
`bash` + inline `python -c` to read and rewrite the same files, and that went through because
bash is governed by the command allow-list, not by the directory rule. Net effect: the
directory boundary holds only for agents without `bash`. `explore`, which has no bash,
reported "could not audit: read access to `~/.config/opencode/` was blocked".

**MCP tools invisible without a prefix rule (the long afternoon).** A Trello MCP server was
added at 12:36 and authenticated. The orchestrator then spent three sessions failing to use
it: it tried `webfetch` against Trello URLs (401) instead, and `list_mcp_resources` (the
server exposes no resources, only tools). Root cause found by the implementer at 14:19: the
orchestrator's `"*": deny` hid every `trello_*` tool because no allow rule matched. Because
the config is only read at startup, the implementer verified each fix by launching fresh
sessions with `opencode run --agent orchestrator "Read-only diagnostic ... list the exact
injected tool names"`: eight such sessions appear in the log between 14:23 and 15:08. The
same round-trip repeated for two remote Supabase servers, where the open question was whether
the injected prefix keeps the hyphen (`my-server_*`) or not (`my_server_*`); the hyphen
form is what worked. Once allowed, the orchestrator used the Trello tools directly (9 calls,
including 4 card writes), which is the one mutation path the orchestrator keeps: an external
tracker, not the repository. One card write failed on a 2048-character `desc` limit.

**Where lessons get recorded.** When asked to "save this knowledge to your global memory",
the implementer appended it to the Claude Code global instructions file; the operator pointed
out it was running in OpenCode, and the note was moved to `~/.config/opencode/AGENTS.md`
(now `opencode/AGENTS.md` here). Harness-specific memory locations need to be spelled out in
the worker prompt.

**Token footprint (sum over sessions).**

| agent | sessions | input | output | cache read |
|---|---|---|---|---|
| plan (design) | 1 | 498k | 9k | 4.6M |
| orchestrator | 17 | 416k | 13k | 1.8M |
| implementer | 9 | 287k | 16k | 2.5M |
| explore | 2 | 32k | 2k | 25k |

**Still to discuss.** Subjective quality of the orchestration and whether `reviewer` earns
its place; it was never invoked in these sessions.
