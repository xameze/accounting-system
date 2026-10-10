"""View-функции главной страницы и общий каркас HTML."""
from django.http import HttpResponse

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/"
    "bootstrap.min.css"
)


def page(title: str, content: str) -> str:
    """Единый каркас HTML-страницы с Bootstrap и навигацией."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
</head>
<body class="bg-light">
<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
    <div class="container">
        <a class="navbar-brand" href="/">Учётные записи</a>
        <div class="navbar-nav">
            <a class="nav-link" href="/users/">Пользователи</a>
            <a class="nav-link" href="/systems/">Системы</a>
            <a class="nav-link" href="/accounts/">Учётные записи</a>
        </div>
    </div>
</nav>
<div class="container">
    {content}
</div>
</body>
</html>"""


def index(request):
    """Главная страница."""
    content = """
    <h1 class="display-4">Система учёта учётных записей</h1>
    <p class="lead">Веб-версия приложения для учёта пользователей,
    информационных систем и учётных записей организации.</p>
    <a href="/users/" class="btn btn-primary me-2">Пользователи</a>
    <a href="/systems/" class="btn btn-secondary me-2">Системы</a>
    <a href="/accounts/" class="btn btn-success">Учётные записи</a>
    """
    return HttpResponse(page("Учётные записи — главная", content))


def page_not_found(request, exception):
    """Страница 404."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )
