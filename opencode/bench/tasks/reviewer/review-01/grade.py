#!/usr/bin/env python3
"""Scores a review-01 response: recall over 5 planted defects, matched by
file + line number within +-2."""
import json
import re
import sys

GROUND_TRUTH = [
    {"file": "inventory/importer.py", "line": 11, "kind": "resource-handling"},
    {"file": "inventory/importer.py", "line": 17, "kind": "security"},
    {"file": "inventory/importer.py", "line": 29, "kind": "off-by-one"},
    {"file": "inventory/importer.py", "line": 37, "kind": "logic-error"},
    {"file": "inventory/importer.py", "line": 45, "kind": "broken-contract"},
]


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

    matched_gt = set()
    matched_findings = 0
    for finding in findings:
        if not isinstance(finding, dict):
            continue
        f_file = finding.get("file")
        f_line = finding.get("line")
        if not isinstance(f_file, str) or not isinstance(f_line, (int, float)):
            continue
        f_file = norm_file(f_file)
        for idx, gt in enumerate(GROUND_TRUTH):
            if idx in matched_gt:
                continue
            if f_file == gt["file"] and abs(f_line - gt["line"]) <= 2:
                matched_gt.add(idx)
                matched_findings += 1
                break

    recall = len(matched_gt) / len(GROUND_TRUTH)
    false_positives = max(0, len(findings) - matched_findings)
    detail = f"recall {len(matched_gt)}/{len(GROUND_TRUTH)}, false_positives={false_positives}"
    result = {"score": round(recall, 2), "detail": detail}
    print(json.dumps(result))
    sys.exit(0 if recall >= 0.6 else 1)


if __name__ == "__main__":
    main()
