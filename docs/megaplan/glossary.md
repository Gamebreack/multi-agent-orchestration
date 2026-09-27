# Glossary

Domain terms only — the vocabulary of the problem, not of the methodology.

A rename edits the existing row. If a term's code pointer no longer resolves, delete the row.

| Term | Meaning | Lives in |
|---|---|---|
| ICM | Interpretable Context Methodology; folder structure as agent orchestration | canonical source linked in `docs/megaplan/megaplan.md` |
| Stage contract | Stage `CONTEXT.md` with Inputs/Process/Outputs | `stages/` (template in `starter/stages/`) |
| Harness | Agent CLI being configured (OpenCode, Claude Code, Antigravity) | `docs/harness-comparison.md` |
| Preset | Named model/variant set for all agents | `opencode/presets/*.tsv` |
| oc-preset | Script switching agents between presets | `opencode/oc-preset` |
| Orchestrator | Read-only primary agent | `opencode/agents/orchestrator.md` |
| Manager | Claude Code equivalent of orchestrator | `agents/manager.md` |
| Toolkit | This repo's portable deliverable | `README.md` |
| Portability boundary | Nothing personal enters this repo — no MCP endpoints, credentials, or machine-specific paths; templates carry only commented placeholders | AGENTS.md (hard rules) |
