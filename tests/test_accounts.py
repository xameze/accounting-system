"""Тесты функций работы с учетными записями."""
from accounts import (
    add_account, find_account, filter_accounts_by_status,
    is_login_unique, get_status_description, check_access,
    check_password_strength, days_until_expiration,
    sort_accounts_by_login,
)


def _make_account(accounts, login, status="active"):
    add_account(accounts, user_id=1, system_id=1, login=login,
                status=status, created_at="2026-01-01",
                expires_at="2099-12-31")


def test_add_account():
    accounts = []
    _make_account(accounts, "ivanov")
    assert len(accounts) == 1
    assert accounts[0]["login"] == "ivanov"


def test_is_login_unique():
    accounts = []
    _make_account(accounts, "ivanov")
    assert not is_login_unique(accounts, "ivanov")
    assert is_login_unique(accounts, "petrov")


def test_find_account():
    accounts = []
    _make_account(accounts, "ivanov")
    _make_account(accounts, "petrov")
    assert len(find_account(accounts, "ivan")) == 1


def test_filter_accounts_by_status():
    accounts = []
    _make_account(accounts, "ivanov", "active")
    _make_account(accounts, "petrov", "blocked")
    assert len(filter_accounts_by_status(accounts, "active")) == 1
    assert len(filter_accounts_by_status(accounts, "blocked")) == 1


def test_sort_accounts_by_login():
    accounts = []
    _make_account(accounts, "Яковлев")
    _make_account(accounts, "Абрамов")
    sorted_accounts = sort_accounts_by_login(accounts)
    assert sorted_accounts[0]["login"] == "Абрамов"


def test_get_status_description():
    assert get_status_description("active") == "Активна"
    assert get_status_description("blocked") == "Заблокирована"
    assert get_status_description("expired") == "Истек срок действия"
    assert get_status_description("other") == "Неизвестный статус"


def test_check_password_strength():
    assert "меньше 8" in check_password_strength("abc")
    assert "только буквы" in check_password_strength("abcdefgh")
    assert "только цифры" in check_password_strength("12345678")
    assert check_password_strength("qwerty123") == "Надёжный"


def test_check_access():
    assert "разрешён" in check_access("1С", "active")
    assert "заблокирована" in check_access("1С", "blocked")
    assert "истёк" in check_access("1С", "expired")


def test_days_until_expiration_positive():
    accounts = []
    _make_account(accounts, "ivanov")
    assert days_until_expiration(accounts[0]["expires_at"]) > 0
