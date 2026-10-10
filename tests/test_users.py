"""Тесты функций работы с пользователями."""
from users import add_user, find_user, generate_login, sort_users_by_name


def test_generate_login():
    assert generate_login("Иванов Иван Иванович") == "иванов.иван.иванович"


def test_add_user():
    users = []
    add_user(users, "Петров Пётр Петрович", "p@example.com", "Инженер")
    assert len(users) == 1
    assert users[0]["id"] == 1


def test_find_user():
    users = []
    add_user(users, "Сидорова Анна", "s@example.com", "Бухгалтер")
    add_user(users, "Петров Пётр", "p@example.com", "Инженер")
    result = find_user(users, "сидорова")
    assert len(result) == 1
    assert result[0]["full_name"] == "Сидорова Анна"


def test_sort_users_by_name():
    users = []
    add_user(users, "Яковлев Яков", "y@example.com", "Инженер")
    add_user(users, "Абрамов Абрам", "a@example.com", "Бухгалтер")
    sorted_users = sort_users_by_name(users)
    assert sorted_users[0]["full_name"] == "Абрамов Абрам"
