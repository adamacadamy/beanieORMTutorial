from pathlib import Path

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_user: str = Field(
        default="root", description="MongoDB username", alias="MONGODB_USER"
    )
    mongo_password: str = Field(
        default="example", description="MongoDB password", alias="MONGO_PASSWORD"
    )
    mongodb_host: str = Field(
        default="localhost", description="MongoDB host", alias="MONGODB_HOST"
    )
    mongodb_port: int = Field(
        default=27017, description="MongoDB port", alias="MONGODB_PORT"
    )
    database_name: str = Field(
        default="mydb", description="Database name", alias="DATABASE_NAME"
    )

    _client: AsyncIOMotorClient | None = None

    class Config:
        env_file = Path(__file__).parent.parent.parent / ".env"
        case_sensitive = (False,)
        extra = "allow"

    @computed_field
    @property
    def mongodb_url(self) -> str:
        return f"mongodb://{self.mongodb_user}:{self.mongo_password}@{self.mongodb_host}:{self.mongodb_port}/{self.database_name}?authSource=admin"

    @property
    def client(self) -> AsyncIOMotorClient:
        if self._client is None:
            self._client = AsyncIOMotorClient(self.mongodb_url)
        return self._client

    def close_client(self) -> None:
        if self._client:
            self._client.close()
            self._client = None


# Global client instance
settings = Settings()
