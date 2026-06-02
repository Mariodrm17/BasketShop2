from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

style_normal = doc.styles["Normal"]
style_normal.font.name = "Calibri"
style_normal.font.size = Pt(11)

for i in range(1, 4):
    h = doc.styles[f"Heading {i}"]
    h.font.name = "Calibri"
    h.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

# ── Portada ──────────────────────────────────────────────────────────────────
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Memoria de uso de Inteligencia Artificial")
run.bold = True
run.font.size = Pt(18)
run.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

doc.add_paragraph()

for label, value in [
    ("Asignatura", "Programación Web II"),
    ("Alumno", "Mario Del Río Merino"),
    ("Fecha", "Mayo 2026"),
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"{label}: "); r.bold = True; r.font.size = Pt(12)
    p.add_run(value).font.size = Pt(12)

doc.add_page_break()

# ── 1. Endpoints ─────────────────────────────────────────────────────────────
doc.add_heading("Endpoints del backend y roles necesarios", 1)

endpoints = [
    ("POST",   "/api/login",              "Público",     "Autenticación, devuelve JWT"),
    ("POST",   "/api/register",           "Público",     "Registro de nuevo usuario (rol: user)"),
    ("GET",    "/api/productos",          "Público",     "Listado de productos (filtrable por ?name=)"),
    ("GET",    "/api/productos/{id}",     "Público",     "Obtener un producto individual por ID"),
    ("POST",   "/api/productos",          "Admin",       "Crear producto (multipart/form-data con imagen)"),
    ("PUT",    "/api/productos/{id}",     "Admin",       "Editar producto (JSON)"),
    ("DELETE", "/api/productos/{id}",     "Admin",       "Eliminar producto"),
    ("GET",    "/api/users",              "Admin",       "Listar todos los usuarios"),
    ("POST",   "/api/users",              "Admin",       "Crear usuario con rol a elección"),
    ("PUT",    "/api/users/{id}",         "Admin",       "Editar usuario"),
    ("DELETE", "/api/users/{id}",         "Admin",       "Eliminar usuario"),
    ("GET",    "/api/me",                 "User/Admin",  "Perfil del usuario autenticado vía JWT"),
    ("GET",    "/api/cart",               "User/Admin",  "Ver carrito del usuario autenticado"),
    ("POST",   "/api/cart/add",           "User/Admin",  "Añadir producto al carrito"),
    ("DELETE", "/api/cart/{product_id}",  "User/Admin",  "Quitar producto del carrito"),
    ("POST",   "/api/orders/checkout",    "User/Admin",  "Finalizar compra — crea pedido y vacía el carrito"),
    ("GET",    "/api/orders/my",          "User/Admin",  "Historial de pedidos del usuario autenticado"),
    ("GET",    "/api/orders",             "Admin",       "Listar todos los pedidos de la plataforma"),
    ("GET",    "/api/health",             "Público",     "Estado del servidor y conexión a base de datos"),
]

table = doc.add_table(rows=1, cols=4)
table.style = "Table Grid"
for i, txt in enumerate(["Método", "Ruta", "Rol mínimo", "Descripción"]):
    hdr = table.rows[0].cells[i]
    hdr.text = txt
    for para in hdr.paragraphs:
        for run in para.runs:
            run.bold = True

for row_data in endpoints:
    row = table.add_row().cells
    for i, val in enumerate(row_data):
        row[i].text = val

doc.add_paragraph()

# ── 2. Introducción ───────────────────────────────────────────────────────────
doc.add_heading("Introducción", 1)
doc.add_paragraph(
    "Durante el desarrollo de esta práctica recurrí a ChatGPT en tres momentos concretos "
    "en los que me encontré con dudas específicas sobre la sintaxis de librerías que no había "
    "usado antes. La arquitectura del proyecto (capas de routers, services y repositories), "
    "el diseño de los modelos y la lógica de negocio fueron trabajo propio, basado en los "
    "contenidos vistos en clase.\n\n"
    "El uso de la IA fue siempre puntual: resolver una duda de sintaxis, obtener un ejemplo "
    "de referencia o aclarar cómo funciona una API concreta. En ningún caso se delegó el "
    "diseño ni la integración del sistema."
)

# ── 3. Prompts ────────────────────────────────────────────────────────────────
doc.add_heading("Registro de prompts e iteraciones", 1)

# -- Prompt 1 -----------------------------------------------------------------
doc.add_heading("Prompt 1 — Generación de tokens JWT con python-jose", 2)
doc.add_paragraph(
    "Contexto: Sabía que necesitaba JWT para proteger las rutas (visto en clase), pero nunca "
    "había usado la librería python-jose en Python. Necesitaba saber cómo crear el token con "
    "el payload adecuado y la expiración."
)
doc.add_paragraph().add_run("Prompt enviado a ChatGPT:").bold = True
doc.add_paragraph(
    "Estoy haciendo un backend con FastAPI y necesito generar un token JWT usando la librería "
    "python-jose. El token tiene que incluir el id del usuario, su username y su rol, y debe "
    "expirar en 1 hora. ¿Cómo sería la función para crear el token y la función para verificarlo?"
)
doc.add_paragraph(
    "La IA me dio un ejemplo funcional con jwt.encode y jwt.decode. Sin embargo, el código "
    "incluía un error de seguridad grave que detecté al revisarlo (documentado en la sección "
    "de análisis crítico). Tomé la estructura general como referencia, pero modifiqué el "
    "payload y la gestión de fechas antes de incorporar el código."
)

# -- Prompt 2 -----------------------------------------------------------------
doc.add_heading("Prompt 2 — Validadores personalizados con Pydantic v2 (con refinamiento)", 2)
doc.add_paragraph(
    "Contexto: Necesitaba validar los datos de entrada: que el username tuviera al menos "
    "3 caracteres, que el precio no fuera negativo, y que la categoría fuera uno de los "
    "valores permitidos. Quería hacerlo con Pydantic para que FastAPI devolviera "
    "automáticamente un 422 bien formateado."
)
doc.add_paragraph().add_run("Primer prompt (resultado no satisfactorio):").bold = True
doc.add_paragraph("¿Cómo valido los campos de un modelo en FastAPI con Pydantic?")
doc.add_paragraph().add_run("Problema con la primera respuesta:").bold = True
doc.add_paragraph(
    "La IA generó código con @validator, que es la sintaxis de Pydantic v1. Al ejecutarlo "
    "con Pydantic v2 lanza error en tiempo de arranque:\n"
    "    PydanticUserError: The `validator` decorator is deprecated. Use `field_validator` instead.\n\n"
    "El prompt era demasiado genérico y la IA respondió con la sintaxis más común en sus "
    "datos de entrenamiento (v1), ya deprecada."
)
doc.add_paragraph().add_run("Prompt refinado:").bold = True
doc.add_paragraph(
    "Estoy usando Pydantic v2 con FastAPI. Necesito crear validadores de campo personalizados "
    "para comprobar que un string no esté vacío y que un número float sea positivo. Sé que en "
    "Pydantic v1 se usaba @validator pero entiendo que en v2 cambió. ¿Cuál es la forma correcta "
    "con @field_validator en v2?"
)
doc.add_paragraph(
    "La IA generó código correcto con @field_validator y @classmethod (sintaxis actual de "
    "Pydantic v2). Lo adapté para todos los schemas del proyecto."
)

# -- Prompt 3 -----------------------------------------------------------------
doc.add_heading("Prompt 3 — Relación many-to-one en SQLAlchemy 2.0 para el carrito", 2)
doc.add_paragraph(
    "Contexto: Diseñé el modelo CartItem con los campos user_id, product_id y quantity. "
    "Al recuperar los items del carrito necesitaba que el producto completo estuviera "
    "disponible (el frontend espera un objeto productId con todos los datos del producto, "
    "no solo el ID)."
)
doc.add_paragraph().add_run("Prompt enviado:").bold = True
doc.add_paragraph(
    "En SQLAlchemy 2.0 tengo un modelo CartItem con una clave foránea product_id que apunta "
    "a la tabla productos. Cuando hago una query de CartItem quiero que el objeto producto "
    "relacionado se cargue automáticamente (eager loading) sin tener que hacer una segunda "
    "consulta manual. ¿Cómo se define el relationship() para esto?"
)
doc.add_paragraph(
    "La IA explicó la diferencia entre lazy='select' (carga lazy, N queries) y lazy='joined' "
    "(carga eager con JOIN, una sola query). Usé lazy='joined' porque el carrito siempre "
    "necesita los datos del producto, eliminando el problema de N+1 queries."
)

# ── 4. Análisis crítico ───────────────────────────────────────────────────────
doc.add_heading("Análisis crítico: error detectado en la IA", 1)
doc.add_heading("Descripción del problema", 2)
doc.add_paragraph(
    "En el Prompt 1 (JWT con python-jose), la IA generó la siguiente función:"
)
code1 = (
    "# Código generado por la IA — contiene errores\n"
    "def create_access_token(user) -> str:\n"
    "    payload = {\n"
    '        "id": str(user.id),\n'
    '        "username": user.username,\n'
    '        "role": user.role,\n'
    '        "password": user.password,   # ERROR GRAVE\n'
    '        "exp": datetime.utcnow() + timedelta(hours=1)  # DEPRECADO\n'
    "    }\n"
    '    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")'
)
p = doc.add_paragraph(code1)
p.runs[0].font.name = "Courier New"
p.runs[0].font.size = Pt(9)

doc.add_heading("Por qué es incorrecto", 2)
doc.add_paragraph().add_run("1. Incluir el hash de la contraseña en el payload del JWT (error de seguridad grave)").bold = True
doc.add_paragraph(
    "Un token JWT está codificado en Base64, no cifrado. Cualquier persona con el token puede "
    "decodificarlo directamente y ver el contenido en texto plano. Si el hash de la contraseña "
    "viaja en el token, se expone a ataques de diccionario offline sin necesidad de interactuar "
    "con el servidor. El payload del JWT solo debe contener la información mínima necesaria: "
    "id, username y role."
)
doc.add_paragraph().add_run("2. datetime.utcnow() está deprecado en Python 3.12").bold = True
doc.add_paragraph(
    "La función datetime.utcnow() devuelve un objeto datetime sin zona horaria (naive). "
    "A partir de Python 3.12 genera DeprecationWarning. La forma correcta es "
    "datetime.now(timezone.utc), que devuelve un objeto aware con UTC explícito."
)

doc.add_heading("Corrección aplicada", 2)
code2 = (
    "# Código corregido manualmente\n"
    "from datetime import datetime, timedelta, timezone\n\n"
    "def create_access_token(data: dict) -> str:\n"
    "    payload = data.copy()\n"
    "    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)\n"
    "    payload['exp'] = expire\n"
    "    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)\n\n"
    "# Al llamarla, el payload solo incluye lo necesario:\n"
    'token = create_access_token({"id": str(user.id), "username": user.username, "role": user.role})'
)
p = doc.add_paragraph(code2)
p.runs[0].font.name = "Courier New"
p.runs[0].font.size = Pt(9)

doc.add_paragraph(
    "Este ejemplo ilustra por qué el código generado por IA no puede usarse sin revisión "
    "crítica: la IA reproduce patrones de su entrenamiento pero no razona sobre las "
    "implicaciones de seguridad. La revisión manual aplicando los criterios vistos en clase "
    "fue imprescindible para detectar y corregir este error."
)

# ── 5. Reflexión final ────────────────────────────────────────────────────────
doc.add_heading("Reflexión final", 1)
doc.add_paragraph(
    "El uso de IA en esta práctica se limitó a tres consultas puntuales sobre la API de "
    "librerías específicas (python-jose, Pydantic v2, SQLAlchemy 2.0), de forma similar a "
    "consultar la documentación oficial pero con respuesta más inmediata. El diseño de la "
    "arquitectura en capas, la definición de los modelos, la lógica de negocio y la "
    "integración con el frontend de la práctica anterior fueron trabajo completamente propio.\n\n"
    "La principal conclusión es que la IA es útil como referencia rápida de sintaxis, pero "
    "requiere una revisión crítica activa: en los tres casos tuve que modificar el código "
    "generado, y en el primero era necesario corregir un error de seguridad que habría "
    "comprometido la aplicación si hubiera pasado desapercibido."
)

out = r"C:\Users\PORTATIL_MSI\Desktop\4 CARRERA\2 Cuatri\Progra Web\BasketShop2\memoria_ia.docx"
doc.save(out)
print("Guardado:", out)
