"""Stock transaction ledger built on top of a Storage."""
from dataclasses import dataclass
from typing import List

from .storage import Storage
from .validation import ValidationError


@dataclass
class Transaction:
    item_id: str
    delta: int
    reason: str


class Ledger:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage
        self.history: List[Transaction] = []

    def adjust(self, item_id: str, delta: int, reason: str = "") -> None:
        item = self.storage.get(item_id)
        if item is None:
            raise ValidationError(f"unknown item: {item_id}")
        new_quantity = item.quantity + delta
        if new_quantity < 0:
            raise ValidationError("insufficient stock")
        item.quantity = new_quantity
        self.history.append(Transaction(item_id, delta, reason))

    def balance(self, item_id: str) -> int:
        item = self.storage.get(item_id)
        return item.quantity if item is not None else 0

    def transactions_for(self, item_id: str) -> List[Transaction]:
        return [t for t in self.history if t.item_id == item_id]
