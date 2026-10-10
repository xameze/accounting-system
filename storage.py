"""Загрузка и сохранение данных через JSON с преобразованием в объекты."""
import json
import os
from typing import List

from models import User, System, Account


def load_data(filename: str, default):
    """Загрузить данные из JSON. При ошибке вернуть default."""
    if not os.path.exists(filename):
        return default
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"[!] Файл {filename} повреждён. Загружены пустые данные.")
        return default
    except OSError as error:
        print(f"[!] Ошибка чтения {filename}: {error}")
        return default


def save_data(filename: str, data) -> None:
    """Сохранить данные в JSON."""
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"[!] Ошибка записи в {filename}: {error}")


# ---------- Загрузка данных в объекты ----------

def load_users(filename: str) -> List[User]:
    """Загрузить пользователей из JSON и преобразовать в объекты User."""
    raw = load_data(filename, [])
    users: List[User] = []
    for data in raw:
        user = User.from_data(data)
        users.append(user)
    return users


def load_systems(filename: str) -> List[System]:
    """Загрузить системы из JSON и преобразовать в объекты System."""
    raw = load_data(filename, [])
    systems: List[System] = []
    for data in raw:
        systems.append(System.from_data(data))
    return systems


def load_accounts(filename: str, users: List[User],
                  systems: List[System]) -> List[Account]:
    """Загрузить учетные записи, связав их с объектами User и System."""
    raw = load_data(filename, [])
    accounts: List[Account] = []
    for data in raw:
        account = Account.from_data(data, users, systems)
        if account is not None:
            accounts.append(account)
        else:
            print(f"[!] Пропущена учетная запись id={data.get('id')}: "
                  f"не найден пользователь или система.")
    return accounts


# ---------- Сохранение объектов в JSON ----------

def save_users(filename: str, users: List[User]) -> None:
    """Сохранить пользователей, преобразовав объекты в dict."""
    save_data(filename, [u.to_dict() for u in users])


def save_systems(filename: str, systems: List[System]) -> None:
    """Сохранить системы."""
    save_data(filename, [s.to_dict() for s in systems])


def save_accounts(filename: str, accounts: List[Account]) -> None:
    """Сохранить учетные записи (в JSON — только id связей)."""
    save_data(filename, [a.to_dict() for a in accounts])
