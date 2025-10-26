# tests/test_mock_email_service.py
import pytest
from src.mailing.email_service import enviar_notificacion

@pytest.mark.api
def test_envio_notificacion_mockeado(mocker):
    """Simula una llamada a la API externa sin hacer una solicitud real."""
    mock_post = mocker.patch("src.mailing.email_service.requests.post")
    mock_post.return_value.status_code = 200

    resultado = enviar_notificacion("test@example.com", "Hola desde Pytest!")
    assert resultado is True
    mock_post.assert_called_once()
    

@pytest.mark.parametrize("status,resultado", [
    (200, True),
    (500, False),
    (404, False),
])
def test_envio_notificacion_varios_estados(mocker, status, resultado):
    mock_post = mocker.patch("src.mailing.email_service.requests.post")
    mock_post.return_value.status_code = status
    assert enviar_notificacion("demo@test.com", "Mensaje") == resultado
    
    
@pytest.fixture
def mock_api_externa(mocker):
    mock = mocker.patch("src.mailing.email_service.requests.post")
    mock.return_value.status_code = 200
    return mock

def test_envio_rapido(mock_api_externa):
    assert enviar_notificacion("user@test.com", "Hola mundo!") is True
    
def test_envio_datos_correctos(mocker):
    mock_post = mocker.patch("src.mailing.email_service.requests.post")
    mock_post.return_value.status_code = 200

    enviar_notificacion("demo@correo.com", "Mensaje de prueba")
    mock_post.assert_called_with(
        "https://api.fake-mailer.com/send",
        json={"email": "demo@correo.com", "mensaje": "Mensaje de prueba"}
    )
        