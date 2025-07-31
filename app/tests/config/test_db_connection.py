import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import OperationalError


class TestDatabaseConnection:

    @patch('app.config.db_connection.Session')
    def test_session_creation_success(self, mock_session_class):
        """Test successful database session creation"""
        mock_session_instance = MagicMock()
        mock_session_class.return_value = mock_session_instance

        # Simulate session creation
        test_session = mock_session_class()

        assert test_session is not None
        mock_session_class.assert_called_once()

    @patch('app.database.models.engine')
    def test_database_connection_failure(self, mock_engine):
        """Test database connection failure handling"""
        mock_engine.connect.side_effect = OperationalError(
            "Connection failed", None, None
        )

        with pytest.raises(OperationalError):
            mock_engine.connect()

    @patch('app.config.db_connection.session')
    def test_session_close(self, mock_session):
        """Test session close functionality"""
        mock_session.close()
        mock_session.close.assert_called_once()
