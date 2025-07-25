# 🔄 How ORM/ODM Works

ORM (Object Relational Mapping) and ODM (Object Document Mapping) allow developers to define database schemas as classes and interact with data using objects rather than writing raw queries. This abstraction simplifies data access, validation, and relationships.

## 🧠 Key Concepts

```
Python Class (Model) <--> ODM/ORM <--> Database Document/Row
```

## 🔁 Workflow Overview

1. **Define Models** – Create Pydantic or ORM classes that describe the structure of your data.
2. **CRUD Operations** – Use methods like `.insert()`, `.find()`, `.update()` to interact with the database.
3. **Schema Mapping** – Fields in your class correspond to fields in the database.
4. **Relationships** –
   - `Link[Other]`: Connects to another document (like a foreign key).
   - `BackLink[Other]`: Reverse-lookup from the connected document.
5. **Data Serialization** – Python objects are converted to BSON/JSON for MongoDB.

## 🔗 Conceptual Diagram

```
[ Python Class ]             [ MongoDB Document ]
+------------------+        +-------------------------+
| class User       |        | {                       |
|------------------|        |   _id: ObjectId,        |
| name: str        |  <---> |   "name": "Alice",      |
| email: EmailStr  |        |   "email": "..."        |
+------------------+        +-------------------------+
```

This enables querying like:
```python
await User.find_one(User.email == "alice@example.com")
```
instead of:
```js
db.users.findOne({ email: "alice@example.com" })
```

---

# 🧠 Beanie ODM + MongoDB Guide

A complete guide to understanding how Beanie ODM works with MongoDB through models, raw documents, and visual relationships.

---

## ✅ What is Beanie?

**Beanie** is an **Object Document Mapper (ODM)** built on top of:

- **Pydantic**: For data validation
- **Motor**: For async access to **MongoDB**

It allows you to work with MongoDB using **Python classes** instead of raw queries.

...


A complete guide to understanding how Beanie ODM works with MongoDB through models, raw documents, and visual relationships.
 
 
---

## 📆 Document Models in Your System

You have 3 main documents:

1. `User`
2. `Article`
3. `Comment`

---

## 🔗 Relationships Overview

```
User
 └──> writes ── Article
                  └──> receives ── Comment
                                   ├──> written by ── User
                                   └──> replies to ── Comment (optional)
```

---

## 🧱 Python ODM Models

### 1. `User`

```python
class User(Document):
    username: str
    email: EmailStr
    age: int | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    updated_at: datetime | None = None
    bio: str | None = None
    is_active: bool = True

    articles: BackLink["Article"] = Field(original_field="author")
```

---

### 2. `Article`

```python
class Article(Document):
    title: str
    content: str
    summary: str | None = None
    author: Link["User"]
    tags: list[str] = Field(default_factory=list)
    status: ArticleStatus = ArticleStatus.DRAFT
    published_at: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None
    view_count: int = Field(default=0)

    comments: BackLink["Comment"] = Field(original_field="article")
```

---

### 3. `Comment`

```python
class Comment(Document):
    article: Link["Article"]
    author: Link["User"]
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None
    is_deleted: bool = False
    is_edited: bool = False
    parent_comment: Link["Comment"] | None = None

    replies: BackLink["Comment"] = Field(original_field="parent_comment")
```

---

## 🗾️ Raw MongoDB Documents

### `users` Collection

```json
{
  "_id": "user123",
  "username": "john_doe",
  "email": "john@example.com",
  "age": 30,
  "created_at": "2025-07-25T08:00:00Z",
  "updated_at": null,
  "bio": "Python developer",
  "is_active": true
}
```

---

### `articles` Collection

```json
{
  "_id": "article456",
  "title": "My First Blog Post",
  "content": "Hello world!",
  "summary": "Intro post",
  "author": "user123",
  "tags": ["blog", "intro"],
  "status": "published",
  "published_at": "2025-07-25T10:00:00Z",
  "created_at": "2025-07-25T08:30:00Z",
  "updated_at": null,
  "view_count": 100
}
```

---

### `comments` Collection

#### Root Comment

```json
{
  "_id": "comment789",
  "article": "article456",
  "author": "user123",
  "content": "Nice post!",
  "created_at": "2025-07-25T11:00:00Z",
  "updated_at": null,
  "is_deleted": false,
  "is_edited": false,
  "parent_comment": null
}
```

#### Reply to Above Comment

```json
{
  "_id": "comment790",
  "article": "article456",
  "author": "user123",
  "content": "Thanks!",
  "created_at": "2025-07-25T11:30:00Z",
  "updated_at": null,
  "is_deleted": false,
  "is_edited": true,
  "parent_comment": "comment789"
}
```

---

## 🗾️ Visual Mapping

```
+------------------------+
|        User           |
+------------------------+
| _id: user123           |
| username: john_doe     |
| email: john@example.com|
+------------------------+
             |
             |  (writes)
             v
+------------------------+
|       Article          |
+------------------------+
| _id: article456        |
| author: user123        |
| title: My First Blog   |
+------------------------+
             |
             |  (receives)
             v
+------------------------+
|       Comment          |
+------------------------+
| _id: comment789        |
| article: article456    |
| author: user123        |
| content: Nice post!    |
| parent_comment: null   |
+------------------------+
             |
             |  (replies)
             v
+------------------------+
|   Comment (Reply)      |
+------------------------+
| _id: comment790        |
| parent_comment: comment789 |
| content: Thanks!       |
+------------------------+
```

---

## 📊 Example Usage

### Insert User

```python
user = User(username="john_doe", email="john@example.com", age=30)
await user.insert()
```

### Insert Article

```python
article = Article(title="My First Blog Post", content="Hello world!", author=user)
await article.insert()
```

### Insert Comment

```python
comment = Comment(content="Nice post!", author=user, article=article)
await comment.insert()
```

### Insert Reply

```python
reply = Comment(content="Thanks!", author=user, article=article, parent_comment=comment)
await reply.insert()
```

---

## 📚 Summary Table

| Concept            | ODM (Beanie) Syntax               | MongoDB Data                     |
| ------------------ | --------------------------------- | -------------------------------- |
| Link (foreign key) | `Link["User"]`                    | `"author": "user123"`            |
| BackLink           | `BackLink["Article"]` in `User`   | Resolved via reverse query       |
| Recursive Link     | `parent_comment: Link["Comment"]` | `"parent_comment": "comment789"` |
| Automatic time     | `default_factory=datetime.utcnow` | ISO timestamps in UTC            |
| Enum field         | `status: ArticleStatus.PUBLISHED` | `"status": "published"`          |

---

 