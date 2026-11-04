from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "matricula",
        "carrera",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "carrera")
    search_fields = ("email", "username", "first_name", "last_name", "matricula")
    ordering = ("id",)

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Datos Académicos / Adicionales (UTSLRC)",
            {"fields": ("matricula", "carrera", "telefono")},
        ),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Datos Académicos / Adicionales (UTSLRC)",
            {"fields": ("email", "first_name", "last_name", "matricula", "carrera", "telefono")},
        ),
    )
