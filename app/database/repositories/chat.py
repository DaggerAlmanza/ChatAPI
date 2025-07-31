from app.config.db_connection import session
from app.database.models import Message as MessageModel
from app.database.repositories.repository import Repository


class Chat(Repository):

    def __init__(self):
        self.session = session
        self.conn = MessageModel
