## Exercise: Designing Beanie Models and CRUD Services with FastAPI

In this exercise, you will design three related Beanie document models (`User`, `Post`, and `Comment`) and outline the corresponding CRUD service functions. Rather than writing full code, focus on defining the model schemas and drafting service function signatures and descriptions.

### 1. Project Setup Questions

1. What commands would you run to create a new virtual environment and activate it?
2. Which dependencies are required for FastAPI, Beanie, Motor, and running the server with Uvicorn?
3. How would you organize your project directories and initial files (e.g., `models`, `services`, `main.py`)?

### 2. Model Design Questions

For each of the following models, specify:

* The Pydantic fields and their types
* Any validation constraints or default values
* Collection names via the `Settings` class

1. **User**

   * Fields should include `username`, `email`, `hashed_password`, and an optional `profile_picture_url`.
   * Consider unique constraints and indexing.

2. **Post**

   * Fields should include `author_id` (referencing a user), `title`, `content`, `created_at`, and an optional list of `tags`.
   * How would you represent the relationship to the `User` model?

3. **Comment**

   * Fields should include `post_id`, `author_id`, `content`, and `created_at`.
   * How would you enforce referential integrity for both `post_id` and `author_id`?

### 3. Service Layer Questions

For each model, outline service function signatures and brief descriptions without implementing full code. Include functions for create, read (single and list), update, and delete.

1. **User Services**

   * `create_user(data: dict) -> User`
   * `get_user(user_id: str) -> User`
   * `list_users() -> List[User]`
   * `update_user(user_id: str, data: dict) -> User`
   * `delete_user(user_id: str) -> None`

2. **Post Services**

   * `create_post(data: dict) -> Post`
   * `get_post(post_id: str) -> Post`
   * `list_posts() -> List[Post]`
   * `update_post(post_id: str, data: dict) -> Post`
   * `delete_post(post_id: str) -> None`

3. **Comment Services**

   * `create_comment(data: dict) -> Comment`
   * `get_comment(comment_id: str) -> Comment`
   * `list_comments(post_id: str) -> List[Comment]`
   * `update_comment(comment_id: str, data: dict) -> Comment`
   * `delete_comment(comment_id: str) -> None`

### 4. Initialization and Startup Questions

1. Describe how you would initialize Beanie with your three document models in `main.py`.
2. What FastAPI event decorator would you use to connect to MongoDB at startup?
3. Which MongoDB connection string format would you supply to `AsyncIOMotorClient`?

### 5. Usage Scenario Questions

Answer the following by outlining which service functions you'd call and in what order, explaining the purpose of each call:

1. **User Registration Flow**: A new user signs up, and you need to store their information and immediately retrieve it to display a welcome message. Which service calls would you use, and why?
2. **Post Creation and Listing**: A registered user creates a new post, then views a feed of all posts. Which service functions would you invoke to support this sequence?
