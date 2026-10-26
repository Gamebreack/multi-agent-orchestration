# Glossary

Domain terms only — the vocabulary of the problem, not of the methodology.

A rename edits the existing row. If a term's code pointer no longer resolves, delete the row.

| Term | Meaning | Lives in |
|---|---|---|
| ICM | Interpretable Context Methodology; folder structure as agent orchestration | canonical source linked in `docs/megaplan/megaplan.md` |
| Stage contract | Stage `CONTEXT.md` with Inputs/Process/Outputs | `stages/` (template in `starter/stages/`) |
| Harness | Agent CLI or app being configured (Claude Code, Codex, OpenCode, …) | `docs/harness-comparison.md` |
| Main agent | The agent the user talks to; plans, delegates, reconciles | `core/AGENTS.md` |
| Role | A `mao-<role>` skill: scout, mechanical, implementer, hard-implementer, reviewer, verifier, documenter | `core/skills/` |
| Tier | Intent for a role's model: fast, standard or deep (no model names) | `docs/policies.md` |
| Access level | read-only, read+shell, edit or edit+shell; mapped to native tool limits by mao-setup | `docs/policies.md` |
| Toolkit | This repo's portable deliverable (`core/`) | `README.md` |
| Portability boundary | Nothing personal or harness-specific enters this repo — no MCP endpoints, credentials, model IDs or machine-specific paths | AGENTS.md (hard rules) |
