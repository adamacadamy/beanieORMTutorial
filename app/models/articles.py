from datetime import UTC, datetime
from enum import Enum
from typing import TYPE_CHECKING, ClassVar

from beanie import BackLink, Document, Insert, Link, Update, before_event
from pydantic import Field, field_validator

if TYPE_CHECKING:
    from .comments import Comment
    from .users import User


class ArticleStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Article(Document):
    title: str = Field(..., min_length=1, max_length=200)
    author: Link["User"]
    content: str = Field(..., min_length=1)
    tags: list[str] = Field(default_factory=list, max_length=10)
    summary: str | None = Field(None, max_digits=300, description="Article Summary")
    status: ArticleStatus = ArticleStatus.DRAFT
    published_at: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None
    comments: BackLink["Comment"] = Field(original_field="articles")
    view_count: int = Field(default=0, ge=0)

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: list[str]) -> list[str]:
        if v:
            cleaned_tags = list({tag.strip().lower() for tag in v if tag.strip()})
            return cleaned_tags[:10]
        return v

    @before_event([Insert, Update])
    async def update(self) -> None:
        self.updated_at = datetime.now(tz=UTC)

        if self.status == ArticleStatus.PUBLISHED and not self.published_at:
            self.published_at = datetime.now(tz=UTC)

    def is_published(self) -> bool:
        return self.status == ArticleStatus.PUBLISHED

    def increment_view_count(self) -> None:
        self.view_count += 1

    class Settings:
        name = "articles"
        indexes: ClassVar[list] = [
            "author",
            "status",
            "created_at",
            "published_at",
            [("author", 1), ("status", -1)],
            [("status", 1), ("published_at", -1)],
            [("title", "text"), ("content", "text")],
        ]
