# Tienda Online — Full Stack Django + React con Autenticación JWT, API de Terceros y SOAP

Proyecto de **Desarrollo Web Integral (DWI)** — **IDGS 9-2 (UTSLRC)**  
**Profesor:** Jose Julian Reyes Patiño  
**Alumno:** Luis Angel Leon Almazan (`23304031`)

---

## Arquitectura del Monorepo (Resultado de Aprendizaje Unidad 2 y 3)

- **`/` (Backend en Django 6.1 + DRF + SimpleJWT + Zeep SOAP + Swagger)**:
  - `users/`: Modelo de usuario personalizado (`USERNAME_FIELD = 'email'`, campos `matricula`, `carrera`, `telefono`), autenticación JWT (`/api/v1/auth/token/`), perfil protegido (`GET /api/v1/auth/me/`), registro público (`POST /api/v1/auth/register/`) y consumo de servicio SOAP (`GET /api/v1/soap/country/?code=MX`).
  - `products/`: CRUD de Categorías y Productos con cálculo de precio final.
  - `tienda_online/`: Configuración del proyecto, CORS (`django-cors-headers`), `SIMPLE_JWT` y documentación interactiva Swagger (`/swagger/`).
- **`frontend/` (Frontend en React 18 + Vite + React Router v6 + Semantic UI + Formik/Yup)**:
  - `src/routes/`: Sistema de rutas divididas en `routes.admin.jsx`, `routes.client.jsx`, `routes.common.jsx` y `Navigation.jsx`.
  - `src/layouts/`: `AdminLayout.jsx` (protegido por sesión JWT), `ClientLayout.jsx` y `CommonLayout.jsx`.
  - `src/context/AuthContext.jsx` y `src/hooks/useAuth.jsx`: Persistencia de sesión con `localStorage` y carga automática de `/api/v1/auth/me/`.
  - `src/pages/common/`: Pantallas de `Login.jsx`, `Register.jsx` y `Error404.jsx`.
  - `src/pages/admin/Dashboard.jsx`: Pantalla protegida que muestra los datos del usuario autenticado (`AuthContext`), un widget de API de terceros con `fetch` (**Open-Meteo Weather API** + **DummyJSON Quotes API**) y un visor interactivo del servicio **SOAP (`zeep`)**.

---

## Instrucciones de Instalación y Ejecución

### 1. Backend (Django + MySQL + JWT + SOAP)

```bash
# 1. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate

# 2. Instalar dependencias (incluye Django, DRF, SimpleJWT, drf-yasg, corsheaders y zeep)
pip install -r requirements.txt

# 3. Aplicar migraciones y ejecutar pruebas automatizadas
python manage.py migrate
python manage.py test

# 4. Iniciar servidor en http://127.0.0.1:8000
python manage.py runserver
```

### 2. Frontend (React + Vite)

```bash
# 1. Entrar al directorio del frontend
cd frontend

# 2. Copiar variables de entorno e instalar paquetes npm
cp .env.example .env
npm install

# 3. Iniciar servidor de desarrollo en http://127.0.0.1:5173
npm run dev
```

---

## Endpoints Principales

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `POST` | `/api/v1/auth/token/` | Obtiene tokens JWT (`access` y `refresh`) con `email` y `password` |
| `POST` | `/api/v1/auth/register/` | Registro público de nuevos usuarios con hash PBKDF2 |
| `GET` | `/api/v1/auth/me/` | Web Service propio protegido con JWT (`Bearer <token>`) |
| `GET` | `/api/v1/soap/country/?code=MX` | Consume el servicio SOAP `CountryInfoService.wso?WSDL` usando `zeep` |
| `GET` | `/swagger/` | Documentación interactiva OpenAPI / Swagger UI |
