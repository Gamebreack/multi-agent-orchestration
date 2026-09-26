import tempfile
import unittest
from pathlib import Path

from inventory import storage
from inventory.models import Item


class StorageTest(unittest.TestCase):
    def setUp(self):
        storage.reset()

    def test_add_and_get(self):
        item = Item(id="a1", name="Widget", quantity=3, price=2.5)
        storage.add_item(item)
        self.assertEqual(storage.get_item("a1"), item)

    def test_get_missing_returns_none(self):
        self.assertIsNone(storage.get_item("missing"))

    def test_remove(self):
        storage.add_item(Item(id="a1", name="Widget", quantity=3, price=2.5))
        storage.remove_item("a1")
        self.assertIsNone(storage.get_item("a1"))

    def test_remove_missing_is_noop(self):
        storage.remove_item("missing")

    def test_all_items_returns_every_item(self):
        storage.add_item(Item(id="a1", name="Widget", quantity=1, price=1.0))
        storage.add_item(Item(id="a2", name="Gadget", quantity=2, price=2.0))
        self.assertEqual({i.id for i in storage.all_items()}, {"a1", "a2"})

    def test_save_and_load_round_trip(self):
        storage.add_item(Item(id="a1", name="Widget", quantity=3, price=2.5, tags=["red"]))
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "data.json")
            storage.save_items(path)
            storage.reset()
            storage.load_items(path)
            self.assertEqual(storage.get_item("a1").tags, ["red"])


if __name__ == "__main__":
    unittest.main()
