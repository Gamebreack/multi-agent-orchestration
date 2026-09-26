"""Command-line entry point for the inventory tool."""
import argparse
import sys
from typing import List, Optional

from . import report
from .ledger import Ledger
from .models import Item
from .plugins import get_formatter, register_formatter
from .storage import Storage
from .validation import ValidationError, validate_item

register_formatter("text", report.format_text)
register_formatter("csv", report.format_csv)
register_formatter("markdown", report.format_markdown)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="inventory")
    sub = parser.add_subparsers(dest="command", required=True)

    add_p = sub.add_parser("add", help="add a new item")
    add_p.add_argument("id")
    add_p.add_argument("name")
    add_p.add_argument("quantity", type=int)
    add_p.add_argument("price", type=float)

    adjust_p = sub.add_parser("adjust", help="adjust stock for an item")
    adjust_p.add_argument("id")
    adjust_p.add_argument("delta", type=int)
    adjust_p.add_argument("--reason", default="")

    report_p = sub.add_parser("report", help="print a report of all items")
    report_p.add_argument("--format", default="text")

    return parser


def run(argv: List[str], storage: Optional[Storage] = None) -> str:
    """Execute a CLI command against `storage`, returning textual output."""
    storage = storage if storage is not None else Storage()
    ledger = Ledger(storage)
    args = build_parser().parse_args(argv)

    if args.command == "add":
        data = {
            "id": args.id,
            "name": args.name,
            "quantity": args.quantity,
            "price": args.price,
        }
        validate_item(data)
        storage.add(Item(**data))
        return f"added {args.id}"

    if args.command == "adjust":
        ledger.adjust(args.id, args.delta, args.reason)
        return f"balance {args.id} = {ledger.balance(args.id)}"

    if args.command == "report":
        formatter = get_formatter(args.format)
        return formatter(storage.all())

    raise ValidationError(f"unknown command: {args.command}")


def main(argv: Optional[List[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    try:
        print(run(argv))
    except ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
