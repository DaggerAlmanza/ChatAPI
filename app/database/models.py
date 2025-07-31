from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import (
    declarative_base,
)

from app.config.constants import (
    DATABASE_URL
)
from app.helpers.util import GeneralHelpers
from sqlalchemy.dialects.sqlite import JSON


Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    def to_json(self, *args, **kwargs):
        return {
            "id": self.id,
            "email": self.email,
            "password_hash": self.password_hash,
        }


class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(
        String, primary_key=True, default=GeneralHelpers.get_message_id
    )
    session_id = Column(String, nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(
        DateTime, nullable=False, default=GeneralHelpers.get_datetime
    )
    sender = Column(String, nullable=False)
    metadata_message = Column(
        JSON, nullable=False,
        comment="Metadatos de procesamiento del mensaje."
    )

    def to_json(self, *args, **kwargs):
        return {
            "message_id": self.message_id,
            "session_id": self.session_id,
            "content": self.content,
            "timestamp": str(self.timestamp),
            "sender": self.sender,
            "metadata": self.metadata_message,
        }


engine = create_engine(
    DATABASE_URL
)
Base.metadata.create_all(engine)
