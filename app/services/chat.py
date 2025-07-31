import re

from app.config.constants import (
    BAD_REQUEST,
    CREATED,
    OK,
)
from app.database.repositories.chat import (
    Chat as ChatRepository
)
from app.helpers.util import GeneralHelpers


general_helpers = GeneralHelpers()
chat_repository = ChatRepository()


class ChatService:

    def __init__(self):
        self.chat_repository = chat_repository
        self.general_helpers = general_helpers

    @staticmethod
    def __add_session_id(data: dict):
        if not data.get("session_id"):
            session_id = general_helpers.get_session_id()
            data["session_id"] = session_id

    @staticmethod
    def __add_timestamp(data: dict):
        timestamp = general_helpers.get_datetime()
        data["timestamp"] = timestamp

    @staticmethod
    def __count_words(prayer: str):
        sentence = re.sub(r'[^\w\s]', '', prayer)
        words = sentence.split()
        return len(words)

    @staticmethod
    def create_metadata(data: dict):
        metadata = {
            "word_count": ChatService.__count_words(data.get("content")),
            "character_count": len(data.get("content")),
            "processed_at": general_helpers.get_datetime()
        }
        data["metadata_message"] = metadata

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
        ChatService.create_metadata(data)
        # response = data

        response = self.chat_repository.create_message(data)
        if response:
            response = response.to_json()
        return {
            "status": "success",
            "data": response,
            "status_code": CREATED if response else OK,
        }

    def get_by_session_id(self, id: str) -> list:
        data = {"session_id": id}
        response = self.chat_repository.get_all_match(data)
        if response:
            response = [data_json.to_json() for data_json in response]
        return {
            "status": "success",
            "data": response if response else [],
            "message":
                "El chat consultado" if response else "El chat no existe",
            "status_code": OK
        }
