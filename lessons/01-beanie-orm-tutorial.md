## Beanie ORM: A Comprehensive Tutorial

This tutorial will guide you through everything you need to know to start using **Beanie**, an asynchronous Object-Document Mapper (ODM) for MongoDB built on top of Motor and Pydantic. We’ll cover setup, model definitions, CRUD operations (with expanded examples), advanced queries, projections, text search, in---

### 10. Migrations Command Cheat Sheeting strategies, migrations, transactions, and best practices.

---

### 1. Prerequisites

* **Python 3.10+**
* **MongoDB** instance (local or Atlas)
* **Motor** async MongoDB driver
* **Pydantic** for data validation

Ensure MongoDB is running and reachable.

---

### 2. Installation

```bash
pip install beanie  motor pydantic
```

---

### 3. Defining Document Models

```python
from beanie import Document, Link, BackLink, before_event, after_event, Insert, Update
from pydantic import Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

class User(Document):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: UserRole = UserRole.USER
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    bio: Optional[str] = Field(None, max_length=500)
    is_active: bool = True
    
    # BackLink to related documents
    articles: BackLink["Article"] = Field(original_field="author")
    comments: BackLink["Comment"] = Field(original_field="author")

    @before_event([Insert, Update])
    async def update_timestamp(self):
        self.updated_at = datetime.utcnow()

    class Settings:
        name = "users"
        indexes = [
            "email",
            "username", 
            {"fields": ["username", "email"], "unique": True}
        ]

class ArticleStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class Article(Document):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    summary: Optional[str] = Field(None, max_length=300)
    author: Link[User]
    tags: List[str] = []
    status: ArticleStatus = ArticleStatus.DRAFT
    published_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    view_count: int = 0
    
    # BackLink to comments
    comments: BackLink["Comment"] = Field(original_field="article")

    @before_event([Insert, Update])
    async def update_timestamp(self):
        self.updated_at = datetime.utcnow()
        if self.status == ArticleStatus.PUBLISHED and not self.published_at:
            self.published_at = datetime.utcnow()

    class Settings:
        name = "articles"
        indexes = [
            "author",
            "status",
            "created_at",
            {"fields": [("author", 1), ("status", -1)]},  # compound
            {"fields": ["title", "content"], "type": "text"}  # text search
        ]

class Comment(Document):
    article: Link[Article]
    author: Link[User]
    content: str = Field(..., min_length=1, max_length=1000)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    is_deleted: bool = False
    parent_comment: Optional[Link["Comment"]] = None  # For nested comments
    
    # BackLink for replies
    replies: BackLink["Comment"] = Field(original_field="parent_comment")

    @before_event([Insert, Update])
    async def update_timestamp(self):
        self.updated_at = datetime.now()

    class Settings:
        name = "comments"
        indexes = [
            "article",
            "author", 
            "created_at",
            {"fields": [("article", 1), ("created_at", -1)]}
        ]
```

---

### 4. Initializing Beanie

```python
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import asyncio

async def init_db():
    # Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://username:password@localhost:27017/mydb")
    database = client.mydb
    
    # Import document classes
    from app.models.users import User
    from app.models.articles import Article
    from app.models.comments import Comment
    
    # Initialize Beanie
    await init_beanie(
        database=database,
        document_models=[User, Article, Comment]
    )
    
    print("Database initialized successfully!")

# Example main function
async def main():
    await init_db()
    # Your application logic here

if __name__ == "__main__":
    asyncio.run(main())
```

Call `init_db()` at application startup.

---

### 5. Basic CRUD Operations (Expanded)

#### Create

```python
# Single insert
user = User(username="alice", email="alice@example.com", bio="Python developer")
await user.insert()
print(f"Created user with ID: {user.id}")

# Insert with validation
try:
    article = Article(
        title="My First Article",
        content="This is the content of my article...",
        author=user,  # Link to user
        tags=["python", "tutorial"],
        status=ArticleStatus.DRAFT
    )
    await article.insert()
except Exception as e:
    print(f"Validation error: {e}")

# Bulk insert
users = [
    User(username="bob", email="bob@example.com"),
    User(username="carol", email="carol@example.com"),
]
inserted_users = await User.insert_many(users)
print(f"Inserted {len(inserted_users.inserted_ids)} users")
```

#### Read

```python
# Find by ID
user = await User.get("507f1f77bcf86cd799439011")

# Find one with filter
alice = await User.find_one(User.username == "alice")

# Find many with filters
published_articles = await Article.find(
    Article.status == ArticleStatus.PUBLISHED
).to_list()

# Projection (select specific fields)
user_summaries = await User.find(
    {},
    projection={"username": 1, "email": 1, "created_at": 1}
).to_list()

# Sorting and limiting
recent_articles = await Article.find(
    Article.status == ArticleStatus.PUBLISHED
).sort(-Article.published_at).limit(10).to_list()

# Count documents
active_users = await User.count_documents(User.is_active == True)

# Check if document exists
exists = await User.find_one(User.email == "test@example.com").exists()

# Fetch with linked documents
article_with_author = await Article.find_one(
    Article.title == "My First Article",
    fetch_links=True
)
print(f"Author: {article_with_author.author.username}")
```

#### Update

```python
# Update single document
await User.find_one(User.username == "alice").update(
    {"$set": {"bio": "Senior Python Developer"}}
)

# Update with upsert
await User.find_one(User.username == "dave").update(
    {"$set": {"email": "dave@example.com", "username": "dave"}},
    upsert=True
)

# Update many documents
await Article.find(Article.status == ArticleStatus.DRAFT).update_many(
    {"$set": {"status": ArticleStatus.PUBLISHED, "published_at": datetime.utcnow()}}
)

# Increment field
await Article.find_one(Article.title == "My First Article").update(
    {"$inc": {"view_count": 1}}
)

# Update using document instance
user = await User.find_one(User.username == "alice")
user.bio = "Updated bio"
await user.save()
```

#### Delete

```python
# Delete single document
await Comment.find_one(Comment.content == "spam comment").delete()

# Delete many documents
await User.find(User.is_active == False).delete_many()

# Soft delete (mark as deleted instead of removing)
await Comment.find_one(Comment.id == comment_id).update(
    {"$set": {"is_deleted": True}}
)

# Delete by ID
await User.find_one(User.id == user_id).delete()

# Delete all documents (use with caution!)
await Comment.delete_all()
```

---

### 6. Advanced Queries & Aggregations

```python
from beanie import PydanticObjectId

# Complex filter: articles by tag or author
pipelines = [
    {"$match": {"tags": "python"}},
    {"$group": {"_id": "$author", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
]
top_authors = await Article.aggregate(pipelines).to_list()

# Lookup comments with article data
pipeline = [
    {"$lookup": {
        "from": "articles",
        "localField": "article",
        "foreignField": "_id",
        "as": "article_info"
    }},
]
comments_with_article = await Comment.aggregate(pipeline).to_list()
```

---

### 7. Projections & Pagination

```python
# Paginate articles
page_size = 10
page = await Article.find({}).skip((page_number-1)*page_size).limit(page_size).to_list()

# Include/exclude fields
users = await User.find({}, projection={"email": 1}, skip=0, limit=20).to_list()
```

---

### 8. Text Search

```python
# Ensure a `text` index on Article.tags or content
search_results = await Article.find(
    Article.content.search("async ODM tutorial")
).to_list()
```

---

### 9. Transactions

```python
async with client.start_session() as s:
    async with s.start_transaction():
        user = User(username="temp", email="temp@example.com")
        await user.insert(session=s)
        article = Article(title="Temp", content="...", author=user)
        await article.insert(session=s)
```

---

 
 
#### Performance Optimization
```python
# Use projections to limit returned fields
users = await User.find({}, projection={"username": 1, "email": 1}).to_list()

# Use indexes for frequently queried fields
# Add compound indexes for multi-field queries

# Batch operations when possible
await User.insert_many(user_list)
```

#### Error Handling
```python
from beanie.exceptions import DocumentNotFound
from pymongo.errors import DuplicateKeyError

try:
    user = await User.find_one(User.username == "nonexistent")
    if not user:
        raise DocumentNotFound("User not found")
except DocumentNotFound:
    print("User not found")
except DuplicateKeyError:
    print("Username already exists")
```

#### Environment Configuration
```python
# Use environment variables for database configuration
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017/mydb"
    database_name: str = "mydb"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

#### Testing
```python
import pytest
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

@pytest.fixture
async def db():
    # Use a test database
    client = AsyncIOMotorClient("mongodb://localhost:27017/test_db")
    database = client.test_db
    await init_beanie(database=database, document_models=[User, Article, Comment])
    yield database
    # Cleanup after tests
    await database.drop_collection("users")
    await database.drop_collection("articles")
    await database.drop_collection("comments")
```

---

### References

* **Beanie Official Documentation** – [https://beanie-odm.dev/](https://beanie-odm.dev/)
* **Beanie API Documentation** – [https://beanie-odm.dev/api-documentation/](https://beanie-odm.dev/api-documentation/)
* **Getting Started** – [https://beanie-odm.dev/getting-started/](https://beanie-odm.dev/getting-started/)
* **Query Operators** – [https://beanie-odm.dev/api-documentation/operators/find/](https://beanie-odm.dev/api-documentation/operators/find/)
* **Relations Guide** – [https://beanie-odm.dev/tutorial/relations/](https://beanie-odm.dev/tutorial/relations/)
* **Migrations Guide** – [https://beanie-odm.dev/tutorial/migrations/](https://beanie-odm.dev/tutorial/migrations/)

---
