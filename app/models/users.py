from datetime import UTC, datetime
from typing import ClassVar

from beanie import Document, Insert, Update, before_event
from pydantic import EmailStr, Field


class User(Document):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: int | None = Field(None, ge=13, le=120)
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    updated_at: datetime | None = None
    bio: str | None = Field(None, max_length=500)
    is_active: bool = True

    @before_event([Insert, Update])
    async def update_timestamp(self):
        self.updated_at = datetime.now(tz=UTC)

    class Settings:
        name = "users"
        indexes: ClassVar[list] = [
            "email",
            "username",
            [("username", 1), ("email", 1)],
        ]
