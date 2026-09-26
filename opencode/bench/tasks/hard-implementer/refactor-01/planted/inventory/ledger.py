"""Stock transaction ledger operating on the module-level item store."""
from dataclasses import dataclass
from typing import List

from . import storage
from .validation import ValidationError


@dataclass
class Transaction:
    item_id: str
    delta: int
    reason: str


class Ledger:
    def __init__(self) -> None:
        self.history: List[Transaction] = []

    def adjust(self, item_id: str, delta: int, reason: str = "") -> None:
        item = storage.get_item(item_id)
        if item is None:
            raise ValidationError(f"unknown item: {item_id}")
        new_quantity = item.quantity + delta
        if new_quantity < 0:
            raise ValidationError("insufficient stock")
        item.quantity = new_quantity
        self.history.append(Transaction(item_id, delta, reason))

    def balance(self, item_id: str) -> int:
        item = storage.get_item(item_id)
        return item.quantity if item is not None else 0

    def transactions_for(self, item_id: str) -> List[Transaction]:
        return [t for t in self.history if t.item_id == item_id]
