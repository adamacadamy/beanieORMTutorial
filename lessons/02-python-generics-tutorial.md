---

# Python Generics: Step-by-Step Lesson

---

## 1. What are Generics?

**Generics** allow you to create classes, functions, and data structures that can work with different data types **without losing type safety**.

Instead of using a concrete type (like `int` or `str`), generics use **type parameters**.

---

## 2. Why Use Generics?

* To make reusable components.
* To provide **type hints** for generic containers like lists, dictionaries, or custom classes.
* To catch type errors during static analysis with tools like **mypy**.

```python
from typing import List

def first_element(items: List[int]) -> int:
    return items[0]

print(first_element([1, 2, 3]))
```

This is limited to `List[int]`. **Generics** allow flexibility for any type.

---

## 3. Type Variables

We define **type variables** using `TypeVar`.

```python
from typing import TypeVar

T = TypeVar('T')

def first_element(items: list[T]) -> T:
    return items[0]

print(first_element([1, 2, 3]))
print(first_element(["a", "b"]))
```

`T` is a placeholder for the actual type.

---

## 4. Generic Functions

```python
T = TypeVar('T')

def get_last_element(items: list[T]) -> T:
    return items[-1]

print(get_last_element([10, 20, 30]))
print(get_last_element(["apple", "banana"]))
```

---

## 5. Generic Classes

```python
from typing import Generic

T = TypeVar('T')

class Box(Generic[T]):
    def __init__(self, content: T):
        self.content = content

    def get_content(self) -> T:
        return self.content

int_box = Box[int](42)
print(int_box.get_content())

str_box = Box[str]("Hello")
print(str_box.get_content())
```

---

## 6. Multiple Type Variables

```python
K = TypeVar('K')
V = TypeVar('V')

class Pair(Generic[K, V]):
    def __init__(self, key: K, value: V):
        self.key = key
        self.value = value

    def __repr__(self):
        return f"Pair({self.key}, {self.value})"

pair = Pair[str, int]("age", 30)
print(pair)
```

---

## 7. Constraining Type Variables

```python
T = TypeVar('T', bound=str)

def shout(value: T) -> T:
    return value.upper()

print(shout("hello"))
```

---

## 8. Variance (Advanced)

* `covariant=True`: allows a generic type to be used in a more derived context.
* `contravariant=True`: allows a generic type to be used in a more base context.

```python
T_co = TypeVar('T_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)
```

---

## 9. Using Protocols with Generics

```python
from typing import Protocol

class SupportsClose(Protocol):
    def close(self) -> None:
        ...

def close_resource(resource: SupportsClose) -> None:
    resource.close()
```

---

## 10. Practical Example – Generic Repository Pattern

```python
class Repository(Generic[T]):
    def __init__(self):
        self._items: list[T] = []

    def add(self, item: T):
        self._items.append(item)

    def get_all(self) -> list[T]:
        return self._items

repo = Repository[int]()
repo.add(10)
repo.add(20)
print(repo.get_all())
```

---

## Practice Tasks

1. **Create a generic function** `reverse_list` that returns a reversed list of any type.
2. **Create a generic class** `Stack` with `push`, `pop`, and `peek` methods.
3. **Create a generic Pair** with two different type variables.
4. **Use a bound TypeVar** to allow only `int` and `float` in a `MathBox` class.

---

## References
* [Python Typing Docs](https://docs.python.org/3/library/typing.html)
* [Typing — Python Docs](https://typing.readthedocs.io/en/latest/)

---

End of Lesson.
