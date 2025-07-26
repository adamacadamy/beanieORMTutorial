import asyncio
import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core import settings
from app.models import Article, Comment, User

logger = logging.getLogger(__name__)


async def drop_collections(db: "AsyncIOMotorClient", collection_names: list[str]):
    try:
        for collection_name in collection_names:
            await db.drop_collection(collection_name)
    except Exception as e:
        print(e)


async def main() -> None:
    client: AsyncIOMotorClient = settings.client

    database = client[settings.database_name]

    collections = [User, Article, Comment]
    collection_names = [collection.Settings.name for collection in collections]

    await drop_collections(db=database, collection_names=collection_names)
    await init_beanie(database=database, document_models=collections)

    logger.info(f"Connected to MongoDb at: {settings.mongodb_url}")
    logger.info(f"Using database: {settings.database_name}")

    # user =  User(
    #     username="devops_ninja",
    #     email="devops.ninja@example.com",
    #     age=29,
    #     bio="DevOps engineer specializing in CI/CD pipelines and infrastructure as code.",
    # )
    """
    user_data = {
        "username": "devops_ninja",
        "email": "devops.ninja@example.com",
        "age": 29,
        "bio": "DevOps engineer specializing in CI/CD pipelines and infrastructure as code.",
    }
    
    **user_data = (username="devops_ninja",
         email="devops.ninja@example.com",
         age=29,
         bio="DevOps engineer specializing in CI/CD pipelines and infrastructure as code.")

    """
    user_data = {
        "username": "devops_ninja",
        "email": "devops.ninja@example.com",
        "age": 34,
        "bio": "DevOps engineer specializing in CI/CD pipelines and infrastructure as code.",
    }
    another_user_data = {
        "username": "sarahsmith",
        "email": "sarah.smith@example.com",
        "age": 34,
        "bio": "Data scientist with a passion for machine learning and AI. Coffee enthusiast and amateur photographer.",
    }

    user = User(**user_data)

    await user.insert()

    another_user = User(**another_user_data)

    await another_user.insert()
    # user_to_update = await User.get(document_id="68851aa94cd5102a5d80348a")
    # user_to_update = await User.find({"username": "devops_ninja"}).to_list()
    # user_to_update = await User.find_one({"email": "devops.ninja@example.com"}).update(
    #     {
    #         "$set": {
    #             "age": 30,
    #         }
    #     }
    # )
    user_to_update = await User.find_many({"age": 34}).update(
        {
            "$set": {
                "age": 30,
            }
        }
    )
    print(user_to_update)

    users_data = [
        {
            "username": "alex_developer",
            "email": "alex.dev@example.com",
            "age": 22,
            "bio": "CS student and aspiring full-stack developer. Currently learning MongoDB and FastAPI.",
        },
        {
            "username": "tech_enthusiast",
            "email": "tech.fan@example.com",
            "age": 45,
            "bio": "Technology enthusiast and blogger. I write about the latest trends in software development.",
        },
    ]

    users = [User(**user_data) for user_data in users_data]

    result = await User.insert_many(users)

    print(result)

    result = await User.find_one({"email": "devops.ninja@example.com"}).delete()

    print(result)

    result = await User.find_many({"age": 34}).delete_many()

    print(result)

    # CREATE  insert, insert_many
    # READ    find, get, find_one, find_many
    # UPDATE - update, update_many
    # DELETE - delete, delete_many

    settings.close_client()


if __name__ == "__main__":
    asyncio.run(main())
