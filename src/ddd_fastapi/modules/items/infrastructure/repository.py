from threading import Lock

from ..domain.models import Item, ItemId, ItemNotFoundError


class InMemoryItemRepository:
    """One instance per application; immutable entities and locked atomic operations."""

    def __init__(self) -> None:
        self._items: dict[ItemId, Item] = {}
        self._lock = Lock()

    def add(self, item: Item) -> None:
        with self._lock:
            if item.id in self._items:
                raise ValueError("Item ID already exists")
            self._items[item.id] = item

    def get(self, item_id: ItemId) -> Item:
        with self._lock:
            return self._get(item_id)

    def _get(self, item_id: ItemId) -> Item:
        try:
            return self._items[item_id]
        except KeyError:
            raise ItemNotFoundError("Item not found") from None

    def list(self, offset: int, limit: int) -> list[Item]:
        with self._lock:
            return list(self._items.values())[offset : offset + limit]

    def update(self, item: Item) -> None:
        with self._lock:
            self._get(item.id)
            self._items[item.id] = item

    def delete(self, item_id: ItemId) -> None:
        with self._lock:
            self._get(item_id)
            del self._items[item_id]
