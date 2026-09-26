import json
import tempfile
import unittest
from pathlib import Path

from inventory.models import Transaction
from inventory.storage import Storage


class StorageTransactionsTest(unittest.TestCase):
    def test_record_and_query_transactions(self):
        storage = Storage()
        storage.record_transaction(Transaction(item_id="a1", delta=3, reason="restock"))
        storage.record_transaction(Transaction(item_id="a2", delta=-1, reason="sale"))
        storage.record_transaction(Transaction(item_id="a1", delta=-2, reason="sale"))
        self.assertEqual(len(storage.transactions_for("a1")), 2)
        self.assertEqual(len(storage.transactions_for("a2")), 1)
        self.assertEqual(len(storage.all_transactions()), 3)

    def test_save_and_load_round_trips_transactions(self):
        storage = Storage()
        storage.record_transaction(Transaction(item_id="a1", delta=3, reason="restock"))
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "data.json")
            storage.save(path)
            loaded = Storage()
            loaded.load(path)
            txns = loaded.transactions_for("a1")
            self.assertEqual(len(txns), 1)
            self.assertEqual(txns[0].delta, 3)
            self.assertEqual(txns[0].reason, "restock")

    def test_load_old_format_file_without_transactions_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "data.json")
            payload = {"version": 1, "items": []}  # pre-existing file, no "transactions" key
            Path(path).write_text(json.dumps(payload))
            loaded = Storage()
            loaded.load(path)  # must not raise
            self.assertEqual(loaded.all_transactions(), [])


if __name__ == "__main__":
    unittest.main()
