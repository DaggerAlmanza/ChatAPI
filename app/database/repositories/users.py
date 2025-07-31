from app.config.db_connection import session
from app.database.models import Users as UsersModel
from app.database.repositories.repository import Repository


class User(Repository):

    def __init__(self):
        self.session = session
        self.conn = UsersModel

    def get_by_email(self, email: str) -> dict:
        kwargs = {
            "email": email
        }
        data = self.session.query(self.conn).filter_by(**kwargs).first()
        return data
