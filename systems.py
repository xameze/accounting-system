"""Функции работы со справочником информационных систем."""


def add_system(systems: list[dict], name: str, description: str) -> None:
    """Добавить систему в список systems."""
    new_id = max((s["id"] for s in systems), default=0) + 1
    systems.append({
        "id": new_id,
        "name": name,
        "description": description,
    })


def find_system(systems: list[dict], query: str) -> list[dict]:
    """Найти системы по подстроке в названии."""
    query_lower = query.lower()
    result = []
    for system in systems:
        if query_lower in system["name"].lower():
            result.append(system)
    return result


def get_system_by_id(systems: list[dict], system_id: int) -> dict | None:
    """Вернуть систему по id или None."""
    for system in systems:
        if system["id"] == system_id:
            return system
    return None


def get_system_name(systems: list[dict], system_id: int) -> str:
    """Вернуть название системы или заглушку, если системы нет."""
    system = get_system_by_id(systems, system_id)
    if system is None:
        return "Неизвестная система"
    return system["name"]
