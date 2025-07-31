from beanie import PydanticObjectId

from app.models import Article
from app.schemas import PaginationResponse
from app.services import base_crud_services


async def get(
    page: int = 1, limit: int = 10, filters: dict[str, any] | None = None
) -> PaginationResponse[Article]:
    return await base_crud_services.get(Article, page, limit, filters)


async def create(
    obj_in: dict[str, any] | list[dict[str, any]],
) -> Article | list[Article] | None:
    return await base_crud_services.create(Article, obj_in)


async def update(
    item_id: str | PydanticObjectId = None,
    filters: dict[str, any] = None,
    update_data: dict[str, any] | None = None,
    update_method: str | None = None,
) -> bool:
    return await base_crud_services.update(
        Article, item_id, filters, update_data, update_method
    )


async def delete(
    item_id: str | PydanticObjectId = None,
    filters: dict[str, any] = None,
) -> bool:
    return await base_crud_services.delete(Article, item_id, filters)


# implement class based generic service that inherits from the base class curd service
class ArticleCrudService(base_crud_services.BaseCrudService):
    def __init__(self):
        super().__init__(model=Article)
