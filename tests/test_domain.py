from dataclasses import FrozenInstanceError
from uuid import UUID

import pytest

from ddd_fastapi.modules.items.domain.models import Item, ItemId, ItemValidationError


@pytest.mark.parametrize("name", ["", "   ", "x" * 201])
def test_invalid_name(name: str) -> None:
    with pytest.raises(ItemValidationError):
        Item(ItemId.new(), name)


def test_description_limit() -> None:
    with pytest.raises(ItemValidationError):
        Item(ItemId.new(), "name", "x" * 2001)


def test_item_normalization_and_value_identity() -> None:
    item_id = ItemId(UUID(int=1))
    assert item_id == ItemId(UUID(int=1))
    item = Item(item_id, "  name  ")
    assert item.name == "name"
    with pytest.raises(FrozenInstanceError):
        item.name = "changed"  # pyright: ignore[reportAttributeAccessIssue]
