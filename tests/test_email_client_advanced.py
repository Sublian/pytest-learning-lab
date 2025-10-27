# tests/test_email_client_advanced.py
import pytest
from src.mailing.email_client import EmailClient

# regla de oro del mocking:
# “Debes parchear donde se usa la función, no donde se define.”
# INCORRECTO
# mocker.patch("src.mailing.email_service.enviar_notificacion")

@pytest.fixture
def mock_envio_exitoso(mocker):
    """Simula una respuesta exitosa desde email_service."""
    mock = mocker.patch("src.mailing.email_client.enviar_notificacion")
    mock.return_value = True
    return mock

@pytest.fixture
def mock_envio_fallido(mocker):
    """Simula una respuesta fallida (False) desde email_service."""
    mock = mocker.patch("src.mailing.email_client.enviar_notificacion")
    mock.return_value = False
    return mock

@pytest.fixture
def mock_envio_error(mocker):
    """Simula un error inesperado lanzando una excepción."""
    mock = mocker.patch("src.mailing.email_client.enviar_notificacion")
    mock.side_effect = Exception("Error de conexión")
    return mock


def test_envio_exitoso(mock_envio_exitoso):
    client = EmailClient()
    assert client.enviar_con_reintento("ok@test.com", "Mensaje") is True


def test_envio_fallido(mock_envio_fallido):
    client = EmailClient()
    assert client.enviar_con_reintento("fail@test.com", "Mensaje") is False


def test_envio_con_excepcion(mock_envio_error):
    client = EmailClient()
    assert  client.enviar_con_reintento("error@test.com", "Mensaje", reintentos=3) is False


def test_simulacion_de_retraso(mocker):
    """Usa time.sleep para medir llamadas con delay simulado."""
    mock_sleep = mocker.patch("time.sleep")
    mock_envio = mocker.patch("src.mailing.email_client.enviar_notificacion")
    # Simula dos fallos y luego éxito
    mock_envio.side_effect = [Exception("API down"), Exception("Timeout"), True]
    
    client = EmailClient(delay=0.5)
    resultado = client.enviar_con_reintento("delay@test.com", "Mensaje", reintentos=3)

    assert resultado is True
    assert mock_sleep.call_count == 3  # se esperaron 3 intentos, con 3 pausas