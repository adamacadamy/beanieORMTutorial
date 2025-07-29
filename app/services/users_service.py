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
) -> bool:
    if update_method:
        user = await User.find_one(id=item_id)
        if user:
            """
            func
             ||
            @before_event([Insert, Update])
            async def update_timestamp(self):
                self.updated_at = datetime.now(tz=UTC)

            """
            # getattr(user, update_method)()
            # user.update_method()
            func = getattr(user, update_method)
            await func()
            result = user
    if update_data:
        result = await User.find_one(id=item_id).update(
            {"$set": update_data},
        )

    if filters:
        result = await User.find_many(filters).update_many(
            {"$set": update_data},
        )

        return bool(result)


async def delete(
    update_data: dict[str, any],
    item_id: str | PydanticObjectId = None,
    filters: dict[str, any] = None,
):
    if item_id:
        result = await User.find_one(id=item_id).delete()

    if filters:
        result = await User.find_many(filters).delete_many()

    return bool(result)
