"""Report formatting for inventory items."""
from typing import List

from .models import Item, Transaction


def format_text(items: List[Item]) -> str:
    lines = [f"{i.id}\t{i.name}\t{i.quantity}\t{i.price:.2f}" for i in _sorted(items)]
    return "\n".join(lines)


def format_csv(items: List[Item]) -> str:
    lines = ["id,name,quantity,price"]
    lines += [f"{i.id},{i.name},{i.quantity},{i.price:.2f}" for i in _sorted(items)]
    return "\n".join(lines)


def format_history(transactions: List[Transaction]) -> str:
    lines = [f"{t.item_id}\t{t.delta:+d}\t{t.reason}" for t in transactions]
    return "\n".join(lines)


def total_value(items: List[Item]) -> float:
    return round(sum(item.total_value for item in items), 2)


def _sorted(items: List[Item]) -> List[Item]:
    return sorted(items, key=lambda i: i.id)
