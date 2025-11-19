from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),

    # gestão interna de usuários (ADMIN)
    path("usuarios/", views.usuario_list_view, name="usuario_list"),
    path("usuarios/novo/", views.usuario_create_view, name="usuario_create"),
    path("usuarios/<int:pk>/editar/", views.usuario_update_view, name="usuario_update"),
    path("usuarios/<int:pk>/", views.usuario_detail_view, name="usuario_detail"),
]
