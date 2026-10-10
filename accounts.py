"""Функции работы с учетными записями."""
from datetime import date


# ---------- Функции, перенесённые из ПР1 без изменений ----------

def get_status_description(status: str) -> str:
    """Возвращает описание статуса учетной записи."""
    if status == "active":
        return "Активна"
    elif status == "blocked":
        return "Заблокирована"
    elif status == "expired":
        return "Истек срок действия"
    else:
        return "Неизвестный статус"


def check_password_strength(password: str) -> str:
    """Проверяет пароль по простым правилам."""
    if len(password) < 8:
        return "Слабый: меньше 8 символов"
    elif password.isalpha():
        return "Слабый: только буквы"
    elif password.isdigit():
        return "Слабый: только цифры"
    else:
        return "Надёжный"


def check_access(system_name: str, status: str) -> str:
    """Определяет, разрешён ли доступ к системе."""
    if status == "active":
        return f"Доступ к системе '{system_name}' разрешён"
    elif status == "blocked":
        return (f"Доступ к системе '{system_name}' запрещён: "
                f"учетная запись заблокирована")
    elif status == "expired":
        return (f"Доступ к системе '{system_name}' запрещён: "
                f"срок действия истёк")
    else:
        return (f"Доступ к системе '{system_name}' не определён: "
                f"неизвестный статус")


def days_until_expiration(expiration_date_str: str) -> int:
    """Вычисляет, сколько дней осталось до истечения срока действия."""
    expiration_date = date.fromisoformat(expiration_date_str)
    today = date.today()
    delta = expiration_date - today
    return delta.days


# ---------- Новые функции ПР2 ----------

def add_account(accounts: list[dict], user_id: int, system_id: int,
                login: str, status: str,
                created_at: str, expires_at: str) -> None:
    """Добавить учетную запись в список accounts."""
    new_id = max((a["id"] for a in accounts), default=0) + 1
    accounts.append({
        "id": new_id,
        "user_id": user_id,
        "system_id": system_id,
        "login": login,
        "status": status,
        "created_at": created_at,
        "expires_at": expires_at,
    })


def find_account(accounts: list[dict], query: str) -> list[dict]:
    """Найти учетные записи по подстроке логина."""
    query_lower = query.lower()
    result = []
    for account in accounts:
        if query_lower in account["login"].lower():
            result.append(account)
    return result


def filter_accounts_by_status(accounts: list[dict],
                              status: str) -> list[dict]:
    """Отобрать учетные записи по статусу."""
    result = []
    for account in accounts:
        if account["status"] == status:
            result.append(account)
    return result


def sort_accounts_by_login(accounts: list[dict]) -> list[dict]:
    """Отсортировать учетные записи по логину (lambda-функция)."""
    return sorted(accounts, key=lambda a: a["login"])


def is_login_unique(accounts: list[dict], login: str) -> bool:
    """Проверить, что логин не занят другой учетной записью."""
    for account in accounts:
        if account["login"] == login:
            return False
    return True


def get_account_by_id(accounts: list[dict], account_id: int) -> dict | None:
    """Вернуть учетную запись по id или None, если не найдена."""
    for account in accounts:
        if account["id"] == account_id:
            return account
    return None


def block_account(accounts: list[dict], account_id: int) -> bool:
    """Заблокировать учетную запись. True — если получилось."""
    account = get_account_by_id(accounts, account_id)
    if account is None:
        return False
    account["status"] = "blocked"
    return True


def delete_account(accounts: list[dict], account_id: int) -> bool:
    """Удалить учетную запись по id. True — если получилось."""
    for i, account in enumerate(accounts):
        if account["id"] == account_id:
            accounts.pop(i)
            return True
    return False


def filter_expiring_soon(accounts: list[dict], days: int) -> list[dict]:
    """Отобрать учетные записи, истекающие в ближайшие days дней."""
    result = []
    for account in accounts:
        left = days_until_expiration(account["expires_at"])
        if 0 <= left <= days:
            result.append(account)
    return result
