"""Validation rules for item data."""

MAX_NAME_LENGTH = 80
MAX_REASON_LENGTH = 200


class ValidationError(Exception):
    """Raised when item data fails validation."""


def validate_item(data: dict) -> None:
    item_id = data.get("id")
    if not item_id or not isinstance(item_id, str):
        raise ValidationError("id is required and must be a string")

    name = data.get("name")
    if not name or not isinstance(name, str):
        raise ValidationError("name is required and must be a string")
    if len(name) > MAX_NAME_LENGTH:
        raise ValidationError(f"name must be at most {MAX_NAME_LENGTH} characters")

    quantity = data.get("quantity")
    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 0:
        raise ValidationError("quantity must be a non-negative integer")

    price = data.get("price")
    if not isinstance(price, (int, float)) or isinstance(price, bool) or price < 0:
        raise ValidationError("price must be a non-negative number")


def validate_reason(reason) -> None:
    if not isinstance(reason, str):
        raise ValidationError("reason must be a string")
    if len(reason) > MAX_REASON_LENGTH:
        raise ValidationError(f"reason must be at most {MAX_REASON_LENGTH} characters")
