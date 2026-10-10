"""Тесты класса User и функций работы с пользователями."""
from models import User
from models.users import add_user, find_user, sort_users_by_name


def test_user_creation():
    user = User(1, "Иванов Иван Иванович", "i@example.com", "Бухгалтер")
    assert user.id == 1
    assert user.full_name == "Иванов Иван Иванович"
    assert user.email == "i@example.com"
    assert user.position == "Бухгалтер"


def test_generate_login_static():
    assert User.generate_login("Иванов Иван") == "иванов.иван"


def test_validate_email_static():
    assert User.validate_email("a@b.com")
    assert not User.validate_email("invalid")


def test_email_domain_property():
    user = User(1, "Иванов Иван", "ivanov@company.ru", "Бухгалтер")
    assert user.email_domain == "company.ru"


def test_from_data_classmethod():
    data = {"id": 5, "full_name": "Петров Пётр",
            "email": "p@example.com", "position": "Инженер"}
    user = User.from_data(data)
    assert user.id == 5
    assert user.full_name == "Петров Пётр"


def test_add_user_returns_object():
    users = []
    user = add_user(users, "Сидоров Сидор", "s@example.com", "Инженер")
    assert isinstance(user, User)
    assert len(users) == 1
    assert users[0].id == 1


def test_find_user():
    users = []
    add_user(users, "Сидорова Анна", "s@example.com", "Бухгалтер")
    add_user(users, "Петров Пётр", "p@example.com", "Инженер")
    result = find_user(users, "сидорова")
    assert len(result) == 1
    assert result[0].full_name == "Сидорова Анна"


def test_sort_users_by_name():
    users = []
    add_user(users, "Яковлев Яков", "y@example.com", "Инженер")
    add_user(users, "Абрамов Абрам", "a@example.com", "Бухгалтер")
    assert sort_users_by_name(users)[0].full_name == "Абрамов Абрам"
