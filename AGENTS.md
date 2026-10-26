# multi-agent-orchestration — repo conventions

Layer 0 of this repo's ICM structure; read CONTEXT.md next for routing. core/ is
the toolkit this repo ships (global instructions, role skills, setup procedure)
— it is not instructions for working on this repo.

## How work happens here

- **Hybrid ICM** (locked 2026-09-25): numbered stages under stages/ organize
  each work item; role agents (mao-*) execute the stage work. docs/megaplan/
  decides WHAT work exists; stages/ decide HOW an item flows. One home per
  fact — never duplicate a rule into a second file.
- **megaplan** owns the backlog: docs/megaplan/backlog.md is the only live
  work index; an item file under docs/megaplan/backlog-items/ holds the
  detail. The done ledger (docs/megaplan/done.md) is written by the
  operator only.
- Role discipline: read-only roles inspect, mechanical/implementer roles
  edit, fresh verifier/reviewer roles check. The main agent plans and
  delegates; it may make a truly trivial edit itself.

## Hard rules

- No commits, pushes, or remote changes without explicit operator
  authorization. Workers never commit or push. Before committing, run the
  repo's pre-commit hooks; never use --no-verify.
- Keep every CONTEXT.md under 80 lines; reference docs under 200.
- Secrets, personal MCP endpoints, credentials, model IDs, harness-specific
  config and machine-specific paths never enter this repo (portability
  boundary; see docs/policies.md). Model names never appear.
