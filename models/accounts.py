"""Класс Account и функции работы с учетными записями."""
from datetime import date
from typing import List, Optional

from .users import User, get_user_by_id
from .systems import System, get_system_by_id


class Account:
    """Учетная запись пользователя в информационной системе.

    Связывает объект User и объект System (композиция).
    """

    def __init__(self, account_id: int, user: User, system: System,
                 login: str, status: str,
                 created_at: str, expires_at: str) -> None:
        self.id = account_id
        self.user = user
        self.system = system
        self.login = login
        self.status = status
        self.created_at = created_at
        self.expires_at = expires_at

    def __str__(self) -> str:
        return (f"[{self.id}] {self.login} | {self.user.full_name} | "
                f"{self.system.name} | {self.status_description}")

    # ---------- Методы, относящиеся к конкретной учетной записи ----------

    def get_status_description(self) -> str:
        """Вернуть человекочитаемое описание статуса."""
        if self.status == "active":
            return "Активна"
        elif self.status == "blocked":
            return "Заблокирована"
        elif self.status == "expired":
            return "Истек срок действия"
        return "Неизвестный статус"

    def check_access(self) -> str:
        """Сообщение о доступе к системе по статусу."""
        if self.status == "active":
            return f"Доступ к системе '{self.system.name}' разрешён"
        elif self.status == "blocked":
            return (f"Доступ к системе '{self.system.name}' запрещён: "
                    f"учетная запись заблокирована")
        elif self.status == "expired":
            return (f"Доступ к системе '{self.system.name}' запрещён: "
                    f"срок действия истёк")
        return (f"Доступ к системе '{self.system.name}' не определён: "
                f"неизвестный статус")

    def days_until_expiration(self) -> int:
        """Сколько дней до истечения срока действия."""
        expires = date.fromisoformat(self.expires_at)
        return (expires - date.today()).days

    def block(self) -> None:
        """Заблокировать учетную запись."""
        self.status = "blocked"

    @staticmethod
    def check_password_strength(password: str) -> str:
        """Проверка пароля (декоратор @staticmethod)."""
        if len(password) < 8:
            return "Слабый: меньше 8 символов"
        elif password.isalpha():
            return "Слабый: только буквы"
        elif password.isdigit():
            return "Слабый: только цифры"
        return "Надёжный"

    # ---------- Свойство: доступ без круглых скобок ----------

    @property
    def status_description(self) -> str:
        """Краткое описание статуса (доступ как account.status_description)."""
        return self.get_status_description()

    # ---------- Конструирование из JSON и обратно ----------

    @classmethod
    def from_data(cls, data: dict, users: List[User],
                  systems: List[System]) -> Optional["Account"]:
        """Создать объект Account, связав его с User и System из коллекций."""
        user = get_user_by_id(users, data["user_id"])
        system = get_system_by_id(systems, data["system_id"])
        if user is None or system is None:
            return None
        return cls(
            account_id=data["id"],
            user=user,
            system=system,
            login=data["login"],
            status=data["status"],
            created_at=data["created_at"],
            expires_at=data["expires_at"],
        )

    def to_dict(self) -> dict:
        """Структура для JSON: сохраняем только идентификаторы связей."""
        return {
            "id": self.id,
            "user_id": self.user.id,
            "system_id": self.system.id,
            "login": self.login,
            "status": self.status,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
        }


# ---------- Функции обработки коллекции объектов Account ----------

def add_account(accounts: List[Account], user: User, system: System,
                login: str, status: str,
                created_at: str, expires_at: str) -> Account:
    """Создать объект Account и добавить его в коллекцию."""
    new_id = max((a.id for a in accounts), default=0) + 1
    account = Account(new_id, user, system, login, status,
                      created_at, expires_at)
    accounts.append(account)
    return account


def find_account(accounts: List[Account], query: str) -> List[Account]:
    """Найти учетные записи по подстроке логина."""
    query_lower = query.lower()
    return [a for a in accounts if query_lower in a.login.lower()]


def filter_accounts_by_status(accounts: List[Account],
                              status: str) -> List[Account]:
    """Отобрать учетные записи по статусу."""
    return [a for a in accounts if a.status == status]


def sort_accounts_by_login(accounts: List[Account]) -> List[Account]:
    """Отсортировать по логину (lambda-функция)."""
    return sorted(accounts, key=lambda a: a.login)


def is_login_unique(accounts: List[Account], login: str) -> bool:
    """Проверить уникальность логина."""
    return all(a.login != login for a in accounts)


def get_account_by_id(accounts: List[Account],
                      account_id: int) -> Optional[Account]:
    """Вернуть учетную запись по id или None."""
    for account in accounts:
        if account.id == account_id:
            return account
    return None


def block_account(accounts: List[Account], account_id: int) -> bool:
    """Заблокировать учетную запись через её метод block()."""
    account = get_account_by_id(accounts, account_id)
    if account is None:
        return False
    account.block()
    return True


def delete_account(accounts: List[Account], account_id: int) -> bool:
    """Удалить учетную запись по id."""
    for i, account in enumerate(accounts):
        if account.id == account_id:
            accounts.pop(i)
            return True
    return False


def filter_expiring_soon(accounts: List[Account],
                         days: int) -> List[Account]:
    """Отобрать учетные записи, истекающие в ближайшие days дней."""
    result = []
    for account in accounts:
        left = account.days_until_expiration()
        if 0 <= left <= days:
            result.append(account)
    return result
def find_account_by_id(accounts: List[Account],
                       account_id: int) -> Optional[Account]:
    """Найти учётную запись по идентификатору."""
    for account in accounts:
        if account.id == account_id:
            return account
    return None
