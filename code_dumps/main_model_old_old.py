import asyncio
import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core import settings
from app.models import Article, Comment, User
from app.services import create, get

logger = logging.getLogger(__name__)


async def main() -> None:
    client: AsyncIOMotorClient = settings.client
    database = client[settings.database_name]
    collections = [User, Article, Comment]

    await init_beanie(database=database, document_models=collections)

    result = await get(
        limit=10,
        page=1,
    )

    logger.warn(result.model_dump())
    user_data = {
        "username": "alex_desssveloper",
        "email": "alexs.dev@examples.com",
        "age": 22,
        "bio": "CS student and aspiring full-stack developer. Currently learning MongoDB and FastAPI.",
    }

    result = await create(obj_in=user_data)

    logger.warning(result)
    users_data = [
        {
            "username": "johnsssdoe",
            "email": "johns.doadfase@exampasfdales.com",
            "age": 28,
            "bio": "Software developer and open source contributor. I love building web applications and learning new technologies.",
        },
        {
            "username": "sarahsmitsssh",
            "email": "sarah.smsdsdafith@exffample.com",
            "age": 34,
            "bio": "Data scientist with a passion for machine learning and AI. Coffee enthusiast and amateur photographer.",
        },
    ]

    result = await create(obj_in=users_data)

    logger.warning(result)

    settings.close_client()


if __name__ == "__main__":
    asyncio.run(main())
