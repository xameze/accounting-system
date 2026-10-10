"""Класс User и функции работы с пользователями."""
from typing import List, Optional


class User:
    """Пользователь организации."""

    def __init__(self, user_id: int, full_name: str,
                 email: str, position: str) -> None:
        self.id = user_id
        self.full_name = full_name
        self.email = email
        self.position = position

    def __str__(self) -> str:
        return f"[{self.id}] {self.full_name} ({self.position})"

    @staticmethod
    def generate_login(full_name: str) -> str:
        """Сформировать логин из ФИО."""
        return full_name.lower().replace(" ", ".")

    @staticmethod
    def validate_email(email: str) -> bool:
        """Простая проверка корректности email."""
        return "@" in email and "." in email.split("@")[-1]

    @property
    def email_domain(self) -> str:
        """Домен электронной почты без круглых скобок."""
        if "@" in self.email:
            return self.email.split("@")[-1]
        return ""

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из набора данных JSON."""
        return cls(
            user_id=data["id"],
            full_name=data["full_name"],
            email=data["email"],
            position=data["position"],
        )

    def to_dict(self) -> dict:
        """Преобразовать объект в структуру для JSON."""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "position": self.position,
        }


# ---------- Функции обработки коллекции объектов User ----------

def add_user(users: List[User], full_name: str, email: str,
             position: str) -> User:
    """Создать объект User и добавить его в коллекцию."""
    new_id = max((u.id for u in users), default=0) + 1
    user = User(new_id, full_name, email, position)
    users.append(user)
    return user


def find_user(users: List[User], query: str) -> List[User]:
    """Найти пользователей по подстроке в ФИО или email."""
    query_lower = query.lower()
    return [
        user for user in users
        if query_lower in user.full_name.lower()
        or query_lower in user.email.lower()
    ]


def sort_users_by_name(users: List[User]) -> List[User]:
    """Отсортировать пользователей по ФИО."""
    return sorted(users, key=lambda u: u.full_name)


def get_user_by_id(users: List[User], user_id: int) -> Optional[User]:
    """Вернуть пользователя по id или None."""
    for user in users:
        if user.id == user_id:
            return user
    return None
def find_user_by_id(users: List[User], user_id: int) -> Optional[User]:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None
