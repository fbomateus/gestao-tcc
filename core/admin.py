from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informações pessoais", {"fields": ("nome_completo", "email", "tipo", "matricula", "area_atuacao")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("username", "nome_completo", "email", "tipo", "is_active")
    search_fields = ("username", "nome_completo", "email", "matricula")
    list_filter = ("tipo", "is_active", "date_joined")
