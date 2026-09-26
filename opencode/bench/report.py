#!/usr/bin/env python3
"""Build results/<stamp>/report.md from runs.jsonl. Usage: report.py [results/<stamp>]"""
import json
import sys
from collections import defaultdict
from pathlib import Path

BENCH = Path(__file__).resolve().parent
SEAT_ORDER = ["orchestrator", "hard-implementer", "implementer", "reviewer", "explore"]


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def consistency(rs):
    """Fraction of reps with an identical pass result, per task, averaged across tasks.
    A task run once (no repeats) trivially agrees with itself (1.0)."""
    by_task = defaultdict(list)
    for r in rs:
        by_task[r["task"]].append(r["pass"])
    fracs = []
    for passes in by_task.values():
        t = sum(passes)
        fracs.append(max(t, len(passes) - t) / len(passes))
    return mean(fracs)


def row(model, rs):
    calls = sum(r["tool_calls"] for r in rs)
    errs = sum(r["tool_errors"] for r in rs)
    flags = []
    if any(r["timed_out"] for r in rs):
        flags.append(f"timeout×{sum(r['timed_out'] for r in rs)}")
    if any(r["error"] and not r["timed_out"] for r in rs):
        flags.append(f"error×{sum(bool(r['error']) and not r['timed_out'] for r in rs)}")
    denied = sum(r.get("tool_denied", 0) for r in rs)
    scores = [r["score"] for r in rs]
    return (f"| {model} | {len(rs)} | {mean([r['pass'] for r in rs]):.0%} "
            f"| {mean(scores):.2f} | {min(scores):.2f} | {consistency(rs):.0%} "
            f"| {mean([r['cost_usd_est'] for r in rs]):.4f} "
            f"| {mean([r['wall_s'] for r in rs]):.0f} | {(errs / calls if calls else 0):.0%} "
            f"({errs}/{calls}) | {denied} | {mean([r['requests'] for r in rs]):.1f} "
            f"| {'⚠ ' + ', '.join(flags) if flags else ''} |")


HEADER = ("| model | runs | pass | mean score | min score | consistency | mean $ est "
          "| mean wall s | tool-err rate | denied | mean requests | flags |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|---|")


def main():
    if len(sys.argv) > 1:
        d = Path(sys.argv[1])
    else:
        d = max((p for p in (BENCH / "results").iterdir() if (p / "runs.jsonl").exists()),
                key=lambda p: p.name)
    runs = [json.loads(line) for line in (d / "runs.jsonl").read_text().splitlines() if line]
    meta = json.loads((d / "meta.json").read_text()) if (d / "meta.json").exists() else {}
    usage = [json.loads(line) for line in (d / "usage.jsonl").read_text().splitlines()
             if line] if (d / "usage.jsonl").exists() else []

    def sort_key(item):
        rs = item[1]
        return (-mean([r["pass"] for r in rs]), -mean([r["score"] for r in rs]),
                mean([r["cost_usd_est"] for r in rs]))

    spend_ratio = meta.get("args", {}).get("spend_ratio", 3.2)
    cost_est_sum = sum(r["cost_usd_est"] for r in runs)
    out = [f"# Bench report — {d.name}", ""]
    out.append(f"Runs: {len(runs)}/{meta.get('planned', '?')} · Σ cost est: ${cost_est_sum:.4f} "
               f"· Σ cost (opencode): ${sum(r.get('cost_usd_opencode', 0) for r in runs):.4f} "
               f"· projected real $ (est × spend-ratio {spend_ratio}): "
               f"${cost_est_sum * spend_ratio:.2f} · Go usage delta est: "
               f"${meta.get('go_usage_delta_usd_est', '?')} · stop: {meta.get('stop_reason')}")
    if usage:
        def fmt(s):
            u = s.get("usage") or {}
            return ", ".join(f"{w} {u[w]['percent']}%" for w in ("rolling", "weekly", "monthly")
                             if w in u) or s.get("error", "?")
        out.append(f"Go usage: start [{fmt(usage[0])}] → end [{fmt(usage[-1])}] "
                   f"({len(usage)} snapshots in usage.jsonl)")
    out += ["", "Sorted by pass rate, then mean score, then cost. tool-err rate excludes "
            "permission denials (own column). ⚠ = at least one timeout/error.", ""]

    by_seat = defaultdict(lambda: defaultdict(list))
    by_model = defaultdict(list)
    for r in runs:
        by_seat[r["seat"]][r["model"]].append(r)
        by_model[r["model"]].append(r)
    for seat in [s for s in SEAT_ORDER if s in by_seat] + \
            sorted(s for s in by_seat if s not in SEAT_ORDER):
        out += [f"## {seat}", "", HEADER]
        out += [row(m, rs) for m, rs in sorted(by_seat[seat].items(), key=sort_key)]
        out.append("")
    out += ["## Overall (per model, all seats)", "", HEADER]
    out += [row(m, rs) for m, rs in sorted(by_model.items(), key=sort_key)]
    bad = [r for r in runs if r["error"]]
    if bad:
        out += ["", "## Errors / timeouts", ""]
        out += [f"- {r['model']} {r['task']}: {r['error']}" for r in bad]
    (d / "report.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(d / "report.md")


if __name__ == "__main__":
    main()
