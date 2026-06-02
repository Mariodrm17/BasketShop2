# Memoria de uso de Inteligencia Artificial — Práctica 2

**Asignatura:** Programación Web II  
**Alumno:** Mario Del Río Merino  
**Fecha:** Mayo 2026

---

## Endpoints del backend y roles necesarios

A continuación se indican los endpoints implementados y el nivel de acceso requerido en cada uno:

| Método | Ruta | Rol mínimo | Descripción |
|--------|------|-----------|-------------|
| POST | /api/login | Público | Autenticación, devuelve JWT |
| POST | /api/register | Público | Registro de nuevo usuario (rol: user) |
| GET | /api/productos | Público | Listado de productos (filtrable por ?name=) |
| POST | /api/productos | Admin | Crear producto (multipart/form-data con imagen) |
| PUT | /api/productos/{id} | Admin | Editar producto (JSON) |
| DELETE | /api/productos/{id} | Admin | Eliminar producto |
| GET | /api/users | Admin | Listar todos los usuarios |
| POST | /api/users | Admin | Crear usuario con rol a elección |
| PUT | /api/users/{id} | Admin | Editar usuario |
| DELETE | /api/users/{id} | Admin | Eliminar usuario |
| GET | /api/cart | User/Admin | Ver carrito del usuario autenticado |
| POST | /api/cart/add | User/Admin | Añadir producto al carrito |
| DELETE | /api/cart/{product_id} | User/Admin | Quitar producto del carrito |
| POST | /api/orders/checkout | User/Admin | Finalizar compra — crea pedido y vacía el carrito |
| GET | /api/orders/my | User/Admin | Historial de pedidos del usuario autenticado |
| GET | /api/orders | Admin | Listar todos los pedidos de la plataforma |
| GET | /api/productos/{id} | Público | Obtener un producto individual por ID |
| GET | /api/me | User/Admin | Perfil del usuario autenticado vía JWT |
| GET | /api/health | Público | Estado del servidor y conexión a base de datos |

---

## Introducción

Durante el desarrollo de esta práctica recurrí a ChatGPT en tres momentos concretos en los que me encontré con dudas específicas sobre la sintaxis de librerías que no había usado antes. La arquitectura del proyecto (capas de routers, services y repositories), el diseño de los modelos y la lógica de negocio fueron trabajo propio, basado en los contenidos vistos en clase.

El uso de la IA fue siempre puntual: resolver una duda de sintaxis, obtener un ejemplo de referencia o aclarar cómo funciona una API concreta. En ningún caso se delegó el diseño ni la integración del sistema.

---

## Registro de prompts e iteraciones

### Prompt 1 — Generación de tokens JWT con python-jose

**Contexto:** Sabía que necesitaba JWT para proteger las rutas (visto en clase), pero nunca había usado la librería `python-jose` en Python. Necesitaba saber cómo crear el token con el payload adecuado y la expiración.

**Prompt enviado a ChatGPT:**

> Estoy haciendo un backend con FastAPI y necesito generar un token JWT usando la librería python-jose. El token tiene que incluir el id del usuario, su username y su rol, y debe expirar en 1 hora. ¿Cómo sería la función para crear el token y la función para verificarlo?

**Respuesta obtenida:**

La IA me dio un ejemplo funcional con `jwt.encode` y `jwt.decode`. Sin embargo, el código incluía un error de seguridad grave que detecté al revisarlo (documentado en la sección de análisis crítico). Tomé la estructura general de llamada a `jwt.encode` como referencia, pero modifiqué el payload y la gestión de fechas antes de incorporar el código.

---

### Prompt 2 — Validadores personalizados con Pydantic v2 (con refinamiento)

**Contexto:** Necesitaba validar los datos de entrada: que el username tuviera al menos 3 caracteres, que el precio no fuera negativo, y que la categoría fuera uno de los valores permitidos. Quería hacerlo con Pydantic para que FastAPI devolviera automáticamente un 422 bien formateado.

**Primer prompt (resultado no satisfactorio):**

> ¿Cómo valido los campos de un modelo en FastAPI con Pydantic?

**Problema con la primera respuesta:**

La IA generó código con `@validator`, que es la sintaxis de **Pydantic v1**:

```python
# Código incorrecto generado con el primer prompt (Pydantic v1)
from pydantic import BaseModel, validator

class ProductoCreate(BaseModel):
    nombre: str
    precio: float

    @validator('precio')
    def precio_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('El precio no puede ser negativo')
        return v
```

Al ejecutarlo con Pydantic v2 (que es la versión que instala FastAPI moderno), este código lanza un error en tiempo de arranque:

```
PydanticUserError: The `validator` decorator is deprecated. Use `field_validator` instead.
```

El prompt era demasiado genérico y la IA respondió con la sintaxis más común en sus datos de entrenamiento (v1), que ya está deprecada.

**Prompt refinado:**

> Estoy usando Pydantic v2 con FastAPI. Necesito crear validadores de campo personalizados para comprobar que un string no esté vacío y que un número float sea positivo. Sé que en Pydantic v1 se usaba @validator pero entiendo que en v2 cambió. ¿Cuál es la forma correcta con @field_validator en v2?

**Resultado con el prompt refinado:**

La IA generó código correcto con `@field_validator` y `@classmethod`, que es la sintaxis actual de Pydantic v2:

```python
from pydantic import BaseModel, field_validator

class ProductoCreate(BaseModel):
    nombre: str
    precio: float

    @field_validator('precio')
    @classmethod
    def precio_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError('El precio no puede ser negativo')
        return v
```

Este sí funcionó correctamente y lo adapté para todos mis schemas.

---

### Prompt 3 — Relación many-to-one en SQLAlchemy 2.0 para el carrito

**Contexto:** Diseñé el modelo `CartItem` con los campos `user_id`, `product_id` y `quantity`. Al recuperar los items del carrito necesitaba que el producto completo estuviera disponible (el frontend espera un objeto `productId` con todos los datos del producto, no solo el ID). Quería saber cómo definir la relación para que SQLAlchemy lo cargara automáticamente.

**Prompt enviado:**

> En SQLAlchemy 2.0 tengo un modelo CartItem con una clave foránea product_id que apunta a la tabla productos. Cuando hago una query de CartItem quiero que el objeto producto relacionado se cargue automáticamente (eager loading) sin tener que hacer una segunda consulta manual. ¿Cómo se define el relationship() para esto?

**Resultado obtenido:**

La IA explicó la diferencia entre `lazy="select"` (carga lazy, hace N queries) y `lazy="joined"` (carga eager con JOIN, una sola query). Lo usé tal cual porque se ajustaba exactamente a mi caso: el carrito siempre necesita los datos del producto, por lo que `lazy="joined"` era la opción correcta para evitar el problema de N+1 queries.

---

## Análisis crítico: error detectado en la IA

### Descripción del problema

En el Prompt 1 (JWT con python-jose), la IA generó la siguiente función de creación de token:

```python
# Código generado por la IA — contiene error de seguridad
def create_access_token(user) -> str:
    payload = {
        "id": str(user.id),
        "username": user.username,
        "role": user.role,
        "password": user.password,   # ← ERROR GRAVE
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

### Por qué es incorrecto

El código tiene **dos problemas**:

**1. Incluir el hash de la contraseña en el payload del JWT (error de seguridad grave)**

Un token JWT está compuesto por tres partes separadas por puntos, codificadas en **Base64**. Base64 no es cifrado: cualquier persona que tenga el token puede decodificarlo directamente con una herramienta online o con `base64 -d` en la terminal y ver todo el contenido del payload en texto plano.

Si el hash de la contraseña viaja en el token, se expone a cualquiera que intercepte o acceda al token (localStorage del navegador, logs del servidor, proxies intermedios). Aunque bcrypt no es reversible directamente, tener el hash facilita ataques de diccionario offline sin necesidad de interactuar con el servidor.

En clase se insistió en que el payload de un JWT solo debe contener la **información mínima necesaria** para identificar al usuario y gestionar sus permisos: en este caso, id, username y role. La contraseña (ni siquiera su hash) tiene ningún sentido en el token.

**2. `datetime.utcnow()` está deprecado en Python 3.12**

La función `datetime.utcnow()` devuelve un objeto `datetime` sin información de zona horaria (*naive*). A partir de Python 3.12 esto genera un `DeprecationWarning` porque mezclar fechas naive y aware puede producir comparaciones incorrectas. La forma correcta es `datetime.now(timezone.utc)`, que devuelve un objeto *aware* con zona horaria UTC explícita, garantizando compatibilidad con python-jose en cualquier entorno.

### Corrección aplicada

```python
# Código corregido manualmente
from datetime import datetime, timedelta, timezone

def create_access_token(data: dict) -> str:
    payload = data.copy()
    # Solo id, username y role — sin datos sensibles
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload["exp"] = expire
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Al llamarla, se construye el payload explícitamente:
token = create_access_token({
    "id": str(user.id),
    "username": user.username,
    "role": user.role
    # password: NO se incluye
})
```

Este ejemplo ilustra bien por qué el código generado por IA no puede usarse sin revisión crítica: la IA reproduce patrones de código que encuentra en su entrenamiento, pero no siempre razona sobre las implicaciones de seguridad de incluir ciertos datos. La revisión manual aplicando los criterios de seguridad vistos en clase fue imprescindible para detectar y corregir este error antes de que llegara a producción.

---

## Reflexión final

El uso de IA en esta práctica se limitó a tres consultas puntuales sobre la API de librerías específicas (`python-jose`, `Pydantic v2`, `SQLAlchemy 2.0`), de forma similar a consultar la documentación oficial pero con respuesta más inmediata. El diseño de la arquitectura en capas, la definición de los modelos, la lógica de negocio y la integración con el frontend de la práctica anterior fueron trabajo completamente propio.

La principal conclusión es que la IA es útil como referencia rápida de sintaxis, pero requiere una revisión crítica activa: en los tres casos tuve que modificar el código generado, y en el primero era necesario corregir un error de seguridad que habría comprometido la aplicación si hubiera pasado desapercibido.
