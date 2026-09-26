import unittest

from inventory.models import Item


class ItemTest(unittest.TestCase):
    def test_total_value(self):
        item = Item(id="a1", name="Widget", quantity=3, price=2.5)
        self.assertEqual(item.total_value, 7.5)

    def test_has_tag(self):
        item = Item(id="a1", name="Widget", quantity=1, price=1.0, tags=["red"])
        self.assertTrue(item.has_tag("red"))
        self.assertFalse(item.has_tag("blue"))

    def test_default_tags_empty(self):
        item = Item(id="a1", name="Widget", quantity=1, price=1.0)
        self.assertEqual(item.tags, [])


if __name__ == "__main__":
    unittest.main()
