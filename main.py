import asyncio
import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core import settings
from app.models import Article, Comment, User

logger = logging.getLogger(__name__)


async def main() -> None:
    client: AsyncIOMotorClient = settings.client

    database = client[settings.database_name]

    await init_beanie(database=database, document_models=[User, Article, Comment])

    logger.info(f"Connected to MongoDb at: {settings.mongodb_url}")
    logger.info(f"Using database: {settings.database_name}")

    settings.close_client()


if __name__ == "__main__":
    asyncio.run(main())
