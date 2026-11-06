import pytest

from ddd_fastapi.modules.items.application.service import ItemService
from ddd_fastapi.modules.items.domain.models import ItemId, ItemNotFoundError
from ddd_fastapi.modules.items.infrastructure.repository import InMemoryItemRepository


def test_service_crud() -> None:
    service = ItemService(InMemoryItemRepository())
    first = service.create("first")
    second = service.create("second")
    assert service.get(first.id) == first
    assert service.list(1, 1) == [second]
    updated = service.update(first.id, "updated", "description")
    assert service.get(first.id) == updated
    service.delete(first.id)
    with pytest.raises(ItemNotFoundError):
        service.get(first.id)


def test_missing_mutations() -> None:
    service = ItemService(InMemoryItemRepository())
    missing = ItemId.new()
    with pytest.raises(ItemNotFoundError):
        service.update(missing, "name")
    with pytest.raises(ItemNotFoundError):
        service.delete(missing)


@pytest.mark.parametrize("offset,limit", [(-1, 1), (0, 0), (0, 101)])
def test_pagination_validation(offset: int, limit: int) -> None:
    with pytest.raises(ValueError):
        ItemService(InMemoryItemRepository()).list(offset, limit)
