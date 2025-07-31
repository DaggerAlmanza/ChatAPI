# API de Procesamiento de Mensajes de Chat
Esta es una API RESTful simple para el procesamiento de mensajes de chat, construida con FastAPI y SQLite (a través de SQLAlchemy). Está diseñada para ser limpia, mantenible y con una cobertura de pruebas adecuada.

## Características
- Endpoint de Mensajes (POST /api/messages):

    - Recibe mensajes de chat en formato JSON.

    - Valida el formato del mensaje.

    - Procesa mensajes válidos (filtrado de contenido, adición de metadatos).

    - Almacena el mensaje procesado en una base de datos SQLite.

    - Devuelve códigos de estado HTTP y respuestas apropiadas (éxito o error).

- Endpoint de Recuperación de Mensajes (GET /api/messages/{session_id}):

    - Devuelve todos los mensajes para una sesión dada.

    - Soporte para paginación (limit, offset).

    - Permite filtrar por remitente (sender).

- Esquema de Mensaje:

    - message_id (string): Identificador único.

    - session_id (string): Identificador de sesión.

    - content (string): Contenido del mensaje.

    - timestamp (ISO datetime): Marca de tiempo del mensaje.

    - sender (string): Quién envió el mensaje ("user" o "system").

- Procesamiento de Mensajes:

    - Validación de formato.

    - Filtrado simple de contenido inapropiado (palabra "badword").

    - Adición de metadatos (longitud del mensaje, conteo de palabras, processed_at).

- Manejo de Errores:

    - Respuestas de error estructuradas con códigos HTTP apropiados para formato inválido, campos faltantes y errores del servidor.

- Organización del Código:

    - Arquitectura limpia con separación de responsabilidades (controladores, servicios, repositorios, modelos).

    - Inyección de dependencias para la sesión de la base de datos.

- Pruebas:

    - Pruebas unitarias para componentes individuales.

    - Pruebas de integración para los endpoints de la API con Pytest.

    - Cobertura de pruebas objetivo del 80%.

- Documentación:

    - Comentarios en el código.

    - Documentación de la API generada automáticamente por FastAPI (Swagger UI / ReDoc).

Estructura del Proyecto
.
├── app
-   ├── config
-   -   ├── __init__.py
-   -   ├── constants.py
-   -   ├── db_connection.py
-   -   ├── routers.py
-   ├── controllers
-   -   ├── __init__.py
-   -   ├── serializers
-   -   -   ├── __init__.py
-   -   -   ├── autenticacion.py
-   -   -   ├── chat.py
-   -   -   ├── response.py
-   -   -   ├── user.py
-   -   ├── views
-   -   -   ├── __init__.py
-   -   -   ├── autenticacion.py
-   -   -   ├── chat.py
-   -   -   ├── user.py
-   ├── database
-   -   ├── __init__.py
-   -   ├── models.py
-   -   ├── repositories
-   -   -   ├── __init__.py
-   -   -   ├── chat.py
-   -   -   ├── repository.py
-   -   -   ├── user.py
-   ├── helpers
-   -   ├── __init__.py
-   -   ├── chatbot.py
-   -   ├── security.py
-   -   ├── util.py
-   ├── services
-   -   ├── __init__.py
-   -   ├── autenticacion.py
-   -   ├── chat.py
-   -   ├── users.py
-   ├── tests
-   -   ├── __init__.py
-   -   ├── config
-   -   -   ├── __init__.py
-   -   -   ├── test_db_connection.py
-   -   ├── database
-   -   -   ├── __init__.py
-   -   -   ├── test_models.py
-   -   ├── helpers
-   -   ├── __init__.py
-   -   -   ├── __init__.py
-   -   -   ├── test_chatbot.py
-   -   -   ├── test_security.py
-   -   -   ├── test_util.py
├── .env
├── .gitignore
├── README.md
└── requirements.txt

# Configuración y Uso
- Construido
    - Python 3.9+
    - Base de dato: PostgreSQL
    - Pruebas: Pytest
    - Frameworks: FastAPI

# Instalación
Clonar el repositorio:

# Si estás clonando desde un repositorio
```sh
    git clone https://github.com/DaggerAlmanza/ChatAPI.git
```
- Crear un entorno virtual (opcional pero recomendado):

2. Instalar virtualEnv e instalarlo
Linux
```sh
virtualenv -p python3 venv
```
o
```sh
python3 -m venv venv
```

```sh
source venv/bin/activate
```
o
```sh
. venv/bin/activate
```

Windows
```sh
python -m venv venv
```

```sh
venv/Scripts/activate
```
3. Instalar requirements.txt
```sh
pip3 install -r requirements.txt
```

- Ejecutar la Aplicación
Para iniciar el servidor FastAPI, ejecuta el siguiente comando desde el directorio raíz del proyecto:

```sh
uvicorn main:app --reload
```
Esto iniciará el servidor en http://127.0.0.1:8000.

Documentación Interactiva de la API (Swagger UI): http://127.0.0.1:8000/docs

Documentación Alternativa de la API (ReDoc): http://127.0.0.1:8000/redoc

# Endpoints de la API
1. POST /api/messages
- Recibe un nuevo mensaje de chat para su procesamiento y almacenamiento.
- Tenemos un pequeño simulador de chatbot para probar la API.
- Aqui guardamos las respuestas de nuestro sistema.
- URL: /api/messages
- Método: POST
- Tipo de Contenido: application/json

- Cuerpo de la Solicitud (Ejemplo):
```json
{
  "message_id": "msg-123456",
  "session_id": "session-abcdef",
  "content": "Hola, ¿cómo puedo ayudarte hoy?",
  "timestamp": "2023-06-15T14:30:00Z",
  "sender": "system"
}
```
## Respuestas Posibles:

- 201 Created (Éxito):

```json
{
  "status": "success",
  "data": {
    "message_id": "msg-123456",
    "session_id": "session-abcdef",
    "content": "Hola, ¿cómo puedo ayudarte hoy?",
    "timestamp": "2023-06-15T14:30:00Z",
    "sender": "system",
    "metadata": {
      "word_count": 6,
      "character_count": 32,
      "processed_at": "2023-06-15T14:30:01Z"
    }
  }
}
```

- 400 Bad Request (Error de Validación):

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_FORMAT",
    "message": "Formato de mensaje inválido",
    "details": "El campo 'sender' debe ser 'user' o 'system'"
  }
}
```

```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Error de validación de entrada",
    "details": [
      {
        "loc": ["body", "message_id"],
        "msg": "field required",
        "type": "missing"
      }
    ]
  }
}
```

- 422 Unprocessable Entity (Contenido Inapropiado):

```json
{
  "status": "error",
  "error": {
    "code": "INAPPROPRIATE_CONTENT",
    "message": "El mensaje contiene contenido inapropiado",
    "details": "La palabra 'badword' no está permitida."
  }
}
```

- 500 Internal Server Error (Error del Servidor):

```json
{
  "status": "error",
  "error": {
    "code": "INTERNAL_SERVER_ERROR",
    "message": "Ocurrió un error inesperado en el servidor",
    "details": "Detalles del error interno."
  }
}
```
2. GET /api/messages/{session_id}
- Recupera mensajes asociados a una session_id específica.
- URL: /api/messages/{session_id}
- Método: GET

-Parámetros de Ruta:
    - session_id (string, requerido): El ID de la sesión.

- Parámetros de Consulta (Opcionales):
    - limit (int): Número máximo de mensajes a devolver (por defecto: 10).
    - offset (int): Número de mensajes a omitir desde el inicio (por defecto: 0).
    - sender (string): Filtra mensajes por remitente ("user" o "system").

Ejemplo de Solicitud:

GET /api/messages/session-abcdef?limit=5&offset=0&sender=user

Respuestas Posibles:

200 OK (Éxito):

{
  "status": "success",
  "data": [
    {
      "message_id": "msg-123456",
      "session_id": "session-abcdef",
      "content": "Hola, ¿cómo puedo ayudarte hoy?",
      "timestamp": "2023-06-15T14:30:00Z",
      "sender": "system",
      "metadata": {
        "word_count": 6,
        "character_count": 32,
        "processed_at": "2023-06-15T14:30:01Z"
      }
    },
    {
      "message_id": "msg-789012",
      "session_id": "session-abcdef",
      "content": "Necesito información sobre el producto X.",
      "timestamp": "2023-06-15T14:31:00Z",
      "sender": "user",
      "metadata": {
        "word_count": 6,
        "character_count": 38,
        "processed_at": "2023-06-15T14:31:01Z"
      }
    }
  ]
}

404 Not Found (Sesión no encontrada):

{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "Sesión no encontrada",
    "details": "No se encontraron mensajes para la sesión 'non-existent-session'."
  }
}

500 Internal Server Error (Error del Servidor):
(Similar al error 500 de POST)

# Ejecutar Pruebas
Para ejecutar las pruebas unitarias y de integración, asegúrate de tener pytest y httpx instalados (pip install pytest). Luego, ejecuta el siguiente comando desde el directorio raíz del proyecto:
- Ejecuta las pruebas:
```sh
pytest
```

Esto ejecutará todas las pruebas definidas..