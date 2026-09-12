from datetime import date


def generate_login(full_name: str) -> str:
    """Формирует логин из ФИО: Иванов Иван Иванович -> ivanov.ivan.ivanovich."""
    login = full_name.lower().replace(" ", ".")
    return login


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
        return f"Доступ к системе '{system_name}' запрещён: учетная запись заблокирована"
    elif status == "expired":
        return f"Доступ к системе '{system_name}' запрещён: срок действия истёк"
    else:
        return f"Доступ к системе '{system_name}' не определён: неизвестный статус"


def days_until_expiration(expiration_date_str: str) -> int:
    """Вычисляет, сколько дней осталось до истечения срока действия."""
    expiration_date = date.fromisoformat(expiration_date_str)
    today = date.today()
    delta = expiration_date - today
    return delta.days


# Основной сценарий
if __name__ == "__main__":
    full_name = "Иванов Иван Иванович"
    system_name = "1С:Предприятие"
    status = "active"
    password = "qwerty123"
    expiration_date_str = "2026-12-31"

    login = generate_login(full_name)
    status_desc = get_status_description(status)
    password_strength = check_password_strength(password)
    access_message = check_access(system_name, status)
    days_left = days_until_expiration(expiration_date_str)

    print("=== Учетная запись ===")
    print(f"Пользователь: {full_name}")
    print(f"Логин: {login}")
    print(f"Система: {system_name}")
    print(f"Статус: {status_desc}")
    print(f"Пароль: {password_strength}")
    print(access_message)
    print(f"До истечения срока: {days_left} дн.")