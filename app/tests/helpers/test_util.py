from unittest.mock import patch, MagicMock
from app.helpers.util import GeneralHelpers


@patch('app.helpers.util.datetime')
def test_get_datetime(mock_datetime):
    mock_datetime.now.return_value.isoformat.return_value = "2023-01-01T12:00:00"
    result = GeneralHelpers.get_datetime()

    assert result == "2023-01-01T12:00:00"


@patch('app.helpers.util.uuid.uuid4')
def test_generate_uuid(mock_uuid):
    mock_uuid.return_value = MagicMock()
    mock_uuid.return_value.__str__ = MagicMock(return_value="test-uuid")
    result = GeneralHelpers.generate_uuid()

    assert result == "test-uuid"


@patch.object(GeneralHelpers, 'generate_uuid')
def test_get_message_id(mock_generate_uuid):
    mock_generate_uuid.return_value = "test-uuid"
    result = GeneralHelpers.get_message_id()

    assert result == "msg-test-uuid"


@patch.object(GeneralHelpers, 'generate_uuid')
def test_get_session_id(mock_generate_uuid):
    mock_generate_uuid.return_value = "test-uuid"
    result = GeneralHelpers.get_session_id()

    assert result == "session-test-uuid"


@patch('app.helpers.util.security.hash_password')
def test_update_user_password(mock_hash_password):
    mock_hash_password.return_value = "hashed_password"
    helper = GeneralHelpers()
    data = {}

    helper.update_user_password(data, "plain_password")

    assert data["password_hash"] == "hashed_password"
    mock_hash_password.assert_called_once_with("plain_password")


def test_the_session_id_is_valid_true():
    valid_session_id = "session-12345678-1234-1234-1234-123456789abc"
    result = GeneralHelpers.the_session_id_is_valid(valid_session_id)

    assert result is True


def test_the_session_id_is_valid_false():
    invalid_session_id = "invalid-session-id"
    result = GeneralHelpers.the_session_id_is_valid(invalid_session_id)

    assert result is False
