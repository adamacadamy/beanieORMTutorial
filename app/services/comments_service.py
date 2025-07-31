from beanie import PydanticObjectId

from app.models import Comment
from app.schemas import PaginationResponse
from app.services import base_crud_services


async def get(
    page: int = 1, limit: int = 10, filters: dict[str, any] | None = None
) -> PaginationResponse[Comment]:
    return await base_crud_services.get(Comment, page, limit, filters)


async def create(
    obj_in: dict[str, any] | list[dict[str, any]],
) -> Comment | list[Comment] | None:
    return await base_crud_services.create(Comment, obj_in)


async def update(
    item_id: str | PydanticObjectId = None,
    filters: dict[str, any] = None,
    update_data: dict[str, any] | None = None,
    update_method: str | None = None,
) -> bool:
    return await base_crud_services.update(
        Comment, item_id, filters, update_data, update_method
    )


async def delete(
    item_id: str | PydanticObjectId = None,
    filters: dict[str, any] = None,
) -> bool:
    return await base_crud_services.delete(Comment, item_id, filters)


# implement class based generic service that inherits from the base class curd service
class CommentCrudService(base_crud_services.BaseCrudService):
    def __init__(self):
        super().__init__(model=Comment)
