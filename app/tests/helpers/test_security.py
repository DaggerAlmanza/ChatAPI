from unittest.mock import patch
from app.helpers.security import Security


@patch('app.helpers.security.bcrypt.hashpw')
@patch('app.helpers.security.bcrypt.gensalt')
def test_hash_password(mock_gensalt, mock_hashpw):
    mock_gensalt.return_value = b"salt"
    mock_hashpw.return_value = b"hashed_password"
    result = Security.hash_password("plain_password")

    assert result == "hashed_password"
    mock_gensalt.assert_called_once_with(rounds=12)
    mock_hashpw.assert_called_once_with(b"plain_password", b"salt")


@patch('app.helpers.security.bcrypt.checkpw')
def test_verify_password_true(mock_checkpw):
    mock_checkpw.return_value = True
    result = Security.verify_password("plain_password", "hashed_password")

    assert result is True
    mock_checkpw.assert_called_once_with(b"plain_password", b"hashed_password")


@patch('app.helpers.security.bcrypt.checkpw')
def test_verify_password_false(mock_checkpw):
    mock_checkpw.return_value = False
    result = Security.verify_password("plain_password", "hashed_password")

    assert result is False


@patch('app.helpers.security.bcrypt.checkpw')
def test_verify_password_exception(mock_checkpw):
    mock_checkpw.side_effect = ValueError("Invalid hash")
    result = Security.verify_password("plain_password", "invalid_hash")

    assert result is False


def test_is_hashed_true():
    hashed_password = "$2b$12$HD93pJSYcOym1JBgmL0Kse5bdsF7bpL6puU4XweyG0Eb6wymy0xBW"
    result = Security.is_hashed(hashed_password)

    assert result is True


def test_is_hashed_false():
    plain_password = "plain_password"
    result = Security.is_hashed(plain_password)

    assert result is False
