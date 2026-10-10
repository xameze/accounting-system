from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("users/", include("users.urls")),
    path("systems/", include("systems.urls")),
    path("accounts/", include("accounts.urls")),
]

handler404 = "homepage.views.page_not_found"
