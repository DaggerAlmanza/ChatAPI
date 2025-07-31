from app.config.constants import (
    CREATED, OK, FORBIDDEN
)
from app.database.repositories.users import (
    User as UsersRepository
)
from app.helpers.security import Security
from app.helpers.util import GeneralHelpers


users_repository = UsersRepository()
security_helpers = Security()
general_helpers = GeneralHelpers()


class UserService:

    def __init__(self):
        self.users_repository = users_repository
        self.security_helpers = security_helpers
        self.general_helpers = general_helpers

    def save(self, data: dict) -> dict:
        self.general_helpers.update_user_password(
            data, data.get("password_hash")
        )
        response = self.users_repository.create(data)
        return {
            "data": response,
            "message":
                "El usuario fue creado"
                if response else
                "El usuario no fue creado",
            "status_code": CREATED if response else OK
        }

    def delete_by_id(self, id: int) -> dict:
        response = self.users_repository.delete(id)
        return {
            "data": response,
            "message":
                "El usuario fue eliminado"
                if response else
                "El usuario no fue eliminado",
            "status_code": OK
        }

    def get_by_id(self, id: int) -> dict:
        response = self.users_repository.get_by_id(id)
        if response:
            response = response.to_json()
        return {
            "data": response if response else {},
            "message":
                "El usuario consultado" if response else "El usuario no existe",
            "status_code": OK
        }

    def get_user_by_email_and_password(self, email: str, password: str) -> dict:
        response = self.users_repository.get_by_email(email)
        if response:
            is_password_correct = self.security_helpers.verify_password(
                password, response.password_hash
            )
            if is_password_correct:
                return response.to_json()
        return {}

    def get_user_with_email(self, email: str) -> dict:
        response = self.users_repository.get_by_email(email)
        if response:
            return response.to_json()
        return {}
