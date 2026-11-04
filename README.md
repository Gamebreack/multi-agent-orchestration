# MAO — multi-agent orchestration for coding agents

[![Latest release](https://img.shields.io/github/v/release/Gamebreack/multi-agent-orchestration)](https://github.com/Gamebreack/multi-agent-orchestration/releases)
[![License: MIT](https://img.shields.io/github/license/Gamebreack/multi-agent-orchestration)](LICENSE)

MAO turns the coding agent you already use into a planner. It splits each task, hands the pieces to helper agents (*roles*) on cheaper or stronger models, has a fresh agent check the result, and commits only when you ask. MAO is plain Markdown, not code: your agent installs it into the tool it runs in (its *harness*, a coding-agent CLI or app).

## What you get

- **Global instructions** in [`core/AGENTS.md`](core/AGENTS.md): communication, roles and tiers, delegation rules, committing.
- **Seven role agents** (diagram below), each with a tier (fast, standard or deep: from cheapest to strongest model; setup maps each tier to your harness's models) and an access level (read-only, read+shell, edit or edit+shell).
- **An agent-run setup** (`mao-setup`) that shows a full plan and changes nothing until you approve. It backs up every file it replaces, records every action, supports a dry run, and can uninstall.
- **Optional: a starter workspace** in [`starter/`](starter/) to copy into other projects. It organizes work in numbered stages (ICM, Interpretable Context Methodology).

## How it works

The main agent (the one you talk to) plans the task, reads the relevant code, and delegates each piece to the
cheapest role that can do it reliably. Role agents do the work and run their own checks.
Beyond trivial changes, review and verification run in a fresh context, never by the author, and never edit.
Workers never commit or push. The main agent commits only when you ask, after running the
repo's pre-commit hooks, which it never bypasses. Pushing is yours. Each role gets only the access it needs; policies and their rationale are in [docs/policies.md](docs/policies.md).

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
- Node.js with npm, only for the OpenSpec and grilling optional dependencies.
- Subagent support is optional. Without it, the main agent follows each role's charter
  itself, at that role's rigor, and does not treat its own work as independently verified.

**Install.** Clone the repo (`git clone https://github.com/Gamebreack/multi-agent-orchestration`), then tell your agent, using your clone's full path:

> `Read /path/to/multi-agent-orchestration/core/skills/mao-setup/SKILL.md and follow it.`

The agent detects its harness, reads the harness's current docs, and shows a full plan.
Nothing is written, no directories are created and no installers run until you approve.
Every replaced file is backed up to `~/.config/mao/backups/`, and every action is recorded in
`~/.config/mao/installed.json`.

Install is user-wide, not per project. It writes your harness's global instructions file (backing up any existing one), links MAO's skills into `~/.agents/skills/`, adds `mao-*` subagents where the harness supports them, and may offer to retire an earlier agent setup it replaces.

**Update.** Keep the clone where it is; the install links to it. To update, `git pull` and give the same prompt again.

**Dry run.** Same prompt, ending "…and follow it in dry-run mode." The agent shows the plan and stops.

**Uninstall.** Same prompt, ending "…and uninstall MAO." Run it inside each harness you installed into. The agent shows the reverse plan, then undoes that harness's recorded actions after you approve. It keeps anything another harness still depends on, leaves alone anything changed since install, and does not restore retired items unless you opt in.

## Optional dependencies

Each is asked separately (y/N) during install.

| Name | What it adds | Source |
|---|---|---|
| OpenSpec CLI | Spec-driven change proposals | [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) |
| `verify` | An independent verification panel for pre-release checks | [Gamebreack/agent-verification](https://github.com/Gamebreack/agent-verification) |
| `megaplan` | A plan-tracking backlog for a project | [Gamebreack/megaplan](https://github.com/Gamebreack/megaplan) |
| `flow-map` | Mermaid flow maps of a repo | [Gamebreack/flow-map](https://github.com/Gamebreack/flow-map) |
| `grilling` and `grill-me` | Stress-test a plan by being questioned | [mattpocock/skills](https://github.com/mattpocock/skills) |

Install commands and exact sources: `core/skills/mao-setup/SKILL.md`, step 3.

`second-brain-interface` is an opt-in template: setup links it only if you ask for it. It needs a Second Brain MCP server that you already run. MAO ships none.

## Repository layout

| Path | What |
|---|---|
| `core/AGENTS.md` | Global instructions: communication, roles by tier, delegation rules |
| `core/skills/mao-<role>/` | Seven role charters |
| `core/skills/mao-setup/` | The install/uninstall procedure your agent runs |
| `core/skills/second-brain-interface/` | Optional template for a Second Brain MCP server |
| `docs/policies.md` | Roles, tiers, access levels, permission philosophy |
| `flow-map.md` | End-to-end flow map (install, task lifecycle, uninstall) as Mermaid diagrams |
| `starter/` | Copyable ICM workspace template for other projects |
| `AGENTS.md`, `CONTEXT.md`, `stages/`, `docs/megaplan/` | How work on this repo itself is run |

## Limits

MAO is instructions, not code: your agent carries out each step.

- Where a harness can only inherit the main agent's model, every role uses that model.
- Where a harness has no global instructions file, setup tells you what to paste.
- Access limits are hard only where the harness can enforce them. Elsewhere they are
  prompt-only, and the setup plan says which.

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Credits

- ICM (Interpretable Context Methodology) by Jake Van Clief: https://github.com/RinDig/Interpretable-Context-Methodology
- `grilling` and `grill-me` from https://github.com/mattpocock/skills

## License

[MIT](LICENSE)
