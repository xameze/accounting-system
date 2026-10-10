"""Точка входа приложения учета учетных записей организации."""
from users import (
    generate_login, add_user, sort_users_by_name, get_user_by_id,
)
from systems import get_system_name
from accounts import (
    get_status_description, check_password_strength, check_access,
    days_until_expiration,
    add_account, find_account, filter_accounts_by_status,
    sort_accounts_by_login, is_login_unique,
    block_account, delete_account, filter_expiring_soon,
)
from storage import load_data, save_data
from utils import input_str, input_int, input_date, input_status

USERS_FILE = "data/users.json"
SYSTEMS_FILE = "data/systems.json"
ACCOUNTS_FILE = "data/accounts.json"


def demo_pr1(users: list[dict], systems: list[dict],
             accounts: list[dict]) -> None:
    """Демонстрация сценария из ПР1 на данных проекта.

    Использует исходные функции ПР1 с их изначальными сигнатурами.
    """
    if not accounts:
        print("Нет учетных записей для демонстрации.")
        return

    account = accounts[0]
    user = get_user_by_id(users, account["user_id"])
    full_name = user["full_name"] if user else "Неизвестный пользователь"
    system_name = get_system_name(systems, account["system_id"])
    status = account["status"]
    password = "qwerty123"

    # Вызовы функций ПР1 — сигнатуры сохранены:
    login = generate_login(full_name)
    status_desc = get_status_description(status)
    password_strength = check_password_strength(password)
    access_message = check_access(system_name, status)
    days_left = days_until_expiration(account["expires_at"])

    print("\n=== Учетная запись (демонстрация ПР1) ===")
    print(f"Пользователь: {full_name}")
    print(f"Логин: {login}")
    print(f"Система: {system_name}")
    print(f"Статус: {status_desc}")
    print(f"Пароль: {password_strength}")
    print(access_message)
    print(f"До истечения срока: {days_left} дн.")


def show_users(users: list[dict]) -> None:
    """Вывести список пользователей."""
    if not users:
        print("Пользователи не найдены.")
        return
    print("\n--- Пользователи ---")
    for user in sort_users_by_name(users):
        print(f"[{user['id']}] {user['full_name']} | "
              f"{user['position']} | {user['email']}")


def show_accounts(accounts: list[dict], users: list[dict],
                  systems: list[dict]) -> None:
    """Вывести список учетных записей."""
    if not accounts:
        print("Учетные записи не найдены.")
        return
    print("\n--- Учетные записи ---")
    for account in sort_accounts_by_login(accounts):
        user = get_user_by_id(users, account["user_id"])
        user_name = user["full_name"] if user else "Неизвестный пользователь"
        system_name = get_system_name(systems, account["system_id"])
        status_desc = get_status_description(account["status"])
        days_left = days_until_expiration(account["expires_at"])
        access = check_access(system_name, account["status"])
        print(f"[{account['id']}] {account['login']} | "
              f"{user_name} | {system_name} | {status_desc} | "
              f"осталось {days_left} дн. | {access}")


def menu_find_account(accounts: list[dict], users: list[dict],
                      systems: list[dict]) -> None:
    """Пункт меню: поиск учетной записи по логину."""
    query = input_str("Введите часть логина: ")
    found = find_account(accounts, query)
    if not found:
        print("Ничего не найдено.")
        return
    show_accounts(found, users, systems)


def menu_filter_by_status(accounts: list[dict], users: list[dict],
                          systems: list[dict]) -> None:
    """Пункт меню: отбор по статусу."""
    status = input_status("Статус (active/blocked/expired): ")
    found = filter_accounts_by_status(accounts, status)
    if not found:
        print("Нет учетных записей с таким статусом.")
        return
    show_accounts(found, users, systems)


def menu_add_account(accounts: list[dict], users: list[dict]) -> None:
    """Пункт меню: добавить учетную запись."""
    if not users:
        print("Сначала добавьте пользователя.")
        return
    show_users(users)
    user_id = input_int("ID пользователя: ")
    if get_user_by_id(users, user_id) is None:
        print("Пользователь не найден.")
        return
    system_id = input_int("ID системы: ")
    login = input_str("Логин: ")
    if not is_login_unique(accounts, login):
        print("Такой логин уже занят.")
        return
    status = input_status("Статус: ")
    created_at = input_date("Дата создания (ГГГГ-ММ-ДД): ")
    expires_at = input_date("Дата истечения (ГГГГ-ММ-ДД): ")
    add_account(accounts, user_id, system_id, login, status,
                created_at, expires_at)
    print("Учетная запись добавлена.")


def menu_add_user(users: list[dict]) -> None:
    """Пункт меню: добавить пользователя."""
    full_name = input_str("ФИО: ")
    email = input_str("Email: ")
    position = input_str("Должность: ")
    add_user(users, full_name, email, position)
    print(f"Пользователь добавлен. Логин по умолчанию: "
          f"{generate_login(full_name)}")


def menu_block_account(accounts: list[dict]) -> None:
    """Пункт меню: заблокировать учетную запись."""
    account_id = input_int("ID учетной записи для блокировки: ")
    if block_account(accounts, account_id):
        print("Учетная запись заблокирована.")
    else:
        print("Учетная запись не найдена.")


def menu_delete_account(accounts: list[dict]) -> None:
    """Пункт меню: удалить учетную запись."""
    account_id = input_int("ID учетной записи для удаления: ")
    if delete_account(accounts, account_id):
        print("Учетная запись удалена.")
    else:
        print("Учетная запись не найдена.")


def menu_expiring(accounts: list[dict], users: list[dict],
                  systems: list[dict]) -> None:
    """Пункт меню: показать скоро истекающие учетные записи."""
    days = input_int("За сколько дней показать истекающие записи: ")
    found = filter_expiring_soon(accounts, days)
    if not found:
        print("Нет учетных записей, истекающих в этот период.")
        return
    show_accounts(found, users, systems)


def print_menu() -> None:
    """Напечатать главное меню."""
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
    users = load_data(USERS_FILE, [])
    systems = load_data(SYSTEMS_FILE, [])
    accounts = load_data(ACCOUNTS_FILE, [])

    # Показываем сценарий ПР1 при запуске
    demo_pr1(users, systems, accounts)

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
            show_accounts(accounts, users, systems)
        elif choice == "3":
            menu_find_account(accounts, users, systems)
        elif choice == "4":
            menu_filter_by_status(accounts, users, systems)
        elif choice == "5":
            menu_expiring(accounts, users, systems)
        elif choice == "6":
            menu_add_user(users)
        elif choice == "7":
            menu_add_account(accounts, users)
        elif choice == "8":
            menu_block_account(accounts)
        elif choice == "9":
            menu_delete_account(accounts)
        elif choice == "10":
            demo_pr1(users, systems, accounts)
        else:
            print("Неизвестное действие.")

    save_data(USERS_FILE, users)
    save_data(ACCOUNTS_FILE, accounts)
    save_data(SYSTEMS_FILE, systems)
    print("Данные сохранены. До свидания.")


if __name__ == "__main__":
    main()
