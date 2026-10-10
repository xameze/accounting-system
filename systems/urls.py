from django.urls import path
from . import views

urlpatterns = [
    path("", views.systems_list, name="systems_list"),
    path("<int:system_id>/", views.system_detail, name="system_detail"),
]
