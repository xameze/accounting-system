"""View-функции для учётных записей."""
from django.http import HttpResponse

from homepage.views import page
from models.accounts import find_account_by_id
from storage import (
    load_users, load_systems, load_accounts,
)

USERS_FILE = "data/users.json"
SYSTEMS_FILE = "data/systems.json"
ACCOUNTS_FILE = "data/accounts.json"


def accounts_list(request):
    """Страница со списком учётных записей."""
    users = load_users(USERS_FILE)
    systems = load_systems(SYSTEMS_FILE)
    accounts = load_accounts(ACCOUNTS_FILE, users, systems)

    items = ""
    for account in accounts:
        status = (
            "отменена" if account.status == "expired"
            else account.status_description
        )
        badge = (
            "bg-success" if account.status == "active"
            else "bg-warning text-dark" if account.status == "blocked"
            else "bg-secondary"
        )
        items += f"""
        <li class="list-group-item d-flex justify-content-between
                   align-items-center">
            <a href="/accounts/{account.id}/">
                {account.login} — {account.user.full_name}
                ({account.system.name})
            </a>
            <span class="badge {badge}">{status}</span>
        </li>
        """
    content = f"""
    <h1>Учётные записи</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Учётные записи", content))


def account_detail(request, account_id: int):
    """Страница отдельной учётной записи."""
    users = load_users(USERS_FILE)
    systems = load_systems(SYSTEMS_FILE)
    accounts = load_accounts(ACCOUNTS_FILE, users, systems)
    account = find_account_by_id(accounts, account_id)

    if account is None:
        content = """
        <h1 class="text-danger">Учётная запись не найдена</h1>
        <a href="/accounts/" class="btn btn-outline-secondary">
            ← к списку учётных записей
        </a>
        """
        return HttpResponse(
            page("Учётная запись не найдена", content),
            status=404,
        )

    status = account.status_description
    badge = (
        "bg-success" if account.status == "active"
        else "bg-warning text-dark" if account.status == "blocked"
        else "bg-secondary"
    )
    days = account.days_until_expiration()
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Логин: {account.login}</h5>
            <p class="card-text"><strong>ID:</strong> {account.id}</p>
            <p class="card-text"><strong>Пользователь:</strong>
                {account.user.full_name}</p>
            <p class="card-text"><strong>Система:</strong>
                {account.system.name}</p>
            <p class="card-text"><strong>Дата создания:</strong>
                {account.created_at}</p>
            <p class="card-text"><strong>Истекает:</strong>
                {account.expires_at} (осталось {days} дн.)</p>
            <p class="card-text"><strong>Статус:</strong>
                <span class="badge {badge}">{status}</span></p>
            <p class="card-text">{account.check_access()}</p>
            <a href="/accounts/" class="btn btn-outline-secondary">
                ← к списку учётных записей
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Учётная запись {account.login}", content))
