import re
import math

from app.config.constants import (
    BAD_REQUEST,
    CREATED,
    OK,
)
from app.database.repositories.chat import (
    Chat as ChatRepository
)
from app.helpers.util import GeneralHelpers
from app.helpers.chatbot import ChatBot


general_helpers = GeneralHelpers()
chat_repository = ChatRepository()
chatbot_helpers = ChatBot()


class ChatService:

    def __init__(self):
        self.chat_repository = chat_repository
        self.general_helpers = general_helpers
        self.chatbot = chatbot_helpers

    @staticmethod
    def __add_session_id(data: dict):
        if not data.get("session_id"):
            session_id = general_helpers.get_session_id()
            data["session_id"] = session_id

    @staticmethod
    def __count_words(prayer: str):
        sentence = re.sub(r'[^\w\s]', '', prayer)
        words = sentence.split()
        return len(words)

    @staticmethod
    def __get_sender(id: str, sender: str = None):
        if sender:
            return {
                "session_id": id,
                "sender": sender
            }
        return {"session_id": id}

    @staticmethod
    def create_metadata(data: dict):
        metadata = {
            "word_count": ChatService.__count_words(data.get("content")),
            "character_count": len(data.get("content")),
            "processed_at": general_helpers.get_datetime()
        }
        data["metadata_message"] = metadata

    def __create_pagination(self, response: list, limit: int, offset: int):
        current_page = (offset // limit) + 1 if limit > 0 else 1
        total_pages = math.ceil(len(response) / limit) if limit > 0 else 1
        return {
            "limit": limit,
            "offset": offset,
            "page": current_page,
            "total_pages": total_pages,
            "total_items": len(response)
        }

    def create_response_message(self, data: dict) -> dict:
        if data.get("sender") == "user":
            message = self.chatbot.get_response(data.get("content"))
            response_message = {}
            response_message["content"] = message
            response_message["session_id"] = data.get("session_id")
            response_message["sender"] = "system"
            ChatService.create_metadata(response_message)
            return response_message
        return {}

    def save_response_message(self, data: dict):
        response_message = self.create_response_message(data)
        if response_message:
            if not self.chat_repository.create_message(response_message):
                print(
                    "El chatbot no respondio correctamente, por favor responder al cliente"
                )

    def save(self, data: dict) -> dict:
        ChatService.__add_session_id(data)
        if not self.general_helpers.the_session_id_is_valid(
            data.get("session_id")
        ):
            return {
                "status": "error",
                "error": {
                    "code": "INVALID_FORMAT",
                    "message": "Formato de session_id inválido",
                    "details":
                        f"El formato {data.get('session_id')} debe ser de la forma: session-1f6d4f16-3fb0-4ae8-befe-dbd1b1c41e9c"
                    },
                "status_code": BAD_REQUEST
            }
        if data.get("sender") not in ["user", "system"]:
            return {
                "status": "error",
                "error": {
                    "code": "INVALID_FORMAT",
                    "message": "El sender debe ser 'user' o 'system'",
                    "details":
                        "El sender debe ser 'user' o 'system', por favor revisa tus parámetros"
                },
                "status_code": BAD_REQUEST
            }
        ChatService.create_metadata(data)
        response = self.chat_repository.create_message(data)
        if response:
            response = response.to_json()
        self.save_response_message(data)
        return {
            "status": "success",
            "data": response,
            "status_code": CREATED if response else OK,
        }

    def get_by_session_id(
        self, id: str, limit: int = 20, offset: int = 0, sender: str = None
    ) -> list:
        if offset == limit:
            return {
                "status": "error",
                "error": {
                    "code": "INVALID_OFFSET",
                    "message": "El offset no puede ser igual al limit",
                    "details":
                        "El offset no puede ser igual al limit, por favor revisa tus parámetros"
                },
                "status_code": BAD_REQUEST
            }
        if not self.general_helpers.the_session_id_is_valid(id):
            return {
                "status": "error",
                "error": {
                    "code": "INVALID_FORMAT",
                    "message": "Formato de session_id inválido",
                    "details":
                        f"El formato {id} debe ser de la forma: session-1f6d4f16-3fb0-4ae8-befe-dbd1b1c41e9c"
                    },
                "status_code": BAD_REQUEST
            }
        data = ChatService.__get_sender(id, sender)
        response = self.chat_repository.get_all_match(data)
        if response:
            response = [data_json.to_json() for data_json in response]
        pagination = self.__create_pagination(response, limit, offset)
        return {
            "status": "success",
            "data": response[offset:offset + limit] if response else [],
            "message":
                "El chat consultado" if response else "El chat no existe",
            "status_code": OK,
            "pagination": pagination
        }
