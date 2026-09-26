import unittest

from inventory import storage
from inventory.cli import run


class CliTest(unittest.TestCase):
    def setUp(self):
        storage.reset()

    def test_add_command(self):
        out = run(["add", "a1", "Widget", "5", "1.5"])
        self.assertEqual(out, "added a1")
        self.assertEqual(storage.get_item("a1").quantity, 5)

    def test_adjust_command(self):
        run(["add", "a1", "Widget", "5", "1.5"])
        out = run(["adjust", "a1", "-2"])
        self.assertEqual(out, "balance a1 = 3")

    def test_report_csv_command(self):
        run(["add", "a1", "Widget", "5", "1.5"])
        out = run(["report", "--format", "csv"])
        self.assertTrue(out.startswith("id,name,quantity,price"))


if __name__ == "__main__":
    unittest.main()
