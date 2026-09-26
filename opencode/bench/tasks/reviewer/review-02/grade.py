#!/usr/bin/env python3
"""Scores a review-02 response: recall over 6 planted defects, matched by
file + line number within +-2, minus a penalty for flagging either of the
2 decoy lines (things that look wrong but are actually correct)."""
import json
import re
import sys

GROUND_TRUTH = [
    {"file": "inventory/pricing.py", "line": 18, "kind": "eq-hash-contract"},
    {"file": "inventory/pricing.py", "line": 21, "kind": "mutable-default"},
    {"file": "inventory/pricing.py", "line": 43, "kind": "float-rounding"},
    {"file": "inventory/pricing.py", "line": 59, "kind": "swallowed-exception"},
    {"file": "inventory/pricing.py", "line": 61, "kind": "iterator-reuse"},
    {"file": "inventory/pricing.py", "line": 66, "kind": "toctou"},
]

DECOYS = [
    {"file": "inventory/pricing.py", "line": 15},  # NotImplemented in __eq__: correct
    {"file": "inventory/pricing.py", "line": 54},  # newline="" for csv.writer: correct
]

DECOY_PENALTY = 0.1


def last_json_block(text):
    blocks = re.findall(r"```json\s*\n(.*?)```", text, re.DOTALL)
    return blocks[-1] if blocks else None


def norm_file(path):
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
        findings = json.loads(block)
    except json.JSONDecodeError:
        print('{"score": 0.0, "detail": "json block did not parse"}')
        sys.exit(1)

    if not isinstance(findings, list):
        print('{"score": 0.0, "detail": "json block is not a list"}')
        sys.exit(1)

    valid_findings = []
    for finding in findings:
        if not isinstance(finding, dict):
            continue
        f_file = finding.get("file")
        f_line = finding.get("line")
        if not isinstance(f_file, str) or not isinstance(f_line, (int, float)):
            continue
        valid_findings.append((norm_file(f_file), f_line))

    matched_gt = set()
    for f_file, f_line in valid_findings:
        for idx, gt in enumerate(GROUND_TRUTH):
            if idx in matched_gt:
                continue
            if f_file == gt["file"] and abs(f_line - gt["line"]) <= 2:
                matched_gt.add(idx)
                break

    matched_decoys = set()
    for f_file, f_line in valid_findings:
        for idx, decoy in enumerate(DECOYS):
            if idx in matched_decoys:
                continue
            if f_file == decoy["file"] and abs(f_line - decoy["line"]) <= 2:
                matched_decoys.add(idx)
                break

    recall = len(matched_gt) / len(GROUND_TRUTH)
    score = max(0.0, min(1.0, recall - DECOY_PENALTY * len(matched_decoys)))
    detail = (f"recall {len(matched_gt)}/{len(GROUND_TRUTH)}, "
              f"decoy_hits={len(matched_decoys)}/{len(DECOYS)}")
    result = {"score": round(score, 2), "detail": detail}
    print(json.dumps(result))
    sys.exit(0 if score >= 0.6 else 1)


if __name__ == "__main__":
    main()
