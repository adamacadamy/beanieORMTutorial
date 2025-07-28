from typing import Generic, TypeVar

from beanie import Document
from pydantic import BaseModel, ConfigDict, Field

DBModelType = TypeVar("DBModelType", bound=Document)


class PaginationResponse(BaseModel, Generic[DBModelType]):
    items: list[DBModelType]
    total: int = Field(description="Total number of items across all pages")
    page: int = Field(description="Current page number (1-based)")
    limit: int = Field(description="Maximum items per page")
    model_config = ConfigDict(arbitrary_types_allowed=True)


""" 
PaginationResponse[User]


class PaginationResponseUser(BaseModel):
    items: list[User]
    total: int = Field(description="Total number of items across all pages")
    page: int = Field(description="Current page number (1-based)")
    limit: int = Field(description="Maximum items per page")
    pages: int = Field(description="Total number of pages")
    has_more: bool = Field(description="Whether there are more pages available")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class PaginationResponseComment(BaseModel):
    items: list[Comment]
    total: int = Field(description="Total number of items across all pages")
    page: int = Field(description="Current page number (1-based)")
    limit: int = Field(description="Maximum items per page")
    pages: int = Field(description="Total number of pages")
    has_more: bool = Field(description="Whether there are more pages available")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class PaginationResponseArticle(BaseModel):
    items: list[Article]
    total: int = Field(description="Total number of items across all pages")
    page: int = Field(description="Current page number (1-based)")
    limit: int = Field(description="Maximum items per page")
    pages: int = Field(description="Total number of pages")
    has_more: bool = Field(description="Whether there are more pages available")

    model_config = ConfigDict(arbitrary_types_allowed=True)
"""
