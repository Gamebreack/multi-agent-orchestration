# MAO — multi-agent orchestration for coding agents

[![Latest release](https://img.shields.io/github/v/release/Gamebreack/multi-agent-orchestration)](https://github.com/Gamebreack/multi-agent-orchestration/releases)
[![License: MIT](https://img.shields.io/github/license/Gamebreack/multi-agent-orchestration)](LICENSE)

MAO is a portable, harness-agnostic agent setup for coding agents. It is one set of
instructions and role skills that your agent installs into whatever harness it runs in.

## What you get

- **Global instructions** in [`core/AGENTS.md`](core/AGENTS.md): communication, roles and tiers, delegation rules, committing.
- **Seven role agents**: scout, mechanical, implementer, hard-implementer, reviewer, verifier and documenter. Each has a tier (fast, standard or deep, which state intent, not models) and an access level (read-only, read+shell, edit or edit+shell).
- **An agent-run setup** (`mao-setup`) that shows a full plan and changes nothing until you approve. It backs up every file it replaces, records every action, supports a dry run, and can uninstall.
- **A copyable ICM starter workspace** in [`starter/`](starter/) for other projects.

## How it works

The main agent plans the task, reads the relevant code, and delegates each piece to the
cheapest role that can do it reliably. Role agents do the work and run their own checks.
Review and verification run in a fresh context, never by the author, and never edit.
Workers never commit or push. The main agent commits only when you ask, after running the
repo's pre-commit hooks, which it never bypasses. Pushing is yours.

> See the [flow map](flow-map.md): what happens from install to a verified commit, who talks
> to whom, and the life of one task.

```
                      MAIN AGENT: plan, delegate, reconcile
                                     |
     +------------+------------+-----+------+-------------+-------------+
     |            |            |            |             |             |
  scout       mechanical   implementer   hard-impl.    reviewer      verifier
  fast        fast         standard      deep          deep          standard
  read-only   edit+shell   edit+shell    edit+shell    read-only     read+shell
                                                                   (+ documenter: fast, docs only)
```

## Quick start

**Prerequisites**

- An agent harness that can read files and run shell commands.
- Git, to clone this repo.
- Subagent support is optional. Without it, the main agent follows each role's charter
  itself, at that role's rigor, and does not treat its own work as independently verified.

**Install.** Clone this repo, then tell your agent:

> Read `<repo>/core/skills/mao-setup/SKILL.md` and follow it.

The agent detects its harness, reads the harness's current docs, and shows a full plan.
Nothing is written, no directories are created and no installers run until you approve.
Every replaced file is backed up to `~/.config/mao/backups/`, and every action is recorded in
`~/.config/mao/installed.json`.

**Dry run.** Add `dry-run` to the same prompt. The agent shows the plan and stops there.

**Uninstall.** Give the same prompt with `uninstall`. The agent shows the reverse plan first,
then reverses the recorded actions after you approve. It leaves alone anything it can no
longer match to what it recorded, and it does not restore retired items unless you opt in.

## Optional dependencies

Each is asked separately (y/N) during install.

| Name | What it adds | Source |
|---|---|---|
| OpenSpec CLI (`npm i -g @fission-ai/openspec`) | Spec-driven change proposals | [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) |
| `verify` | An independent verification panel of fresh-context reviewers, for pre-release checks | [Gamebreack/agent-verification](https://github.com/Gamebreack/agent-verification) |
| `megaplan` | A plan-tracking backlog for a project | [Gamebreack/megaplan](https://github.com/Gamebreack/megaplan) |
| `flow-map` | Mermaid flow maps of a repo | [Gamebreack/flow-map](https://github.com/Gamebreack/flow-map) |
| `grilling` and `grill-me` | Stress-test a plan by being questioned | [mattpocock/skills](https://github.com/mattpocock/skills) |

`second-brain-interface` is an opt-in template. It needs a Second Brain MCP server that you
already run. MAO ships none.

## Repository layout

| Path | What |
|---|---|
| `core/AGENTS.md` | Global instructions: communication, roles by tier, delegation rules |
| `core/skills/mao-<role>/` | Seven role charters (scout, mechanical, implementer, hard-implementer, reviewer, verifier, documenter) |
| `core/skills/mao-setup/` | The install/uninstall procedure your agent runs |
| `core/skills/second-brain-interface/` | Optional template for a Second Brain MCP server |
| `docs/policies.md` | Roles, tiers, access levels, permission philosophy |
| `flow-map.md` | End-to-end flow map (install, task lifecycle, uninstall) as Mermaid diagrams |
| `starter/` | Copyable ICM workspace template for other projects |
| `AGENTS.md`, `CONTEXT.md`, `stages/`, `docs/megaplan/` | How work on this repo itself is run |

## Limits

MAO is instructions, not code: your agent carries out each step.

- Where a harness cannot set a model per subagent, the tiers collapse to one model.
- Where a harness has no global instructions file, setup tells you what to paste.
- Access limits are hard only where the harness can enforce them. Elsewhere they are
  prompt-only, and the setup plan says which.
- Harness docs change fast, so `mao-setup` re-reads the harness's live docs on every run.

## Principles

- **Deny by default.** Each role gets only the access its charter needs.
- **Workers never commit or push.** Commits and pushes happen only when you ask.
- **Verification never edits.** A fix goes back through a delegated implementer.
- **Review runs in a fresh context,** never by the author of the change.
- **Portability boundary.** No model IDs, credentials, MCP endpoints, hostnames or machine
  paths are committed.

See [docs/policies.md](docs/policies.md) for the rationale.

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Credits

- ICM (Interpretable Context Methodology) by Jake Van Clief: https://github.com/RinDig/Interpretable-Context-Methodology
- `grilling` and `grill-me` from https://github.com/mattpocock/skills

## License

[MIT](LICENSE)
