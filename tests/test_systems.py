"""Тесты класса System и функций работы с системами."""
from models import System
from models.systems import add_system, find_system, get_system_by_id


def test_system_creation():
    system = System(1, "1С:Предприятие", "Учет")
    assert system.id == 1
    assert system.name == "1С:Предприятие"


def test_from_data_classmethod():
    data = {"id": 3, "name": "CRM", "description": "Работа с клиентами"}
    system = System.from_data(data)
    assert system.id == 3
    assert system.name == "CRM"


def test_add_system():
    systems = []
    system = add_system(systems, "CRM", "Работа с клиентами")
    assert isinstance(system, System)
    assert systems[0].name == "CRM"


def test_find_system():
    systems = []
    add_system(systems, "1С:Предприятие", "Учет")
    add_system(systems, "CRM", "Клиенты")
    found = find_system(systems, "crm")
    assert len(found) == 1
    assert found[0].name == "CRM"


def test_get_system_by_id():
    systems = []
    add_system(systems, "1С", "Учет")
    assert get_system_by_id(systems, 1) is not None
    assert get_system_by_id(systems, 99) is None
