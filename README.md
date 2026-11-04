# Tienda Online API — Backend con Django, DRF y JWT

Proyecto de **Desarrollo para Dispositivos Inteligentes** (IDGS 9-2 — UTSLRC).
API RESTful construida con **Django 6.1**, **Django REST Framework**, **SimpleJWT** y **Swagger (`drf-yasg`)**.

## Características principales (Unidad 3 - Práctica 4)

1. **Documentación interactiva con Swagger (`drf-yasg`)**:
   - Disponible en `/swagger/` y `/redocs/` con título y descripción propios del proyecto (`Tienda Online API — Gestión de Usuarios, Productos y JWT`).
2. **Modelo de Usuario Personalizado (`users.User`)**:
   - Autenticación por correo electrónico (`USERNAME_FIELD = 'email'`).
   - Campos adicionales: `matricula`, `carrera` y `telefono`.
3. **Autenticación JWT (`djangorestframework-simplejwt`)**:
   - `ACCESS_TOKEN_LIFETIME` configurado a `timedelta(minutes=60)`.
   - Endpoints:
     - `POST /api/v1/auth/token/` — Obtención de tokens `access` y `refresh`.
     - `POST /api/v1/auth/token/refresh/` — Renovación de token de acceso.
     - `GET /api/v1/auth/me/` — Datos personales del usuario autenticado.
4. **Correcciones de Seguridad en `UserSerializer` y `UserApiViewSet`**:
   - `password` configurado como `write_only=True` para jamás exponer el hash de la contraseña en las respuestas JSON.
   - Al actualizar un usuario (`PUT`/`PATCH /api/v1/users/{id}/`) sin enviar el campo `password`, se conserva la contraseña original del usuario editado y **nunca** se sobrescribe con `request.user.password`.

## Instalación local

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
