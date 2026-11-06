from ..domain.models import Item, ItemId
from ..domain.repository import ItemRepository


class ItemService:
    def __init__(self, repository: ItemRepository) -> None:
        self.repository = repository

    def create(self, name: str, description: str = "") -> Item:
        item = Item(ItemId.new(), name, description)
        self.repository.add(item)
        return item

    def get(self, item_id: ItemId) -> Item:
        return self.repository.get(item_id)

    def list(self, offset: int = 0, limit: int = 100) -> list[Item]:
        if offset < 0 or not 1 <= limit <= 100:
            raise ValueError("Invalid pagination")
        return self.repository.list(offset, limit)

    def update(self, item_id: ItemId, name: str, description: str = "") -> Item:
        item = Item(item_id, name, description)
        self.repository.update(item)
        return item

    def delete(self, item_id: ItemId) -> None:
        self.repository.delete(item_id)
