import unittest

from inventory.ledger import Ledger
from inventory.models import Item
from inventory.storage import Storage
from inventory.validation import ValidationError


class LedgerTest(unittest.TestCase):
    def setUp(self):
        self.storage = Storage()
        self.storage.add(Item(id="a1", name="Widget", quantity=5, price=1.0))
        self.ledger = Ledger(self.storage)

    def test_adjust_increases_balance(self):
        self.ledger.adjust("a1", 3, reason="restock")
        self.assertEqual(self.ledger.balance("a1"), 8)

    def test_adjust_decreases_balance(self):
        self.ledger.adjust("a1", -2, reason="sale")
        self.assertEqual(self.ledger.balance("a1"), 3)

    def test_adjust_to_exactly_zero_allowed(self):
        self.ledger.adjust("a1", -5, reason="sale")
        self.assertEqual(self.ledger.balance("a1"), 0)

    def test_adjust_below_zero_rejected(self):
        with self.assertRaises(ValidationError):
            self.ledger.adjust("a1", -6, reason="sale")

    def test_adjust_unknown_item_rejected(self):
        with self.assertRaises(ValidationError):
            self.ledger.adjust("missing", 1)

    def test_balance_unknown_item_is_zero(self):
        self.assertEqual(self.ledger.balance("missing"), 0)

    def test_transactions_for_filters_by_item(self):
        self.storage.add(Item(id="a2", name="Gadget", quantity=1, price=1.0))
        self.ledger.adjust("a1", 1)
        self.ledger.adjust("a2", 1)
        self.assertEqual(len(self.ledger.transactions_for("a1")), 1)


if __name__ == "__main__":
    unittest.main()
