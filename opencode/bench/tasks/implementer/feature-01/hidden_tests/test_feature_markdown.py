import unittest

from inventory import cli  # noqa: F401  (import triggers formatter registration)
from inventory.models import Item
from inventory.plugins import get_formatter
from inventory.report import format_markdown


class MarkdownReportTest(unittest.TestCase):
    def setUp(self):
        self.items = [
            Item(id="b1", name="Bolt", quantity=10, price=0.5),
            Item(id="a1", name="Anvil", quantity=1, price=100.0),
        ]

    def test_format_markdown_table(self):
        expected = (
            "| id | name | quantity | price |\n"
            "| --- | --- | --- | --- |\n"
            "| a1 | Anvil | 1 | 100.00 |\n"
            "| b1 | Bolt | 10 | 0.50 |"
        )
        self.assertEqual(format_markdown(self.items), expected)

    def test_registered_under_markdown_name(self):
        formatter = get_formatter("markdown")
        self.assertEqual(formatter(self.items), format_markdown(self.items))


if __name__ == "__main__":
    unittest.main()
