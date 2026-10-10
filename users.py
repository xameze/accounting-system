"""Функции работы с пользователями организации."""


def generate_login(full_name: str) -> str:
    """Формирует логин из ФИО: Иванов Иван Иванович -> ivanov.ivan.ivanovich."""
    login = full_name.lower().replace(" ", ".")
    return login


def add_user(users: list[dict], full_name: str, email: str,
             position: str) -> None:
    """Добавить пользователя в список users."""
    new_id = max((u["id"] for u in users), default=0) + 1
    users.append({
        "id": new_id,
        "full_name": full_name,
        "email": email,
        "position": position,
    })


def find_user(users: list[dict], query: str) -> list[dict]:
    """Найти пользователей по подстроке в ФИО или email."""
    query_lower = query.lower()
    result = []
    for user in users:
        if (query_lower in user["full_name"].lower()
                or query_lower in user["email"].lower()):
            result.append(user)
    return result


def sort_users_by_name(users: list[dict]) -> list[dict]:
    """Отсортировать пользователей по ФИО."""
    return sorted(users, key=lambda u: u["full_name"])


def get_user_by_id(users: list[dict], user_id: int) -> dict | None:
    """Вернуть пользователя по id или None, если не найден."""
    for user in users:
        if user["id"] == user_id:
            return user
    return None
