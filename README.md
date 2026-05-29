# BasketShop — Práctica 2: Backend Python con FastAPI

Backend reescrito íntegramente en **Python / FastAPI** con arquitectura limpia en capas,
autenticación JWT y persistencia en **SQLite** mediante **SQLAlchemy**.
El frontend en **Svelte 5** de la práctica anterior se conecta sin cambios en su lógica.

---

## Estructura del proyecto

```
BasketShop2/
├── backend/
│   ├── app/
│   │   ├── main.py               # Punto de entrada, CORS y manejadores globales
│   │   ├── config.py             # Configuración centralizada (pydantic-settings)
│   │   ├── database.py           # Motor SQLAlchemy y sesión
│   │   ├── exceptions.py         # Excepciones de dominio personalizadas
│   │   ├── models/               # Modelos ORM (User, Producto, CartItem)
│   │   ├── schemas/              # Esquemas Pydantic (validación de entrada/salida)
│   │   ├── repositories/         # Acceso a datos (patrón repositorio)
│   │   ├── services/             # Lógica de negocio
│   │   ├── routers/              # Controladores HTTP (auth, users, productos, cart)
│   │   └── dependencies/         # Dependencias FastAPI (autenticación JWT)
│   ├── uploads/                  # Imágenes subidas por el admin
│   ├── requirements.txt
│   ├── seed.py                   # Script de datos iniciales
│   └── .env.example
└── frontend/                     # Frontend Svelte 5 (práctica 1, sin cambios)
```

---

## Requisitos previos

- **Python 3.10+**
- **Node.js 18+** (para el frontend)

---

## Instalación y ejecución

### 1. Backend (FastAPI)

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate
# Activar (Linux/macOS)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# (Opcional) Cargar usuarios y productos de ejemplo
python seed.py

# Arrancar el servidor en http://localhost:8000
uvicorn app.main:app --reload --port 8000
```

> La base de datos SQLite (`basketshop.db`) se crea automáticamente al iniciar.

### 2. Frontend (Svelte 5)

```bash
cd frontend
npm install
npm run dev
```

Accede en **http://localhost:5173**. El Vite proxy redirige `/api` → `http://localhost:8000`.

---

## Credenciales por defecto (tras ejecutar seed.py)

| Usuario | Contraseña | Rol   |
|---------|-----------|-------|
| admin   | admin123  | admin |
| user    | user123   | user  |

---

## Endpoints principales

### Autenticación
| Método | Ruta           | Auth | Descripción          |
|--------|----------------|------|----------------------|
| POST   | /api/login     | —    | Obtener token JWT    |
| POST   | /api/register  | —    | Registrar usuario    |

### Productos
| Método | Ruta                  | Auth   | Descripción              |
|--------|-----------------------|--------|--------------------------|
| GET    | /api/productos        | —      | Listar (filtra con ?name=)|
| POST   | /api/productos        | Admin  | Crear (multipart/form-data)|
| PUT    | /api/productos/{id}   | Admin  | Actualizar (JSON)        |
| DELETE | /api/productos/{id}   | Admin  | Eliminar                 |

### Usuarios (solo admin)
| Método | Ruta              | Auth  | Descripción   |
|--------|-------------------|-------|---------------|
| GET    | /api/users        | Admin | Listar        |
| POST   | /api/users        | Admin | Crear         |
| PUT    | /api/users/{id}   | Admin | Actualizar    |
| DELETE | /api/users/{id}   | Admin | Eliminar      |

### Carrito (usuario autenticado)
| Método | Ruta                    | Auth | Descripción          |
|--------|-------------------------|------|----------------------|
| GET    | /api/cart               | User | Ver carrito          |
| POST   | /api/cart/add           | User | Añadir producto      |
| DELETE | /api/cart/{product_id}  | User | Quitar producto      |

---

## Documentación interactiva

FastAPI genera Swagger UI automáticamente en:
- **http://localhost:8000/docs**

---

## Variables de entorno

Copia `.env.example` a `.env` y ajusta los valores:

```
SECRET_KEY=cambia-esto-por-una-clave-secreta-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./basketshop.db
UPLOAD_DIR=uploads
```
