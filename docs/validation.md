# Validation status

What is actually tested on which platform — no claims beyond the evidence.
Evidence per cell lives in the linked docs; re-validate a new platform with
the steps at the bottom.

| Harness | Linux | macOS | WSL |
|---|---|---|---|
| OpenCode | validated | pending | pending |
| Claude Code | validated | pending | pending |
| Antigravity | validated | pending | pending |

Validated means: the harness's orchestration layer ran end to end on that
platform — agents loaded, boundaries enforced, install/uninstall cycle passed.
Pending means: no machine was available; nothing beyond the evidence below is
claimed.

## Evidence (Linux)

- **OpenCode** — the toolkit was built and run on OpenCode on Linux —
  seven of the eight tiers executed real work (hard-implementer was defined
  and statically verified, never needed live); the read-only boundary held
  across all sessions (docs/opencode.md); the V2 migration and the
  install/uninstall cycles passed fresh verification; oc-preset ran live.
- **Claude Code** — agents, the manager hook and its allow-list were
  validated live on 2.1.263 (docs/claude-code-observations.md); the installer
  settings merge and uninstall passed sandbox cycles (recorded in
  docs/megaplan/done.md).
- **Antigravity** — the multitask-team plugin's tool whitelist and delegation
  were verified by tool listing, a delegation smoke test and a scoping probe
  (docs/antigravity.md); install/uninstall passed sandbox cycles (recorded
  in docs/megaplan/done.md).

## Validating a new platform

1. Run the installer cycle in a sandbox — `CLAUDE_CONFIG_DIR`,
   `OPENCODE_CONFIG_DIR`, `GEMINI_CONFIG_DIR`, `AGYO_BIN_DIR` pointing at
   temp dirs: install, uninstall, reinstall, --purge.
2. Install for real, then run one small work item through the stages with
   that harness's agents: a read-only primary, delegated edits, fresh
   verification.
3. Record the result here — validated or failed — with the same evidence
   shape as the Linux section.

Known portability caveats: install.sh, uninstall.sh and oc-preset assume a
GNU userland (sed -i, date, cmp, install) — macOS ships BSD sed; test before
trusting (oc-preset's header documents its assumptions).
