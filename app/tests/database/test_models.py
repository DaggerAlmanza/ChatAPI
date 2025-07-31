from unittest.mock import patch, MagicMock
from datetime import datetime
from app.database.models import Users, Message


@patch('app.database.models.create_engine')
@patch('app.database.models.Base.metadata.create_all')
def test_users_to_json(mock_create_all, mock_engine):
    mock_engine.return_value = MagicMock()

    user = Users()
    user.id = 1
    user.email = "test@example.com"
    user.password_hash = "hashed_password"

    result = user.to_json()

    expected = {
        "id": 1,
        "email": "test@example.com",
        "password_hash": "hashed_password"
    }
    assert result == expected


@patch('app.database.models.create_engine')
@patch('app.database.models.Base.metadata.create_all')
@patch('app.database.models.GeneralHelpers.get_message_id')
@patch('app.database.models.GeneralHelpers.get_datetime')
def test_message_to_json(
    mock_datetime, mock_message_id, mock_create_all, mock_engine
):
    mock_engine.return_value = MagicMock()
    mock_datetime.return_value = datetime(2023, 1, 1, 12, 0, 0)
    mock_message_id.return_value = "msg-123"

    message = Message()
    message.message_id = "msg-123"
    message.session_id = "session-456"
    message.content = "Hello world"
    message.timestamp = datetime(2023, 1, 1, 12, 0, 0)
    message.sender = "user1"
    message.metadata_message = {"type": "text"}

    result = message.to_json()

    expected = {
        "message_id": "msg-123",
        "session_id": "session-456",
        "content": "Hello world",
        "timestamp": "2023-01-01 12:00:00",
        "sender": "user1",
        "metadata": {"type": "text"}
    }
    assert result == expected
