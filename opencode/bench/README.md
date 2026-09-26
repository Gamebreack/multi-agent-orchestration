# OpenCode Go model bake-off

Runs each model in a models file on each task under `tasks/<seat>/<task-id>/`, scores it with
the task's `check.sh` and writes `results/<stamp>/{runs.jsonl,usage.jsonl,meta.json,report.md}`.

How each run works: `fixture/` is copied to `$TMPDIR/opencode-bench/<stamp>/...` (outside the repo, so it doesn't pick up `opencode/opencode.jsonc` or `AGENTS.md`) → `setup.sh` → `opencode run --standalone --auto --agent bench-<seat> --model <m>#<variant>` with `prompt.md` on stdin and the seat's agent/permissions in `OPENCODE_CONFIG_CONTENT` → `.bench/response.md` → `check.sh` → run dir moved to `results/<stamp>/runs/<model>/<seat>/<task>/`. Tokens/cost/served model come from `~/.local/share/opencode/opencode.db` (`session_message`), tool calls/errors from `.bench/events.jsonl`. Requires the background service (`opencode api`).

## Ordering

Task-major, cheapest seat first: `explore` → `implementer` → `reviewer` → `orchestrator` →
`hard-implementer`, tasks alphabetical within a seat; `--repeat` reps and models interleaved
inside each task. A guard stop leaves every model with the same partial coverage.

## Dry run (plan only, no model calls)

    python3 run.py --dry-run --models-file models-r2.txt --repeat 2 --tasks 'implementer/*'

## Full run

    python3 run.py --models-file models-r2.txt --tasks '*/fix-03' '*/refactor-02' '*/review-02' \
        --repeat 2 --parallel 3 --max-rolling-pct 25 --budget-usd 3

Flags: `--models-file` (default `models.txt`; one model per line or comma list), `--tasks`
(fnmatch globs on `seat/task-id`, e.g. `'*/fix-03'`, `'reviewer/*'`), `--repeat` (reruns per
model×task, default 1), `--timeout-s` (600/run), `--parallel` (3).

**Guards**, checked before every run launch: `--max-rolling-pct` (default 25, primary) stops new
launches once the Go rolling-window `percent` has moved that many points since the run started
(handles a mid-run reset, stops if any window's `status != "ok"`) — real spend, via a cached
(30 s) call to the Go usage endpoint. `--budget-usd` (default 10) is a secondary guard on
Σ`cost_usd_est` × `--spend-ratio` (default 3.2: round 1's estimate totalled $3.36 while real Go
usage moved $10.8, a 3.2x gap).

**Resume:** `--results-dir <dir>` reuses a results dir (under `results/`, or absolute) instead of
a fresh `--stamp`. `--skip-done` skips (model, task, rep) triples already in its `runs.jsonl`;
`--retry-failed` still reruns ones that errored or timed out.

## Report

    python3 report.py results/<stamp>    # default: latest stamp

`report.md` has one table per seat (pass rate, mean/min score, consistency — fraction of reps
with an identical pass result — mean $, mean wall, tool-error rate, denials, requests) plus an
overall per-model table, and the projected real $ (Σ cost_usd_est × spend-ratio) in the header.
⚠ marks timeouts/errors, detailed at the end; see `results/<stamp>/runs/...` and
`.bench/{events.jsonl,stderr.txt}` per run.
