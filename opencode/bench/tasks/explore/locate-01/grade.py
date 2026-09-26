#!/usr/bin/env python3
"""Scores a locate-01 response: exact-match fraction over 5 questions."""
import json
import re
import sys

ANSWERS = {
    "q1": {"file": "inventory/models.py", "symbols": {"total_value", "item.total_value"}},
    "q2": {"file": "inventory/validation.py", "symbols": {"validate_item"}},
    "q3": {"file": "inventory/validation.py", "symbols": {"max_name_length"}},
    "q4": {"file": "inventory/ledger.py", "symbols": {"adjust", "ledger.adjust"}},
    "q5": {"file": "inventory/report.py", "symbols": {"format_csv"}},
}


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
        answers = json.loads(block)
    except json.JSONDecodeError:
        print('{"score": 0.0, "detail": "json block did not parse"}')
        sys.exit(1)

    if not isinstance(answers, dict):
        print('{"score": 0.0, "detail": "json block is not an object"}')
        sys.exit(1)

    correct = 0
    for key, expected in ANSWERS.items():
        got = answers.get(key)
        if not isinstance(got, dict):
            continue
        got_file = norm_file(got.get("file", ""))
        got_symbol = str(got.get("symbol", "")).strip().lower()
        if got_file.endswith(expected["file"]) and got_symbol in expected["symbols"]:
            correct += 1

    fraction = correct / len(ANSWERS)
    detail = f"{correct}/{len(ANSWERS)} correct"
    print(json.dumps({"score": round(fraction, 2), "detail": detail}))
    sys.exit(0 if fraction >= 0.8 else 1)


if __name__ == "__main__":
    main()
