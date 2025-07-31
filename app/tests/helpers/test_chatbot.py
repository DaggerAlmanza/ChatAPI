import pytest
from unittest.mock import patch
from app.helpers.chatbot import ChatBot


@pytest.fixture
def chatbot():
    return ChatBot()


def test_process_text(chatbot):
    text = "¡Hola! ¿Cómo estás?"
    result = chatbot.process_text(text)
    assert result == "hola cómo estás"


def test_find_category_saludos(chatbot):
    message = "Hola, buenos días"
    result = chatbot.find_category(message)
    assert result == "saludos"


def test_find_category_despedidas(chatbot):
    message = "Adiós, hasta luego"
    result = chatbot.find_category(message)
    assert result == "despedidas"


def test_find_category_not_found(chatbot):
    message = "mensaje sin patrón conocido"
    result = chatbot.find_category(message)
    assert result is None


@patch('app.helpers.chatbot.random.choice')
def test_get_response_with_category(mock_choice, chatbot):
    mock_choice.return_value = "¡Hola! ¿En qué te puedo ayudar?"

    result = chatbot.get_response("Hola")

    assert result == "¡Hola! ¿En qué te puedo ayudar?"
    mock_choice.assert_called_once()


@patch('app.helpers.chatbot.random.choice')
def test_get_response_default(mock_choice, chatbot):
    mock_choice.return_value = "Interesante. ¿Puedes contarme más sobre eso?"

    result = chatbot.get_response("mensaje desconocido")

    assert result == "Interesante. ¿Puedes contarme más sobre eso?"
    mock_choice.assert_called_once_with(chatbot.responses_default)
