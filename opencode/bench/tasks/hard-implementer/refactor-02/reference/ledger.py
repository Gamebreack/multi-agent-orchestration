"""Stock transaction ledger built on top of a Storage."""
from typing import List

from .models import Transaction
from .storage import Storage
from .validation import ValidationError, validate_reason


class Ledger:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def adjust(self, item_id: str, delta: int, reason: str = "") -> None:
        validate_reason(reason)
        item = self.storage.get(item_id)
        if item is None:
            raise ValidationError(f"unknown item: {item_id}")
        new_quantity = item.quantity + delta
        if new_quantity < 0:
            raise ValidationError("insufficient stock")
        item.quantity = new_quantity
        self.storage.record_transaction(Transaction(item_id, delta, reason))

    def balance(self, item_id: str) -> int:
        item = self.storage.get(item_id)
        return item.quantity if item is not None else 0

    def transactions_for(self, item_id: str) -> List[Transaction]:
        return self.storage.transactions_for(item_id)
