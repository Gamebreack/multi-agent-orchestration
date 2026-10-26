# Shared policies — rationale

One home per fact: this file states every policy that applies across harnesses. The runtime
source that agents read is `core/AGENTS.md` plus the role skills under `core/skills/`; this
file is the rationale for them. Harness facts live in
[harness-comparison.md](harness-comparison.md).

| Layer | Home |
|---|---|
| Policy rationale (this file) | docs/policies.md |
| Runtime instructions | core/AGENTS.md |
| Role charters | core/skills/mao-<role>/SKILL.md |
| Install procedure | core/skills/mao-setup/SKILL.md |
| Harness capabilities (dated snapshot) | docs/harness-comparison.md |
| Repo workflow | CONTEXT.md + stages/ |
| Work backlog | docs/megaplan/ |

## Roles

Every role is a skill named `mao-<role>`. The main agent plans, delegates and reconciles; it
may make a truly trivial edit itself.

| Role | Tier | Access | Charter (one line) |
|---|---|---|---|
| mao-scout | fast | read-only | Repository investigation; findings with file:line |
| mao-mechanical | fast | edit+shell | Deterministic, well-specified edits only |
| mao-implementer | standard | edit+shell | Default implementation and repair |
| mao-hard-implementer | deep | edit+shell | Genuinely difficult or high-risk work only |
| mao-reviewer | deep | read-only | Independent adversarial review; never fixes |
| mao-verifier | standard | read+shell | Runs tests/builds/lint; reports, never fixes |
| mao-documenter | fast | edit (docs only) | Brings docs in line with implemented code |

## Tiers

Tiers state intent; no model names are committed.

- **fast**: cheapest capable model, low reasoning effort.
- **standard**: the default capable model, medium effort.
- **deep**: the strongest model, high effort.

A harness that chooses the model per spawn gets the tier's model from the main agent at
spawn time; one that fixes it per subagent file gets one chosen by `mao-setup`; one that only
inherits collapses the tiers to a single model. See harness-comparison.md.

## Access levels

| Level | Meaning |
|---|---|
| read-only | Read and search; no edit, no shell |
| read+shell | Read, search and run commands; no edit |
| edit | Read, search and edit; no shell |
| edit+shell | Read, search, edit and run commands |

`mao-setup` maps each level to the harness's native tool limits, using the closest limit that
still lets the role work where the harness is coarser, plus a prompt-level note for the remainder. Where a harness has no limits, the level is prompt-only.

## Permission philosophy

- **Deny by default**, fail closed: grant each role only the access its charter needs.
- Workers never commit or push. Commits and pushes happen only when the user asks, and the
  main agent runs the repo's pre-commit hooks first and never bypasses them.
- Verification never edits; a fix always goes back through a delegated implementer, never a
  "quick fix" by the verifier.
- Review and verification run in a fresh context, never by the author.
- No command is classified as "safe": roles that must not change files get no edit tools,
  not a promise.
- Enforcement is either HARD (native tool limits) or PROMPT (charter text). Which one applies
  depends on the harness; `mao-setup` states it in its plan.

## Verification ladder

| Change | Verification |
|---|---|
| Trivial, low-risk | implementer's own check |
| Ordinary feature | fresh verifier |
| Significant / cross-cutting / risky | reviewer + verifier, fixes re-verified |
| Pre-release | independent panel (for example the verify skill) |

## Burst policy

At most 3 concurrent implementers; group tiny edits by file ownership, not one worker per
edit. Delegation depth is one: a worker never spawns workers.

## Portability boundary

Nothing personal or harness-specific is committed: no model IDs, no harness config files, no
MCP endpoints, credentials, hostnames or machine paths. `mao-setup` translates the
tool-neutral content into each harness's native local config on the user's machine, records
what it did in a manifest, and can reverse it. Model names may appear only in
harness-comparison.md, as harness facts.
