# Claude Code: what we observed while making the manager read-only

Companion to the [README](../README.md), which documents the setup itself. Everything below
was observed on Claude Code **2.1.263** in September 2026 while installing and validating
the manager + 6 roles layout.

## Things that had to be true for the design to work (verified)

1. **The main session reports `agent_type` to hooks.** When launched with
   `claude --agent manager`, `PreToolUse` hook input carries `agent_type: "manager"`, so a
   user-scope hook with matcher `*` can single out the orchestrator and stay a no-op for every
   other session. This is what makes a *global* hook safe to install.
2. **Subagent tool lists are independent of the parent's.** A manager with no
   Edit/Write/Bash can still spawn a `worker` whose frontmatter grants them. Validated
   end-to-end: manager denied, worker edits applied.
3. **`Agent(<role>, …)` in frontmatter restricts spawnable types**, and the hook double-checks
   with an exact match on `subagent_type`, so `general-purpose`, `fork` and untyped calls are
   denied.
4. **Model aliases resolve as documented.** `fable`, `opus`, `sonnet`, `haiku` mapped to
   `claude-fable-5-1`, `claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5-20251001`
   (seen in `modelUsage`).
5. **Haiku was reliable for mechanical edits** and verified itself with `git diff`; the
   `maxTurns` caps on the two haiku roles are there so a looping cheap agent returns a partial
   report instead of burning the usage window.

## Things that broke, and the fix

### Auto mode paused because of the workers (2026-09-07)
Parallel workers running routine commands (a browser automation tool, `git add`/`commit`,
`node`, `npx`) tripped the auto-mode classifier. After **3 consecutive blocks auto mode
pauses and prompts for everything**, which defeats delegation. Findings:

* A subagent's frontmatter `permissionMode` is **ignored** in auto mode.
* `permissions.allow` rules resolve **before** the classifier, so they are the fix.
* The rules must live at **user scope** (`~/.claude/settings.json`) if you switch projects
  often; project-scope would need redoing per repo.
* Claude cannot edit `permissions.allow` itself (the classifier blocks that write). The
  workaround is to prepare the script and have the operator run it with the `!` prefix.
* Do not add broad wildcards such as `Bash(make:*)` or `Bash(git push:*)`; production
  targets rely on the classifier's soft deny.

### A global Stop hook blocked every subagent (2026-09-08)
A pre-existing user-scope `Stop` hook required a `SendMessage` reply whenever the transcript
contained an inbound cross-session message. In team mode every subagent receives its task as
`<teammate-message teammate_id="team-lead">` and has **no SendMessage tool**
("SendMessage is disabled for this session, in subagents as well as here"), so it could never
satisfy the hook: 31 blocked transcripts in one day. Fix: the hook exits 0 when the
transcript's first line is an `agent-setting` record (a subagent), and ignores inbound lines
whose `teammate_id` is `team-lead` or `system`, plus `teammate_terminated` /
`shutdown_approved` notices. Lesson: any Stop/PreToolUse hook you already have runs inside
your subagents too; test it against a subagent transcript before installing agents.

### A syntax error in a `matcher: "*"` hook blocks every tool call everywhere
During a verify pass a broken `manager-boundary.sh` exited 2 for all tools in all sessions,
and only the operator could undo it (`! mv` the file away). Now: `bash -n` and the synthetic
decision suite run **before** `install.sh`.

### After the fixes (2026-09-08, two projects)
Two manager sessions later the same day spawned 10 subagents between them (explorer ×3,
worker ×5, mechanical-worker, reviewer), used the Asana MCP tools from the manager, and show
**no** hook denials, no auto-mode pause and no Stop-hook block in their transcripts.

## Platform behaviours worth knowing

* **`LSP` is stripped from background subagents** (the default), so `explorer` and
  `reviewer` effectively have Read/Grep/Glob.
* **`Monitor` is a shell tool** (its `command` parameter is a shell); it must be denied for the
  manager together with Bash.
* **User-scope agents appear in every session's Agent list.** The implementation roles carry a
  "For use by the manager orchestrator" description prefix so ordinary sessions do not route
  to them.
* **Do not set `"agent": "manager"` globally**; every ordinary session would lose editing.
  Set it per project in `.claude/settings.json` if wanted.
* The `manager` identification is an exact match on `agent_type == "manager"`; renaming the
  agent or packaging it as a plugin (`plugin:manager`) fails open unless the hook is updated.
