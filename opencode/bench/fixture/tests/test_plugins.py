import unittest

from inventory.plugins import available_formatters, get_formatter, register_formatter


class PluginsTest(unittest.TestCase):
    def test_register_and_get(self):
        register_formatter("noop", lambda items: "")
        self.assertIn("noop", available_formatters())
        self.assertTrue(callable(get_formatter("noop")))

    def test_unknown_formatter_raises(self):
        with self.assertRaises(KeyError):
            get_formatter("does-not-exist")


if __name__ == "__main__":
    unittest.main()
