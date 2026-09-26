#!/usr/bin/env python3
"""Scores a plan-01 response deterministically:
- coverage: each of the 4 required files owned by exactly one task (0.4)
- no bogus files referenced (0.3)
- required dependency edges present at the task level (0.3)
"""
import json
import re
import sys

REQUIRED_FILES = {
    "inventory/models.py",
    "inventory/report.py",
    "inventory/plugins.py",
    "inventory/cli.py",
}

# (dependent_file, file_it_must_depend_on)
REQUIRED_EDGES = [
    ("inventory/report.py", "inventory/models.py"),
    ("inventory/plugins.py", "inventory/report.py"),
    ("inventory/cli.py", "inventory/report.py"),
    ("inventory/cli.py", "inventory/plugins.py"),
]


def last_json_block(text):
    blocks = re.findall(r"```json\s*\n(.*?)```", text, re.DOTALL)
    return blocks[-1] if blocks else None


def norm(path):
    return str(path).strip().replace("\\", "/").lstrip("./")


def main():
    response_path = sys.argv[1]
    try:
        text = open(response_path, encoding="utf-8").read()
    except OSError:
        print('{"score": 0.0, "detail": "no response file"}')
        sys.exit(1)

    block = last_json_block(text)
    if block is None:
        print('{"score": 0.0, "detail": "no fenced json block found"}')
        sys.exit(1)

    try:
        plan = json.loads(block)
    except json.JSONDecodeError:
        print('{"score": 0.0, "detail": "json block did not parse"}')
        sys.exit(1)

    tasks = plan.get("tasks") if isinstance(plan, dict) else None
    if not isinstance(tasks, list) or not tasks:
        print('{"score": 0.0, "detail": "no tasks list found"}')
        sys.exit(1)

    file_owners = {}
    all_entries = 0
    bogus_entries = 0
    depends_on = {}

    for task in tasks:
        if not isinstance(task, dict):
            continue
        tid = task.get("id")
        files = [norm(f) for f in task.get("files", []) if isinstance(f, str)]
        depends_on[tid] = set(task.get("depends_on", []) or [])
        for f in files:
            all_entries += 1
            file_owners.setdefault(f, []).append(tid)
            if f not in REQUIRED_FILES:
                bogus_entries += 1

    covered = sum(1 for f in REQUIRED_FILES if len(file_owners.get(f, [])) == 1)
    coverage = covered / len(REQUIRED_FILES)

    no_bogus = 1.0 if all_entries == 0 else max(0.0, (all_entries - bogus_entries) / all_entries)

    edges_ok = 0
    for dependent_file, required_file in REQUIRED_EDGES:
        dep_owners = file_owners.get(dependent_file, [])
        req_owners = file_owners.get(required_file, [])
        if len(dep_owners) == 1 and len(req_owners) == 1:
            dep_task, req_task = dep_owners[0], req_owners[0]
            if req_task in depends_on.get(dep_task, set()):
                edges_ok += 1
    edge_score = edges_ok / len(REQUIRED_EDGES)

    score = round(0.4 * coverage + 0.3 * no_bogus + 0.3 * edge_score, 2)
    detail = (
        f"coverage={covered}/{len(REQUIRED_FILES)} "
        f"bogus={bogus_entries}/{all_entries} "
        f"edges={edges_ok}/{len(REQUIRED_EDGES)}"
    )
    print(json.dumps({"score": score, "detail": detail}))
    sys.exit(0 if score >= 0.75 else 1)


if __name__ == "__main__":
    main()
