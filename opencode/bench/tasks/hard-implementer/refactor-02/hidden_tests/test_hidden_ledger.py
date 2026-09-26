import tempfile
import unittest
from pathlib import Path

from inventory.ledger import Ledger
from inventory.models import Item
from inventory.storage import Storage
from inventory.validation import ValidationError


class LedgerPersistenceTest(unittest.TestCase):
    def setUp(self):
        self.storage = Storage()
        self.storage.add(Item(id="a1", name="Widget", quantity=5, price=1.0))
        self.ledger = Ledger(self.storage)

    def test_adjust_rejects_overlong_reason(self):
        with self.assertRaises(ValidationError):
            self.ledger.adjust("a1", 1, reason="x" * 201)

    def test_adjust_accepts_reason_at_max_length(self):
        self.ledger.adjust("a1", 1, reason="x" * 200)  # should not raise
        self.assertEqual(self.ledger.balance("a1"), 6)

    def test_transactions_survive_storage_reload(self):
        self.ledger.adjust("a1", 3, reason="restock")
        self.ledger.adjust("a1", -1, reason="sale")
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "data.json")
            self.storage.save(path)
            reloaded_storage = Storage()
            reloaded_storage.load(path)
            reloaded_ledger = Ledger(reloaded_storage)
            self.assertEqual(len(reloaded_ledger.transactions_for("a1")), 2)


if __name__ == "__main__":
    unittest.main()
