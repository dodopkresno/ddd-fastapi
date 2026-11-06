from typing import Annotated, cast
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import BaseModel, Field

from ..application.service import ItemService
from ..domain.models import Item, ItemId
from ..domain.repository import ItemRepository

router = APIRouter(prefix="/api/v1/items", tags=["items"])


class ItemInput(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)


class ItemOutput(ItemInput):
    id: UUID

    @classmethod
    def from_item(cls, item: Item) -> "ItemOutput":
        return cls(id=item.id.value, name=item.name, description=item.description)


def get_service(request: Request) -> ItemService:
    return ItemService(cast(ItemRepository, request.app.state.item_repository))


Service = Annotated[ItemService, Depends(get_service)]


@router.post("", status_code=status.HTTP_201_CREATED)
def create_item(body: ItemInput, service: Service, response: Response) -> ItemOutput:
    item = service.create(body.name, body.description)
    response.headers["Location"] = f"/api/v1/items/{item.id.value}"
    return ItemOutput.from_item(item)


@router.get("")
def list_items(
    service: Service,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[ItemOutput]:
    return [ItemOutput.from_item(item) for item in service.list(offset, limit)]


@router.get("/{item_id}")
def get_item(item_id: UUID, service: Service) -> ItemOutput:
    return ItemOutput.from_item(service.get(ItemId(item_id)))


@router.put("/{item_id}")
def update_item(item_id: UUID, body: ItemInput, service: Service) -> ItemOutput:
    return ItemOutput.from_item(service.update(ItemId(item_id), body.name, body.description))


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: UUID, service: Service) -> Response:
    service.delete(ItemId(item_id))
    return Response(status_code=204)
