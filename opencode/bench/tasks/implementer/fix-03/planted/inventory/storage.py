"""Persistence layer for inventory items."""
import json
from dataclasses import replace
from pathlib import Path
from typing import Dict, List, Optional

from .models import Item

STORAGE_VERSION = 1


class Storage:
    """In-memory item store with optional JSON file persistence."""

    def __init__(self) -> None:
        self._items: Dict[str, Item] = {}

    def add(self, item: Item) -> None:
        self._items[item.id] = item

    def get(self, item_id: str) -> Optional[Item]:
        # Return a defensive copy so a caller can't corrupt our internal
        # state by mutating an object it got back from a previous call.
        item = self._items.get(item_id)
        return replace(item) if item is not None else None

    def remove(self, item_id: str) -> None:
        self._items.pop(item_id, None)

    def all(self) -> List[Item]:
        return list(self._items.values())

    def save(self, path: str) -> None:
        data = {
            "version": STORAGE_VERSION,
            "items": [item.__dict__ for item in self._items.values()],
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
