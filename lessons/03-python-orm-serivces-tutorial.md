# Beanie ODM Service Layer (CRUD Only)

This document demonstrates how to implement a **service layer** using **Beanie ODM** for MongoDB, without using FastAPI routers. It includes both **function-based** and **class-based** service styles.

---

## Project Structure

```
app/
├── main.py
├── models/
│   └── user.py
├── services/
│   └── user_service.py
```

---

## 1. `models/user.py` – Beanie Document

```python
from beanie import Document
from pydantic import EmailStr
from typing import Optional

class User(Document):
    name: str
    email: EmailStr

    class Settings:
        name = "users"
```

---

## 2. `services/user_service.py` – Function-Based Service Layer

```python
from typing import List, Optional
from app.models.user import User
from pydantic import EmailStr

# CREATE
async def create_user(name: str, email: EmailStr) -> User:
    user = User(name=name, email=email)
    await user.insert()
    return user

# READ by ID
async def get_user_by_id(user_id: str) -> Optional[User]:
    return await User.get(user_id)

# READ all
async def get_all_users() -> List[User]:
    return await User.find_all().to_list()

# UPDATE
async def update_user_name(user_id: str, new_name: str) -> Optional[User]:
    user = await User.get(user_id)
    if user:
        user.name = new_name
        await user.save()
    return user

# DELETE
async def delete_user(user_id: str) -> bool:
    user = await User.get(user_id)
    if user:
        await user.delete()
        return True
    return False
```

---

## 3. `services/user_service.py` – Class-Based Service Layer

```python
class UserService:
    async def create(self, name: str, email: EmailStr) -> User:
        user = User(name=name, email=email)
        await user.insert()
        return user

    async def get_by_id(self, user_id: str) -> Optional[User]:
        return await User.get(user_id)

    async def get_all(self) -> List[User]:
        return await User.find_all().to_list()

    async def update_name(self, user_id: str, new_name: str) -> Optional[User]:
        user = await User.get(user_id)
        if user:
            user.name = new_name
            await user.save()
        return user

    async def delete(self, user_id: str) -> bool:
        user = await User.get(user_id)
        if user:
            await user.delete()
            return True
        return False
```

---

## 4. Example Usage – Function-Based CRUD

```python
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.user import User
from app.services.user_service import (
    create_user,
    get_user_by_id,
    get_all_users,
    update_user_name,
    delete_user
)

async def main():
    # 1. Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.mydb, document_models=[User])

    # 2. Create a user
    user = await create_user(name="Bob", email="bob@example.com")
    print("✅ Created:", user)

    # 3. Get user by ID
    found_user = await get_user_by_id(str(user.id))
    print("🔍 Found:", found_user)

    # 4. Update user name
    updated_user = await update_user_name(str(user.id), "Bobby")
    print("✏️ Updated:", updated_user)

    # 5. Get all users
    users = await get_all_users()
    print("📃 All users:", users)

    # 6. Delete user
    deleted = await delete_user(str(user.id))
    print("🗑️ Deleted:", deleted)

# Run it
asyncio.run(main())
```

---

## ✅ Summary

* This service layer avoids a repository layer and interacts directly with Beanie ODM.
* Use the function-based or class-based style depending on your project needs.
* Easy to integrate into FastAPI later if needed.

---

## 🧪 Practice Exercises

These exercises are designed to reinforce your understanding of Beanie service layers. You can apply them to the existing `User` model or explore different domain models.

### ✅ Required Models

You must implement at least one of the following domain-specific models:

```python
class Order(Document):
    product_name: str
    quantity: int
    price: float
    created_at: datetime
    is_deleted: bool = False

    class Settings:
        name = "orders"
 
class Sale(Document):
    item_id: str
    amount: float
    sale_date: datetime
    status: str  # e.g., "completed", "pending"
    is_deleted: bool = False

    class Settings:
        name = "sales"
 
class User(Document):
    name: str
    email: EmailStr
    age: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_deleted: bool = False

    class Settings:
        name = "users"
```

### 🧪 Exercises

Apply the following exercises to **any model** (`User`, `Order`,   `Sale`) based on your context:

1. **Add an extra field** (e.g., `age`, `status`, `is_deleted`) and update all CRUD methods to support it.
2. **Create a method to find a document by name or another field** using exact and partial matches.
3. **Write a method to update multiple fields** in a single operation (e.g., name and email or quantity and price).
4. **Add pagination support** to the "get all" method using `skip` and `limit` parameters.
5. **Implement a soft delete mechanism** by marking documents as deleted (e.g., `is_deleted=True`) instead of physically removing them.
6. **Find documents created within the last 7 days** using a `datetime` filter (e.g., `created_at`).

These tasks will help you get more comfortable with Beanie’s query capabilities and service design. with Beanie’s query capabilities and service design.

---

## 🔗 References

* [Beanie Documentation](https://roman-right.github.io/beanie/) – Official Beanie ODM guide
* [Motor (Async MongoDB Driver)](https://motor.readthedocs.io/en/stable/)
* [Pydantic](https://docs.pydantic.dev/)
* [MongoDB](https://www.mongodb.com/)
