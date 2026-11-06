from dataclasses import dataclass
from uuid import UUID, uuid4


class ItemValidationError(ValueError):
    pass


class ItemNotFoundError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class ItemId:
    value: UUID

    @classmethod
    def new(cls) -> "ItemId":
        return cls(uuid4())


@dataclass(frozen=True, slots=True)
class Item:
    id: ItemId
    name: str
    description: str = ""

    def __post_init__(self) -> None:
        name = self.name.strip()
        if not name or len(name) > 200:
            raise ItemValidationError("Name must contain 1 to 200 characters")
        if len(self.description) > 2000:
            raise ItemValidationError("Description must contain at most 2000 characters")
        object.__setattr__(self, "name", name)
