"""Domain model for inventory items."""
from dataclasses import dataclass, field
from typing import List


@dataclass
class Item:
    id: str
    name: str
    quantity: int
    price: float
    tags: List[str] = field(default_factory=list)

    @property
    def total_value(self) -> float:
        return round(self.quantity * self.price, 2)

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags


@dataclass
class Transaction:
    item_id: str
    delta: int
    reason: str
