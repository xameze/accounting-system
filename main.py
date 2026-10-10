"""Точка входа приложения учета учетных записей организации."""
from models import User, Account
from models.users import (
    add_user, sort_users_by_name, get_user_by_id,
)
from models.systems import get_system_by_id
from models.accounts import (
    add_account, find_account, filter_accounts_by_status,
    sort_accounts_by_login, is_login_unique,
    block_account, delete_account, filter_expiring_soon,
)
from storage import (
    load_users, load_systems, load_accounts,
    save_users, save_systems, save_accounts,
)
from utils import input_str, input_int, input_date, input_status

USERS_FILE = "data/users.json"
SYSTEMS_FILE = "data/systems.json"
ACCOUNTS_FILE = "data/accounts.json"


def demo_pr1(accounts: list) -> None:
    """Демонстрация сценария ПР1 через методы объекта Account."""
    if not accounts:
        print("Нет учетных записей для демонстрации.")
        return

    account = accounts[0]
    password = "qwerty123"

    print("\n=== Демонстрация сценария ПР1 ===")
    print(f"Пользователь: {account.user.full_name}")
    print(f"Логин: {account.login}")
    print(f"Система: {account.system.name}")
    print(f"Статус: {account.status_description}")
    print(f"Пароль: {Account.check_password_strength(password)}")
    print(account.check_access())
    print(f"До истечения срока: "
          f"{account.days_until_expiration()} дн.")


def show_users(users: list) -> None:
    """Вывести список пользователей (объектов User)."""
    if not users:
        print("Пользователи не найдены.")
        return
    print("\n--- Пользователи ---")
    for user in sort_users_by_name(users):
        print(user)


def show_accounts(accounts: list) -> None:
    """Вывести список учетных записей (объектов Account)."""
    if not accounts:
        print("Учетные записи не найдены.")
        return
    print("\n--- Учетные записи ---")
    for account in sort_accounts_by_login(accounts):
        print(f"{account} | осталось "
              f"{account.days_until_expiration()} дн. | "
              f"{account.check_access()}")


def menu_add_user(users: list) -> None:
    """Добавить пользователя."""
    full_name = input_str("ФИО: ")
    email = input_str("Email: ")
    position = input_str("Должность: ")
    user = add_user(users, full_name, email, position)
    print(f"Пользователь добавлен: {user}")
    print(f"Логин по умолчанию: {User.generate_login(full_name)}")


def menu_add_account(accounts: list, users: list, systems: list) -> None:
    """Добавить учетную запись."""
    if not users or not systems:
        print("Сначала добавьте пользователя и систему.")
        return
    show_users(users)
    user_id = input_int("ID пользователя: ")
    user = get_user_by_id(users, user_id)
    if user is None:
        print("Пользователь не найден.")
        return
    for s in systems:
        print(s)
    system_id = input_int("ID системы: ")
    system = get_system_by_id(systems, system_id)
    if system is None:
        print("Система не найдена.")
        return
    login = input_str("Логин: ")
    if not is_login_unique(accounts, login):
        print("Логин занят.")
        return
    status = input_status("Статус (active/blocked/expired): ")
    created_at = input_date("Дата создания (ГГГГ-ММ-ДД): ")
    expires_at = input_date("Дата истечения (ГГГГ-ММ-ДД): ")
    account = add_account(accounts, user, system, login, status,
                          created_at, expires_at)
    print(f"Учетная запись создана: {account}")


def menu_find_account(accounts: list) -> None:
    """Поиск учетной записи по логину."""
    query = input_str("Часть логина: ")
    found = find_account(accounts, query)
    if not found:
        print("Ничего не найдено.")
        return
    show_accounts(found)


def menu_filter_by_status(accounts: list) -> None:
    """Отбор учетных записей по статусу."""
    status = input_status("Статус (active/blocked/expired): ")
    found = filter_accounts_by_status(accounts, status)
    if not found:
        print("Нет учетных записей с таким статусом.")
        return
    show_accounts(found)


def menu_block_account(accounts: list) -> None:
    """Заблокировать учетную запись."""
    account_id = input_int("ID учетной записи: ")
    if block_account(accounts, account_id):
        print("Учетная запись заблокирована.")
    else:
        print("Учетная запись не найдена.")


def menu_delete_account(accounts: list) -> None:
    """Удалить учетную запись."""
    account_id = input_int("ID учетной записи: ")
    if delete_account(accounts, account_id):
        print("Учетная запись удалена.")
    else:
        print("Учетная запись не найдена.")


def menu_expiring(accounts: list) -> None:
    """Показать истекающие учетные записи."""
    days = input_int("За сколько дней: ")
    found = filter_expiring_soon(accounts, days)
    if not found:
        print("Нет истекающих записей.")
        return
    show_accounts(found)


def print_menu() -> None:
    """Главное меню."""
    print("\n== Система учета учетных записей ==")
    print("1. Показать пользователей")
    print("2. Показать учетные записи")
    print("3. Найти учетную запись по логину")
    print("4. Отобрать по статусу")
    print("5. Показать истекающие записи")
    print("6. Добавить пользователя")
    print("7. Добавить учетную запись")
    print("8. Заблокировать учетную запись")
    print("9. Удалить учетную запись")
    print("10. Демонстрация сценария ПР1")
    print("0. Выход")


def main() -> None:
    """Точка запуска приложения."""
    users = load_users(USERS_FILE)
    systems = load_systems(SYSTEMS_FILE)
    accounts = load_accounts(ACCOUNTS_FILE, users, systems)

    demo_pr1(accounts)

    while True:
        print_menu()
        try:
            choice = input("Выберите действие: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nВыход.")
            break

        if choice == "0":
            break
        elif choice == "1":
            show_users(users)
        elif choice == "2":
            show_accounts(accounts)
        elif choice == "3":
            menu_find_account(accounts)
        elif choice == "4":
            menu_filter_by_status(accounts)
        elif choice == "5":
            menu_expiring(accounts)
        elif choice == "6":
            menu_add_user(users)
        elif choice == "7":
            menu_add_account(accounts, users, systems)
        elif choice == "8":
            menu_block_account(accounts)
        elif choice == "9":
            menu_delete_account(accounts)
        elif choice == "10":
            demo_pr1(accounts)
        else:
            print("Неизвестное действие.")

    save_users(USERS_FILE, users)
    save_systems(SYSTEMS_FILE, systems)
    save_accounts(ACCOUNTS_FILE, accounts)
    print("Данные сохранены. До свидания.")


if __name__ == "__main__":
    main()
