from beanie import PydanticObjectId

from app.models import User
from app.schemas import PaginationResponse


async def get(
    page: int = 1, limit: int = 10, filters: dict[str, any] | None = None
) -> PaginationResponse[User]:
    """
    1 - 10 = page 1
    11 - 20 = page 2
    21 - 30 = page 3

    total pages = 30 page = 1, limit = 10

    offset = 1
    end = 10

    total pages = 30 page = 2, limit = 10

    offset = (page - 1) * limit = 1 * 10 = 10
    end = skip + limit = 10 + 10 = 20

    """
    filters = filters or {}
    skip = (page - 1) * limit

    query = User.find(filters)
    total = await query.count()
    items = await query.skip(skip).limit(limit).to_list()

    response = PaginationResponse(items=items, page=page, limit=limit, total=total)

    return response


async def create(
    obj_in: dict[str, any] | list[dict[str, any]],
) -> User | list[User] | None:
    if isinstance(obj_in, dict):
        user = User(**obj_in)

        return await user.insert()

        return user
    if isinstance(obj_in, list):
        users = [User(**item) for item in obj_in]

        return await User.insert_many(users)

    return None


async def update(
    item_id: str | PydanticObjectId = None,
    filters: dict[str, any] = None,
    update_data: dict[str, any] | None = None,
    update_method: str | None = None,
): ...


async def delete(
    update_data: dict[str, any],
    item_id: str | PydanticObjectId = None,
    filters: dict[str, any] = None,
): ...
