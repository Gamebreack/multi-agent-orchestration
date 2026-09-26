#!/usr/bin/env python3
"""Metrics collection for bench runs: model catalog/prices, session metrics, Go usage."""
import json
import os
import sqlite3
import subprocess
import time
import urllib.request
from pathlib import Path

DB_PATH = Path.home() / ".local/share/opencode/opencode.db"
AUTH_PATH = Path.home() / ".local/share/opencode/auth.json"
# Same endpoint the @cardinal4/opencode-quota plugin uses (dist/lib/opencode-go.js).
GO_USAGE_URL = "https://opencode.ai/zen/go/v1/usage"
# Go limits per window as a fraction of the monthly limit (opencode.ai/docs/go).
GO_WINDOW_SHARE = {"rolling": 0.2, "weekly": 0.5, "monthly": 1.0}


def model_catalog():
    """{'provider/model': model dict} from the running service's /api/model."""
    out = subprocess.run(["opencode", "api", "GET", "/api/model"],
                         capture_output=True, text=True, timeout=60, check=True).stdout
    return {f"{m['providerID']}/{m['id']}": m for m in json.loads(out)["data"]}


def _price_for(model, prompt_tokens):
    """Pick the cost tier: highest context tier whose size the prompt exceeds, else base."""
    tiers = model.get("cost") or []
    if isinstance(tiers, dict):
        tiers = [tiers]
    base = next((t for t in tiers if "tier" not in t), tiers[0] if tiers else {})
    best, best_size = base, -1
    for t in tiers:
        size = (t.get("tier") or {}).get("size")
        if size is not None and prompt_tokens > size and size > best_size:
            best, best_size = t, size
    return best


def estimate_cost(model, tokens):
    """USD from one message's tokens × catalog prices (per 1M tokens)."""
    cache = tokens.get("cache") or {}
    prompt = tokens.get("input", 0) + cache.get("read", 0) + cache.get("write", 0)
    p = _price_for(model, prompt)
    pc = p.get("cache") or {}
    return (tokens.get("input", 0) * p.get("input", 0)
            + (tokens.get("output", 0) + tokens.get("reasoning", 0)) * p.get("output", 0)
            + cache.get("read", 0) * pc.get("read", 0)
            + cache.get("write", 0) * pc.get("write", 0)) / 1e6


def session_metrics(session_id, model_info):
    """Token/cost/model metrics for one session from the local OpenCode DB (read-only)."""
    con = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True, timeout=30)
    try:
        rows = con.execute(
            "select data from session_message where session_id=? and type='assistant' order by seq",
            (session_id,)).fetchall()
        srow = con.execute("select agent, model, idle_outcome from session_v2 where id=?",
                           (session_id,)).fetchone()
    finally:
        con.close()
    m = {"requests": 0, "tokens_in": 0, "tokens_out": 0, "tokens_reasoning": 0,
         "tokens_cache_read": 0, "tokens_cache_write": 0, "cost_usd_est": 0.0,
         "cost_usd_opencode": 0.0, "served_models": [], "agent": None, "idle_outcome": None,
         "db_text": ""}
    served = set()
    for (data,) in rows:
        d = json.loads(data)
        m["requests"] += 1
        t = d.get("tokens") or {}
        c = t.get("cache") or {}
        m["tokens_in"] += t.get("input", 0)
        m["tokens_out"] += t.get("output", 0)
        m["tokens_reasoning"] += t.get("reasoning", 0)
        m["tokens_cache_read"] += c.get("read", 0)
        m["tokens_cache_write"] += c.get("write", 0)
        m["cost_usd_opencode"] += d.get("cost") or 0.0
        if model_info:
            m["cost_usd_est"] += estimate_cost(model_info, t)
        md = d.get("model") or {}
        served.add(f"{md.get('providerID')}/{md.get('id')}#{md.get('variant')}")
        texts = [x.get("text", "") for x in d.get("content") or [] if x.get("type") == "text"]
        if any(texts):
            m["db_text"] = "".join(texts)
    m["served_models"] = sorted(served)
    if srow:
        m["agent"], m["idle_outcome"] = srow[0], srow[2]
    return m


def event_metrics(events_path):
    """Session id, final assistant text and tool-call stats from `opencode run --format json`."""
    session_id, texts, last_msg = None, {}, None
    calls = errors = denied = 0
    error_samples, run_errors = [], []
    with open(events_path, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            session_id = session_id or ev.get("sessionID")
            part = ev.get("part") or {}
            if ev.get("type") == "text":
                mid = part.get("messageID")
                texts.setdefault(mid, []).append(part.get("text", ""))
                last_msg = mid
            elif ev.get("type") == "error":
                e = ev.get("error") or {}
                run_errors.append(f"{e.get('type')}: {str(e.get('message', ''))[:160]}")
            elif ev.get("type") == "tool_use":
                calls += 1
                st = part.get("state") or {}
                if st.get("status") == "error":
                    err = str(st.get("error", ""))
                    if err.startswith("Permission denied"):
                        denied += 1
                    else:
                        errors += 1
                    if len(error_samples) < 5:
                        error_samples.append(f"{part.get('tool')}: {err[:160]}")
    return {"session_id": session_id,
            "final_text": "".join(texts.get(last_msg, [])) if last_msg else "",
            "tool_calls": calls, "tool_errors": errors, "tool_denied": denied,
            "tool_error_samples": error_samples, "run_errors": run_errors}


def go_usage_snapshot():
    """Raw Go usage windows (percent + resetsAt). Needs a non-urllib UA (Cloudflare 1010)."""
    key = os.environ.get("OPENCODE_API_KEY")
    if not key:
        key = json.loads(AUTH_PATH.read_text())["opencode-go"]["key"]
    req = urllib.request.Request(GO_USAGE_URL, headers={
        "Authorization": f"Bearer {key}", "Accept": "application/json",
        "User-Agent": "opencode-bench/1.0"})
    snap = {"ts": time.time()}
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            snap["usage"] = json.loads(r.read())["usage"]
    except Exception as e:  # recorded, never fatal
        snap["error"] = f"{type(e).__name__}: {e}"
    return snap


class UsageTracker:
    """Accumulates Go usage % per window across snapshots, handling window resets."""

    def __init__(self, monthly_usd):
        self.monthly_usd = monthly_usd
        self.prev = {}
        self.pct = {w: 0.0 for w in GO_WINDOW_SHARE}
        self.rate_limited = False

    def add(self, snap):
        usage = snap.get("usage") or {}
        self.rate_limited = any((usage.get(w) or {}).get("status") == "rate-limited"
                                for w in GO_WINDOW_SHARE)
        for w in GO_WINDOW_SHARE:
            cur = usage.get(w)
            if not cur:
                continue
            prev = self.prev.get(w)
            if prev is not None:
                # resetsAt drifts on the rolling window, so a drop in percent is the only
                # reliable reset signal; after a reset the new percent is all fresh usage.
                if cur["percent"] >= prev["percent"]:
                    self.pct[w] += cur["percent"] - prev["percent"]
                else:
                    self.pct[w] += cur["percent"]
            self.prev[w] = cur

    def delta_usd(self):
        """Largest per-window $ estimate of usage since the first snapshot."""
        return max(self.pct[w] / 100 * GO_WINDOW_SHARE[w] * self.monthly_usd
                   for w in GO_WINDOW_SHARE)
