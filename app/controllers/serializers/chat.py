from datetime import datetime
from typing import Optional, Literal, Dict, Any

from pydantic import BaseModel, Field, model_validator


class MessageMetadata(BaseModel):
    """
    Modelo Pydantic para los metadatos de un mensaje procesado.
    """
    word_count: int = Field(
        ...,
        description="Número de palabras en el contenido del mensaje."
    )
    character_count: int = Field(
        ...,
        description="Número de caracteres en el contenido del mensaje."
    )
    processed_at: datetime = Field(
        ...,
        description="Marca de tiempo cuando el mensaje fue procesado (formato ISO datetime)."
    )


class MessageCreate(BaseModel):
    session_id: Optional[str] = Field(
        None,
        min_length=1,
        description="Identificador de la sesión del chat."
    )
    content: str = Field(
        ...,
        min_length=1,
        description="Contenido textual del mensaje."
    )
    sender: Literal["user", "system"] = Field(
        ...,
        description="Remitente del mensaje: 'user' o 'system'."
    )

    @model_validator(mode='after')
    def validate_sender_value(self):
        """
        Valida que el campo 'sender' sea 'user' o 'system'.
        """
        if self.sender not in ["user", "system"]:
            raise ValueError("El campo 'sender' debe ser 'user' o 'system'")
        return self

    class Config:
        """Configuración de Pydantic para el modelo."""
        json_schema_extra = {
            "example": {
                "session_id": "session-1f6d4f16-3fb0-4ae8-befe-dbd1b1c41e9c",
                "content": "Hola, ¿cómo puedo ayudarte hoy?",
                "sender": "user"
            }
        }


class MessageResponse(MessageCreate):
    """
    Modelo Pydantic para la respuesta de un mensaje procesado (salida POST y GET).
    Extiende MessageCreate y añade los metadatos.
    """
    metadata: MessageMetadata = Field(..., description="Metadatos adicionales del mensaje procesado.")

    class Config:
        """Configuración de Pydantic para el modelo."""
        json_schema_extra = {
            "example": {
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


class ErrorDetail(BaseModel):
    """
    Modelo Pydantic para los detalles de un error.
    """
    loc: Optional[list[str]] = None
    msg: str
    type: str


class ErrorResponse(BaseModel):
    """
    Modelo Pydantic para una respuesta de error estandarizada.
    """
    status: str = "error"
    error: Dict[str, Any] = Field(..., description="Objeto que contiene el código, mensaje y detalles del error.")

    class Config:
        """Configuración de Pydantic para el modelo."""
        json_schema_extra = {
            "examples": [
                {
                    "status": "error",
                    "error": {
                        "code": "INVALID_FORMAT",
                        "message": "Formato de mensaje inválido",
                        "details": "El campo 'sender' debe ser 'user' o 'system'"
                    }
                },
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
                },
                {
                    "status": "error",
                    "error": {
                        "code": "INAPPROPRIATE_CONTENT",
                        "message": "El mensaje contiene contenido inapropiado",
                        "details": "La palabra 'badword' no está permitida."
                    }
                },
                {
                    "status": "error",
                    "error": {
                        "code": "INTERNAL_SERVER_ERROR",
                        "message": "Ocurrió un error inesperado en el servidor",
                        "details": "Detalles del error interno."
                    }
                }
            ]
        }
