import unittest

from inventory import storage
from inventory.ledger import Ledger
from inventory.models import Item
from inventory.validation import ValidationError


class LedgerTest(unittest.TestCase):
    def setUp(self):
        storage.reset()
        storage.add_item(Item(id="a1", name="Widget", quantity=5, price=1.0))
        self.ledger = Ledger()

    def test_adjust_increases_balance(self):
        self.ledger.adjust("a1", 3, reason="restock")
        self.assertEqual(self.ledger.balance("a1"), 8)

    def test_adjust_decreases_balance(self):
        self.ledger.adjust("a1", -2, reason="sale")
        self.assertEqual(self.ledger.balance("a1"), 3)

    def test_adjust_below_zero_rejected(self):
        with self.assertRaises(ValidationError):
            self.ledger.adjust("a1", -6, reason="sale")

    def test_adjust_unknown_item_rejected(self):
        with self.assertRaises(ValidationError):
            self.ledger.adjust("missing", 1)

    def test_balance_unknown_item_is_zero(self):
        self.assertEqual(self.ledger.balance("missing"), 0)


if __name__ == "__main__":
    unittest.main()
