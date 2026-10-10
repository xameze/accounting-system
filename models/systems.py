"""Класс System и функции работы со справочником систем."""
from typing import List, Optional


class System:
    """Информационная система организации."""

    def __init__(self, system_id: int, name: str, description: str) -> None:
        self.id = system_id
        self.name = name
        self.description = description

    def __str__(self) -> str:
        return f"[{self.id}] {self.name}"

    @staticmethod
    def validate_name(name: str) -> bool:
        """Название системы не должно быть пустым."""
        return bool(name and name.strip())

    @classmethod
    def from_data(cls, data: dict) -> "System":
        """Создать систему из набора данных JSON."""
        return cls(
            system_id=data["id"],
            name=data["name"],
            description=data["description"],
        )

    def to_dict(self) -> dict:
        """Преобразовать объект в структуру для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }


# ---------- Функции обработки коллекции объектов System ----------

def add_system(systems: List[System], name: str,
               description: str) -> System:
    """Создать объект System и добавить в коллекцию."""
    new_id = max((s.id for s in systems), default=0) + 1
    system = System(new_id, name, description)
    systems.append(system)
    return system


def find_system(systems: List[System], query: str) -> List[System]:
    """Найти системы по подстроке в названии."""
    query_lower = query.lower()
    return [
        system for system in systems
        if query_lower in system.name.lower()
    ]


def get_system_by_id(systems: List[System],
                     system_id: int) -> Optional[System]:
    """Вернуть систему по id или None."""
    for system in systems:
        if system.id == system_id:
            return system
    return None
def find_system_by_id(systems: List[System],
                      system_id: int) -> Optional[System]:
    """Найти систему по идентификатору."""
    for system in systems:
        if system.id == system_id:
            return system
    return None
