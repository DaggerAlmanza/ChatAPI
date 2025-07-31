import re
import uuid
from datetime import datetime

from app.helpers.security import Security


security = Security()


class GeneralHelpers:

    @staticmethod
    def get_datetime():
        return datetime.now().isoformat()

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())

    @staticmethod
    def get_message_id():
        return f"msg-{GeneralHelpers.generate_uuid()}"

    @staticmethod
    def get_session_id():
        return f"session-{GeneralHelpers.generate_uuid()}"

    def update_user_password(self, data: dict, password: str):
        """
        Actualiza la contraseña de un usuario
        """
        data["password_hash"] = security.hash_password(password)

    @staticmethod
    def the_session_id_is_valid(session_id: str):
        patron = r"^session-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
        if re.match(patron, session_id):
            return True
        return False
