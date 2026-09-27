# Shared policies — the canonical home

One home per fact: this file states every policy that applies across all
three harnesses. Harness docs hold the adapters (how each harness expresses
these policies); agent files carry the runtime copies they must be
self-contained with, and defer to this file as canonical.

| Layer | Home |
|---|---|
| Shared policy (this file) | docs/policies.md |
| Harness adapters | docs/opencode.md, docs/antigravity.md, docs/claude-code-observations.md, docs/harness-comparison.md |
| Optional presets (models) | opencode/presets/*.tsv + opencode/oc-preset |
| Repo workflow | CONTEXT.md + stages/ |
| Work backlog | docs/megaplan/ |

## Roles

| Family | Charter (one line) | Claude Code | OpenCode | Antigravity |
|---|---|---|---|---|
| Primary | Plans, delegates, reconciles; never edits, no shell | agents/manager.md | opencode/agents/orchestrator.md | multitask-team/agents/orchestrator-agent/ |
| Discovery | Read-only codebase and external research | agents/explorer.md | opencode/agents/explore.md + scout.md | researcher-agent/, planner-agent/ |
| Mechanical | Deterministic, well-specified edits only | agents/mechanical-worker.md | opencode/agents/mechanical.md | — |
| Implementation | Default implementation and repair | agents/worker.md | opencode/agents/implementer.md | writer-agent/ (no shell), documenter-agent/ |
| Hard implementation | Genuinely difficult work only | agents/hard-worker.md | opencode/agents/hard-implementer.md | — |
| Review | Independent adversarial read-only review | agents/reviewer.md | opencode/agents/reviewer.md | reviewer-agent/ |
| Verification | Runs tests/builds/lint; reports, never fixes | agents/verifier.md | opencode/agents/verifier.md | merged into reviewer-agent/ |

Antigravity collapses the tiers (one writer with no shell, one reviewer
that also runs tests): a harness limit, not a policy divergence.

## Permission philosophy

- The primary agent is read-only with **no shell at all**; commands are
  never classified as safe — deny wholesale instead.
- **Deny by default**, fail closed, on every harness.
- Edits happen only through delegated workers; verification never edits.
- Workers never commit or push. Commits and pushes are operator-authorized
  (OpenCode also hard-denies `git push*` in the worker shell rules).
- Enforcement is either HARD (checked by hook or permissions array) or
  PROMPT (charter text) — which is which, per harness, see the harness docs.

Mechanism per harness (adapter layer): Claude Code = frontmatter `tools:`
plus the PreToolUse hook (hooks/manager-boundary.sh); OpenCode = ordered
permissions arrays, `"*": deny` first; Antigravity = `tools:` whitelist.

## Verification ladder

| Change | Verification |
|---|---|
| Trivial, low-risk | worker's own check |
| Ordinary feature | fresh verifier |
| Significant / cross-cutting / risky | reviewer + verifier, fixes re-verified |
| Pre-release | verify-skill panel |

Always in a fresh context; the author never verifies their own work.

## Burst policy

At most 3 concurrent implementers; group tiny edits by file ownership,
not one worker per edit.

## Model routing

Optional per harness — every agent file pins a default; change via each
harness's own mechanism.
OpenCode agents pin the merged form, e.g. `openai/gpt-6-astra#high`.

| Family | Claude (alias) | OpenCode openai preset | OpenCode go preset | Antigravity |
|---|---|---|---|---|
| Primary | fable, high | openai/gpt-6-astra, high | opencode-go/glm-5.2, high | session model |
| Discovery | haiku | openai/gpt-6-luna-fast (scout: gpt-6-luna) | opencode-go/deepseek-v4.1-flash | session model (planner pins pro) |
| Mechanical | haiku | openai/gpt-6-luna | opencode-go/mimo-v2.6-flash | — |
| Implementation | sonnet | openai/gpt-5.6-terra | opencode-go/mimo-v2.6-flash | session model |
| Hard implementation | opus | openai/gpt-6-sol | opencode-go/mimo-v2.6-pro | — |
| Review | opus | openai/gpt-6-sol | opencode-go/glm-5.2 | session model |
| Verification | sonnet | openai/gpt-5.6-terra | opencode-go/mimo-v2.6-flash | (reviewer-agent) |

## Provider prerequisites

- **Claude Code**: model aliases (fable/opus/sonnet/haiku) resolve on
  ≥ 2.1.263.
- **OpenCode, openai preset**: OpenAI auth (OAuth or API key) covering the
  pinned `openai/*` model IDs.
- **OpenCode, go preset**: an OpenCode Go API key (opencode.ai/console).
- Switch presets with `opencode/oc-preset` (assumptions in its header);
  any provider works by editing each agent's `model:` line.
- **Antigravity**: agents inherit the session model; only planner pins one.

## Supported versions

| Harness | Supported | Validated |
|---|---|---|
| Claude Code | ≥ 2.1.263 | 2.1.263 |
| OpenCode | 2.x (V2 `mcp.servers` semantics) | 2.0.14 (features); 1.18.29 baseline |
| Antigravity CLI | 1.1.x | 1.1.27 |

Platform validation status (Linux validated; macOS/WSL pending): docs/validation.md.

## Known bounded duplication

No harness supports includes, so runtime files must be self-contained and
carry operational copies of their charter and rules. This file is
canonical; the copies are bounded and acknowledged. Known accepted
duplication: the four OpenCode worker shell maps remain identical and
self-contained per agent (b07, 2026-09-27: the operator chose the safe option —
no shared top-level block, since it would apply to every agent in the
config chain and would need installer support to reach agents outside
this repo).
