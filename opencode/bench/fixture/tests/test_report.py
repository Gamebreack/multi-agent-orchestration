import unittest

from inventory.models import Item
from inventory.report import format_csv, format_text, total_value


class ReportTest(unittest.TestCase):
    def setUp(self):
        self.items = [
            Item(id="b1", name="Bolt", quantity=10, price=0.5),
            Item(id="a1", name="Anvil", quantity=1, price=100.0),
        ]

    def test_format_text_sorted_by_id(self):
        text = format_text(self.items)
        lines = text.splitlines()
        self.assertTrue(lines[0].startswith("a1"))
        self.assertTrue(lines[1].startswith("b1"))

    def test_format_csv_header_and_rows(self):
        csv_text = format_csv(self.items)
        lines = csv_text.splitlines()
        self.assertEqual(lines[0], "id,name,quantity,price")
        self.assertEqual(len(lines), 3)

    def test_total_value(self):
        self.assertEqual(total_value(self.items), 105.0)


if __name__ == "__main__":
    unittest.main()
