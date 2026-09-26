"""Persistence layer for inventory items (ad-hoc dict-based)."""
import json
from pathlib import Path

from .models import Item

STORAGE_VERSION = 1

_ITEMS = {}


def reset():
    _ITEMS.clear()


def add_item(item):
    _ITEMS[item.id] = item


def get_item(item_id):
    return _ITEMS.get(item_id)


def remove_item(item_id):
    _ITEMS.pop(item_id, None)


def all_items():
    return list(_ITEMS.values())


def save_items(path):
    data = {
        "version": STORAGE_VERSION,
        "items": [item.__dict__ for item in _ITEMS.values()],
    }
    Path(path).write_text(json.dumps(data, indent=2))


def load_items(path):
    payload = json.loads(Path(path).read_text())
    _ITEMS.clear()
    for record in payload.get("items", []):
        _ITEMS[record["id"]] = Item(
            id=record["id"],
            name=record["name"],
            quantity=record["quantity"],
            price=record["price"],
            tags=record.get("tags", []),
        )
