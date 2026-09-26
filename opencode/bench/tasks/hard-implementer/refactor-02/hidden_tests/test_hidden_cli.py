import unittest

from inventory.cli import run
from inventory.storage import Storage


class CliHistoryTest(unittest.TestCase):
    def setUp(self):
        self.storage = Storage()

    def test_history_lists_past_adjustments(self):
        run(["add", "a1", "Widget", "5", "1.5"], self.storage)
        run(["adjust", "a1", "3", "--reason", "restock"], self.storage)
        run(["adjust", "a1", "-1", "--reason", "sale"], self.storage)
        out = run(["history", "a1"], self.storage)
        self.assertEqual(out.splitlines(), ["a1\t+3\trestock", "a1\t-1\tsale"])

    def test_history_of_unknown_item_is_empty_not_an_error(self):
        out = run(["history", "missing"], self.storage)
        self.assertEqual(out, "")


if __name__ == "__main__":
    unittest.main()
