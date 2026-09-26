import unittest

from inventory.validation import ValidationError, validate_item


class ValidateItemTest(unittest.TestCase):
    def test_valid_item_passes(self):
        validate_item({"id": "a1", "name": "Widget", "quantity": 5, "price": 1.5})

    def test_missing_id_rejected(self):
        with self.assertRaises(ValidationError):
            validate_item({"name": "Widget", "quantity": 5, "price": 1.5})

    def test_missing_name_rejected(self):
        with self.assertRaises(ValidationError):
            validate_item({"id": "a1", "quantity": 5, "price": 1.5})

    def test_negative_quantity_rejected(self):
        with self.assertRaises(ValidationError):
            validate_item({"id": "a1", "name": "Widget", "quantity": -1, "price": 1.5})

    def test_non_integer_quantity_rejected(self):
        with self.assertRaises(ValidationError):
            validate_item({"id": "a1", "name": "Widget", "quantity": 1.5, "price": 1.5})

    def test_negative_price_rejected(self):
        with self.assertRaises(ValidationError):
            validate_item({"id": "a1", "name": "Widget", "quantity": 1, "price": -1})

    def test_name_too_long_rejected(self):
        with self.assertRaises(ValidationError):
            validate_item({"id": "a1", "name": "x" * 81, "quantity": 1, "price": 1})

    def test_zero_quantity_allowed(self):
        validate_item({"id": "a1", "name": "Widget", "quantity": 0, "price": 1.5})


if __name__ == "__main__":
    unittest.main()
