# Harness capability snapshot (2026-10-26)

What `mao-setup` needs to know about each harness, from official docs as of 2026-10-26.
It is a dated snapshot, not a contract: harnesses change names and paths fast, so
`mao-setup` re-reads the live docs and trusts them over this table. This is the only file in
the repo that may name models or harness-specific paths.

## Table

| Harness | Global instructions | User skills paths | User subagent files | Subagent model choice | Per-subagent tool limits | Model listing | User config | Implication for mao-setup |
|---|---|---|---|---|---|---|---|---|
| Claude Code | `~/.claude/CLAUDE.md` (`@` imports; reads `AGENTS.md` only in projects without `CLAUDE.md`) | `~/.claude/skills` | `~/.claude/agents/*.md` | per-spawn `model` param (aliases haiku/sonnet/opus/inherit) + frontmatter | `tools` / `disallowedTools` | n/a (aliases) | `~/.claude/settings.json` | Write a `CLAUDE.md` stub importing `core/AGENTS.md`; link skills into `~/.claude/skills` too; per-spawn model, so `model: inherit` |
| Codex | `~/.codex/AGENTS.md` | `~/.agents/skills` | `~/.codex/agents/*.toml` (`name`, `description`, `developer_instructions`, `model`, `model_reasoning_effort`) | per-spawn, then `[agents]` defaults, then parent; a custom name overrides built-ins (`default`, `worker`, `explorer`) | sandbox / `skills.config` | none | `~/.codex/config.toml` | Skills only in `~/.agents/skills`; TOML subagents; per-spawn model, so inherit; avoid the built-in names |
| OpenCode | `~/.config/opencode/AGENTS.md` | `~/.config/opencode/skills`, `~/.claude/skills`, `~/.agents/skills` | `~/.config/opencode/agents/*.md` (`mode: subagent`) | per agent; else the primary's model | `permission` | `opencode models` | `opencode.json(c)` | Per-agent model: pick tier models from `opencode models` |
| Cursor | project `AGENTS.md` / `CLAUDE.md`; user rules in Settings UI (no file) | `~/.agents/skills`, `~/.cursor/skills`, `~/.claude/skills`, `~/.codex/skills` | `~/.cursor/agents/*.md` (also reads `~/.claude/agents`, `~/.codex/agents`) | frontmatter `model` (default inherit); parent can name a model at launch | `readonly: true` | `agent models` / `--list-models` | `~/.cursor/cli-config.json` | No global file: tell the user to paste it; inherit plus per-launch model |
| Gemini CLI (replaced by Antigravity CLI for unpaid / Google One users from 2026-06-18) | `~/.gemini/GEMINI.md` (`AGENTS.md` via `context.fileName`) | `~/.gemini/skills`, `~/.agents/skills` | `~/.gemini/agents/*.md` | per agent / `agents.overrides` | `tools` allowlist | none | `~/.gemini/settings.json` | Point `context.fileName` at `AGENTS.md` or link `GEMINI.md`; per-agent model; check which CLI is installed |
| GitHub Copilot (CLI + VS Code) | `~/.copilot/copilot-instructions.md` (`AGENTS.md` repo-level; `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`) | `~/.copilot/skills`, `~/.claude/skills`, `~/.agents/skills` | `~/.copilot/agents/*.agent.md` (VS Code also `~/.claude/agents`) | per-spawn explicit model | `tools` list | `copilot help` | `~/.copilot/settings.json` | Per-spawn model, so inherit; `.agent.md` suffix |
| Devin Desktop/CLI (formerly Windsurf; Cascade legacy) | `~/.config/devin/AGENTS.md` (Cascade: `~/.codeium/windsurf/memories/global_rules.md`) | `~/.config/devin/skills`, `~/.agents/skills` | `~/.config/devin/agents/<name>.md` | per agent (profile); unset falls to server router | `allowed-tools` | `/model` only | `~/.config/devin/config.json` | Per-agent model, chosen by asking the user (no list CLI) |
| Cline | `~/.agents/AGENTS.md` + global rules dirs | `~/.cline/skills` | built-in `spawn_agent` only | inherit (undocumented) | by mode | none | `~/.cline/data/settings/*.json` | No role subagents; link skills into `~/.cline/skills`; tiers collapse |
| Kilo Code | `instructions` key in `~/.config/kilo/kilo.jsonc` | `~/.kilo/skills`, `~/.agents/skills` | `~/.config/kilo/agents/*.md` | per agent, else inherit | `permission` allow/ask/deny | `/models` (TUI) | `kilo.jsonc` | Add `core/AGENTS.md` to `instructions`; per-agent model, else inherit |
| Amp | `~/.config/amp/AGENTS.md` | `~/.agents/skills` (+ others) | plugins only | inherit only (mode low..ultra) | global only | none | `~/.config/amp/settings.json` | No role subagents; tiers collapse |
| Factory Droid | `AGENTS.md` under `~/.factory/` | `~/.factory/skills`, `~/.agents/skills` | `~/.factory/droids/*.md` | per droid, or per-spawn `complexity` light/medium/heavy mapped by `subagentModelSettings` | `tools` array / category | none | `~/.factory/settings.json` | Map tiers to light/medium/heavy or per-droid model |
| Goose | `AGENTS.md` / `.goosehints` in `~/.config/goose/` | `~/.agents/skills` | `~/.agents/agents/*.md` | per agent | none | none | `~/.config/goose/config.yaml` | Per-agent model by asking the user; no tool limits, so access levels are prompt-only |
| Kiro | `~/.kiro/steering/AGENTS.md` | `~/.kiro/skills` | `~/.kiro/agents/` (json/md) | per agent | tools + permissions | `kiro-cli chat --list-models --format json` | `~/.kiro/settings/cli.json` | Link skills into `~/.kiro/skills`; tier models from the listing |
| Junie | `~/.junie/AGENTS.md` | `~/.junie/skills`, `~/.agents/skills` | `~/.junie/agents/*.md` | per agent, else `SameModelOnly` / `Auto` | `tools` / `disallowedTools` | none | `~/.junie/config.json` | Per-agent model by asking, or leave on Auto |
| Roo Code | shut down 2026-05-15 (secondary source) | | | | | | | Not supported |

Reading the last column: **per-spawn** model choice means the subagent file says `inherit`
and the main agent names the tier's model at spawn time; **per-agent** means `mao-setup`
writes a concrete model per tier; **inherit-only** means the tiers collapse to one model and
the plan must say so.

## Sources

- Claude Code: code.claude.com/docs/en/{memory,sub-agents}
- Codex: learn.chatgpt.com/docs/{build-skills,agent-configuration/subagents}
- OpenCode: opencode.ai/docs/{skills,agents}
- Cursor: cursor.com/docs/context/{subagents,skills,rules}, cursor.com/docs/cli/reference/{parameters,configuration}
- Gemini CLI: geminicli.com/docs/{core/subagents,cli/skills,cli/gemini-md,reference/configuration}
- GitHub Copilot: docs.github.com/en/copilot/reference/custom-agents-configuration, docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/{add-custom-instructions,create-skills}, code.visualstudio.com/docs/copilot/agents/subagents
- Devin: docs.devin.ai/{desktop/devin-local,cli/subagents,cli/models}
- Cline: docs.cline.bot/features/{skills,subagents}
- Kilo Code: kilo.ai/docs/customize/{custom-subagents,skills}
- Amp: ampcode.com/docs/{customize/agents-md,customize/skills,models-and-subagents}
- Factory Droid: docs.factory.com/cli/configuration/{custom-droids,settings,skills}
- Goose: goose-docs.ai/docs/guides/context-engineering/{custom-agents,using-skills}
- Kiro: kiro.dev/docs/{custom-agents/subagents,steering}
- Junie: junie.jetbrains.com/docs/{junie-cli-subagents,agent-skills,junie-cli-configuration}.html

## Observed on Claude Code 2.1.263 (September 2026)

Behaviors from earlier validation that affect setup:

- **User-scope agents appear in every session's agent list.** A role description that says
  when to use it keeps ordinary sessions from routing to it by accident.
- **`LSP` is stripped from background subagents**, so read-only roles effectively have
  read/search only.
- **Hooks run inside subagents too.** A user-scope Stop or PreToolUse hook that assumes it
  runs in the main session can block every subagent (one such hook blocked 31 transcripts in
  a day). Test existing hooks against a subagent transcript before installing agents.
- **A syntax error in a `matcher: "*"` hook blocks every tool call in every session**, and
  only the user can undo it. Run `bash -n` on any hook script before installing it.
- **Auto mode pauses after 3 consecutive classifier blocks.** A subagent's frontmatter
  `permissionMode` is ignored there; `permissions.allow` rules resolve before the
  classifier, and the classifier blocks the agent from editing them itself, so the user must
  apply that change.
