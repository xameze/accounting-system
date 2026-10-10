"""View-функции для информационных систем."""
from django.http import HttpResponse

from homepage.views import page
from models.systems import find_system_by_id
from storage import load_systems

SYSTEMS_FILE = "data/systems.json"


def systems_list(request):
    """Страница со списком систем."""
    items = ""
    for system in load_systems(SYSTEMS_FILE):
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between align-items-center">'
            f'<a href="/systems/{system.id}/">{system.name}</a>'
            f'<span class="text-muted">{system.description}</span>'
            f'</li>'
        )
    content = f"""
    <h1>Информационные системы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Информационные системы", content))


def system_detail(request, system_id: int):
    """Страница отдельной системы."""
    systems = load_systems(SYSTEMS_FILE)
    system = find_system_by_id(systems, system_id)
    if system is None:
        content = """
        <h1 class="text-danger">Система не найдена</h1>
        <a href="/systems/" class="btn btn-outline-secondary">
            ← к списку систем
        </a>
        """
        return HttpResponse(
            page("Система не найдена", content),
            status=404,
        )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{system.name}</h5>
            <p class="card-text"><strong>ID:</strong> {system.id}</p>
            <p class="card-text"><strong>Описание:</strong>
                {system.description}</p>
            <a href="/systems/" class="btn btn-outline-secondary">
                ← к списку систем
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(system.name, content))
