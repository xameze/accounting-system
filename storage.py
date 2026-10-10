"""Сохранение и загрузка данных проекта в JSON-файлах."""
import json
import os


def load_data(filename: str, default):
    """Загрузить данные из JSON-файла. При ошибке вернуть default."""
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
    """Сохранить данные в JSON-файл."""
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"[!] Ошибка записи в {filename}: {error}")
