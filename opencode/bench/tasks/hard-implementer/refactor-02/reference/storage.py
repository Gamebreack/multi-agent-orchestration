"""Persistence layer for inventory items."""
import json
from pathlib import Path
from typing import Dict, List, Optional

from .models import Item, Transaction

STORAGE_VERSION = 1


class Storage:
    """In-memory item store with optional JSON file persistence."""

    def __init__(self) -> None:
        self._items: Dict[str, Item] = {}
        self._transactions: List[Transaction] = []

    def add(self, item: Item) -> None:
        self._items[item.id] = item

    def get(self, item_id: str) -> Optional[Item]:
        return self._items.get(item_id)

    def remove(self, item_id: str) -> None:
        self._items.pop(item_id, None)

    def all(self) -> List[Item]:
        return list(self._items.values())

    def record_transaction(self, txn: Transaction) -> None:
        self._transactions.append(txn)

    def transactions_for(self, item_id: str) -> List[Transaction]:
        return [t for t in self._transactions if t.item_id == item_id]

    def all_transactions(self) -> List[Transaction]:
        return list(self._transactions)

    def save(self, path: str) -> None:
        data = {
            "version": STORAGE_VERSION,
            "items": [item.__dict__ for item in self._items.values()],
            "transactions": [t.__dict__ for t in self._transactions],
        }
        Path(path).write_text(json.dumps(data, indent=2))

    def load(self, path: str) -> None:
        payload = json.loads(Path(path).read_text())
        items: Dict[str, Item] = {}
        for record in payload.get("items", []):
            items[record["id"]] = Item(
                id=record["id"],
                name=record["name"],
                quantity=record["quantity"],
                price=record["price"],
                tags=record.get("tags", []),
            )
        self._items = items
        # "transactions" is absent in files saved before this feature existed.
        self._transactions = [
            Transaction(item_id=r["item_id"], delta=r["delta"], reason=r["reason"])
            for r in payload.get("transactions", [])
        ]
