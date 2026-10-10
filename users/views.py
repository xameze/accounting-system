"""View-функции для пользователей."""
from django.http import HttpResponse

from homepage.views import page
from models.users import find_user_by_id
from storage import load_users

USERS_FILE = "data/users.json"


def users_list(request):
    """Страница со списком пользователей."""
    items = ""
    for user in load_users(USERS_FILE):
        text = f"{user.full_name} — {user.position}"
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between align-items-center">'
            f'<a href="/users/{user.id}/">{text}</a>'
            f'<span class="badge bg-secondary">{user.email}</span>'
            f'</li>'
        )
    content = f"""
    <h1>Пользователи</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Пользователи", content))


def user_detail(request, user_id: int):
    """Страница отдельного пользователя."""
    users = load_users(USERS_FILE)
    user = find_user_by_id(users, user_id)
    if user is None:
        content = """
        <h1 class="text-danger">Пользователь не найден</h1>
        <a href="/users/" class="btn btn-outline-secondary">
            ← к списку пользователей
        </a>
        """
        return HttpResponse(
            page("Пользователь не найден", content),
            status=404,
        )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{user.full_name}</h5>
            <p class="card-text"><strong>ID:</strong> {user.id}</p>
            <p class="card-text"><strong>Email:</strong> {user.email}</p>
            <p class="card-text"><strong>Должность:</strong>
                {user.position}</p>
            <p class="card-text"><strong>Домен:</strong>
                {user.email_domain}</p>
            <a href="/users/" class="btn btn-outline-secondary">
                ← к списку пользователей
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(user.full_name, content))
