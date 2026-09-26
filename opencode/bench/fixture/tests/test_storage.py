import json
import tempfile
import unittest
from pathlib import Path

from inventory.models import Item
from inventory.storage import Storage


class StorageTest(unittest.TestCase):
    def setUp(self):
        self.storage = Storage()

    def test_add_and_get(self):
        item = Item(id="a1", name="Widget", quantity=3, price=2.5)
        self.storage.add(item)
        self.assertEqual(self.storage.get("a1"), item)

    def test_get_missing_returns_none(self):
        self.assertIsNone(self.storage.get("missing"))

    def test_remove(self):
        self.storage.add(Item(id="a1", name="Widget", quantity=3, price=2.5))
        self.storage.remove("a1")
        self.assertIsNone(self.storage.get("a1"))

    def test_remove_missing_is_noop(self):
        self.storage.remove("missing")  # should not raise

    def test_all_returns_every_item(self):
        self.storage.add(Item(id="a1", name="Widget", quantity=1, price=1.0))
        self.storage.add(Item(id="a2", name="Gadget", quantity=2, price=2.0))
        self.assertEqual({i.id for i in self.storage.all()}, {"a1", "a2"})

    def test_save_and_load_round_trip(self):
        self.storage.add(Item(id="a1", name="Widget", quantity=3, price=2.5, tags=["red"]))
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "data.json")
            self.storage.save(path)
            loaded = Storage()
            loaded.load(path)
            self.assertEqual(loaded.get("a1"), self.storage.get("a1"))

    def test_load_defaults_missing_tags_to_empty_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "data.json")
            payload = {
                "version": 1,
                "items": [{"id": "a1", "name": "Widget", "quantity": 1, "price": 1.0}],
            }
            Path(path).write_text(json.dumps(payload))
            loaded = Storage()
            loaded.load(path)
            self.assertEqual(loaded.get("a1").tags, [])


if __name__ == "__main__":
    unittest.main()
