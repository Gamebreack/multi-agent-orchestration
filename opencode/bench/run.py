#!/usr/bin/env python3
"""OpenCode Go model bake-off runner. See README.md."""
import argparse
import concurrent.futures
import datetime
import fnmatch
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

import collect

BENCH = Path(__file__).resolve().parent
SEAT_VARIANT = {"orchestrator": "high", "hard-implementer": "high", "reviewer": "high",
                "implementer": "medium", "explore": "low"}
# Execution order: cheapest seat first, so a guard stop leaves every model with the same
# partial coverage (see README "Ordering").
EXEC_SEAT_ORDER = ["explore", "implementer", "reviewer", "orchestrator", "hard-implementer"]
WRITE_SEATS = {"implementer", "hard-implementer"}
BASH_ALLOW = ["python3 *", "ls", "ls *", "cat *", "grep *", "find *", "git *"]
# Checked after the allows (last match wins): keep bash inside the run dir, since
# external_directory is not enforced on bash arguments.
BASH_DENY_AFTER = ["* /*", "*~*", "*..*"]
USAGE_EVERY = 5


def agent_config(seat):
    perm = {"*": "deny", "read": "allow", "glob": "allow", "grep": "allow", "list": "allow",
            "edit": "deny", "bash": "deny", "task": "deny", "webfetch": "deny",
            "websearch": "deny", "external_directory": "deny"}
    if seat in WRITE_SEATS:
        perm["edit"] = "allow"
        perm["bash"] = {"*": "deny", **{p: "allow" for p in BASH_ALLOW},
                        **{p: "deny" for p in BASH_DENY_AFTER}}
    prompt = (f"You are the {seat} agent in an automated benchmark. Work only inside the "
              "current working directory. Nobody will answer questions: complete the task "
              "autonomously and end with your final answer.")
    return {"default_agent": f"bench-{seat}",
            "agent": {f"bench-{seat}": {"mode": "primary", "description": f"bench {seat}",
                                        "prompt": prompt, "permission": perm}}}


def discover_tasks(root, patterns):
    tasks = []
    for prompt in sorted(Path(root).glob("*/*/prompt.md")):
        tdir = prompt.parent
        tid = f"{tdir.parent.name}/{tdir.name}"
        if tdir.parent.name not in SEAT_VARIANT:
            continue
        if patterns and not any(fnmatch.fnmatch(tid, p) for p in patterns):
            continue
        tasks.append({"id": tid, "seat": tdir.parent.name, "dir": tdir})
    return tasks


def load_models(spec):
    p = Path(spec)
    if p.is_file():
        lines = p.read_text().splitlines()
    else:
        lines = spec.split(",")
    out = []
    for line in lines:
        line = line.split("#", 1)[0].strip()
        if line:
            out.append(line if "/" in line else f"opencode-go/{line}")
    return out


def resolve_variant(model_info, seat):
    want = SEAT_VARIANT[seat]
    ids = {v.get("id") for v in (model_info or {}).get("variants") or []}
    return want if want in ids else None


def run_cmd(cmd, cwd, timeout, env=None, stdin=None, stdout=None, stderr=None):
    """Run in its own process group; kill the whole group on timeout. Returns (rc, timed_out)."""
    p = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=stdin, stdout=stdout, stderr=stderr,
                         start_new_session=True)
    try:
        return p.wait(timeout=timeout), False
    except subprocess.TimeoutExpired:
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(p.pid, sig)
            except ProcessLookupError:
                break
            try:
                p.wait(timeout=10)
                break
            except subprocess.TimeoutExpired:
                continue
        return None, True


class RollingGuard:
    """Stops new launches once the Go rolling-window percent has moved --max-rolling-pct
    since the first check (handles a mid-run window reset, where percent drops). This is the
    primary spend guard: round 1's token-based cost_usd_est estimate totalled $3.36 while real
    Go usage moved $10.8 (rolling 1%->88%), a 3.2x gap, so cost_usd_est alone cannot be trusted
    to stop the run in time."""

    def __init__(self, max_pct, cache_s=30):
        self.max_pct = max_pct
        self.cache_s = cache_s
        self.lock = threading.Lock()
        self.prev_pct = None
        self.cum_pct = 0.0
        self._cache_ts = 0.0
        self._cache_snap = None

    def _snapshot(self):
        now = time.monotonic()
        if self._cache_snap is None or now - self._cache_ts >= self.cache_s:
            self._cache_snap = collect.go_usage_snapshot()
            self._cache_ts = now
        return self._cache_snap

    def check(self):
        """Returns a stop-reason string, or None if it's fine to launch another run."""
        with self.lock:
            snap = self._snapshot()
            usage = snap.get("usage")
            if not usage:
                return None  # transient fetch error: don't block the run on it
            bad = [w for w, v in usage.items() if v.get("status") != "ok"]
            if bad:
                return f"Go usage window(s) not ok: {bad}"
            cur = usage["rolling"]["percent"]
            if self.prev_pct is None:
                self.prev_pct = cur
            elif cur >= self.prev_pct:
                self.cum_pct += cur - self.prev_pct
                self.prev_pct = cur
            else:  # window reset mid-run: the new (lower) percent is all fresh usage
                self.cum_pct += cur
                self.prev_pct = cur
            if self.cum_pct >= self.max_pct:
                return f"rolling usage +{self.cum_pct:.1f}pp ≥ --max-rolling-pct {self.max_pct}"
            return None


def run_one(job, args, stamp_dir, work_root):
    model, task, info = job["model"], job["task"], job["info"]
    short = model.split("/", 1)[1]
    suffix = f"-rep{job['rep']}" if args.repeat > 1 else ""
    work = work_root / short / task["seat"] / (task["dir"].name + suffix)
    final = stamp_dir / "runs" / short / task["seat"] / (task["dir"].name + suffix)
    rec = {"model": model, "seat": task["seat"], "task": task["id"], "variant": job["variant"],
           "rep": job["rep"],
           "pass": False, "score": 0.0, "detail": "", "wall_s": 0.0, "requests": 0,
           "tokens_in": 0, "tokens_out": 0, "tokens_reasoning": 0, "tokens_cache_read": 0,
           "tokens_cache_write": 0, "cost_usd_est": 0.0, "cost_usd_opencode": 0.0,
           "tool_calls": 0, "tool_errors": 0, "tool_denied": 0, "timed_out": False,
           "error": None, "session_id": None, "served_models": [], "run_dir": str(final)}
    try:
        shutil.copytree(args.fixture, work, ignore=shutil.ignore_patterns("reference"))
        setup = task["dir"] / "setup.sh"
        if setup.exists():
            rc, to = run_cmd(["bash", str(setup), str(work)], task["dir"], 300,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if rc != 0:
                raise RuntimeError(f"setup.sh failed rc={rc} timed_out={to}")
        bench = work / ".bench"
        bench.mkdir(exist_ok=True)
        # PWD must match cwd: opencode takes the project dir from $PWD, not getcwd().
        env = dict(os.environ, PWD=str(work),
                   OPENCODE_CONFIG_CONTENT=json.dumps(agent_config(task["seat"])))
        mflag = model + (f"#{job['variant']}" if job["variant"] else "")
        cmd = ["opencode", "run", "--standalone", "--auto", "--agent", f"bench-{task['seat']}",
               "--model", mflag, "--format", "json", "--title", f"bench {short} {task['id']}"]
        t0 = time.monotonic()
        with open(task["dir"] / "prompt.md", "rb") as fin, \
                open(bench / "events.jsonl", "wb") as fout, open(bench / "stderr.txt", "wb") as ferr:
            rc, rec["timed_out"] = run_cmd(cmd, work, args.timeout_s, env=env,
                                           stdin=fin, stdout=fout, stderr=ferr)
        rec["wall_s"] = round(time.monotonic() - t0, 1)
        ev = collect.event_metrics(bench / "events.jsonl")
        rec["session_id"] = ev["session_id"]
        for k in ("tool_calls", "tool_errors", "tool_denied", "tool_error_samples", "run_errors"):
            rec[k] = ev[k]
        text = ev["final_text"]
        if ev["session_id"]:
            sm = collect.session_metrics(ev["session_id"], info)
            text = text or sm.pop("db_text")
            sm.pop("db_text", None)
            rec.update(sm)
            rec["cost_usd_est"] = round(rec["cost_usd_est"], 6)
            rec["cost_usd_opencode"] = round(rec["cost_usd_opencode"], 6)
            if rec["served_models"] and not all(s.startswith(model + "#")
                                                for s in rec["served_models"]):
                rec["error"] = f"served by unexpected model: {rec['served_models']}"
        (bench / "response.md").write_text(text or "", encoding="utf-8")
        if rec["timed_out"]:
            rec["error"] = rec["error"] or f"timeout after {args.timeout_s}s"
        elif rc != 0:
            rec["error"] = rec["error"] or f"opencode run rc={rc}" + (
                f" ({ev['run_errors'][-1]})" if ev["run_errors"] else "")
        elif not ev["session_id"]:
            rec["error"] = "no session id in event stream"
        if not rec["timed_out"]:
            chk = subprocess.run(["bash", str(task["dir"] / "check.sh"), str(work)],
                                 cwd=task["dir"], capture_output=True, text=True, timeout=300)
            res = {}
            for line in reversed(chk.stdout.splitlines()):
                try:
                    res = json.loads(line)
                    break
                except ValueError:
                    continue
            rec["pass"] = chk.returncode == 0 and rec["error"] is None
            rec["score"] = float(res.get("score", 0.0) or 0.0)
            rec["detail"] = str(res.get("detail", chk.stderr.strip()[-300:]))
    except Exception as e:
        rec["error"] = f"{type(e).__name__}: {e}"
    finally:
        if work.exists():
            final.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(work), str(final))
    return rec


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--models-file", default=str(BENCH / "models.txt"),
                    help="file with one model per line, or comma list")
    ap.add_argument("--tasks", nargs="*", default=[], help="fnmatch globs on seat/task-id")
    ap.add_argument("--tasks-root", default=str(BENCH / "tasks"))
    ap.add_argument("--fixture", default=str(BENCH / "fixture"))
    ap.add_argument("--parallel", type=int, default=3)
    ap.add_argument("--repeat", type=int, default=1, help="reruns per (model, task)")
    ap.add_argument("--budget-usd", type=float, default=10.0,
                    help="secondary guard: stop when cost_usd_est sum x --spend-ratio "
                         "reaches this")
    ap.add_argument("--spend-ratio", type=float, default=3.2,
                    help="cost_usd_est underestimates real Go spend (round 1: est $3.36 vs "
                         "real $10.8, a 3.2x gap); --budget-usd is checked against "
                         "cost_usd_est x this ratio")
    ap.add_argument("--max-rolling-pct", type=float, default=25,
                    help="primary guard: stop launching once the Go rolling-window percent "
                         "has moved this many points since the run started")
    ap.add_argument("--timeout-s", type=int, default=600, help="wall seconds per run")
    ap.add_argument("--go-monthly-usd", type=float, default=60.0,
                    help="Go monthly limit used to convert usage %% to $ (informational only)")
    ap.add_argument("--work-root", default=str(Path(tempfile.gettempdir()) / "opencode-bench"),
                    help="run dirs live here during a run (must be outside any dir holding "
                         "opencode config/AGENTS.md), then move into results/")
    ap.add_argument("--stamp", default=datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    ap.add_argument("--results-dir", default=None,
                    help="reuse this results dir (relative to results/, or absolute) instead "
                         "of results/<stamp>; combine with --skip-done to resume")
    ap.add_argument("--skip-done", action="store_true",
                    help="skip (model, task, rep) triples already in the results dir's "
                         "runs.jsonl")
    ap.add_argument("--retry-failed", action="store_true",
                    help="with --skip-done, still rerun triples whose recorded run errored "
                         "or timed out")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, run nothing")
    args = ap.parse_args()

    catalog = collect.model_catalog()
    models = load_models(args.models_file)
    tasks = discover_tasks(args.tasks_root, args.tasks)
    unknown = [m for m in models if m not in catalog]
    if unknown:
        sys.exit(f"models not in /api/model: {unknown}")
    if not tasks:
        sys.exit(f"no tasks under {args.tasks_root} matching {args.tasks}")
    if not Path(args.fixture).is_dir():
        sys.exit(f"fixture missing: {args.fixture}")

    if args.results_dir:
        stamp_dir = Path(args.results_dir)
        if not stamp_dir.is_absolute():
            stamp_dir = BENCH / "results" / stamp_dir
    else:
        stamp_dir = BENCH / "results" / args.stamp

    # task-major, cheapest-seat first, reps and models interleaved within each task: a guard
    # stop leaves every model with the same partial coverage. See README "Ordering".
    tasks = sorted(tasks, key=lambda t: (EXEC_SEAT_ORDER.index(t["seat"])
                                        if t["seat"] in EXEC_SEAT_ORDER else len(EXEC_SEAT_ORDER),
                                        t["id"]))
    jobs = [{"model": m, "task": t, "rep": r, "info": catalog[m],
             "variant": resolve_variant(catalog[m], t["seat"])}
            for t in tasks for r in range(args.repeat) for m in models]

    if args.skip_done:
        done = set()
        runs_path = stamp_dir / "runs.jsonl"
        if runs_path.exists():
            for line in runs_path.read_text().splitlines():
                if not line:
                    continue
                r = json.loads(line)
                if args.retry_failed and (r.get("error") or r.get("timed_out")):
                    continue
                done.add((r["model"], r["task"], r.get("rep", 0)))
        jobs = [j for j in jobs if (j["model"], j["task"]["id"], j["rep"]) not in done]

    if args.dry_run:
        for j in jobs:
            print(json.dumps({"model": j["model"], "task": j["task"]["id"], "rep": j["rep"],
                              "variant": j["variant"],
                              "check_sh": (j["task"]["dir"] / "check.sh").exists()}))
        snap = collect.go_usage_snapshot()
        print(f"# {len(jobs)} runs; go usage now: {json.dumps(snap)}")
        return

    stamp_dir.mkdir(parents=True, exist_ok=True)
    work_root = Path(args.work_root) / args.stamp
    work_root.mkdir(parents=True, exist_ok=True)
    tracker = collect.UsageTracker(args.go_monthly_usd)
    rolling_guard = RollingGuard(args.max_rolling_pct)
    lock = threading.Lock()
    state = {"done": 0, "cost": 0.0, "stop": None}
    meta = {"args": vars(args), "started": time.time(), "planned": len(jobs)}

    def snapshot(tag):
        snap = collect.go_usage_snapshot()
        snap["tag"] = tag
        tracker.add(snap)
        snap["delta_usd_est"] = round(tracker.delta_usd(), 4)
        snap["runs_done"], snap["cost_usd_est_sum"] = state["done"], round(state["cost"], 6)
        with open(stamp_dir / "usage.jsonl", "a") as f:
            f.write(json.dumps(snap) + "\n")
        print(f"[usage {tag}] {json.dumps(snap.get('usage') or snap.get('error'))} "
              f"delta≈${snap['delta_usd_est']}", flush=True)

    def guarded(job):
        if state["stop"]:
            return None
        reason = rolling_guard.check()
        if reason:
            with lock:
                state["stop"] = state["stop"] or reason
            return None
        rec = run_one(job, args, stamp_dir, work_root)
        with lock:
            state["done"] += 1
            state["cost"] += rec["cost_usd_est"]
            with open(stamp_dir / "runs.jsonl", "a") as f:
                f.write(json.dumps(rec) + "\n")
            print(f"[{state['done']}/{len(jobs)}] {rec['model']} {rec['task']} "
                  f"rep={rec['rep']} pass={rec['pass']} score={rec['score']} "
                  f"${rec['cost_usd_est']:.4f} {rec['wall_s']}s err={rec['error']}", flush=True)
            projected = state["cost"] * args.spend_ratio
            if projected >= args.budget_usd:
                state["stop"] = state["stop"] or (
                    f"projected real spend ${projected:.2f} (cost_usd_est ${state['cost']:.4f} "
                    f"x spend-ratio {args.spend_ratio}) ≥ --budget-usd {args.budget_usd}")
            if state["done"] % USAGE_EVERY == 0:
                snapshot(f"after-{state['done']}")
        return rec

    snapshot("start")
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.parallel) as pool:
            list(pool.map(guarded, jobs))
    except KeyboardInterrupt:
        state["stop"] = "interrupted"
        raise
    finally:
        snapshot("end")
        meta.update(finished=time.time(), runs_done=state["done"],
                    cost_usd_est_sum=round(state["cost"], 6), stop_reason=state["stop"],
                    go_usage_delta_usd_est=round(tracker.delta_usd(), 4),
                    projected_real_usd=round(state["cost"] * args.spend_ratio, 4))
        (stamp_dir / "meta.json").write_text(json.dumps(meta, indent=2, default=str))
        shutil.rmtree(work_root, ignore_errors=True)
    print(f"done: {state['done']}/{len(jobs)} runs, stop={state['stop']}, results in {stamp_dir}")
    print(f"report: python3 {BENCH / 'report.py'} {stamp_dir}")


if __name__ == "__main__":
    main()
