"""
URL configuration for tienda_online project.
"""

from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

api_v1_patterns = [
    path("api/v1/", include("users.urls")),
    path("api/v1/", include("products.urls")),
]

# Cambio 1: Configuración de Swagger con el nombre y descripción propios del proyecto Tienda Online
schema_view = get_schema_view(
    openapi.Info(
        title="Tienda Online API — Gestión de Usuarios, Productos y JWT",
        default_version="v1",
        description=(
            "API RESTful de Tienda Online (Unidad 3 - Práctica 4: Backend con Django, DRF, "
            "Modelo de Usuario Personalizado con Matrícula y Autenticación JWT)."
        ),
        terms_of_service="https://github.com/Lok-yo/tienda-online-django",
        contact=openapi.Contact(email="luis.leon@utslrc.edu.mx"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=api_v1_patterns,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redocs/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair_legacy"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh_legacy"),
    path("api/", include("products.urls")),
] + api_v1_patterns
