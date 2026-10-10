"""Вспомогательные функции безопасного ввода."""
from datetime import date


def input_str(prompt: str) -> str:
    """Запросить у пользователя непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Значение не может быть пустым. Попробуйте снова.")


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Некорректный ввод. Введите целое число.")


def input_date(prompt: str) -> str:
    """Запросить дату в формате ГГГГ-ММ-ДД и проверить её."""
    while True:
        value = input(prompt).strip()
        try:
            date.fromisoformat(value)
            return value
        except ValueError:
            print("Некорректная дата. Используйте формат ГГГГ-ММ-ДД.")


def input_status(prompt: str) -> str:
    """Запросить статус из допустимого набора."""
    allowed = ("active", "blocked", "expired")
    while True:
        value = input(prompt).strip().lower()
        if value in allowed:
            return value
        print(f"Допустимые статусы: {', '.join(allowed)}")
