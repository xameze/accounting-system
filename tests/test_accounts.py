"""Тесты класса Account и функций работы с учетными записями."""
from models import User, System, Account
from models.accounts import (
    add_account, find_account, filter_accounts_by_status,
    is_login_unique, sort_accounts_by_login,
    get_account_by_id, block_account, delete_account,
)


def _make_user(users, name="Иванов Иван"):
    user = User(len(users) + 1, name, "u@example.com", "Бухгалтер")
    users.append(user)
    return user


def _make_system(systems, name="1С"):
    system = System(len(systems) + 1, name, "Учет")
    systems.append(system)
    return system


def _make_account(accounts, user, system,
                  login="ivanov", status="active"):
    add_account(accounts, user, system, login, status,
                "2026-01-01", "2099-12-31")


def test_account_creation_and_links():
    user = User(1, "Иванов Иван", "i@example.com", "Бухгалтер")
    system = System(1, "1С", "Учет")
    accounts = []
    _make_account(accounts, user, system)
    account = accounts[0]
    assert account.user is user
    assert account.system is system
    assert account.login == "ivanov"


def test_status_description_property():
    user = User(1, "Иванов Иван", "i@example.com", "Бухгалтер")
    system = System(1, "1С", "Учет")
    accounts = []
    _make_account(accounts, user, system, status="active")
    assert accounts[0].status_description == "Активна"


def test_check_access_method():
    user = User(1, "Иванов Иван", "i@example.com", "Бухгалтер")
    system = System(1, "1С", "Учет")
    accounts = []
    _make_account(accounts, user, system, status="blocked")
    assert "заблокирована" in accounts[0].check_access()


def test_check_password_strength_static():
    assert "меньше 8" in Account.check_password_strength("abc")
    assert Account.check_password_strength("qwerty123") == "Надёжный"


def test_block_method():
    user = User(1, "Иванов Иван", "i@example.com", "Бухгалтер")
    system = System(1, "1С", "Учет")
    accounts = []
    _make_account(accounts, user, system, status="active")
    accounts[0].block()
    assert accounts[0].status == "blocked"


def test_is_login_unique():
    user = User(1, "Иванов Иван", "i@example.com", "Бухгалтер")
    system = System(1, "1С", "Учет")
    accounts = []
    _make_account(accounts, user, system, login="ivanov")
    assert not is_login_unique(accounts, "ivanov")
    assert is_login_unique(accounts, "petrov")


def test_find_account():
    user = User(1, "Иванов Иван", "i@example.com", "Бухгалтер")
    system = System(1, "1С", "Учет")
    accounts = []
    _make_account(accounts, user, system, login="ivanov")
    _make_account(accounts, user, system, login="petrov")
    assert len(find_account(accounts, "ivan")) == 1


def test_filter_accounts_by_status():
    user = User(1, "Иванов Иван", "i@example.com", "Бухгалтер")
    system = System(1, "1С", "Учет")
    accounts = []
    _make_account(accounts, user, system, login="a", status="active")
    _make_account(accounts, user, system, login="b", status="blocked")
    assert len(filter_accounts_by_status(accounts, "active")) == 1
    assert len(filter_accounts_by_status(accounts, "blocked")) == 1


def test_sort_accounts_by_login():
    user = User(1, "Иванов Иван", "i@example.com", "Бухгалтер")
    system = System(1, "1С", "Учет")
    accounts = []
    _make_account(accounts, user, system, login="Яковлев")
    _make_account(accounts, user, system, login="Абрамов")
    assert sort_accounts_by_login(accounts)[0].login == "Абрамов"


def test_get_account_by_id():
    user = User(1, "Иванов Иван", "i@example.com", "Бухгалтер")
    system = System(1, "1С", "Учет")
    accounts = []
    _make_account(accounts, user, system)
    assert get_account_by_id(accounts, 1) is accounts[0]
    assert get_account_by_id(accounts, 99) is None


def test_block_and_delete():
    user = User(1, "Иванов Иван", "i@example.com", "Бухгалтер")
    system = System(1, "1С", "Учет")
    accounts = []
    _make_account(accounts, user, system)
    assert block_account(accounts, 1)
    assert accounts[0].status == "blocked"
    assert delete_account(accounts, 1)
    assert len(accounts) == 0
