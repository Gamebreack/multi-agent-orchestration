import unittest

from inventory.cli import run
from inventory.storage import Storage


class CliTest(unittest.TestCase):
    def setUp(self):
        self.storage = Storage()

    def test_add_command(self):
        out = run(["add", "a1", "Widget", "5", "1.5"], self.storage)
        self.assertEqual(out, "added a1")
        self.assertEqual(self.storage.get("a1").quantity, 5)

    def test_adjust_command(self):
        run(["add", "a1", "Widget", "5", "1.5"], self.storage)
        out = run(["adjust", "a1", "-2"], self.storage)
        self.assertEqual(out, "balance a1 = 3")

    def test_report_text_command(self):
        run(["add", "a1", "Widget", "5", "1.5"], self.storage)
        out = run(["report", "--format", "text"], self.storage)
        self.assertIn("a1", out)

    def test_report_csv_command(self):
        run(["add", "a1", "Widget", "5", "1.5"], self.storage)
        out = run(["report", "--format", "csv"], self.storage)
        self.assertTrue(out.startswith("id,name,quantity,price"))


if __name__ == "__main__":
    unittest.main()
