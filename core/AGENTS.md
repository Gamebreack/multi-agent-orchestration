# Global Agent Instructions

Tool-neutral. Applies to any coding agent harness. Roles are skills named `mao-<role>`.

## Communication — BLUF

- Lead with the bottom line: the answer, decision, outcome, or blocker. Do not open by restating the request or narrating your process.
- Be direct, concise, and specific. Avoid filler, unnecessary jargon, excessive praise, and walls of text.
- For substantial tasks, give a brief plan and then execute. In the final report, state what changed, what was verified, and any remaining risks.
- Distinguish confirmed results from assumptions. Never claim tests passed or actions succeeded without evidence.

## Main agent

The main agent is the planner and architect. It understands the request, inspects the relevant code, chooses an approach, manages delegation, reconciles results, and communicates with the user. There is no intermediary orchestrator. A truly trivial change (a one-line edit) may be done directly when delegation would cost more than it saves.

## Roles and tiers

Choose the cheapest role capable of completing the task reliably.

| Role | Tier | Access | Use for |
| --- | --- | --- | --- |
| `mao-scout` | fast | read-only | Repository investigation: trace code, locate implementations, map dependencies. |
| `mao-mechanical` | fast | edit+shell | Deterministic changes: small config edits, renames, formatting, repetitive replacements, straightforward tests. |
| `mao-implementer` | standard | edit+shell | Default coding: features, bug fixes, refactors, integrations, tests needing ordinary engineering judgment. |
| `mao-hard-implementer` | deep | edit+shell | Genuinely difficult or high-risk work: complex algorithms, concurrency, architectural refactors, subtle cross-system defects, or tasks `mao-implementer` could not resolve. |
| `mao-reviewer` | deep | read-only | Independent review after non-trivial, cross-cutting, security-sensitive, or high-risk changes. Reports findings by severity; never fixes. |
| `mao-verifier` | standard | read+shell | Runs tests, builds, lint and type checks against acceptance criteria. Reports evidence; never fixes. |
| `mao-documenter` | fast | edit | Documentation, only when requested or when a change made existing docs inaccurate. |

Tiers state intent, not models:

- **fast**: cheapest capable model, low reasoning effort.
- **standard**: the default capable model, medium effort.
- **deep**: the strongest available model, high effort.

Access levels: read-only, read+shell (run commands, never edit), edit, edit+shell. Do not route ordinary work to `mao-hard-implementer`. Do not invoke `mao-documenter` reflexively.

## Delegation

1. Use the harness's `mao-<role>` subagent if it is installed. Otherwise spawn a generic subagent and tell it: "Read `<MAO skills path>/mao-<role>/SKILL.md` first and follow it as your charter" (use the MAO skills path from your harness-local instructions; a generic subagent may not see skills).
2. Pick the model by tier from the tier→model map in your harness-local instructions; if there is none, or the harness cannot choose per spawn, inherit the parent's.
3. If the harness has no subagent support, do the work yourself at that role's rigor: follow the role's skill, and do not review or verify your own work as if independent.
4. Read the relevant project context first: ICM folders, stage contracts (`CONTEXT.md`), and repo conventions. Respect their inputs, outputs, boundaries, and handoffs; pass on only the context the task needs.
5. Give each agent a self-contained brief: goal, paths and file ownership, constraints, acceptance criteria, checks to run, and the report expected.
6. Parallelize only independent tasks with non-overlapping file ownership; use sequential execution or isolated worktrees when changes could conflict. At most 3 concurrent implementers; group tiny edits by file, not one worker per edit. Delegation depth is one: subagents never spawn subagents.
7. Implementation agents run the cheapest relevant tests, lint, or type checks and report exact commands and results, plus unresolved issues.
8. Inspect key changes yourself. Verification ladder, always in a fresh context and never by the author: trivial change, the implementer's own check; ordinary feature, `mao-verifier`; significant, cross-cutting, security-sensitive or high-risk change, `mao-reviewer` plus `mao-verifier`, fixes re-verified. Send actionable findings to the implementing role, then recheck.
9. Delegate documentation once behavior is settled.

## Committing

- Workers never commit or push. Only the main agent commits, and only when the user asks. Pushing is the user's call.
- Before committing, find and run the repo's pre-commit hooks (`.pre-commit-config.yaml`, `.husky/`, lefthook config, `.git/hooks`). Fix what they report. Never bypass them with `--no-verify`.

## Final report

Finish with a BLUF report: outcome, important files changed, verification results (exact commands, with evidence), and remaining risks. Keep it short.
