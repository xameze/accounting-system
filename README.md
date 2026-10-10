# Система учета учетных записей организации

Консольное приложение для учета учетных записей сотрудников
в информационных системах организации. Реализовано на принципах ООП.

## Возможности

- просмотр и поиск пользователей;
- просмотр учетных записей с расшифровкой статуса;
- отбор учетных записей по статусу;
- просмотр скоро истекающих учетных записей;
- добавление пользователей, систем и учетных записей;
- блокировка и удаление учетных записей;
- хранение данных в JSON-файлах.

## Основные сущности

### User — пользователь организации
Атрибуты: `id`, `full_name`, `email`, `position`.
Методы:
- `__str__()` — строковое представление;
- `generate_login(full_name)` — @staticmethod, формирование логина;
- `validate_email(email)` — @staticmethod, проверка email;
- `email_domain` — @property, домен электронной почты;
- `from_data(data)` — @classmethod, создание из JSON;
- `to_dict()` — сериализация.

### System — информационная система
Атрибуты: `id`, `name`, `description`.
Методы:
- `__str__()`;
- `validate_name(name)` — @staticmethod;
- `from_data(data)` — @classmethod;
- `to_dict()`.

### Account — учетная запись
Атрибуты: `id`, `user` (объект `User`), `system` (объект `System`),
`login`, `status`, `created_at`, `expires_at`.
Методы:
- `__str__()`;
- `get_status_description()` — человекочитаемый статус;
- `check_access()` — проверка доступа по статусу;
- `days_until_expiration()` — дней до истечения;
- `block()` — блокировка;
- `check_password_strength(password)` — @staticmethod;
- `status_description` — @property;
- `from_data(data, users, systems)` — @classmethod;
- `to_dict()`.

**Взаимодействие объектов:** `Account` хранит ссылки на объекты
`User` и `System` (композиция). Это позволяет обращаться к данным
связанных объектов напрямую: `account.user.full_name`,
`account.system.name`.

## Структура проекта

- `main.py` — точка запуска, меню, вывод данных;
- `models/__init__.py` — экспорт классов пакета;
- `models/users.py` — класс `User` + функции работы с коллекцией;
- `models/systems.py` — класс `System` + функции работы;
- `models/accounts.py` — класс `Account` + функции работы;
- `storage.py` — загрузка/сохранение JSON с преобразованием в объекты;
- `utils.py` — безопасный ввод с обработкой исключений;
- `data/` — JSON-файлы данных;
- `tests/` — автоматизированные тесты pytest.

## Хранение данных

Данные хранятся в JSON:
- `data/users.json`;
- `data/systems.json`;
- `data/accounts.json`.

При загрузке JSON-словари преобразуются в объекты `User`, `System`,
`Account`. При сохранении объекты преобразуются обратно в JSON.
В `accounts.json` связи хранятся как `user_id` и `system_id`.

## Требования

- Python 3.10+;
- pytest;
- flake8.

Установка зависимостей:

    pip install -r requirements.txt

## Запуск программы

    python main.py

## Запуск тестов

    pytest -v

## Проверка качества кода

    flake8 .
