# MAO: how I work with coding agents

A portable, harness-agnostic agent setup. One set of instructions and role skills; your agent
translates them into whatever harness it runs in (any agent harness). Nothing here is tied to a vendor, a model ID, or a person.

The main agent plans, delegates and reconciles. Role agents do the work, each on the
cheapest tier that can do it reliably. Tiers state intent (fast, standard, deep), not models.

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

Workers never commit or push. Review and verification run in a fresh context and never edit.
Before any commit, the repo's pre-commit hooks run; they are never bypassed.

## What is in the repo

| Path | What |
|---|---|
| `core/AGENTS.md` | Global instructions: communication, roles by tier, delegation rules |
| `core/skills/mao-<role>/` | Seven role charters (scout, mechanical, implementer, hard-implementer, reviewer, verifier, documenter) |
| `core/skills/mao-setup/` | The install/uninstall procedure your agent runs |
| `core/skills/second-brain-interface/` | Optional template for a Second Brain MCP server |
| `docs/policies.md` | Roles, tiers, access levels, permission philosophy |
| `starter/` | Copyable ICM workspace template for other projects |
| `AGENTS.md`, `CONTEXT.md`, `stages/`, `docs/megaplan/` | How work on this repo itself is run |

## Install

Clone this repo, then tell your agent:

> Read `<repo>/core/skills/mao-setup/SKILL.md` and follow it.

The agent detects its harness, reads the harness's current docs, shows a full plan, and
changes nothing until you approve. Every replaced file is backed up to
`~/.config/mao/backups/` and every action is recorded in `~/.config/mao/installed.json`.

Uninstall: same prompt with `uninstall`. It reverses the manifest, after showing you the plan.

## Optional dependencies

Each is asked separately (y/N) during install.

- [OpenSpec CLI](https://github.com/Fission-AI/OpenSpec): `npm i -g @fission-ai/openspec`
- [`verify` skill](https://github.com/Gamebreack/agent-verification)
- [`megaplan` skill](https://github.com/Gamebreack/megaplan)
- [`grilling` and `grill-me` skills](https://github.com/mattpocock/skills)

## Flagged

- `second-brain-interface` needs a Second Brain MCP server you already run; MAO ships none.
- Where a harness cannot set a model per subagent, the tiers collapse to one model.
- Where a harness has no global instructions file, setup tells you what to paste.
- Read-only limits are hard only where the harness can enforce them; otherwise they are instructions.
- Harness docs change fast; `mao-setup` re-reads the harness's live docs every run.

See [docs/policies.md](docs/policies.md).

## License

[MIT](LICENSE)
