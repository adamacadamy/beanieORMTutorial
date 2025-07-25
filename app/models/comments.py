from datetime import UTC, datetime
from typing import TYPE_CHECKING, ClassVar

from beanie import BackLink, Document, Insert, Link, Update, before_event
from pydantic import Field, field_validator

if TYPE_CHECKING:
    from .articles import Article
    from .comments import Comment
    from .users import User


class Comment(Document):
    article: Link["Article"]
    author: Link["User"]
    content: str = Field(..., min_length=1, max_length=1000)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None
    is_deleted: bool = Field(default=False)
    is_edited: bool = Field(default=False)
    parent_comment: Link["Comment"] | None = Field(
        None, description="Parent comment for replies"
    )
    replies: BackLink["Comment"] = Field(original_field="parent_comment")

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        if v:
            cleaned_content = v.strip()
            if not cleaned_content:
                raise ValueError("Comment content cannot be empty")
            return cleaned_content
        raise ValueError("Comment content is required")

    @before_event([Insert, Update])
    async def update_timestamp(self) -> None:
        now = datetime.now(tz=UTC)

        if self.created_at:
            self.is_edited = True

        self.updated_at = now

    def soft_delete(self) -> None:
        self.is_deleted = True
        self.content = "[This comment has been deleted]"

    def is_reply(self) -> bool:
        return self.parent_comment is not None

    def is_root_comment(self) -> bool:
        return self.parent_comment is None

    class Settings:
        name = "comment"
        indexes: ClassVar[list] = [
            "article",
            "author",
            "created_at",
            "is_deleted",
            "parent_comment",
            [("article", 1), ("created_at", -1)],
            [("article", 1), ("is_deleted", 1)],
            [("parent_comment", 1), ("created_at", 1)],
        ]
