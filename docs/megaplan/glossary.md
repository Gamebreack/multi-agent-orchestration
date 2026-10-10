# Glossary

Domain terms only — the vocabulary of the problem, not of the methodology.

A rename edits the existing row. If a term's code pointer no longer resolves, delete the row.

| Term | Meaning | Lives in |
|---|---|---|
| ICM | Interpretable Context Methodology; folder structure as agent orchestration | canonical source linked in `docs/megaplan/megaplan.md` |
| Stage contract | Stage `CONTEXT.md` with Inputs/Process/Outputs | `stages/` (template in `starter/stages/`) |
| Orchestrator | Primary agent: plans, delegates and reconciles; never writes files (also called manager) | `stages/` (named in stage contracts) |
| Explore | Read-only tier that maps code and docs with file:line evidence | `stages/02-design/` |
| Scout | Read-only tier for external research (web docs) | `stages/02-design/` |
| Worker | Any editing tier the orchestrator delegates to (mechanical, implementer, hard-implementer) | `stages/` |
| Mechanical worker | Editing tier for deterministic, well-specified edits only | `stages/` |
| Implementer | Default editing tier for ordinary implementation and repair | `stages/03-implement/` |
| Hard-implementer | Editing tier reserved for genuinely difficult work | `stages/03-implement/` |
| Verifier | Fresh-context tier that runs checks and reports PASS/FAIL; never edits | `stages/04-verify/` |
| Reviewer | Fresh-context, read-only adversarial review tier | `stages/04-verify/` |
| Verify-skill panel | Several fresh reviewers run together before a release | `stages/04-verify/` |
| Portability boundary | Nothing personal enters this repo — no MCP endpoints, credentials, or machine-specific paths; templates carry only commented placeholders | AGENTS.md (hard rules) |
