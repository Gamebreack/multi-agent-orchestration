# multi-agent-orchestration — repo conventions

Layer 0 of this repo's ICM structure; read CONTEXT.md next for routing. The
repo holds two things: the hybrid ICM workflow (run live here, and shipped
as the reusable starter in starter/) and agent-core, an agent factory being
specified under openspec/.

## How work happens here

- **Hybrid ICM** (locked 2026-09-25): numbered stages under stages/ organize
  each work item; specialist agents execute the stage work. docs/megaplan/
  decides WHAT work exists; stages/ decide HOW an item flows. One home per
  fact — never duplicate a rule into a second file.
- **megaplan** owns the backlog: docs/megaplan/backlog.md is the only live
  work index; an item file under docs/megaplan/backlog-items/ holds the
  detail. The done ledger (docs/megaplan/done.md) is written by the
  operator only.
- Tier discipline: read-only tiers inspect, mechanical/implementer tiers
  edit, fresh verifier/reviewer tiers check. The primary orchestrator never
  writes files.

## Hard rules

- No commits, pushes, or remote changes without explicit operator
  authorization. Workers never push (permission-denied by design).
- Keep every CONTEXT.md under 80 lines; reference docs under 200.
- Secrets, personal MCP endpoints, credentials and machine-specific paths
  never enter this repo (portability boundary; see docs/megaplan/glossary.md).
