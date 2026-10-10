# Tasks

## 1. Remove harness toolkits

- [x] 1.1 `git rm -r agents hooks opencode antigravity install.sh uninstall.sh` and verify none of those paths appear in `git ls-files`
- [x] 1.2 `git rm docs/policies.md docs/validation.md docs/harness-comparison.md docs/opencode.md docs/antigravity.md docs/claude-code-observations.md` and verify `git ls-files docs` lists only `docs/megaplan/` files
- [x] 1.3 `git rm .env.example` and remove the bench-results and Python-cache entries from `.gitignore`; verify `.gitignore` still ignores `.env` and has no `opencode/` or Python lines

## 2. Fix references in kept files

- [x] 2.1 Edit `AGENTS.md` to drop the harness-toolkit paragraph and describe the repo as hybrid ICM + agent-core; verify it stays under 80 lines and names no removed path
- [x] 2.2 Edit `CONTEXT.md` routing table to remove rows for removed paths and add a row for `openspec/` (agent-core change); verify it stays under 80 lines and names no removed path
- [x] 2.3 Rewrite `README.md` for the new direction (hybrid ICM starter + agent-core in progress); verify every link in it resolves to an existing file
- [x] 2.4 Edit `starter/README.md` to drop the `docs/policies.md` pointer; verify it names no removed path
- [x] 2.5 Edit `docs/megaplan/glossary.md`: remove Harness/Preset/oc-preset rows and give tier names (orchestrator, explore, mechanical, implementer, hard-implementer, verifier, reviewer) plain definitions with no file pointers; verify every tier named in `stages/*/CONTEXT.md` has a glossary row
- [x] 2.6 Rewrite the "what already exists" list in `docs/megaplan/megaplan.md` to current truth; verify it names no removed path

## 3. Integration check

- [x] 3.1 Run `grep -rnE "opencode|antigravity|agents/|hooks/|install\.sh|uninstall\.sh|policies\.md|validation\.md|harness-comparison" --include=*.md . --exclude-dir=openspec --exclude-dir=.claude --exclude-dir=.agents` and verify the only hits are in `docs/megaplan/done.md`
- [x] 3.2 Verify `docs/megaplan/done.md` is unchanged (`git diff --quiet HEAD -- docs/megaplan/done.md`)

## Workflow follow-up

- Commit only with explicit operator authorization (AGENTS.md hard rule).
- Archive the change after operator review.
